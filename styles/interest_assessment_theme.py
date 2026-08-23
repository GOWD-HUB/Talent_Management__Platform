import streamlit as st


def apply_interest_assessment_theme():

    st.markdown(
        """
<style>

.interest-hero {
    padding: 34px 38px;
    border-radius: 24px;
    background: linear-gradient(135deg,#FFF7ED,#EEF2FF);
    border: 1px solid #E2E8F0;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(15,23,42,.05);
}

.interest-eyebrow {
    color: #7C3AED !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.interest-title {
    color: #0F172A !important;
    font-size: 34px !important;
    font-weight: 800;
    margin-top: 7px;
}

.interest-description {
    color: #64748B !important;
    font-size: 14px !important;
    line-height: 1.7;
    max-width: 850px;
    margin-top: 8px;
}

.interest-progress-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 20px;
}

.interest-question-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 20px;
    margin-top: 12px;
    margin-bottom: 8px;
    box-shadow: 0 6px 18px rgba(15,23,42,.035);
}

.interest-question-number {
    color: #7C3AED !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: .8px;
}

.interest-question-text {
    color: #0F172A !important;
    font-size: 17px !important;
    font-weight: 700;
    line-height: 1.5;
    margin-top: 6px;
}

.interest-result-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 22px;
    min-height: 180px;
    box-shadow: 0 8px 22px rgba(15,23,42,.04);
}

.interest-result-icon {
    font-size: 28px;
}

.interest-result-rank {
    color: #7C3AED !important;
    font-size: 10px !important;
    font-weight: 800;
    margin-top: 10px;
}

.interest-result-title {
    color: #0F172A !important;
    font-size: 19px !important;
    font-weight: 800;
    margin-top: 4px;
}

.interest-result-score {
    color: #059669 !important;
    font-size: 13px !important;
    font-weight: 800;
    margin-top: 8px;
}

.interest-result-description {
    color: #64748B !important;
    font-size: 12px !important;
    line-height: 1.6;
    margin-top: 7px;
}

</style>
""",
        unsafe_allow_html=True,
    )