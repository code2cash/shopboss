import logging
import requests
import streamlit as st
import json
import os

logging.basicConfig(level=logging.DEBUG)

class MailwizzAPI:
    def __init__(self, instance_name, api_url, public_key, secret_key, list_id):
        self.instance_name = instance_name
        self.api_url = api_url.rstrip('/').rstrip('/api')
        if not self.api_url.endswith('/api'):
            self.api_url += '/api'
        self.public_key = public_key
        self.secret_key = secret_key
        self.list_id = list_id
        logging.debug(f"Initialized MailwizzAPI instance: {instance_name}")
        logging.debug(f"API URL: {self.api_url}")

    def test_connection(self):
        try:
            url = f"{self.api_url}/lists/{self.list_id}"
            headers = {
                'X-MW-PUBLIC-KEY': self.public_key,
                'X-MW-PRIVATE-KEY': self.secret_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            logging.debug(f"Testing connection to URL: {url}")
            logging.debug(f"Headers: {headers}")
            response = requests.get(url, headers=headers)
            logging.debug(f"API response status code: {response.status_code}")
            logging.debug(f"API response content: {response.text}")
            if response.status_code == 200:
                return True, "Connection successful"
            else:
                return False, f"Connection failed with status: {response.status_code}. Response: {response.text}"
        except Exception as e:
            logging.exception("Error in test_connection:")
            return False, f"Connection failed with error: {str(e)}"

    def get_list_data(self):
        try:
            url = f"{self.api_url}/lists/{self.list_id}"
            headers = {
                'X-MW-PUBLIC-KEY': self.public_key,
                'X-MW-PRIVATE-KEY': self.secret_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            logging.debug(f"Fetching list data from URL: {url}")
            response = requests.get(url, headers=headers)
            logging.debug(f"API response status code: {response.status_code}")
            logging.debug(f"API response content: {response.text}")
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to fetch list data. Status code: {response.status_code}")
                return None
        except Exception as e:
            logging.exception("Error in get_list_data:")
            return None

def render_mailwizz_section():
    st.title("Mailwizz Integration")

    # Load existing instances
    if 'mailwizz_instances' not in st.session_state:
        st.session_state.mailwizz_instances = {}

    # Add new instance form
    st.subheader("Add New Mailwizz Instance")
    instance_name = st.text_input("Instance Name")
    api_url = st.text_input("API URL")
    public_key = st.text_input("Public Key")
    secret_key = st.text_input("Secret Key")
    list_id = st.text_input("List ID")

    if st.button("Add Instance"):
        if instance_name and api_url and public_key and secret_key and list_id:
            new_instance = MailwizzAPI(instance_name, api_url, public_key, secret_key, list_id)
            success, message = new_instance.test_connection()
            if success:
                st.session_state.mailwizz_instances[instance_name] = new_instance
                st.success(f"Instance '{instance_name}' added successfully!")
            else:
                st.error(f"Failed to add instance: {message}")
        else:
            st.warning("Please fill in all fields.")

    # Display existing instances
    st.subheader("Existing Mailwizz Instances")
    for name, instance in st.session_state.mailwizz_instances.items():
        st.write(f"Instance: {name}")
        if st.button(f"Fetch List Data for {name}"):
            list_data = instance.get_list_data()
            if list_data:
                st.json(list_data)
            else:
                st.error(f"Failed to fetch list data for {name}")

if __name__ == "__main__":
    render_mailwizz_section()
