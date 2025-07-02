import openai
from config import OPENAI_API_KEY

class GPTClient:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def generate_checkin_script(self, date_str: str) -> str:
        """
        Build and send a prompt to GPT-4, returning the check-in text.
        """
        # TODO: implement prompt template and API call
        return "GPT-generated script"