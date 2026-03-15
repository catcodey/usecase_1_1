import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

class TranscriptAI:
    def __init__(self, project_id, location, credentials_info=None):
        if credentials_info:
            credentials = service_account.Credentials.from_service_account_info(credentials_info)
            vertexai.init(project=project_id, location=location, credentials=credentials)
        else:
            vertexai.init(project=project_id, location=location)
        
        self.model = GenerativeModel(
            "gemini-2.0-flash",
            system_instruction="Keep every response extremely brief. Summaries must be 5 short bullets. All follow-ups under 50 words."
        )

    def start_new_chat(self):
        return self.model.start_chat()
