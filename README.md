<div align="center">

# ibisPaint .ipv Format &amp; PNG Extraction Guide

[![Format](https://img.shields.io/badge/Format-ibisPaint_.ipv-blue?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiPjxjaXJjbGUgY3g9IjEzLjUiIGN5PSI2LjUiIHI9Ii41Ii8+PGNpcmNsZSBjeD0iMTcuNSIgY3k9IjEwLjUiIHI9Ii41Ii8+PGNpcmNsZSBjeD0iOC41IiBjeT0iNy41IiByPSIuNSIvPjxjaXJjbGUgY3g9IjYuNSIgY3k9IjEyLjUiIHI9Ii41Ii8+PHBhdGggZD0iTTEyIDJDNi41IDIgMiA2LjUgMiAxMnM0LjUgMTAgMTAgMTBjLjkyNiAwIDEuNjQ4LS43NDYgMS42NDgtMS42ODggMC0uNDM3LS4xOC0uODM1LS40MzctMS4xMjUtLjI5LS4yODktLjQzOC0uNjUyLS40MzgtMS4xMjVhMS42NCAxLjY0IDAgMCAxIDEuNjY4LTEuNjY4aDEuOTk2YzMuMDUxIDAgNS41NTUtMi41MDMgNS41NTUtNS41NTRDMjEuOTY1IDYuMDEyIDE3LjQ2MSAyIDEyIDJ6Ii8+PC9zdmc+)](https://github.com/vyvegroup/ipv-images)
[![Language](https://img.shields.io/badge/Language-Python_3-3776AB?style=flat-square&logo=python&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)]()
[![Platform](https://img.shields.io/badge/Platform-Cross--platform-9CF?style=flat-square)]()

**Hướng dẫn kỹ thuật toàn diện về định dạng file .ipv của ibisPaint X  
và phương pháp trích xuất artwork PNG nguyên bản.**

[bat-dau](#-bat-dau-nhanh) &middot;
[cau-truc](#-cau-truc-ky-thuat) &middot;
[huong-dan](#-huong-dan-trich-xuat) &middot;
[tool](#-cong-cu)

</div>

---

## Muc luc

- [Tong quan](#-tong-quan)
- [Bat dau nhanh](#-bat-dau-nhanh)
- [Dinh dang .ipv la gi](#-dinh-dang-ipv-la-gi)
- [Cau truc ky thuat](#-cau-truc-ky-thuat-cua-file-ipv)
  - [Header chinh](#31-header-chinh)
  - [Bang mau](#32-bang-mau-color-table)
  - [Du lieu layer](#33-du-lieu-layer)
  - [Du lieu canvas da gop](#34-du-lieu-canvas-da-gop-merged-artwork)
  - [Metadata cuoi file](#35-metadata-cuoi-file)
- [Huong dan trich xuat PNG](#-huong-dan-trich-xuat-png)
  - [Yeu cau he thong](#41-yeu-cau-he-thong)
  - [Cach 1 Script Python](#42-cach-1-su-dung-script-python-khuyen-dung)
  - [Cach 2 Thu cong](#43-cach-2-trich-xuat-thu-cong-voi-hex-editor)
- [Phan tich chuyen sau](#-phan-tich-chuyen-sau)
  - [Nhieu PNG trong mot file](#51-tai-sao-co-nhieu-png-trong-mot-file-ipv)
  - [Xac dinh PNG dung](#52-cach-xac-dinh-png-artwork-nguyen-ban)
  - [Layer compositing](#53-layer-compositing-ghép-nhieu-layer)
- [Xu ly su co](#-xu-ly-su-co-thuong-gap)
- [Cong cu va tham khao](#-cong-cu-tai-lieu-tham-khao)

---

## <img src="https://fonts.gstatic.com/s/i/short-strings/materialsymbols/outlined/info_wght400grad25_20x20.png" width="20" valign="middle"> Tong quan

ibisPaint X la ung dung ve tranh ky thuat so pho bien tren iOS va Android, voi hon 300 triệu lượt tai tren ca hai nha kho ung dung. Ung dung nay luu du lieu du an (project) duoi dang file co phan mo rong **`.ipv`** (ibisPaint Version) -- mot dinh dang file thuoc so huu cua ibisPaint Inc., khong duoc tai lieu hoa cong khai.

Van de trung tam: **ban khong the mo file .ipv truc tiep bang bat ky phan mem hinh anh nao** (Photoshop, GIMP, Preview, Windows Photos...). Dinh dang nay khong duoc ho tro boi cac chuan hinh anh pho thong (JPEG, PNG, WebP, BMP, TIFF). Khi ban can chuyen artwork tu ibisPaint sang dinh dang chung de su dung o cac nen tang khac (xu ly anh tiep tuc, in an, dang tai len web, hoac chia se), ban can phai trich xuat PNG nguyen ban tu ben trong file .ipv.

Tai lieu nay cung cap toan bo kien thuc ky thuat can thiet de hieu va xu ly dinh dang .ipv, bao gom ca cau truc binary, phuong phap trich xuat tu dong bang Python, va nhung hieu ung ma ban co the gap phai trong qua trinh lam viec voi file nay. Noi dung duoc xay dung dua tren viec phan tich doc lap (reverse engineering) tren hang chuc file .ipv thuc te tu cac phien ban ibisPaint X khac nhau.

> [!NOTE]
> Moi thong tin trong tai lieu nay duoc thu thap thong qua phan tich reverse engineering doc lap. Dinh dang .ipv la thuoc so huu cua ibisPaint Inc. va co the thay doi giua cac phien ban. Tai lieu nay khong lien he voi va khong duoc ho tro boi ibisPaint Inc.

---

## <img src="https://fonts.gstatic.com/s/i/short-strings/materialsymbols/outlined/rocket_launch_wght400grad25_20x20.png" width="20" valign="middle"> Bat dau nhanh

Neu ban chi muon trich xuat PNG ma khong can hieu ky thuat chi tiet, day la cach nhanh nhat:

```bash
# 1. Tai script trich xuat
curl -O https://raw.githubusercontent.com/vyvegroup/ipv-images/main/extract_ipv.py

# 2. Chay script voi file .ipv cua ban
python3 extract_ipv.py duong/dan/toi/file.ipv

# 3. PNG se duoc luu cung thu muc voi file goc
```

Script se tu dong:
- Doc header file .ipv de lay kich thuoc canvas goc
- Quet toan bo file de tim tat ca PNG duoi dang nhung phan (chunk)
- Xac dinh PNG co kich thuoc khop voi canvas (day la artwork da gop day du)
- Trich xuat va luu thanh file PNG doc lap voi ten giong file goc

---

## <img src="https://fonts.gstatic.com/s/i/short-strings/materialsymbols/outlined/description_wght400grad25_20x20.png" width="20" valign="middle"> Dinh dang .ipv la gi

**`.ipv`** (ibisPaint Project Version) la dinh dang file du an thuoc so huu cua ung dung ibisPaint X. No luu tru toan bo du lieu cua mot du an ve: cac layer, bang mau, duong dan ve (stroke path), brush settings, va metadata du an. Day la dinh dang binary da nang, khong phai la hinh anh, va khong the doc boi cac phan mem chuan.

Dinh dang nay khong dong voi bat ky chuan hinh anh nao hien co. No khong phai la PNG, JPEG, BMP, WebP, hay TIFF. No la mot cau truc du lieu rieng biet duoc thiet ke de luu tru nhieu loai du lieu khac nhau trong cung mot file: du lieu pixel (duoi dang PNG da nen), du lieu vector (duong dan brush stroke), cau hinh layer (blend mode, opacity, vi tri), va metadata (ten du an, thoi gian tao, phien ban ibisPaint).

**Tại sao ibisPaint khong dung PNG/JPEG thuong?** Vi mot du an ibisPaint thuong chua nhieu layer doc lap, moi layer co kich thuoc rieng, blend mode rieng, va opacity rieng. PNG hoac JPEG chi luu duoc mot hinh anh da gop (flattened), trong khi .ipv giu nguyen toan bo cau truc layer de nguoi dung co the quay lai chinh sua tung layer mot cach doc lap. Day la tuong tu nhu cach Photoshop luu file .psd hoac Procreate luu file .procreate.

| Thuoc tinh | Mo ta |
|---|---|
| Phan mo rong | `.ipv` |
| Loai file | Binary (thuoc so huu) |
| Ung dung nguon | ibisPaint X (iOS / Android) |
| Noi dung | Layer data, canvas, color table, stroke paths, metadata |
| Hinh anh noi bo | PNG (nen), co the chua nhieu PNG trong mot file |
| Khong phai la | PNG, JPEG, BMP, WebP hay bat ky dinh dang anh chuan nao |

> [!TIP]
> Cach don gian nhat de xuat PNG tu ibisPaint la dung chuc nang Export co san trong ung dung (Menu > Export > PNG). Tuy nhien, trong mot so truong hop (file bi loi, ung dung crash, can xuat hang loat), viec trich xuat truc tiep tu file .ipv la phuong phap duy nhat kha thi.

---

## <img src="https://fonts.gstatic.com/s/i/short-strings/materialsymbols/outlined/account_tree_wght400grad25_20x20.png" width="20" valign="middle"> Cau truc ky thuat cua file .ipv

Duoi day la ket qua phan tich reverse engineering tren cau truc binary cua file .ipv. Cau truc co the thay doi giua cac phien ban ibisPaint, nhung cac phan tu co ban da duoc xac dinh nhat quan.

### 3.1. Header chinh

File bat dau voi mot header co do dai co dinh chua thong tin ve du an va canvas. Header nay luon o cuoi cung cua file, giup xac dinh nhanh kich thuoc canvas ma khong can phan tich toan bo file.

```
Offset   Size   Type       Mo ta
------   ----   ----       ----
0x00     4      bytes      Magic number / Version: 01 00 01 00
0x04     4      uint32     So hieu phien ban ibisPaint (thuong la 29 = 0x1D)
0x08     8      bytes      Timestamp (epoch milliseconds, big-endian)
0x10     4      uint32     Canvas Width (big-endian)
0x14     4      uint32     Canvas Height (big-endian)
0x18     4      uint32     Kich thuoc metadata (xap xi)
0x1C     1      byte       So luong section tiep theo
0x1D     ...    bytes      Ten section ID (ASCII string, ket thuc bang 0x00)
```

**Vi du header thuc te** (file Khong Co Tieu De6.ipv):

```
01 00 01 00  -- Magic: phien ban 1, sub-version 1
00 00 00 1D  -- So phien ban ibisPaint: 29
41 DA 74 16 F5 1D 8C 65  -- Timestamp
00 00 03 E8  -- Canvas Width: 1000 pixels
00 00 03 E8  -- Canvas Height: 1000 pixels
00 0A        -- Dai section name: 10 bytes
4D 4C 58 30 41 33 34 4F 56 43  -- Section ID: "MLX0A34OVC" (unique per project)
```

> [!IMPORTANT]
> Bytes tai offset **0x10-0x17** luon luu kich thuoc canvas duoi dang hai gia tri uint32 big-endian (Width, Height). Day la thong tin quan trong nhat de xac dinh PNG artwork dung, vi PNG artwork nguyen ban phai co kich thuoc chinh xac bang voi canvas.

### 3.2. Bang mau (Color Table)

Ngay sau header chinh la mot bang mau (color palette) duoc su dung boi du an. Bang mau nay luu tru cac mau duoc dung trong thanh mau (color picker) cua ibisPaint, khong phai la mau cua artwork. No giup ibisPaint hien thi lai danh sach mau yeu thich khi nguoi dung mo lai du an.

Bang mau co cau truc tuong doi don gian: mot chuoi cac gia tri mau theo tung pixel, thuong duoc nen bang Deflate (cung thuat toan nen dung trong PNG). Muc dich chinh cua phan nay la luu trang thai giao dien nguoi dung, khong anh huong den noi dung artwork.

### 3.3. Du lieu layer

Phan lon noi dung cua file .ipv la du lieu cua tung layer. Moi layer bao gom:

- **Du lieu pixel**: Duoc luu duoi dang PNG da nen, nhung khong nam trong mot PNG file doc lap. Thay vao do, du lieu PNG duoc "nhung" (embedded) truc tiep vao stream binary cua file .ipv. Ban co the tim thay chu ky PNG (`89 50 4E 47`) xuat hien nhieu lan trong file.
- **Metadata layer**: Gom blend mode (Normal, Multiply, Screen, Overlay...), opacity (0-255), vi tri (x, y offset so voi canvas), va kich thuoc layer. Metadata nay thuong nam truoc du lieu pixel cua layer tuong ung.

**Cau truc metadata layer (RPNG block)**

Mot so layer duoc tien boi mot block "RPNG" (co the la "Raw PNG" hoac "Recorded PNG"). Block nay chua thong tin ve vi tri va kich thuoc cua layer:

```
Offset   Type     Mo ta
------   ----     ----
0x00     4 bytes  Marker: "RPNG" (52 50 4E 47)
0x04     uint32   Header size (thuong la 45 = 0x2D)
0x08     uint32   Flags (0 = khong co dac biet)
0x0C     ...      Layer metadata (vi tri, kich thuoc, blend mode)
         ...      Du lieu PNG (89 50 4E 47 ... IEND)
```

### 3.4. Du lieu canvas da gop (Merged Artwork)

Ben canh cac layer rieng le, file .ipv cung luu tru mot ban sao cua toan bo artwork da gop (merged/flattened). Day la kha nang cao la PNG ma ibisPaint hien thi trong giao dien preview (thumbnail) va dung de export nhanh khi nguoi dung chon "Export as PNG".

**Dac diem de nhan biet merged artwork:**

| Thuoc tinh | Layer rieng le | Merged artwork |
|---|---|---|
| Kich thuoc | Co the nho hon canvas | Bang chinh xac kich thuoc canvas |
| Transparency | Thuong co vung trong suot | Rất ít hoac khong co vung trong suot |
| Vi tri trong file | O giua file | Thuong o cuoi file |
| So unique colors | It (mot layer) | Nhieu (tat ca layer da gop) |
| Opacity | Co vung semi-transparent | Toan bo hoac phan lon la opaque |

Mot merged artwork PNG thuong co kich thuoc bang chinh xac voi canvas (doc tu header tai offset 0x10-0x17) va gan nhu 100% pixel la opaque (alpha = 255). Day la tieu chi quan trong nhat de phan biet merged artwork voi cac layer rieng le.

### 3.5. Metadata cuoi file

Cuoi file .ipv chua mot phan metadata gom:
- **File header trung lai**: Mot ban sao cua header chinh (magic number, canvas size, timestamp), giup ibisPaint doc nhanh thong tin co ban ma khong can quet toan bo file.
- **Project ID**: Mot chuoi ky tu duy nhat xac dinh du an (vi du "MLX0A34OVC", "WNDDGOCOSO", "SI9RNAAZGN").
- **Ten du an**: Duoc luu duoi dang UTF-8, ket thuc bang null byte.
- **Footer marker**: Cac gia tri dac biet de danh dau ket thuc file.

---

## <img src="https://fonts.gstatic.com/s/i/short-strings/materialsymbols/outlined/build_wght400grad25_20x20.png" width="20" valign="middle"> Huong dan trich xuat PNG

### 4.1. Yeu cau he thong

| Yeu cau | Phiên ban toi thieu | Ghi chu |
|---|---|---|
| Python | 3.6+ | Khuyen dung 3.9+ |
| Pillow (PIL) | 8.0+ | De verify PNG hop le |
| He dieu hanh | Bat ky | Windows, macOS, Linux |

Cai dat dependencies:

```bash
pip install Pillow
```

### 4.2. Cach 1: Su dung script Python (Khuyen dung)

Script `extract_ipv.py` duoc thiet ke de trich xuat PNG artwork nguyen ban tu file .ipv mot cach tu dong va an toan.

```bash
# Trich xuat mot file
python3 extract_ipv.py duong/dan/toi/file.ipv

# Trich xuat nhieu file cung luc
python3 extract_ipv.py file1.ipv file2.ipv file3.ipv

# Trich xuat tat ca file .ipv trong thu muc
python3 extract_ipv.py thu_muc_chua_ipv/*.ipv
```

**Cach script hoat dong:**

1. **Doc header**: Lay kich thuoc canvas (width, height) tu offset 0x10-0x17 cua file.
2. **Quet toan bo file**: Tim tat ca chu ky PNG (`89 50 4E 47`) va ket thuc PNG (`49 45 4E 44 AE 42 60 82`) trong file.
3. **Phan loai PNG**: Voi moi PNG tim thay, doc IHDR chunk de lay kich thuoc, roi so sanh voi kich thuoc canvas.
4. **Chon PNG dung**: PNG co kich thuoc khop voi canvas va co ty le opaque cao nhat la merged artwork.
5. **Xuat file**: Ghi du lieu PNG ra file moi voi cung ten nhung phan mo rong `.png`.

```python
import struct
import sys

def extract_ipv(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    # Doc kich thuoc canvas tu header
    canvas_w = struct.unpack('>I', data[16:20])[0]
    canvas_h = struct.unpack('>I', data[20:24])[0]

    # Tim tat ca PNG
    matches = []
    pos = 0
    while True:
        idx = data.find(b'\x89PNG', pos)
        if idx == -1:
            break
        iend = data.find(b'IEND', idx)
        if iend == -1:
            pos = idx + 1
            continue
        png_end = iend + 8  # IEND + CRC (4 bytes)

        # Doc kich thuoc PNG tu IHDR
        ihdr = data[idx + 16:idx + 24]
        pw = struct.unpack('>I', ihdr[0:4])[0]
        ph = struct.unpack('>I', ihdr[4:8])[0]

        if pw == canvas_w and ph == canvas_h:
            matches.append((idx, png_end, png_end - idx))

        pos = png_end

    if not matches:
        print(f"Khong tim thay PNG khop voi canvas {canvas_w}x{canvas_h}")
        return

    # Lay PNG cuoi cung (thuong la merged artwork)
    start, end, size = matches[-1]
    out = filepath.rsplit('.', 1)[0] + '.png'
    with open(out, 'wb') as f:
        f.write(data[start:end])

    print(f"Da trich xuat: {out} ({size:,} bytes, {canvas_w}x{canvas_h})")

if __name__ == '__main__':
    for f in sys.argv[1:]:
        extract_ipv(f)
```

### 4.3. Cach 2: Trich xuat thu cong voi hex editor

Neu ban muon hieu ro qua trinh hoac khong co Python, ban co the trich xuat PNG thu cong bang hex editor nhu HxD (Windows), 0xED (macOS), hoac hexdump (Linux).

**Buoc 1: Mo file .ipv bang hex editor**

Tai va cai dat mot hex editor bat ky. HxD cho Windows la lua chon tot nhat cho nguoi moi bat dau. Mo file .ipv, ban se thay du lieu binary duoc hien thi dang hex.

**Buoc 2: Xac dinh kich thuoc canvas**

Nhin vao offset `0x10` (dong thu 3, cot thu 3 trong hien thi hex mac dinh cua HxD). Doc 4 bytes tai offset 0x10 (width) va 4 bytes tai offset 0x14 (height). Vi du, neu thay `00 00 03 E8` tai ca hai vi tri, canvas la 1000x1000.

**Buoc 3: Tim chu ky PNG**

Su dung chuc nang Search (Ctrl+F trong HxD), chon "Hex values", va tim kiem `89504E47`. Day la magic number cua PNG. Danh dau vi tri tim thay dau tien.

**Buoc 4: Xac dinh ket thuc PNG**

Tu vi tri PNG bat dau, tim kiem tiep `49454E44`. Day la marker "IEND" (Image End) cua PNG. Noi dung PNG ket thuc 4 bytes sau IEND marker (bao gom CRC).

**Buoc 5: Copy va luu**

Select tu byte `89` dau tien den byte cuoi cung cua CRC (8 bytes sau IEND), copy, paste vao file moi, va luu voi phan mo rong `.png`. Mo file bang trinh duyet hinh anh de kiem tra.

> [!WARNING]
> Mot file .ipv co the chua nhieu PNG. PNG dau tien ban tim thay thuong la mot layer rieng le (co the co kich thuoc nho hon canvas va nhieu vung trong suot). Ban can tim PNG co kich thuoc **bang chinh xac** voi canvas de lay artwork nguyen ban.

---

## <img src="https://fonts.gstatic.com/s/i/short-strings/materialsymbols/outlined/psychology_wght400grad25_20x20.png" width="20" valign="middle"> Phan tich chuyen sau

### 5.1. Tai sao co nhieu PNG trong mot file .ipv

Mot file .ipv thuong chua tu 2 den 4 (hoac nhieu hon) PNG duoi dang embedded chunks. Moi PNG dai dien cho mot thanh phan khac nhau cua du an:

| Vi tri | Vai tro | Dac diem |
|---|---|---|
| PNG dau tien | Layer hoac thumbnail | Thuong co kich thuoc nho hon canvas, nhieu vung transparent |
| PNG giua | Layer khac hoac preview | Kich thuoc bien dong, co the chua semi-transparent pixels |
| PNG cuoi cung (canvas size) | Merged artwork | Kich thuoc bang canvas, gan nhu toan opaque |

Vi du thuc te tu phan tich file "Khong Co Tieu De6.ipv" (canvas 1000x1000):

```
PNG #1: 648x640, 52,771 bytes    --> Layer rieng le (93.8% opaque, nhung sai kich thuoc)
PNG #2: 816x804, 349,157 bytes   --> Layer khac (72.0% opaque, sai kich thuoc)
PNG #3: 1000x1000, 288,546 bytes --> Merged artwork (100% opaque, dung kich thuoc canvas)
```

Chi PNG #3 moi la artwork hoan chinh. Hai PNG con lai chi la du lieu cua tung layer rieng le.

### 5.2. Cach xac dinh PNG artwork nguyen ban

Khi co nhieu PNG trong mot file .ipv, dung cac tieu chi sau de xac dinh PNG chua artwork nguyen ban:

**Tieu chi 1: Kich thuoc khop canvas (quan trong nhat)**

PNG artwork phai co kich thuoc **chinh xac** bang voi kich thuoc canvas ghi trong header (offset 0x10-0x17). Neu canvas la 1000x1000, PNG artwork cung phai la 1000x1000. Day la tieu chi co the tin cay nhat.

**Tieu chi 2: Ty le pixel opaque**

Merged artwork thuong co ty le opaque rat cao (tre'n 95%), vi no la ket qua cua viec gop tat ca layer tren nen trang (white background). Layer rieng le thuong co nhieu vung trong suot (transparent).

**Tieu chi 3: So luong unique colors**

Merged artwork chua mau tu tat ca layer nen co so luong mau doc nhat (unique colors) nhieu hon dang ke so voi bat ky layer rieng le nao. Mot layer chi ve duong vien (lineart) co the chi co it mau, nhung merged artwork co ca lineart, fill, shading, va background.

**Thuat toan lua chon PNG:**

```
1. Doc canvas_w va canvas_h tu header (offset 0x10-0x17)
2. Tim tat ca PNG trong file
3. Loc nhung PNG co kich thuoc == (canvas_w, canvas_h)
4. Neu co nhieu PNG khop, chon PNG cuoi cung (thuong la merged)
5. Neu khong co PNG nao khop, chon PNG co kich thuoc lon nhat
```

### 5.3. Layer compositing (ghep nhieu layer)

Trong truong hop file .ipv khong chua merged artwork (chi chua layer rieng le), ban can ghep (composite) cac layer lai de tao artwork hoan chinh.

> [!CAUTION]
> Qua trinh compositing thu cong se khong tao ra ket qua chinh xac 100% so voi ibisPaint, boi nhung ly do: blend mode phuc tap, layer mask, adjustment layer, va thu tu layer co the khong duoc luu hoan chinh trong file. Dung cach nay chi khi khong con lua chon khac.

**Viec compositing can biet:**

- **Thu tu layer**: File .ipv khong luu ro rang thu tu z-order cua cac layer. Ban can phan tich metadata RPNG block de doan.
- **Blend mode**: Moi layer co blend mode khac nhau (Normal, Multiply, Screen...). Cac blend mode nay can duoc ap dung dung cach.
- **Opacity**: Moi layer co gia tri opacity tu 0 den 255.
- **Vi tri**: Moi layer co offset (x, y) so voi canvas.

Vi phan tich metadata RPNG chua day du, viec compositing chinh xac hien tai van la mot thach thuc. Cach khuyen dung la luon chon PNG merged (canvas size) khi co the.

---

## <img src="https://fonts.gstatic.com/s/i/short-strings/materialsymbols/outlined/bug_report_wght400grad25_20x20.png" width="20" valign="middle"> Xu ly su co thuong gap

| Van de | Nguyen nhan | Cach khac phuc |
|---|---|---|
| PNG xuat ra toan mau trang/trang | Da lay PNG background thay vi merged artwork | Dung script co kiem tra canvas size. Chi lay PNG co kich thuoc khop voi header. |
| PNG co duong ke loi/lun xun | Da lay layer rieng le thay vi merged | Tim PNG cuoi cung co kich thuoc bang canvas. Layer rieng le thuong o giua file, merged thuong o cuoi. |
| PNG co vung trong suot (transparent) | Day la layer chua background | Can ghep (composite) voi layer background, hoac tim merged PNG khac trong file. |
| Khong tim thay PNG nao khop canvas | File khong chua merged artwork, chi co layer | Phai composite cac layer thu cong. Xem phan 5.3. |
| PNG dung nhung sai mau | Color profile khac nhau | Chuyen doi color profile bang ImageMagick: `convert input.png -profile sRGB.icc output.png` |
| File .ipv khong mo duoc / loi | File bi loi hoac khong phai .ipv that | Kiem tra 4 bytes dau tien: phai la `01 00 01 00`. Neu khong, file co the bi loi hoac la dinh dang khac. |
| Script bao "Khong tim thay PNG" | PNG duoc nen bang cach khac | Mot so phien ban ibisPaint co the dung deflate thieu thay vi PNG. Can phan tich them. |
| Artwork bi cat / thieu | Layer vuot khoi canvas | Kiem tra xem co layer nao co kich thuoc lon hon canvas. Co the can ghep nhieu PNG. |

> [!TIP]
> Luon kiem tra kich thuoc canvas truoc khi trich xuat. Gia tri tai offset 0x10-0x17 cua file .ipv la nguon chan ly tin cay nhat. Neu PNG ban trich xuat co kich thuoc khac voi gia tri nay, do chua chac la artwork nguyen ban.

---

## <img src="https://fonts.gstatic.com/s/i/short-strings/materialsymbols/outlined/construction_wght400grad25_20x20.png" width="20" valign="middle"> Cong cu & tai lieu tham khao

**Cong cu su dung trong tai lieu nay:**

| Cong cu | Muc dich | Link |
|---|---|---|
| Python 3 | Ngon ngu lap trinh chinh | [python.org](https://python.org) |
| Pillow (PIL) | Xu ly hinh anh | [pillow.readthedocs.io](https://pillow.readthedocs.io) |
| HxD | Hex editor (Windows) | [mh-nexus.de/en/hxd](https://mh-nexus.de/en/hxd/) |
| 0xED | Hex editor (macOS) [0xed.it](https://www.suavetech.com/0xed/0xed.html) |
| ImageMagick | Xu ly anh command-line | [imagemagick.org](https://imagemagick.org) |

**Tai lieu tham khao:**

- [PNG Specification (ISO/IEC 15948:2003)](https://www.w3.org/TR/2003/REC-PNG-20031110/) -- Chu ky PNG, IHDR chunk, IEND marker
- [ibisPaint X Official Site](https://ibispaint.com/) -- Ung dung nguon cua file .ipv
- [Python struct module](https://docs.python.org/3/library/struct.html) -- Xu ly binary data trong Python
- [ZLIB / Deflate](https://www.rfc-editor.org/rfc/rfc1950) -- Thuat toan nen duoc su dung trong PNG

---

<div align="center">

**Tai lieu duoc xay dung dua tren viec phan tich doc lap.  
Khong lien he voi ibisPaint Inc.**

<br>

[![](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)

</div>
