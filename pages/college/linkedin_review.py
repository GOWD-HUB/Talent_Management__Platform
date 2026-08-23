# ==========================================================
# TALENTSPHERE ELEVATE
# LINKEDIN PDF REVIEW
# pages/college/linkedin_review.py
# ==========================================================

import re
from io import BytesIO

import streamlit as st
from pypdf import PdfReader

from styles.college.theme import apply_college_theme


# ==========================================================
# SKILL KEYWORDS
# ==========================================================

TECHNICAL_SKILLS = [

    # Programming
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "Go",
    "Rust",
    "PHP",
    "Kotlin",
    "Swift",

    # Frontend
    "HTML",
    "CSS",
    "React",
    "React.js",
    "Angular",
    "Vue",
    "Bootstrap",
    "Tailwind",
    "Material UI",

    # Backend
    "Node.js",
    "Express",
    "FastAPI",
    "Flask",
    "Django",
    "Spring Boot",

    # Databases
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQLite",
    "Oracle",
    "Redis",

    # Data / AI
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "AI",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "OpenCV",

    # DevOps / Cloud
    "Git",
    "GitHub",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Jenkins",
    "CI/CD",
    "Linux",

    # CS Fundamentals
    "Data Structures",
    "DSA",
    "Algorithms",
    "OOP",
    "DBMS",
    "Operating Systems",
    "Computer Networks",

    # Tools
    "Postman",
    "VS Code",
    "Jupyter Notebook",
    "Power BI",
    "Tableau",
    "Excel",

    # Other
    "REST API",
    "REST APIs",
    "API",
    "JWT",
    "Microservices",
]


SOFT_SKILLS = [
    "Communication",
    "Leadership",
    "Teamwork",
    "Problem Solving",
    "Time Management",
    "Adaptability",
    "Critical Thinking",
    "Creativity",
    "Decision Making",
    "Collaboration",
]


# ==========================================================
# HELPER: SAFE SCORE
# ==========================================================

def clamp_score(value):

    try:
        value = int(value)
    except Exception:
        value = 0

    return max(
        0,
        min(
            100,
            value
        )
    )


# ==========================================================
# PDF TEXT EXTRACTION
# ==========================================================

def extract_pdf_text(uploaded_file):

    try:

        uploaded_file.seek(0)

        reader = PdfReader(
            BytesIO(
                uploaded_file.read()
            )
        )

        pages = []

        for page in reader.pages:

            text = (
                page.extract_text()
                or ""
            )

            if text.strip():
                pages.append(
                    text.strip()
                )

        return "\n".join(
            pages
        ).strip()

    except Exception as error:

        raise RuntimeError(
            f"Unable to read PDF: {error}"
        )


# ==========================================================
# NORMALIZE TEXT
# ==========================================================

def normalize_text(text):

    return re.sub(
        r"\s+",
        " ",
        str(text or "")
    ).strip()


# ==========================================================
# SECTION DETECTION
# ==========================================================

def detect_section(
    text,
    keywords,
):

    text_lower = text.lower()

    return any(
        keyword.lower()
        in text_lower
        for keyword in keywords
    )


# ==========================================================
# DETECT LINKEDIN SECTIONS
# ==========================================================

def detect_sections(text):

    sections = {

        "about": detect_section(
            text,
            [
                "about",
                "summary",
            ]
        ),

        "experience": detect_section(
            text,
            [
                "experience",
                "employment",
                "work experience",
            ]
        ),

        "education": detect_section(
            text,
            [
                "education",
                "university",
                "college",
                "bachelor",
                "b.tech",
                "btech",
                "degree",
            ]
        ),

        "skills": detect_section(
            text,
            [
                "skills",
                "top skills",
            ]
        ),

        "projects": detect_section(
            text,
            [
                "projects",
                "project",
            ]
        ),

        "certifications": detect_section(
            text,
            [
                "licenses & certifications",
                "licenses and certifications",
                "certifications",
                "certification",
            ]
        ),

        "achievements": detect_section(
            text,
            [
                "achievements",
                "honors",
                "awards",
                "accomplishments",
            ]
        ),

        "contact": detect_section(
            text,
            [
                "linkedin.com",
                "github.com",
                "@gmail.com",
                "@outlook.com",
            ]
        ),
    }

    return sections


# ==========================================================
# DETECT SKILLS
# ==========================================================

def detect_skills(
    text,
    skill_bank,
):

    text_lower = text.lower()

    detected = []

    for skill in skill_bank:

        pattern = (
            r"(?<!\w)"
            + re.escape(
                skill.lower()
            )
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text_lower
        ):

            detected.append(
                skill
            )

    # Remove duplicate synonyms
    unique = []

    seen = set()

    for skill in detected:

        normalized = (
            skill.lower()
            .replace(
                ".",
                ""
            )
            .replace(
                " ",
                ""
            )
        )

        if normalized not in seen:

            seen.add(
                normalized
            )

            unique.append(
                skill
            )

    return unique


# ==========================================================
# EMAIL DETECTION
# ==========================================================

def detect_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return (
        match.group(0)
        if match
        else ""
    )


# ==========================================================
# URL DETECTION
# ==========================================================

def detect_urls(text):

    urls = re.findall(
        r"https?://[^\s]+|www\.[^\s]+",
        text
    )

    clean_urls = []

    for url in urls:

        url = url.rstrip(
            ".,);]"
        )

        if url not in clean_urls:
            clean_urls.append(
                url
            )

    return clean_urls


# ==========================================================
# PROFILE NAME
# ==========================================================

def detect_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return "LinkedIn Profile"

    for line in lines[:8]:

        # Avoid LinkedIn boilerplate headings
        invalid = [
            "linkedin",
            "contact",
            "experience",
            "education",
            "skills",
        ]

        if any(
            word in line.lower()
            for word in invalid
        ):
            continue

        if (
            2 <= len(line.split()) <= 5
            and len(line) <= 60
        ):
            return line

    return "LinkedIn Profile"


# ==========================================================
# PROFILE HEADLINE
# ==========================================================

def detect_headline(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if len(lines) < 2:
        return ""

    for line in lines[1:10]:

        line_lower = line.lower()

        invalid_words = [
            "contact info",
            "connections",
            "followers",
            "linkedin",
            "experience",
            "education",
        ]

        if any(
            word in line_lower
            for word in invalid_words
        ):
            continue

        if (
            10 <= len(line) <= 160
        ):
            return line

    return ""


# ==========================================================
# SCORE CALCULATION
# ==========================================================

def calculate_scores(
    text,
    sections,
    technical_skills,
    soft_skills,
):

    # ------------------------------------------------------
    # PROFILE SCORE
    # ------------------------------------------------------

    profile_score = 0

    email = detect_email(
        text
    )

    urls = detect_urls(
        text
    )

    headline = detect_headline(
        text
    )

    if email:
        profile_score += 25

    if urls:
        profile_score += 20

    if headline:
        profile_score += 30

    if len(
        normalize_text(
            text
        )
    ) > 500:
        profile_score += 25

    profile_score = clamp_score(
        profile_score
    )


    # ------------------------------------------------------
    # ABOUT SCORE
    # ------------------------------------------------------

    about_score = (
        100
        if sections[
            "about"
        ]
        else 25
    )


    # ------------------------------------------------------
    # EXPERIENCE SCORE
    # ------------------------------------------------------

    if sections[
        "experience"
    ]:

        experience_score = 100

    elif sections[
        "projects"
    ]:

        experience_score = 55

    else:

        experience_score = 20


    # ------------------------------------------------------
    # EDUCATION SCORE
    # ------------------------------------------------------

    education_score = (
        100
        if sections[
            "education"
        ]
        else 20
    )


    # ------------------------------------------------------
    # SKILL SCORE
    # ------------------------------------------------------

    technical_count = len(
        technical_skills
    )

    soft_count = len(
        soft_skills
    )

    skill_score = min(
        100,
        (
            technical_count * 5
            +
            soft_count * 5
        )
    )


    # ------------------------------------------------------
    # PROJECT SCORE
    # ------------------------------------------------------

    project_score = (
        100
        if sections[
            "projects"
        ]
        else 25
    )


    # ------------------------------------------------------
    # CERTIFICATION SCORE
    # ------------------------------------------------------

    certification_score = (
        100
        if sections[
            "certifications"
        ]
        else 30
    )


    # ------------------------------------------------------
    # OVERALL SCORE
    # ------------------------------------------------------

    overall = round(

        profile_score
        * 0.15

        +

        about_score
        * 0.15

        +

        experience_score
        * 0.20

        +

        education_score
        * 0.10

        +

        skill_score
        * 0.20

        +

        project_score
        * 0.10

        +

        certification_score
        * 0.10

    )

    return {

        "overall":
            clamp_score(
                overall
            ),

        "profile":
            clamp_score(
                profile_score
            ),

        "about":
            clamp_score(
                about_score
            ),

        "experience":
            clamp_score(
                experience_score
            ),

        "education":
            clamp_score(
                education_score
            ),

        "skills":
            clamp_score(
                skill_score
            ),

        "projects":
            clamp_score(
                project_score
            ),

        "certifications":
            clamp_score(
                certification_score
            ),
    }


# ==========================================================
# BUILD STRENGTHS
# ==========================================================

def build_strengths(
    sections,
    technical_skills,
    soft_skills,
    email,
    urls,
):

    strengths = []

    if sections[
        "education"
    ]:

        strengths.append(
            "Education information is clearly represented."
        )

    if sections[
        "experience"
    ]:

        strengths.append(
            "Experience or internship information is available."
        )

    if sections[
        "projects"
    ]:

        strengths.append(
            "Projects provide practical evidence of your skills."
        )

    if sections[
        "certifications"
    ]:

        strengths.append(
            "Certifications strengthen your professional credibility."
        )

    if len(
        technical_skills
    ) >= 8:

        strengths.append(
            "Strong range of technical skills detected."
        )

    elif len(
        technical_skills
    ) >= 4:

        strengths.append(
            "Good technical skill foundation detected."
        )

    if soft_skills:

        strengths.append(
            "Professional soft skills are visible in the profile."
        )

    if email:

        strengths.append(
            "Professional contact information was detected."
        )

    if urls:

        strengths.append(
            "Professional links are included in the profile."
        )

    return strengths


# ==========================================================
# BUILD RECOMMENDATIONS
# ==========================================================

def build_recommendations(
    sections,
    technical_skills,
    soft_skills,
    email,
    urls,
):

    recommendations = []

    if not sections[
        "about"
    ]:

        recommendations.append(
            "Add a strong LinkedIn About section of approximately "
            "4–6 lines covering your education, key skills, "
            "projects and target career."
        )

    if not sections[
        "experience"
    ]:

        recommendations.append(
            "Add internships, training, volunteering or practical "
            "experience to strengthen recruiter confidence."
        )

    if not sections[
        "projects"
    ]:

        recommendations.append(
            "Add your strongest academic and personal projects "
            "with technologies, features and your contribution."
        )

    if not sections[
        "certifications"
    ]:

        recommendations.append(
            "Add relevant certifications from recognized platforms "
            "such as NPTEL, Infosys Springboard, Google, Microsoft or Coursera."
        )

    if len(
        technical_skills
    ) < 8:

        recommendations.append(
            "Increase the Skills section with role-relevant technical "
            "skills. Aim for at least 8–12 strong skills."
        )

    if not soft_skills:

        recommendations.append(
            "Include professional skills such as communication, "
            "teamwork, adaptability and problem solving."
        )

    if not email:

        recommendations.append(
            "Ensure your professional contact email is visible."
        )

    if not urls:

        recommendations.append(
            "Add GitHub, portfolio or other professional links."
        )

    recommendations.append(
        "Use measurable impact in project and internship descriptions, "
        "for example: improved accuracy by 15% or reduced processing time."
    )

    recommendations.append(
        "Use keywords related to your target job role so recruiters "
        "can discover your profile more easily."
    )

    recommendations.append(
        "Keep your headline specific, for example: "
        "'CSE AI & ML Student | Python | MERN Stack | Machine Learning'."
    )

    return recommendations


# ==========================================================
# ANALYZE PDF
# ==========================================================

def analyze_linkedin_pdf(
    uploaded_file
):

    text = extract_pdf_text(
        uploaded_file
    )

    if not text:

        return {
            "success": False,
            "error": (
                "No readable text was found in this PDF. "
                "Please upload the LinkedIn PDF exported directly "
                "from your LinkedIn profile."
            ),
        }

    sections = detect_sections(
        text
    )

    technical_skills = detect_skills(
        text,
        TECHNICAL_SKILLS,
    )

    soft_skills = detect_skills(
        text,
        SOFT_SKILLS,
    )

    email = detect_email(
        text
    )

    urls = detect_urls(
        text
    )

    name = detect_name(
        text
    )

    headline = detect_headline(
        text
    )

    scores = calculate_scores(
        text,
        sections,
        technical_skills,
        soft_skills,
    )

    strengths = build_strengths(
        sections,
        technical_skills,
        soft_skills,
        email,
        urls,
    )

    recommendations = (
        build_recommendations(
            sections,
            technical_skills,
            soft_skills,
            email,
            urls,
        )
    )

    return {

        "success":
            True,

        "text":
            text,

        "name":
            name,

        "headline":
            headline,

        "email":
            email,

        "urls":
            urls,

        "sections":
            sections,

        "technical_skills":
            technical_skills,

        "soft_skills":
            soft_skills,

        "scores":
            scores,

        "strengths":
            strengths,

        "recommendations":
            recommendations,
    }


# ==========================================================
# LABEL
# ==========================================================

def score_label(
    score
):

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Strong"

    if score >= 55:
        return "Good"

    if score >= 40:
        return "Developing"

    return "Needs Improvement"


# ==========================================================
# PAGE
# ==========================================================

def render():

    apply_college_theme()


    # ======================================================
    # HERO
    # ======================================================

    st.html(
        """<div class="college-hero">

            <div class="college-hero-badge">
                💼 LINKEDIN PDF ANALYZER
            </div>

            <div class="college-hero-title">
                LinkedIn Profile Review
            </div>

            <div class="college-hero-description">
                Upload your LinkedIn profile PDF and TalentSphere
                will evaluate your professional presence, skills,
                education, experience, projects, certifications
                and recruiter readiness.
            </div>

        </div>"""
    )


    # ======================================================
    # UPLOAD AREA
    # ======================================================

    st.html(
        """<div class="college-section-header">

            <div>

                <div class="college-section-title">
                    📄 Upload LinkedIn Profile
                </div>

                <div class="college-section-subtitle">
                    Upload the PDF exported from your LinkedIn profile.
                </div>

            </div>

            <div class="college-section-tag">
                PDF Analysis
            </div>

        </div>"""
    )


    linkedin_pdf = st.file_uploader(

        "Upload LinkedIn Profile PDF",

        type=[
            "pdf"
        ],

        key="linkedin_profile_pdf",

        help=(
            "Upload the PDF version of your LinkedIn profile."
        ),
    )


    if linkedin_pdf:

        size_kb = round(
            linkedin_pdf.size
            / 1024,
            1,
        )


        col1, col2 = st.columns(
            [
                4,
                1,
            ]
        )


        with col1:

            st.success(
                f"✅ {linkedin_pdf.name}"
            )


        with col2:

            st.metric(
                "File Size",
                f"{size_kb} KB",
            )


    analyze_button = st.button(

        "💼 Analyze LinkedIn PDF",

        type="primary",

        use_container_width=True,

        key="analyze_linkedin_pdf",

    )


    # ======================================================
    # ANALYSIS
    # ======================================================

    if analyze_button:

        if linkedin_pdf is None:

            st.warning(
                "Please upload your LinkedIn profile PDF first."
            )

            return


        with st.spinner(
            "Analyzing LinkedIn profile..."
        ):

            try:

                result = (
                    analyze_linkedin_pdf(
                        linkedin_pdf
                    )
                )

            except Exception as error:

                st.error(
                    f"Unable to analyze LinkedIn PDF: {error}"
                )

                return


        if not result.get(
            "success"
        ):

            st.error(
                result.get(
                    "error",
                    "Unable to analyze PDF."
                )
            )

            return


        st.session_state[
            "linkedin_pdf_analysis"
        ] = result


    # ======================================================
    # RESULT
    # ======================================================

    result = st.session_state.get(
        "linkedin_pdf_analysis"
    )


    if not result:

        st.info(
            "👆 Upload your LinkedIn Profile PDF and click "
            "**Analyze LinkedIn PDF**."
        )

        return


    scores = result[
        "scores"
    ]

    sections = result[
        "sections"
    ]

    technical_skills = result[
        "technical_skills"
    ]

    soft_skills = result[
        "soft_skills"
    ]

    overall = scores[
        "overall"
    ]


    # ======================================================
    # PROFILE SUMMARY
    # ======================================================

    st.html(
        """<div class="college-section-header">

            <div>

                <div class="college-section-title">
                    👤 Profile Overview
                </div>

                <div class="college-section-subtitle">
                    Information detected from your LinkedIn PDF.
                </div>

            </div>

        </div>"""
    )


    st.markdown(
        f"### {result['name']}"
    )


    if result[
        "headline"
    ]:

        st.caption(
            result[
                "headline"
            ]
        )


    if result[
        "email"
    ]:

        st.write(
            f"📧 {result['email']}"
        )


    # ======================================================
    # TOP METRICS
    # ======================================================

    section_count = sum(
        1
        for value in sections.values()
        if value
    )


    st.html(
        f"""<div class="college-metric-grid">

            <div class="college-metric-card">

                <div class="college-metric-icon">
                    💼
                </div>

                <div class="college-metric-label">
                    LINKEDIN SCORE
                </div>

                <div class="college-metric-value">
                    {overall}%
                </div>

                <div class="college-metric-caption">
                    {score_label(overall)} profile
                </div>

            </div>


            <div class="college-metric-card">

                <div class="college-metric-icon">
                    📑
                </div>

                <div class="college-metric-label">
                    PROFILE SECTIONS
                </div>

                <div class="college-metric-value">
                    {section_count}/8
                </div>

                <div class="college-metric-caption">
                    Sections detected
                </div>

            </div>


            <div class="college-metric-card">

                <div class="college-metric-icon">
                    💻
                </div>

                <div class="college-metric-label">
                    TECHNICAL SKILLS
                </div>

                <div class="college-metric-value">
                    {len(technical_skills)}
                </div>

                <div class="college-metric-caption">
                    Skills detected
                </div>

            </div>


            <div class="college-metric-card">

                <div class="college-metric-icon">
                    🤝
                </div>

                <div class="college-metric-label">
                    SOFT SKILLS
                </div>

                <div class="college-metric-value">
                    {len(soft_skills)}
                </div>

                <div class="college-metric-caption">
                    Professional skills
                </div>

            </div>

        </div>"""
    )


    st.progress(
        overall / 100
    )


    # ======================================================
    # SCORE BREAKDOWN
    # ======================================================

    st.html(
        """<div class="college-section-header">

            <div>

                <div class="college-section-title">
                    📊 LinkedIn Score Breakdown
                </div>

                <div class="college-section-subtitle">
                    See how each section contributes to your profile.
                </div>

            </div>

        </div>"""
    )


    score_items = [

        (
            "👤 Profile Completeness",
            scores[
                "profile"
            ],
        ),

        (
            "📝 About Section",
            scores[
                "about"
            ],
        ),

        (
            "💼 Experience",
            scores[
                "experience"
            ],
        ),

        (
            "🎓 Education",
            scores[
                "education"
            ],
        ),

        (
            "💻 Skills",
            scores[
                "skills"
            ],
        ),

        (
            "🚀 Projects",
            scores[
                "projects"
            ],
        ),

        (
            "🏅 Certifications",
            scores[
                "certifications"
            ],
        ),

    ]


    for label, score in score_items:

        c1, c2 = st.columns(
            [
                5,
                1
            ]
        )


        with c1:

            st.markdown(
                f"**{label}**"
            )


        with c2:

            st.markdown(
                f"**{score}%**"
            )


        st.progress(
            score / 100
        )


    # ======================================================
    # SECTION STATUS
    # ======================================================

    st.html(
        """<div class="college-section-header">

            <div>

                <div class="college-section-title">
                    📑 Profile Sections
                </div>

                <div class="college-section-subtitle">
                    Sections identified from your LinkedIn PDF.
                </div>

            </div>

        </div>"""
    )


    section_labels = {

        "about":
            "About",

        "experience":
            "Experience",

        "education":
            "Education",

        "skills":
            "Skills",

        "projects":
            "Projects",

        "certifications":
            "Certifications",

        "achievements":
            "Achievements",

        "contact":
            "Contact / Links",
    }


    rows = list(
        section_labels.items()
    )


    for start in range(
        0,
        len(rows),
        4,
    ):

        chunk = rows[
            start:start + 4
        ]

        columns = st.columns(
            len(chunk)
        )


        for column, (
            key,
            label,
        ) in zip(
            columns,
            chunk,
        ):

            with column:

                status = (
                    "✅ Added"
                    if sections[
                        key
                    ]
                    else "❌ Missing"
                )


                st.metric(
                    label,
                    status
                )


    # ======================================================
    # TECHNICAL SKILLS
    # ======================================================

    st.html(
        """<div class="college-section-header">

            <div>

                <div class="college-section-title">
                    💻 Detected Technical Skills
                </div>

                <div class="college-section-subtitle">
                    Technologies and technical keywords identified
                    from your LinkedIn profile.
                </div>

            </div>

        </div>"""
    )


    if technical_skills:

        skills_html = "".join(

            f"""<span style="
                display:inline-block;
                background:#eff6ff;
                border:1px solid #dbeafe;
                color:#1d4ed8;
                padding:7px 12px;
                border-radius:999px;
                margin:4px;
                font-size:12px;
                font-weight:700;
            ">
                {skill}
            </span>"""

            for skill in technical_skills

        )


        st.html(
            f"""<div style="
                background:#ffffff;
                border:1px solid #e2e8f0;
                border-radius:20px;
                padding:22px;
            ">
                {skills_html}
            </div>"""
        )


    else:

        st.warning(
            "No major technical keywords were detected."
        )


    # ======================================================
    # SOFT SKILLS
    # ======================================================

    if soft_skills:

        st.markdown(
            "### 🤝 Detected Soft Skills"
        )


        soft_html = "".join(

            f"""<span style="
                display:inline-block;
                background:#ecfdf5;
                border:1px solid #a7f3d0;
                color:#047857;
                padding:7px 12px;
                border-radius:999px;
                margin:4px;
                font-size:12px;
                font-weight:700;
            ">
                {skill}
            </span>"""

            for skill in soft_skills

        )


        st.html(
            soft_html
        )


    # ======================================================
    # STRENGTHS
    # ======================================================

    st.html(
        """<div class="college-section-header">

            <div>

                <div class="college-section-title">
                    ✅ Profile Strengths
                </div>

                <div class="college-section-subtitle">
                    Positive signals identified for recruiters.
                </div>

            </div>

        </div>"""
    )


    if result[
        "strengths"
    ]:

        for strength in result[
            "strengths"
        ]:

            st.success(
                strength
            )


    else:

        st.info(
            "Complete more LinkedIn sections to create stronger recruiter signals."
        )


    # ======================================================
    # RECOMMENDATIONS
    # ======================================================

    st.html(
        """<div class="college-section-header">

            <div>

                <div class="college-section-title">
                    🎯 Recommended Improvements
                </div>

                <div class="college-section-subtitle">
                    Actions to make your LinkedIn profile more
                    professional and recruiter-friendly.
                </div>

            </div>

            <div class="college-section-tag">
                Action Plan
            </div>

        </div>"""
    )


    for index, recommendation in enumerate(
        result[
            "recommendations"
        ],
        start=1,
    ):

        st.html(
            f"""<div style="
                background:#ffffff;
                border:1px solid #e2e8f0;
                border-radius:17px;
                padding:18px 20px;
                margin-bottom:10px;
                box-shadow:0 6px 18px rgba(15,23,42,.035);
            ">

                <div style="
                    color:#4f46e5;
                    font-size:11px;
                    font-weight:900;
                    letter-spacing:1px;
                ">
                    ACTION {index:02d}
                </div>

                <div style="
                    color:#334155;
                    font-size:13px;
                    line-height:1.7;
                    margin-top:7px;
                ">
                    {recommendation}
                </div>

            </div>"""
        )


    # ======================================================
    # PROFESSIONAL LINKS
    # ======================================================

    if result[
        "urls"
    ]:

        st.html(
            """<div class="college-section-header">

                <div>

                    <div class="college-section-title">
                        🔗 Professional Links Detected
                    </div>

                </div>

            </div>"""
        )


        for url in result[
            "urls"
        ][
            :10
        ]:

            st.write(
                f"• {url}"
            )


    # ======================================================
    # EXTRACTED TEXT
    # ======================================================

    with st.expander(
        "🔍 View Extracted LinkedIn PDF Text"
    ):

        st.text_area(
            "Extracted Text",
            value=result[
                "text"
            ],
            height=350,
            disabled=True,
        )


    # ======================================================
    # FINAL ASSESSMENT
    # ======================================================

    st.html(
        """<div class="college-section-header">

            <div>

                <div class="college-section-title">
                    🏆 Final LinkedIn Assessment
                </div>

            </div>

        </div>"""
    )


    if overall >= 85:

        st.success(
            "🏆 Excellent LinkedIn profile. Your profile presents "
            "strong recruiter-facing information and career evidence."
        )


    elif overall >= 70:

        st.success(
            "🚀 Strong LinkedIn profile. Improve a few sections "
            "to make your professional presence even stronger."
        )


    elif overall >= 55:

        st.info(
            "👍 Good LinkedIn foundation. Improve your About section, "
            "skills, project descriptions and experience details."
        )


    elif overall >= 40:

        st.warning(
            "📚 Your LinkedIn profile is developing. Complete missing "
            "sections and strengthen role-specific keywords."
        )


    else:

        st.error(
            "🎯 Your LinkedIn profile needs improvement before using "
            "it as a primary placement profile."
        )


# ==========================================================
# DIRECT RUN
# ==========================================================

if __name__ == "__main__":

    render()