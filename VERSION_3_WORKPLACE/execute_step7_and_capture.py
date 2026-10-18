import os
import sys
import time
import ctypes
import tkinter as tk
from ctypes import wintypes
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
WORK_DIR = r'D:\THARUN PROJECT\VERSION_3_WORKPLACE'
os.chdir(WORK_DIR)
sys.path.insert(0, WORK_DIR)

import study_balancer

def capture_widget(widget, out_path):
    for _ in range(12):
        widget.update_idletasks()
        widget.update()
        time.sleep(0.04)
    hwnd = widget.winfo_id()
    w = widget.winfo_width()
    h = widget.winfo_height()
    hwndDC = ctypes.windll.user32.GetWindowDC(hwnd)
    mfcDC = ctypes.windll.gdi32.CreateCompatibleDC(hwndDC)
    saveBitMap = ctypes.windll.gdi32.CreateCompatibleBitmap(hwndDC, w, h)
    ctypes.windll.gdi32.SelectObject(mfcDC, saveBitMap)
    ctypes.windll.user32.PrintWindow(hwnd, mfcDC, 2)

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ('biSize', wintypes.DWORD),
            ('biWidth', wintypes.LONG),
            ('biHeight', wintypes.LONG),
            ('biPlanes', wintypes.WORD),
            ('biBitCount', wintypes.WORD),
            ('biCompression', wintypes.DWORD),
            ('biSizeImage', wintypes.DWORD),
            ('biXPelsPerMeter', wintypes.LONG),
            ('biYPelsPerMeter', wintypes.LONG),
            ('biClrUsed', wintypes.DWORD),
            ('biClrImportant', wintypes.DWORD),
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
    img = Image.frombuffer('RGBA', (w, h), buf, 'raw', 'BGRA', 0, 1).convert('RGB')
    img.save(out_path)
    ctypes.windll.gdi32.DeleteObject(saveBitMap)
    ctypes.windll.gdi32.DeleteDC(mfcDC)
    ctypes.windll.user32.ReleaseDC(hwnd, hwndDC)

def main():
    root = tk.Tk()
    root.title('ScholasticPulse V3 - Step 7 Evaluator & Topper Guide')
    root.geometry('1300x860')
    app = study_balancer.DesktopApp(root)

    artifact_dir = r'C:\Users\spmad\.gemini\antigravity\brain\eea1be30-f8c7-496e-a4ef-2be06e683be2'

    # Select Tab 2: Host Exam & AI
    app.notebook.select(2)
    root.update_idletasks()
    root.update()

    ctrl = app.host_exam_controller
    ctrl.switch_subview('topper')
    root.update_idletasks()
    root.update()

    # 1. Capture Graded Script View
    out_eval = os.path.join(artifact_dir, 'step7_cbse_evaluator_verified.png')
    capture_widget(root, out_eval)
    print('Captured Step 7 Evaluator Graded View:', out_eval)

    # 2. Switch to Topper Model Guide View
    if hasattr(ctrl, "topper_controller") and ctrl.topper_controller:
        ctrl.topper_controller._switch_tab("topper")
        root.update_idletasks()
        root.update()

    out_topper = os.path.join(artifact_dir, 'step7_topper_model_guide_verified.png')
    capture_widget(root, out_topper)
    print('Captured Step 7 Topper Model Guide View:', out_topper)

    root.destroy()

if __name__ == '__main__':
    main()
