"""Note type chuẩn "Hanzi Type": cấu trúc field + giao diện thẻ (templates/)."""
from pathlib import Path

import genanki

# ID cố định: mọi bộ thẻ dùng chung một note type trong Anki.
# Sửa giao diện rồi import bộ mới -> giao diện của mọi bộ cũ cùng được cập nhật.
# KHÔNG đổi số này, trừ khi muốn tách thành một note type khác hẳn.
MODEL_ID = 1228803704
MODEL_NAME = "Hanzi Type"

# Thứ tự field trong Anki. Chinese đứng đầu: Anki dùng field đầu tiên để phát hiện câu trùng.
FIELDS = ["Chinese", "Pinyin", "Vietnamese", "English", "Phonetic VI", "Audio", "Video", "Image", "No"]

TEMPLATES = Path(__file__).parent / "templates"


def build_model() -> genanki.Model:
    return genanki.Model(
        MODEL_ID,
        MODEL_NAME,
        fields=[{"name": f} for f in FIELDS],
        templates=[{
            "name": "Việt → Trung (gõ)",
            "qfmt": (TEMPLATES / "front.html").read_text(encoding="utf-8"),
            "afmt": (TEMPLATES / "back.html").read_text(encoding="utf-8"),
        }],
        css=(TEMPLATES / "style.css").read_text(encoding="utf-8"),
        sort_field_index=FIELDS.index("Chinese"),
    )
