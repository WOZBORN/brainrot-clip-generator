import json
import os
import re

from dotenv import load_dotenv

from AI.image_gen import generate_image
from AI.video_gen import VideoService
from AI.prompt_gen import generate_brainrot_prompt
from AI.voice_gen import generate_voice
from utils.ffmpeg_process import merge_with_ffmpeg

load_dotenv()
AK = os.getenv("KLING_AK")
SK = os.getenv("KLING_SK")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

video_service = VideoService(AK, SK)

def main():
    raw = generate_brainrot_prompt()

    clean = re.sub(r'^```(?:json)?\s*', '', raw)
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

    generate_voice(phrase)
    merge_with_ffmpeg(
        video_path="../video.mp4",
        voice_path="voice.mp3",
        music_path="music.mp3",
        out_path="output.mp4"
    )

if __name__ == "__main__":
    main()