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

    def summarize_chunks(self, chunks):
        """The Map-Reduce implementation"""
        # 1. MAP STAGE: Summarize each chunk independently
        chunk_summaries = []
        for chunk in chunks:
            response = self.model.generate_content(f"Summarize this section briefly:\n\n{chunk}")
            chunk_summaries.append(response.text)
        
        # 2. REDUCE STAGE: Combine summaries into the final 5 points
        combined_text = "\n\n".join(chunk_summaries)
        
        # We use a fresh chat session for the final reduction to ensure focus
        reduction_chat = self.start_new_chat()
        final_response = reduction_chat.send_message(
            f"Below are summaries of a long transcript. Combine them into a final cohesive 5-point summary:\n\n{combined_text}"
        )
        
        # Return the final summary and the active chat session for follow-ups
        return final_response.text, reduction_chat
