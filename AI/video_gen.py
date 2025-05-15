import time
import requests
from .jwt_gen import encode_jwt_token

class VideoService:
    def __init__(self, ak: str, sk: str):
        self.api_token = encode_jwt_token(ak, sk)
        self.base_url = "https://api.klingai.com/v1/videos/image2video"

    def start_image2video_with_retry(self,
                                     image_b64: str,
                                     prompt: str,
                                     model_name: str = "kling-v2-master",
                                     mode: str = "pro",
                                     duration: int = 10,
                                     cfg_scale: float = 0.5,
                                     max_retries: int = 5,
                                     backoff: int = 5) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "model_name": model_name,
            "mode": mode,
            "duration": str(duration),
            "image": image_b64,
            "prompt": prompt,
            "cfg_scale": cfg_scale
        }
        for attempt in range(max_retries):
            resp = requests.post(self.base_url, json=payload, headers=headers)
            print(f"Attempt {attempt+1}: status {resp.status_code}")
            print("Response:", resp.text)
            if resp.status_code == 429:
                wait = backoff * (2 ** attempt)
                print(f"429 Too Many Requests, retrying in {wait}s…")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError("Не удалось запустить задачу после нескольких попыток из-за 429")

    def poll_status_and_download(self, task_id: str, interval: int = 5) -> list[str]:
        status_url = f"{self.base_url}/{task_id}"
        headers = {"Authorization": f"Bearer {self.api_token}"}

        while True:
            r = requests.get(status_url, headers=headers)
            r.raise_for_status()
            data = r.json().get("data", {})
            status = data.get("task_status")
            print(f"Polling: task_status = {status}")

            if status == "succeed":
                files = []
                for v in data.get("task_result", {}).get("videos", []):
                    vid_id = v["id"]
                    url    = v["url"]
                    filename = f"video.mp4"
                    print(f"Downloading {url} → {filename}")
                    dl = requests.get(url, stream=True); dl.raise_for_status()
                    with open(filename, "wb") as f:
                        for chunk in dl.iter_content(8192):
                            f.write(chunk)
                    files.append(filename)
                return files

            if status == "failed":
                raise RuntimeError("Генерация не удалась")

            time.sleep(interval)
