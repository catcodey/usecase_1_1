import vertexai
from vertexai.generative_models import GenerativeModel

class TranscriptAI:
    def __init__(self, project_id, location):
        
        vertexai.init(project=project_id, location=location)
        
        self.model = GenerativeModel(
            "gemini-2.0-flash",
            system_instruction="Keep every response extremely brief. Summaries must be 5 short bullets. All follow-ups under 50 words."
        )

    def start_new_chat(self):
        return self.model.start_chat()
