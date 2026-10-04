"""Xử lý chữ: bỏ HTML, chuẩn hoá dấu câu, sinh pinyin."""
import html
import re

from pypinyin import Style, lazy_pinyin

# dấu câu Latin -> dấu toàn khổ, khớp với những gì bộ gõ tiếng Trung gõ ra (để thẻ type chấm đúng)
_FULLWIDTH = str.maketrans({"?": "？", "!": "！", ",": "，", ".": "。", ":": "：", ";": "；"})
# ngược lại, cho pinyin
_LATIN = str.maketrans("，。？！：；、（）“”", ",.?!:;,()\"\"")


def strip_html(s: str) -> str:
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()


def clean_chinese(s: str) -> str:
    """Bỏ HTML, bỏ khoảng trắng, đổi dấu câu sang toàn khổ."""
    return re.sub(r"\s+", "", strip_html(s)).translate(_FULLWIDTH)


def to_pinyin(chinese: str) -> str:
    """我回来了 -> 'wǒ huí lái le'; dấu câu dính vào chữ phía trước."""
    out = ""
    for tok in lazy_pinyin(clean_chinese(chinese), style=Style.TONE, errors=lambda x: x):
        if tok.isalpha():
            out += (" " if out and not out.endswith(("(", '"')) else "") + tok
        else:
            out += tok.translate(_LATIN)
    return out.strip()
