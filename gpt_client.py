# gpt_client.py
import openai
from config import OPENAI_API_KEY

class GPTClient:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def generate_checkin_script(self, date_str: str) -> str:
        """
        Ask GPT-4 to produce a dynamic check-in prompt.
        """
        system = {
            "role": "system",
            "content": (
                "You are a friendly but firm accountability coach. "
                "Each day you generate a personalized check-in conversation "
                "asking about the user's goals, moods, habits, and any rule violations."
            )
        }
        user = {
            "role": "user",
            "content": f"Today is {date_str}. Create a check-in script that starts the conversation."
        }
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system, user],
            temperature=0.7,
            max_tokens=200
        )
        return resp.choices[0].message.content.strip()

    def generate_followup(self, script: str, user_reply: str) -> str:
        """
        Given the initial script and the user's reply, ask GPT-4 for the next question or comment.
        """
        system = {
            "role": "system",
            "content": "You are continuing an accountability conversation based on prior context."
        }
        messages = [
            {"role": "assistant", "content": script},
            {"role": "user", "content": user_reply}
        ]
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[system] + messages,
            temperature=0.7,
            max_tokens=150
        )
        return resp.choices[0].message.content.strip()
