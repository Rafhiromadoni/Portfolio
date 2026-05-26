import re
from pathlib import Path

import pandas as pd
import streamlit as st
from pypdf import PdfReader
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Resume Job Match Analyzer",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# PATH CONFIG
# =========================================================
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SAMPLE_RESUME_DIR = DATA_DIR / "sample_resume"
JOB_DESC_DIR = DATA_DIR / "job_descriptions"


# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
    .block-container {
        max-width: 1200px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    .hero {
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        color: white;
        padding: 24px 28px;
        border-radius: 18px;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        font-size: 15px;
        opacity: 0.95;
    }

    .metric-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        min-height: 115px;
    }

    .metric-label {
        color: #6B7280;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #111827;
        font-size: 28px;
        font-weight: 800;
        line-height: 1.2;
    }

    .strong {
        background: #EAF8EE;
        color: #166534;
        padding: 14px 16px;
        border-left: 6px solid #22C55E;
        border-radius: 14px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .moderate {
        background: #FFF7E8;
        color: #92400E;
        padding: 14px 16px;
        border-left: 6px solid #F59E0B;
        border-radius: 14px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .low {
        background: #FDECEC;
        color: #991B1B;
        padding: 14px 16px;
        border-left: 6px solid #EF4444;
        border-radius: 14px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .small-muted {
        color: #6B7280;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">🧠 AI Resume Screening & Multi-Industry Job Match Analyzer</div>
    <div class="hero-subtitle">
        Compare candidate resumes with IT and non-IT job roles using NLP, TF-IDF, cosine similarity,
        skill extraction, and skill gap analysis.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# TEXT EXTRACTION FUNCTIONS
# =========================================================
def extract_text_from_pdf(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text).strip()


def extract_text_from_docx(uploaded_file) -> str:
    document = Document(uploaded_file)
    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text.strip())

    return "\n".join(paragraphs).strip()


def extract_text_from_txt(uploaded_file) -> str:
    return uploaded_file.read().decode("utf-8", errors="ignore").strip()


def extract_text_from_uploaded_file(uploaded_file) -> str:
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    if file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    if file_name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)

    return ""


# =========================================================
# CLEANING AND NLP FUNCTIONS
# =========================================================
def normalize_pdf_spacing(text: str) -> str:
    """
    General text normalization for PDF extraction issues.
    This uses a general rule, not manual keyword replacement.
    """
    text = re.sub(r"([A-Za-z])\s+([A-Za-z]{2,})", r"\1\2", text)
    text = re.sub(r"([A-Za-z])\s+([A-Za-z]{2,})", r"\1\2", text)
    return text


def clean_text(text: str) -> str:
    text = str(text)

    # Normalize hyphenation line breaks: "machine-\nlearning" -> "machine learning"
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1 \2", text)

    # Replace line breaks with spaces
    text = re.sub(r"[\r\n\t]+", " ", text)

    # Normalize common PDF spacing issues using a general rule
    text = normalize_pdf_spacing(text)

    # Lowercase
    text = text.lower()

    # Keep useful symbols for tech terms: c++, c#, .net, next.js
    text = re.sub(r"[^a-z0-9+#.\s/-]", " ", text)

    # Normalize separators
    text = re.sub(r"[/|,;:]+", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def calculate_similarity(text1: str, text2: str) -> float:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1
    )

    matrix = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return float(score)


def calculate_final_match_score(text_similarity: float, skill_match_rate: float) -> float:
    """
    Final score combines:
    - text similarity: overall resume-job relevance
    - skill match rate: direct required skill alignment
    """
    final_score = (0.40 * text_similarity) + (0.60 * skill_match_rate)
    return round(final_score, 2)


def get_match_category(score: float) -> tuple[str, str]:
    if score >= 70:
        return "Strong Match", "strong"
    if score >= 45:
        return "Moderate Match", "moderate"
    return "Low Match", "low"


def extract_skills(text: str, skill_list: list[str]) -> list[str]:
    text_clean = clean_text(text)
    found_skills = []

    for skill in skill_list:
        skill_clean = clean_text(skill)
        pattern = rf"(?<![a-z0-9+#.]){re.escape(skill_clean)}(?![a-z0-9+#.])"

        if re.search(pattern, text_clean):
            found_skills.append(skill)

    return sorted(set(found_skills))


def top_keywords(text: str, top_n: int = 15) -> pd.DataFrame:
    text_clean = clean_text(text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=1000
    )

    matrix = vectorizer.fit_transform([text_clean])
    scores = matrix.toarray()[0]
    terms = vectorizer.get_feature_names_out()

    return pd.DataFrame({
        "keyword": terms,
        "score": scores
    }).sort_values("score", ascending=False).head(top_n)


# =========================================================
# JOB DESCRIPTION PARSER
# =========================================================
def parse_job_file(file_path: Path) -> list[dict]:
    text = file_path.read_text(encoding="utf-8")
    blocks = re.split(r"### ROLE:", text)

    jobs = []

    for block in blocks:
        block = block.strip()

        if not block:
            continue

        role_match = re.match(r"(.+)", block)
        category_match = re.search(r"CATEGORY:\s*(.+)", block)
        description_match = re.search(r"DESCRIPTION:\s*(.+)", block, re.DOTALL)

        role = role_match.group(1).strip() if role_match else "Unknown Role"
        category = category_match.group(1).strip() if category_match else "Uncategorized"
        description = description_match.group(1).strip() if description_match else block

        jobs.append({
            "role": role,
            "category": category,
            "description": description,
            "source_file": file_path.name
        })

    return jobs


def load_all_jobs() -> list[dict]:
    jobs = []

    if not JOB_DESC_DIR.exists():
        return jobs

    for file_path in JOB_DESC_DIR.glob("*.txt"):
        jobs.extend(parse_job_file(file_path))

    return jobs


def load_sample_resumes() -> dict:
    resumes = {}

    main_resume_path = DATA_DIR / "sample_resume.txt"

    if main_resume_path.exists():
        resumes["Main Sample Resume"] = main_resume_path.read_text(encoding="utf-8")

    if SAMPLE_RESUME_DIR.exists():
        for file_path in SAMPLE_RESUME_DIR.glob("*.txt"):
            name = file_path.stem.replace("_", " ").title()
            resumes[name] = file_path.read_text(encoding="utf-8")

    return resumes


# =========================================================
# RECOMMENDATION FUNCTION
# =========================================================
def get_recommendation(
    best_role: str,
    missing_skills: list[str],
    score: float
) -> str:
    if score >= 70:
        base = f"The resume is strongly aligned with the {best_role} role."
    elif score >= 45:
        base = f"The resume has moderate alignment with the {best_role} role."
    else:
        base = f"The resume has low alignment with the {best_role} role."

    if missing_skills:
        missing_text = ", ".join(missing_skills[:8])
        return (
            f"{base} To improve the match, add stronger evidence or experience related to: "
            f"{missing_text}."
        )

    return f"{base} The resume already covers most of the required skills for this role."


# =========================================================
# SKILL DICTIONARY
# =========================================================
skill_list = [
    # Data, analytics, AI
    "python", "sql", "excel", "tableau", "power bi", "looker",
    "data visualization", "dashboard", "machine learning", "deep learning",
    "statistics", "statistical analysis", "pandas", "numpy", "scikit-learn",
    "tensorflow", "keras", "pytorch", "etl", "elt", "data cleaning",
    "data quality", "data warehouse", "bigquery", "snowflake", "redshift",
    "airflow", "dbt", "spark", "hadoop", "business intelligence",
    "reporting", "kpi", "analytics", "exploratory data analysis", "eda",
    "forecasting", "time series", "nlp", "natural language processing",
    "computer vision", "recommendation system", "a/b testing",
    "hypothesis testing", "regression", "classification", "clustering",
    "segmentation", "feature engineering", "model evaluation",
    "xgboost", "random forest", "svd", "rag", "llm", "hugging face",
    "gradio", "shap", "plotly", "bert", "transformer", "yolo", "yolov8",
    "cnn", "lstm", "gru", "bilstm", "qwen", "vision-language model",

    # Software, web, cloud
    "api", "fastapi", "streamlit", "git", "github", "docker", "cloud",
    "aws", "gcp", "azure", "javascript", "typescript", "react", "next.js",
    "laravel", "node.js", "express.js", "postgresql", "mysql", "rest api",
    "html", "css", "tailwind css", "ui/ux", "frontend", "backend",
    "database", "authentication", "deployment",

    # QA and security
    "manual testing", "automation testing", "selenium", "postman",
    "test case", "bug tracking", "quality assurance", "cybersecurity",
    "network security", "siem", "threat analysis", "risk assessment",
    "incident response", "linux",

    # Business and non-IT
    "business analysis", "requirement gathering", "process mapping",
    "documentation", "stakeholder communication", "presentation",
    "problem solving", "communication", "teamwork", "leadership",
    "adaptability", "analytical thinking", "attention to detail",
    "microsoft office", "administration", "data entry", "organization",

    # Marketing and content
    "digital marketing", "social media marketing", "google ads", "seo",
    "content marketing", "campaign analysis", "copywriting", "creativity",
    "content writing", "editing", "storytelling", "audience research",

    # HR
    "recruitment", "interview coordination", "employee relations",
    "hr administration", "onboarding", "training coordination",
    "training", "employee development",

    # Finance
    "financial analysis", "budgeting", "accounting", "financial reporting",
    "variance analysis", "business understanding",

    # Operations, supply chain, project, sales
    "operations analysis", "process improvement", "project coordination",
    "scheduling", "task tracking", "customer communication",
    "customer support", "relationship management", "sales", "negotiation",
    "prospecting", "business development", "supply chain analysis",
    "inventory planning", "logistics", "procurement", "vendor management",
    "public relations", "media relations", "event coordination"
]


# =========================================================
# LOAD DATA
# =========================================================
jobs = load_all_jobs()
sample_resumes = load_sample_resumes()

if not jobs:
    st.error("No job descriptions found. Please add it_jobs.txt and non_it_jobs.txt in data/job_descriptions/.")
    st.stop()

if not sample_resumes:
    st.error("No sample resumes found. Please add sample_resume.txt or files in data/sample_resume/.")
    st.stop()


# =========================================================
# ANALYSIS FUNCTIONS
# =========================================================
def run_job_match_analysis(resume_text: str, job_scope: str, jobs: list[dict]) -> pd.DataFrame:
    if job_scope == "IT Jobs Only":
        selected_jobs = [
            job for job in jobs
            if job["source_file"] == "it_jobs.txt"
        ]
    elif job_scope == "Non-IT Jobs Only":
        selected_jobs = [
            job for job in jobs
            if job["source_file"] == "non_it_jobs.txt"
        ]
    else:
        selected_jobs = jobs

    resume_clean = clean_text(resume_text)
    resume_skills = extract_skills(resume_text, skill_list)

    results = []

    for job in selected_jobs:
        jd_clean = clean_text(job["description"])
        text_similarity = calculate_similarity(resume_clean, jd_clean) * 100

        jd_skills = extract_skills(job["description"], skill_list)
        matched_skills = sorted(set(resume_skills).intersection(set(jd_skills)))
        missing_skills = sorted(set(jd_skills).difference(set(resume_skills)))

        skill_match_rate = (
            len(matched_skills) / len(jd_skills) * 100
            if jd_skills else 0
        )

        final_match_score = calculate_final_match_score(
            text_similarity,
            skill_match_rate
        )

        match_category, _ = get_match_category(final_match_score)

        results.append({
            "role": job["role"],
            "category": job["category"],
            "match_score": final_match_score,
            "text_similarity": round(text_similarity, 2),
            "skill_match_rate": round(skill_match_rate, 2),
            "matched_skill_count": len(matched_skills),
            "missing_skill_count": len(missing_skills),
            "match_category": match_category,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "description": job["description"]
        })

    return pd.DataFrame(results).sort_values(
        by=["match_score", "skill_match_rate", "text_similarity"],
        ascending=False
    ).reset_index(drop=True)


def display_match_result(result_df: pd.DataFrame):
    best = result_df.iloc[0]
    _, best_category_class = get_match_category(best["match_score"])

    recommendation = get_recommendation(
        best_role=best["role"],
        missing_skills=best["missing_skills"],
        score=best["match_score"]
    )

    st.subheader("Multi-Industry Job Match Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Best Fit Role</div>
            <div class="metric-value">{best["role"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Final Match Score</div>
            <div class="metric-value">{best["match_score"]}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Skill Match Rate</div>
            <div class="metric-value">{best["skill_match_rate"]}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        f"<div class='{best_category_class}'>Match Category: {best['match_category']}</div>",
        unsafe_allow_html=True
    )

    st.info(recommendation)

    st.markdown("### Top Matching Roles")

    display_df = result_df[[
        "role",
        "category",
        "match_score",
        "text_similarity",
        "skill_match_rate",
        "matched_skill_count",
        "missing_skill_count",
        "match_category"
    ]].head(10)

    st.dataframe(display_df, use_container_width=True)

    st.bar_chart(
        display_df.set_index("role")[["match_score", "skill_match_rate", "text_similarity"]]
    )

    st.markdown("### Skill Gap for Best Fit Role")

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("#### Matched Skills")
        if best["matched_skills"]:
            st.success(", ".join(best["matched_skills"]))
        else:
            st.warning("No matched skills detected.")

    with col5:
        st.markdown("#### Missing Skills")
        if best["missing_skills"]:
            st.error(", ".join(best["missing_skills"]))
        else:
            st.success("No missing skills detected.")

    with st.expander("View Top Keywords from Best Fit Job Description"):
        keyword_df = top_keywords(best["description"], top_n=15)
        st.dataframe(keyword_df, use_container_width=True)
        st.bar_chart(keyword_df.set_index("keyword"))

    with st.expander("View Full Ranking"):
        st.dataframe(
            result_df.drop(columns=["description"]),
            use_container_width=True
        )

    with st.expander("View Score Explanation"):
        st.markdown("""
        **Final Match Score** is calculated using:

        ```text
        Final Match Score = 40% Text Similarity + 60% Skill Match Rate
        ```

        - **Text Similarity** measures overall relevance between resume and job description using TF-IDF and cosine similarity.
        - **Skill Match Rate** measures direct alignment between detected resume skills and required job skills.
        """)


# =========================================================
# PAGE NAVIGATION USING SESSION STATE
# =========================================================
pages = ["📄 Input", "📊 Match Result", "ℹ️ Guide"]

if "active_page" not in st.session_state:
    st.session_state.active_page = "📄 Input"

if "result_df" not in st.session_state:
    st.session_state.result_df = None

if "last_resume_text" not in st.session_state:
    st.session_state.last_resume_text = ""

page = st.radio(
    "Navigation",
    pages,
    horizontal=True,
    label_visibility="collapsed",
    index=pages.index(st.session_state.active_page)
)

st.session_state.active_page = page


# =========================================================
# INPUT PAGE
# =========================================================
if st.session_state.active_page == "📄 Input":
    st.subheader("Candidate Resume Input")

    input_mode = st.radio(
        "Choose input mode",
        ["Use sample resume", "Upload resume file", "Paste custom resume"],
        horizontal=True
    )

    resume_text = ""

    if input_mode == "Use sample resume":
        selected_resume_name = st.selectbox(
            "Select sample resume",
            list(sample_resumes.keys())
        )
        resume_text = sample_resumes[selected_resume_name]

    elif input_mode == "Upload resume file":
        uploaded_resume = st.file_uploader(
            "Upload Resume / CV",
            type=["pdf", "docx", "txt"]
        )

        if uploaded_resume is not None:
            try:
                resume_text = extract_text_from_uploaded_file(uploaded_resume)

                if resume_text:
                    st.success(f"Resume file uploaded successfully: {uploaded_resume.name}")
                else:
                    st.warning("The file was uploaded, but no readable text was found.")

            except Exception as error:
                st.error(f"Failed to read uploaded file: {error}")
                resume_text = ""

    else:
        resume_text = ""

    resume_text = st.text_area(
        "Resume / CV Text",
        value=resume_text,
        height=320,
        placeholder="Paste resume text here or upload a PDF/DOCX/TXT resume."
    )

    job_scope = st.radio(
        "Job matching scope",
        ["All Jobs", "IT Jobs Only", "Non-IT Jobs Only"],
        horizontal=True
    )

    analyze_btn = st.button(
        "🚀 Analyze Multi-Job Match",
        use_container_width=True
    )

    if analyze_btn:
        if not resume_text.strip():
            st.error("Please provide resume text first.")
        else:
            result_df = run_job_match_analysis(
                resume_text=resume_text,
                job_scope=job_scope,
                jobs=jobs
            )

            st.session_state.result_df = result_df
            st.session_state.last_resume_text = resume_text
            st.session_state.active_page = "📊 Match Result"
            st.rerun()


# =========================================================
# MATCH RESULT PAGE
# =========================================================
elif st.session_state.active_page == "📊 Match Result":
    if st.session_state.result_df is not None:
        display_match_result(st.session_state.result_df)
    else:
        st.info("Please run the analysis from the Input page first.")


# =========================================================
# GUIDE PAGE
# =========================================================
elif st.session_state.active_page == "ℹ️ Guide":
    st.subheader("How This App Works")

    st.markdown("""
    This app compares a candidate resume with multiple IT and non-IT job descriptions.

    **Input options:**
    - Use sample resume
    - Upload resume file in PDF, DOCX, or TXT format
    - Paste custom resume text manually

    **Main steps:**
    1. Extract resume text.
    2. Load multiple job descriptions from `it_jobs.txt` and `non_it_jobs.txt`.
    3. Clean and normalize text.
    4. Convert resume and job descriptions into TF-IDF vectors.
    5. Calculate cosine similarity.
    6. Extract matched and missing skills.
    7. Calculate final match score.
    8. Rank job roles and generate recommendation.

    **Final score formula:**

    ```text
    Final Match Score = 40% Text Similarity + 60% Skill Match Rate
    ```

    **Match category:**
    - Strong Match: score >= 70%
    - Moderate Match: score 45% - 69%
    - Low Match: score < 45%

    **Use cases:**
    - Resume screening
    - Job role recommendation
    - Career fit analysis
    - Skill gap analysis

    **Important note:**
    This app is a decision-support tool, not a replacement for human recruitment judgment.
    """)
