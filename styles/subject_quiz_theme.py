import streamlit as st


def apply_subject_quiz_theme():

    st.markdown(
        """
<style>

.quiz-hero {
    padding: 36px 40px;
    border-radius: 24px;
    background: linear-gradient(135deg,#EEF2FF,#ECFEFF);
    border: 1px solid #DDE7F5;
    box-shadow: 0 12px 34px rgba(15,23,42,.05);
    margin-bottom: 24px;
}

.quiz-eyebrow {
    color: #4F46E5 !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.quiz-title {
    color: #0F172A !important;
    font-size: 35px !important;
    font-weight: 800;
    margin-top: 7px;
}

.quiz-description {
    color: #64748B !important;
    font-size: 14px !important;
    line-height: 1.7;
    max-width: 850px;
    margin-top: 8px;
}

.quiz-subject-card {
    padding: 20px;
    min-height: 145px;
    border-radius: 18px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    box-shadow: 0 7px 20px rgba(15,23,42,.04);
}

.quiz-subject-title {
    color: #0F172A !important;
    font-size: 17px !important;
    font-weight: 800;
}

.quiz-subject-meta {
    color: #64748B !important;
    font-size: 11px !important;
    line-height: 1.6;
    margin-top: 6px;
}

.quiz-question-card {
    padding: 19px 21px;
    margin-top: 13px;
    border-radius: 17px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    box-shadow: 0 5px 15px rgba(15,23,42,.03);
}

.quiz-question-number {
    color: #4F46E5 !important;
    font-size: 10px !important;
    font-weight: 800;
    letter-spacing: .7px;
}

.quiz-question-text {
    color: #0F172A !important;
    font-size: 16px !important;
    font-weight: 700;
    line-height: 1.55;
    margin-top: 5px;
}

.quiz-difficulty {
    display: inline-block;
    margin-top: 8px;
    padding: 4px 8px;
    border-radius: 999px;
    background: #F1F5F9;
    color: #475569 !important;
    font-size: 9px !important;
    font-weight: 700;
}

.quiz-result-card {
    padding: 25px;
    border-radius: 22px;
    background: linear-gradient(135deg,#F0FDF4,#EFF6FF);
    border: 1px solid #D1FAE5;
    margin-bottom: 22px;
}

.quiz-result-score {
    color: #0F172A !important;
    font-size: 36px !important;
    font-weight: 900;
}

.quiz-result-label {
    color: #64748B !important;
    font-size: 12px !important;
    margin-top: 4px;
}

.quiz-review-correct {
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #BBF7D0;
    background: #F0FDF4;
    margin-top: 10px;
}

.quiz-review-wrong {
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #FECACA;
    background: #FEF2F2;
    margin-top: 10px;
}

.quiz-review-title {
    color: #0F172A !important;
    font-size: 13px !important;
    font-weight: 800;
}

.quiz-review-text {
    color: #475569 !important;
    font-size: 11px !important;
    line-height: 1.6;
    margin-top: 5px;
}

</style>
""",
        unsafe_allow_html=True,
    )
