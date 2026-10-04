"""Build một bộ thẻ (thư mục trong decks/) thành file .apkg."""
import csv
import json
import random
from datetime import datetime
from pathlib import Path

import genanki

from . import media
from .notetype import FIELDS, build_model
from .text import clean_chinese, to_pinyin

# Cột của deck.csv. Bắt buộc: Chinese, Vietnamese. Còn lại có thể để trống.
COLUMNS = ["No", "Chinese", "Pinyin", "Vietnamese", "English", "Phonetic VI", "Audio", "Video", "Image", "Tags"]
REQUIRED = ["Chinese", "Vietnamese"]


class DeckError(Exception):
    pass


def load_meta(folder: Path) -> dict:
    path = folder / "deck.json"
    if not path.exists():
        raise DeckError(f"Thiếu {path}")
    meta = json.loads(path.read_text(encoding="utf-8"))
    for key in ("id", "name"):
        if key not in meta:
            raise DeckError(f"{path}: thiếu khoá '{key}'")
    return meta


def load_rows(folder: Path):
    path = folder / "deck.csv"
    if not path.exists():
        raise DeckError(f"Thiếu {path}")
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        unknown = [c for c in header if c not in COLUMNS]
        if unknown:
            raise DeckError(f"{path}: cột không hợp lệ {unknown}. Cột cho phép: {COLUMNS}")
        missing = [c for c in REQUIRED if c not in header]
        if missing:
            raise DeckError(f"{path}: thiếu cột bắt buộc {missing}")
        rows = [{k: (v or "").strip() for k, v in r.items()} for r in reader]
    return header, [r for r in rows if any(r.values())]


def validate(rows, media_dir: Path):
    errors, seen = [], {}
    for i, r in enumerate(rows, start=2):  # dòng 1 là header
        for c in REQUIRED:
            if not r.get(c):
                errors.append(f"dòng {i}: thiếu {c}")
        cn = clean_chinese(r.get("Chinese", ""))
        if cn in seen:
            errors.append(f"dòng {i}: trùng câu với dòng {seen[cn]} ({cn})")
        seen.setdefault(cn, i)
        for c in ("Audio", "Video", "Image"):
            name = r.get(c)
            if name and not (media_dir / name).exists():
                errors.append(f"dòng {i}: không thấy file {c} '{name}' trong {media_dir}")
    if errors:
        raise DeckError("deck.csv có lỗi:\n  " + "\n  ".join(errors))


def build_deck(folder: Path, fresh: bool = False, tts: bool = True, write_pinyin: bool = False) -> Path:
    folder = folder.resolve()
    meta = load_meta(folder)
    header, rows = load_rows(folder)
    media_dir = folder / "media"
    media_dir.mkdir(exist_ok=True)
    validate(rows, media_dir)

    voice = meta.get("voice", media.DEFAULT_VOICE)
    deck_id, deck_name = int(meta["id"]), meta["name"]
    if fresh:
        # bản "mới hoàn toàn": tên kèm ngày giờ + id/guid ngẫu nhiên -> import thành deck riêng, không đè deck cũ
        stamp = datetime.now().strftime("%Y-%m-%d %Hh%M")
        deck_name = f"{deck_name} {stamp}"
        deck_id = random.randrange(1 << 30, 1 << 31)
        out = folder.parent.parent / "build" / f"{folder.name}_{stamp.replace(' ', '_')}.apkg"
    else:
        out = folder / f"{folder.name}.apkg"

    model = build_model()
    deck = genanki.Deck(deck_id, deck_name, meta.get("description", ""))
    files, used_tts = set(), set()

    for idx, r in enumerate(rows, start=1):
        cn = clean_chinese(r["Chinese"])
        if not r.get("Pinyin"):
            r["Pinyin"] = to_pinyin(cn)

        audio = ""
        if r.get("Audio"):
            audio = r["Audio"]
        elif tts:
            audio = media.ensure_tts(cn, voice, media_dir)
            used_tts.add(audio)
        video = media.ensure_video_pair(r["Video"], media_dir) if r.get("Video") else []

        values = {
            "Chinese": cn,
            "Pinyin": r["Pinyin"],
            "Vietnamese": r["Vietnamese"],
            "English": r.get("English", ""),
            "Phonetic VI": r.get("Phonetic VI", ""),
            "Audio": media.audio_html(audio) if audio else "",
            "Video": media.video_html(*video) if video else "",
            "Image": media.image_html(r["Image"]) if r.get("Image") else "",
            "No": r.get("No") or str(idx),
        }
        files.update(x for x in [audio, *video, r.get("Image")] if x)

        # guid ổn định theo (deck, câu tiếng Trung): import lại bản mới sẽ cập nhật thẻ cũ, giữ tiến độ học
        guid = genanki.guid_for(random.random()) if fresh else genanki.guid_for(meta["id"], cn)
        tags = r.get("Tags", "").split() + [folder.name]
        deck.add_note(genanki.Note(model=model, fields=[values[f] for f in FIELDS],
                                   guid=guid, tags=tags, due=idx))
        print(f"{values['No']:>4}. {cn}  {r['Pinyin']}  {audio}")

    # dọn audio TTS cũ không còn dùng (do đã sửa/xoá câu)
    if tts:
        for p in media_dir.glob(f"{media.TTS_PREFIX}*.mp3"):
            if p.name not in used_tts:
                p.unlink()
                print(f"  xoá audio thừa: {p.name}")

    if write_pinyin:
        cols = header if "Pinyin" in header else header[:header.index("Chinese") + 1] + ["Pinyin"] + header[header.index("Chinese") + 1:]
        with open(folder / "deck.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        print("  đã ghi pinyin vào deck.csv")

    out.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(deck, media_files=[str(media_dir / f) for f in sorted(files)]).write_to_file(str(out))
    print(f"\nDeck: {deck_name}  ({len(rows)} thẻ)\n-> {out}")
    return out


def new_deck(decks_dir: Path, slug: str, name: str) -> Path:
    folder = decks_dir / slug
    if folder.exists():
        raise DeckError(f"{folder} đã tồn tại")
    (folder / "media").mkdir(parents=True)
    meta = {
        "id": random.randrange(1 << 30, 1 << 31),
        "name": f"Hanzi Type::{name}",
        "description": "",
        "voice": media.DEFAULT_VOICE,
    }
    (folder / "deck.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with open(folder / "deck.csv", "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow(COLUMNS)
    (folder / "media" / ".gitkeep").touch()
    return folder
