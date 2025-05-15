import subprocess
import os

def make_boomerang_clip(input_video: str, boomerang_video: str):
    """
    Создаёт файл boomerang_video, где input_video проигрывается вперёд и сразу назад.
    """
    cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-filter_complex",
        "[0:v]split[vf][vr];"     # разделяем видео на две дорожки
        "[vr]reverse[rv];"        # одну переворачиваем
        "[vf][rv]concat=n=2:v=1:a=0[outv]",  # склеиваем вперёд+назад
        "-map", "[outv]",
        "-c:v", "libx264",
        boomerang_video
    ]
    subprocess.run(cmd, check=True)
    print(f"Boomerang video saved to {boomerang_video}")

def merge_loop_and_audio(boomerang_video: str, voice_path: str, music_path: str, final_output: str):
    """
    Зацикливает boomerang_video (-stream_loop -1), микширует голос и музыку
    и обрезает по длине аудио (voice_path), сохраняя в final_output.
    """
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", boomerang_video,
        "-i", voice_path,
        "-i", music_path,
        "-filter_complex",
        # микс аудио: голос 100%, музыка 20%
        "[1:a]volume=1[a1];"
        "[2:a]volume=0.2[a2];"
        "[a1][a2]amix=inputs=2:duration=first:dropout_transition=3[outa]",
        "-map", "0:v",      # видео из boomerang, зацикленного
        "-map", "[outa]",   # замикшированное аудио
        "-c:v", "copy",     # копируем видео без перекодирования
        "-c:a", "aac",
        "-shortest",        # обрезаем по аудио
        final_output
    ]
    subprocess.run(cmd, check=True)
    print(f"Final boomerang video with audio saved to {final_output}")

if __name__ == "__main__":
    # пути к файлам
    src_video = "../video.mp4"
    boomerang = "boomerang.mp4"
    voice = "../voice.mp3"
    music = "../resources/music.mp3"
    out = "final_output.mp4"

    # 1) делаем boomerang
    make_boomerang_clip(src_video, boomerang)

    # 2) зацикливаем boomerang, микшуем звук и обрезаем
    merge_loop_and_audio(boomerang, voice, music, out)
