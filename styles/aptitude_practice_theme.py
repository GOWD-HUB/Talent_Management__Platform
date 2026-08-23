import streamlit as st


def apply_aptitude_theme():

    st.markdown(
        """
<style>

.aptitude-hero {
    padding: 34px 38px;
    border-radius: 24px;
    background: linear-gradient(135deg,#FFF7ED,#EEF2FF);
    border: 1px solid #E2E8F0;
    box-shadow: 0 12px 34px rgba(15,23,42,.05);
    margin-bottom: 22px;
}

.aptitude-eyebrow {
    color: #EA580C !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.aptitude-title {
    color: #0F172A !important;
    font-size: 34px !important;
    font-weight: 850;
    margin-top: 7px;
}

.aptitude-description {
    color: #64748B !important;
    font-size: 14px !important;
    line-height: 1.7;
    margin-top: 8px;
}

.aptitude-grid {
    display: grid;
    grid-template-columns: repeat(3,minmax(0,1fr));
    gap: 16px;
    margin-bottom: 22px;
}

.aptitude-card {
    padding: 20px;
    border-radius: 18px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
}

.aptitude-card-title {
    color: #0F172A !important;
    font-size: 17px !important;
    font-weight: 850;
}

.aptitude-card-text {
    color: #64748B !important;
    font-size: 11px !important;
    line-height: 1.6;
    margin-top: 6px;
}

.aptitude-summary-grid {
    display: grid;
    grid-template-columns: repeat(4,minmax(0,1fr));
    gap: 14px;
    margin: 18px 0;
}

.aptitude-summary-card {
    padding: 17px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
}

.aptitude-summary-label {
    color: #94A3B8 !important;
    font-size: 9px !important;
    font-weight: 800;
    text-transform: uppercase;
}

.aptitude-summary-value {
    color: #0F172A !important;
    font-size: 18px !important;
    font-weight: 850;
    margin-top: 5px;
}

.aptitude-result {
    padding: 20px;
    border-radius: 18px;
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
    margin: 16px 0;
}

@media(max-width:900px) {
    .aptitude-grid,
    .aptitude-summary-grid {
        grid-template-columns: 1fr;
    }
}

</style>
""",
        unsafe_allow_html=True,
    )
