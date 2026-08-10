import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("AI Resume Analyzer")

# --- INPUT SECTION ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

with col2:
    st.subheader("2. Job Description")
    job_desc = st.text_area("Paste the Job Description here", height=200)

def extract_text(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += " " + extracted
    except Exception:
        pass
    return text

SKILLS_LIST = [
    "python", "c++", "java", "sql", "mongodb", "artificial intelligence",
    "data science", "machine learning", "data analysis", "problem solving",
    "streamlit", "pandas", "numpy", "pytorch", "tensorflow", "scikit-learn",
    "fastapi", "flask", "nlp", "rest api", "communication", "teamwork",
    "docker", "aws"
]

if st.button("Analyze Resume", type="primary"):
    if uploaded_file and job_desc:
        raw_resume = extract_text(uploaded_file).lower()
        clean_resume = " ".join(raw_resume.split())
        job_raw = job_desc.lower()

        required_skills = [skill for skill in SKILLS_LIST if skill in job_raw]

        if not required_skills:
            words = re.findall(r'\b[a-z]{3,}\b', job_raw)
            required_skills = list(set(words))

        matched_skills = []
        missing_skills = []

        for skill in required_skills:
            if skill in clean_resume:
                matched_skills.append(skill.title())
            else:
                missing_skills.append(skill.title())

        total = len(required_skills)
        score = int((len(matched_skills) / total) * 100) if total > 0 else 0

        st.divider()
        st.subheader("🎯 Resume Match Score")
        st.progress(score / 100)
        st.title(f"{score}%")

        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.markdown("### ✅ Matching Skills")
            if matched_skills:
                for skill in matched_skills:
                    st.success(f"• {skill}")
            else:
                st.write("None found")

        with res_col2:
            st.markdown("### ❌ Missing Skills")
            if missing_skills:
                for skill in missing_skills:
                    st.error(f"• {skill}")
            else:
                st.write("None found")

        st.divider()
        st.markdown("### 💡 Recommendations")
        if missing_skills:
            for skill in missing_skills[:3]:
                st.write(f"• Consider adding projects or coursework related to **{skill}**.")
        if "Sql" in missing_skills or "SQL" in missing_skills:
            st.write("• Highlight any database querying or relational database experience.")
        if score >= 70:
            st.write("• Your resume aligns well! Focus on quantifying achievements with metrics.")
        else:
            st.write("• Tailor your experience bullet points to mirror the job description keywords.")
            
    else:
        st.error("Please provide both a resume PDF and a job description.")