import streamlit as st


def apply_college_theme():

    st.markdown(
        """
<style>

/* =========================================================
   PAGE BACKGROUND
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 95% 0%,
            rgba(99, 102, 241, 0.08),
            transparent 28%
        ),
        linear-gradient(
            180deg,
            #F8FBFF 0%,
            #F4F7FC 100%
        ) !important;
}


/* =========================================================
   MAIN CONTAINER
   ========================================================= */

[data-testid="stMainBlockContainer"] {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}


/* =========================================================
   GLOBAL TEXT
   ========================================================= */

[data-testid="stMainBlockContainer"] h1,
[data-testid="stMainBlockContainer"] h2,
[data-testid="stMainBlockContainer"] h3,
[data-testid="stMainBlockContainer"] h4,
[data-testid="stMainBlockContainer"] p,
[data-testid="stMainBlockContainer"] span,
[data-testid="stMainBlockContainer"] label,
[data-testid="stMainBlockContainer"] li {
    color: #0F172A;
}


/* =========================================================
   HERO
   ========================================================= */

.college-hero {

    position: relative;

    padding: 42px 46px;

    border-radius: 28px;

    background:

        radial-gradient(
            circle at 92% 18%,
            rgba(255,255,255,.17) 0px,
            rgba(255,255,255,.17) 85px,
            transparent 86px
        ),

        linear-gradient(
            135deg,
            #4338CA 0%,
            #4F46E5 45%,
            #7C3AED 100%
        );

    box-shadow:
        0 22px 50px rgba(79,70,229,.18);

    margin-bottom: 30px;

    overflow: hidden;
}


.college-hero-badge {

    display: inline-block;

    padding: 7px 14px;

    border-radius: 999px;

    background:
        rgba(255,255,255,.14);

    border:
        1px solid rgba(255,255,255,.24);

    color: #FFFFFF !important;

    font-size: 10px !important;

    font-weight: 800;

    letter-spacing: 1px;
}


.college-hero-title {

    color: #FFFFFF !important;

    font-size: 40px !important;

    font-weight: 900 !important;

    line-height: 1.15 !important;

    margin-top: 20px;

    margin-bottom: 12px;
}


.college-hero-description {

    color: #E0E7FF !important;

    font-size: 14px !important;

    line-height: 1.8 !important;

    max-width: 900px;
}


/* =========================================================
   SECTION HEADERS
   ========================================================= */

.college-section-header {

    display: flex;

    align-items: flex-end;

    justify-content: space-between;

    margin-top: 34px;

    margin-bottom: 18px;
}


.college-section-title {

    color: #0F172A !important;

    font-size: 27px !important;

    font-weight: 900 !important;
}


.college-section-subtitle {

    color: #64748B !important;

    font-size: 12px !important;

    margin-top: 4px;
}


.college-section-tag {

    color: #4F46E5 !important;

    font-size: 11px !important;

    font-weight: 800 !important;
}


/* =========================================================
   METRIC GRID
   ========================================================= */

.college-metric-grid {

    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 18px;

    margin: 20px 0 15px 0;
}


/* =========================================================
   METRIC CARD
   ========================================================= */

.college-metric-card {

    min-height: 190px;

    padding: 24px;

    border-radius: 20px;

    background: #FFFFFF;

    border:
        1px solid #DCE5F0;

    box-shadow:
        0 8px 25px rgba(15,23,42,.045);

    overflow: hidden;
}


.college-metric-icon {

    width: 48px;

    height: 48px;

    border-radius: 14px;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #EEF2FF;

    font-size: 22px;

    margin-bottom: 19px;
}


.college-metric-label {

    color: #8291AD !important;

    font-size: 10px !important;

    font-weight: 800 !important;

    letter-spacing: 1px;

    text-transform: uppercase;

    line-height: 1.3;
}


/* IMPORTANT:
   all metric values use SAME font size */

.college-metric-value {

    color: #07152F !important;

    font-size: 24px !important;

    font-weight: 900 !important;

    line-height: 1.25 !important;

    margin-top: 8px;

    margin-bottom: 8px;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;
}


.college-metric-caption {

    color: #65748B !important;

    font-size: 11px !important;

    line-height: 1.55 !important;

    margin-top: 6px;
}


/* =========================================================
   PROFILE FORM SECTION
   ========================================================= */

.college-profile-section {

    padding: 24px;

    border-radius: 20px;

    background: #FFFFFF;

    border:
        1px solid #E2E8F0;

    box-shadow:
        0 8px 24px rgba(15,23,42,.04);

    margin-top: 18px;

    margin-bottom: 18px;
}


/* =========================================================
   FEATURE CARDS
   ========================================================= */

.college-feature-card {

    min-height: 180px;

    padding: 24px;

    border-radius: 22px;

    border:
        1px solid #E2E8F0;

    box-shadow:
        0 10px 28px rgba(15,23,42,.045);

    margin-bottom: 7px;
}


.card-purple {
    background:
        linear-gradient(
            135deg,
            #F5F3FF,
            #FAF5FF
        );
}


.card-blue {
    background:
        linear-gradient(
            135deg,
            #EFF6FF,
            #F0F9FF
        );
}


.card-green {
    background:
        linear-gradient(
            135deg,
            #ECFDF5,
            #F0FDF4
        );
}


.card-orange {
    background:
        linear-gradient(
            135deg,
            #FFF7ED,
            #FFFBEB
        );
}


.card-pink {
    background:
        linear-gradient(
            135deg,
            #FDF2F8,
            #FFF1F2
        );
}


.card-cyan {
    background:
        linear-gradient(
            135deg,
            #ECFEFF,
            #F0FDFA
        );
}


.college-feature-icon {

    width: 50px;

    height: 50px;

    border-radius: 15px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        rgba(255,255,255,.75);

    font-size: 23px;

    margin-bottom: 20px;
}


.college-feature-title {

    color: #0F172A !important;

    font-size: 17px !important;

    font-weight: 900 !important;
}


.college-feature-description {

    color: #64748B !important;

    font-size: 11px !important;

    line-height: 1.65 !important;

    margin-top: 8px;
}


/* =========================================================
   FORM INPUTS
   ========================================================= */

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {

    border-radius: 11px !important;

    border:
        1px solid #D9E2EC !important;

    background:
        #FFFFFF !important;

    color:
        #0F172A !important;
}


[data-testid="stSelectbox"] > div > div {

    border-radius: 11px !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

div.stButton > button {

    width: 100%;

    min-height: 50px;

    border-radius: 13px;

    border: none !important;

    background:
        linear-gradient(
            90deg,
            #2563EB,
            #3B82F6
        ) !important;

    color: #FFFFFF !important;

    font-weight: 800 !important;

    box-shadow:
        0 8px 20px rgba(37,99,235,.18);

    transition:
        all .18s ease;
}


div.stButton > button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 12px 25px rgba(37,99,235,.24);
}


/* =========================================================
   FORM SUBMIT BUTTON
   ========================================================= */

[data-testid="stFormSubmitButton"] button {

    width: 100%;

    min-height: 52px;

    border-radius: 13px !important;

    border: none !important;

    background:
        linear-gradient(
            90deg,
            #4F46E5,
            #6366F1
        ) !important;

    color: #FFFFFF !important;

    font-size: 14px !important;

    font-weight: 800 !important;
}


/* =========================================================
   PROGRESS
   ========================================================= */

[data-testid="stProgress"] {

    margin-top: 10px;

    margin-bottom: 20px;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media(max-width: 1100px) {

    .college-metric-grid {

        grid-template-columns:
            repeat(2, 1fr);
    }
}


@media(max-width: 700px) {

    .college-metric-grid {

        grid-template-columns:
            1fr;
    }


    .college-hero {

        padding:
            30px 24px;
    }


    .college-hero-title {

        font-size:
            30px !important;
    }
}

</style>
""",
        unsafe_allow_html=True,
    )