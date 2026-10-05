"""Chuyển cột Explanation (định dạng rút gọn, mỗi ý một dòng) thành HTML cho mặt sau thẻ.

    多 (duō · ĐA): nhiều           -> dòng tách nghĩa: chữ (pinyin · HÁN VIỆT): nghĩa
    = Bao nhiêu tiền?              -> Nghĩa cả câu
    ! Nghĩa đen là ...             -> Lưu ý: nghĩa bóng, bẫy, phân biệt
    > Dùng khi ...                 -> Cách dùng
    + 太 + tính từ + 了 ...         -> Mẫu câu
    * Tương truyền ...             -> Mẹo nhớ: câu chuyện, chiết tự, liên tưởng
    (dòng khác)                    -> đoạn văn thường
"""
import html
import re

KINDS = {
    "=": ("mean", "Nghĩa"),
    "!": ("note", "Lưu ý"),
    ">": ("use", "Cách dùng"),
    "+": ("pattern", "Mẫu câu"),
    "*": ("tip", "Mẹo nhớ"),
}

_WORD = re.compile(r"^(?P<zh>[^\s(（]+)\s*[(（](?P<reading>[^)）]*)[)）]\s*[:：]\s*(?P<vi>.+)$")


def _esc(s: str) -> str:
    return html.escape(s.strip(), quote=False)


def render(text: str) -> str:
    if not text.strip():
        return ""
    words, blocks = [], []

    def flush_words():
        if words:
            blocks.append('<table class="ex-words">' + "".join(words) + "</table>")
            words.clear()

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        kind = KINDS.get(line[0])
        if kind:
            flush_words()
            cls, label = kind
            blocks.append(f'<div class="ex-line ex-{cls}"><span class="ex-tag">{label}</span>'
                          f"<span>{_esc(line[1:])}</span></div>")
            continue
        m = _WORD.match(line)
        if m:
            parts = [p.strip() for p in m["reading"].split("·")]
            py = _esc(parts[0])
            hv = f'<span class="ex-hv">{_esc(parts[1])}</span>' if len(parts) > 1 and parts[1] else ""
            words.append(f'<tr><td class="ex-zh">{_esc(m["zh"])}</td>'
                         f'<td class="ex-py">{py}{hv}</td>'
                         f'<td class="ex-vi">{_esc(m["vi"])}</td></tr>')
            continue
        flush_words()
        blocks.append(f'<div class="ex-line">{_esc(line)}</div>')
    flush_words()
    return '<div class="ex">' + "".join(blocks) + "</div>"
