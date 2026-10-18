"""
EXAM VAULT & SOURCE LIBRARY VIEW (SESSION 7 DEDICATED MENU)
------------------------------------------------------------
Dedicated, unmingled UI Controller for:
Subject Vault & Learning Material Library.

Provides:
1. Pure separation: completely isolated from Question Paper Architect & Evaluator.
2. Subject-by-subject navigation across all 7 master CBSE subjects:
   - Mathematics
   - Physical Science
   - Biology
   - Social Science
   - English
   - Hindi
   - Tamil
3. Direct Upload & Ingestion Center:
   - 📘 Full Complete Textbook (Whole book scans)
   - 📑 Topic / Chapter Photocopy (Exercise & problem scans)
   - 📝 School Model Exam Paper (Term 1 / Periodic Test papers)
   - Live canonical standardization preview
4. Vault Explorer for each subject:
   - View, open PDF, inspect metadata, toggle active source, and manage vault files.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Dict, Any, List, Optional

if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from exam_ground_truth_v3 import SubjectCatalog, EXAM_SYSTEM_DIR, BASE_DIR
from exam_smart_ingestion_wizard_v3 import SmartIngestionWizard, TEXTBOOKS_VAULT_ROOT


class ExamVaultLibraryView:
    """
    Dedicated view for uploading, organizing, and managing textbooks and learning materials.
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
        self.filter_category_var = tk.StringVar(value="all")

        # Form State for Left Upload Panel
        self.upload_file_path_var = tk.StringVar(value="")
        self.material_type_var = tk.StringVar(value="topic_photocopy")
        self.chapter_var = tk.StringVar(value="Ch 09 Algebraic Expressions")
        self.exercise_var = tk.StringVar(value="Ex 9.3 Identities")
        self.book_title_var = tk.StringVar(value="NCERT Class 8")
        self.notes_var = tk.StringVar(value="")
        self.canonical_preview_var = tk.StringVar(value="")

    def build_ui(self):
        """Constructs the dedicated Subject Vault & Library interface."""
        for w in self.parent.winfo_children():
            w.destroy()

        self.main_container = tk.Frame(self.parent, bg=self.colors["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # 1. Header Banner & Global Actions
        self._build_header(self.main_container)

        # 2. Subject Selector Tab Strip (7 Subjects)
        self._build_subject_tabs(self.main_container)

        # 3. Main Split View: Left Upload Center (380px), Right Vault Explorer (Expand)
        work_area = tk.Frame(self.main_container, bg=self.colors["bg"])
        work_area.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

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
        self._build_right_vault_explorer()

        # Update preview & list
        self._update_canonical_preview()
        self._refresh_vault_explorer()

    # =========================================================================
    # 1. HEADER BANNER
    # =========================================================================
    def _build_header(self, parent):
        hdr = tk.Frame(parent, bg="#131c2e", padx=14, pady=5, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground=self.colors["border"])
        hdr.pack(fill=tk.X)

        title_box = tk.Frame(hdr, bg="#131c2e")
        title_box.pack(side=tk.LEFT)

        lbl_t = tk.Label(
            title_box,
            text="📚 DEDICATED SUBJECT VAULT & LEARNING SOURCE LIBRARY",
            font=("Segoe UI", 11, "bold"),
            fg="#f97316",
            bg="#131c2e"
        )
        lbl_t.pack(anchor="w")

        lbl_sub = tk.Label(
            title_box,
            text="Class 8 CBSE • Permanent 7-Subject Repositories • Textbooks, Photocopies & School Model Papers",
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
            text="📁 Open Vault Root",
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
            fg="#38bdf8",
            bg="#1e293b",
            activebackground="#334155",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self._refresh_vault_explorer
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
                btn.configure(bg="#f97316", fg="#ffffff", activebackground="#ea580c")
            else:
                btn.configure(bg="#1e293b", fg="#94a3b8", activebackground="#334155")

    def _on_subject_tab_selected(self, subj_name: str):
        self.selected_subject_var.set(subj_name)
        self._update_subject_tab_styles()
        self._update_canonical_preview()
        self._refresh_vault_explorer()

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

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        hdr = tk.Label(
            content,
            text="📥 UPLOAD TO SUBJECT VAULT",
            font=("Segoe UI", 9, "bold"),
            fg="#38bdf8",
            bg=self.colors["card_bg"],
            anchor="w"
        )
        hdr.pack(fill=tk.X, padx=12, pady=(4, 2))

        # Target Subject Indicator
        self.lbl_target_subj = tk.Label(
            content,
            text="Target Vault: Mathematics (01_Mathematics)",
            font=("Segoe UI", 8, "bold"),
            fg="#34d399",
            bg="#161f30",
            relief=tk.SOLID,
            bd=1,
            padx=8,
            pady=3,
            anchor="w"
        )
        self.lbl_target_subj.pack(fill=tk.X, padx=12, pady=(0, 3))

        # Step 1: Browse File
        lbl_s1 = tk.Label(content, text="1. SELECT PDF OR PHOTOCOPY:", font=("Segoe UI", 8, "bold"), fg="#f8fafc", bg=self.colors["card_bg"], anchor="w")
        lbl_s1.pack(fill=tk.X, padx=12, pady=(1, 1))

        f_box = tk.Frame(content, bg="#161f30", padx=6, pady=2, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground=self.colors["border"])
        f_box.pack(fill=tk.X, padx=12, pady=(0, 3))

        entry_f = tk.Entry(f_box, textvariable=self.upload_file_path_var, font=("Segoe UI", 8), bg="#0f172a", fg="#f8fafc", relief=tk.FLAT)
        entry_f.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        btn_br = tk.Button(
            f_box,
            text="Browse...",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#0284c7",
            relief=tk.FLAT,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self._on_browse_file
        )
        btn_br.pack(side=tk.RIGHT)

        # Step 2: Material Category
        lbl_s2 = tk.Label(content, text="2. MATERIAL CLASSIFICATION:", font=("Segoe UI", 8, "bold"), fg="#f8fafc", bg=self.colors["card_bg"], anchor="w")
        lbl_s2.pack(fill=tk.X, padx=12, pady=(1, 1))

        cat_box = tk.Frame(content, bg=self.colors["card_bg"])
        cat_box.pack(fill=tk.X, padx=12, pady=(0, 2))

        rb1 = tk.Radiobutton(
            cat_box, text="📑 Topic Photocopy", variable=self.material_type_var, value="topic_photocopy",
            fg="#e2e8f0", bg=self.colors["card_bg"], selectcolor="#0f172a", activebackground=self.colors["card_bg"], font=("Segoe UI", 8),
            command=self._on_type_changed
        )
        rb1.pack(side=tk.LEFT, padx=(0, 6))

        rb2 = tk.Radiobutton(
            cat_box, text="📘 Full Textbook", variable=self.material_type_var, value="full_textbook",
            fg="#e2e8f0", bg=self.colors["card_bg"], selectcolor="#0f172a", activebackground=self.colors["card_bg"], font=("Segoe UI", 8),
            command=self._on_type_changed
        )
        rb2.pack(side=tk.LEFT, padx=(0, 6))

        rb3 = tk.Radiobutton(
            cat_box, text="📝 Model Exam", variable=self.material_type_var, value="model_exam_paper",
            fg="#e2e8f0", bg=self.colors["card_bg"], selectcolor="#0f172a", activebackground=self.colors["card_bg"], font=("Segoe UI", 8),
            command=self._on_type_changed
        )
        rb3.pack(side=tk.LEFT)

        # Step 3: Dynamic Detail Fields
        self.detail_container = tk.Frame(content, bg="#161f30", padx=8, pady=3, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground=self.colors["border"])
        self.detail_container.pack(fill=tk.X, padx=12, pady=(0, 3))
        self._render_dynamic_fields()

        # Step 4: Canonical Preview
        lbl_s4 = tk.Label(content, text="3. CANONICAL STANDARDIZATION PREVIEW:", font=("Segoe UI", 8, "bold"), fg="#fbbf24", bg=self.colors["card_bg"], anchor="w")
        lbl_s4.pack(fill=tk.X, padx=12, pady=(1, 1))

        prev_box = tk.Frame(content, bg="#0b1120", padx=8, pady=2, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#fbbf24")
        prev_box.pack(fill=tk.X, padx=12, pady=(0, 3))

        self.lbl_prev_canon = tk.Label(
            prev_box,
            textvariable=self.canonical_preview_var,
            font=("Consolas", 8, "bold"),
            fg="#34d399",
            bg="#0b1120",
            anchor="w",
            wraplength=330,
            justify=tk.LEFT
        )
        self.lbl_prev_canon.pack(fill=tk.X)

        # Primary Ingest Button
        self.btn_ingest = tk.Button(
            content,
            text="🚀 INGEST & SAVE TO VAULT",
            font=("Segoe UI", 9, "bold"),
            fg="#ffffff",
            bg="#16a34a",
            activebackground="#15803d",
            relief=tk.FLAT,
            bd=0,
            pady=4,
            cursor="hand2",
            command=self._on_ingest_clicked
        )
        self.btn_ingest.pack(fill=tk.X, padx=12, pady=(2, 6))

    def _render_dynamic_fields(self):
        for w in self.detail_container.winfo_children():
            w.destroy()

        t = self.material_type_var.get()
        if t == "topic_photocopy":
            r1 = tk.Frame(self.detail_container, bg="#161f30")
            r1.pack(fill=tk.X, pady=1)
            tk.Label(r1, text="Chapter:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#161f30", width=7, anchor="w").pack(side=tk.LEFT)
            e1 = tk.Entry(r1, textvariable=self.chapter_var, font=("Segoe UI", 8), bg="#0f172a", fg="#f8fafc", relief=tk.FLAT)
            e1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
            tk.Label(r1, text="Ex:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#161f30", width=3, anchor="w").pack(side=tk.LEFT)
            e2 = tk.Entry(r1, textvariable=self.exercise_var, font=("Segoe UI", 8), bg="#0f172a", fg="#f8fafc", relief=tk.FLAT, width=12)
            e2.pack(side=tk.LEFT, fill=tk.X, expand=True)
            e1.bind("<KeyRelease>", lambda e: self._update_canonical_preview())
            e2.bind("<KeyRelease>", lambda e: self._update_canonical_preview())

        elif t == "full_textbook":
            r1 = tk.Frame(self.detail_container, bg="#161f30")
            r1.pack(fill=tk.X, pady=1)
            tk.Label(r1, text="Book Title:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#161f30", width=10, anchor="w").pack(side=tk.LEFT)
            e1 = tk.Entry(r1, textvariable=self.book_title_var, font=("Segoe UI", 8), bg="#0f172a", fg="#f8fafc", relief=tk.FLAT)
            e1.pack(side=tk.LEFT, fill=tk.X, expand=True)
            e1.bind("<KeyRelease>", lambda e: self._update_canonical_preview())

        else:  # model_exam_paper
            r1 = tk.Frame(self.detail_container, bg="#161f30")
            r1.pack(fill=tk.X, pady=1)
            tk.Label(r1, text="Exam Title:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#161f30", width=10, anchor="w").pack(side=tk.LEFT)
            e1 = tk.Entry(r1, textvariable=self.book_title_var, font=("Segoe UI", 8), bg="#0f172a", fg="#f8fafc", relief=tk.FLAT)
            e1.pack(side=tk.LEFT, fill=tk.X, expand=True)
            e1.bind("<KeyRelease>", lambda e: self._update_canonical_preview())

    def _on_type_changed(self):
        self._render_dynamic_fields()
        self._update_canonical_preview()

    def _update_canonical_preview(self):
        subj = self.selected_subject_var.get()
        t = self.material_type_var.get()
        folder_name = SmartIngestionWizard.SUBJECT_FOLDER_MAP.get(subj, "01_Mathematics")

        if hasattr(self, "lbl_target_subj"):
            self.lbl_target_subj.configure(text=f"Target Vault: {subj} ({folder_name})")

        src = self.upload_file_path_var.get().strip()
        ext = os.path.splitext(src)[1] if src else ".pdf"

        canon = SmartIngestionWizard.generate_canonical_filename(
            subject=subj,
            material_type=t,
            chapter_name=self.chapter_var.get(),
            exercise_or_topic=self.exercise_var.get(),
            book_title=self.book_title_var.get(),
            original_ext=ext or ".pdf"
        )
        self.canonical_preview_var.set(f"Canonical: {canon}")

    def _on_browse_file(self):
        path = filedialog.askopenfilename(
            parent=self.parent,
            title="Select Textbook, Photocopy, or Model Exam Paper",
            filetypes=[("PDF and Images", "*.pdf *.png *.jpg *.jpeg"), ("All Files", "*.*")]
        )
        if path:
            self.upload_file_path_var.set(path)
            self._update_canonical_preview()

    def _on_ingest_clicked(self):
        src = self.upload_file_path_var.get().strip()
        if not src or not os.path.exists(src):
            messagebox.showerror("Error", "Please select a valid existing PDF or image file first.", parent=self.parent)
            return

        subj = self.selected_subject_var.get()
        m_type = self.material_type_var.get()

        res = SmartIngestionWizard.ingest_file_to_vault(
            source_file_path=src,
            subject=subj,
            material_type=m_type,
            chapter_name=self.chapter_var.get(),
            exercise_or_topic=self.exercise_var.get(),
            book_title=self.book_title_var.get(),
            notes=self.notes_var.get()
        )

        if res.get("success"):
            messagebox.showinfo(
                "Ingestion Successful",
                f"File successfully ingested into {subj} vault!\n\n"
                f"Canonical Filename:\n{res['canonical_name']}\n\n"
                f"Pages Detected: {res['page_count']}",
                parent=self.parent
            )
            self.upload_file_path_var.set("")
            self._refresh_vault_explorer()
        else:
            messagebox.showerror("Ingestion Failed", res.get("error", "Unknown error"), parent=self.parent)

    # =========================================================================
    # 4. RIGHT VAULT EXPLORER
    # =========================================================================
    def _build_right_vault_explorer(self):
        panel = self.right_panel

        # Top Explorer Toolbar
        top_bar = tk.Frame(panel, bg="#161f30", padx=14, pady=8)
        top_bar.pack(fill=tk.X)

        self.lbl_explorer_title = tk.Label(
            top_bar,
            text="VAULT INVENTORY: Mathematics",
            font=("Segoe UI", 9, "bold"),
            fg="#38bdf8",
            bg="#161f30"
        )
        self.lbl_explorer_title.pack(side=tk.LEFT)

        btn_open_subj_folder = tk.Button(
            top_bar,
            text="📁 Open This Subject Folder",
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

        # Scrollable Content Area for Vault Cards with 6px Custom Dark Scrollbar
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

    def _refresh_vault_explorer(self):
        """Refreshes the list of files in the currently selected subject vault."""
        subj = self.selected_subject_var.get()
        folder_name = SmartIngestionWizard.SUBJECT_FOLDER_MAP.get(subj, "01_Mathematics")
        self.lbl_explorer_title.configure(text=f"VAULT INVENTORY: {subj} (Folder: {folder_name})")

        for w in self.cards_frame.winfo_children():
            w.destroy()

        materials = SmartIngestionWizard.list_subject_materials(subj)

        if not materials:
            empty_box = tk.Frame(self.cards_frame, bg="#131c2e", padx=20, pady=30, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#334155")
            empty_box.pack(fill=tk.X, pady=20)

            tk.Label(
                empty_box,
                text="📂 No Materials Uploaded Yet in This Subject Vault",
                font=("Segoe UI", 10, "bold"),
                fg="#f8fafc",
                bg="#131c2e"
            ).pack(pady=(0, 4))

            tk.Label(
                empty_box,
                text=f"Use the Upload panel on the left to add textbooks, topic photocopies, or school model exam papers for {subj}.\n"
                     f"Files will be canonically named and stored permanently in: EXAM_SYSTEM_V3/02_UPLOADED_TEXTBOOKS_PDF/{folder_name}/",
                font=("Segoe UI", 8),
                fg="#94a3b8",
                bg="#131c2e",
                justify=tk.CENTER
            ).pack()
            return

        # Render Material Cards
        for idx, item in enumerate(reversed(materials), 1):
            self._render_material_card(self.cards_frame, item)

    def _render_material_card(self, parent, item: Dict[str, Any]):
        card = tk.Frame(
            parent,
            bg="#161f30",
            padx=12,
            pady=10,
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground="#f97316" if item.get("is_active_source") else "#334155"
        )
        card.pack(fill=tk.X, pady=(0, 8))

        # Top Line: Canonical Name & Type Badge
        top_row = tk.Frame(card, bg="#161f30")
        top_row.pack(fill=tk.X)

        canon_name = item.get("canonical_filename", "UNKNOWN_FILE.pdf")
        lbl_name = tk.Label(
            top_row,
            text=f"📄 {canon_name}",
            font=("Consolas", 9, "bold"),
            fg="#f8fafc",
            bg="#161f30",
            anchor="w"
        )
        lbl_name.pack(side=tk.LEFT)

        # Type Badge
        m_type = item.get("material_type", "")
        badge_text_map = {
            "full_textbook": "📘 Full Textbook",
            "topic_photocopy": "📑 Topic Photocopy",
            "model_exam_paper": "📝 Model Exam Paper"
        }
        badge_bg_map = {
            "full_textbook": "#1e3a8a",
            "topic_photocopy": "#7c2d12",
            "model_exam_paper": "#4c1d95"
        }
        lbl_badge = tk.Label(
            top_row,
            text=badge_text_map.get(m_type, "📑 Material"),
            font=("Segoe UI", 7, "bold"),
            fg="#ffffff",
            bg=badge_bg_map.get(m_type, "#334155"),
            padx=6,
            pady=2
        )
        lbl_badge.pack(side=tk.RIGHT)

        # Middle Details Row
        mid_row = tk.Frame(card, bg="#161f30")
        mid_row.pack(fill=tk.X, pady=(4, 6))

        pages = item.get("total_pages", 1)
        size_kb = int(item.get("file_size_bytes", 0) / 1024)
        ch = item.get("chapter_name", "")
        ex = item.get("exercise_or_topic", "")
        bk = item.get("book_title", "")
        detail_txt = f"Pages: {pages} • Size: {size_kb} KB"
        if ch or ex:
            detail_txt += f" • {ch} | {ex}"
        if bk:
            detail_txt += f" • {bk}"

        lbl_detail = tk.Label(
            mid_row,
            text=detail_txt,
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#161f30",
            anchor="w"
        )
        lbl_detail.pack(side=tk.LEFT)

        # Bottom Action Strip
        bot_row = tk.Frame(card, bg="#161f30")
        bot_row.pack(fill=tk.X, pady=(4, 0))

        is_active = item.get("is_active_source", False)
        if is_active:
            lbl_act = tk.Label(
                bot_row,
                text="🟢 ACTIVE SOURCE FOR EXAMS",
                font=("Segoe UI", 7, "bold"),
                fg="#34d399",
                bg="#064e3b",
                padx=6,
                pady=2
            )
            lbl_act.pack(side=tk.LEFT)
        else:
            btn_set_act = tk.Button(
                bot_row,
                text="⭐ Set as Active",
                font=("Segoe UI", 7, "bold"),
                fg="#cbd5e1",
                bg="#334155",
                activebackground="#f97316",
                relief=tk.FLAT,
                bd=0,
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda r_id=item["id"]: self._on_set_active_material(r_id)
            )
            btn_set_act.pack(side=tk.LEFT)

        # Open File Button
        btn_open = tk.Button(
            bot_row,
            text="👁️ Open Document",
            font=("Segoe UI", 7, "bold"),
            fg="#ffffff",
            bg="#0284c7",
            activebackground="#0369a1",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=2,
            cursor="hand2",
            command=lambda p=item.get("absolute_path", ""): self._open_document(p)
        )
        btn_open.pack(side=tk.RIGHT, padx=(4, 0))

        # Direct 1-Click Send to Face A Architect
        btn_face_a = tk.Button(
            bot_row,
            text="⚡ Send to Face A ➔",
            font=("Segoe UI", 7, "bold"),
            fg="#ffffff",
            bg="#f97316",
            activebackground="#ea580c",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=2,
            cursor="hand2",
            command=lambda r_id=item["id"]: self._send_to_face_a(r_id)
        )
        btn_face_a.pack(side=tk.RIGHT, padx=(4, 0))

    def _send_to_face_a(self, record_id: str):
        SmartIngestionWizard.set_active_material(record_id)
        if hasattr(self.controller, "switch_subview"):
            self.controller.switch_subview("face_a")

    def _on_set_active_material(self, record_id: str):
        SmartIngestionWizard.set_active_material(record_id)
        self._refresh_vault_explorer()

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
            os.makedirs(TEXTBOOKS_VAULT_ROOT, exist_ok=True)
            os.startfile(TEXTBOOKS_VAULT_ROOT)
        except Exception as e:
            messagebox.showinfo("Vault Directory", f"Root Directory:\n{TEXTBOOKS_VAULT_ROOT}")

    def _open_current_subject_folder(self):
        subj = self.selected_subject_var.get()
        folder_name = SmartIngestionWizard.SUBJECT_FOLDER_MAP.get(subj, "01_Mathematics")
        p = os.path.join(TEXTBOOKS_VAULT_ROOT, folder_name)
        try:
            os.makedirs(p, exist_ok=True)
            os.startfile(p)
        except Exception as e:
            messagebox.showinfo("Subject Vault", f"Subject Directory:\n{p}")
