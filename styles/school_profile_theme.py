import streamlit as st


def apply_school_profile_theme():

    st.markdown(
        """
<style>

/* =========================================================
   PROFILE HERO
   ========================================================= */

.student-profile-hero {
    padding: 34px 38px;
    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            #EEF2FF,
            #E0F2FE
        );

    border: 1px solid #D7E5F5;

    box-shadow:
        0 14px 36px
        rgba(15,23,42,.06);

    margin-bottom: 22px;
}

.student-profile-eyebrow {
    color: #2563EB !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.student-profile-title {
    color: #0F172A !important;
    font-size: 36px !important;
    font-weight: 800;
    margin-top: 8px;
}

.student-profile-description {
    color: #64748B !important;
    font-size: 14px !important;
    line-height: 1.7;
    max-width: 780px;
    margin-top: 8px;
}


/* =========================================================
   PROFILE METRICS
   ========================================================= */

.profile-metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0,1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.profile-metric-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 19px;

    box-shadow:
        0 8px 24px
        rgba(15,23,42,.045);
}

.profile-metric-label {
    color: #94A3B8 !important;
    font-size: 10px !important;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .7px;
}

.profile-metric-value {
    color: #0F172A !important;
    font-size: 23px !important;
    font-weight: 800;
    margin-top: 7px;
}

.profile-metric-text {
    color: #64748B !important;
    font-size: 11px !important;
    margin-top: 5px;
}


/* =========================================================
   FORM
   ========================================================= */

.student-profile-section {
    margin-top: 20px;
    margin-bottom: 10px;
}

.student-profile-section-title {
    color: #0F172A !important;
    font-size: 21px !important;
    font-weight: 800;
}

.student-profile-section-description {
    color: #64748B !important;
    font-size: 12px !important;
    margin-top: 3px;
}


div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 22px;

    padding: 25px;

    box-shadow:
        0 10px 30px
        rgba(15,23,42,.05);
}


div[data-testid="stForm"] label p {
    color: #1E293B !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}


div[data-testid="stForm"] input,
div[data-testid="stForm"] textarea {
    background: #F8FAFC !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;

    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}


div[data-testid="stForm"] input::placeholder,
div[data-testid="stForm"] textarea::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
}


div[data-testid="stForm"]
.stFormSubmitButton > button {
    min-height: 48px;

    border-radius: 11px !important;

    background:
        linear-gradient(
            135deg,
            #2563EB,
            #4F46E5
        ) !important;

    color: #FFFFFF !important;

    border: none !important;

    font-size: 14px !important;
    font-weight: 700 !important;
}


div[data-testid="stForm"]
.stFormSubmitButton > button p {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}


/* =========================================================
   SNAPSHOT
   ========================================================= */

.profile-summary-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: 17px;
    margin-top: 20px;
}

.profile-summary-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 20px;

    box-shadow:
        0 8px 22px
        rgba(15,23,42,.04);
}

.profile-summary-icon {
    font-size: 24px;
    margin-bottom: 10px;
}

.profile-summary-title {
    color: #0F172A !important;
    font-size: 15px !important;
    font-weight: 800;
}

.profile-summary-value {
    color: #64748B !important;
    font-size: 12px !important;
    line-height: 1.6;
    margin-top: 6px;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 950px) {

    .profile-metric-grid,
    .profile-summary-grid {
        grid-template-columns: repeat(2, 1fr);
    }

}

@media (max-width: 650px) {

    .profile-metric-grid,
    .profile-summary-grid {
        grid-template-columns: 1fr;
    }

}

</style>
""",
        unsafe_allow_html=True,
    )