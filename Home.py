import streamlit as st

st.set_page_config(
    page_title="Hype Personal Dashboard",
    page_icon="🏠",
)

st.session_state.otp_code = False

st.title('Hype Personal Dashboard')

st.markdown(
    """
    **Hello User, this is a WebApp for Hype card owners.**
"""    
)