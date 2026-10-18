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
from exam_sample_questions_engine_v3 import SampleQuestionsEngine

def create_sample_model_paper_pdf(pdf_path):
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(306, 740, "SENTHIL PUBLIC SCHOOL - DHARMAPURI")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(306, 720, "CLASS 8 - MATHEMATICS - TERM 1 MODEL EXAMINATION")
    c.setFont("Helvetica", 10)
    c.drawString(72, 695, "Time: 3 Hours")
    c.drawRightString(540, 695, "Maximum Marks: 80")
    
    c.line(72, 685, 540, 685)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(72, 665, "SECTION A (Multiple Choice Questions - 1 Mark each)")
    
    c.setFont("Helvetica", 10)
    c.drawString(72, 645, "1. What is the coefficient of x in the algebraic term -7xy^2?")
    c.drawString(90, 628, "(A) -7     (B) y^2     (C) -7y^2     (D) 7")
    
    c.drawString(72, 605, "2. Which of the following is a binomial expression?")
    c.drawString(90, 588, "(A) 4x^2   (B) 2x + 3y   (C) 3x + y + z   (D) 100")
    
    c.drawString(72, 565, "3. The product of (x + 4) and (x - 4) using standard identities is:")
    c.drawString(90, 548, "(A) x^2 - 16   (B) x^2 + 16   (C) x^2 - 8x + 16   (D) 2x - 8")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(72, 515, "SECTION B (Short Answer Type I - 2 Marks each)")
    c.setFont("Helvetica", 10)
    c.drawString(72, 495, "4. Subtract 3xy + 5yz - 7zx from 5xy - 2yz - 2zx + 10xyz.")
    c.drawString(72, 470, "5. Using suitable identity, evaluate (102)^2.")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(72, 435, "SECTION C (Short Answer Type II - 3 Marks each)")
    c.setFont("Helvetica", 10)
    c.drawString(72, 415, "6. Simplify: (a + b)(2a - 3b + c) - (2a - 3b)c.")
    c.drawString(72, 390, "7. Verify the identity (x + a)(x + b) = x^2 + (a + b)x + ab for x=3, a=2, b=5.")
    
    c.save()
    print("Created sample school model question paper PDF at:", pdf_path)

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
    sample_pdf = os.path.join(WORK_DIR, 'EXAM_SYSTEM_V3', 'sps_math_term1_model_paper.pdf')
    create_sample_model_paper_pdf(sample_pdf)

    # Ingest file via SampleQuestionsEngine
    res = SampleQuestionsEngine.ingest_sample_paper(
        source_file_path=sample_pdf,
        subject="Mathematics",
        exam_category="term_1_model",
        paper_title="Senthil SPS Term1 Model 2025",
        total_marks=80,
        time_mins=180,
        school_name="Senthil Public School",
        notes="Official SPS Term 1 Sample Model Question Paper for Class 8 Math"
    )
    print("Sample Paper Ingestion Result:", res)

    root = tk.Tk()
    root.title('ScholasticPulse V3 - Step 3 Verification')
    root.geometry('1360x920')
    app = study_balancer.DesktopApp(root)
    app.notebook.select(2)
    ctrl = app.host_exam_controller

    # Select Subview 3: School Sample Questions & Model Papers Vault
    ctrl.switch_subview('sample_q')

    artifact_dir = r'C:\Users\spmad\.gemini\antigravity\brain\eea1be30-f8c7-496e-a4ef-2be06e683be2'
    out3 = os.path.join(artifact_dir, 'step3_sample_questions_vault_verified.png')

    capture_widget(root, out3)
    print('SUCCESS: Captured Step 3 Screenshot to:', out3)

    root.destroy()

if __name__ == '__main__':
    main()
