"""Audio (TTS) và video cho thẻ."""
import asyncio
import hashlib
import subprocess
from pathlib import Path

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"
TTS_PREFIX = "tts_"


def tts_filename(text: str, voice: str) -> str:
    """Tên file cố định theo (giọng, câu): đổi câu -> file mới, không đổi -> dùng lại file cũ."""
    return f"{TTS_PREFIX}{hashlib.sha1((voice + text).encode()).hexdigest()[:12]}.mp3"


def ensure_tts(text: str, voice: str, media_dir: Path, retries: int = 3) -> str:
    """Sinh mp3 bằng edge-tts nếu chưa có trong media_dir. Trả về tên file."""
    import edge_tts

    name = tts_filename(text, voice)
    path = media_dir / name
    if path.exists():
        return name
    for attempt in range(1, retries + 1):
        try:
            asyncio.run(edge_tts.Communicate(text, voice).save(str(path)))
            return name
        except Exception as e:  # lỗi mạng / bị giới hạn tốc độ
            path.unlink(missing_ok=True)
            if attempt == retries:
                raise RuntimeError(f"TTS lỗi với câu {text!r}: {e}") from e
            asyncio.run(asyncio.sleep(2 * attempt))
    return name


def _ffmpeg() -> str:
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def ensure_video_pair(name: str, media_dir: Path) -> list:
    """Đảm bảo có cả .webm (Anki máy tính) và .mp4 (iPhone/iPad); tự chuyển đổi bản còn thiếu.

    Trả về danh sách tên file theo thứ tự ưu tiên [webm, mp4].
    """
    src = media_dir / name
    if not src.exists():
        raise FileNotFoundError(f"Không thấy video: {src}")
    stem = src.stem
    webm, mp4 = media_dir / f"{stem}.webm", media_dir / f"{stem}.mp4"
    if not webm.exists():
        print(f"  chuyển {name} -> {webm.name} ...")
        subprocess.run([_ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
                        "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "36", "-c:a", "libopus", "-b:a", "64k",
                        str(webm)], check=True)
    if not mp4.exists():
        print(f"  chuyển {name} -> {mp4.name} ...")
        subprocess.run([_ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "26", "-c:a", "aac", "-b:a", "96k",
                        "-movflags", "+faststart", str(mp4)], check=True)
    return [webm.name, mp4.name]


def audio_html(name: str) -> str:
    # <audio> thay vì [sound:]: Anki tự phát mọi [sound:] ở mặt trước, kể cả khi bị ẩn,
    # nên gợi ý "Nghe" sẽ lộ đáp án. <audio> chỉ phát khi bấm (mặt sau tự phát bằng JS).
    return f'<audio src="{name}" preload="auto"></audio>'


def video_html(webm: str, mp4: str) -> str:
    return (
        '<video controls playsinline preload="metadata">'
        f'<source src="{webm}" type="video/webm">'
        f'<source src="{mp4}" type="video/mp4">'
        "</video>"
    )


def image_html(name: str) -> str:
    return f'<img src="{name}">'
