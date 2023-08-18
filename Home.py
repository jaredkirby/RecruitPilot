import streamlit as st

from config.site_config import (
    LAYOUT,
    PAGE_TITLE,
    PAGE_ICON,
    FOOTER,
)

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)
st.markdown(
    f"<h1 style='text-align: center;'>{PAGE_TITLE} {PAGE_ICON}</h1>",
    unsafe_allow_html=True,
)
st.markdown("### this is a site of 🚮 tools")
st.markdown(FOOTER)
