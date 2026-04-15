 # openai_client.py


from openai import OpenAI, APIConnectionError, APITimeoutError
from config import OPENAI_API_KEY
import time

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_llm(prompt: str, retries=3):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a traceability data analysis agent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                timeout=30
            )
            return response.choices[0].message.content

        except (APIConnectionError, APITimeoutError) as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return "⚠️ LLM service is temporarily unreachable. Please try again."
