import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

class TranscriptAI:
    def __init__(self, project_id, location):
        if "gcp_service_account" in st.secrets:
            creds_info = st.secrets["gcp_service_account"]
            credentials = service_account.Credentials.from_service_account_info(creds_info)
            vertexai.init(project=project_id, location=location, credentials=credentials)
        else:
            st.error("GCP Credentials 'gcp_service_account' not found in Streamlit Secrets!")
            st.stop()
        
        self.model = GenerativeModel("gemini-2.0-flash")

    def start_new_chat(self):
        return self.model.start_chat()
