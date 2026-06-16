from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()


class LLMGenerator:

    def __init__(self):

        self.client = InferenceClient(
            provider="auto",
            api_key=os.getenv("HF_TOKEN")
        )

        self.model = "meta-llama/Llama-3.3-70B-Instruct"

    def generate(
        self,
        query,
        context,
        current_time
    ):

        prompt = f"""
Current Time:
{current_time}

Question:
{query}

Relevant Events:
{context}

Instructions:
- Answer only from the supplied events
- Mention uncertainty if necessary
- Prioritize recent information
- Mention deadlines and commitments
- Keep the answer concise
"""

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300,
            temperature=0.2
        )

        return completion.choices[0].message.content
