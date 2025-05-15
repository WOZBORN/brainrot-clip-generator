import json
import os
import re

from dotenv import load_dotenv

from AI.prompt_gen import generate_brainrot_prompt
from AI.image_gen import generate_image
from AI.voice_gen import generate_voice
from concurrent.futures import ThreadPoolExecutor
from AI.video_gen import VideoService
from upload.upload_shorts import upload_short
from utils.ffmpeg_process import make_boomerang_clip, merge_loop_and_audio


def pipeline_task():
    # 1) Генерируем промпт
    load_dotenv()
    AK = os.getenv("KLING_AK")
    SK = os.getenv("KLING_SK")
    print("Generating prompt...")
    prompt = generate_brainrot_prompt()
    print("Prompt generated:", prompt)
    video_service = VideoService(AK, SK)

    # 2) Параллельно создаём картинку и аудио
    with ThreadPoolExecutor() as ex:
        clean = re.sub(r'^```(?:json)?\s*', '', prompt)
        clean = re.sub(r'\s*```$', '', clean)

        data = json.loads(clean)

        name = data["name"]
        italian_name = data["italian_name"]
        img_prompt = data["image_prompt"]
        phrase = data["phrase"]

        image_b64 = generate_image(img_prompt)
        print("Image generated, length of base64:", len(image_b64))

        result = video_service.start_image2video_with_retry(
            image_b64=image_b64,
            prompt=""
        )

        task_id = result.get("task_id") or result.get("data", {}).get("task_id")
        if task_id:
            print("Task started, ID:", task_id)
            saved_files = video_service.poll_status_and_download(task_id)
            print("Downloaded videos:", saved_files)

        generate_voice(f"{italian_name}! {phrase}")
        make_boomerang_clip("video.mp4", "boomerang.mp4")

        # 2) зацикливаем boomerang, микшуем звук и обрезаем
        merge_loop_and_audio("boomerang.mp4", "voice.mp3", "resources/music.mp3", "output.mp4")

        upload_short("output.mp4", name, phrase, "shorts", "public")