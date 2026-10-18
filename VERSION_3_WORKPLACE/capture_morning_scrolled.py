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
    root.title('ScholasticPulse V3')
    root.geometry('1300x860')
    app = study_balancer.DesktopApp(root)

    artifact_dir = r'C:\Users\spmad\.gemini\antigravity\brain\eea1be30-f8c7-496e-a4ef-2be06e683be2'

    # Select Tab 0: Daily Schedule
    app.notebook.select(0)
    app.active_diary_date = "2026-10-16"
    app.apply_diary_to_timetable(silent=True)
    root.update_idletasks()
    root.update()

    # Scroll down to morning slots
    if hasattr(app, "sched_canvas"):
        app.sched_canvas.yview_moveto(0.7)
        root.update_idletasks()
        root.update()

    out_sched = os.path.join(artifact_dir, 'daily_schedule_morning_645_exam_verified.png')
    capture_widget(root, out_sched)
    print('Captured Morning Schedule Scrolled View:', out_sched)

    root.destroy()

if __name__ == '__main__':
    main()
