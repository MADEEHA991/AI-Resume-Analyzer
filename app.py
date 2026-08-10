import streamlit as st
import pdfplumber
import re
from datetime import datetime


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    padding: 2rem;
}

.title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #666;
    margin-bottom: 25px;
}

.score-card {
    padding: 25px;
    border-radius: 15px;
    background-color: #f5f7fb;
    text-align: center;
    margin-bottom: 20px;
}

.skill-box {
    padding: 10px;
    margin: 5px 0px;
    border-radius: 8px;
}

.footer {
    text-align: center;
    color: #777;
    margin-top: 40px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume against a job description and discover '
    'your matching and missing skills.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SKILL DATABASE
# =========================================================

SKILLS = {
    "python": "Python",
    "java": "Java",
    "c++": "C++",
    "c#": "C#",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "mongodb": "MongoDB",

    "artificial intelligence": "Artificial Intelligence",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "natural language processing": "Natural Language Processing",
    "nlp": "NLP",

    "data science": "Data Science",
    "data analysis": "Data Analysis",
    "data visualization": "Data Visualization",

    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",

    "streamlit": "Streamlit",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "rest api": "REST API",

    "docker": "Docker",
    "kubernetes": "Kubernetes",

    "aws": "AWS",
    "azure": "Azure",
    "google cloud": "Google Cloud",

    "git": "Git",
    "github": "GitHub",

    "power bi": "Power BI",
    "tableau": "Tableau",

    "excel": "Excel",

    "communication": "Communication",
    "teamwork": "Teamwork",
    "leadership": "Leadership",
    "problem solving": "Problem Solving"
}


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_text(file):

    text = ""

    try:
        with pdfplumber.open(file) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += " " + extracted

    except Exception as e:

        st.error("Could not read the PDF file.")

    return text


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):

    text = text.lower()

    # Replace line breaks and multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# SKILL DETECTION
# =========================================================

def contains_skill(text, skill):

    """
    Checks whether a skill appears as a complete term
    instead of matching random parts of words.
    """

    escaped_skill = re.escape(skill)

    pattern = r"(?<![a-zA-Z0-9+#])" + escaped_skill + r"(?![a-zA-Z0-9+#])"

    return re.search(pattern, text, re.IGNORECASE) is not None


def detect_skills(text):

    detected = []

    for skill in SKILLS:

        if contains_skill(text, skill):

            display_name = SKILLS[skill]

            if display_name not in detected:
                detected.append(display_name)

    return detected


# =========================================================
# GET REQUIRED JOB SKILLS
# =========================================================

def extract_job_skills(job_description):

    required = []

    for skill in SKILLS:

        if contains_skill(job_description, skill):

            display_name = SKILLS[skill]

            if display_name not in required:
                required.append(display_name)

    return required


# =========================================================
# CONTACT INFORMATION
# =========================================================

def extract_email(text):

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    emails = re.findall(pattern, text)

    if emails:
        return emails[0]

    return "Not found"


def extract_phone(text):

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    phones = re.findall(pattern, text)

    if phones:
        return phones[0]

    return "Not found"


# =========================================================
# SCORE CALCULATION
# =========================================================

def calculate_score(matched, required):

    if not required:
        return 0

    score = int((len(matched) / len(required)) * 100)

    return min(score, 100)


# =========================================================
# RECOMMENDATIONS
# =========================================================

def generate_recommendations(missing_skills, score):

    recommendations = []

    if missing_skills:

        for skill in missing_skills[:5]:

            recommendations.append(
                f"Consider adding a project, certification, "
                f"coursework, or practical experience related to **{skill}**."
            )

    if score >= 80:

        recommendations.append(
            "Your resume has a strong skill match. "
            "Focus on adding measurable achievements such as percentages, "
            "numbers, accuracy, performance improvements, or project impact."
        )

    elif score >= 50:

        recommendations.append(
            "Your resume has a moderate match. "
            "Tailor your skills and project descriptions to the job requirements."
        )

    else:

        recommendations.append(
            "Your resume has a low skill match. "
            "Consider developing projects around the missing job requirements "
            "before applying."
        )

    recommendations.append(
        "Use clear project descriptions and mention the technologies "
        "you actually used."
    )

    return recommendations


# =========================================================
# REPORT GENERATION
# =========================================================

def generate_report(
    score,
    matched_skills,
    missing_skills,
    email,
    phone,
    recommendations
):

    report = []

    report.append("AI RESUME ANALYZER")
    report.append("=" * 50)

    report.append(
        f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    report.append("")

    report.append(f"RESUME MATCH SCORE: {score}%")

    report.append("")

    report.append("CONTACT INFORMATION")
    report.append("-" * 30)

    report.append(f"Email: {email}")
    report.append(f"Phone: {phone}")

    report.append("")

    report.append("MATCHING SKILLS")
    report.append("-" * 30)

    if matched_skills:

        for skill in matched_skills:
            report.append(f"- {skill}")

    else:
        report.append("None found")

    report.append("")

    report.append("MISSING SKILLS")
    report.append("-" * 30)

    if missing_skills:

        for skill in missing_skills:
            report.append(f"- {skill}")

    else:
        report.append("None")

    report.append("")

    report.append("RECOMMENDATIONS")
    report.append("-" * 30)

    for recommendation in recommendations:

        # Remove Markdown bold markers for text report
        clean_recommendation = recommendation.replace("**", "")

        report.append(f"- {clean_recommendation}")

    report.append("")
    report.append("=" * 50)
    report.append("Generated by AI Resume Analyzer")

    return "\n".join(report)


# =========================================================
# INPUT SECTION
# =========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("1️⃣ Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload your PDF resume",
        type=["pdf"]
    )

with col2:

    st.subheader("2️⃣ Job Description")

    job_desc = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder=(
            "Example: We are looking for a Data Scientist "
            "with Python, SQL, Machine Learning, Pandas..."
        )
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.divider()

analyze_button = st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    if not uploaded_file:

        st.error("❌ Please upload a PDF resume.")

    elif not job_desc.strip():

        st.error("❌ Please paste a job description.")

    else:

        with st.spinner("🔎 Analyzing your resume..."):

            resume_text = extract_text(uploaded_file)

            if not resume_text.strip():

                st.error(
                    "❌ Could not extract text from this PDF. "
                    "Please try a text-based PDF."
                )

            else:

                # Clean text
                clean_resume = clean_text(resume_text)
                clean_job = clean_text(job_desc)

                # Detect skills
                resume_skills = detect_skills(clean_resume)
                required_skills = extract_job_skills(clean_job)

                # Matching and missing
                matched_skills = [
                    skill for skill in required_skills
                    if skill in resume_skills
                ]

                missing_skills = [
                    skill for skill in required_skills
                    if skill not in resume_skills
                ]

                # Score
                score = calculate_score(
                    matched_skills,
                    required_skills
                )

                # Contact
                email = extract_email(resume_text)
                phone = extract_phone(resume_text)

                # Recommendations
                recommendations = generate_recommendations(
                    missing_skills,
                    score
                )


                # =================================================
                # RESULTS
                # =================================================

                st.divider()

                st.header("📊 Resume Analysis Results")


                # =================================================
                # SCORE
                # =================================================

                st.markdown(
                    '<div class="score-card">',
                    unsafe_allow_html=True
                )

                st.subheader("🎯 Resume Match Score")

                st.metric(
                    "Job Skill Match",
                    f"{score}%"
                )

                st.progress(score / 100)

                if score >= 80:

                    st.success(
                        "Excellent match! Your resume contains most "
                        "of the required skills."
                    )

                elif score >= 50:

                    st.warning(
                        "Moderate match. Consider improving the missing skills."
                    )

                else:

                    st.error(
                        "Low match. Your resume needs more alignment "
                        "with the job requirements."
                    )

                st.markdown("</div>", unsafe_allow_html=True)


                # =================================================
                # SUMMARY METRICS
                # =================================================

                m1, m2, m3 = st.columns(3)

                with m1:

                    st.metric(
                        "Required Skills",
                        len(required_skills)
                    )

                with m2:

                    st.metric(
                        "Matched Skills",
                        len(matched_skills)
                    )

                with m3:

                    st.metric(
                        "Missing Skills",
                        len(missing_skills)
                    )


                # =================================================
                # CONTACT INFORMATION
                # =================================================

                st.divider()

                st.subheader("👤 Resume Contact Information")

                c1, c2 = st.columns(2)

                with c1:

                    st.info(f"📧 **Email:** {email}")

                with c2:

                    st.info(f"📱 **Phone:** {phone}")


                # =================================================
                # SKILL ANALYSIS
                # =================================================

                st.divider()

                st.header("🧠 Skill Analysis")

                skill_col1, skill_col2 = st.columns(2)


                # =================================================
                # MATCHED SKILLS
                # =================================================

                with skill_col1:

                    st.subheader("✅ Matching Skills")

                    if matched_skills:

                        for skill in matched_skills:

                            st.success(
                                f"✓ {skill}"
                            )

                    else:

                        st.info(
                            "No required skills were found in your resume."
                        )


                # =================================================
                # MISSING SKILLS
                # =================================================

                with skill_col2:

                    st.subheader("❌ Missing Skills")

                    if missing_skills:

                        for skill in missing_skills:

                            st.error(
                                f"✗ {skill}"
                            )

                    else:

                        st.success(
                            "🎉 No required skills are missing!"
                        )


                # =================================================
                # SKILL CHART
                # =================================================

                st.divider()

                st.subheader("📈 Skill Match Breakdown")

                chart_data = {
                    "Matching Skills": len(matched_skills),
                    "Missing Skills": len(missing_skills)
                }

                st.bar_chart(chart_data)


                # =================================================
                # RECOMMENDATIONS
                # =================================================

                st.divider()

                st.header("💡 Personalized Recommendations")

                for recommendation in recommendations:

                    st.write(
                        f"• {recommendation}"
                    )


                # =================================================
                # JOB SKILLS
                # =================================================

                st.divider()

                st.subheader("📋 Skills Detected in Job Description")

                if required_skills:

                    st.write(
                        ", ".join(required_skills)
                    )

                else:

                    st.warning(
                        "No technical or professional skills from our "
                        "current skill database were detected in the job description."
                    )


                # =================================================
                # DOWNLOAD REPORT
                # =================================================

                st.divider()

                st.subheader("📥 Download Analysis")

                report = generate_report(
                    score,
                    matched_skills,
                    missing_skills,
                    email,
                    phone,
                    recommendations
                )

                st.download_button(
                    label="📄 Download Analysis Report",
                    data=report,
                    file_name="resume_analysis_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )


                # =================================================
                # PRIVACY NOTE
                # =================================================

                st.divider()

                st.caption(
                    "🔒 Privacy note: This application processes the uploaded "
                    "resume during the current session. Avoid uploading resumes "
                    "containing information you do not want processed."
                )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'Built with Python + Streamlit + PDFPlumber'
    '</div>',
    unsafe_allow_html=True
)