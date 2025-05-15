import os

from dotenv import load_dotenv
from openai import OpenAI

from config import BRAINROT_GEN_PROMPT

load_dotenv()

client = OpenAI(
  base_url="https://api.proxyapi.ru/openai/v1",
  api_key=os.environ.get("OPENROUTER_API_KEY"),
)

def generate_brainrot_prompt() -> str:
  # completion = client.chat.completions.create(
  #   model="gpt-4o",
  #   messages=[
  #     {
  #       "role": "user",
  #       "content": BRAINROT_GEN_PROMPT
  #     }
  #   ]
  # )
  return """{  
  "name": "Космокот",  
  "italian_name": "Gatto Cosmico",  
  "image_prompt": "Нарисуй Космокота: футуристического кота-астронавта в полный рост, парящего в невесомости среди звёзд, с прозрачным шлемом, наполненным мерцающими галактиками, и реактивными ботинками, оставляющими светящийся след. На его груди — мини-экран с картой Вселенной. 3D",  
  "phrase": "Gatto Cosmico è l’esploratore più audace della Via Lattea. Nato su una stazione spaziale, ha viaggiato attraverso nebulose e buchi neri, collezionando stelle come souvenir. Il suo sogno? Trovare la leggendaria Pianeta dei Topi, dove si dice che il formaggio sia eterno."  
}"""