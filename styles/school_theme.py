import streamlit as st


def apply_school_theme():

    st.markdown(
        """
<style>

/* =========================================================
   SCHOOL DASHBOARD WRAPPER
   ========================================================= */

.school-page {
    width: 100%;
}


/* =========================================================
   HERO
   ========================================================= */

.school-hero {
    position: relative;
    overflow: hidden;

    min-height: 290px;

    padding: 42px 44px;

    border-radius: 28px;

    background:
        radial-gradient(
            circle at 88% 20%,
            rgba(255,255,255,.25),
            transparent 24%
        ),
        radial-gradient(
            circle at 78% 100%,
            rgba(255,255,255,.10),
            transparent 26%
        ),
        linear-gradient(
            135deg,
            #4338CA 0%,
            #4F46E5 48%,
            #7C3AED 100%
        );

    box-shadow:
        0 22px 50px
        rgba(79,70,229,.18);

    margin-bottom: 0;
}

.school-hero::before {
    content: "";

    position: absolute;

    width: 280px;
    height: 280px;

    right: -65px;
    top: -105px;

    border-radius: 50%;

    border:
        38px solid
        rgba(255,255,255,.07);
}

.school-hero::after {
    content: "";

    position: absolute;

    width: 220px;
    height: 220px;

    right: 100px;
    bottom: -135px;

    border-radius: 50%;

    border:
        30px solid
        rgba(255,255,255,.045);
}

.school-hero-content {
    position: relative;
    z-index: 3;

    max-width: 820px;
}

.school-hero-badge {
    display: inline-flex;

    align-items: center;

    padding: 7px 13px;

    border-radius: 999px;

    background:
        rgba(255,255,255,.14);

    border:
        1px solid
        rgba(255,255,255,.18);

    color: #FFFFFF !important;

    font-size: 11px !important;

    font-weight: 800;

    letter-spacing: 1px;
}

.school-hero h1 {
    color: #FFFFFF !important;

    font-size: 43px !important;

    line-height: 1.12;

    font-weight: 800;

    margin:
        20px 0 12px 0;

    letter-spacing: -1px;
}

.school-hero p {
    color:
        rgba(255,255,255,.86) !important;

    font-size: 15px !important;

    line-height: 1.75;

    max-width: 760px;
}


/* =========================================================
   SEARCH
   ========================================================= */

.school-search-wrapper {
    position: relative;

    z-index: 10;

    margin:
        -30px 28px 34px 28px;
}

.school-search-box {
    min-height: 62px;

    display: flex;

    align-items: center;

    gap: 13px;

    padding: 0 20px;

    background: #FFFFFF;

    border:
        1px solid #E2E8F0;

    border-radius: 18px;

    box-shadow:
        0 14px 34px
        rgba(15,23,42,.10);
}

.school-search-icon {
    font-size: 20px;
}

.school-search-text {
    color: #94A3B8 !important;

    font-size: 14px !important;

    font-weight: 500;
}


/* =========================================================
   SECTION HEADER
   ========================================================= */

.school-section-header {
    display: flex;

    align-items: flex-end;

    justify-content: space-between;

    gap: 20px;

    margin:
        34px 0 18px 0;
}

.school-section-title {
    color: #0F172A !important;

    font-size: 26px !important;

    font-weight: 800;
}

.school-section-subtitle {
    color: #64748B !important;

    font-size: 13px !important;

    margin-top: 5px;
}

.school-section-action {
    color: #4F46E5 !important;

    font-size: 12px !important;

    font-weight: 700;
}


/* =========================================================
   QUICK ACCESS GRID
   ========================================================= */

.quick-grid {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 18px;
}


/* =========================================================
   QUICK CARD
   ========================================================= */

.quick-card {
    position: relative;

    min-height: 185px;

    padding: 22px;

    border-radius: 22px;

    border:
        1px solid rgba(226,232,240,.92);

    box-shadow:
        0 9px 24px
        rgba(15,23,42,.055);

    transition:
        transform .20s ease,
        box-shadow .20s ease,
        border-color .20s ease;
}

.quick-card:hover {
    transform:
        translateY(-5px);

    box-shadow:
        0 18px 36px
        rgba(15,23,42,.09);

    border-color:
        rgba(99,102,241,.20);
}

.quick-card-icon {
    width: 50px;
    height: 50px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 15px;

    background:
        rgba(255,255,255,.72);

    font-size: 25px;

    margin-bottom: 17px;
}

.quick-card-title {
    color: #0F172A !important;

    font-size: 17px !important;

    font-weight: 800;

    margin-bottom: 7px;
}

.quick-card-description {
    color: #64748B !important;

    font-size: 13px !important;

    line-height: 1.6;
}

.quick-card-arrow {
    position: absolute;

    right: 18px;
    bottom: 17px;

    width: 28px;
    height: 28px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    background:
        rgba(255,255,255,.70);

    color: #475569 !important;

    font-size: 14px;
}


/* =========================================================
   CARD COLORS
   ========================================================= */

.quick-purple {
    background:
        linear-gradient(
            145deg,
            #F1ECFF,
            #FBF9FF
        );
}

.quick-orange {
    background:
        linear-gradient(
            145deg,
            #FFF0E4,
            #FFF9F5
        );
}

.quick-blue {
    background:
        linear-gradient(
            145deg,
            #E8F3FF,
            #F7FBFF
        );
}

.quick-green {
    background:
        linear-gradient(
            145deg,
            #E8F8F0,
            #F7FFFA
        );
}

.quick-pink {
    background:
        linear-gradient(
            145deg,
            #FFE9F2,
            #FFF8FB
        );
}

.quick-yellow {
    background:
        linear-gradient(
            145deg,
            #FFF6D9,
            #FFFDF6
        );
}

.quick-cyan {
    background:
        linear-gradient(
            145deg,
            #E6F8FA,
            #F8FEFF
        );
}

.quick-lavender {
    background:
        linear-gradient(
            145deg,
            #EFEFFF,
            #FAFAFF
        );
}


/* =========================================================
   PROGRESS GRID
   ========================================================= */

.progress-grid {
    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 17px;
}

.progress-card {
    min-height: 150px;

    padding: 20px;

    background: #FFFFFF;

    border:
        1px solid #E2E8F0;

    border-radius: 19px;

    box-shadow:
        0 8px 22px
        rgba(15,23,42,.045);
}

.progress-icon {
    width: 42px;
    height: 42px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 12px;

    background: #EFF6FF;

    font-size: 21px;

    margin-bottom: 13px;
}

.progress-label {
    color: #94A3B8 !important;

    font-size: 10px !important;

    font-weight: 800;

    letter-spacing: .7px;

    text-transform: uppercase;
}

.progress-value {
    color: #0F172A !important;

    font-size: 27px !important;

    font-weight: 800;

    margin-top: 6px;
}

.progress-description {
    color: #64748B !important;

    font-size: 11px !important;

    margin-top: 5px;
}


/* =========================================================
   PROFILE SNAPSHOT
   ========================================================= */

.snapshot-grid {
    display: grid;

    grid-template-columns:
        1.35fr .65fr;

    gap: 18px;
}

.snapshot-card {
    background: #FFFFFF;

    border:
        1px solid #E2E8F0;

    border-radius: 20px;

    padding: 24px;

    box-shadow:
        0 8px 22px
        rgba(15,23,42,.045);
}

.snapshot-title {
    color: #0F172A !important;

    font-size: 18px !important;

    font-weight: 800;
}

.snapshot-subtitle {
    color: #64748B !important;

    font-size: 12px !important;

    margin-top: 5px;
}

.snapshot-row {
    display: grid;

    grid-template-columns:
        repeat(2, minmax(0,1fr));

    gap: 12px;

    margin-top: 18px;
}

.snapshot-item {
    padding: 14px;

    border-radius: 14px;

    background: #F8FAFC;

    border:
        1px solid #EEF2F7;
}

.snapshot-item-label {
    color: #94A3B8 !important;

    font-size: 10px !important;

    font-weight: 800;

    text-transform: uppercase;
}

.snapshot-item-value {
    color: #0F172A !important;

    font-size: 14px !important;

    font-weight: 700;

    margin-top: 5px;
}


/* =========================================================
   CONTINUE LEARNING
   ========================================================= */

.learning-grid {
    display: grid;

    grid-template-columns:
        repeat(2, minmax(0,1fr));

    gap: 18px;
}

.learning-card {
    display: flex;

    align-items: center;

    gap: 18px;

    min-height: 130px;

    padding: 22px;

    background: #FFFFFF;

    border:
        1px solid #E2E8F0;

    border-radius: 20px;

    box-shadow:
        0 8px 22px
        rgba(15,23,42,.045);
}

.learning-icon {
    width: 58px;
    height: 58px;

    flex-shrink: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 17px;

    background: #EFF6FF;

    font-size: 28px;
}

.learning-title {
    color: #0F172A !important;

    font-size: 17px !important;

    font-weight: 800;
}

.learning-description {
    color: #64748B !important;

    font-size: 12px !important;

    line-height: 1.6;

    margin-top: 5px;
}


/* =========================================================
   DAILY PLAN CARD
   ========================================================= */

.daily-plan {
    background:
        linear-gradient(
            135deg,
            #0F172A,
            #1E293B
        );

    border-radius: 22px;

    padding: 26px;

    margin-top: 18px;

    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 20px;
}

.daily-plan-label {
    color: #818CF8 !important;

    font-size: 10px !important;

    font-weight: 800;

    letter-spacing: 1px;
}

.daily-plan-title {
    color: #FFFFFF !important;

    font-size: 22px !important;

    font-weight: 800;

    margin-top: 7px;
}

.daily-plan-text {
    color: #CBD5E1 !important;

    font-size: 12px !important;

    margin-top: 5px;
}

.daily-plan-icon {
    width: 54px;
    height: 54px;

    flex-shrink: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 16px;

    background: #FFFFFF;

    font-size: 26px;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 1050px) {

    .quick-grid {
        grid-template-columns:
            repeat(2, 1fr);
    }

    .progress-grid {
        grid-template-columns:
            repeat(2, 1fr);
    }

    .snapshot-grid {
        grid-template-columns:
            1fr;
    }
}

@media (max-width: 700px) {

    .school-hero {
        padding:
            30px 24px;
    }

    .school-hero h1 {
        font-size:
            33px !important;
    }

    .school-search-wrapper {
        margin:
            -24px 12px 25px 12px;
    }

    .quick-grid,
    .progress-grid,
    .snapshot-row,
    .learning-grid {
        grid-template-columns:
            1fr;
    }

}
/* =========================================================
   DASHBOARD OVERVIEW
   ========================================================= */

.dashboard-metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 17px;
    margin-bottom: 18px;
}

.dashboard-metric-card {
    min-height: 155px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 19px;
    padding: 20px;

    box-shadow:
        0 8px 24px
        rgba(15,23,42,.045);
}

.dashboard-metric-icon {
    width: 42px;
    height: 42px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 12px;

    background: #EFF6FF;

    font-size: 21px;

    margin-bottom: 12px;
}

.dashboard-metric-label {
    color: #94A3B8 !important;

    font-size: 10px !important;

    font-weight: 800;

    letter-spacing: .7px;

    text-transform: uppercase;
}

.dashboard-metric-value {
    color: #0F172A !important;

    font-size: 25px !important;

    font-weight: 800;

    margin-top: 6px;
}

.dashboard-metric-description {
    color: #64748B !important;

    font-size: 11px !important;

    line-height: 1.5;

    margin-top: 5px;
}


/* =========================================================
   DASHBOARD DETAILS
   ========================================================= */

.dashboard-detail-grid {
    display: grid;

    grid-template-columns:
        1.3fr .7fr;

    gap: 18px;

    margin-top: 18px;
}

.dashboard-panel {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 20px;

    padding: 23px;

    box-shadow:
        0 8px 24px
        rgba(15,23,42,.045);
}

.dashboard-panel-heading {
    color: #0F172A !important;

    font-size: 18px !important;

    font-weight: 800;
}

.dashboard-panel-subtitle {
    color: #64748B !important;

    font-size: 12px !important;

    margin-top: 4px;
}

.dashboard-info-grid {
    display: grid;

    grid-template-columns:
        repeat(2, minmax(0,1fr));

    gap: 12px;

    margin-top: 18px;
}

.dashboard-info-item {
    padding: 14px;

    border-radius: 14px;

    background: #F8FAFC;

    border: 1px solid #EDF2F7;
}

.dashboard-info-item span,
.dashboard-goal-box span {
    display: block;

    color: #94A3B8 !important;

    font-size: 10px !important;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: .5px;
}

.dashboard-info-item strong,
.dashboard-goal-box strong {
    display: block;

    color: #0F172A !important;

    font-size: 14px !important;

    margin-top: 5px;
}

.dashboard-goal-box {
    margin-top: 13px;

    padding: 14px;

    border-radius: 14px;

    background:
        linear-gradient(
            135deg,
            #F8FAFC,
            #F4F7FB
        );

    border:
        1px solid #EDF2F7;
}


@media (max-width: 1050px) {

    .dashboard-metric-grid {
        grid-template-columns:
            repeat(2, 1fr);
    }

    .dashboard-detail-grid {
        grid-template-columns:
            1fr;
    }

}

@media (max-width: 700px) {

    .dashboard-metric-grid,
    .dashboard-info-grid {
        grid-template-columns:
            1fr;
    }

}

</style>
""",
        unsafe_allow_html=True
    )