"""Dòng lệnh:

    python -m hanzi_type new <slug> "<Tên bộ>"     tạo thư mục bộ thẻ mới trong decks/
    python -m hanzi_type build decks/<slug>        build ra decks/<slug>/<slug>.apkg
    python -m hanzi_type build --all               build mọi bộ trong decks/
"""
import argparse
import sys
from pathlib import Path

from .build import DeckError, build_deck, new_deck

ROOT = Path(__file__).resolve().parent.parent
DECKS = ROOT / "decks"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m hanzi_type", description="Build bộ thẻ Anki Hanzi Type từ CSV")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="tạo bộ thẻ mới")
    p_new.add_argument("slug", help="tên thư mục, vd 002-mua-sam")
    p_new.add_argument("name", help='tên deck hiển thị trong Anki, vd "Mua sắm"')

    p_build = sub.add_parser("build", help="build bộ thẻ thành .apkg")
    p_build.add_argument("folders", nargs="*", type=Path, help="thư mục bộ thẻ (vd decks/001-chao-hoi-co-ban)")
    p_build.add_argument("--all", action="store_true", help="build mọi bộ trong decks/")
    p_build.add_argument("--fresh", action="store_true",
                         help="xuất bản mới hoàn toàn (tên kèm ngày giờ, id mới) vào build/ để test, không đè deck cũ")
    p_build.add_argument("--no-tts", action="store_true", help="không sinh audio TTS (chạy offline)")
    p_build.add_argument("--write-pinyin", action="store_true", help="ghi pinyin tự sinh ngược vào deck.csv")

    args = ap.parse_args(argv)
    try:
        if args.cmd == "new":
            folder = new_deck(DECKS, args.slug, args.name)
            print(f"Đã tạo {folder.relative_to(ROOT)}/ — điền câu vào deck.csv rồi chạy:\n"
                  f"  python -m hanzi_type build {folder.relative_to(ROOT)}")
        else:
            folders = sorted(p for p in DECKS.iterdir() if (p / "deck.json").exists()) if args.all else args.folders
            if not folders:
                ap.error("cần chỉ định thư mục bộ thẻ hoặc --all")
            for folder in folders:
                print(f"=== {folder.name} ===")
                build_deck(folder, fresh=args.fresh, tts=not args.no_tts, write_pinyin=args.write_pinyin)
    except DeckError as e:
        print(f"Lỗi: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
