"""
HOST EXAM FACE A UI CONTROLLER (SESSION 6)
------------------------------------------
Clean, modern, responsive Desktop UI Controller for:
Face A: Question Paper Architect.

Integrates:
1. Top Command Deck with [🟢 Gemini AI Active] badge and API key modal.
2. Complete 7-Subject Selector (Math, Physical Science, Biology, SST, English, Hindi, Tamil).
3. The Combined Smart Time & Intensity Dial (Chips, Precision Slider, Live Breakdown).
4. One-Click "No Homework Today" Weak-Subject Error Bank Healer.
5. Live Split-Screen Print Studio Preview with:
   - [🖨️ Print / Web] (HTML Print Preview with KaTeX)
   - [📄 Export PDF] (Vector PDF with THARUN REVISION BANNER)
   - [📝 Blank Booklet] (75/25 Math Workspace Answer Booklet)
"""

import os
import sys
import json
import webbrowser
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, Any, List, Optional
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

# Import Verified Engine Modules from Sessions 1 - 5
from exam_ground_truth_v3 import SubjectCatalog, GeminiGateway, DiaryGroundTruth, EXAM_SYSTEM_DIR
from exam_smart_time_dial_v3 import SmartTimeIntensityDial
from exam_phase_assembler_v3 import ExamSpecAssembler
from exam_lifecycle_controller_v3 import ExamLifecycleController
from exam_weak_subject_engine_v3 import WeakSubjectHealingEngine
from exam_question_architect_v3 import GeminiQuestionArchitect
from exam_print_studio_v3 import ExamPrintStudio
from exam_math_fraction_engine_v3 import MathFractionEngine
from exam_smart_ingestion_wizard_v3 import SmartIngestionWizard, SmartIngestionDialog
from exam_sample_questions_engine_v3 import SampleQuestionsEngine


class HostExamFaceAView:
    """
    Renders Face A (Question Paper Architect) inside the main desktop application.
    """

    def __init__(self, parent_tab, app_controller):
        self.tab = parent_tab
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

        self.active_spec: Optional[Dict[str, Any]] = None
        self.active_paper: Optional[Dict[str, Any]] = None

        # Variables
        self.selected_subject_var = tk.StringVar(value="Mathematics")
        self.grounding_source_var = tk.StringVar(value="blueprint")
        self.active_vault_filename_var = tk.StringVar(value="(Checking vault...)")
        self.active_sample_q_var = tk.StringVar(value="(Checking sample papers...)")
        self.time_slider_var = tk.IntVar(value=15)
        self.active_preset_var = tk.StringVar(value="express_10m")

    def build_ui(self):
        """Builds the split-screen Face A interface."""
        # Top Container
        self.main_container = tk.Frame(self.tab, bg=self.colors["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        # Split Layout: Left Control Deck (360px), Right Live Preview (Expand)
        self.left_deck = tk.Frame(self.main_container, bg=self.colors["card_bg"], width=360, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground=self.colors["border"])
        self.left_deck.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.left_deck.pack_propagate(False)

        self.right_preview = tk.Frame(self.main_container, bg=self.colors["card_bg"], relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground=self.colors["border"])
        self.right_preview.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_left_control_deck()
        self._build_right_preview_studio()

        # Trigger initial time breakdown calculation and vault status
        self._on_time_slider_changed(self.time_slider_var.get())
        self._refresh_vault_status_for_subject()

    def _build_left_control_deck(self):
        """Constructs the left command controls."""
        panel = self.left_deck
        from host_exam_ui import CustomDarkScrollbar

        canvas = tk.Canvas(panel, bg=self.colors["card_bg"], highlightthickness=0, bd=0)
        scrollbar = CustomDarkScrollbar(panel, target_widget=canvas, width=6, bg="#0b1120", thumb_color="#334155")
        content = tk.Frame(canvas, bg=self.colors["card_bg"])

        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        win_id = canvas.create_window((0, 0), window=content, anchor="nw", width=346)

        def _on_canvas_cfg(e):
            if e.width > 50:
                canvas.itemconfig(win_id, width=e.width - 8)
        canvas.bind("<Configure>", _on_canvas_cfg)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        deck = content

        # Section Header
        hdr = tk.Label(
            deck,
            text="⚙️ QUESTION PAPER ARCHITECT",
            font=("Segoe UI", 9, "bold"),
            fg="#f97316",
            bg=self.colors["card_bg"],
            anchor="w"
        )
        hdr.pack(fill=tk.X, padx=12, pady=(4, 2))

        # 1. Academic Lifecycle Mode Pill
        mode, ctx = ExamLifecycleController.detect_academic_mode()
        mode_label_map = {
            "balanced_daily": "🟢 Balanced Daily (6:45 AM Alert Active)",
            "pre_exam_planner": "🟠 Pre-Exam Planner Season",
            "exam_eve_sprint": "🔥 Exam Eve Sprint (Model Rehearsal)"
        }
        lbl_mode = tk.Label(
            deck,
            text=mode_label_map.get(mode, "🟢 Balanced Daily Routine"),
            font=("Segoe UI", 8, "bold"),
            fg="#34d399",
            bg="#161f30",
            relief=tk.SOLID,
            bd=1,
            padx=6,
            pady=2
        )
        lbl_mode.pack(fill=tk.X, padx=12, pady=(0, 3))

        # 2. Subject Selector (All 7 Master Subjects)
        lbl_subj = tk.Label(deck, text="1. SELECT CBSE SUBJECT:", font=("Segoe UI", 8, "bold"), fg=self.colors["text"], bg=self.colors["card_bg"], anchor="w")
        lbl_subj.pack(fill=tk.X, padx=12, pady=(1, 1))

        subjects = SubjectCatalog.get_all_subject_names()
        self.combo_subject = ttk.Combobox(
            deck,
            textvariable=self.selected_subject_var,
            values=subjects,
            state="readonly",
            font=("Segoe UI", 8)
        )
        self.combo_subject.pack(fill=tk.X, padx=12, pady=(0, 3))
        self.combo_subject.bind("<<ComboboxSelected>>", lambda e: self._on_subject_changed())

        # 3. Grounding Source Radio
        lbl_src = tk.Label(deck, text="2. QUESTION GROUNDING SOURCE:", font=("Segoe UI", 8, "bold"), fg=self.colors["text"], bg=self.colors["card_bg"], anchor="w")
        lbl_src.pack(fill=tk.X, padx=12, pady=(1, 1))

        rb_row = tk.Frame(deck, bg=self.colors["card_bg"])
        rb_row.pack(fill=tk.X, padx=12, pady=(0, 2))

        rb1 = tk.Radiobutton(
            rb_row,
            text="Curriculum Blueprint",
            variable=self.grounding_source_var,
            value="blueprint",
            font=("Segoe UI", 8),
            fg="#e2e8f0",
            bg=self.colors["card_bg"],
            selectcolor="#0f172a",
            activebackground=self.colors["card_bg"]
        )
        rb1.pack(side=tk.LEFT, padx=(0, 6))

        rb2 = tk.Radiobutton(
            rb_row,
            text="Uploaded School PDF",
            variable=self.grounding_source_var,
            value="pdf",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg=self.colors["card_bg"],
            selectcolor="#0f172a",
            activebackground=self.colors["card_bg"]
        )
        rb2.pack(side=tk.LEFT)

        # Vault Control Strip (Session 7 Smart Ingestion Wizard)
        vault_box = tk.Frame(deck, bg="#161f30", padx=6, pady=3, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground=self.colors["border"])
        vault_box.pack(fill=tk.X, padx=12, pady=(0, 3))

        v_top = tk.Frame(vault_box, bg="#161f30")
        v_top.pack(fill=tk.X)

        self.btn_open_vault_menu = tk.Button(
            v_top,
            text="📚 Textbook Vault ↗",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#f97316",
            activebackground="#ea580c",
            relief=tk.FLAT,
            padx=4,
            pady=2,
            cursor="hand2",
            command=self._go_to_dedicated_vault_menu
        )
        self.btn_open_vault_menu.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))

        self.btn_open_sample_q = tk.Button(
            v_top,
            text="📑 Sample Qs Vault ↗",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#9333ea",
            activebackground="#7e22ce",
            relief=tk.FLAT,
            padx=4,
            pady=2,
            cursor="hand2",
            command=self._go_to_sample_q_menu
        )
        self.btn_open_sample_q.pack(side=tk.RIGHT, expand=True, fill=tk.X)

        self.lbl_vault_active = tk.Label(
            vault_box,
            textvariable=self.active_vault_filename_var,
            font=("Consolas", 7),
            fg="#34d399",
            bg="#161f30",
            anchor="w",
            wraplength=310,
            justify=tk.LEFT
        )
        self.lbl_vault_active.pack(fill=tk.X, pady=(2, 0))

        self.lbl_sample_q_active = tk.Label(
            vault_box,
            textvariable=self.active_sample_q_var,
            font=("Consolas", 7),
            fg="#c084fc",
            bg="#161f30",
            anchor="w",
            wraplength=310,
            justify=tk.LEFT
        )
        self.lbl_sample_q_active.pack(fill=tk.X, pady=(1, 0))

        # 4. Smart Time & Intensity Dial
        lbl_dial = tk.Label(deck, text="3. SMART TIME & INTENSITY DIAL:", font=("Segoe UI", 8, "bold"), fg=self.colors["text"], bg=self.colors["card_bg"], anchor="w")
        lbl_dial.pack(fill=tk.X, padx=12, pady=(1, 1))

        # Method 1: Quick Preset Chips
        chips_frame = tk.Frame(deck, bg=self.colors["card_bg"])
        chips_frame.pack(fill=tk.X, padx=12, pady=(0, 2))

        presets = [("🏃 5m", 5), ("⚡ 10m", 10), ("🎯 20m", 20), ("🏆 35m", 35)]
        for label, mins in presets:
            btn = tk.Button(
                chips_frame,
                text=label,
                font=("Segoe UI", 8, "bold"),
                fg="#f8fafc",
                bg="#334155",
                activebackground="#f97316",
                relief=tk.FLAT,
                bd=0,
                padx=4,
                pady=2,
                cursor="hand2",
                command=lambda m=mins: self._on_preset_chip_clicked(m)
            )
            btn.pack(side=tk.LEFT, padx=(0, 3), expand=True, fill=tk.X)

        # Method 2: Precision Slider
        slider_frame = tk.Frame(deck, bg=self.colors["card_bg"])
        slider_frame.pack(fill=tk.X, padx=12, pady=(0, 2))

        self.slider = tk.Scale(
            slider_frame,
            from_=5,
            to=50,
            orient=tk.HORIZONTAL,
            variable=self.time_slider_var,
            bg=self.colors["card_bg"],
            fg="#38bdf8",
            highlightthickness=0,
            troughcolor="#0f172a",
            command=self._on_time_slider_changed
        )
        self.slider.pack(fill=tk.X)

        # Method 3: Live Synchronized Breakdown Preview Box
        self.lbl_breakdown = tk.Label(
            deck,
            text="4 Questions (8 Marks) • Est. Time: 10 Mins\nBreakdown: 2 MCQs + 2 VSA (Zero Long Essays)",
            font=("Segoe UI", 7),
            fg="#fbbf24",
            bg="#161f30",
            relief=tk.SOLID,
            bd=1,
            padx=6,
            pady=3,
            justify=tk.LEFT
        )
        self.lbl_breakdown.pack(fill=tk.X, padx=12, pady=(0, 4))

        # 5. Primary Generate Button
        self.btn_generate = tk.Button(
            deck,
            text="⚡ GENERATE CBSE QUESTION PAPER",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#ef4444",
            activebackground="#dc2626",
            relief=tk.FLAT,
            bd=0,
            pady=5,
            cursor="hand2",
            command=self._on_generate_clicked
        )
        self.btn_generate.pack(fill=tk.X, padx=12, pady=(0, 4))

        # 6. One-Click "No Homework Today" Weak-Subject Healer Button
        self.btn_no_hw = tk.Button(
            deck,
            text="🏖️ No Homework Today (Heal Weak Spots)",
            font=("Segoe UI", 8, "bold"),
            fg="#34d399",
            bg="#161f30",
            activebackground="#065f46",
            relief=tk.SOLID,
            bd=1,
            pady=4,
            cursor="hand2",
            command=self._on_no_homework_clicked
        )
        self.btn_no_hw.pack(fill=tk.X, padx=12, pady=(0, 4))

    def _build_right_preview_studio(self):
        """Constructs the right-hand live preview studio."""
        preview = self.right_preview

        # Studio Header & Toolbar
        bar = tk.Frame(preview, bg="#161f30", padx=14, pady=8)
        bar.pack(fill=tk.X)

        lbl_title = tk.Label(bar, text="📄 LIVE PRINT STUDIO PREVIEW", font=("Segoe UI", 9, "bold"), fg="#38bdf8", bg="#161f30")
        lbl_title.pack(side=tk.LEFT)

        # Action Buttons
        self.btn_print_web = tk.Button(
            bar,
            text="🖨️ Print / Web",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#0284c7",
            activebackground="#0369a1",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2",
            command=self._open_web_preview
        )
        self.btn_print_web.pack(side=tk.RIGHT, padx=(4, 0))

        self.btn_export_pdf = tk.Button(
            bar,
            text="📄 Export PDF",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#16a34a",
            activebackground="#15803d",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2",
            command=self._open_qp_pdf
        )
        self.btn_export_pdf.pack(side=tk.RIGHT, padx=(4, 0))

        self.btn_blank_booklet = tk.Button(
            bar,
            text="📝 Blank Booklet",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#f97316",
            activebackground="#ea580c",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2",
            command=self._open_blank_booklet
        )
        self.btn_blank_booklet.pack(side=tk.RIGHT, padx=(4, 0))

        # Preview Scrollable Text View
        from host_exam_ui import CustomDarkScrollbar
        self.preview_text = tk.Text(
            preview,
            bg="#090d16",
            fg="#f8fafc",
            insertbackground="#38bdf8",
            font=("Consolas", 9),
            wrap=tk.WORD,
            padx=14,
            pady=12,
            relief=tk.FLAT,
            bd=0
        )
        scrollbar_p = CustomDarkScrollbar(preview, target_widget=self.preview_text, width=6, bg="#0b1120", thumb_color="#334155")
        scrollbar_p.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._render_placeholder_in_preview()

    def _render_placeholder_in_preview(self):
        """Displays initial welcome guidance in the preview window."""
        self.preview_text.configure(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)

        msg = (
            "========================================================================================\n"
            "                               THARUN REVISION BANNER                                  \n"
            "                 CLASS 8 CBSE • DAILY RETENTION & HOST EXAMINATION ENGINE               \n"
            "========================================================================================\n\n"
            "  Student Name   : Tharun\n"
            "  Class Standard : Class 8 CBSE (Senthil Public School)\n"
            "  Ready Subjects : Mathematics, Physical Science, Biology, Social Science, English, Hindi, Tamil\n\n"
            "  HOW TO USE FACE A:\n"
            "  1. Select any subject from the dropdown on the left.\n"
            "  2. Choose your time pace via the Smart Time Dial (5m Rapid, 10m Express, 20m Standard).\n"
            "  3. Click [ ⚡ GENERATE CBSE QUESTION PAPER ] to generate questions in real-time.\n"
            "  4. Click [ 🖨️ Print / Web ] or [ 📝 Blank Booklet ] to print classroom-ready copies.\n\n"
            "========================================================================================\n"
        )
        self.preview_text.insert(tk.END, msg)
        self.preview_text.configure(state=tk.DISABLED)

    def _on_time_slider_changed(self, val):
        """Updates question breakdown when the slider moves."""
        mins = int(val)
        subj = self.selected_subject_var.get()
        cfg = SmartTimeIntensityDial.calculate_breakdown_for_minutes(subj, mins)
        b = cfg["breakdown"]

        txt = (
            f"{cfg['summary_text']}\n"
            f"Breakdown: {b['mcq_count']} MCQs + {b['vsa_count']} VSA(2M) + {b['sa_count']} SA(3M) + {b['la_count']} LA"
        )
        self.lbl_breakdown.configure(text=txt)

    def _on_preset_chip_clicked(self, mins: int):
        """Quickly snaps slider to preset minutes."""
        self.time_slider_var.set(mins)
        self._on_time_slider_changed(mins)

    def _on_subject_changed(self):
        """Updates breakdown and vault status when subject changes."""
        self._on_time_slider_changed(self.time_slider_var.get())
        self._refresh_vault_status_for_subject()

    def _open_ingestion_wizard(self):
        """Opens the Smart Ingestion Wizard modal."""
        SmartIngestionDialog(
            parent=self.tab,
            default_subject=self.selected_subject_var.get(),
            on_success_callback=self._on_material_ingested
        )

    def _open_subject_vault_folder(self):
        """Opens the OS directory of the currently selected subject vault."""
        subj = self.selected_subject_var.get()
        folder_name = SmartIngestionWizard.SUBJECT_FOLDER_MAP.get(subj, "01_Mathematics")
        folder_path = os.path.join(EXAM_SYSTEM_DIR, "02_UPLOADED_TEXTBOOKS_PDF", folder_name)
        os.makedirs(folder_path, exist_ok=True)
        try:
            os.startfile(folder_path)
        except Exception:
            messagebox.showinfo("Vault Folder", f"Subject Vault Location:\n{folder_path}")

    def _on_material_ingested(self, record: Dict[str, Any]):
        """Callback when a new file is ingested via the wizard."""
        self.grounding_source_var.set("pdf")
        self._refresh_vault_status_for_subject()

    def _refresh_vault_status_for_subject(self):
        """Refreshes active textbook and sample question labels for the selected subject."""
        subj = self.selected_subject_var.get()
        active = SmartIngestionWizard.get_active_material(subj)
        if active:
            fname = active.get("canonical_filename", "")
            mtype = active.get("material_type", "")
            pages = active.get("total_pages", 1)
            self.active_vault_filename_var.set(f"Textbook [{mtype} • {pages}p]:\n{fname}")
        else:
            self.active_vault_filename_var.set("(No Textbook in vault)")

        active_smp = SampleQuestionsEngine.get_active_style_reference(subj)
        if active_smp:
            fname = active_smp.get("canonical_filename", "")
            self.active_sample_q_var.set(f"School Sample Pattern:\n{fname}")
        else:
            self.active_sample_q_var.set("(No School Sample Paper - standard CBSE)")

    def _go_to_dedicated_vault_menu(self):
        """Switches to the dedicated Textbook Vault menu."""
        if hasattr(self.app, "switch_subview"):
            self.app.switch_subview("vault")
        else:
            self._open_ingestion_wizard()

    def _go_to_sample_q_menu(self):
        """Switches to the dedicated Sample Questions menu."""
        if hasattr(self.app, "switch_subview"):
            self.app.switch_subview("sample_q")

    def _on_generate_clicked(self):
        """Generates the question paper using Gemini AI and Print Studio."""
        subj = self.selected_subject_var.get()
        target_mins = self.time_slider_var.get()

        # Disable button temporarily
        self.btn_generate.configure(state=tk.DISABLED, text="⏳ Generating Question Paper...")
        self.tab.update_idletasks()

        def worker():
            try:
                # 1. Assemble Blueprint Spec
                portions = DiaryGroundTruth.get_portions_for_subject(subj)
                spec = ExamSpecAssembler.assemble_individual_paper_spec(
                    subject=subj,
                    mode="balanced_daily",
                    exam_type="daily_recall",
                    exam_date=datetime.now().strftime("%Y-%m-%d"),
                    topics=portions
                )

                # Grounding Source: Check if Grounded in Uploaded School PDF
                grounding_mode = self.grounding_source_var.get()
                if grounding_mode == "pdf":
                    active_mat = SmartIngestionWizard.get_active_material(subj)
                    if active_mat:
                        extracted_txt = SmartIngestionWizard.extract_text_from_material(active_mat, max_pages=6)
                        spec["grounding_content"] = extracted_txt
                        spec["grounding_type"] = active_mat.get("material_type", "topic_photocopy")
                        spec["grounding_filename"] = active_mat.get("canonical_filename", "")
                        spec["exam_title"] = f"{subj} Examination [Grounded in {active_mat.get('canonical_filename', '')}]"

                # Also check active sample question pattern to emulate school teacher style
                active_smp = SampleQuestionsEngine.get_active_style_reference(subj)
                if active_smp:
                    sample_txt = SampleQuestionsEngine.extract_text_from_sample_paper(active_smp, max_pages=4)
                    spec["sample_question_reference"] = sample_txt
                    spec["sample_question_filename"] = active_smp.get("canonical_filename", "")

                # 2. Call Gemini Question Architect with Time Dial
                paper = GeminiQuestionArchitect.generate_question_paper(
                    spec=spec,
                    custom_time_mins=target_mins
                )

                self.active_spec = spec
                self.active_paper = paper

                # 3. Compile Print Studio Documents
                exam_id = paper["metadata"]["exam_id"]
                qp_pdf = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}.pdf")
                ans_pdf = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}_BLANK_ANSWER_SHEET.pdf")
                html_path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}.html")

                ExamPrintStudio.render_question_paper_pdf(paper, qp_pdf)
                ExamPrintStudio.render_blank_answer_sheet_pdf(paper, ans_pdf)
                html_content = ExamPrintStudio.render_question_paper_html(paper)
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                json_path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(paper, f, indent=2, ensure_ascii=False)

                # Update UI on main thread
                self.tab.after(0, lambda: self._on_generation_success(paper))

            except Exception as e:
                self.tab.after(0, lambda: self._on_generation_error(str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_generation_success(self, paper: Dict[str, Any]):
        """Renders the generated paper text into the preview window."""
        self.btn_generate.configure(state=tk.NORMAL, text="⚡ GENERATE CBSE QUESTION PAPER")
        self.preview_text.configure(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)

        meta = paper["metadata"]
        lines = []
        lines.append("=" * 88)
        lines.append("                               THARUN REVISION BANNER                                  ")
        lines.append(f"               {meta.get('exam_title', 'CBSE EXAMINATION').upper()}                    ")
        lines.append("=" * 88)
        lines.append(f" Student: Tharun | Class: Class 8 CBSE | Subject: {meta.get('subject')} | Mode: {meta.get('generation_mode')}")
        lines.append(f" Time Allowed: {meta.get('time_allowed_mins')} Mins | Max Marks: {meta.get('max_marks')} Marks | Exam ID: {meta.get('exam_id')}")
        lines.append("-" * 88)

        for sec in paper.get("sections", []):
            s_name = sec.get("section_name", "SECTION")
            s_marks = sec.get("allocated_marks", "")
            lines.append(f"\n >>> {s_name.upper()} ({s_marks} Marks) <<< \n")

            for q in sec.get("questions", []):
                q_num = q.get("question_number", "Q.")
                q_m = q.get("marks", 1)
                q_txt = q.get("question_text", "")
                lines.append(f" {q_num} [{q_m}M]  {q_txt}")
                for opt in q.get("options", []):
                    lines.append(f"       {opt}")
                lines.append("")

        lines.append("=" * 88)
        lines.append("  [ 🖨️ Click 'Print / Web' for HTML Preview ]  [ 📄 Click 'Export PDF' for Vector PDF ]  ")
        lines.append("=" * 88)

        self.preview_text.insert(tk.END, "\n".join(lines))
        self.preview_text.configure(state=tk.DISABLED)
        if not getattr(self, "suppress_modal", False):
            messagebox.showinfo("Exam Paper Ready", f"Successfully generated CBSE Question Paper for {meta.get('subject')}!")

    def _on_generation_error(self, err_msg: str):
        self.btn_generate.configure(state=tk.NORMAL, text="⚡ GENERATE CBSE QUESTION PAPER")
        if not getattr(self, "suppress_modal", False):
            messagebox.showerror("Generation Error", f"Failed to generate question paper:\n{err_msg}")
        print(f"[Face A] Generation Error: {err_msg}")

    def generate_paper_sync(self) -> Dict[str, Any]:
        """Synchronously executes question paper generation (for deterministic execution & testing)."""
        subj = self.selected_subject_var.get()
        target_mins = self.time_slider_var.get()
        portions = DiaryGroundTruth.get_portions_for_subject(subj)
        spec = ExamSpecAssembler.assemble_individual_paper_spec(
            subject=subj,
            mode="balanced_daily",
            exam_type="daily_recall",
            exam_date=datetime.now().strftime("%Y-%m-%d"),
            topics=portions
        )
        grounding_mode = self.grounding_source_var.get()
        if grounding_mode == "pdf":
            active_mat = SmartIngestionWizard.get_active_material(subj)
            if active_mat:
                extracted_txt = SmartIngestionWizard.extract_text_from_material(active_mat, max_pages=6)
                spec["grounding_content"] = extracted_txt
                spec["grounding_type"] = active_mat.get("material_type", "topic_photocopy")
                spec["grounding_filename"] = active_mat.get("canonical_filename", "")
                spec["exam_title"] = f"{subj} Examination [Grounded in {active_mat.get('canonical_filename', '')}]"

        active_smp = SampleQuestionsEngine.get_active_style_reference(subj)
        if active_smp:
            sample_txt = SampleQuestionsEngine.extract_text_from_sample_paper(active_smp, max_pages=4)
            spec["sample_question_reference"] = sample_txt
            spec["sample_question_filename"] = active_smp.get("canonical_filename", "")

        paper = GeminiQuestionArchitect.generate_question_paper(
            spec=spec,
            custom_time_mins=target_mins
        )
        self.active_spec = spec
        self.active_paper = paper

        exam_id = paper["metadata"]["exam_id"]
        qp_pdf = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}.pdf")
        ans_pdf = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}_BLANK_ANSWER_SHEET.pdf")
        html_path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}.html")

        ExamPrintStudio.render_question_paper_pdf(paper, qp_pdf)
        ExamPrintStudio.render_blank_answer_sheet_pdf(paper, ans_pdf)
        html_content = ExamPrintStudio.render_question_paper_html(paper)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        json_path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(paper, f, indent=2, ensure_ascii=False)

        self._on_generation_success(paper)
        return paper

    def _on_no_homework_clicked(self):
        """Handles the 'No Homework Today' weak-subject healer modal."""
        ranked = WeakSubjectHealingEngine.analyze_weak_subjects()
        if not ranked:
            messagebox.showinfo("Error Bank Clean", "No past errors found in Error Bank! All subjects are healthy.")
            return

        top_subjs = [f"{r['subject']} ({r['total_errors']} errors - {', '.join(r['focus_categories'][:2])})" for r in ranked[:4]]
        prompt_txt = "Tharun has no school homework today!\nChoose a weak subject to level up tonight and test tomorrow morning:\n\n"
        for idx, s in enumerate(top_subjs, 1):
            prompt_txt += f" {idx}. {s}\n"
        prompt_txt += "\nEnter Subject Name to Focus on:"

        chosen = simpledialog.askstring("No Homework Day - Weak Subject Healer", prompt_txt, initialvalue=ranked[0]["subject"])
        if chosen:
            res = WeakSubjectHealingEngine.mark_no_homework_day(
                date_str=datetime.now().strftime("%Y-%m-%d"),
                chosen_weak_subject=chosen.strip(),
                student_notes="Evening error bank revision"
            )
            if res["success"]:
                messagebox.showinfo(
                    "Weak Subject Scheduled",
                    f"🎯 Scheduled {chosen} for evening healing!\n"
                    f"Tomorrow's 6:45 AM test will target these weak categories:\n"
                    f"{', '.join(res['record']['focus_areas'])}"
                )
                self.selected_subject_var.set(chosen.strip())
                self._on_subject_changed()

    def _open_web_preview(self):
        if not self.active_paper:
            messagebox.showinfo("No Paper", "Please generate a question paper first.")
            return
        exam_id = self.active_paper["metadata"]["exam_id"]
        path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}.html")
        if os.path.exists(path):
            webbrowser.open(f"file:///{path}")

    def _open_qp_pdf(self):
        if not self.active_paper:
            messagebox.showinfo("No Paper", "Please generate a question paper first.")
            return
        exam_id = self.active_paper["metadata"]["exam_id"]
        path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}.pdf")
        if os.path.exists(path):
            os.startfile(path)

    def _open_blank_booklet(self):
        if not self.active_paper:
            messagebox.showinfo("No Paper", "Please generate a question paper first.")
            return
        exam_id = self.active_paper["metadata"]["exam_id"]
        path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", f"{exam_id}_BLANK_ANSWER_SHEET.pdf")
        if os.path.exists(path):
            os.startfile(path)


# ==============================================================================
# VERIFICATION RUNNER
# ==============================================================================
def run_face_a_ui_verification():
    """Headless sanity check of Face A UI Controller."""
    root = tk.Tk()
    root.withdraw()
    tab = tk.Frame(root)
    app_mock = type("AppMock", (), {"colors": {"bg": "#0f172a", "card_bg": "#1e293b", "border": "#334155", "accent": "#f97316", "text": "#f8fafc", "subtext": "#94a3b8"}})()

    view = HostExamFaceAView(tab, app_mock)
    view.build_ui()
    print("=" * 75)
    print("   ✅ SESSION 6: FACE A UI CONTROLLER INITIALIZED CLEANLY!")
    print(f" -> Active Subject Dropdown: {view.selected_subject_var.get()}")
    print(f" -> Time Slider Initialized: {view.time_slider_var.get()} Mins")
    print(f" -> Live Breakdown Text:     {view.lbl_breakdown.cget('text').split(chr(10))[0]}")
    print("=" * 75)
    root.destroy()


if __name__ == "__main__":
    run_face_a_ui_verification()
