import streamlit as st


def apply_skills_roadmap_theme():

    st.markdown(
        """
<style>

.skills-hero {
    padding: 36px 40px;
    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            #ECFDF5,
            #EEF2FF
        );

    border: 1px solid #DDE7E6;

    box-shadow:
        0 12px 34px
        rgba(15,23,42,.05);

    margin-bottom: 24px;
}


.skills-eyebrow {
    color: #059669 !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: 1.2px;
}


.skills-title {
    color: #0F172A !important;
    font-size: 35px !important;
    font-weight: 800;
    margin-top: 8px;
}


.skills-description {
    color: #64748B !important;
    font-size: 14px !important;
    line-height: 1.7;
    margin-top: 8px;
    max-width: 850px;
}


.skills-summary-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: 16px;
    margin-bottom: 24px;
}


.skills-summary-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 19px;
}


.skills-summary-label {
    color: #94A3B8 !important;
    font-size: 10px !important;
    font-weight: 800;
    text-transform: uppercase;
}


.skills-summary-value {
    color: #0F172A !important;
    font-size: 18px !important;
    font-weight: 800;
    margin-top: 6px;
}


.skills-level-header {
    margin-top: 28px;
    margin-bottom: 12px;

    padding: 17px 20px;

    border-radius: 16px;

    background: #F8FAFC;

    border: 1px solid #E2E8F0;
}


.skills-level-title {
    color: #0F172A !important;
    font-size: 20px !important;
    font-weight: 800;
}


.skills-level-description {
    color: #64748B !important;
    font-size: 11px !important;
    margin-top: 4px;
}


.skill-card {
    padding: 18px;

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 17px;

    min-height: 135px;

    box-shadow:
        0 6px 18px
        rgba(15,23,42,.035);
}


.skill-card-title {
    color: #0F172A !important;
    font-size: 15px !important;
    font-weight: 800;
}


.skill-card-description {
    color: #64748B !important;
    font-size: 11px !important;
    line-height: 1.6;
    margin-top: 6px;
}


.next-skill-card {
    padding: 20px;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            #EFF6FF,
            #F5F3FF
        );

    border: 1px solid #BFDBFE;

    margin-top: 20px;
}


.next-skill-label {
    color: #2563EB !important;
    font-size: 10px !important;
    font-weight: 800;
    text-transform: uppercase;
}


.next-skill-title {
    color: #0F172A !important;
    font-size: 19px !important;
    font-weight: 800;
    margin-top: 5px;
}


.next-skill-text {
    color: #64748B !important;
    font-size: 12px !important;
    line-height: 1.6;
    margin-top: 5px;
}


@media(max-width: 800px) {

    .skills-summary-grid {
        grid-template-columns: 1fr;
    }

}

</style>
""",
        unsafe_allow_html=True,
    )