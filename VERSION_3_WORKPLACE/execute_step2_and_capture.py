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

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import study_balancer
from exam_smart_ingestion_wizard_v3 import SmartIngestionWizard

def create_sample_pdf(pdf_path):
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, 720, "NCERT Mathematics Class 8 - Chapter 9")
    c.setFont("Helvetica", 11)
    c.drawString(72, 695, "Topic: Algebraic Expressions and Identities - Exercise 9.1")
    c.drawString(72, 670, "1. Identify the terms and their coefficients for each expression:")
    c.drawString(90, 650, "(i) 5xyz^2 - 3zy")
    c.drawString(90, 630, "(ii) 1 + x + x^2")
    c.drawString(72, 600, "2. Classify polynomials into monomials, binomials, trinomials:")
    c.drawString(90, 580, "(i) x + y  (ii) 1000  (iii) 2y - 3y^2")
    c.drawString(72, 550, "3. Add the following expressions:")
    c.drawString(90, 530, "ab - bc, bc - ca, ca - ab")
    c.save()
    print("Created sample PDF at:", pdf_path)

def capture_widget(widget, out_path):
    for _ in range(12):
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
    sample_pdf = os.path.join(WORK_DIR, 'EXAM_SYSTEM_V3', 'sample_math_ex9_1_scan.pdf')
    create_sample_pdf(sample_pdf)

    # Ingest file via SmartIngestionWizard
    res = SmartIngestionWizard.ingest_file_to_vault(
        source_file_path=sample_pdf,
        subject="Mathematics",
        material_type="topic_photocopy",
        chapter_name="Ch 09 Algebraic Expressions",
        exercise_or_topic="Ex 9.1 Concept Sprint",
        book_title="NCERT Class 8",
        notes="Textbook photocopy page 138 Ex 9.1 Q1-Q3"
    )
    print("Ingestion Result:", res)

    root = tk.Tk()
    root.title('ScholasticPulse V3 - Step 2 Verification')
    root.geometry('1280x850')
    app = study_balancer.DesktopApp(root)
    app.notebook.select(2)
    ctrl = app.host_exam_controller

    # Select Subview 2: Textbook Vault
    ctrl.switch_subview('vault')

    artifact_dir = r'C:\Users\spmad\.gemini\antigravity\brain\eea1be30-f8c7-496e-a4ef-2be06e683be2'
    out2 = os.path.join(artifact_dir, 'step2_textbook_vault_verified.png')

    capture_widget(root, out2)
    print('SUCCESS: Captured Step 2 Screenshot to:', out2)

    root.destroy()

if __name__ == '__main__':
    main()
