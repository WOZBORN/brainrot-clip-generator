from AI.prompt_gen import generate_brainrot_prompt
from AI.image_gen import generate_image
from AI.voice_gen import generate_voice
from utils import assemble_video_pieces
from concurrent.futures import ThreadPoolExecutor

def pipeline_task():
    # 1) Генерируем промпт
    prompt = generate_brainrot_prompt()

    # 2) Параллельно создаём картинку и аудио
    with ThreadPoolExecutor() as ex:
        video_fut = ex.submit(ge, prompt)
        aud_fut = ex.submit(generate_voice, prompt)
        video_path = "img_fut.result()"
        audio_path = aud_fut.result()
        music_path = "resources/music.mp3"

    # 3) Склеиваем видео через ffmpeg
    assemble_video_pieces()
