import streamlit as st
from mailwizz_integration import MailwizzAPI
from woocommerce_integration import render_woocommerce_insights
from google_analytics_integration import render_google_analytics_section

def render_mailwizz_section():
    st.title("Mailwizz Integration")
    
    api = MailwizzAPI()
    
    if st.button("Test Mailwizz Connection"):
        connection_status, message = api.test_connection()
        if connection_status:
            st.success(message)
        else:
            st.error(message)
    
    if st.button("Get Mailing Lists"):
        response = api.get_lists()
        if response.status_code == 200:
            lists = response.json()['data']['records']
            for list_info in lists:
                st.write(f"List Name: {list_info['name']}, Subscribers: {list_info['subscribers_count']}")
        else:
            st.error("Failed to retrieve mailing lists")

def main():
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
