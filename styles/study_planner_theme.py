import streamlit as st


def apply_study_planner_theme():

    st.markdown(
        """
<style>

.study-hero {
    padding: 36px 40px;
    border-radius: 24px;
    background: linear-gradient(135deg,#EEF2FF,#ECFDF5);
    border: 1px solid #DDE7F5;
    box-shadow: 0 12px 34px rgba(15,23,42,.05);
    margin-bottom: 24px;
}

.study-eyebrow {
    color: #2563EB !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.study-title {
    color: #0F172A !important;
    font-size: 35px !important;
    font-weight: 850;
    margin-top: 7px;
}

.study-description {
    color: #64748B !important;
    font-size: 14px !important;
    line-height: 1.7;
    max-width: 880px;
    margin-top: 8px;
}

.study-summary-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0,1fr));
    gap: 14px;
    margin-bottom: 22px;
}

.study-summary-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 17px;
    padding: 18px;
}

.study-summary-label {
    color: #94A3B8 !important;
    font-size: 9px !important;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .7px;
}

.study-summary-value {
    color: #0F172A !important;
    font-size: 18px !important;
    font-weight: 800;
    margin-top: 6px;
}

.study-day-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 19px;
    padding: 18px;
    margin-top: 15px;
    box-shadow: 0 6px 18px rgba(15,23,42,.035);
}

.study-day-title {
    color: #0F172A !important;
    font-size: 19px !important;
    font-weight: 800;
}

.study-task-card {
    padding: 15px;
    border-radius: 14px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    margin-top: 8px;
}

.study-task-title {
    color: #0F172A !important;
    font-size: 13px !important;
    font-weight: 800;
}

.study-task-meta {
    color: #64748B !important;
    font-size: 10px !important;
    margin-top: 4px;
}

.study-next-card {
    padding: 19px;
    border-radius: 17px;
    background: linear-gradient(135deg,#FFF7ED,#F5F3FF);
    border: 1px solid #FED7AA;
    margin: 18px 0;
}

.study-next-label {
    color: #C2410C !important;
    font-size: 9px !important;
    font-weight: 800;
    text-transform: uppercase;
}

.study-next-title {
    color: #0F172A !important;
    font-size: 17px !important;
    font-weight: 800;
    margin-top: 5px;
}

.study-next-text {
    color: #64748B !important;
    font-size: 11px !important;
    margin-top: 4px;
}

@media(max-width: 900px) {
    .study-summary-grid {
        grid-template-columns: repeat(2,1fr);
    }
}

@media(max-width: 600px) {
    .study-summary-grid {
        grid-template-columns: 1fr;
    }
}

</style>
""",
        unsafe_allow_html=True,
    )
