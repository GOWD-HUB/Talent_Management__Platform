import streamlit as st


def quick_card(
    icon,
    title,
    description,
    color_class="card-purple"
):

    html = (
        f'<div class="quick-card {color_class}">'
        f'<div class="quick-icon">{icon}</div>'
        f'<div class="quick-title">{title}</div>'
        f'<div class="quick-desc">{description}</div>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def school_stat(
    title,
    value,
    description
):

    html = (
        '<div class="school-stat">'
        f'<div class="school-stat-label">{title}</div>'
        f'<div class="school-stat-value">{value}</div>'
        f'<div class="school-stat-sub">{description}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def feature_card(
    icon,
    title,
    description
):

    quick_card(
        icon,
        title,
        description,
        "card-blue"
    )


def metric_card(
    title,
    value,
    description=""
):

    school_stat(
        title,
        value,
        description
    )