#!/usr/bin/env python3
"""
extract_ipv.py - Trich xuat artwork PNG nguyen ban tu file .ipv (ibisPaint X)

Cach su dung:
    python3 extract_ipv.py file.ipv
    python3 extract_ipv.py file1.ipv file2.ipv file3.ipv
    python3 extract_ipv.py thu_muc/*.ipv

Tac gia: vyvegroup
Giay phe: MIT
"""

import struct
import sys
import os
from pathlib import Path


def read_canvas_size(data: bytes):
    """Doc kich thuoc canvas tu header .ipv (offset 0x10-0x17)."""
    if len(data) < 24:
        raise ValueError("File qua nho de doc header")

    magic = data[0:4]
    if magic != b'\x01\x00\x01\x00':
        print(f"  [!] Canh bao: Magic number khong dung (co the khong phai file .ipv): {magic.hex()}")

    version = struct.unpack('>I', data[4:8])[0]
    width = struct.unpack('>I', data[16:20])[0]
    height = struct.unpack('>I', data[20:24])[0]

    return width, height, version


def find_all_pngs(data: bytes):
    """Tim tat ca PNG embedded trong binary data. Tra ve danh sach (offset, end, size)."""
    pngs = []
    pos = 0

    while True:
        idx = data.find(b'\x89PNG', pos)
        if idx == -1:
            break

        # Kiem tra day co phai PNG hop le (co IHDR chunk sau magic)
        if idx + 24 > len(data):
            pos = idx + 1
            continue

        ihdr_marker = data[idx + 12:idx + 16]
        if ihdr_marker != b'IHDR':
            pos = idx + 1
            continue

        # Doc kich thuoc tu IHDR
        pw = struct.unpack('>I', data[idx + 16:idx + 20])[0]
        ph = struct.unpack('>I', data[idx + 20:idx + 24])[0]

        # Tim IEND chunk
        iend = data.find(b'IEND', idx)
        if iend == -1:
            pos = idx + 1
            continue

        # PNG ket thuc 4 bytes sau IEND (CRC)
        png_end = iend + 8

        pngs.append({
            'offset': idx,
            'end': png_end,
            'size': png_end - idx,
            'width': pw,
            'height': ph,
        })

        pos = png_end

    return pngs


def find_best_png(pngs, canvas_w, canvas_h):
    """Chon PNG artwork nguyen ban tu danh sach PNG.

    Thuat toan:
    1. Uu tien PNG co kich thuoc khop chinh xac voi canvas
    2. Neu co nhieu, chon PNG cuoi cung (thuong la merged artwork)
    3. Neu khong co, chon PNG co dien tich lon nhat
    """
    canvas_match = [p for p in pngs if p['width'] == canvas_w and p['height'] == canvas_h]

    if canvas_match:
        # Chon PNG cuoi cung (vi merged artwork thuong o cuoi file)
        return canvas_match[-1], 'canvas_match'

    # Fallback: chon PNG lon nhat
    largest = max(pngs, key=lambda p: p['size'])
    return largest, 'largest_fallback'


def extract_ipv(filepath: str, output_dir: str = None):
    """Trich xuat PNG tu file .ipv."""
    filepath = Path(filepath)

    if not filepath.exists():
        print(f"  [!] File khong ton tai: {filepath}")
        return False

    print(f"[*] Dang xu ly: {filepath.name}")

    try:
        with open(filepath, 'rb') as f:
            data = f.read()
    except IOError as e:
        print(f"  [!] Khong the doc file: {e}")
        return False

    if len(data) < 100:
        print(f"  [!] File qua nho ({len(data)} bytes), khong phai file .ipv hop le")
        return False

    # Doc kich thuoc canvas
    try:
        canvas_w, canvas_h, version = read_canvas_size(data)
    except ValueError as e:
        print(f"  [!] Loi doc header: {e}")
        return False

    print(f"    Canvas: {canvas_w} x {canvas_h} | Phien ban ibisPaint: {version}")

    # Tim tat ca PNG
    pngs = find_all_pngs(data)
    if not pngs:
        print(f"  [!] Khong tim thay PNG nao trong file")
        return False

    print(f"    Tim thay {len(pngs)} PNG:")
    for i, p in enumerate(pngs):
        match = " <-- Khop canvas" if p['width'] == canvas_w and p['height'] == canvas_h else ""
        print(f"      PNG #{i+1}: {p['width']}x{p['height']}, {p['size']:,} bytes{match}")

    # Chon PNG tot nhat
    best, method = find_best_png(pngs, canvas_w, canvas_h)

    if method == 'largest_fallback':
        print(f"  [!] Khong tim thay PNG khop canvas {canvas_w}x{canvas_h}")
        print(f"      Dung PNG lon nhat thay the: {best['width']}x{best['height']}")

    # Xuat file
    png_data = data[best['offset']:best['end']]

    if output_dir:
        out_path = Path(output_dir) / (filepath.stem + '.png')
    else:
        out_path = filepath.with_suffix('.png')

    with open(out_path, 'wb') as f:
        f.write(png_data)

    print(f"  [ok] Da luu: {out_path} ({best['size']:,} bytes)")
    return True


def main():
    if len(sys.argv) < 2:
        print("extract_ipv.py - Trich xuat PNG tu file .ipv (ibisPaint X)")
        print()
        print("Cach su dung:")
        print(f"  python3 {sys.argv[0]} file.ipv")
        print(f"  python3 {sys.argv[0]} file1.ipv file2.ipv file3.ipv")
        print(f"  python3 {sys.argv[0]} thu_muc/*.ipv")
        print()
        print("Tuy chon:")
        print(f"  -o, --output DIR    Luu PNG vao thu muc khac")
        sys.exit(0)

    # Parse arguments
    args = sys.argv[1:]
    output_dir = None

    if '-o' in args:
        idx = args.index('-o')
        if idx + 1 < len(args):
            output_dir = args[idx + 1]
            args = args[:idx] + args[idx+2:]
    elif '--output' in args:
        idx = args.index('--output')
        if idx + 1 < len(args):
            output_dir = args[idx + 1]
            args = args[:idx] + args[idx+2:]

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Xu ly tung file
    success = 0
    total = len(args)

    for filepath in args:
        if extract_ipv(filepath, output_dir):
            success += 1
        print()

    print(f"--- Ket qua: {success}/{total} file thanh cong ---")


if __name__ == '__main__':
    main()
