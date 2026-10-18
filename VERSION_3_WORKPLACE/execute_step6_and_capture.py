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
from exam_vision_ocr_engine_v3 import VisionOCREngineV3, ANSWER_SHEETS_DIR

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
    artifact_dir = r'C:\Users\spmad\.gemini\antigravity\brain\eea1be30-f8c7-496e-a4ef-2be06e683be2'
    exam_id = "EXAM-MAT-DAI-20261018-664F52"
    sheet_name = "EXAM-MAT-DAI-20261018-664F52_student_handwritten_sheet.txt"
    sheet_path = os.path.join(ANSWER_SHEETS_DIR, sheet_name)

    print(f"[Step 6] Verifying Face B Vision OCR Ingestion for {exam_id}...")
    assert os.path.exists(sheet_path), f"Answer sheet missing: {sheet_path}"

    # Launch desktop application
    root = tk.Tk()
    root.title('ScholasticPulse V3 - Step 6 Verification (Face B Answer Sheet Vision OCR Ingestion)')
    root.geometry('1360x900')
    app = study_balancer.DesktopApp(root)
    app.notebook.select(2)
    ctrl = app.host_exam_controller

    # Switch to Subview 5: Face B (Answer Evaluator)
    ctrl.switch_subview('face_b')
    face_b = ctrl.face_b_controller
    face_b.suppress_modal = True

    # Configure Face B Ingestion Deck
    face_b.selected_exam_var.set(exam_id)
    face_b.selected_sheet_var.set(sheet_name)
    face_b.lbl_exam_info.configure(text=face_b._get_exam_info_text())

    # Execute Vision OCR & Question Alignment
    print("[Step 6] Executing Vision OCR & Question Alignment...")
    res = face_b.run_ocr_sync(exam_id=exam_id, sheet_path=sheet_path, force_offline=False)
    print(f" -> Aligned: {res['aligned_count']}/{res['total_questions']} Questions")
    print(f" -> Confidence: {res['confidence_percentage']}%")
    print(f" -> Status: {res['alignment_status']}")

    # Let UI settle and render cards
    root.update_idletasks()
    root.update()
    time.sleep(0.5)

    # Capture live application screen directly
    out6 = os.path.join(artifact_dir, 'step6_face_b_ocr_verified.png')
    capture_widget(root, out6)
    print('SUCCESS: Captured Step 6 Screenshot to:', out6)

    root.destroy()

if __name__ == '__main__':
    main()
