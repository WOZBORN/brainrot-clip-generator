import subprocess


def merge_with_ffmpeg(video_path: str, voice_path: str, music_path: str, out_path: str):
    """
    Смешивает видео + голос + музыку в один файл при помощи ffmpeg CLI.
    """
    cmd = [
        "ffmpeg",
        "-y",  # перезаписывать выходной файл без вопроса
        "-i", video_path,
        "-i", voice_path,
        "-i", music_path,
        "-filter_complex",
        "[1:a]volume=1[a1];"      # дорожка 1 (voice) — громкость 100%
        "[2:a]volume=0.2[a2];"    # дорожка 2 (music) — громкость 20%
        "[a1][a2]amix=inputs=2:duration=first:dropout_transition=3[outa]",
        "-map", "0:v",            # видео из первого входа
        "-map", "[outa]",         # аудио из микса
        "-c:v", "copy",           # копировать видеопоток без перекодирования
        "-c:a", "aac",            # кодек для аудио
        out_path
    ]

    # Запускаем и ждём завершения
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("ffmpeg error:", result.stderr)
        raise RuntimeError(f"ffmpeg завершился с ошибкой {result.returncode}")
    print("Готово, сохранён файл:", out_path)