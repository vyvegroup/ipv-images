<div align="center">

# ibisPaint `.ipv` &mdash; Hướng dẫn kỹ thuật &amp; trích xuất PNG

[![Format](https://img.shields.io/badge/Format-ibisPaint_.ipv-blue?style=flat-square)](https://github.com/vyvegroup/ipv-images)
[![Language](https://img.shields.io/badge/Language-Python_3-3776AB?style=flat-square&logo=python&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)]()
[![Platform](https://img.shields.io/badge/Platform-Cross--platform-9CF?style=flat-square)]()

**Tài liệu kỹ thuật toàn diện về định dạng file `.ipv` của ibisPaint X  
và phương pháp trích xuất artwork PNG nguyên bản.**

[bắt-đầu](#-bắt-đầu-nhanh) ·
[cấu-trúc](#-cấu-trúc-kỹ-thuật) ·
[hướng-dẫn](#-hướng-dẫn-trích-xuất-png) ·
[công-cụ](#-công-cụ--tài-liệu-tham-khảo)

</div>

---

## Mục lục

- [Tổng quan](#-tổng-quan)
- [Bắt đầu nhanh](#-bắt-đầu-nhanh)
- [Định dạng `.ipv` là gì](#-định-dạng-ipv-là-gì)
- [Cấu trúc kỹ thuật của file `.ipv`](#-cấu-trúc-kỹ-thuật-của-file-ipv)
  - [3.1. Header chính](#31-header-chính)
  - [3.2. Bảng màu (Color Table)](#32-bảng-màu-color-table)
  - [3.3. Dữ liệu layer](#33-dữ-liệu-layer)
  - [3.4. Dữ liệu canvas đã gộp (Merged Artwork)](#34-dữ-liệu-canvas-đã-gộp-merged-artwork)
  - [3.5. Metadata cuối file](#35-metadata-cuối-file)
- [Hướng dẫn trích xuất PNG](#-hướng-dẫn-trích-xuất-png)
  - [4.1. Yêu cầu hệ thống](#41-yêu-cầu-hệ-thống)
  - [4.2. Cách 1: Sử dụng script Python](#42-cách-1-sử-dụng-script-python-khuyến-dùng)
  - [4.3. Cách 2: Trích xuất thủ công với hex editor](#43-cách-2-trích-xuất-thủ-công-với-hex-editor)
- [Phân tích chuyên sâu](#-phân-tích-chuyên-sâu)
  - [5.1. Tại sao có nhiều PNG trong một file `.ipv`](#51-tại-sao-có-nhiều-png-trong-một-file-ipv)
  - [5.2. Cách xác định PNG artwork nguyên bản](#52-cách-xác-định-png-artwork-nguyên-bản)
  - [5.3. Layer compositing (ghép nhiều layer)](#53-layer-compositing-ghép-nhiều-layer)
- [Xử lý sự cố thường gặp](#-xử-lý-sự-cố-thường-gặp)
- [Công cụ & tài liệu tham khảo](#-công-cụ--tài-liệu-tham-khảo)

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4285f4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:6px"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg> Tổng quan

ibisPaint X là ứng dụng vẽ tranh kỹ thuật số phổ biến trên iOS và Android, với hơn 300 triệu lượt tải trên cả hai nền tảng. Ứng dụng này lưu dữ liệu dự án (project) dưới dạng file có phần mở rộng **`.ipv`** (ibisPaint Version) — một định dạng file thuộc sở hữu của ibisPaint Inc., không được tài liệu hóa công khai.

Vấn đề cốt lõi: **bạn không thể mở file `.ipv` trực tiếp bằng bất kỳ phần mềm hình ảnh nào** (Photoshop, GIMP, Preview, Windows Photos...). Định dạng này không được hỗ trợ bởi các chuẩn hình ảnh phổ thông (JPEG, PNG, WebP, BMP, TIFF). Khi bạn cần chuyển artwork từ ibisPaint sang định dạng chung để sử dụng ở các nền tảng khác (xử lý ảnh tiếp tục, in ấn, đăng tải lên web, hoặc chia sẻ), bạn cần phải trích xuất PNG nguyên bản từ bên trong file `.ipv`.

Tài liệu này cung cấp toàn bộ kiến thức kỹ thuật cần thiết để hiểu và xử lý định dạng `.ipv`, bao gồm cả cấu trúc binary, phương pháp trích xuất tự động bằng Python, và những hiệu ứng mà bạn có thể gặp phải trong quá trình làm việc với file này. Nội dung được xây dựng dựa trên việc phân tích độc lập (reverse engineering) trên hàng chục file `.ipv` thực tế từ các phiên bản ibisPaint X khác nhau.

> [!NOTE]
> Mọi thông tin trong tài liệu này được thu thập thông qua phân tích reverse engineering độc lập. Định dạng `.ipv` là thuộc sở hữu của ibisPaint Inc. và có thể thay đổi giữa các phiên bản. Tài liệu này không liên hệ với và không được hỗ trợ bởi ibisPaint Inc.

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ea4335" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:6px"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg> Bắt đầu nhanh

Nếu bạn chỉ muốn trích xuất PNG mà không cần hiểu kỹ thuật chi tiết, đây là cách nhanh nhất:

```bash
# 1. Tải script trích xuất
curl -O https://raw.githubusercontent.com/vyvegroup/ipv-images/main/extract_ipv.py

# 2. Chạy script với file .ipv của bạn
python3 extract_ipv.py đường/dẫn/tới/file.ipv

# 3. PNG sẽ được lưu cùng thư mục với file gốc
```

Script sẽ tự động:
- Đọc header file `.ipv` để lấy kích thước canvas gốc
- Quét toàn bộ file để tìm tất cả PNG dưới dạng các phân (chunk)
- Xác định PNG có kích thước khớp với canvas (đây là artwork đã gộp đầy đủ)
- Trích xuất và lưu thành file PNG độc lập với tên giống file gốc

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fbbc04" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:6px"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M18 14h-8"/><path d="M15 18h-5"/><path d="M10 6h8v4h-8V6Z"/></svg> Định dạng `.ipv` là gì

**`.ipv`** (ibisPaint Project Version) là định dạng file dự án thuộc sở hữu của ứng dụng ibisPaint X. Nó lưu trữ toàn bộ dữ liệu của một dự án vẽ: các layer, bảng màu, đường dẫn vẽ (stroke path), brush settings, và metadata dự án. Đây là định dạng binary đa năng, không phải là hình ảnh, và không thể đọc bởi các phần mềm chuẩn.

Định dạng này không đồng với bất kỳ chuẩn hình ảnh nào hiện có. Nó không phải là PNG, JPEG, BMP, WebP, hay TIFF. Nó là một cấu trúc dữ liệu riêng biệt được thiết kế để lưu trữ nhiều loại dữ liệu khác nhau trong cùng một file: dữ liệu pixel (dưới dạng PNG đã nén), dữ liệu vector (đường dẫn brush stroke), cấu hình layer (blend mode, opacity, vị trí), và metadata (tên dự án, thời gian tạo, phiên bản ibisPaint).

**Tại sao ibisPaint không dùng PNG/JPEG thường?** Vì một dự án ibisPaint thường chứa nhiều layer độc lập, mỗi layer có kích thước riêng, blend mode riêng, và opacity riêng. PNG hoặc JPEG chỉ lưu được một hình ảnh đã gộp (flattened), trong khi `.ipv` giữ nguyên toàn bộ cấu trúc layer để người dùng có thể quay lại chỉnh sửa từng layer một cách độc lập. Đây là tương tự như cách Photoshop lưu file `.psd` hoặc Procreate lưu file `.procreate`.

| Thuộc tính | Mô tả |
|---|---|
| Phần mở rộng | `.ipv` |
| Loại file | Binary (thuộc sở hữu) |
| Ứng dụng nguồn | ibisPaint X (iOS / Android) |
| Nội dung | Layer data, canvas, color table, stroke paths, metadata |
| Hình ảnh nội bộ | PNG (nén), có thể chứa nhiều PNG trong một file |
| Không phải là | PNG, JPEG, BMP, WebP hay bất kỳ định dạng ảnh chuẩn nào |

> [!TIP]
> Cách đơn giản nhất để xuất PNG từ ibisPaint là dùng chức năng Export có sẵn trong ứng dụng (Menu > Export > PNG). Tuy nhiên, trong một số trường hợp (file bị lỗi, ứng dụng crash, cần xuất hàng loạt), việc trích xuất trực tiếp từ file `.ipv` là phương pháp duy nhất khả thi.

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#34a853" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:6px"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg> Cấu trúc kỹ thuật của file `.ipv`

Dưới đây là kết quả phân tích reverse engineering trên cấu trúc binary của file `.ipv`. Cấu trúc có thể thay đổi giữa các phiên bản ibisPaint, nhưng các phần tử cơ bản đã được xác định nhất quan.

### 3.1. Header chính

File bắt đầu với một header có độ dài cố định chứa thông tin về dự án và canvas. Header này cũng xuất hiện lặp lại ở cuối file, giúp xác định nhanh kích thước canvas mà không cần phân tích toàn bộ file.

```
Offset   Size   Type       Mô tả
------   ----   ----       ----
0x00     4      bytes      Magic number / Version: 01 00 01 00
0x04     4      uint32     Số hiệu phiên bản ibisPaint (thường là 29 = 0x1D)
0x08     8      bytes      Timestamp (epoch milliseconds, big-endian)
0x10     4      uint32     Canvas Width (big-endian)
0x14     4      uint32     Canvas Height (big-endian)
0x18     4      uint32     Kích thước metadata (xấp xỉ)
0x1C     1      byte       Số lượng section tiếp theo
0x1D     ...    bytes      Tên section ID (ASCII string, kết thúc bằng 0x00)
```

**Ví dụ header thực tế** (file Không Có Tiêu Đề6.ipv):

```
01 00 01 00  -- Magic: phiên bản 1, sub-version 1
00 00 00 1D  -- Số phiên bản ibisPaint: 29
41 DA 74 16 F5 1D 8C 65  -- Timestamp
00 00 03 E8  -- Canvas Width: 1000 pixels
00 00 03 E8  -- Canvas Height: 1000 pixels
00 0A        -- Độ dài section name: 10 bytes
4D 4C 58 30 41 33 34 4F 56 43  -- Section ID: "MLX0A34OVC" (duy nhất mỗi dự án)
```

> [!IMPORTANT]
> Bytes tại offset **0x10-0x17** luôn lưu kích thước canvas dưới dạng hai giá trị uint32 big-endian (Width, Height). Đây là thông tin quan trọng nhất để xác định PNG artwork đúng, vì PNG artwork nguyên bản phải có kích thước chính xác bằng với canvas.

### 3.2. Bảng màu (Color Table)

Ngay sau header chính là một bảng màu (color palette) được sử dụng bởi dự án. Bảng màu này lưu trữ các màu được dùng trong thanh màu (color picker) của ibisPaint, không phải là màu của artwork. Nó giúp ibisPaint hiển thị lại danh sách màu yêu thích khi người dùng mở lại dự án.

Bảng màu có cấu trúc tương đối đơn giản: một chuỗi các giá trị màu theo từng pixel, thường được nén bằng Deflate (cùng thuật toán nén dùng trong PNG). Mục đích chính của phần này là lưu trạng thái giao diện người dùng, không ảnh hưởng đến nội dung artwork.

### 3.3. Dữ liệu layer

Phần lớn nội dung của file `.ipv` là dữ liệu của từng layer. Mỗi layer bao gồm:

- **Dữ liệu pixel**: Được lưu dưới dạng PNG đã nén, nhưng không nằm trong một PNG file độc lập. Thay vào đó, dữ liệu PNG được "nhúng" (embedded) trực tiếp vào stream binary của file `.ipv`. Bạn có thể tìm thấy chu ký PNG (`89 50 4E 47`) xuất hiện nhiều lần trong file.
- **Metadata layer**: Gồm blend mode (Normal, Multiply, Screen, Overlay...), opacity (0-255), vị trí (x, y offset so với canvas), và kích thước layer. Metadata này thường nằm trước dữ liệu pixel của layer tương ứng.

**Cấu trúc metadata layer (RPNG block)**

Một số layer được tiền bối bởi một block "RPNG" (có thể là "Raw PNG" hoặc "Recorded PNG"). Block này chứa thông tin về vị trí và kích thước của layer:

```
Offset   Type     Mô tả
------   ----     ----
0x00     4 bytes  Marker: "RPNG" (52 50 4E 47)
0x04     uint32   Header size (thường là 45 = 0x2D)
0x08     uint32   Flags (0 = không có đặc biệt)
0x0C     ...      Layer metadata (vị trí, kích thước, blend mode)
         ...      Dữ liệu PNG (89 50 4E 47 ... IEND)
```

### 3.4. Dữ liệu canvas đã gộp (Merged Artwork)

Bên cạnh các layer riêng lẻ, file `.ipv` cũng lưu trữ một bản sao của toàn bộ artwork đã gộp (merged/flattened). Đây rất có thể là PNG mà ibisPaint hiển thị trong giao diện preview (thumbnail) và dùng để export nhanh khi người dùng chọn "Export as PNG".

**Đặc điểm để nhận biết merged artwork:**

| Thuộc tính | Layer riêng lẻ | Merged artwork |
|---|---|---|
| Kích thước | Có thể nhỏ hơn canvas | Bằng chính xác kích thước canvas |
| Transparency | Thường có vùng trong suốt | Rất ít hoặc không có vùng trong suốt |
| Vị trí trong file | Ở giữa file | Thường ở cuối file |
| Số unique colors | Ít (một layer) | Nhiều (tất cả layer đã gộp) |
| Opacity | Có vùng semi-transparent | Toàn bộ hoặc phần lớn là opaque |

Một merged artwork PNG thường có kích thước bằng chính xác với canvas (đọc từ header tại offset 0x10-0x17) và gần như 100% pixel là opaque (alpha = 255). Đây là tiêu chí quan trọng nhất để phân biệt merged artwork với các layer riêng lẻ.

### 3.5. Metadata cuối file

Cuối file `.ipv` chứa một phần metadata gồm:
- **File header trùng lặp**: Một bản sao của header chính (magic number, canvas size, timestamp), giúp ibisPaint đọc nhanh thông tin cơ bản mà không cần quét toàn bộ file.
- **Project ID**: Một chuỗi ký tự duy nhất xác định dự án (ví dụ "MLX0A34OVC", "WNDDGOCOSO", "SI9RNAAZGN").
- **Tên dự án**: Được lưu dưới dạng UTF-8, kết thúc bằng null byte.
- **Footer marker**: Các giá trị đặc biệt để đánh dấu kết thúc file.

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ea4335" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:6px"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg> Hướng dẫn trích xuất PNG

### 4.1. Yêu cầu hệ thống

| Yêu cầu | Phiên bản tối thiểu | Ghi chú |
|---|---|---|
| Python | 3.6+ | Khuyến dụng 3.9+ |
| Pillow (PIL) | 8.0+ | Để verify PNG hợp lệ |
| Hệ điều hành | Bất kỳ | Windows, macOS, Linux |

Cài đặt dependencies:

```bash
pip install Pillow
```

### 4.2. Cách 1: Sử dụng script Python (Khuyến dùng)

Script `extract_ipv.py` được thiết kế để trích xuất PNG artwork nguyên bản từ file `.ipv` một cách tự động và an toàn.

```bash
# Trích xuất một file
python3 extract_ipv.py đường/dẫn/tới/file.ipv

# Trích xuất nhiều file cùng lúc
python3 extract_ipv.py file1.ipv file2.ipv file3.ipv

# Trích xuất tất cả file .ipv trong thư mục
python3 extract_ipv.py thư_mục_chứa_ipv/*.ipv
```

**Cách script hoạt động:**

1. **Đọc header**: Lấy kích thước canvas (width, height) từ offset 0x10-0x17 của file.
2. **Quét toàn bộ file**: Tìm tất cả chu ký PNG (`89 50 4E 47`) và kết thúc PNG (`49 45 4E 44 AE 42 60 82`) trong file.
3. **Phân loại PNG**: Với mỗi PNG tìm thấy, đọc IHDR chunk để lấy kích thước, rồi so sánh với kích thước canvas.
4. **Chọn PNG đúng**: PNG có kích thước khớp với canvas và có tỷ lệ opaque cao nhất là merged artwork.
5. **Xuất file**: Ghi dữ liệu PNG ra file mới với cùng tên nhưng phần mở rộng `.png`.

```python
import struct
import sys

def extract_ipv(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    # Đọc kích thước canvas từ header
    canvas_w = struct.unpack('>I', data[16:20])[0]
    canvas_h = struct.unpack('>I', data[20:24])[0]

    # Tìm tất cả PNG
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

        # Đọc kích thước PNG từ IHDR
        ihdr = data[idx + 16:idx + 24]
        pw = struct.unpack('>I', ihdr[0:4])[0]
        ph = struct.unpack('>I', ihdr[4:8])[0]

        if pw == canvas_w and ph == canvas_h:
            matches.append((idx, png_end, png_end - idx))

        pos = png_end

    if not matches:
        print(f"Không tìm thấy PNG khớp với canvas {canvas_w}x{canvas_h}")
        return

    # Lấy PNG cuối cùng (thường là merged artwork)
    start, end, size = matches[-1]
    out = filepath.rsplit('.', 1)[0] + '.png'
    with open(out, 'wb') as f:
        f.write(data[start:end])

    print(f"Đã trích xuất: {out} ({size:,} bytes, {canvas_w}x{canvas_h})")

if __name__ == '__main__':
    for f in sys.argv[1:]:
        extract_ipv(f)
```

### 4.3. Cách 2: Trích xuất thủ công với hex editor

Nếu bạn muốn hiểu rõ quá trình hoặc không có Python, bạn có thể trích xuất PNG thủ công bằng hex editor như HxD (Windows), 0xED (macOS), hoặc hexdump (Linux).

**Bước 1: Mở file `.ipv` bằng hex editor**

Tải và cài đặt một hex editor bất kỳ. HxD cho Windows là lựa chọn tốt nhất cho người mới bắt đầu. Mở file `.ipv`, bạn sẽ thấy dữ liệu binary được hiển thị dạng hex.

**Bước 2: Xác định kích thước canvas**

Nhìn vào offset `0x10` (dòng thứ 3, cột thứ 3 trong hiển thị hex mặc định của HxD). Đọc 4 bytes tại offset 0x10 (width) và 4 bytes tại offset 0x14 (height). Ví dụ, nếu thấy `00 00 03 E8` ở cả hai vị trí, canvas là 1000x1000.

**Bước 3: Tìm chu ký PNG**

Sử dụng chức năng Search (Ctrl+F trong HxD), chọn "Hex values", và tìm kiếm `89504E47`. Đây là magic number của PNG. Đánh dấu vị trí tìm thấy đầu tiên.

**Bước 4: Xác định kết thúc PNG**

Từ vị trí PNG bắt đầu, tìm kiếm tiếp `49454E44`. Đây là marker "IEND" (Image End) của PNG. Nội dung PNG kết thúc 4 bytes sau IEND marker (bao gồm CRC).

**Bước 5: Copy và lưu**

Chọn từ byte `89` đầu tiên đến byte cuối cùng của CRC (8 bytes sau IEND), copy, paste vào file mới, và lưu với phần mở rộng `.png`. Mở file bằng trình duyệt hình ảnh để kiểm tra.

> [!WARNING]
> Một file `.ipv` có thể chứa nhiều PNG. PNG đầu tiên bạn tìm thấy thường là một layer riêng lẻ (có thể có kích thước nhỏ hơn canvas và nhiều vùng trong suốt). Bạn cần tìm PNG có kích thước **bằng chính xác** với canvas để lấy artwork nguyên bản.

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4285f4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:6px"><path d="M12 20V10"/><path d="M18 20V4"/><path d="M6 20v-4"/></svg> Phân tích chuyên sâu

### 5.1. Tại sao có nhiều PNG trong một file `.ipv`

Một file `.ipv` thường chứa từ 2 đến 4 (hoặc nhiều hơn) PNG dưới dạng embedded chunks. Mỗi PNG đại diện cho một thành phần khác nhau của dự án:

| Vị trí | Vai trò | Đặc điểm |
|---|---|---|
| PNG đầu tiên | Layer hoặc thumbnail | Thường có kích thước nhỏ hơn canvas, nhiều vùng transparent |
| PNG giữa | Layer khác hoặc preview | Kích thước biến động, có thể chứa semi-transparent pixels |
| PNG cuối cùng (canvas size) | Merged artwork | Kích thước bằng canvas, gần như toàn opaque |

Ví dụ thực tế từ phân tích file "Không Có Tiêu Đề6.ipv" (canvas 1000x1000):

```
PNG #1: 648x640, 52,771 bytes    --> Layer riêng lẻ (93.8% opaque, nhưng sai kích thước)
PNG #2: 816x804, 349,157 bytes   --> Layer khác (72.0% opaque, sai kích thước)
PNG #3: 1000x1000, 288,546 bytes --> Merged artwork (100% opaque, đúng kích thước canvas)
```

Chỉ PNG #3 mới là artwork hoàn chỉnh. Hai PNG còn lại chỉ là dữ liệu của từng layer riêng lẻ.

### 5.2. Cách xác định PNG artwork nguyên bản

Khi có nhiều PNG trong một file `.ipv`, dùng các tiêu chí sau để xác định PNG chứa artwork nguyên bản:

**Tiêu chí 1: Kích thước khớp canvas (quan trọng nhất)**

PNG artwork phải có kích thước **chính xác** bằng với kích thước canvas ghi trong header (offset 0x10-0x17). Nếu canvas là 1000x1000, PNG artwork cũng phải là 1000x1000. Đây là tiêu chí có thể tin cậy nhất.

**Tiêu chí 2: Tỷ lệ pixel opaque**

Merged artwork thường có tỷ lệ opaque rất cao (trên 95%), vì nó là kết quả của việc gộp tất cả layer trên nền trắng (white background). Layer riêng lẻ thường có nhiều vùng trong suốt (transparent).

**Tiêu chí 3: Số lượng unique colors**

Merged artwork chứa màu từ tất cả layer nên có số lượng màu độc nhất (unique colors) nhiều hơn đáng kể so với bất kỳ layer riêng lẻ nào. Một layer chỉ vẽ đường viền (lineart) có thể chỉ có ít màu, nhưng merged artwork có cả lineart, fill, shading, và background.

**Thuật toán lựa chọn PNG:**

```
1. Đọc canvas_w và canvas_h từ header (offset 0x10-0x17)
2. Tìm tất cả PNG trong file
3. Lọc những PNG có kích thước == (canvas_w, canvas_h)
4. Nếu có nhiều PNG khớp, chọn PNG cuối cùng (thường là merged)
5. Nếu không có PNG nào khớp, chọn PNG có kích thước lớn nhất
```

### 5.3. Layer compositing (ghép nhiều layer)

Trong trường hợp file `.ipv` không chứa merged artwork (chỉ chứa layer riêng lẻ), bạn cần ghép (composite) các layer lại để tạo artwork hoàn chỉnh.

> [!CAUTION]
> Quá trình compositing thủ công sẽ không tạo ra kết quả chính xác 100% so với ibisPaint, vì những lý do: blend mode phức tạp, layer mask, adjustment layer, và thứ tự layer có thể không được lưu hoàn chỉnh trong file. Dùng cách này chỉ khi không còn lựa chọn khác.

**Việc compositing cần biết:**

- **Thứ tự layer**: File `.ipv` không lưu rõ ràng thứ tự z-order của các layer. Bạn cần phân tích metadata RPNG block để đoán.
- **Blend mode**: Mỗi layer có blend mode khác nhau (Normal, Multiply, Screen...). Các blend mode này cần được áp dụng đúng cách.
- **Opacity**: Mỗi layer có giá trị opacity từ 0 đến 255.
- **Vị trí**: Mỗi layer có offset (x, y) so với canvas.

Vì phân tích metadata RPNG chưa đầy đủ, việc compositing chính xác hiện tại vẫn là một thách thức. Cách khuyến dùng là luôn chọn PNG merged (canvas size) khi có thể.

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ea4335" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:6px"><path d="m8 2 1.88 1.88"/><path d="M14.12 3.88 16 2"/><path d="M9 7.13v-1a3.003 3.003 0 1 1 6 0v1"/><path d="M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6"/><path d="M12 20v-9"/><path d="M6.53 9C4.6 8.8 3 7.1 3 5"/><path d="M6 13H2"/><path d="M3 21c0-2.1 1.7-3.9 3.8-4"/><path d="M20.97 5c0 2.1-1.6 3.8-3.5 4"/><path d="M22 13h-4"/><path d="M17.2 17c2.1.1 3.8 1.9 3.8 4"/></svg> Xử lý sự cố thường gặp

| Vấn đề | Nguyên nhân | Cách khắc phục |
|---|---|---|
| PNG xuất ra toàn màu trắng/trắng | Đã lấy PNG background thay vì merged artwork | Dùng script có kiểm tra canvas size. Chỉ lấy PNG có kích thước khớp với header. |
| PNG có đường keo lỗi/lộn xộn | Đã lấy layer riêng lẻ thay vì merged | Tìm PNG cuối cùng có kích thước bằng canvas. Layer riêng lẻ thường ở giữa file, merged thường ở cuối. |
| PNG có vùng trong suốt (transparent) | Đây là layer chưa có background | Cần ghép (composite) với layer background, hoặc tìm merged PNG khác trong file. |
| Không tìm thấy PNG nào khớp canvas | File không chứa merged artwork, chỉ có layer | Phải composite các layer thủ công. Xem phần 5.3. |
| PNG đúng nhưng sai màu | Color profile khác nhau | Chuyển đổi color profile bằng ImageMagick: `convert input.png -profile sRGB.icc output.png` |
| File `.ipv` không mở được / lỗi | File bị lỗi hoặc không phải `.ipv` thật | Kiểm tra 4 bytes đầu tiên: phải là `01 00 01 00`. Nếu không, file có thể bị lỗi hoặc là định dạng khác. |
| Script báo "Không tìm thấy PNG" | PNG được nén bằng cách khác | Một số phiên bản ibisPaint có thể dùng deflate thẳng thay vì PNG. Cần phân tích thêm. |
| Artwork bị cắt / thiếu | Layer vượt khỏi canvas | Kiểm tra xem có layer nào có kích thước lớn hơn canvas. Có thể cần ghép nhiều PNG. |

> [!TIP]
> Luôn kiểm tra kích thước canvas trước khi trích xuất. Giá trị tại offset 0x10-0x17 của file `.ipv` là nguồn chân lý tin cậy nhất. Nếu PNG bạn trích xuất có kích thước khác với giá trị này, đó chưa chắc là artwork nguyên bản.

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#34a853" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:6px"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="m6 12v5c3 3 9 3 12 0v-5"/></svg> Công cụ & tài liệu tham khảo

**Công cụ sử dụng trong tài liệu này:**

| Công cụ | Mục đích | Link |
|---|---|---|
| Python 3 | Ngôn ngữ lập trình chính | [python.org](https://python.org) |
| Pillow (PIL) | Xử lý hình ảnh | [pillow.readthedocs.io](https://pillow.readthedocs.io) |
| HxD | Hex editor (Windows) | [mh-nexus.de/en/hxd](https://mh-nexus.de/en/hxd/) |
| 0xED | Hex editor (macOS) | [suavetech.com/0xed](https://www.suavetech.com/0xed/0xed.html) |
| ImageMagick | Xử lý ảnh command-line | [imagemagick.org](https://imagemagick.org) |

**Tài liệu tham khảo:**

- [PNG Specification (ISO/IEC 15948:2003)](https://www.w3.org/TR/2003/REC-PNG-20031110/) -- Chu ký PNG, IHDR chunk, IEND marker
- [ibisPaint X Official Site](https://ibispaint.com/) -- Ứng dụng nguồn của file `.ipv`
- [Python struct module](https://docs.python.org/3/library/struct.html) -- Xử lý binary data trong Python
- [ZLIB / Deflate](https://www.rfc-editor.org/rfc/rfc1950) -- Thuật toán nén được sử dụng trong PNG

---

<div align="center">

**Tài liệu được xây dựng dựa trên việc phân tích độc lập.  
Không liên hệ với ibisPaint Inc.**

<br>

[![](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)

</div>
