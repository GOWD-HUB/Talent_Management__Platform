import streamlit as st


def apply_school_report_theme():

    st.markdown(
        """
<style>

.report-hero {
    padding: 36px 40px;
    border-radius: 24px;
    background: linear-gradient(135deg,#ECFDF5,#EEF2FF);
    border: 1px solid #DDE7E6;
    box-shadow: 0 12px 34px rgba(15,23,42,.05);
    margin-bottom: 22px;
}

.report-eyebrow {
    color: #059669 !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.report-title {
    color: #0F172A !important;
    font-size: 35px !important;
    font-weight: 850;
    margin-top: 7px;
}

.report-description {
    color: #64748B !important;
    font-size: 14px !important;
    line-height: 1.7;
    margin-top: 8px;
}

.report-grid {
    display: grid;
    grid-template-columns: repeat(4,minmax(0,1fr));
    gap: 14px;
    margin: 18px 0 22px 0;
}

.report-card {
    padding: 18px;
    border-radius: 17px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
}

.report-label {
    color: #94A3B8 !important;
    font-size: 9px !important;
    font-weight: 800;
    text-transform: uppercase;
}

.report-value {
    color: #0F172A !important;
    font-size: 18px !important;
    font-weight: 850;
    margin-top: 6px;
}

.report-section {
    padding: 21px;
    border-radius: 19px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    box-shadow: 0 7px 20px rgba(15,23,42,.04);
    margin-top: 14px;
}

.report-section-title {
    color: #0F172A !important;
    font-size: 18px !important;
    font-weight: 850;
}

.report-section-text {
    color: #64748B !important;
    font-size: 11px !important;
    line-height: 1.7;
    margin-top: 7px;
}

.report-score {
    padding: 23px;
    border-radius: 20px;
    background: linear-gradient(135deg,#EFF6FF,#F5F3FF);
    border: 1px solid #C7D2FE;
    margin: 18px 0;
}

.report-score-value {
    color: #0F172A !important;
    font-size: 42px !important;
    font-weight: 900;
}

.report-score-label {
    color: #6366F1 !important;
    font-size: 12px !important;
    font-weight: 800;
}

.report-action {
    padding: 13px 15px;
    border-radius: 13px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    margin-top: 8px;
    color: #334155 !important;
    font-size: 11px !important;
}

@media(max-width:900px) {
    .report-grid {
        grid-template-columns: repeat(2,1fr);
    }
}

@media(max-width:600px) {
    .report-grid {
        grid-template-columns: 1fr;
    }
}

</style>
""",
        unsafe_allow_html=True,
    )
