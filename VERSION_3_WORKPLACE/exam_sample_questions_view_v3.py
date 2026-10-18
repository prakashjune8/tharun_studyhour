"""
SAMPLE QUESTIONS & SCHOOL MODEL PAPERS VIEW (SESSION 7 DEDICATED MENU)
----------------------------------------------------------------------
Dedicated UI Menu for:
Uploading and managing School Sample Question Papers & Model Exam Papers.

Provides:
1. Complete unmingled isolation: purely dedicated to Sample Questions & School Patterns.
2. 7-Subject navigation (Mathematics, Physical Science, Biology, SST, English, Hindi, Tamil).
3. Dedicated Upload & Ingestion Center:
   - 🏆 Term 1 Half-Yearly Model Papers
   - ⚡ Periodic Tests 1 & 2 Sample Papers
   - 📝 Unit Test & Revision Worksheets
   - 🎯 Annual / Final Model Papers
4. Canonical Naming & Metadata Indexing:
   e.g., MATH_SAMPLE_Q_TERM1_SENTHIL_2025.pdf
5. Real-time Setting of Active Style Reference for the Gemini Question Architect.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Dict, Any, List, Optional

sys.stdout.reconfigure(encoding="utf-8")

from exam_ground_truth_v3 import SubjectCatalog, EXAM_SYSTEM_DIR, BASE_DIR
from exam_sample_questions_engine_v3 import SampleQuestionsEngine, MODEL_PAPERS_VAULT_ROOT


class ExamSampleQuestionsView:
    """
    Dedicated view for uploading and managing sample question papers and school exam patterns.
    """

    def __init__(self, parent_frame: tk.Frame, app_controller=None):
        self.parent = parent_frame
        self.app = app_controller
        raw = getattr(app_controller, "colors", {}) or {}
        self.colors = {
            "bg": raw.get("bg", "#0f172a"),
            "card_bg": raw.get("card_bg", "#1e293b"),
            "border": raw.get("card_border", raw.get("border", "#334155")),
            "accent": raw.get("accent", "#f97316"),
            "primary": raw.get("primary", "#38bdf8"),
            "text": raw.get("fg", raw.get("text", "#f8fafc")),
            "subtext": raw.get("fg_muted", raw.get("subtext", "#94a3b8"))
        }

        self.selected_subject_var = tk.StringVar(value="Mathematics")
        self.upload_file_path_var = tk.StringVar(value="")
        self.exam_category_var = tk.StringVar(value="term_1_model")
        self.paper_title_var = tk.StringVar(value="Senthil SPS Term1 2025")
        self.total_marks_var = tk.StringVar(value="80")
        self.time_mins_var = tk.StringVar(value="180")
        self.notes_var = tk.StringVar(value="")
        self.canonical_preview_var = tk.StringVar(value="")

    def build_ui(self):
        """Constructs the dedicated Sample Questions interface."""
        for w in self.parent.winfo_children():
            w.destroy()

        self.main_container = tk.Frame(self.parent, bg=self.colors["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # 1. Header Banner & Global Actions
        self._build_header(self.main_container)

        # 2. Subject Selector Tab Strip (7 Subjects)
        self._build_subject_tabs(self.main_container)

        # 3. Main Split View: Left Upload Center (380px), Right Explorer (Expand)
        work_area = tk.Frame(self.main_container, bg=self.colors["bg"])
        work_area.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        self.left_panel = tk.Frame(
            work_area,
            bg=self.colors["card_bg"],
            width=380,
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.colors["border"]
        )
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.left_panel.pack_propagate(False)

        self.right_panel = tk.Frame(
            work_area,
            bg=self.colors["card_bg"],
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.colors["border"]
        )
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_left_upload_center()
        self._build_right_explorer()

        self._update_canonical_preview()
        self._refresh_explorer()

    # =========================================================================
    # 1. HEADER BANNER
    # =========================================================================
    def _build_header(self, parent):
        hdr = tk.Frame(parent, bg="#131c2e", padx=14, pady=10, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground=self.colors["border"])
        hdr.pack(fill=tk.X)

        title_box = tk.Frame(hdr, bg="#131c2e")
        title_box.pack(side=tk.LEFT)

        lbl_t = tk.Label(
            title_box,
            text="📑 DEDICATED SAMPLE QUESTIONS & SCHOOL MODEL PAPERS VAULT",
            font=("Segoe UI", 11, "bold"),
            fg="#a855f7",
            bg="#131c2e"
        )
        lbl_t.pack(anchor="w")

        lbl_sub = tk.Label(
            title_box,
            text="Upload School Sample Question Papers & Term 1 Model Papers to Guide AI Question Style & Phrasing",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#131c2e"
        )
        lbl_sub.pack(anchor="w", pady=(2, 0))

        # Action Buttons on Right
        act_box = tk.Frame(hdr, bg="#131c2e")
        act_box.pack(side=tk.RIGHT)

        btn_folder = tk.Button(
            act_box,
            text="📁 Open Model Vault Root",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#334155",
            activebackground="#475569",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self._open_vault_root
        )
        btn_folder.pack(side=tk.LEFT, padx=(0, 6))

        btn_refresh = tk.Button(
            act_box,
            text="🔄 Refresh",
            font=("Segoe UI", 8, "bold"),
            fg="#a855f7",
            bg="#1e293b",
            activebackground="#334155",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self._refresh_explorer
        )
        btn_refresh.pack(side=tk.LEFT)

    # =========================================================================
    # 2. SUBJECT SELECTOR STRIP (7 SUBJECTS)
    # =========================================================================
    def _build_subject_tabs(self, parent):
        bar = tk.Frame(parent, bg="#0b1120", height=38)
        bar.pack(fill=tk.X, pady=(6, 0))
        bar.pack_propagate(False)

        subjects = [
            ("Mathematics", "🔢 Mathematics"),
            ("Physical Science", "🔬 Physical Science"),
            ("Biology", "🌱 Biology"),
            ("Social Science", "🌍 Social Science"),
            ("English", "📖 English"),
            ("Hindi", "🇮🇳 Hindi"),
            ("Tamil", "🌺 Tamil")
        ]

        self.subject_tab_buttons = {}
        for subj_key, label in subjects:
            btn = tk.Button(
                bar,
                text=label,
                font=("Segoe UI", 8, "bold"),
                relief=tk.FLAT,
                bd=0,
                padx=10,
                pady=5,
                cursor="hand2",
                command=lambda s=subj_key: self._on_subject_tab_selected(s)
            )
            btn.pack(side=tk.LEFT, padx=(0, 3))
            self.subject_tab_buttons[subj_key] = btn

        self._update_subject_tab_styles()

    def _update_subject_tab_styles(self):
        cur = self.selected_subject_var.get()
        for k, btn in self.subject_tab_buttons.items():
            if k == cur:
                btn.configure(bg="#a855f7", fg="#ffffff", activebackground="#9333ea")
            else:
                btn.configure(bg="#1e293b", fg="#94a3b8", activebackground="#334155")

    def _on_subject_tab_selected(self, subj_name: str):
        self.selected_subject_var.set(subj_name)
        self._update_subject_tab_styles()
        self._update_canonical_preview()
        self._refresh_explorer()

    # =========================================================================
    # 3. LEFT UPLOAD CENTER
    # =========================================================================
    def _build_left_upload_center(self):
        panel = self.left_panel
        from host_exam_ui import CustomDarkScrollbar

        canvas = tk.Canvas(panel, bg=self.colors["card_bg"], highlightthickness=0, bd=0)
        scrollbar = CustomDarkScrollbar(panel, target_widget=canvas, width=6, bg="#0b1120", thumb_color="#334155")
        content = tk.Frame(canvas, bg=self.colors["card_bg"])

        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        win_id = canvas.create_window((0, 0), window=content, anchor="nw", width=366)

        def _on_canvas_cfg(e):
            if e.width > 50:
                canvas.itemconfig(win_id, width=e.width - 8)
        canvas.bind("<Configure>", _on_canvas_cfg)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        hdr = tk.Label(
            content,
            text="📥 UPLOAD SAMPLE QUESTION PAPER",
            font=("Segoe UI", 9, "bold"),
            fg="#c084fc",
            bg=self.colors["card_bg"],
            anchor="w"
        )
        hdr.pack(fill=tk.X, padx=12, pady=(2, 1))

        # Target Indicator
        self.lbl_target_subj = tk.Label(
            content,
            text="Target Subject: Mathematics",
            font=("Segoe UI", 8, "bold"),
            fg="#34d399",
            bg="#161f30",
            relief=tk.SOLID,
            bd=1,
            padx=8,
            pady=2,
            anchor="w"
        )
        self.lbl_target_subj.pack(fill=tk.X, padx=12, pady=(0, 2))

        # Step 1: File Picker
        lbl_s1 = tk.Label(content, text="1. SELECT SAMPLE QUESTION PDF / SCAN:", font=("Segoe UI", 8, "bold"), fg="#f8fafc", bg=self.colors["card_bg"], anchor="w")
        lbl_s1.pack(fill=tk.X, padx=12, pady=(1, 1))

        f_box = tk.Frame(content, bg="#161f30", padx=6, pady=2, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground=self.colors["border"])
        f_box.pack(fill=tk.X, padx=12, pady=(0, 2))

        entry_f = tk.Entry(f_box, textvariable=self.upload_file_path_var, font=("Segoe UI", 8), bg="#0f172a", fg="#f8fafc", relief=tk.FLAT)
        entry_f.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        btn_br = tk.Button(
            f_box,
            text="Browse...",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#9333ea",
            relief=tk.FLAT,
            padx=8,
            pady=1,
            cursor="hand2",
            command=self._on_browse_file
        )
        btn_br.pack(side=tk.RIGHT)

        # Step 2: Category Selector (2x2 Grid)
        lbl_s2 = tk.Label(content, text="2. EXAM CATEGORY PATTERN:", font=("Segoe UI", 8, "bold"), fg="#f8fafc", bg=self.colors["card_bg"], anchor="w")
        lbl_s2.pack(fill=tk.X, padx=12, pady=(1, 1))

        cat_box = tk.Frame(content, bg=self.colors["card_bg"])
        cat_box.pack(fill=tk.X, padx=12, pady=(0, 2))

        cat_r1 = tk.Frame(cat_box, bg=self.colors["card_bg"])
        cat_r1.pack(fill=tk.X, pady=0)
        rb1 = tk.Radiobutton(
            cat_r1, text="🏆 Term 1 Model", variable=self.exam_category_var, value="term_1_model",
            fg="#e2e8f0", bg=self.colors["card_bg"], selectcolor="#0f172a", activebackground=self.colors["card_bg"], font=("Segoe UI", 8),
            command=self._update_canonical_preview
        )
        rb1.pack(side=tk.LEFT, padx=(0, 10))

        rb2 = tk.Radiobutton(
            cat_r1, text="⚡ Periodic Test", variable=self.exam_category_var, value="periodic_test",
            fg="#e2e8f0", bg=self.colors["card_bg"], selectcolor="#0f172a", activebackground=self.colors["card_bg"], font=("Segoe UI", 8),
            command=self._update_canonical_preview
        )
        rb2.pack(side=tk.LEFT)

        cat_r2 = tk.Frame(cat_box, bg=self.colors["card_bg"])
        cat_r2.pack(fill=tk.X, pady=0)
        rb3 = tk.Radiobutton(
            cat_r2, text="📝 Unit Test", variable=self.exam_category_var, value="unit_test",
            fg="#e2e8f0", bg=self.colors["card_bg"], selectcolor="#0f172a", activebackground=self.colors["card_bg"], font=("Segoe UI", 8),
            command=self._update_canonical_preview
        )
        rb3.pack(side=tk.LEFT, padx=(0, 28))

        rb4 = tk.Radiobutton(
            cat_r2, text="🎯 Annual Model", variable=self.exam_category_var, value="annual_model",
            fg="#e2e8f0", bg=self.colors["card_bg"], selectcolor="#0f172a", activebackground=self.colors["card_bg"], font=("Segoe UI", 8),
            command=self._update_canonical_preview
        )
        rb4.pack(side=tk.LEFT)

        # Step 3: Details Box (Single Row Title + Marks + Mins)
        det_box = tk.Frame(content, bg="#161f30", padx=6, pady=2, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground=self.colors["border"])
        det_box.pack(fill=tk.X, padx=12, pady=(0, 2))

        r1 = tk.Frame(det_box, bg="#161f30")
        r1.pack(fill=tk.X, pady=0)
        tk.Label(r1, text="Title:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#161f30", width=5, anchor="w").pack(side=tk.LEFT)
        e1 = tk.Entry(r1, textvariable=self.paper_title_var, font=("Segoe UI", 8), bg="#0f172a", fg="#f8fafc", relief=tk.FLAT)
        e1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        e1.bind("<KeyRelease>", lambda e: self._update_canonical_preview())

        tk.Label(r1, text="Marks:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#161f30", width=6, anchor="w").pack(side=tk.LEFT)
        e2 = tk.Entry(r1, textvariable=self.total_marks_var, font=("Segoe UI", 8), bg="#0f172a", fg="#f8fafc", width=5, relief=tk.FLAT)
        e2.pack(side=tk.LEFT, padx=(0, 6))

        tk.Label(r1, text="Mins:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#161f30", width=5, anchor="w").pack(side=tk.LEFT)
        e3 = tk.Entry(r1, textvariable=self.time_mins_var, font=("Segoe UI", 8), bg="#0f172a", fg="#f8fafc", width=5, relief=tk.FLAT)
        e3.pack(side=tk.LEFT)

        # Step 4: Canonical Preview Box
        prev_box = tk.Frame(content, bg="#0b1120", padx=6, pady=2, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#fbbf24")
        prev_box.pack(fill=tk.X, padx=12, pady=(1, 2))

        self.lbl_prev_canon = tk.Label(
            prev_box,
            textvariable=self.canonical_preview_var,
            font=("Consolas", 7, "bold"),
            fg="#c084fc",
            bg="#0b1120",
            anchor="w",
            wraplength=340,
            justify=tk.LEFT
        )
        self.lbl_prev_canon.pack(fill=tk.X)

        # Primary Ingest Button
        self.btn_ingest = tk.Button(
            content,
            text="🚀 INGEST SAMPLE QUESTION PAPER",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#9333ea",
            activebackground="#7e22ce",
            relief=tk.FLAT,
            bd=0,
            pady=5,
            cursor="hand2",
            command=self._on_ingest_clicked
        )
        self.btn_ingest.pack(fill=tk.X, padx=12, pady=(0, 3))

    def _update_canonical_preview(self):
        subj = self.selected_subject_var.get()
        cat = self.exam_category_var.get()
        title = self.paper_title_var.get()
        src = self.upload_file_path_var.get().strip()
        ext = os.path.splitext(src)[1] if src else ".pdf"

        folder_name = SampleQuestionsEngine.SUBJECT_FOLDER_MAP.get(subj, "01_Mathematics")
        if hasattr(self, "lbl_target_subj"):
            self.lbl_target_subj.configure(text=f"Target Vault: {subj} ({folder_name})")

        canon = SampleQuestionsEngine.generate_canonical_filename(
            subject=subj,
            exam_category=cat,
            paper_title=title,
            original_ext=ext or ".pdf"
        )
        self.canonical_preview_var.set(f"Canonical:\n{canon}")

    def _on_browse_file(self):
        path = filedialog.askopenfilename(
            parent=self.parent,
            title="Select Sample Question Paper or Model Exam PDF",
            filetypes=[("PDF and Images", "*.pdf *.png *.jpg *.jpeg"), ("All Files", "*.*")]
        )
        if path:
            self.upload_file_path_var.set(path)
            self._update_canonical_preview()

    def _on_ingest_clicked(self):
        src = self.upload_file_path_var.get().strip()
        if not src or not os.path.exists(src):
            messagebox.showerror("Error", "Please select a valid existing PDF or image sample paper first.", parent=self.parent)
            return

        subj = self.selected_subject_var.get()
        cat = self.exam_category_var.get()
        title = self.paper_title_var.get().strip()
        try:
            m = int(self.total_marks_var.get())
        except Exception:
            m = 80
        try:
            t = int(self.time_mins_var.get())
        except Exception:
            t = 180

        res = SampleQuestionsEngine.ingest_sample_paper(
            source_file_path=src,
            subject=subj,
            exam_category=cat,
            paper_title=title,
            total_marks=m,
            time_mins=t,
            school_name="Senthil Public School",
            notes=self.notes_var.get()
        )

        if res.get("success"):
            messagebox.showinfo(
                "Sample Paper Ingested",
                f"Sample question paper successfully saved into {subj} Model Vault!\n\n"
                f"Canonical Filename:\n{res['canonical_name']}\n\n"
                f"Pages Detected: {res['page_count']}\n"
                f"Set as Active Style Reference for Question Generation.",
                parent=self.parent
            )
            self.upload_file_path_var.set("")
            self._refresh_explorer()
        else:
            messagebox.showerror("Ingestion Failed", res.get("error", "Unknown error"), parent=self.parent)

    # =========================================================================
    # 4. RIGHT EXPLORER
    # =========================================================================
    def _build_right_explorer(self):
        panel = self.right_panel

        top_bar = tk.Frame(panel, bg="#161f30", padx=14, pady=8)
        top_bar.pack(fill=tk.X)

        self.lbl_explorer_title = tk.Label(
            top_bar,
            text="SAMPLE QUESTION PAPERS: Mathematics",
            font=("Segoe UI", 9, "bold"),
            fg="#c084fc",
            bg="#161f30"
        )
        self.lbl_explorer_title.pack(side=tk.LEFT)

        btn_open_subj_folder = tk.Button(
            top_bar,
            text="📁 Open This Subject Model Folder",
            font=("Segoe UI", 8),
            fg="#cbd5e1",
            bg="#334155",
            activebackground="#475569",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2",
            command=self._open_current_subject_folder
        )
        btn_open_subj_folder.pack(side=tk.RIGHT)

        canvas = tk.Canvas(panel, bg="#090d16", highlightthickness=0, bd=0)
        from host_exam_ui import CustomDarkScrollbar
        scrollbar = CustomDarkScrollbar(panel, target_widget=canvas, width=6, bg="#0b1120", thumb_color="#334155")
        self.cards_frame = tk.Frame(canvas, bg="#090d16", padx=12, pady=10)

        self.cards_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        win_id = canvas.create_window((0, 0), window=self.cards_frame, anchor="nw", width=680)

        def _on_canvas_resize(e):
            if e.width > 50:
                canvas.itemconfig(win_id, width=e.width - 12)
        canvas.bind("<Configure>", _on_canvas_resize)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.explorer_canvas = canvas

    def _refresh_explorer(self):
        subj = self.selected_subject_var.get()
        folder_name = SampleQuestionsEngine.SUBJECT_FOLDER_MAP.get(subj, "01_Mathematics")
        self.lbl_explorer_title.configure(text=f"SAMPLE QUESTION PAPERS: {subj} (Folder: 02_SCHOOL_MODEL_PAPERS_PDF/{folder_name})")

        for w in self.cards_frame.winfo_children():
            w.destroy()

        papers = SampleQuestionsEngine.list_subject_sample_papers(subj)

        if not papers:
            empty_box = tk.Frame(self.cards_frame, bg="#131c2e", padx=20, pady=30, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#334155")
            empty_box.pack(fill=tk.X, pady=20)

            tk.Label(
                empty_box,
                text="📂 No Sample Question Papers Uploaded Yet for This Subject",
                font=("Segoe UI", 10, "bold"),
                fg="#f8fafc",
                bg="#131c2e"
            ).pack(pady=(0, 4))

            tk.Label(
                empty_box,
                text=f"Upload Senthil Public School Term 1 model papers, Periodic Test papers, or sample question scans on the left.\n"
                     f"The AI will automatically study the teacher's questioning style and emulate it during daily exams.",
                font=("Segoe UI", 8),
                fg="#94a3b8",
                bg="#131c2e",
                justify=tk.CENTER
            ).pack()
            return

        for item in reversed(papers):
            self._render_paper_card(self.cards_frame, item)

    def _render_paper_card(self, parent, item: Dict[str, Any]):
        card = tk.Frame(
            parent,
            bg="#161f30",
            padx=12,
            pady=10,
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground="#a855f7" if item.get("is_active_style_reference") else "#334155"
        )
        card.pack(fill=tk.X, pady=(0, 8))

        top_row = tk.Frame(card, bg="#161f30")
        top_row.pack(fill=tk.X)

        cat_badge_map = {
            "term_1_model": ("🏆 Term 1 Model", "#6b21a8"),
            "periodic_test": ("⚡ Periodic Test", "#b45309"),
            "unit_test": ("📝 Unit Test", "#1e3a8a"),
            "annual_model": ("🎯 Annual Model", "#047857")
        }
        b_txt, b_col = cat_badge_map.get(item.get("exam_category", ""), ("📑 Sample Paper", "#334155"))
        lbl_badge = tk.Label(
            top_row,
            text=b_txt,
            font=("Segoe UI", 7, "bold"),
            fg="#ffffff",
            bg=b_col,
            padx=6,
            pady=2
        )
        lbl_badge.pack(side=tk.RIGHT)

        lbl_name = tk.Label(
            top_row,
            text=f"📑 {item.get('canonical_filename', '')}",
            font=("Consolas", 9, "bold"),
            fg="#f8fafc",
            bg="#161f30",
            anchor="w"
        )
        lbl_name.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Mid details
        mid_row = tk.Frame(card, bg="#161f30")
        mid_row.pack(fill=tk.X, pady=(4, 6))

        marks = item.get("total_marks", 80)
        mins = item.get("time_mins", 180)
        pages = item.get("total_pages", 1)
        size_kb = int(item.get("file_size_bytes", 0) / 1024)
        school = item.get("school_name", "SPS")
        title = item.get("paper_title", "")

        info_txt = f"{title} • {school} • {marks} Marks ({mins} Mins) • {pages} Pages • {size_kb} KB"
        lbl_info = tk.Label(mid_row, text=info_txt, font=("Segoe UI", 8), fg="#94a3b8", bg="#161f30", anchor="w")
        lbl_info.pack(side=tk.LEFT)

        # Bot row
        bot_row = tk.Frame(card, bg="#161f30")
        bot_row.pack(fill=tk.X, pady=(4, 0))

        is_active = item.get("is_active_style_reference", False)
        if is_active:
            lbl_act = tk.Label(
                bot_row,
                text="🟢 ACTIVE STYLE REFERENCE FOR AI",
                font=("Segoe UI", 7, "bold"),
                fg="#a855f7",
                bg="#2e1065",
                padx=6,
                pady=2
            )
            lbl_act.pack(side=tk.LEFT)
        else:
            btn_set_act = tk.Button(
                bot_row,
                text="⭐ Set as Style Reference",
                font=("Segoe UI", 7, "bold"),
                fg="#cbd5e1",
                bg="#334155",
                activebackground="#a855f7",
                relief=tk.FLAT,
                bd=0,
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda r_id=item["id"]: self._on_set_active_paper(r_id)
            )
            btn_set_act.pack(side=tk.LEFT)

        btn_open = tk.Button(
            bot_row,
            text="👁️ Open Document",
            font=("Segoe UI", 7, "bold"),
            fg="#ffffff",
            bg="#7c3aed",
            activebackground="#6d28d9",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=2,
            cursor="hand2",
            command=lambda p=item.get("absolute_path", ""): self._open_document(p)
        )
        btn_open.pack(side=tk.RIGHT, padx=(4, 0))

        # Direct 1-Click Apply to Face A
        btn_apply = tk.Button(
            bot_row,
            text="⚡ Apply to Face A ➔",
            font=("Segoe UI", 7, "bold"),
            fg="#ffffff",
            bg="#f97316",
            activebackground="#ea580c",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=2,
            cursor="hand2",
            command=lambda r_id=item["id"]: self._apply_and_switch_to_face_a(r_id)
        )
        btn_apply.pack(side=tk.RIGHT, padx=(4, 0))

    def _apply_and_switch_to_face_a(self, record_id: str):
        SampleQuestionsEngine.set_active_style_reference(record_id)
        if hasattr(self.controller, "switch_subview"):
            self.controller.switch_subview("face_a")

    def _on_set_active_paper(self, record_id: str):
        SampleQuestionsEngine.set_active_style_reference(record_id)
        self._refresh_explorer()

    def _open_document(self, path: str):
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", f"File does not exist:\n{path}", parent=self.parent)
            return
        try:
            os.startfile(path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open document: {e}", parent=self.parent)

    def _open_vault_root(self):
        try:
            SampleQuestionsEngine.ensure_vault_directories()
            os.startfile(MODEL_PAPERS_VAULT_ROOT)
        except Exception as e:
            messagebox.showinfo("Vault Directory", f"Model Papers Directory:\n{MODEL_PAPERS_VAULT_ROOT}")

    def _open_current_subject_folder(self):
        subj = self.selected_subject_var.get()
        folder_name = SampleQuestionsEngine.SUBJECT_FOLDER_MAP.get(subj, "01_Mathematics")
        p = os.path.join(MODEL_PAPERS_VAULT_ROOT, folder_name)
        try:
            os.makedirs(p, exist_ok=True)
            os.startfile(p)
        except Exception as e:
            messagebox.showinfo("Subject Model Vault", f"Subject Directory:\n{p}")
