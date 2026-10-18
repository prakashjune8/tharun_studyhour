import os
import sys
import time
import ctypes
from ctypes import wintypes
import tkinter as tk
from PIL import Image

# Ensure utf-8
sys.stdout.reconfigure(encoding='utf-8')

WORK_DIR = r"D:\THARUN PROJECT\VERSION_3_WORKPLACE"
os.chdir(WORK_DIR)
sys.path.insert(0, WORK_DIR)

import study_balancer

def capture_tk_window(widget, out_path, crop_box=None):
    for _ in range(6):
        widget.update_idletasks()
        widget.update()
        time.sleep(0.05)
    hwnd = ctypes.windll.user32.GetParent(widget.winfo_id()) or widget.winfo_id()
    w = widget.winfo_width()
    h = widget.winfo_height()
    hwndDC = ctypes.windll.user32.GetWindowDC(hwnd)
    mfcDC = ctypes.windll.gdi32.CreateCompatibleDC(hwndDC)
    saveBitMap = ctypes.windll.gdi32.CreateCompatibleBitmap(hwndDC, w, h)
    ctypes.windll.gdi32.SelectObject(mfcDC, saveBitMap)
    ctypes.windll.user32.PrintWindow(hwnd, mfcDC, 2)

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ("biSize", wintypes.DWORD),
            ("biWidth", wintypes.LONG),
            ("biHeight", wintypes.LONG),
            ("biPlanes", wintypes.WORD),
            ("biBitCount", wintypes.WORD),
            ("biCompression", wintypes.DWORD),
            ("biSizeImage", wintypes.DWORD),
            ("biXPelsPerMeter", wintypes.LONG),
            ("biYPelsPerMeter", wintypes.LONG),
            ("biClrUsed", wintypes.DWORD),
            ("biClrImportant", wintypes.DWORD),
        ]

    bi = BITMAPINFOHEADER()
    bi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bi.biWidth = w
    bi.biHeight = -h
    bi.biPlanes = 1
    bi.biBitCount = 32
    bi.biCompression = 0
    buf = ctypes.create_string_buffer(w * h * 4)
    ctypes.windll.gdi32.GetDIBits(mfcDC, saveBitMap, 0, h, buf, ctypes.byref(bi), 0)
    img = Image.frombuffer("RGBA", (w, h), buf, "raw", "BGRA", 0, 1).convert("RGB")
    if crop_box:
        img = img.crop(crop_box)
    img.save(out_path)
    ctypes.windll.gdi32.DeleteObject(saveBitMap)
    ctypes.windll.gdi32.DeleteDC(mfcDC)
    ctypes.windll.user32.ReleaseDC(hwnd, hwndDC)
    return img.size

def capture_subviews():
    artifacts_dir = r"C:\Users\spmad\.gemini\antigravity\brain\eea1be30-f8c7-496e-a4ef-2be06e683be2"
    os.makedirs(artifacts_dir, exist_ok=True)

    print("Launching DesktopApp in VERSION_3_WORKPLACE...")
    root = tk.Tk()
    root.geometry("1440x920+50+50")
    
    app = study_balancer.DesktopApp(root)
    root.update_idletasks()
    root.update()

    # Switch to Exam tab
    print("Switching to tab_exam...")
    if hasattr(app, "custom_tab_bar"):
        app.custom_tab_bar.select_tab("tab_exam")
    app.notebook.select(app.tab_exam)
    root.update_idletasks()
    root.update()
    time.sleep(0.5)

    exam_ui = app.host_exam_controller
    subviews = [
        ("ledger", "v3_desktop_subview1_ledger.png"),
        ("face_a", "v3_desktop_subview2_face_a.png"),
        ("face_b", "v3_desktop_subview3_face_b.png"),
        ("topper", "v3_desktop_subview4_topper.png")
    ]

    for sv_id, fname in subviews:
        print(f"Selecting subview: {sv_id} -> {fname}")
        exam_ui.switch_subview(sv_id)
        for _ in range(8):
            root.update_idletasks()
            root.update()
            time.sleep(0.04)

        save_path = os.path.join(artifacts_dir, fname)
        sz = capture_tk_window(root, save_path, crop_box=(0, 0, 1440, 856))
        print(f"Captured: {save_path} ({sz[0]}x{sz[1]})")

    root.destroy()
    print("All 4 desktop subviews captured successfully.")

if __name__ == "__main__":
    capture_subviews()
