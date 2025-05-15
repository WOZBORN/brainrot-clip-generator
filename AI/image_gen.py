import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.proxyapi.ru/openai/v1"
)

def generate_image(prompt: str):
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        n=1,
        quality="low",
        size="1024x1024"
    )
    return resp.data[0].b64_json
