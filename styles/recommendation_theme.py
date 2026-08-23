import streamlit as st


def apply_recommendation_theme():

    st.markdown(
        """
<style>

.rec-hero {
    padding: 36px 40px;
    border-radius: 24px;
    background: linear-gradient(135deg,#FFF7ED,#EEF2FF);
    border: 1px solid #E2E8F0;
    box-shadow: 0 12px 34px rgba(15,23,42,.05);
    margin-bottom: 24px;
}

.rec-eyebrow {
    color: #7C3AED !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.rec-title {
    color: #0F172A !important;
    font-size: 35px !important;
    font-weight: 850;
    margin-top: 7px;
}

.rec-description {
    color: #64748B !important;
    font-size: 14px !important;
    line-height: 1.7;
    max-width: 880px;
    margin-top: 8px;
}

.rec-card {
    min-height: 210px;
    padding: 21px;
    border-radius: 19px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    box-shadow: 0 7px 20px rgba(15,23,42,.04);
    margin-bottom: 8px;
}

.rec-icon {
    font-size: 26px;
}

.rec-card-title {
    color: #0F172A !important;
    font-size: 17px !important;
    font-weight: 800;
    margin-top: 10px;
}

.rec-card-text {
    color: #64748B !important;
    font-size: 12px !important;
    line-height: 1.6;
    margin-top: 6px;
}

.rec-action {
    margin-top: 12px;
    padding: 9px 11px;
    border-radius: 10px;
    background: #F8FAFC;
    color: #334155 !important;
    font-size: 10px !important;
    line-height: 1.5;
}

</style>
""",
        unsafe_allow_html=True,
    )
