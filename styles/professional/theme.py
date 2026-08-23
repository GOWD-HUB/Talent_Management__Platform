import streamlit as st


def apply_professional_theme():
    st.markdown(
        """
        <style>
        :root{
            --pro-navy:#0f172a;
            --pro-slate:#475569;
            --pro-border:#e2e8f0;
            --pro-blue:#2563eb;
            --pro-indigo:#4f46e5;
            --pro-violet:#7c3aed;
            --pro-bg:#f6f8fc;
        }

        .stApp{
            background:#f6f8fc;
        }

        .block-container{
            max-width:1180px;
            padding-top:2rem;
            padding-bottom:4rem;
        }

        .pro-hero{
            position:relative;
            overflow:hidden;
            background:linear-gradient(135deg,#0f172a 0%,#1e3a8a 48%,#4f46e5 100%);
            color:#fff;
            border-radius:28px;
            padding:36px 40px;
            margin-bottom:24px;
            box-shadow:0 18px 50px rgba(30,58,138,.18);
        }

        .pro-hero:after{
            content:"";
            position:absolute;
            width:210px;
            height:210px;
            border-radius:50%;
            right:-65px;
            top:-70px;
            background:rgba(255,255,255,.08);
            border:25px solid rgba(255,255,255,.06);
        }

        .pro-badge{
            display:inline-block;
            padding:7px 13px;
            border-radius:999px;
            border:1px solid rgba(255,255,255,.28);
            background:rgba(255,255,255,.11);
            font-size:11px;
            font-weight:800;
            letter-spacing:.08em;
            margin-bottom:15px;
        }

        .pro-title{
            color:#fff !important;
            font-size:36px;
            line-height:1.18;
            font-weight:900;
            margin:0;
        }

        .pro-desc{
            max-width:900px;
            color:rgba(255,255,255,.88);
            font-size:14px;
            line-height:1.7;
            margin-top:12px;
        }

        .pro-section{
            display:flex;
            align-items:flex-end;
            justify-content:space-between;
            gap:16px;
            margin:30px 0 14px 0;
        }

        .pro-section-title{
            font-size:25px;
            line-height:1.2;
            font-weight:900;
            color:#0f172a;
        }

        .pro-section-sub{
            color:#64748b;
            font-size:13px;
            margin-top:5px;
        }

        .pro-tag{
            padding:7px 11px;
            border-radius:999px;
            background:#eef2ff;
            color:#4f46e5;
            border:1px solid #e0e7ff;
            font-size:11px;
            font-weight:800;
            white-space:nowrap;
        }

        .pro-grid{
            display:grid;
            grid-template-columns:repeat(4,minmax(0,1fr));
            gap:14px;
            margin:16px 0 18px 0;
        }

        .pro-card{
            background:#fff;
            border:1px solid #e2e8f0;
            border-radius:20px;
            padding:20px;
            box-shadow:0 8px 24px rgba(15,23,42,.04);
        }

        .pro-card-icon{
            width:42px;
            height:42px;
            border-radius:13px;
            display:flex;
            align-items:center;
            justify-content:center;
            background:#eef2ff;
            font-size:21px;
            margin-bottom:13px;
        }

        .pro-label{
            color:#94a3b8;
            font-size:10px;
            font-weight:900;
            letter-spacing:.09em;
        }

        .pro-value{
            color:#0f172a;
            font-size:24px;
            line-height:1.2;
            font-weight:900;
            margin-top:7px;
            overflow-wrap:anywhere;
        }

        .pro-caption{
            color:#64748b;
            font-size:11px;
            line-height:1.55;
            margin-top:7px;
        }

        .pro-mini-grid{
            display:grid;
            grid-template-columns:repeat(3,minmax(0,1fr));
            gap:14px;
        }

        .pro-chip{
            display:inline-block;
            margin:4px 5px 4px 0;
            padding:7px 11px;
            border-radius:999px;
            background:#eef2ff;
            color:#4338ca;
            border:1px solid #e0e7ff;
            font-size:11px;
            font-weight:750;
        }

        .pro-success{
            background:#ecfdf5;
            color:#047857;
            border-color:#a7f3d0;
        }

        .pro-warning{
            background:#fff7ed;
            color:#c2410c;
            border-color:#fed7aa;
        }

        .pro-danger{
            background:#fef2f2;
            color:#b91c1c;
            border-color:#fecaca;
        }

        .pro-panel{
            background:#fff;
            border:1px solid #e2e8f0;
            border-radius:22px;
            padding:22px;
            box-shadow:0 8px 24px rgba(15,23,42,.035);
        }

        .pro-row{
            background:#fff;
            border:1px solid #e2e8f0;
            border-radius:17px;
            padding:17px 19px;
            margin-bottom:10px;
            box-shadow:0 5px 16px rgba(15,23,42,.03);
        }

        .pro-row-kicker{
            color:#4f46e5;
            font-size:10px;
            font-weight:900;
            letter-spacing:.09em;
        }

        .pro-row-title{
            color:#0f172a;
            font-size:16px;
            font-weight:850;
            margin-top:5px;
        }

        .pro-row-sub{
            color:#64748b;
            font-size:12px;
            line-height:1.65;
            margin-top:5px;
        }

        div[data-testid="stButton"]>button,
        div[data-testid="stDownloadButton"]>button,
        div[data-testid="stLinkButton"]>a{
            border-radius:12px !important;
            font-weight:800 !important;
            min-height:44px;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-baseweb="select"] > div{
            border-radius:12px !important;
        }

        @media(max-width:900px){
            .pro-grid{grid-template-columns:repeat(2,minmax(0,1fr));}
            .pro-mini-grid{grid-template-columns:1fr;}
        }

        @media(max-width:600px){
            .pro-grid{grid-template-columns:1fr;}
            .pro-hero{padding:28px 24px;}
            .pro-title{font-size:30px;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title, description, badge="PROFESSIONAL WORKSPACE"):
    st.html(
        f"""<div class="pro-hero">
        <div class="pro-badge">{badge}</div>
        <div class="pro-title">{title}</div>
        <div class="pro-desc">{description}</div>
        </div>"""
    )


def section(title, subtitle="", tag=""):
    tag_html = f'<div class="pro-tag">{tag}</div>' if tag else ""
    st.html(
        f"""<div class="pro-section">
        <div>
            <div class="pro-section-title">{title}</div>
            <div class="pro-section-sub">{subtitle}</div>
        </div>
        {tag_html}
        </div>"""
    )


def metrics(cards):
    html_cards = []
    for card in cards:
        icon, label, value, caption = card
        html_cards.append(
            f"""<div class="pro-card">
            <div class="pro-card-icon">{icon}</div>
            <div class="pro-label">{label}</div>
            <div class="pro-value">{value}</div>
            <div class="pro-caption">{caption}</div>
            </div>"""
        )
    st.html('<div class="pro-grid">' + "".join(html_cards) + '</div>')
