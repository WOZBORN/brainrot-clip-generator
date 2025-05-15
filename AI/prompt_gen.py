import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.environ.get("OPENROUTER_API_KEY"),
)

def generate_brainrot_prompt() -> dict:
  completion = client.chat.completions.create(
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=[
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  )
  return completion.choices[0].message.content