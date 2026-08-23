import streamlit as st


def render():

    # ======================================================
    # HERO
    # ======================================================

    st.markdown(
        (
            '<section class="home-hero">'

            '<div class="home-hero-content">'

            '<span class="home-badge">'
            'AI-POWERED CAREER DEVELOPMENT PLATFORM'
            '</span>'

            '<h1>'
            'Build skills. Discover opportunities. '
            'Grow with confidence.'
            '</h1>'

            '<p>'
            'TalentSphere Elevate provides personalised learning, '
            'placement preparation and professional career development '
            'for students and working professionals.'
            '</p>'

            '<div class="home-tags">'
            '<span>🎓 Learning</span>'
            '<span>💻 Placement Preparation</span>'
            '<span>🎯 Career Planning</span>'
            '<span>🤖 AI Guidance</span>'
            '</div>'

            '</div>'

            '<div class="home-hero-visual">'
            '<div class="hero-circle hero-circle-one"></div>'
            '<div class="hero-circle hero-circle-two"></div>'
            '<div class="hero-visual-card">'
            '<div class="hero-visual-icon">🚀</div>'
            '<strong>Career Growth</strong>'
            '<small>Learn • Prepare • Grow</small>'
            '</div>'
            '</div>'

            '</section>'
        ),
        unsafe_allow_html=True
    )


    # ======================================================
    # PLATFORM SUMMARY
    # ======================================================

    stat_cols = st.columns(4)

    statistics = [
        ("3", "Career Stages"),
        ("25+", "Career Tools"),
        ("100%", "Personalised"),
        ("24/7", "Guidance"),
    ]

    for column, (value, label) in zip(
        stat_cols,
        statistics
    ):

        with column:

            st.markdown(
                (
                    '<div class="home-stat-card">'
                    f'<div class="home-stat-value">{value}</div>'
                    f'<div class="home-stat-label">{label}</div>'
                    '</div>'
                ),
                unsafe_allow_html=True
            )


    # ======================================================
    # CAREER STAGES
    # ======================================================

    st.markdown(
        (
            '<div class="home-section-header">'
            '<span>PERSONALISED WORKSPACES</span>'
            '<h2>Choose your career stage</h2>'
            '<p>'
            'Select the workspace designed for where you are '
            'in your academic or professional journey.'
            '</p>'
            '</div>'
        ),
        unsafe_allow_html=True
    )


    # ======================================================
    # CAREER STAGE GRID
    # ======================================================

    st.markdown(
        (
            '<div class="career-stage-grid">'

            # SCHOOL
            '<div class="career-stage-card school-stage">'

            '<div class="stage-top">'
            '<div class="stage-icon school-icon">🎓</div>'
            '<div class="stage-number">01</div>'
            '</div>'

            '<h3>School Student</h3>'

            '<p>'
            'Discover your interests, improve academics and '
            'build a clear understanding of future career options.'
            '</p>'

            '<div class="stage-features">'
            '<div>✓ Career Explorer</div>'
            '<div>✓ Interest Assessment</div>'
            '<div>✓ Subject Learning</div>'
            '<div>✓ Future Skills Roadmap</div>'
            '<div>✓ AI Study Mentor</div>'
            '</div>'

            '<div class="stage-footer">'
            'Explore School Workspace'
            '<span>→</span>'
            '</div>'

            '</div>'


            # COLLEGE
            '<div class="career-stage-card college-stage">'

            '<div class="stage-top">'
            '<div class="stage-icon college-icon">💻</div>'
            '<div class="stage-number">02</div>'
            '</div>'

            '<h3>College Student</h3>'

            '<p>'
            'Prepare for placements through coding, resumes, '
            'interviews, internships and job-readiness tools.'
            '</p>'

            '<div class="stage-features">'
            '<div>✓ Coding Practice</div>'
            '<div>✓ Resume Builder</div>'
            '<div>✓ ATS Resume Checker</div>'
            '<div>✓ Mock Interviews</div>'
            '<div>✓ Job Matching</div>'
            '</div>'

            '<div class="stage-footer">'
            'Explore College Workspace'
            '<span>→</span>'
            '</div>'

            '</div>'


            # PROFESSIONAL
            '<div class="career-stage-card professional-stage">'

            '<div class="stage-top">'
            '<div class="stage-icon professional-icon">💼</div>'
            '<div class="stage-number">03</div>'
            '</div>'

            '<h3>Working Professional</h3>'

            '<p>'
            'Develop high-value skills, evaluate promotion readiness '
            'and make smarter career and salary decisions.'
            '</p>'

            '<div class="stage-features">'
            '<div>✓ Learning & Skills</div>'
            '<div>✓ Career Transition</div>'
            '<div>✓ Promotion Readiness</div>'
            '<div>✓ Salary Insights</div>'
            '<div>✓ Leadership Growth</div>'
            '</div>'

            '<div class="stage-footer">'
            'Explore Professional Workspace'
            '<span>→</span>'
            '</div>'

            '</div>'

            '</div>'
        ),
        unsafe_allow_html=True
    )


    # ======================================================
    # WHY TALENTSPHERE
    # ======================================================

    st.markdown(
        (
            '<div class="home-section-header">'
            '<span>WHY TALENTSPHERE</span>'
            '<h2>A complete career-development ecosystem</h2>'
            '<p>'
            'Use one platform to learn, analyse your readiness '
            'and plan the next stage of your career.'
            '</p>'
            '</div>'
        ),
        unsafe_allow_html=True
    )


    st.markdown(
        (
            '<div class="capability-grid">'

            '<div class="capability-card">'
            '<div class="capability-icon purple-cap">🧠</div>'
            '<h4>Smart Guidance</h4>'
            '<p>'
            'Personalised recommendations based on your profile, '
            'skills and career goals.'
            '</p>'
            '</div>'

            '<div class="capability-card">'
            '<div class="capability-icon blue-cap">📊</div>'
            '<h4>Progress Tracking</h4>'
            '<p>'
            'Monitor assessments, learning progress and career readiness.'
            '</p>'
            '</div>'

            '<div class="capability-card">'
            '<div class="capability-icon green-cap">🎯</div>'
            '<h4>Career Intelligence</h4>'
            '<p>'
            'Understand suitable roles, skill gaps and recommended actions.'
            '</p>'
            '</div>'

            '<div class="capability-card">'
            '<div class="capability-icon orange-cap">📑</div>'
            '<h4>Growth Reports</h4>'
            '<p>'
            'Generate structured reports containing scores, gaps and roadmaps.'
            '</p>'
            '</div>'

            '</div>'
        ),
        unsafe_allow_html=True
    )


    # ======================================================
    # FINAL CTA
    # ======================================================

    st.markdown(
        (
            '<div class="home-final-cta">'

            '<div>'
            '<span>START YOUR JOURNEY</span>'

            '<h2>'
            'Turn your career goals into measurable progress.'
            '</h2>'

            '<p>'
            'Create your TalentSphere account and unlock a '
            'workspace designed specifically for your career stage.'
            '</p>'
            '</div>'

            '<div class="home-final-arrow">→</div>'

            '</div>'
        ),
        unsafe_allow_html=True
    )