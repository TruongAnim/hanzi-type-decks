# hanzi-type-decks

Bộ thẻ [Anki](https://apps.ankiweb.net/) học tiếng Trung theo **phương pháp gõ chữ Hán**: nhìn câu tiếng Việt, tự gõ lại câu tiếng Trung, Anki chấm từng chữ đúng/sai.

Mỗi bộ từ là một thư mục gồm **file CSV danh sách câu** và **file `.apkg` build sẵn** để import thẳng vào Anki. Ai cũng có thể thêm bộ từ mới chỉ bằng cách viết file CSV; công cụ sẽ tự sinh pinyin, audio và đóng gói thành `.apkg`.

---

## Mục lục

- [Thẻ trông như thế nào](#thẻ-trông-như-thế-nào)
- [Dùng bộ thẻ có sẵn (không cần cài gì)](#dùng-bộ-thẻ-có-sẵn-không-cần-cài-gì)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Cài đặt công cụ](#cài-đặt-công-cụ)
- [Tạo một bộ từ mới](#tạo-một-bộ-từ-mới)
- [Định dạng `deck.csv`](#định-dạng-deckcsv)
- [Viết phần giải thích (`Explanation`)](#viết-phần-giải-thích-explanation)
- [Định dạng `deck.json`](#định-dạng-deckjson)
- [Audio, video, hình ảnh](#audio-video-hình-ảnh)
- [Lệnh build và các tuỳ chọn](#lệnh-build-và-các-tuỳ-chọn)
- [Cập nhật bộ thẻ đã import](#cập-nhật-bộ-thẻ-đã-import)
- [Note type "Hanzi Type" và chỉnh giao diện](#note-type-hanzi-type-và-chỉnh-giao-diện)
- [Đóng góp bộ từ](#đóng-góp-bộ-từ)
- [Lưu ý và giới hạn](#lưu-ý-và-giới-hạn)
- [Câu hỏi thường gặp](#câu-hỏi-thường-gặp)

---

## Thẻ trông như thế nào

**Mặt trước**: gõ câu tiếng Trung, có gợi ý khi bí.

```
                 #7
            Mấy giờ rồi?                 ← tiếng Việt
          What time is it?               ← tiếng Anh
   ┌──────────────────────────────┐
   │      [ ô gõ chữ Hán ]        │      ← gõ xong nhấn Enter
   └──────────────────────────────┘
   - - - - - - - GỢI Ý - - - - - - -
     ( Pinyin )  ( Nghe )  ( Video )     ← bấm mới hiện / mới phát
```

**Mặt sau**: kết quả chấm + đáp án.

```
            Mấy giờ rồi?
          What time is it?
     几点了？                            ← chữ gõ đúng xanh, sai đỏ, thiếu xám
                ───
             几点了？                     ← chữ Hán cỡ lớn
           jǐ diǎn le?                   ← pinyin
               ( ▶ )                     ← audio tự phát, bấm để nghe lại
     ĐỌC BỒI  Chí tiến lơ?
   - - - - - - - - - - - - - - - - - -
     几   jǐ  · KỶ      mấy               ← giải thích: tách nghĩa từng chữ,
     点   diǎn · ĐIỂM   giờ                  kèm âm Hán Việt
     了   le  · LIỄU    rồi
     [NGHĨA] Mấy giờ rồi?
     [CÁCH DÙNG] ...  [MẪU CÂU] ...  [MẸO NHỚ] ...
         [ video ]  [ ảnh ]              ← nếu có
```

- Có **chế độ tối** (tự đổi theo Anki), hiển thị tốt trên điện thoại.
- Field nào trống thì tự ẩn (không có video thì không có nút Video…).
- Nút gợi ý đã bấm sẽ đổi màu, để bạn biết câu đó mình đã phải nhờ gợi ý.

---

## Dùng bộ thẻ có sẵn (không cần cài gì)

1. Vào thư mục [`decks/`](decks/), chọn một bộ, tải file `.apkg` trong đó.
2. Mở Anki → **File → Import** → chọn file `.apkg`.
3. Các bộ sẽ nằm chung dưới deck cha **Hanzi Type**.

Học trên: Anki máy tính (Windows/macOS/Linux), AnkiDroid (Android), AnkiMobile (iPhone/iPad).

> **Mẹo gõ:** cài bộ gõ tiếng Trung giản thể (Pinyin) trên máy/điện thoại. Gõ cả dấu câu
> (`？` `！` `，` `。`) — bộ gõ tiếng Trung sẽ tự ra dấu toàn khổ, đúng với đáp án.

### Danh sách bộ từ

| Thư mục | Tên | Số câu | Ghi chú |
|---|---|---|---|
| [`001-chao-hoi-co-ban`](decks/001-chao-hoi-co-ban/) | Chào hỏi cơ bản | 10 | Bộ mẫu. Video là video test |
| [`002-100-cau-co-ban`](decks/002-100-cau-co-ban/) | 100 câu cơ bản | 100 | Câu thông dụng nhất cho người mới: chào hỏi, giới thiệu, hỏi đáp, ăn uống, mua sắm… Có đọc bồi + giải thích đầy đủ |

---

## Cấu trúc thư mục

```
hanzi-type-decks/
├── README.md
├── requirements.txt
├── hanzi_type/                  # công cụ build (Python)
│   ├── __main__.py              #   dòng lệnh: new / build
│   ├── build.py                 #   đọc CSV, kiểm tra lỗi, đóng gói .apkg
│   ├── notetype.py              #   note type "Hanzi Type": field + id cố định
│   ├── media.py                 #   audio TTS, chuyển đổi video
│   ├── explain.py               #   chuyển cột Explanation thành HTML
│   ├── text.py                  #   sinh pinyin, chuẩn hoá dấu câu
│   └── templates/               #   giao diện thẻ
│       ├── front.html           #     mặt trước
│       ├── back.html            #     mặt sau
│       └── style.css            #     màu sắc, cỡ chữ
├── decks/                       # các bộ từ — mỗi bộ một thư mục
│   └── 001-chao-hoi-co-ban/
│       ├── deck.json            #   tên deck, id, giọng đọc
│       ├── deck.csv             #   danh sách câu (nguồn gốc của bộ thẻ)
│       ├── media/               #   audio / video / ảnh dùng trong thẻ
│       └── 001-chao-hoi-co-ban.apkg   # file build sẵn để import vào Anki
└── build/                       # bản build thử (--fresh), không đưa lên git
```

**Nguyên tắc:** `deck.csv` là nguồn gốc. File `.apkg` luôn được build lại từ CSV — đừng sửa thẻ trong Anki rồi mong nó quay về repo; hãy sửa CSV rồi build lại.

---

## Cài đặt công cụ

Chỉ cần nếu bạn muốn **tạo hoặc sửa** bộ từ. Yêu cầu Python 3.9 trở lên.

```bash
git clone https://github.com/<your-username>/hanzi-type-decks.git
cd hanzi-type-decks

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Các thư viện dùng:

| Thư viện | Dùng để |
|---|---|
| `genanki` | tạo file `.apkg` |
| `pypinyin` | sinh pinyin từ chữ Hán |
| `edge-tts` | sinh audio giọng đọc tiếng Trung (miễn phí, cần mạng) |
| `imageio-ffmpeg` | chuyển đổi video (kèm sẵn ffmpeg, không cần cài riêng) |

> Các lệnh bên dưới giả định đã `source .venv/bin/activate`. Nếu không, thay `python` bằng `.venv/bin/python`.

---

## Tạo một bộ từ mới

### 1. Tạo thư mục bộ từ

```bash
python -m hanzi_type new 002-mua-sam "002 Mua sắm"
```

Lệnh này tạo:

```
decks/002-mua-sam/
├── deck.json      # đã có id ngẫu nhiên + tên "Hanzi Type::002 Mua sắm"
├── deck.csv       # chỉ có dòng tiêu đề
└── media/
```

**Đặt tên thư mục:** `<số thứ tự 3 chữ số>-<chủ đề không dấu, nối bằng gạch ngang>`, ví dụ `003-nha-hang`, `004-hsk1-tu-vung`.

### 2. Điền câu vào `deck.csv`

Mở bằng Excel, Google Sheets, Numbers hoặc trình soạn thảo bất kỳ. Tối thiểu chỉ cần 2 cột `Chinese` và `Vietnamese`:

```csv
No,Chinese,Pinyin,Vietnamese,English,Phonetic VI,Explanation,Audio,Video,Image,Tags
,多少钱？,,Bao nhiêu tiền?,How much is it?,,,,,,
,太贵了！,,Đắt quá!,Too expensive!,,,,,,
,可以便宜一点吗？,,Có thể rẻ hơn chút không?,Can it be cheaper?,,,,,,
```

> **Lưu file dạng CSV UTF-8.** Excel: *File → Save As → CSV UTF-8 (Comma delimited)*.
> Google Sheets: *File → Download → Comma-separated values*.

### 3. Build

```bash
python -m hanzi_type build decks/002-mua-sam
```

Kết quả:

```
=== 002-mua-sam ===
   1. 多少钱？  duō shǎo qián?  tts_1a2b3c4d5e6f.mp3
   2. 太贵了！  tài guì le!  tts_...
   3. 可以便宜一点吗？  kě yǐ pián yi yì diǎn ma?  tts_...

Deck: Hanzi Type::002 Mua sắm  (3 thẻ)
-> decks/002-mua-sam/002-mua-sam.apkg
```

Công cụ tự:
- kiểm tra lỗi CSV (thiếu cột, câu trùng, thiếu file media…) và **dừng lại báo dòng nào lỗi** nếu có;
- sinh **pinyin** cho câu nào để trống cột `Pinyin`;
- sinh **audio** cho câu nào để trống cột `Audio` (lưu vào `media/`, lần sau dùng lại, không sinh lại);
- chuẩn hoá dấu câu tiếng Trung sang dạng toàn khổ (`?` → `？`) để khớp với bộ gõ;
- đánh số thứ tự theo thứ tự dòng nếu cột `No` để trống.

### 4. Kiểm tra trong Anki

Build bản thử để import mà **không đụng tới deck đang học**:

```bash
python -m hanzi_type build decks/002-mua-sam --fresh
# -> build/002-mua-sam_2026-10-04_17h49.apkg  (deck tên "... 2026-10-04 17h49")
```

Import file trong `build/`, xem thử, xoá deck thử đi khi xong.

### 5. Soát pinyin (khuyến nghị)

`pypinyin` đúng phần lớn trường hợp nhưng có thể sai với chữ đa âm. Ghi pinyin tự sinh ngược vào CSV để soát và sửa tay:

```bash
python -m hanzi_type build decks/002-mua-sam --write-pinyin
```

Sau đó sửa cột `Pinyin` nếu sai — câu nào đã có pinyin thì công cụ giữ nguyên, không sinh lại.

---

## Định dạng `deck.csv`

| Cột | Bắt buộc | Nội dung | Ví dụ |
|---|---|---|---|
| `No` | | Số thứ tự hiển thị trên thẻ. Trống → tự đánh theo thứ tự dòng | `7` |
| `Chinese` | **✓** | Câu tiếng Trung — **đáp án cần gõ** | `几点了？` |
| `Pinyin` | | Pinyin có dấu thanh. Trống → tự sinh | `jǐ diǎn le?` |
| `Vietnamese` | **✓** | Nghĩa tiếng Việt (câu hỏi ở mặt trước) | `Mấy giờ rồi?` |
| `English` | | Nghĩa tiếng Anh (hiện ở cả hai mặt) | `What time is it?` |
| `Phonetic VI` | | Đọc bồi kiểu Việt, chỉ để tham khảo (xem quy ước bên dưới) | `Chí tiến lơ?` |
| `Explanation` | | Giải thích câu, nhiều dòng trong một ô (xem [mục riêng](#viết-phần-giải-thích-explanation)) | `钱 (qián · TIỀN): tiền` |
| `Audio` | | Tên file audio trong `media/`. Trống → tự sinh TTS | `cau7.mp3` |
| `Video` | | Tên file video trong `media/` | `cau7.mp4` |
| `Image` | | Tên file ảnh trong `media/` | `dong-ho.jpg` |
| `Tags` | | Tag Anki, cách nhau bằng dấu cách | `hoi-dap thoi-gian` |

Quy tắc:
- Thứ tự cột không quan trọng, cột không dùng có thể bỏ hẳn (trừ `Chinese`, `Vietnamese`).
- **Không được trùng câu** `Chinese` trong cùng một bộ.
- `Chinese` nên ngắn gọn, chỉ chứa đúng thứ người học phải gõ. Không chèn HTML, chú thích, dấu ngoặc giải thích.
- Mỗi thẻ tự có thêm tag là tên thư mục bộ từ (vd `002-mua-sam`), tiện lọc trong Anki.

**Quy ước đọc bồi** (`Phonetic VI`) — gần đúng, chỉ để tham khảo, luôn ưu tiên nghe audio:

| Pinyin | Ghi | | Pinyin | Ghi |
|---|---|---|---|---|
| thanh 1 / 2 / 3 / 4 | không dấu / sắc / hỏi / huyền | | j / q / x | ch / sch / x |
| b / p | p / p | | zh / ch / sh / r | tr / ch / s / r |
| d / t | t / th | | z / c / s | z / x / x |
| g / k / h | c / kh / h | | f | ph |

Ghi theo cách đọc thật (có biến điệu): `你好` → `Ní hảo`, `一路平安` → `Í lù pính an`.

---

## Viết phần giải thích (`Explanation`)

Phần giải thích hiện ở **mặt sau** thẻ, giúp hiểu vì sao câu có nghĩa như vậy và nhớ lâu hơn. Mỗi ý viết một dòng, trong **cùng một ô** CSV. Ký tự đầu dòng quyết định cách hiển thị:

| Dòng bắt đầu bằng | Ý nghĩa | Hiển thị |
|---|---|---|
| `chữ (pinyin · HÁN VIỆT): nghĩa` | Tách nghĩa từng chữ / từ | Bảng: chữ Hán to, pinyin + Hán Việt nhỏ |
| `=` | Nghĩa cả câu (luôn nên có) | Nhãn **NGHĨA**, chữ đậm |
| `!` | Lưu ý: nghĩa bóng, bẫy, phân biệt | Nhãn **LƯU Ý**, nền vàng |
| `>` | Cách dùng: nói khi nào, với ai, đáp lại thế nào | Nhãn **CÁCH DÙNG** |
| `+` | Mẫu câu dùng lại được | Nhãn **MẪU CÂU**, có khung |
| `*` | Mẹo nhớ: câu chuyện, chiết tự, liên tưởng | Nhãn **MẸO NHỚ**, chữ nghiêng |
| (dòng khác) | Đoạn văn thường | |

Trong dòng tách nghĩa, phần Hán Việt có thể bỏ: `了吗 (le ma): ...chưa?`

**Ví dụ:**

```
太 (tài · THÁI): quá
贵 (guì · QUÝ): đắt
了 (le): (cảm thán)
= Đắt quá!
+ 太 + tính từ + 了: 太好了 (tốt quá), 太累了 (mệt quá)
* 贵 là "quý" trong "quý giá". Đồ quý thì đắt.
```

```
加 (jiā · GIA): thêm
油 (yóu · DU): dầu
= Cố lên!
! Nghĩa đen là "đổ thêm dầu", như đổ xăng cho xe chạy tiếp → tiếp sức, cổ vũ.
* Tương truyền từ thời đèn dầu: học trò thức khuya, đèn sắp tắt thì châm thêm dầu để học tiếp.
```

**Xuống dòng trong một ô:** Excel `Alt + Enter` (macOS: `⌃ ⌥ Enter`), Google Sheets `Ctrl + Enter` (macOS: `⌘ Enter`). Trong file CSV, ô nhiều dòng được bọc trong dấu ngoặc kép `"..."` — Excel/Sheets tự làm việc này khi lưu.

### Viết gì cho hay

Mục tiêu là **dễ hiểu, dễ nhớ**, không phải luận văn. Mỗi thẻ nên **3–8 dòng** — dài hơn người học sẽ bỏ qua. Ưu tiên theo thứ tự:

1. **Âm Hán Việt** — vũ khí riêng của người Việt: `问题` = "vấn đề", `当然` = "đương nhiên", `贵` = "quý" (→ đắt). Ghi vào dòng tách nghĩa cho mọi chữ có âm Hán Việt.
2. **Chiết tự** — tách chữ thành bộ phận để nhớ mặt chữ (rất cần cho phương pháp gõ): `好` = `女` + `子`, `饿` = `饣` (ăn) + `我` (tôi) → tôi cần ăn → đói.
3. **Cách dùng** — `你吃饭了吗？` là câu chào, không phải lời mời; `您` dùng với người lớn; `谢谢` → đáp `不客气`.
4. **Mẫu câu** — `太 + tính từ + 了`, `我想 + động từ`… học một mẫu, ghép được nhiều câu.
5. **Mẹo nhớ** — câu chuyện, liên tưởng âm thanh, chuyện vui. **Không cần đúng sự thật**, miễn dễ nhớ và liên quan; chuyện truyền miệng thì mở đầu bằng "Tương truyền…".
6. **Lưu ý** — bẫy cho người Việt (`便宜` viết như "tiện nghi" nhưng nghĩa là *rẻ*), nghĩa bóng, phân biệt từ dễ nhầm (`困` buồn ngủ ≠ `累` mệt).

Không cần đủ cả 6 loại — câu đơn giản chỉ cần tách nghĩa + nghĩa cả câu + một dòng bất kỳ đáng nhớ.

---

## Định dạng `deck.json`

```json
{
  "id": 2112374030,
  "name": "Hanzi Type::001 Chào hỏi cơ bản",
  "description": "10 câu giao tiếp cơ bản cho người mới bắt đầu.",
  "voice": "zh-CN-XiaoxiaoNeural"
}
```

| Khoá | Ý nghĩa |
|---|---|
| `id` | ID của deck trong Anki. Tạo ngẫu nhiên bởi lệnh `new`. **Không đổi** sau khi đã phát hành, nếu không người dùng import bản mới sẽ ra deck trùng |
| `name` | Tên deck. `::` tạo deck con — giữ tiền tố `Hanzi Type::` để mọi bộ nằm chung một chỗ |
| `description` | Mô tả, hiện trong màn hình tổng quan deck của Anki |
| `voice` | Giọng đọc TTS (xem bên dưới) |

---

## Audio, video, hình ảnh

Mọi file media của một bộ để trong `decks/<bộ>/media/`.

### Audio

- **Để trống cột `Audio`** → tự sinh bằng [edge-tts](https://github.com/rany2/edge-tts) (giọng neural của Microsoft, miễn phí, không cần tài khoản). File tên `tts_<mã>.mp3`, mã tính theo nội dung câu + giọng đọc:
  - câu không đổi → dùng lại file cũ, không cần mạng;
  - sửa/xoá câu → file cũ không còn dùng sẽ **tự bị xoá** khi build.
- **Dùng file thu âm riêng** → bỏ file vào `media/`, ghi tên vào cột `Audio`. Nên dùng **mp3** (Anki máy tính không phát được m4a/AAC trong thẻ).
- Đổi giọng: sửa `voice` trong `deck.json`. Một số giọng tiếng Trung phổ thông:

  | Giọng | Mô tả |
  |---|---|
  | `zh-CN-XiaoxiaoNeural` | nữ, mặc định |
  | `zh-CN-XiaoyiNeural` | nữ, trẻ |
  | `zh-CN-YunxiNeural` | nam, trẻ |
  | `zh-CN-YunjianNeural` | nam, trầm |
  | `zh-TW-HsiaoChenNeural` | nữ, giọng Đài Loan |

  Xem toàn bộ: `edge-tts --list-voices | grep zh-`

- Chạy offline / không muốn audio: `--no-tts`.

### Video

Ghi tên file vào cột `Video`, ví dụ `cau7.mp4` (định dạng nguồn bất kỳ: mp4, mov, webm…).

Khi build, công cụ đảm bảo trong `media/` có **cả hai bản** `cau7.webm` và `cau7.mp4`, tự chuyển đổi bản còn thiếu:

| Bản | Cho |
|---|---|
| `.webm` (VP9) | Anki máy tính — không phát được mp4/H.264 trong thẻ |
| `.mp4` (H.264) | iPhone/iPad — không phát được webm |

Thiết bị nào cũng tự chọn bản phát được. Nên giữ video **ngắn (vài giây) và nhẹ**, vì mọi người tải bộ thẻ sẽ tải cả video.

### Hình ảnh

Ghi tên file vào cột `Image` (jpg/png/webp). Ảnh hiện ở cuối mặt sau.

---

## Lệnh build và các tuỳ chọn

```bash
python -m hanzi_type build decks/001-chao-hoi-co-ban      # build một bộ
python -m hanzi_type build decks/001-... decks/002-...    # build nhiều bộ
python -m hanzi_type build --all                          # build mọi bộ trong decks/
```

| Tuỳ chọn | Tác dụng |
|---|---|
| `--fresh` | Xuất **bản mới hoàn toàn** vào `build/`: tên deck kèm ngày giờ, id/guid ngẫu nhiên → import thành deck riêng, không cập nhật đè deck đang học. Dùng để test |
| `--no-tts` | Không sinh audio (câu nào chưa có audio sẽ không có nút Nghe) |
| `--write-pinyin` | Ghi pinyin tự sinh ngược vào `deck.csv` để soát |

---

## Cập nhật bộ thẻ đã import

Bản build thường (không `--fresh`) dùng **id deck và guid cố định**, nên khi sửa CSV, build lại rồi import đè:

| Thay đổi trong CSV | Sau khi import bản mới vào Anki |
|---|---|
| Sửa nghĩa, pinyin, đọc bồi, audio, video… | Thẻ cũ được **cập nhật**, giữ nguyên tiến độ học |
| Thêm câu mới | Thẻ mới được thêm vào |
| **Sửa chữ trong cột `Chinese`** | Anki coi là **câu mới** (guid tính theo câu tiếng Trung) → có thêm thẻ mới, thẻ cũ vẫn còn, phải xoá tay |
| Xoá câu | Anki **không tự xoá** thẻ đã có → xoá tay trong Anki (Browse → tìm → Delete) |

Nếu muốn bắt đầu lại sạch sẽ: xoá deck trong Anki rồi import lại (mất tiến độ học của deck đó).

---

## Note type "Hanzi Type" và chỉnh giao diện

Mọi bộ thẻ dùng chung một note type tên **Hanzi Type** với **id cố định** (`MODEL_ID` trong [`hanzi_type/notetype.py`](hanzi_type/notetype.py)). Nhờ vậy, khi giao diện được cải tiến, chỉ cần import một bộ bất kỳ đã build lại là **mọi bộ Hanzi Type trong Anki cùng được cập nhật giao diện**.

> Không đổi `MODEL_ID` và không đổi tên/thứ tự field nếu không thật cần thiết — sẽ làm hỏng việc cập nhật cho người đã import.

### Các field

| # | Field | Nội dung |
|---|---|---|
| 1 | `Chinese` | Câu tiếng Trung, đáp án cần gõ. Đứng đầu để Anki phát hiện câu trùng |
| 2 | `Pinyin` | Pinyin |
| 3 | `Vietnamese` | Nghĩa tiếng Việt |
| 4 | `English` | Nghĩa tiếng Anh |
| 5 | `Phonetic VI` | Đọc bồi |
| 6 | `Explanation` | Giải thích (HTML, build từ định dạng rút gọn trong CSV) |
| 7 | `Audio` | `<audio src="...">` |
| 8 | `Video` | `<video><source webm><source mp4></video>` |
| 9 | `Image` | `<img src="...">` |
| 10 | `No` | Số thứ tự |

### Sửa giao diện

| File | Nội dung |
|---|---|
| [`templates/front.html`](hanzi_type/templates/front.html) | Mặt trước: câu hỏi, ô gõ, các nút gợi ý (+ JavaScript xử lý nút) |
| [`templates/back.html`](hanzi_type/templates/back.html) | Mặt sau: kết quả chấm, đáp án, audio tự phát, giải thích, video, ảnh |
| [`templates/style.css`](hanzi_type/templates/style.css) | Màu sắc, cỡ chữ, chế độ tối |

Màu chính khai báo ở đầu `style.css` (và bản chế độ tối ngay bên dưới):

```css
--zh: #b4232a;       /* màu chữ Hán */
--pinyin: #0f766e;   /* màu pinyin, nút gợi ý, nút phát */
--bg: #f7f4ee;       /* nền */
```

Sửa xong → build lại một bộ với `--fresh` → import để xem.

### Vì sao audio dùng `<audio>` thay vì `[sound:...]` của Anki

Anki **tự phát mọi `[sound:...]` có ở mặt trước**, kể cả khi bị ẩn — nút gợi ý "Nghe" sẽ đọc luôn đáp án ngay khi mở thẻ. Thẻ `<audio>` chỉ phát khi bấm; mặt sau tự phát bằng JavaScript. Đánh đổi: phím tắt **R** (phát lại) của Anki không dùng được, thay bằng nút ▶ trên thẻ.

---

## Đóng góp bộ từ

Rất hoan nghênh bộ từ mới! Quy trình:

1. Fork repo, tạo nhánh mới.
2. `python -m hanzi_type new <số>-<chu-de> "<số> <Chủ đề>"` (lấy số tiếp theo chưa dùng trong `decks/`).
3. Điền `deck.csv`, thêm media (nếu có) vào `media/`.
4. `python -m hanzi_type build decks/<bộ>` — sửa hết lỗi nếu có.
5. Import thử file `.apkg` (hoặc bản `--fresh`) vào Anki, học thử vài thẻ.
6. Thêm một dòng vào bảng [Danh sách bộ từ](#danh-sách-bộ-từ) trong README.
7. Commit **cả** `deck.json`, `deck.csv`, `media/` và file `.apkg`, rồi mở Pull Request.

Checklist trước khi gửi:

- [ ] Chữ Hán đúng (cẩn thận lỗi OCR/gõ nhầm: `要`/`耍`, `天`/`夭`, `来`/`夹`, `大`/`犬`…)
- [ ] Pinyin đã soát (`--write-pinyin`), nghĩa tiếng Việt tự nhiên, không lỗi chính tả
- [ ] (Khuyến khích) Có phần `Explanation`, âm Hán Việt đúng
- [ ] Câu ngắn gọn, phù hợp trình độ ghi trong mô tả
- [ ] Không có nội dung thô tục, xúc phạm
- [ ] Media là của bạn hoặc được phép chia sẻ; video ngắn, nhẹ
- [ ] Build không lỗi, đã thử trong Anki

---

## Lưu ý và giới hạn

- **edge-tts không phải API chính thức** của Microsoft. Miễn phí và ổn định trong thực tế, nhưng có thể đôi lúc lỗi khi Microsoft thay đổi dịch vụ — thường chỉ cần `pip install -U edge-tts`. Công cụ tự thử lại 3 lần khi lỗi mạng. Audio đã sinh nằm trong `media/` nên build lại không cần mạng.
- **Dung lượng repo:** audio TTS rất nhẹ (~10 KB/câu), nhưng video thì nặng. GitHub giới hạn file 100 MB; nếu có nhiều video, cân nhắc [Git LFS](https://git-lfs.com/) hoặc đính kèm `.apkg` vào GitHub Releases.
- **Audio tự phát ở mặt sau** dựa vào JavaScript: chạy trên Anki máy tính và AnkiDroid; AnkiMobile (iOS) có thể chặn — khi đó bấm nút ▶.
- **Thẻ type chấm từng ký tự**, kể cả dấu câu. Thiếu `？` ở cuối sẽ bị đánh dấu thiếu.
- Pinyin tự sinh **có** biến điệu của `一` và `不` (`不是` → `bú shì`, `一个` → `yí gè`) nhưng **không** biến điệu thanh 3 (`你好` → `nǐ hǎo`, đọc thật là `ní hǎo`). Thanh nhẹ cũng có thể khác (`便宜` → `pián yi`). Muốn ghi khác thì sửa tay cột `Pinyin`.

---

## Câu hỏi thường gặp

**Import xong không thấy ô gõ chữ?**
Kiểm tra note type của thẻ là `Hanzi Type` (Browse → cột Note). Nếu trước đó bạn đã import một bản cũ có cùng note type nhưng giao diện khác, Anki có thể hỏi có cập nhật note type không — chọn cập nhật.

**Import xong thấy note type tên lạ kiểu `Hanzi Type-a1b2c`?**
Do trước đó bạn đã import một bản có note type `Hanzi Type` với số field khác (ví dụ bản trước khi có cột `Explanation`). Anki không gộp được nên tạo bản sao. Cách sạch nhất: xoá các deck Hanzi Type cũ, vào **Tools → Manage Note Types** xoá các note type `Hanzi Type…` không còn dùng, rồi import lại.

**Gõ đúng mà vẫn bị báo sai?**
Thường do dấu câu: bộ gõ tiếng Anh ra `?`, đáp án là `？`. Bật bộ gõ tiếng Trung khi gõ cả câu.

**Video không phát trên máy tính?**
Kiểm tra `media/` có bản `.webm` và đã build lại. Anki máy tính không phát được mp4.

**Muốn tạo bộ có hàng trăm câu?**
Được. Lần build đầu sinh audio mất khoảng 1–2 giây/câu; các lần sau dùng lại audio đã có nên rất nhanh.

**Có cần mạng không?**
Chỉ khi cần sinh audio cho câu mới. Học trên Anki thì hoàn toàn offline.

---

## Giấy phép

Chưa chọn. Gợi ý: [MIT](https://choosealicense.com/licenses/mit/) cho mã nguồn và [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) cho nội dung bộ từ.
