import os

from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.environ.get("API_PASSWORD")
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
BRAINROT_GEN_PROMPT = """
Придумай необычный гибрид предмета и животного. Это должен быть полный синтез животного и предмета. Опиши его максимально подробно в формате промта для Midjourney. Пример: «Бомбардиро Крокодило — крокодил с крыльями истребителя, камуфляжной окраской и реактивными двигателями вместо лап». Каждый раз формируй уникальный объект в формате JSON со строго следующей структурой:

{
  "name": "<короткое, броское русское имя персонажа>",
  "italian_name": "<итальянская адаптация имени>",
  "image_prompt": "Нарисуй <русское имя>: <антропоморфный или фэнтези-персонаж> в полный рост, <описание места>, с <необычный атрибут или предмет>, в <стильная одежда или стилистика>, <дополнительные детали>. 3D на английском",
  "phrase": "<развёрнутая история на итальянском: 1 абзац, раскрывающая характер и окружение героя>"
}

Правила генерации:
1. «name» — по-русски, 1–3 слова, отражает суть персонажа.
2. «italian_name» — перевод или созвучная адаптация «name» на итальянский.
3. «image_prompt» — яркое, чёткое описание для нейросети. Каждый раз меняй среду, предметы (могут быть любыми), форму (может быть любой), но сохраняй формат «Нарисуй… 3D». 
4. «phrase» — развернутый текст на итальянском, 1 абзац. Расскажи предысторию, привычки или мечты героя, добавь эмоций и деталей.
5. JSON строго соблюдай: кавычки, запятые и формат — без ошибок.

Пример с учётом новых требований:

```json
{
  "name": "Археомедузо",
  "italian_name": "Archeomedusa",
  "image_prompt": "A surreal hybrid creature called "Yupigruton the Grand" — a colossal space pig with Jupiter-like swirling gas patterns in amber, gold, and pink across its spherical body; cyclone eyes crackling with lightning; a translucent gaseous trunk emitting meteor dust; gravitational metal hooves; baby piglets orbiting as moons with glowing rings; antenna ears absorbing cosmic waves; space-time bending breath; bacon ion trail, hyper-realistic cosmic fantasy art, 8k, concept art, galactic scale, majestic and terrifying, cinematic lighting --v 6 --ar 1:1 --style surreal 3D",
  "phrase": "Archeomedusa esplora i misteri sottomarini con una curiosità senza limiti. Figlia delle correnti oceaniche, ha imparato a leggere geroglifici incisi su colonne sommerse e a decifrare antichi codici custoditi nelle conchiglie più rare. "
}
```
"""


CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
TOKEN_PATH = 'token.json'

# ----------------- Параметры для загрузки -----------------
FILE_PATH   = "output.mp4"          # путь к .mp4 (≤60 сек)
TITLE       = "Мой 2"                       # заголовок ролика
DESCRIPTION = "Краткое описание видео"          # описание ролика
TAGS        = ["shorts", "пример", "2025"]      # список тегов
PRIVACY     = "public"                        # опции: "public", "unlisted", "private"
# ---------------------------------------------------------