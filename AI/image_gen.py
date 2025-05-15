import base64
from openai import OpenAI

def generate_image(prompt: str):
    client = OpenAI()
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        n=1,
        quality="low",
        size="1024x1024"
    )
    img_bytes = base64.b64decode(resp.data[0].b64_json)

    with open("output.png", "wb") as f:
        f.write(img_bytes)

    return "output.png"
