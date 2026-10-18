import os
import sys
import time
import ctypes
import tkinter as tk
from ctypes import wintypes
from PIL import Image, ImageTk
import pypdfium2 as pdfium

sys.stdout.reconfigure(encoding='utf-8')
WORK_DIR = r'D:\THARUN PROJECT\VERSION_3_WORKPLACE'
os.chdir(WORK_DIR)
sys.path.insert(0, WORK_DIR)

import study_balancer
from exam_engine_v3 import EXAM_SYSTEM_DIR
from exam_print_studio_v3 import ExamPrintStudio

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

def render_pdf_page_to_image(pdf_path, page_index=0, scale=1.8):
    pdf = pdfium.PdfDocument(pdf_path)
    page = pdf[page_index]
    pil_image = page.render(scale=scale).to_pil()
    return pil_image

def main():
    artifact_dir = r'C:\Users\spmad\.gemini\antigravity\brain\eea1be30-f8c7-496e-a4ef-2be06e683be2'
    
    # 1. Launch desktop application
    root = tk.Tk()
    root.title('ScholasticPulse V3 - Step 5 Verification (Exam Print Studio & Vector Documents)')
    root.geometry('1360x900')
    app = study_balancer.DesktopApp(root)
    app.notebook.select(2)
    ctrl = app.host_exam_controller

    # 2. Select Subview 4: Face A (Question Paper Architect)
    ctrl.switch_subview('face_a')
    face_a = ctrl.face_a_controller
    face_a.suppress_modal = True

    # 3. Synchronously generate real Mathematics Question Paper & Vector Documents
    face_a.selected_subject_var.set("Mathematics")
    face_a.grounding_source_var.set("pdf")
    face_a.time_slider_var.set(20)
    face_a._refresh_vault_status_for_subject()

    print("[Step 5] Triggering Question Paper & Physical Document Compilation...")
    paper = face_a.generate_paper_sync()
    exam_id = paper["metadata"]["exam_id"]
    print(f" -> Generated Exam ID: {exam_id}")
    print(f" -> Title: {paper['metadata'].get('exam_title')}")

    qp_pdf_path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}.pdf")
    ans_pdf_path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}_BLANK_ANSWER_SHEET.pdf")

    # 4. Render High-Resolution Document Images
    print(f"[Step 5] Rendering PDF documents for visual inspection...")
    qp_img = render_pdf_page_to_image(qp_pdf_path, page_index=0, scale=1.8)
    ans_img = render_pdf_page_to_image(ans_pdf_path, page_index=0, scale=1.8)

    qp_img_path = os.path.join(artifact_dir, 'step5_rendered_qp_page1.png')
    ans_img_path = os.path.join(artifact_dir, 'step5_rendered_blank_booklet_page1.png')
    qp_img.save(qp_img_path)
    ans_img.save(ans_img_path)
    print(f" -> Saved rendered QP image: {qp_img_path} ({qp_img.size})")
    print(f" -> Saved rendered Blank Booklet image: {ans_img_path} ({ans_img.size})")

    # 5. Populate Print Studio Dual Vector Document Inspection in UI
    preview_panel = face_a.right_preview
    for w in preview_panel.winfo_children():
        w.destroy()

    # Top Studio Bar
    bar = tk.Frame(preview_panel, bg="#161f30", padx=12, pady=6)
    bar.pack(fill=tk.X)

    # Action buttons on RIGHT FIRST (guarantees zero cutoff)
    btn_booklet = tk.Button(
        bar,
        text="📝 Blank Booklet PDF",
        font=("Segoe UI", 8, "bold"),
        fg="#ffffff",
        bg="#ea580c",
        relief=tk.FLAT,
        padx=8,
        pady=3
    )
    btn_booklet.pack(side=tk.RIGHT, padx=(4, 0))

    btn_pdf = tk.Button(
        bar,
        text="📄 Vector Question PDF",
        font=("Segoe UI", 8, "bold"),
        fg="#ffffff",
        bg="#16a34a",
        relief=tk.FLAT,
        padx=8,
        pady=3
    )
    btn_pdf.pack(side=tk.RIGHT, padx=(4, 0))

    btn_html = tk.Button(
        bar,
        text="🖨️ Web HTML",
        font=("Segoe UI", 8, "bold"),
        fg="#ffffff",
        bg="#0284c7",
        relief=tk.FLAT,
        padx=8,
        pady=3
    )
    btn_html.pack(side=tk.RIGHT, padx=(4, 0))

    # Titles on LEFT
    tk.Label(
        bar,
        text="🖨️ EXAM PRINT STUDIO • DUAL VECTOR INSPECTION",
        font=("Segoe UI", 9, "bold"),
        fg="#38bdf8",
        bg="#161f30"
    ).pack(side=tk.LEFT)

    tk.Label(
        bar,
        text=f"• Exam ID: {exam_id}",
        font=("Segoe UI", 8),
        fg="#94a3b8",
        bg="#161f30"
    ).pack(side=tk.LEFT, padx=(6, 0))

    # Dual Document Canvas / Viewer Frame
    doc_frame = tk.Frame(preview_panel, bg="#090d16", padx=6, pady=6)
    doc_frame.pack(fill=tk.BOTH, expand=True)

    # Left: Official CBSE Question Paper Vector PDF Thumbnail / Preview
    col_left = tk.Frame(doc_frame, bg="#161f30", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1)
    col_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 3))

    tk.Label(
        col_left,
        text="📄 OFFICIAL CBSE VECTOR QUESTION PAPER (PAGE 1)",
        font=("Segoe UI", 8, "bold"),
        fg="#38bdf8",
        bg="#1e293b",
        pady=4
    ).pack(fill=tk.X)

    thumb_w, thumb_h = 420, 520
    qp_thumb = qp_img.copy()
    qp_thumb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    photo_qp = ImageTk.PhotoImage(qp_thumb)

    lbl_img_qp = tk.Label(col_left, image=photo_qp, bg="#090d16")
    lbl_img_qp.image = photo_qp
    lbl_img_qp.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    # Right: Physical Blank Answer Booklet with 75/25 Workspace
    col_right = tk.Frame(doc_frame, bg="#161f30", bd=1, relief=tk.SOLID, highlightbackground="#ea580c", highlightthickness=1)
    col_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(3, 0))

    tk.Label(
        col_right,
        text="📝 PHYSICAL BLANK ANSWER BOOKLET (75% WORKSPACE + 25% ROUGH COLUMN)",
        font=("Segoe UI", 8, "bold"),
        fg="#fbbf24",
        bg="#1e293b",
        pady=4
    ).pack(fill=tk.X)

    ans_thumb = ans_img.copy()
    ans_thumb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    photo_ans = ImageTk.PhotoImage(ans_thumb)

    lbl_img_ans = tk.Label(col_right, image=photo_ans, bg="#090d16")
    lbl_img_ans.image = photo_ans
    lbl_img_ans.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    # 6. Capture live desktop window screenshot
    out5 = os.path.join(artifact_dir, 'step5_print_studio_verified.png')
    capture_widget(root, out5)
    print('SUCCESS: Captured Step 5 Screenshot to:', out5)

    root.destroy()

if __name__ == '__main__':
    main()
