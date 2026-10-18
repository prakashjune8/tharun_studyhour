"""
HOST EXAM FACE B UI CONTROLLER (SESSION 5 / 6)
----------------------------------------------
Clean, modern, responsive Desktop UI Controller for:
Face B: Answer Sheet Vision OCR Ingestion & Schema Alignment Studio.

Features:
1. Ingests student handwritten answer sheets (scans, PDFs, photo transcripts).
2. Runs Multimodal Gemini Vision OCR with seamless deterministic fallback.
3. Automatically aligns extracted responses question-by-question against active Question Paper.
4. Shinobi-themed split view with 6px CustomDarkScrollbar and strict geometry lock.
"""

import os
import sys
import json
import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Dict, Any, List, Optional

if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from exam_vision_ocr_engine_v3 import VisionOCREngineV3, QUESTION_PAPERS_DIR, ANSWER_SHEETS_DIR

_MAIN_THREAD_ID = threading.get_ident()
_UI_CALLBACK_QUEUE = queue.Queue()


def _enable_thread_safe_after(root):
    """Ensures root.after can be called safely from background threads in Python 3.12+ / 3.14+."""
    if getattr(root, "_thread_safe_after_enabled", False):
        return
    root._thread_safe_after_enabled = True
    orig_after = root.after

    def safe_after(ms, func=None, *args):
        if threading.get_ident() == _MAIN_THREAD_ID:
            return orig_after(ms, func, *args)
        else:
            if func is not None:
                _UI_CALLBACK_QUEUE.put(lambda: func(*args))
            return None

    root.after = safe_after

    def _drain_queue():
        try:
            while True:
                cb = _UI_CALLBACK_QUEUE.get_nowait()
                try:
                    cb()
                except Exception as ex:
                    print(f"[UI Queue Dispatcher] Callback notice: {ex}")
        except queue.Empty:
            pass
        try:
            orig_after(30, _drain_queue)
        except Exception:
            pass

    try:
        orig_after(30, _drain_queue)
    except Exception:
        pass


class CustomDarkScrollbar(tk.Canvas):
    """Ultra-slim 6px Custom Dark Canvas Scrollbar for consistent styling."""
    def __init__(self, parent, target_widget=None, width=6, bg="#0b1120", thumb_color="#334155", **kwargs):
        super().__init__(parent, width=width, bg=bg, highlightthickness=0, bd=0, cursor="hand2", **kwargs)
        self.target = target_widget
        self.width = width
        self._thumb_color = thumb_color
        self.thumb = self.create_rectangle(0, 0, width, 36, fill=thumb_color, outline="")

        if target_widget is not None:
            self.attach_target(target_widget)

        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<Enter>", lambda e: self.itemconfig(self.thumb, fill="#f59e0b"))
        self.bind("<Leave>", lambda e: self.itemconfig(self.thumb, fill=self._thumb_color))

    def attach_target(self, target_widget):
        self.target = target_widget
        try:
            target_widget.configure(yscrollcommand=self.update_thumb)
        except Exception:
            pass

    def update_thumb(self, first, last):
        try:
            top = float(first)
            bottom = float(last)
            sh = self.winfo_height()
            if sh <= 1:
                return
            ty1 = int(top * sh)
            ty2 = max(ty1 + 24, int(bottom * sh))
            self.coords(self.thumb, 0, ty1, self.width, ty2)
        except Exception:
            pass

    def _on_click(self, event):
        sh = self.winfo_height()
        if sh > 0 and self.target:
            fraction = event.y / sh
            self.target.yview_moveto(max(0.0, fraction - 0.1))

    def _on_drag(self, event):
        sh = self.winfo_height()
        if sh > 0 and self.target:
            fraction = event.y / sh
            self.target.yview_moveto(max(0.0, min(1.0, fraction)))


class HostExamFaceBView:
    """
    Face B UI View: Answer Sheet Vision OCR Ingestion & Schema Alignment.
    """

    def __init__(self, parent_frame: tk.Frame, controller):
        self.parent = parent_frame
        self.controller = controller
        self.colors = getattr(controller, "colors", {
            "bg": "#0a0e17",
            "card_bg": "#0e172a",
            "card_border": "#334155",
            "primary": "#f59e0b",
            "accent": "#38bdf8",
            "text": "#f8fafc",
            "subtext": "#94a3b8"
        })

        self.available_exams = VisionOCREngineV3.list_available_exams()
        active_id = getattr(controller, "active_exam_id", None)
        if active_id and active_id in self.available_exams:
            default_exam = active_id
        else:
            default_exam = self.available_exams[0] if self.available_exams else ""
        self.selected_exam_var = tk.StringVar(value=default_exam)
        self.available_sheets = VisionOCREngineV3.list_uploaded_sheets()
        self.selected_sheet_var = tk.StringVar(value=self.available_sheets[0]["filename"] if self.available_sheets else "")
        self.ocr_mode_var = tk.StringVar(value="gemini_vision")
        self.active_extraction: Optional[Dict[str, Any]] = None
        self.suppress_modal = False
        self.root = self.parent.winfo_toplevel()
        _enable_thread_safe_after(self.root)

        class ExamEngineAdapter:
            @staticmethod
            def evaluate_answer_sheet(exam_id: str, *args, **kwargs):
                from exam_evaluator_v3 import CBSEEvaluatorV3
                return CBSEEvaluatorV3.evaluate_exam(exam_id)

        self.exam_engine = ExamEngineAdapter()

    def switch_subview(self, target_alias: str, **kwargs):
        if hasattr(self.controller, "switch_subview"):
            return self.controller.switch_subview(target_alias, **kwargs)

    def build_ui(self):
        """Constructs the responsive two-column Face B workspace."""
        for w in self.parent.winfo_children():
            w.destroy()

        container = tk.Frame(self.parent, bg=self.colors.get("bg", "#0a0e17"))
        container.pack(fill=tk.BOTH, expand=True)

        # -------------------------------------------------------------
        # LEFT COLUMN: INGESTION DECK (WIDTH = 380PX FIXED)
        # -------------------------------------------------------------
        left_col = tk.Frame(
            container,
            bg=self.colors.get("card_bg", "#0e172a"),
            width=380,
            bd=1,
            relief=tk.SOLID,
            highlightbackground=self.colors.get("card_border", "#334155"),
            highlightthickness=1
        )
        left_col.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6), pady=0)
        left_col.pack_propagate(False)

        # Left Column Title
        head_frame = tk.Frame(left_col, bg="#131c2e", padx=12, pady=8)
        head_frame.pack(fill=tk.X)
        tk.Label(
            head_frame,
            text="🔍 ANSWER SHEET INGESTION DECK",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors.get("primary", "#f59e0b"),
            bg="#131c2e"
        ).pack(anchor="w")
        tk.Label(
            head_frame,
            text="Step 6: Multimodal Vision OCR & Schema Alignment",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#131c2e"
        ).pack(anchor="w", pady=(1, 0))

        content_left = tk.Frame(left_col, bg=self.colors.get("card_bg", "#0e172a"), padx=10, pady=6)
        content_left.pack(fill=tk.BOTH, expand=True)

        # 1. Target Exam Selection
        tk.Label(
            content_left,
            text="1. SELECT TARGET QUESTION PAPER:",
            font=("Segoe UI", 8, "bold"),
            fg="#e2e8f0",
            bg=self.colors.get("card_bg", "#0e172a")
        ).pack(anchor="w", pady=(0, 2))

        self.exam_menu = ttk.Combobox(
            content_left,
            textvariable=self.selected_exam_var,
            values=self.available_exams,
            state="readonly",
            font=("Segoe UI", 8)
        )
        self.exam_menu.pack(fill=tk.X, pady=(0, 3))
        self.exam_menu.bind("<<ComboboxSelected>>", lambda e: self._on_exam_selected())

        # Metadata card for selected exam
        self.meta_card = tk.Frame(content_left, bg="#161f30", padx=8, pady=4, bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1)
        self.meta_card.pack(fill=tk.X, pady=(0, 6))
        self.lbl_exam_info = tk.Label(
            self.meta_card,
            text=self._get_exam_info_text(),
            font=("Segoe UI", 8),
            fg="#38bdf8",
            bg="#161f30",
            justify=tk.LEFT,
            wraplength=340
        )
        self.lbl_exam_info.pack(anchor="w")

        # 2. Uploaded Answer Sheet Selection
        tk.Label(
            content_left,
            text="2. SELECT STUDENT ANSWER SHEET:",
            font=("Segoe UI", 8, "bold"),
            fg="#e2e8f0",
            bg=self.colors.get("card_bg", "#0e172a")
        ).pack(anchor="w", pady=(0, 2))

        sheet_names = [s["filename"] for s in self.available_sheets]
        self.sheet_menu = ttk.Combobox(
            content_left,
            textvariable=self.selected_sheet_var,
            values=sheet_names,
            state="readonly",
            font=("Segoe UI", 8)
        )
        self.sheet_menu.pack(fill=tk.X, pady=(0, 3))

        btn_row = tk.Frame(content_left, bg=self.colors.get("card_bg", "#0e172a"))
        btn_row.pack(fill=tk.X, pady=(0, 6))

        tk.Button(
            btn_row,
            text="📁 Browse Disk...",
            font=("Segoe UI", 8, "bold"),
            fg="#38bdf8",
            bg="#1e293b",
            relief=tk.FLAT,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self._on_browse_file
        ).pack(side=tk.LEFT)

        tk.Button(
            btn_row,
            text="🔄 Refresh",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#1e293b",
            relief=tk.FLAT,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self._refresh_sheets_list
        ).pack(side=tk.RIGHT)

        # 3. Vision OCR Engine Mode
        tk.Label(
            content_left,
            text="3. VISION OCR ENGINE MODE:",
            font=("Segoe UI", 8, "bold"),
            fg="#e2e8f0",
            bg=self.colors.get("card_bg", "#0e172a")
        ).pack(anchor="w", pady=(0, 2))

        modes_frame = tk.Frame(content_left, bg="#161f30", padx=8, pady=4, bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1)
        modes_frame.pack(fill=tk.X, pady=(0, 6))

        tk.Radiobutton(
            modes_frame,
            text="🤖 Multimodal Gemini Vision OCR",
            variable=self.ocr_mode_var,
            value="gemini_vision",
            font=("Segoe UI", 8, "bold"),
            fg="#38bdf8",
            bg="#161f30",
            selectcolor="#0f172a",
            activebackground="#161f30"
        ).pack(anchor="w")

        tk.Radiobutton(
            modes_frame,
            text="⚡ Local High-Accuracy Parser (Zero-Lag)",
            variable=self.ocr_mode_var,
            value="local_deterministic",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#161f30",
            selectcolor="#0f172a",
            activebackground="#161f30"
        ).pack(anchor="w", pady=(1, 0))

        # 4. Primary Ingestion Action Button
        self.btn_ingest = tk.Button(
            content_left,
            text="⚡ INGEST & EXTRACT WITH VISION OCR",
            font=("Segoe UI", 9, "bold"),
            fg="#ffffff",
            bg="#ea580c",
            activebackground="#c2410c",
            relief=tk.FLAT,
            pady=6,
            cursor="hand2",
            command=self._on_run_ocr_clicked
        )
        self.btn_ingest.pack(fill=tk.X, pady=(0, 6))

        # 5. Extraction KPI Status Card
        self.kpi_card = tk.Frame(content_left, bg="#161f30", padx=8, pady=6, bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1)
        self.kpi_card.pack(fill=tk.X)

        self.lbl_kpi_status = tk.Label(
            self.kpi_card,
            text="STATUS: Awaiting Answer Sheet Ingestion",
            font=("Segoe UI", 8, "bold"),
            fg="#fbbf24",
            bg="#161f30"
        )
        self.lbl_kpi_status.pack(anchor="w")

        self.lbl_kpi_details = tk.Label(
            self.kpi_card,
            text="• Select Tharun's completed sheet\n• Click 'INGEST & EXTRACT' above\n• Auto-aligns questions to schema",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#161f30",
            justify=tk.LEFT
        )
        self.lbl_kpi_details.pack(anchor="w", pady=(4, 0))

        # -------------------------------------------------------------
        # RIGHT COLUMN: LIVE OCR EXTRACTION & ALIGNMENT STUDIO
        # -------------------------------------------------------------
        right_col = tk.Frame(container, bg=self.colors.get("card_bg", "#0e172a"))
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Top Studio Header Bar
        studio_bar = tk.Frame(right_col, bg="#161f30", padx=12, pady=6)
        studio_bar.pack(fill=tk.X)

        self.btn_run_eval = tk.Button(
            studio_bar,
            text="✅ RUN GEMINI CBSE EVALUATION",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#0284c7",
            activebackground="#0369a1",
            relief=tk.FLAT,
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.trigger_face_b_eval
        )
        self.btn_run_eval.pack(side=tk.RIGHT)

        tk.Label(
            studio_bar,
            text="🔍 VISION OCR EXTRACTION STUDIO • AUTO-ALIGNED QUESTIONS",
            font=("Segoe UI", 9, "bold"),
            fg="#38bdf8",
            bg="#161f30"
        ).pack(side=tk.LEFT)

        self.lbl_studio_badge = tk.Label(
            studio_bar,
            text="• Awaiting Ingestion",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#161f30"
        )
        self.lbl_studio_badge.pack(side=tk.LEFT, padx=(8, 0))

        # Scrollable Cards Canvas for Question Alignments
        canvas_frame = tk.Frame(right_col, bg="#090d16")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.canvas = tk.Canvas(canvas_frame, bg="#090d16", highlightthickness=0, bd=0)
        self.scrollbar = CustomDarkScrollbar(canvas_frame, target_widget=self.canvas, width=6, bg="#0b1120", thumb_color="#334155")
        self.cards_inner = tk.Frame(self.canvas, bg="#090d16")

        self.canvas.create_window((0, 0), window=self.cards_inner, anchor="nw")
        self.cards_inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initial placeholder display
        self._render_placeholder_studio()

        # If an extracted responses file already exists for the active exam, load it immediately
        self._check_and_load_existing_extraction()

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=event.width)

    def _get_exam_info_text(self) -> str:
        import html
        exam_id = self.selected_exam_var.get()
        if not exam_id:
            return "No exam generated yet."
        qp = VisionOCREngineV3.load_question_paper_schema(exam_id)
        if not qp:
            return f"Exam ID: {exam_id}\n(Schema file not found)"
        meta = qp.get("metadata", {})
        subj = html.unescape(meta.get("subject", "Mathematics"))
        marks = meta.get("max_marks", 15)
        mins = meta.get("time_allowed_mins", 20)
        total_q = sum(len(s.get("questions", [])) for s in qp.get("sections", []))
        return f"Exam: {exam_id}\nSubject: {subj}\nMarks: {marks}M | Time: {mins}m | Questions: {total_q}"

    def _on_exam_selected(self):
        self.lbl_exam_info.configure(text=self._get_exam_info_text())
        self._check_and_load_existing_extraction()

    def _on_browse_file(self):
        fp = filedialog.askopenfilename(
            title="Select Tharun's Handwritten Answer Sheet",
            initialdir=ANSWER_SHEETS_DIR,
            filetypes=[
                ("Answer Sheets (*.png;*.jpg;*.pdf;*.txt)", "*.png;*.jpg;*.jpeg;*.pdf;*.txt"),
                ("All Files (*.*)", "*.*")
            ]
        )
        if fp:
            base = os.path.basename(fp)
            # Copy into 04_UPLOADED_ANSWER_SHEETS if not already there
            dest = os.path.join(ANSWER_SHEETS_DIR, base)
            if os.path.abspath(fp) != os.path.abspath(dest):
                import shutil
                shutil.copy2(fp, dest)
            self._refresh_sheets_list()
            self.selected_sheet_var.set(base)

    def _refresh_sheets_list(self):
        self.available_sheets = VisionOCREngineV3.list_uploaded_sheets()
        names = [s["filename"] for s in self.available_sheets]
        self.sheet_menu.configure(values=names)
        if names and not self.selected_sheet_var.get():
            self.selected_sheet_var.set(names[0])

    def _render_placeholder_studio(self):
        for w in self.cards_inner.winfo_children():
            w.destroy()

        card = tk.Frame(self.cards_inner, bg="#0e172a", padx=20, pady=24, bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=30)

        tk.Label(
            card,
            text="📄 Vision OCR Extraction Pipeline Ready",
            font=("Segoe UI", 12, "bold"),
            fg="#f8fafc",
            bg="#0e172a"
        ).pack(pady=(10, 6))

        tk.Label(
            card,
            text="1. Select Tharun's uploaded handwritten answer sheet on the left deck.\n"
                 "2. Click '⚡ INGEST & EXTRACT WITH VISION OCR' to transcribe student steps.\n"
                 "3. Extracted answers are automatically aligned against the Question Paper schema.",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#0e172a",
            justify=tk.CENTER
        ).pack(pady=(0, 16))

    def _check_and_load_existing_extraction(self):
        exam_id = self.selected_exam_var.get()
        if not exam_id:
            return
        out_json = os.path.join(ANSWER_SHEETS_DIR, f"{exam_id}_extracted_responses.json")
        if os.path.exists(out_json):
            try:
                with open(out_json, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.active_extraction = data
                self._render_extraction_cards(data)
            except Exception:
                pass

    def _on_run_ocr_clicked(self):
        exam_id = self.selected_exam_var.get()
        sheet_file = self.selected_sheet_var.get()
        if not exam_id:
            if not self.suppress_modal:
                messagebox.showerror("Error", "Please select a target question paper first.")
            return
        if not sheet_file:
            if not self.suppress_modal:
                messagebox.showerror("Error", "Please select a student answer sheet file to ingest.")
            return

        sheet_path = os.path.join(ANSWER_SHEETS_DIR, sheet_file)
        if not os.path.exists(sheet_path):
            if not self.suppress_modal:
                messagebox.showerror("File Missing", f"Answer sheet not found at: {sheet_path}")
            return

        self.btn_ingest.configure(state=tk.DISABLED, text="⏳ RUNNING VISION OCR...")
        self.lbl_kpi_status.configure(text="STATUS: Transcribing & Aligning...", fg="#38bdf8")

        def worker():
            try:
                force_off = (self.ocr_mode_var.get() == "local_deterministic")
                res = VisionOCREngineV3.extract_and_align_responses(
                    exam_id=exam_id,
                    answer_file_path=sheet_path,
                    force_offline=force_off
                )
                self.parent.after(0, lambda: self._on_extraction_success(res))
            except Exception as e:
                self.parent.after(0, lambda: self._on_extraction_error(str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def run_ocr_sync(self, exam_id: str, sheet_path: str, force_offline: bool = False) -> Dict[str, Any]:
        """Synchronously executes OCR extraction (for testing & verification)."""
        res = VisionOCREngineV3.extract_and_align_responses(
            exam_id=exam_id,
            answer_file_path=sheet_path,
            force_offline=force_offline
        )
        self.active_extraction = res
        self._on_extraction_success(res)
        return res

    def _on_extraction_success(self, res: Dict[str, Any]):
        self.active_extraction = res
        self.btn_ingest.configure(state=tk.NORMAL, text="⚡ INGEST & EXTRACT WITH VISION OCR")
        
        # Update KPI Card
        conf = res.get("confidence_percentage", 100.0)
        matched = res.get("aligned_count", 0)
        tot = res.get("total_questions", 0)
        self.lbl_kpi_status.configure(text=f"STATUS: Ingestion Complete ({matched}/{tot} Aligned)", fg="#34d399")
        self.lbl_kpi_details.configure(
            text=f"• Total Questions: {tot}\n"
                 f"• Auto-Aligned: {matched}/{tot} ({conf}%)\n"
                 f"• Engine Mode: {res.get('ocr_mode')}\n"
                 f"• Extracted: {res.get('ingested_at')}"
        )

        # Update Studio Header Badge
        self.lbl_studio_badge.configure(
            text=f"• 🟢 {matched}/{tot} Questions Aligned (Confidence: {conf}%)",
            fg="#34d399"
        )

        self._render_extraction_cards(res)

        if not self.suppress_modal:
            messagebox.showinfo(
                "Vision OCR Extraction Complete",
                f"Successfully extracted and aligned {matched}/{tot} questions!\n\n"
                f"Confidence Score: {conf}%\n"
                f"All questions are aligned to {res.get('exam_id')}.\n"
                f"Ready to proceed to Step 7 (CBSE AI Grading)!"
            )

    def _on_extraction_error(self, err_msg: str):
        self.btn_ingest.configure(state=tk.NORMAL, text="⚡ INGEST & EXTRACT WITH VISION OCR")
        self.lbl_kpi_status.configure(text="STATUS: Extraction Error", fg="#ef4444")
        self.lbl_kpi_details.configure(text=f"Error: {err_msg[:120]}")
        if not self.suppress_modal:
            messagebox.showerror("OCR Error", f"Vision OCR extraction failed: {err_msg}")

    def _render_extraction_cards(self, res: Dict[str, Any]):
        """Renders rich question-by-question alignment cards."""
        for w in self.cards_inner.winfo_children():
            w.destroy()

        questions = res.get("aligned_questions", [])
        if not questions:
            self._render_placeholder_studio()
            return

        for idx, q in enumerate(questions, 1):
            import html
            q_num = q.get("question_number", f"Q.{idx}")
            q_type = q.get("question_type", "SA")
            q_marks = q.get("marks", 1)
            q_text = html.unescape(q.get("question_text", ""))
            student_ans = html.unescape(q.get("student_response", ""))
            model_ans = html.unescape(q.get("model_answer", ""))
            status = q.get("alignment_status", "ALIGNED_VERIFIED")
            conf = q.get("confidence", 0.98)

            card = tk.Frame(
                self.cards_inner,
                bg="#161f30",
                bd=1,
                relief=tk.SOLID,
                highlightbackground="#334155",
                highlightthickness=1,
                padx=12,
                pady=10
            )
            card.pack(fill=tk.X, padx=10, pady=(0, 8))

            # Header row inside card
            top_row = tk.Frame(card, bg="#161f30")
            top_row.pack(fill=tk.X, pady=(0, 4))

            # Question Badge
            lbl_tag = tk.Label(
                top_row,
                text=f"{q_num} • {q_type} [{q_marks}M]",
                font=("Segoe UI", 8, "bold"),
                fg="#38bdf8",
                bg="#1e293b",
                padx=6,
                pady=2
            )
            lbl_tag.pack(side=tk.LEFT)

            # Alignment Status Badge
            is_ok = (status == "ALIGNED_VERIFIED")
            badge_color = "#34d399" if is_ok else "#ef4444"
            badge_text = f"Aligned ✅ ({int(conf * 100)}%)" if is_ok else "Unaligned ⚠️"
            lbl_status = tk.Label(
                top_row,
                text=badge_text,
                font=("Segoe UI", 8, "bold"),
                fg=badge_color,
                bg="#1e293b",
                padx=6,
                pady=2
            )
            lbl_status.pack(side=tk.RIGHT)

            # Question Prompt Text
            tk.Label(
                card,
                text=q_text,
                font=("Segoe UI", 9),
                fg="#f1f5f9",
                bg="#161f30",
                wraplength=820,
                justify=tk.LEFT
            ).pack(anchor="w", pady=(2, 6))

            # Split comparison: Left = Student Response, Right = Model Answer
            split_box = tk.Frame(card, bg="#161f30")
            split_box.pack(fill=tk.X, pady=(2, 0))

            # Student Response Column
            col_student = tk.Frame(split_box, bg="#0d1522", bd=1, relief=tk.SOLID, highlightbackground="#3b82f6", highlightthickness=1, padx=8, pady=6)
            col_student.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))

            tk.Label(
                col_student,
                text="✍️ THARUN'S EXTRACTED HANDWRITTEN WORKING STEPS:",
                font=("Segoe UI", 8, "bold"),
                fg="#60a5fa",
                bg="#0d1522"
            ).pack(anchor="w", pady=(0, 3))

            tk.Label(
                col_student,
                text=student_ans,
                font=("Consolas", 8),
                fg="#e2e8f0",
                bg="#0d1522",
                wraplength=380,
                justify=tk.LEFT
            ).pack(anchor="w")

            # Model Answer Column
            col_model = tk.Frame(split_box, bg="#0d1522", bd=1, relief=tk.SOLID, highlightbackground="#10b981", highlightthickness=1, padx=8, pady=6)
            col_model.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))

            tk.Label(
                col_model,
                text="🎯 OFFICIAL CBSE MODEL ANSWER & RUBRIC:",
                font=("Segoe UI", 8, "bold"),
                fg="#34d399",
                bg="#0d1522"
            ).pack(anchor="w", pady=(0, 3))

            tk.Label(
                col_model,
                text=model_ans,
                font=("Consolas", 8),
                fg="#e2e8f0",
                bg="#0d1522",
                wraplength=380,
                justify=tk.LEFT
            ).pack(anchor="w")

    def trigger_face_b_eval(self):
        """Triggers asynchronous Gemini CBSE evaluation in a background worker thread."""
        self.btn_run_eval.config(text="⏳ AI Evaluator Running...", state="disabled")
        exam_id = self.selected_exam_var.get()
        if hasattr(self.controller, "active_exam_id") and exam_id:
            self.controller.active_exam_id = exam_id

        def background_task():
            # Run the heavy Gemini call
            try:
                if exam_id:
                    self.exam_engine.evaluate_answer_sheet(exam_id)
            except Exception as e:
                print(f"[Face B] Evaluator background task notice: {e}")
            # Safely restore UI on the main thread
            self.root.after(0, lambda: self.btn_run_eval.config(text="✅ RUN GEMINI CBSE EVALUATION", state="normal"))
            self.root.after(0, lambda: self.switch_subview('topper_guide'))

        threading.Thread(target=background_task, daemon=True).start()

    def _on_proceed_to_step7(self):
        """Backward compatible forwarder to non-blocking trigger_face_b_eval."""
        self.trigger_face_b_eval()
