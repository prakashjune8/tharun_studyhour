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
    for _ in range(15):
        widget.update_idletasks()
        widget.update()
        time.sleep(0.05)
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
    root.title('ScholasticPulse V3 - Step 4 Verification (Face A Question Architect)')
    root.geometry('1360x900')
    app = study_balancer.DesktopApp(root)
    app.notebook.select(2)
    ctrl = app.host_exam_controller

    # Select Subview 4: Face A (Question Paper Architect)
    ctrl.switch_subview('face_a')
    face_a = ctrl.face_a_controller
    face_a.suppress_modal = True

    # Configure Generation: Mathematics, Grounded in Uploaded School PDF from Step 2, styled by Step 3
    face_a.selected_subject_var.set("Mathematics")
    face_a.grounding_source_var.set("pdf")
    face_a.time_slider_var.set(20) # 20 mins standard daily sprint
    face_a._refresh_vault_status_for_subject()

    print("[Step 4] Triggering Question Paper Generation...")
    paper = face_a.generate_paper_sync()
    meta = paper.get("metadata", {})
    print(f" -> Generated Exam Title: {meta.get('exam_title')}")
    print(f" -> Mode: {meta.get('generation_mode')}")
    print(f" -> Subject: {meta.get('subject')}")
    print(f" -> Time Allowed: {meta.get('time_allowed_mins')} Mins")
    print(f" -> Max Marks: {meta.get('max_marks')} Marks")
    print(f" -> Total Sections: {len(paper.get('sections', []))}")

    # Give UI a moment to update layout and render
    root.update_idletasks()
    root.update()

    artifact_dir = r'C:\Users\spmad\.gemini\antigravity\brain\eea1be30-f8c7-496e-a4ef-2be06e683be2'
    out4 = os.path.join(artifact_dir, 'step4_face_a_verified.png')

    capture_widget(root, out4)
    print('SUCCESS: Captured Step 4 Screenshot to:', out4)

    root.destroy()

if __name__ == '__main__':
    main()
