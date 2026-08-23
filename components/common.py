import streamlit as st


def page_header(
    title,
    description=""
):

    html = (
        f'<div class="page-title">'
        f'<h1>{title}</h1>'
        f'<p>{description}</p>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def section_title(title):

    st.markdown(
        f"<h2>{title}</h2>",
        unsafe_allow_html=True
    )