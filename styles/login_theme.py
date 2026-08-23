import streamlit as st


def apply_login_theme():

    st.markdown(
        """
<style>

/* =========================================================
   LOGIN PAGE SPACING
   ========================================================= */

.auth-card-header {

    margin-top:
        12px;

    padding:
        30px
        32px
        20px
        32px;

    background:
        #FFFFFF;

    border:
        1px solid
        #E2E8F0;

    border-bottom:
        none;

    border-radius:
        22px
        22px
        0
        0;

    text-align:
        center;

    box-shadow:
        0
        16px
        40px
        rgba(15,23,42,.07);
}


/* =========================================================
   LOGO
   ========================================================= */

.auth-logo {

    width:
        56px;

    height:
        56px;

    margin:
        0 auto 15px auto;

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
            #EAF2FF,
            #EDE9FE
        );

    font-size:
        28px;
}


/* =========================================================
   TITLE
   ========================================================= */

.auth-eyebrow {

    color:
        #2563EB !important;

    font-size:
        10px !important;

    font-weight:
        800;

    letter-spacing:
        1.4px;

    margin-bottom:
        8px;
}


.auth-title {

    color:
        #0F172A !important;

    font-size:
        28px !important;

    font-weight:
        800;

    letter-spacing:
        -.7px;
}


.auth-description {

    max-width:
        380px;

    margin:
        8px auto 0 auto;

    color:
        #64748B !important;

    font-size:
        13px !important;

    line-height:
        1.6;
}


/* =========================================================
   FORM
   ========================================================= */

div[data-testid="stForm"] {

    background:
        #FFFFFF;

    border:
        1px solid
        #E2E8F0;

    border-top:
        none;

    border-radius:
        0
        0
        22px
        22px;

    padding:
        8px
        30px
        28px
        30px;

    box-shadow:
        0
        16px
        40px
        rgba(15,23,42,.07);
}


/* =========================================================
   LABELS
   ========================================================= */

div[data-testid="stForm"] label p {

    color:
        #1E293B !important;

    font-size:
        13px !important;

    font-weight:
        700 !important;
}


/* =========================================================
   INPUTS
   ========================================================= */

div[data-testid="stForm"]
.stTextInput input {

    min-height:
        47px !important;

    background:
        #F8FAFC !important;

    color:
        #0F172A !important;

    -webkit-text-fill-color:
        #0F172A !important;

    border:
        1px solid
        #CBD5E1 !important;

    border-radius:
        10px !important;

    padding-left:
        14px !important;

    font-size:
        14px !important;

    box-shadow:
        none !important;
}


div[data-testid="stForm"]
.stTextInput input:focus {

    border:
        1px solid
        #3B82F6 !important;

    box-shadow:
        0
        0
        0
        3px
        rgba(59,130,246,.10) !important;
}


div[data-testid="stForm"]
.stTextInput input::placeholder {

    color:
        #94A3B8 !important;

    -webkit-text-fill-color:
        #94A3B8 !important;

    opacity:
        1 !important;
}


/* =========================================================
   PASSWORD EYE
   ========================================================= */

div[data-testid="stForm"]
button[kind="icon"] {

    background:
        transparent !important;

    border:
        none !important;

    box-shadow:
        none !important;
}


/* =========================================================
   SUBMIT BUTTON
   ========================================================= */

div[data-testid="stForm"]
.stFormSubmitButton > button {

    width:
        100%;

    min-height:
        48px;

    margin-top:
        8px;

    border:
        none !important;

    border-radius:
        11px !important;

    background:
        linear-gradient(
            135deg,
            #2563EB,
            #4F46E5
        ) !important;

    color:
        #FFFFFF !important;

    font-size:
        14px !important;

    font-weight:
        700 !important;

    box-shadow:
        0
        9px
        22px
        rgba(37,99,235,.22) !important;
}


div[data-testid="stForm"]
.stFormSubmitButton > button p {

    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;
}


/* =========================================================
   BACK HOME BUTTON
   ========================================================= */

div[data-testid="stButton"]
button {

    min-height:
        40px !important;

    background:
        #FFFFFF !important;

    color:
        #334155 !important;

    border:
        1px solid
        #E2E8F0 !important;

    border-radius:
        11px !important;

    font-size:
        13px !important;

    font-weight:
        700 !important;

    box-shadow:
        0
        4px
        14px
        rgba(15,23,42,.05) !important;
}


div[data-testid="stButton"]
button p {

    color:
        #334155 !important;

    -webkit-text-fill-color:
        #334155 !important;
}


div[data-testid="stButton"]
button:hover {

    background:
        #EFF6FF !important;

    color:
        #2563EB !important;

    border-color:
        #BFDBFE !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.auth-card-footer {

    margin-top:
        14px;

    text-align:
        center;
}


.auth-security {

    display:
        inline-block;

    padding:
        7px
        12px;

    border-radius:
        999px;

    background:
        #ECFDF5;

    color:
        #047857 !important;

    font-size:
        10px !important;

    font-weight:
        700;
}


.auth-register-message {

    margin-top:
        10px;

    color:
        #64748B !important;

    font-size:
        11px !important;
}


.auth-register-message b {

    color:
        #2563EB !important;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 700px) {

    .auth-card-header {

        margin-top:
            5px;

        padding:
            25px
            20px
            17px
            20px;
    }


    div[data-testid="stForm"] {

        padding:
            5px
            18px
            22px
            18px;
    }


    .auth-title {

        font-size:
            25px !important;
    }

}

</style>
""",
        unsafe_allow_html=True,
    )