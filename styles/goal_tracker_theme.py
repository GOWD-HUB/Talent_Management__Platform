import streamlit as st

def apply_goal_tracker_theme():
    st.markdown("""
<style>
.goal-hero{padding:36px 40px;border-radius:24px;background:linear-gradient(135deg,#FFF7ED,#EEF2FF);border:1px solid #E2E8F0;box-shadow:0 12px 34px rgba(15,23,42,.05);margin-bottom:24px}
.goal-eyebrow{color:#EA580C!important;font-size:10px!important;font-weight:800;letter-spacing:1.2px}
.goal-title{color:#0F172A!important;font-size:35px!important;font-weight:850;margin-top:7px}
.goal-description{color:#64748B!important;font-size:14px!important;line-height:1.7;max-width:880px;margin-top:8px}
.goal-summary-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-bottom:20px}
.goal-summary-card{padding:18px;border-radius:17px;background:#FFF;border:1px solid #E2E8F0}
.goal-summary-label{color:#94A3B8!important;font-size:9px!important;font-weight:800;text-transform:uppercase}
.goal-summary-value{color:#0F172A!important;font-size:21px!important;font-weight:850;margin-top:6px}
.goal-card{padding:21px;border-radius:19px;background:#FFF;border:1px solid #E2E8F0;box-shadow:0 7px 20px rgba(15,23,42,.04);margin-top:14px}
.goal-category{color:#7C3AED!important;font-size:9px!important;font-weight:800;text-transform:uppercase;letter-spacing:.7px}
.goal-card-title{color:#0F172A!important;font-size:19px!important;font-weight:850;margin-top:5px}
.goal-card-text{color:#64748B!important;font-size:11px!important;line-height:1.6;margin-top:6px}
.goal-meta{margin-top:10px;color:#475569!important;font-size:10px!important}
.goal-recommendation{padding:18px;border-radius:16px;background:#EFF6FF;border:1px solid #BFDBFE;margin:16px 0 22px 0}
.goal-recommendation-title{color:#1D4ED8!important;font-size:11px!important;font-weight:800}
.goal-recommendation-text{color:#475569!important;font-size:11px!important;line-height:1.6;margin-top:4px}
@media(max-width:850px){.goal-summary-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:550px){.goal-summary-grid{grid-template-columns:1fr}}
</style>
""", unsafe_allow_html=True)
