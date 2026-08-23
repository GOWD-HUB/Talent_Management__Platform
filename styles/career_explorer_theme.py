import streamlit as st


def apply_career_explorer_theme():

    st.markdown(
        """
<style>

/* =========================================================
   HERO
   ========================================================= */

.hs-career-hero {

    padding:
        36px
        40px;

    border-radius:
        25px;

    background:
        linear-gradient(
            135deg,
            #EEF6FF,
            #EEF2FF
        );

    border:
        1px solid
        #D7E5F4;

    box-shadow:
        0 14px 34px
        rgba(15,23,42,.055);

    margin-bottom:
        24px;
}


.hs-career-badge {

    color:
        #2563EB !important;

    font-size:
        10px !important;

    font-weight:
        800;

    letter-spacing:
        1.3px;
}


.hs-career-title {

    color:
        #0F172A !important;

    font-size:
        36px !important;

    font-weight:
        800;

    line-height:
        1.2;

    margin-top:
        8px;
}


.hs-career-description {

    color:
        #64748B !important;

    font-size:
        14px !important;

    line-height:
        1.7;

    max-width:
        850px;

    margin-top:
        9px;
}


/* =========================================================
   SNAPSHOT
   ========================================================= */

.hs-profile-grid {

    display:
        grid;

    grid-template-columns:
        repeat(
            4,
            minmax(0, 1fr)
        );

    gap:
        15px;

    margin-bottom:
        28px;
}


.hs-profile-card {

    min-height:
        105px;

    padding:
        18px;

    background:
        #FFFFFF;

    border:
        1px solid
        #E2E8F0;

    border-radius:
        17px;

    box-shadow:
        0 7px 20px
        rgba(15,23,42,.035);
}


.hs-profile-label {

    color:
        #94A3B8 !important;

    font-size:
        9px !important;

    font-weight:
        800;

    letter-spacing:
        .7px;

    text-transform:
        uppercase;
}


.hs-profile-value {

    color:
        #0F172A !important;

    font-size:
        14px !important;

    font-weight:
        700;

    line-height:
        1.5;

    margin-top:
        7px;
}


/* =========================================================
   INFO STRIP
   ========================================================= */

.hs-guidance-strip {

    display:
        flex;

    align-items:
        center;

    gap:
        14px;

    padding:
        17px 19px;

    margin-bottom:
        28px;

    border-radius:
        17px;

    background:
        #FFFBEB;

    border:
        1px solid
        #FDE68A;
}


.hs-guidance-icon {

    font-size:
        25px;
}


.hs-guidance-title {

    color:
        #92400E !important;

    font-size:
        13px !important;

    font-weight:
        800;
}


.hs-guidance-text {

    color:
        #A16207 !important;

    font-size:
        11px !important;

    margin-top:
        3px;
}


/* =========================================================
   SECTION
   ========================================================= */

.hs-section-title {

    color:
        #0F172A !important;

    font-size:
        27px !important;

    font-weight:
        800;

    margin-top:
        23px;
}


.hs-section-description {

    color:
        #64748B !important;

    font-size:
        13px !important;

    line-height:
        1.6;

    margin-top:
        4px;

    margin-bottom:
        18px;
}


/* =========================================================
   CATEGORY
   ========================================================= */

.hs-category-card {

    min-height:
        285px;

    padding:
        22px;

    background:
        #FFFFFF;

    border:
        1px solid
        #E2E8F0;

    border-radius:
        22px;

    box-shadow:
        0 8px 24px
        rgba(15,23,42,.045);

    margin-bottom:
        6px;

    transition:
        all .20s ease;
}


.hs-category-card:hover {

    transform:
        translateY(-4px);

    border-color:
        #BFDBFE;

    box-shadow:
        0 15px 30px
        rgba(37,99,235,.08);
}


.hs-category-icon {

    width:
        55px;

    height:
        55px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        16px;

    background:
        linear-gradient(
            135deg,
            #EFF6FF,
            #EEF2FF
        );

    font-size:
        27px;
}


.hs-category-title {

    color:
        #0F172A !important;

    font-size:
        20px !important;

    font-weight:
        800;

    margin-top:
        15px;
}


.hs-category-description {

    color:
        #64748B !important;

    font-size:
        12px !important;

    line-height:
        1.65;

    margin-top:
        7px;
}


.hs-match {

    display:
        inline-block;

    padding:
        6px
        10px;

    margin-top:
        13px;

    border-radius:
        999px;

    background:
        #ECFDF5;

    color:
        #047857 !important;

    font-size:
        10px !important;

    font-weight:
        800;
}


.hs-stream {

    margin-top:
        12px;

    padding:
        10px;

    border-radius:
        11px;

    background:
        #F8FAFC;

    color:
        #475569 !important;

    font-size:
        10px !important;

    line-height:
        1.5;
}


/* =========================================================
   DETAILS
   ========================================================= */

.hs-detail-card {

    padding:
        26px;

    background:
        linear-gradient(
            135deg,
            #F8FAFC,
            #FFFFFF
        );

    border:
        1px solid
        #E2E8F0;

    border-radius:
        22px;

    box-shadow:
        0 8px 24px
        rgba(15,23,42,.045);

    margin-top:
        18px;
}


.hs-detail-title {

    color:
        #0F172A !important;

    font-size:
        26px !important;

    font-weight:
        800;
}


.hs-detail-description {

    color:
        #64748B !important;

    font-size:
        13px !important;

    line-height:
        1.7;

    margin-top:
        7px;
}


/* =========================================================
   CAREER OPTION
   ========================================================= */

.hs-career-option {

    padding:
        22px;

    margin-top:
        18px;

    border-radius:
        19px;

    background:
        #FFFFFF;

    border:
        1px solid
        #E2E8F0;
}


.hs-career-option-title {

    color:
        #0F172A !important;

    font-size:
        19px !important;

    font-weight:
        800;
}


.hs-career-option-text {

    color:
        #64748B !important;

    font-size:
        12px !important;

    line-height:
        1.65;

    margin-top:
        6px;
}


/* =========================================================
   PATH
   ========================================================= */

.hs-path-box {

    padding:
        15px;

    margin-top:
        10px;

    border-radius:
        14px;

    background:
        #F8FAFC;

    border:
        1px solid
        #E2E8F0;
}


.hs-path-label {

    color:
        #2563EB !important;

    font-size:
        10px !important;

    font-weight:
        800;

    letter-spacing:
        .6px;

    text-transform:
        uppercase;
}


.hs-path-value {

    color:
        #334155 !important;

    font-size:
        12px !important;

    line-height:
        1.6;

    margin-top:
        5px;
}


/* =========================================================
   FINAL NOTE
   ========================================================= */

.hs-explore-note {

    padding:
        20px;

    margin-top:
        25px;

    background:
        #EFF6FF;

    border:
        1px solid
        #BFDBFE;

    border-radius:
        17px;
}


.hs-explore-note-title {

    color:
        #1D4ED8 !important;

    font-size:
        14px !important;

    font-weight:
        800;
}


.hs-explore-note-text {

    color:
        #475569 !important;

    font-size:
        11px !important;

    line-height:
        1.65;

    margin-top:
        5px;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media(max-width: 1000px) {

    .hs-profile-grid {

        grid-template-columns:
            repeat(2, 1fr);
    }
}


@media(max-width: 650px) {

    .hs-career-hero {

        padding:
            28px
            22px;
    }


    .hs-career-title {

        font-size:
            29px !important;
    }


    .hs-profile-grid {

        grid-template-columns:
            1fr;
    }
}

</style>
""",
        unsafe_allow_html=True,
    )