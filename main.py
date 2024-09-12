import streamlit as st
from mailwizz_integration import render_mailwizz_section
from woocommerce_integration import render_woocommerce_insights
from google_analytics_integration import render_google_analytics_section
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    logging.debug("Starting the Streamlit application")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "WooCommerce Insights", "Mailwizz Integration", "Google Analytics"])

    if page == "Home":
        st.title("E-commerce Marketing Dashboard")
        st.write("Welcome to your personalized e-commerce marketing dashboard!")
    elif page == "WooCommerce Insights":
        render_woocommerce_insights()
    elif page == "Mailwizz Integration":
        render_mailwizz_section()
    elif page == "Google Analytics":
        render_google_analytics_section()

if __name__ == "__main__":
    main()
