import streamlit as st


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

def configure_page():

    st.set_page_config(
        page_title="TalentSphere Elevate",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )


# ==========================================================
# MAIN THEME
# ==========================================================

def load_theme():

    st.markdown(
        """
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

html,
body,
[class*="css"],
.stApp {

    font-family:
        Inter,
        "Segoe UI",
        Arial,
        sans-serif !important;
}


.stApp {

    background:
        linear-gradient(
            180deg,
            #F8FBFF 0%,
            #F4F8FC 100%
        ) !important;

    color:
        #0F172A !important;
}


.main .block-container {

    max-width:
        1380px !important;

    padding-top:
        1.5rem !important;

    padding-left:
        3rem !important;

    padding-right:
        3rem !important;

    padding-bottom:
        4rem !important;
}


/* =========================================================
   HIDE STREAMLIT DEFAULT UI
   ========================================================= */

header[data-testid="stHeader"] {

    display:
        none !important;
}


[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {

    display:
        none !important;
}


#MainMenu {

    display:
        none !important;
}


footer {

    visibility:
        hidden !important;
}


/* =========================================================
   GLOBAL TYPOGRAPHY
   ========================================================= */

h1,
h2,
h3,
h4,
h5,
h6 {

    color:
        #0F172A !important;
}


h1 {

    font-size:
        46px !important;

    font-weight:
        800 !important;
}


h2 {

    font-size:
        36px !important;

    font-weight:
        800 !important;
}


h3 {

    font-size:
        26px !important;

    font-weight:
        750 !important;
}


h4 {

    font-size:
        20px !important;

    font-weight:
        700 !important;
}


p {

    color:
        #475569 !important;

    font-size:
        16px !important;

    line-height:
        1.75;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {

    background:
        #FFFFFF !important;

    border-right:
        1px solid
        #E2E8F0 !important;

    box-shadow:
        6px 0 28px
        rgba(
            15,
            23,
            42,
            0.035
        );
}


section[data-testid="stSidebar"] * {

    color:
        #0F172A !important;
}


/* =========================================================
   SIDEBAR BRAND
   ========================================================= */

.sidebar-brand {

    padding:
        10px
        8px
        24px
        8px;
}


.sidebar-logo {

    width:
        56px;

    height:
        56px;

    border-radius:
        16px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        linear-gradient(
            135deg,
            #E0F2FE,
            #DBEAFE
        );

    font-size:
        29px;

    margin-bottom:
        14px;
}


.sidebar-brand-title {

    color:
        #0F172A !important;

    font-size:
        24px !important;

    font-weight:
        800;
}


.sidebar-brand-subtitle {

    color:
        #64748B !important;

    font-size:
        12px !important;

    margin-top:
        4px;
}


/* =========================================================
   SIDEBAR USER CARD
   ========================================================= */

.sidebar-user-card {

    margin:
        6px
        3px
        20px
        3px;

    padding:
        15px;

    border-radius:
        16px;

    background:
        linear-gradient(
            135deg,
            #EEF2FF,
            #F0F9FF
        );

    border:
        1px solid
        #DCE6F2;
}


.sidebar-user-label {

    color:
        #4F46E5 !important;

    font-size:
        10px !important;

    font-weight:
        800;
}


.sidebar-user-name {

    color:
        #0F172A !important;

    font-size:
        16px !important;

    font-weight:
        800;

    margin-top:
        5px;
}


.sidebar-user-role {

    color:
        #64748B !important;

    font-size:
        12px !important;

    margin-top:
        3px;
}


/* =========================================================
   SIDEBAR NAVIGATION
   ========================================================= */

section[data-testid="stSidebar"]
.stRadio div[role="radiogroup"] {

    gap:
        5px;
}


section[data-testid="stSidebar"]
.stRadio div[role="radiogroup"] > label {

    min-height:
        46px;

    padding:
        9px
        12px;

    border-radius:
        11px;

    border:
        1px solid
        transparent;

    transition:
        all 0.2s ease;
}


section[data-testid="stSidebar"]
.stRadio div[role="radiogroup"] > label:hover {

    background:
        #F1F7FF;
}


section[data-testid="stSidebar"]
.stRadio div[role="radiogroup"]
> label:has(input:checked) {

    background:
        #EAF3FF;

    border-color:
        #CFE1F6;
}


section[data-testid="stSidebar"]
.stRadio [role="radio"] {

    display:
        none !important;
}


section[data-testid="stSidebar"]
.stRadio p {

    color:
        #334155 !important;

    font-size:
        14px !important;

    font-weight:
        600 !important;
}


/* =========================================================
   TOP NAVBAR
   ========================================================= */

.top-navbar {

    min-height:
        72px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    padding:
        12px
        20px;

    margin-bottom:
        24px;

    background:
        rgba(
            255,
            255,
            255,
            0.96
        );

    border:
        1px solid
        #E2E8F0;

    border-radius:
        17px;

    box-shadow:
        0
        8px
        26px
        rgba(
            15,
            23,
            42,
            0.05
        );
}


.top-brand {

    display:
        flex;

    align-items:
        center;

    gap:
        12px;
}


.top-logo {

    width:
        44px;

    height:
        44px;

    border-radius:
        13px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        linear-gradient(
            135deg,
            #2563EB,
            #3B82F6
        );

    color:
        #FFFFFF !important;

    font-size:
        20px;

    font-weight:
        800;
}


.top-brand-name {

    color:
        #0F172A !important;

    font-size:
        19px !important;

    font-weight:
        800;
}


.top-brand-sub {

    color:
        #94A3B8 !important;

    font-size:
        10px !important;

    margin-top:
        2px;
}


/* =========================================================
   LOGGED-IN NAVBAR USER
   ========================================================= */

.top-user-area {

    display:
        flex;

    align-items:
        center;

    gap:
        12px;
}


.top-user-info {

    text-align:
        right;
}


.top-user-name {

    color:
        #0F172A !important;

    font-size:
        14px;

    font-weight:
        700;
}


.top-user-role {

    color:
        #64748B !important;

    font-size:
        11px;

    margin-top:
        2px;
}


.top-user-avatar {

    width:
        42px;

    height:
        42px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        13px;

    background:
        linear-gradient(
            135deg,
            #2563EB,
            #4F46E5
        );

    color:
        #FFFFFF !important;

    font-size:
        16px;

    font-weight:
        800;
}


/* =========================================================
   PUBLIC NAVBAR BUTTONS
   FIXED: BLUE BACKGROUND + WHITE TEXT
   ========================================================= */

div[data-testid="stHorizontalBlock"]
.stButton > button {

    min-height:
        46px !important;

    background:
        linear-gradient(
            135deg,
            #2563EB,
            #3B82F6
        ) !important;

    color:
        #FFFFFF !important;

    border:
        1px solid
        #2563EB !important;

    border-radius:
        12px !important;

    font-size:
        15px !important;

    font-weight:
        700 !important;

    box-shadow:
        0
        6px
        16px
        rgba(
            37,
            99,
            235,
            0.18
        ) !important;

    transition:
        all 0.2s ease !important;
}


div[data-testid="stHorizontalBlock"]
.stButton > button p {

    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;

    font-size:
        15px !important;

    font-weight:
        700 !important;
}


div[data-testid="stHorizontalBlock"]
.stButton > button:hover {

    background:
        linear-gradient(
            135deg,
            #1D4ED8,
            #2563EB
        ) !important;

    color:
        #FFFFFF !important;

    border-color:
        #1D4ED8 !important;

    transform:
        translateY(-2px);

    box-shadow:
        0
        10px
        22px
        rgba(
            37,
            99,
            235,
            0.25
        ) !important;
}


div[data-testid="stHorizontalBlock"]
.stButton > button:hover p {

    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;
}


div[data-testid="stHorizontalBlock"]
.stButton > button:active {

    background:
        #1D4ED8 !important;

    transform:
        translateY(0);
}


div[data-testid="stHorizontalBlock"]
.stButton > button:focus {

    color:
        #FFFFFF !important;

    border-color:
        #2563EB !important;

    box-shadow:
        0
        0
        0
        3px
        rgba(
            37,
            99,
            235,
            0.15
        ) !important;
}


/* =========================================================
   HOME HERO
   ========================================================= */

.home-hero {

    position:
        relative;

    overflow:
        hidden;

    padding:
        58px
        56px;

    min-height:
        390px;

    border-radius:
        28px;

    background:
        radial-gradient(
            circle at 88% 18%,
            rgba(
                255,
                255,
                255,
                0.55
            ),
            transparent 20%
        ),
        radial-gradient(
            circle at 78% 92%,
            rgba(
                125,
                211,
                252,
                0.40
            ),
            transparent 25%
        ),
        linear-gradient(
            120deg,
            #DFF4FF 0%,
            #C9EDFF 48%,
            #A8E1F9 100%
        );

    border:
        1px solid
        #BAE6FD;

    box-shadow:
        0
        20px
        50px
        rgba(
            14,
            116,
            144,
            0.10
        );

    margin-bottom:
        30px;
}


.home-badge {

    display:
        inline-block;

    padding:
        8px
        14px;

    border-radius:
        999px;

    background:
        rgba(
            255,
            255,
            255,
            0.75
        );

    color:
        #075985 !important;

    font-size:
        11px !important;

    font-weight:
        800;

    letter-spacing:
        1px;

    margin-bottom:
        20px;
}


.home-hero h1 {

    max-width:
        900px;

    color:
        #0F172A !important;

    font-size:
        58px !important;

    line-height:
        1.08;

    font-weight:
        800;

    letter-spacing:
        -2px;

    margin:
        0
        0
        20px
        0;
}


.home-hero p {

    max-width:
        820px;

    color:
        #334155 !important;

    font-size:
        17px !important;

    line-height:
        1.75;
}


.home-tags {

    display:
        flex;

    flex-wrap:
        wrap;

    gap:
        10px;

    margin-top:
        24px;
}


.home-tags span {

    padding:
        9px
        14px;

    border-radius:
        999px;

    background:
        rgba(
            255,
            255,
            255,
            0.72
        );

    color:
        #334155 !important;

    font-size:
        13px !important;

    font-weight:
        600;
}


/* =========================================================
   STAT CARDS
   ========================================================= */

.home-stat-card {

    background:
        #FFFFFF;

    border:
        1px solid
        #E2E8F0;

    border-radius:
        18px;

    padding:
        21px;

    text-align:
        center;

    box-shadow:
        0
        8px
        24px
        rgba(
            15,
            23,
            42,
            0.04
        );
}


.home-stat-value {

    color:
        #0F172A !important;

    font-size:
        32px !important;

    font-weight:
        800;
}


.home-stat-label {

    color:
        #64748B !important;

    font-size:
        11px !important;

    font-weight:
        800;

    margin-top:
        5px;

    text-transform:
        uppercase;
}


/* =========================================================
   SECTION HEADER
   ========================================================= */

.home-section-header {

    margin:
        50px
        0
        24px
        0;
}


.home-section-header span {

    color:
        #2563EB !important;

    font-size:
        11px !important;

    font-weight:
        800;

    letter-spacing:
        1.2px;
}


.home-section-header h2 {

    color:
        #0F172A !important;

    font-size:
        40px !important;

    font-weight:
        800;

    margin:
        7px
        0
        10px
        0;
}


.home-section-header p {

    color:
        #64748B !important;

    font-size:
        15px !important;

    max-width:
        760px;
}


/* =========================================================
   CAREER STAGE GRID
   ========================================================= */

.career-stage-grid {

    display:
        grid;

    grid-template-columns:
        repeat(
            3,
            1fr
        );

    gap:
        22px;

    margin-top:
        20px;
}


.career-stage-card {

    min-height:
        390px;

    display:
        flex;

    flex-direction:
        column;

    background:
        #FFFFFF;

    border:
        1px solid
        #E2E8F0;

    border-radius:
        23px;

    padding:
        28px;

    box-shadow:
        0
        12px
        32px
        rgba(
            15,
            23,
            42,
            0.05
        );

    transition:
        0.2s ease;
}


.career-stage-card:hover {

    transform:
        translateY(-5px);

    border-color:
        #93C5FD;

    box-shadow:
        0
        20px
        42px
        rgba(
            37,
            99,
            235,
            0.10
        );
}


.school-stage {

    border-top:
        4px solid
        #8B5CF6;
}


.college-stage {

    border-top:
        4px solid
        #3B82F6;
}


.professional-stage {

    border-top:
        4px solid
        #10B981;
}


.stage-top {

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    margin-bottom:
        20px;
}


.stage-icon {

    width:
        58px;

    height:
        58px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        16px;

    font-size:
        28px;
}


.school-icon {

    background:
        #F3EEFF;
}


.college-icon {

    background:
        #EAF4FF;
}


.professional-icon {

    background:
        #EAF9F1;
}


.stage-number {

    color:
        #94A3B8 !important;

    font-size:
        14px !important;

    font-weight:
        800;
}


.career-stage-card h3 {

    color:
        #0F172A !important;

    font-size:
        26px !important;

    font-weight:
        800;

    margin-bottom:
        12px;
}


.career-stage-card p {

    color:
        #64748B !important;

    font-size:
        15px !important;

    line-height:
        1.7;
}


.stage-features {

    margin-top:
        17px;

    flex-grow:
        1;
}


.stage-features div {

    color:
        #334155 !important;

    font-size:
        14px !important;

    margin-bottom:
        11px;
}


.stage-footer {

    margin-top:
        20px;

    padding-top:
        17px;

    border-top:
        1px solid
        #E2E8F0;

    color:
        #2563EB !important;

    font-size:
        14px !important;

    font-weight:
        700;
}


/* =========================================================
   CAPABILITY GRID
   ========================================================= */

.capability-grid {

    display:
        grid;

    grid-template-columns:
        repeat(
            4,
            1fr
        );

    gap:
        18px;

    margin-top:
        20px;
}


.capability-card {

    min-height:
        190px;

    background:
        #FFFFFF;

    border:
        1px solid
        #E2E8F0;

    border-radius:
        20px;

    padding:
        24px;

    box-shadow:
        0
        10px
        28px
        rgba(
            15,
            23,
            42,
            0.04
        );
}


.capability-icon {

    width:
        48px;

    height:
        48px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        14px;

    background:
        #EFF6FF;

    font-size:
        24px;

    margin-bottom:
        16px;
}


.capability-card h4 {

    color:
        #0F172A !important;

    font-size:
        19px !important;

    font-weight:
        750;

    margin-bottom:
        8px;
}


.capability-card p {

    color:
        #64748B !important;

    font-size:
        14px !important;

    line-height:
        1.65;
}


/* =========================================================
   PROFILE HEADER
   ========================================================= */

.profile-header {

    padding:
        34px
        38px;

    border-radius:
        24px;

    margin-bottom:
        26px;

    background:
        linear-gradient(
            120deg,
            #E0F2FE,
            #DBEAFE
        );

    border:
        1px solid
        #BFDBFE;
}


.profile-header h1 {

    color:
        #0F172A !important;

    font-size:
        40px !important;

    font-weight:
        800;

    margin-bottom:
        8px;
}


.profile-header p {

    color:
        #475569 !important;

    font-size:
        16px !important;
}


/* =========================================================
   GENERIC CARDS
   ========================================================= */

.ts-card {

    background:
        #FFFFFF;

    border:
        1px solid
        #E2E8F0;

    border-radius:
        20px;

    padding:
        25px;

    margin-bottom:
        20px;

    box-shadow:
        0
        10px
        30px
        rgba(
            15,
            23,
            42,
            0.045
        );
}


.ts-card-title {

    color:
        #0F172A !important;

    font-size:
        21px !important;

    font-weight:
        750;

    margin-bottom:
        8px;
}


.ts-card-description {

    color:
        #64748B !important;

    font-size:
        15px !important;

    line-height:
        1.65;
}


/* =========================================================
   INPUTS
   ========================================================= */

.stTextInput label,
.stTextArea label,
.stNumberInput label,
.stSelectbox label,
.stDateInput label,
.stMultiSelect label {

    color:
        #0F172A !important;

    font-size:
        14px !important;

    font-weight:
        700 !important;
}


.stTextInput input,
.stNumberInput input {

    min-height:
        48px !important;

    background:
        #FFFFFF !important;

    color:
        #0F172A !important;

    -webkit-text-fill-color:
        #0F172A !important;

    border:
        1px solid
        #CBD5E1 !important;

    border-radius:
        11px !important;

    font-size:
        15px !important;
}


.stTextArea textarea {

    background:
        #FFFFFF !important;

    color:
        #0F172A !important;

    -webkit-text-fill-color:
        #0F172A !important;

    border:
        1px solid
        #CBD5E1 !important;

    border-radius:
        11px !important;

    font-size:
        15px !important;
}


.stTextInput input::placeholder,
.stTextArea textarea::placeholder {

    color:
        #94A3B8 !important;

    -webkit-text-fill-color:
        #94A3B8 !important;

    opacity:
        1 !important;
}


div[data-baseweb="select"] > div {

    min-height:
        48px;

    background:
        #FFFFFF !important;

    color:
        #0F172A !important;

    border-color:
        #CBD5E1 !important;

    border-radius:
        11px !important;
}


div[data-baseweb="select"] span {

    color:
        #0F172A !important;

    font-size:
        15px !important;
}


/* =========================================================
   GENERAL BUTTONS
   ========================================================= */

.stButton > button,
.stFormSubmitButton > button {

    min-height:
        46px;

    border-radius:
        11px !important;

    padding:
        10px
        22px !important;

    font-size:
        14px !important;

    font-weight:
        700 !important;

    background:
        linear-gradient(
            135deg,
            #2563EB,
            #3B82F6
        ) !important;

    color:
        #FFFFFF !important;

    border:
        none !important;

    box-shadow:
        0
        8px
        20px
        rgba(
            37,
            99,
            235,
            0.18
        );

    transition:
        all 0.20s ease;
}


.stButton > button:hover,
.stFormSubmitButton > button:hover {

    transform:
        translateY(-2px);

    background:
        linear-gradient(
            135deg,
            #1D4ED8,
            #2563EB
        ) !important;

    box-shadow:
        0
        12px
        26px
        rgba(
            37,
            99,
            235,
            0.25
        );
}


.stButton > button p,
.stFormSubmitButton > button p {

    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;

    font-size:
        14px !important;

    font-weight:
        700 !important;
}


/* =========================================================
   DOWNLOAD BUTTON
   ========================================================= */

.stDownloadButton > button {

    min-height:
        46px;

    border-radius:
        11px !important;

    background:
        #0F172A !important;

    color:
        #FFFFFF !important;

    border:
        none !important;

    font-weight:
        700 !important;
}


.stDownloadButton > button p {

    color:
        #FFFFFF !important;
}


/* =========================================================
   TABS
   ========================================================= */

button[data-baseweb="tab"] {

    font-size:
        15px !important;

    font-weight:
        650 !important;

    color:
        #475569 !important;
}


button[data-baseweb="tab"][aria-selected="true"] {

    color:
        #2563EB !important;
}


/* =========================================================
   EXPANDERS
   ========================================================= */

[data-testid="stExpander"] {

    background:
        #FFFFFF !important;

    border:
        1px solid
        #E2E8F0 !important;

    border-radius:
        14px !important;

    overflow:
        hidden;

    margin-bottom:
        12px;
}


[data-testid="stExpander"] summary {

    color:
        #0F172A !important;

    font-size:
        15px !important;

    font-weight:
        700 !important;
}


/* =========================================================
   ALERTS
   ========================================================= */

[data-testid="stAlert"] {

    border-radius:
        13px !important;
}


[data-testid="stAlert"] p {

    color:
        #0F172A !important;

    font-size:
        14px !important;
}


/* =========================================================
   METRICS
   ========================================================= */

[data-testid="stMetric"] {

    background:
        #FFFFFF;

    border:
        1px solid
        #E2E8F0;

    border-radius:
        16px;

    padding:
        18px;
}


[data-testid="stMetricLabel"] {

    color:
        #64748B !important;
}


[data-testid="stMetricValue"] {

    color:
        #0F172A !important;

    font-size:
        30px !important;

    font-weight:
        800 !important;
}


/* =========================================================
   FILE UPLOADER
   ========================================================= */

[data-testid="stFileUploader"] {

    background:
        #FFFFFF;

    border-radius:
        15px;
}


[data-testid="stFileUploader"] section {

    background:
        #F8FAFC !important;

    border:
        1.5px dashed
        #94A3B8 !important;

    border-radius:
        14px !important;
}


[data-testid="stFileUploader"] * {

    color:
        #334155 !important;
}


/* =========================================================
   CHAT
   ========================================================= */

[data-testid="stChatMessage"] {

    background:
        #FFFFFF !important;

    border:
        1px solid
        #E2E8F0 !important;

    border-radius:
        16px !important;

    padding:
        12px;
}


[data-testid="stChatMessage"] p {

    color:
        #0F172A !important;

    font-size:
        15px !important;
}


[data-testid="stChatInput"] textarea {

    background:
        #FFFFFF !important;

    color:
        #0F172A !important;

    -webkit-text-fill-color:
        #0F172A !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.app-footer {

    margin-top:
        55px;

    padding:
        28px
        10px;

    text-align:
        center;

    border-top:
        1px solid
        #E2E8F0;

    color:
        #94A3B8 !important;

    font-size:
        12px !important;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 1050px) {

    .career-stage-grid {

        grid-template-columns:
            1fr;
    }


    .capability-grid {

        grid-template-columns:
            repeat(
                2,
                1fr
            );
    }


    .home-hero h1 {

        font-size:
            46px !important;
    }

}


@media (max-width: 700px) {

    .main .block-container {

        padding-left:
            1rem !important;

        padding-right:
            1rem !important;
    }


    .home-hero {

        padding:
            35px
            24px;
    }


    .home-hero h1 {

        font-size:
            36px !important;
    }


    .home-section-header h2 {

        font-size:
            30px !important;
    }


    .capability-grid {

        grid-template-columns:
            1fr;
    }

}
/* =========================================================
   LOGIN PAGE
   ========================================================= */

.login-page-heading {
    max-width: 650px;
    margin: 25px auto 28px auto;
    text-align: center;
}

.login-page-heading span {
    color: #2563EB !important;
    font-size: 11px !important;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.login-page-heading h1 {
    color: #0F172A !important;
    font-size: 38px !important;
    font-weight: 800;
    margin: 8px 0 8px 0;
}

.login-page-heading p {
    color: #64748B !important;
    font-size: 14px !important;
    margin: 0 auto;
}


.login-card-top {
    display: flex;
    align-items: center;
    gap: 14px;

    padding: 22px 24px;

    background: #FFFFFF;

    border:
        1px solid #E2E8F0;

    border-radius:
        20px 20px 0 0;

    border-bottom: none;
}


.login-icon {
    width: 48px;
    height: 48px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 14px;

    background:
        linear-gradient(
            135deg,
            #EEF2FF,
            #E0F2FE
        );

    font-size: 24px;
}


.login-title {
    color: #0F172A !important;
    font-size: 17px !important;
    font-weight: 800;
}


.login-subtitle {
    color: #64748B !important;
    font-size: 11px !important;
    margin-top: 3px;
}


/* LOGIN FORM CARD */

div[data-testid="stForm"] {
    background: #FFFFFF;

    border:
        1px solid #E2E8F0;

    border-radius:
        0 0 20px 20px;

    padding:
        10px 24px 24px 24px;

    box-shadow:
        0 15px 35px
        rgba(15,23,42,.07);
}


/* LOGIN INPUTS */

div[data-testid="stForm"]
.stTextInput input {

    min-height: 47px !important;

    background:
        #F8FAFC !important;

    color:
        #0F172A !important;

    -webkit-text-fill-color:
        #0F172A !important;

    border:
        1px solid #CBD5E1 !important;

    border-radius:
        10px !important;
}


div[data-testid="stForm"]
.stTextInput input::placeholder {

    color:
        #94A3B8 !important;

    -webkit-text-fill-color:
        #94A3B8 !important;
}


.login-security-note {

    margin-top: 15px;

    padding: 12px 14px;

    border-radius: 11px;

    background: #EFF6FF;

    color: #475569 !important;

    font-size: 11px !important;

    text-align: center;
}


/* =========================================================
   SIDEBAR LOGOUT BUTTON
   ========================================================= */

section[data-testid="stSidebar"]
.stButton > button {

    width: 100%;

    min-height: 44px;

    background:
        #FFF1F2 !important;

    color:
        #BE123C !important;

    border:
        1px solid #FECDD3 !important;

    box-shadow: none !important;

    border-radius: 11px !important;
}


section[data-testid="stSidebar"]
.stButton > button p {

    color:
        #BE123C !important;

    -webkit-text-fill-color:
        #BE123C !important;

    font-weight: 700 !important;
}


section[data-testid="stSidebar"]
.stButton > button:hover {

    background:
        #FFE4E6 !important;

    border-color:
        #FDA4AF !important;

    transform: none !important;
}
</style>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# COMPATIBILITY ALIAS
# ==========================================================

def apply_theme():

    load_theme()