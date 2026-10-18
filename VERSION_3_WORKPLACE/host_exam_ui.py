"""
host_exam_ui.py - Host Examination & Gemini AI CBSE Evaluator UI Controller (V3)
Integrates with ScholasticPulse Version 3 Desktop Application (study_balancer.py).

Features:
- Sub-View 1: Subject Study Ledger & 3-Phase Host Examination Selector (Weekly/Month-End, 3-Day, Morning Sprint)
- Sub-View 2: Face A - Question Paper Architect & Print Studio (Specified PDF vs. General CBSE)
- Sub-View 3: Face B - Answer Sheet Uploader & Corrected Soft Copy Viewer (Step-wise step marking, red-ink annotations, anti-daydreaming audit)
- Sub-View 4: CBSE Topper Model Answer Guide (P-E-E-D protocol, comparative analysis)
- Gemini API Key & Class setting widget (Connected to Gemini AI status)
"""

import os
import sys
import json
import threading
import subprocess
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import datetime
from typing import Dict, Any, List, Optional

import exam_engine_v3
from exam_engine_v3 import (
    SubjectStudyLedger,
    ExamPhaseAssembler,
    GeminiExamClient,
    EXAM_SYSTEM_DIR,
    SKILLS_DIR,
    HOMEWORK_LOGS_DIR,
    TEXTBOOKS_PDF_DIR,
    QUESTION_PAPERS_DIR,
    ANSWER_SHEETS_DIR,
    CORRECTED_COPIES_DIR,
    MODEL_ANSWERS_DIR,
)

class HostExamTabController:
    """Controller for the 'Host Exam & Gemini Evaluator (V3)' Tab in ScholasticPulse Desktop."""

    def __init__(self, app, tab_frame: tk.Frame):
        self.app = app
        self.parent = tab_frame
        self.colors = app.colors

        # State
        self.active_subview = "ledger"  # "ledger", "face_a", "face_b", "topper"
        self.active_question_paper: Optional[Dict[str, Any]] = None
        self.active_evaluation: Optional[Dict[str, Any]] = None
        self.active_exam_id: str = ""
        self.uploaded_answer_files: List[str] = []

        # Auto-sync ledger on init
        try:
            SubjectStudyLedger.auto_sync_from_diary_and_portions()
        except Exception as e:
            print(f"[HostExamTabController] Warning during ledger auto-sync: {e}")

    def build_ui(self):
        """Construct the entire Host Examination UI inside the tab frame."""
        for w in self.parent.winfo_children():
            w.destroy()

        pad = tk.Frame(self.parent, bg=self.colors["bg"], padx=12, pady=8)
        pad.pack(fill=tk.BOTH, expand=True)
        self.pad = pad

        # 1. Top Command Deck
        self._build_top_command_deck(pad)

        # 2. Sub-View Navigation Bar
        self._build_subview_navigation_bar(pad)

        # 3. Main Dynamic Sub-View Container
        self.subview_container = tk.Frame(pad, bg=self.colors["bg"])
        self.subview_container.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

        # Show initial subview
        self.switch_subview("ledger")

    # ==========================================
    # 1. TOP COMMAND DECK & STATUS BAR
    # ==========================================
    def _build_top_command_deck(self, parent):
        deck = tk.Frame(
            parent,
            bg="#0e172a",
            bd=1,
            relief=tk.SOLID,
            highlightbackground="#d4af5a",
            highlightthickness=1,
            padx=14,
            pady=8
        )
        deck.pack(fill=tk.X, pady=(0, 6))

        # Top row: Title + Status Indicators
        top_row = tk.Frame(deck, bg="#0e172a")
        top_row.pack(fill=tk.X)

        # Title Block
        t_box = tk.Frame(top_row, bg="#0e172a")
        t_box.pack(side=tk.LEFT)

        lbl_title = tk.Label(
            t_box,
            text="🎯  HOST EXAMINATION & GEMINI EVALUATOR (V3)",
            font=("Segoe UI", 12, "bold"),
            fg="#f8fafc",
            bg="#0e172a"
        )
        lbl_title.pack(anchor="w")

        lbl_sub = tk.Label(
            t_box,
            text="Anti-Daydreaming Verification Engine • Class 8 CBSE (Senthil Public School) • Direct Gemini AI Link",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#0e172a"
        )
        lbl_sub.pack(anchor="w")

        # Status & Action Buttons on Right
        actions_box = tk.Frame(top_row, bg="#0e172a")
        actions_box.pack(side=tk.RIGHT)

        # Class Badge
        cfg = GeminiExamClient.load_config()
        current_class = cfg.get("class_level", "Class 8 CBSE")
        self.btn_class_badge = tk.Button(
            actions_box,
            text=f"🏫 {current_class}",
            font=("Segoe UI", 8, "bold"),
            fg="#38bdf8",
            bg="#161f30",
            activeforeground="#ffffff",
            activebackground="#0284c7",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._on_change_class_level
        )
        self.btn_class_badge.pack(side=tk.LEFT, padx=(0, 6))

        # Gemini Connection Status Badge
        self.lbl_gemini_status = tk.Label(
            actions_box,
            text=self._get_gemini_status_text(),
            font=("Segoe UI", 8, "bold"),
            fg=self._get_gemini_status_color(),
            bg="#161f30",
            padx=8,
            pady=4,
            relief=tk.SOLID,
            bd=1
        )
        self.lbl_gemini_status.pack(side=tk.LEFT, padx=(0, 6))

        # Set API Key Button
        btn_key = tk.Button(
            actions_box,
            text="🔑 Gemini API Key",
            font=("Segoe UI", 8, "bold"),
            fg="#fbbf24",
            bg="#1e293b",
            activeforeground="#ffffff",
            activebackground="#d97706",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._open_api_key_modal
        )
        btn_key.pack(side=tk.LEFT, padx=(0, 6))

        # Sync Ledger Button
        btn_sync = tk.Button(
            actions_box,
            text="🔄 Sync Ledger",
            font=("Segoe UI", 8, "bold"),
            fg="#34d399",
            bg="#1e293b",
            activeforeground="#ffffff",
            activebackground="#059669",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._on_sync_ledger
        )
        btn_sync.pack(side=tk.LEFT, padx=(0, 6))

        # Open Exam Directory Button
        btn_folder = tk.Button(
            actions_box,
            text="📂 Exam Folder",
            font=("Segoe UI", 8),
            fg="#cbd5e1",
            bg="#1e293b",
            activeforeground="#ffffff",
            activebackground="#334155",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._open_exam_folder
        )
        btn_folder.pack(side=tk.LEFT)

    def _get_gemini_status_text(self) -> str:
        cfg = GeminiExamClient.load_config()
        key = cfg.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY", "")
        if key.strip():
            return "🟢 Gemini AI Active"
        return "⚪ Offline Local Mode"

    def _get_gemini_status_color(self) -> str:
        cfg = GeminiExamClient.load_config()
        key = cfg.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY", "")
        if key.strip():
            return "#34d399"  # Emerald
        return "#94a3b8"  # Slate

    def _open_api_key_modal(self):
        cfg = GeminiExamClient.load_config()
        current_key = cfg.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY", "")
        
        prompt_txt = (
            "Enter Google Gemini API Key:\n\n"
            "(If left blank, ScholasticPulse V3 will use the robust offline deterministic CBSE evaluator.\n"
            "Entering an API key enables direct Gemini 2.5 AI grading and dynamic question paper creation)."
        )
        new_key = simpledialog.askstring("Gemini API Key Configuration", prompt_txt, initialvalue=current_key)
        if new_key is not None:
            GeminiExamClient.set_api_key(new_key.strip())
            self.lbl_gemini_status.configure(
                text=self._get_gemini_status_text(),
                fg=self._get_gemini_status_color()
            )
            messagebox.showinfo("Gemini API Key Saved", "Gemini API key updated and stored securely in local configuration.")

    def _on_change_class_level(self):
        cfg = GeminiExamClient.load_config()
        curr = cfg.get("class_level", "Class 8 CBSE")
        new_class = simpledialog.askstring(
            "Target Class Level",
            "Enter Student Class Level (e.g., 'Class 8 CBSE', 'Class 9 CBSE', 'Class 10 CBSE'):",
            initialvalue=curr
        )
        if new_class and new_class.strip():
            cfg["class_level"] = new_class.strip()
            GeminiExamClient.save_config(cfg)
            self.btn_class_badge.configure(text=f"🏫 {new_class.strip()}")
            messagebox.showinfo("Class Updated", f"Target student class updated to: {new_class.strip()}")

    def _on_sync_ledger(self):
        try:
            res = SubjectStudyLedger.auto_sync_from_diary_and_portions()
            entries = res.get("entries", [])
            messagebox.showinfo("Ledger Synced", f"Successfully synced Subject Study Ledger!\nTotal entries logged: {len(entries)}")
            if self.active_subview == "ledger":
                self._render_ledger_table()
        except Exception as e:
            messagebox.showerror("Sync Error", f"Failed to sync study ledger: {e}")

    def _open_exam_folder(self):
        try:
            if sys.platform == "win32":
                os.startfile(EXAM_SYSTEM_DIR)
            else:
                subprocess.Popen(["xdg-open", EXAM_SYSTEM_DIR])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open exam folder: {e}")

    # ==========================================
    # 2. SUB-VIEW NAVIGATION BAR
    # ==========================================
    def _build_subview_navigation_bar(self, parent):
        bar = tk.Frame(parent, bg="#131c2e", height=38)
        bar.pack(fill=tk.X, pady=(0, 6))
        self.subview_nav_bar = bar

        self.subview_buttons = {}
        tabs = [
            ("ledger", "📋 1. Study Ledger & 3-Phase Selector"),
            ("face_a", "📝 2. Face A: Question Paper Architect"),
            ("face_b", "🔍 3. Face B: Answer Sheet Evaluator"),
            ("topper", "⭐ 4. CBSE Topper Model Answer Guide")
        ]

        for key, label in tabs:
            btn = tk.Button(
                bar,
                text=label,
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT,
                bd=0,
                padx=12,
                pady=6,
                cursor="hand2",
                command=lambda k=key: self.switch_subview(k)
            )
            btn.pack(side=tk.LEFT, padx=(0, 4))
            self.subview_buttons[key] = btn

        self._update_subview_tab_styles()

    def _update_subview_tab_styles(self):
        for k, btn in self.subview_buttons.items():
            if k == self.active_subview:
                btn.configure(
                    bg="#f59e0b",
                    fg="#0f172a",
                    activebackground="#d97706",
                    activeforeground="#0f172a"
                )
            else:
                btn.configure(
                    bg="#1e293b",
                    fg="#94a3b8",
                    activebackground="#334155",
                    activeforeground="#f8fafc"
                )

    def switch_subview(self, subview_key: str):
        self.active_subview = subview_key
        self._update_subview_tab_styles()

        for w in self.subview_container.winfo_children():
            w.destroy()

        if subview_key == "ledger":
            self._render_subview_ledger(self.subview_container)
        elif subview_key == "face_a":
            self._render_subview_face_a(self.subview_container)
        elif subview_key == "face_b":
            self._render_subview_face_b(self.subview_container)
        elif subview_key == "topper":
            self._render_subview_topper(self.subview_container)

    # ==========================================
    # SUB-VIEW 1: STUDY LEDGER & 3-PHASE SELECTOR
    # ==========================================
    def _render_subview_ledger(self, parent):
        pane = tk.PanedWindow(parent, orient=tk.VERTICAL, bg=self.colors["bg"], sashrelief=tk.FLAT)
        pane.pack(fill=tk.BOTH, expand=True)

        # Top section: 3-Phase Host Examination Selector Cards
        phase_frame = tk.Frame(pane, bg="#0e172a", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1, padx=10, pady=8)
        pane.add(phase_frame, minsize=140)

        lbl_phase_title = tk.Label(
            phase_frame,
            text="⚡ SELECT HOST EXAMINATION PHASE (TRIGGER REAL LEARNING VERIFICATION)",
            font=("Segoe UI", 9, "bold"),
            fg="#f59e0b",
            bg="#0e172a"
        )
        lbl_phase_title.pack(anchor="w", pady=(0, 6))

        cards_row = tk.Frame(phase_frame, bg="#0e172a")
        cards_row.pack(fill=tk.X)

        # Phase 1 Card
        c1 = tk.Frame(cards_row, bg="#161f30", bd=1, relief=tk.SOLID, highlightbackground="#38bdf8", highlightthickness=1, padx=8, pady=6)
        c1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        tk.Label(c1, text="PHASE 1: SUNDAY / MONTH-END", font=("Segoe UI", 8, "bold"), fg="#38bdf8", bg="#161f30").pack(anchor="w")
        tk.Label(c1, text="35 Marks / 80 Marks • 1.5h / 3h\nExamines all weekly/monthly homework", font=("Segoe UI", 7), fg="#cbd5e1", bg="#161f30", justify=tk.LEFT).pack(anchor="w", pady=2)
        btn_p1_w = tk.Button(c1, text="⚡ Weekly Test (35M)", font=("Segoe UI", 7, "bold"), fg="#0f172a", bg="#38bdf8", activebackground="#0284c7", relief=tk.FLAT, bd=0, padx=6, pady=3, cursor="hand2", command=lambda: self._launch_phase(1, "weekly"))
        btn_p1_w.pack(side=tk.LEFT, pady=3, padx=(0, 4))
        btn_p1_m = tk.Button(c1, text="🏆 Month-End (80M)", font=("Segoe UI", 7, "bold"), fg="#ffffff", bg="#0369a1", activebackground="#0284c7", relief=tk.FLAT, bd=0, padx=6, pady=3, cursor="hand2", command=lambda: self._launch_phase(1, "monthend"))
        btn_p1_m.pack(side=tk.LEFT, pady=3)

        # Phase 2 Card
        c2 = tk.Frame(cards_row, bg="#161f30", bd=1, relief=tk.SOLID, highlightbackground="#a855f7", highlightthickness=1, padx=8, pady=6)
        c2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        tk.Label(c2, text="PHASE 2: 3-DAY CHECKPOINT", font=("Segoe UI", 8, "bold"), fg="#c084fc", bg="#161f30").pack(anchor="w")
        tk.Label(c2, text="25 Marks • 1 Hour\nRetesting 3-day homework block retention", font=("Segoe UI", 7), fg="#cbd5e1", bg="#161f30", justify=tk.LEFT).pack(anchor="w", pady=2)
        btn_p2 = tk.Button(c2, text="⚡ 3-Day Checkpoint (25M)", font=("Segoe UI", 7, "bold"), fg="#0f172a", bg="#c084fc", activebackground="#a855f7", relief=tk.FLAT, bd=0, padx=6, pady=3, cursor="hand2", command=lambda: self._launch_phase(2, "3day"))
        btn_p2.pack(anchor="w", pady=3)

        # Phase 3 Card
        c3 = tk.Frame(cards_row, bg="#161f30", bd=1, relief=tk.SOLID, highlightbackground="#10b981", highlightthickness=1, padx=8, pady=6)
        c3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(c3, text="PHASE 3: MORNING SPRINT", font=("Segoe UI", 8, "bold"), fg="#34d399", bg="#161f30").pack(anchor="w")
        tk.Label(c3, text="25 Marks • 45 Mins\nRapid recall on yesterday's homework & morning", font=("Segoe UI", 7), fg="#cbd5e1", bg="#161f30", justify=tk.LEFT).pack(anchor="w", pady=2)
        p3_row = tk.Frame(c3, bg="#161f30")
        p3_row.pack(anchor="w", pady=2)
        self.p3_sub_var = tk.StringVar(value="Mathematics")
        p3_combo = ttk.Combobox(p3_row, textvariable=self.p3_sub_var, values=["Mathematics", "Physical Science", "Biological Science", "Social Science", "English", "Tamil", "Hindi"], width=13, font=("Segoe UI", 7), state="readonly")
        p3_combo.pack(side=tk.LEFT, padx=(0, 4))
        btn_p3 = tk.Button(p3_row, text="⚡ Morning Sprint (25M)", font=("Segoe UI", 7, "bold"), fg="#0f172a", bg="#34d399", activebackground="#059669", relief=tk.FLAT, bd=0, padx=6, pady=3, cursor="hand2", command=lambda: self._launch_phase(3, self.p3_sub_var.get()))
        btn_p3.pack(side=tk.LEFT)

        # Bottom section: Interactive Study Ledger Table
        ledger_frame = tk.Frame(pane, bg="#0e172a", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1, padx=10, pady=8)
        pane.add(ledger_frame, minsize=220)

        # Toolbar above ledger
        tb = tk.Frame(ledger_frame, bg="#0e172a")
        tb.pack(fill=tk.X, pady=(0, 6))

        tk.Label(tb, text="📖 SUBJECT STUDY LEDGER (HOMEWORK & EXAM PORTIONS LOG)", font=("Segoe UI", 9, "bold"), fg="#e2e8f0", bg="#0e172a").pack(side=tk.LEFT)

        # Filter dropdown
        tk.Label(tb, text="Filter:", font=("Segoe UI", 8), fg="#94a3b8", bg="#0e172a").pack(side=tk.LEFT, padx=(16, 4))
        self.ledger_filter_var = tk.StringVar(value="All Subjects")
        f_combo = ttk.Combobox(
            tb,
            textvariable=self.ledger_filter_var,
            values=["All Subjects", "Mathematics", "Physical Science", "Biological Science", "Social Science", "English", "Tamil", "Hindi"],
            width=15,
            state="readonly",
            font=("Segoe UI", 8)
        )
        f_combo.pack(side=tk.LEFT, padx=(0, 8))
        f_combo.bind("<<ComboboxSelected>>", lambda e: self._render_ledger_table())

        btn_add_entry = tk.Button(tb, text="➕ Log Custom Study Topic", font=("Segoe UI", 8, "bold"), fg="#38bdf8", bg="#1e293b", relief=tk.FLAT, bd=0, padx=8, pady=3, cursor="hand2", command=self._open_add_study_entry_modal)
        btn_add_entry.pack(side=tk.RIGHT, padx=(4, 0))

        # Treeview table
        cols = ("date", "subject", "chapter", "task", "status", "source")
        self.ledger_tree = ttk.Treeview(ledger_frame, columns=cols, show="headings", height=10)
        self.ledger_tree.heading("date", text="Date")
        self.ledger_tree.heading("subject", text="Subject")
        self.ledger_tree.heading("chapter", text="Chapter / Topic")
        self.ledger_tree.heading("task", text="Task Description")
        self.ledger_tree.heading("status", text="Status")
        self.ledger_tree.heading("source", text="Source")

        self.ledger_tree.column("date", width=85, anchor="center")
        self.ledger_tree.column("subject", width=120, anchor="w")
        self.ledger_tree.column("chapter", width=180, anchor="w")
        self.ledger_tree.column("task", width=340, anchor="w")
        self.ledger_tree.column("status", width=75, anchor="center")
        self.ledger_tree.column("source", width=110, anchor="center")

        sb = ttk.Scrollbar(ledger_frame, orient=tk.VERTICAL, command=self.ledger_tree.yview)
        self.ledger_tree.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.ledger_tree.pack(fill=tk.BOTH, expand=True)

        self._render_ledger_table()

    def _render_ledger_table(self):
        if not hasattr(self, "ledger_tree") or not self.ledger_tree.winfo_exists():
            return
        for i in self.ledger_tree.get_children():
            self.ledger_tree.delete(i)

        data = SubjectStudyLedger.load_ledger()
        entries = data.get("entries", [])
        filter_sub = getattr(self, "ledger_filter_var", None)
        filter_val = filter_sub.get() if filter_sub else "All Subjects"

        # Sort by date descending
        sorted_entries = sorted(entries, key=lambda x: x.get("date", ""), reverse=True)

        for e in sorted_entries:
            sub = e.get("subject", "")
            if filter_val != "All Subjects" and filter_val.lower() not in sub.lower():
                continue
            self.ledger_tree.insert("", tk.END, values=(
                e.get("date", ""),
                e.get("subject", ""),
                e.get("chapter_topic", ""),
                e.get("task_description", ""),
                e.get("study_status", "studied"),
                e.get("source", "diary")
            ))

    def _open_add_study_entry_modal(self):
        d_win = tk.Toplevel(self.parent)
        d_win.title("Log Custom Study Topic to Ledger")
        d_win.geometry("500x320")
        d_win.configure(bg="#0f172a")
        d_win.transient(self.parent)

        tk.Label(d_win, text="➕ Log Study Topic for Host Examination", font=("Segoe UI", 10, "bold"), fg="#f59e0b", bg="#0f172a").pack(anchor="w", padx=16, pady=(14, 10))

        form = tk.Frame(d_win, bg="#0f172a", padx=16)
        form.pack(fill=tk.BOTH, expand=True)

        tk.Label(form, text="Date (YYYY-MM-DD):", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0f172a").grid(row=0, column=0, sticky="w", pady=4)
        ent_date = ttk.Entry(form, width=25)
        ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        ent_date.grid(row=0, column=1, sticky="w", pady=4)

        tk.Label(form, text="Subject:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0f172a").grid(row=1, column=0, sticky="w", pady=4)
        sub_var = tk.StringVar(value="Mathematics")
        ent_sub = ttk.Combobox(form, textvariable=sub_var, values=["Mathematics", "Physical Science", "Biological Science", "Social Science", "English", "Tamil", "Hindi"], width=23, state="readonly")
        ent_sub.grid(row=1, column=1, sticky="w", pady=4)

        tk.Label(form, text="Chapter / Topic:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0f172a").grid(row=2, column=0, sticky="w", pady=4)
        ent_topic = ttk.Entry(form, width=35)
        ent_topic.grid(row=2, column=1, sticky="w", pady=4)

        tk.Label(form, text="Task Description:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0f172a").grid(row=3, column=0, sticky="w", pady=4)
        ent_task = ttk.Entry(form, width=35)
        ent_task.grid(row=3, column=1, sticky="w", pady=4)

        def save_manual_entry():
            d = ent_date.get().strip()
            s = sub_var.get().strip()
            tp = ent_topic.get().strip()
            tk_desc = ent_task.get().strip()
            if not tp or not tk_desc:
                messagebox.showwarning("Incomplete", "Please enter Chapter/Topic and Task Description.")
                return
            SubjectStudyLedger.record_entry(d, s, tp, tk_desc, source="manual_host")
            self._render_ledger_table()
            d_win.destroy()
            messagebox.showinfo("Saved", "Study entry recorded to Subject Study Ledger.")

        btn_row = tk.Frame(d_win, bg="#0f172a", pady=10)
        btn_row.pack(fill=tk.X, padx=16)
        tk.Button(btn_row, text="💾 Save to Ledger", font=("Segoe UI", 9, "bold"), fg="#0f172a", bg="#f59e0b", relief=tk.FLAT, bd=0, padx=12, pady=5, cursor="hand2", command=save_manual_entry).pack(side=tk.RIGHT)
        tk.Button(btn_row, text="Cancel", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b", relief=tk.FLAT, bd=0, padx=10, pady=5, cursor="hand2", command=d_win.destroy).pack(side=tk.RIGHT, padx=8)

    def _launch_phase(self, phase_num: int, sub_type: str):
        """Assemble exam blueprint based on phase, populate Face A, and switch to Face A."""
        spec = None
        if phase_num == 1:
            if sub_type == "weekly":
                spec = ExamPhaseAssembler.assemble_phase1_weekly_sunday_test()
            else:
                spec = ExamPhaseAssembler.assemble_phase1_monthend_mega_exam()
        elif phase_num == 2:
            spec = ExamPhaseAssembler.assemble_phase2_3day_checkpoint()
        elif phase_num == 3:
            spec = ExamPhaseAssembler.assemble_phase3_morning_sprint(sub_type)

        if spec:
            self.assembled_exam_spec = spec
            self.switch_subview("face_a")
            self._populate_face_a_with_spec(spec)

    # ==========================================
    # SUB-VIEW 2: FACE A - QUESTION PAPER ARCHITECT
    # ==========================================
    def _render_subview_face_a(self, parent):
        pane = tk.PanedWindow(parent, orient=tk.HORIZONTAL, bg=self.colors["bg"], sashrelief=tk.FLAT)
        pane.pack(fill=tk.BOTH, expand=True)

        # Left Column: Configuration Controls
        ctrl_frame = tk.Frame(pane, bg="#0e172a", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1, padx=12, pady=10)
        pane.add(ctrl_frame, minsize=320, width=340)

        lbl_hdr = tk.Label(ctrl_frame, text="⚙️ QUESTION PAPER ARCHITECT", font=("Segoe UI", 10, "bold"), fg="#f59e0b", bg="#0e172a")
        lbl_hdr.pack(anchor="w", pady=(0, 6))

        # Source Selection Mode
        lbl_src = tk.Label(ctrl_frame, text="Question Grounding Source:", font=("Segoe UI", 8, "bold"), fg="#38bdf8", bg="#0e172a")
        lbl_src.pack(anchor="w", pady=(4, 2))

        self.face_a_source_mode = tk.StringVar(value="textbook_pdf")
        r1 = tk.Radiobutton(ctrl_frame, text="📘 Grounded in Specific Textbook PDF", variable=self.face_a_source_mode, value="textbook_pdf", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0e172a", selectcolor="#161f30", activebackground="#0e172a", activeforeground="#f8fafc", command=self._on_source_mode_changed)
        r1.pack(anchor="w")

        # Textbook PDF selection dropdown & upload button
        self.pdf_select_frame = tk.Frame(ctrl_frame, bg="#0e172a", padx=16)
        self.pdf_select_frame.pack(fill=tk.X, pady=(2, 6))

        self.selected_textbook_pdf_var = tk.StringVar()
        self.combo_textbook_pdf = ttk.Combobox(self.pdf_select_frame, textvariable=self.selected_textbook_pdf_var, state="readonly", font=("Segoe UI", 8), width=24)
        self.combo_textbook_pdf.pack(fill=tk.X, pady=(0, 3))
        self._refresh_uploaded_textbooks_list()

        btn_upload_pdf = tk.Button(self.pdf_select_frame, text="📁 Upload Chapter PDF...", font=("Segoe UI", 7, "bold"), fg="#38bdf8", bg="#1e293b", relief=tk.FLAT, bd=0, padx=6, pady=2, cursor="hand2", command=self._upload_textbook_pdf)
        btn_upload_pdf.pack(anchor="w")

        r2 = tk.Radiobutton(ctrl_frame, text="🏛️ Official CBSE Standard Curriculum Blueprint", variable=self.face_a_source_mode, value="cbse_curriculum", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0e172a", selectcolor="#161f30", activebackground="#0e172a", activeforeground="#f8fafc", command=self._on_source_mode_changed)
        r2.pack(anchor="w", pady=(2, 6))

        # Divider
        tk.Frame(ctrl_frame, bg="#334155", height=1).pack(fill=tk.X, pady=6)

        # Exam Metadata Form
        tk.Label(ctrl_frame, text="Subject:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0e172a").pack(anchor="w")
        self.fa_subject_var = tk.StringVar(value="Mathematics")
        self.combo_fa_subject = ttk.Combobox(ctrl_frame, textvariable=self.fa_subject_var, values=["Mathematics", "Physical Science", "Biological Science", "Social Science", "English", "Tamil", "Hindi"], state="readonly", font=("Segoe UI", 8))
        self.combo_fa_subject.pack(fill=tk.X, pady=(2, 6))

        tk.Label(ctrl_frame, text="Exam Title / Phase:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0e172a").pack(anchor="w")
        self.fa_title_var = tk.StringVar(value="Phase 1: Weekly Sunday Examination - Week 3")
        self.ent_fa_title = ttk.Entry(ctrl_frame, textvariable=self.fa_title_var, font=("Segoe UI", 8))
        self.ent_fa_title.pack(fill=tk.X, pady=(2, 6))

        tk.Label(ctrl_frame, text="Max Marks:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0e172a").pack(anchor="w")
        self.fa_marks_var = tk.StringVar(value="35")
        self.combo_fa_marks = ttk.Combobox(ctrl_frame, textvariable=self.fa_marks_var, values=["25", "35", "50", "80"], state="readonly", font=("Segoe UI", 8))
        self.combo_fa_marks.pack(fill=tk.X, pady=(2, 6))

        tk.Label(ctrl_frame, text="Time Allowed:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0e172a").pack(anchor="w")
        self.fa_time_var = tk.StringVar(value="1.5 Hours")
        self.combo_fa_time = ttk.Combobox(ctrl_frame, textvariable=self.fa_time_var, values=["45 Minutes", "1 Hour", "1.5 Hours", "2 Hours", "3 Hours"], state="readonly", font=("Segoe UI", 8))
        self.combo_fa_time.pack(fill=tk.X, pady=(2, 10))

        # Primary Action: Generate Question Paper
        self.btn_generate_qp = tk.Button(
            ctrl_frame,
            text="⚡ GENERATE CBSE QUESTION PAPER",
            font=("Segoe UI", 9, "bold"),
            fg="#0f172a",
            bg="#f59e0b",
            activeforeground="#0f172a",
            activebackground="#d97706",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2",
            command=self._generate_question_paper_thread
        )
        self.btn_generate_qp.pack(fill=tk.X, pady=(4, 6))

        # Status Label
        self.lbl_fa_status = tk.Label(ctrl_frame, text="Ready to generate question paper.", font=("Segoe UI", 7), fg="#94a3b8", bg="#0e172a", wraplength=280)
        self.lbl_fa_status.pack(fill=tk.X, pady=(0, 6))

        # Right Column: Question Paper Preview & Export Studio
        prev_frame = tk.Frame(pane, bg="#0e172a", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1, padx=12, pady=10)
        pane.add(prev_frame, minsize=420)

        # Export & Print Toolbar
        prev_tb = tk.Frame(prev_frame, bg="#0e172a")
        prev_tb.pack(fill=tk.X, pady=(0, 6))

        tk.Label(prev_tb, text="📄 QUESTION PAPER PREVIEW (PRINT STUDIO)", font=("Segoe UI", 9, "bold"), fg="#f8fafc", bg="#0e172a").pack(side=tk.LEFT)

        btn_copy = tk.Button(prev_tb, text="📋 Copy", font=("Segoe UI", 7, "bold"), fg="#cbd5e1", bg="#1e293b", relief=tk.FLAT, bd=0, padx=6, pady=3, cursor="hand2", command=self._copy_question_paper_text)
        btn_copy.pack(side=tk.RIGHT, padx=3)

        btn_pdf = tk.Button(prev_tb, text="📄 Export PDF", font=("Segoe UI", 7, "bold"), fg="#ffffff", bg="#0284c7", activebackground="#0369a1", relief=tk.FLAT, bd=0, padx=6, pady=3, cursor="hand2", command=self._export_question_paper_pdf)
        btn_pdf.pack(side=tk.RIGHT, padx=3)

        btn_print = tk.Button(prev_tb, text="🖨️ Print / Web", font=("Segoe UI", 7, "bold"), fg="#0f172a", bg="#38bdf8", activebackground="#0284c7", relief=tk.FLAT, bd=0, padx=8, pady=3, cursor="hand2", command=self._print_question_paper_html)
        btn_print.pack(side=tk.RIGHT, padx=3)

        # Monospace Text Preview Area with Scrollbars
        text_container = tk.Frame(prev_frame, bg="#020617")
        text_container.pack(fill=tk.BOTH, expand=True)

        self.fa_text = tk.Text(
            text_container,
            wrap=tk.WORD,
            bg="#020617",
            fg="#f8fafc",
            insertbackground="#f59e0b",
            font=("Consolas", 9),
            padx=12,
            pady=12,
            bd=0
        )
        sb_fa = ttk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.fa_text.yview)
        self.fa_text.configure(yscrollcommand=sb_fa.set)
        sb_fa.pack(side=tk.RIGHT, fill=tk.Y)
        self.fa_text.pack(fill=tk.BOTH, expand=True)

        # Show placeholder
        self._display_question_paper_placeholder()

    def _on_source_mode_changed(self):
        if self.face_a_source_mode.get() == "textbook_pdf":
            self.pdf_select_frame.pack(fill=tk.X, pady=(2, 6))
        else:
            self.pdf_select_frame.pack_forget()

    def _refresh_uploaded_textbooks_list(self):
        files = [f for f in os.listdir(TEXTBOOKS_PDF_DIR) if f.lower().endswith(".pdf")]
        self.combo_textbook_pdf["values"] = files
        if files:
            self.selected_textbook_pdf_var.set(files[0])
        else:
            self.selected_textbook_pdf_var.set("No PDFs Uploaded")

    def _upload_textbook_pdf(self):
        filepath = filedialog.askopenfilename(
            title="Upload Textbook Chapter PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if filepath:
            fname = os.path.basename(filepath)
            dest = os.path.join(TEXTBOOKS_PDF_DIR, fname)
            try:
                import shutil
                shutil.copy2(filepath, dest)
                self._refresh_uploaded_textbooks_list()
                self.selected_textbook_pdf_var.set(fname)
                messagebox.showinfo("Uploaded", f"Uploaded textbook chapter PDF:\n{fname}")
            except Exception as e:
                messagebox.showerror("Upload Error", f"Failed to upload PDF: {e}")

    def _populate_face_a_with_spec(self, spec: Dict[str, Any]):
        if hasattr(self, "fa_subject_var"):
            self.fa_subject_var.set(spec.get("subject", "Mathematics"))
            self.fa_title_var.set(spec.get("exam_title", "CBSE Examination"))
            self.fa_marks_var.set(str(spec.get("max_marks", 35)))
            self.fa_time_var.set(spec.get("time_allowed", "1.5 Hours"))

    def _display_question_paper_placeholder(self):
        self.fa_text.delete("1.0", tk.END)
        placeholder = (
            "========================================================================================\n"
            "                      SENTHIL PUBLIC SCHOOL, DHARMAPURI\n"
            "                    HOST-CONDUCTED CBSE EVALUATION SYSTEM\n"
            "========================================================================================\n\n"
            "  [Question Paper Preview Area]\n\n"
            "  1. Select Examination Phase in Tab 1, or configure parameters on the left.\n"
            "  2. Choose whether to ground questions in a specific Textbook PDF or standard CBSE syllabus.\n"
            "  3. Click '⚡ GENERATE CBSE QUESTION PAPER' to architect the paper.\n"
            "  4. The generated paper adheres strictly to CBSE formatting:\n"
            "     - Right-aligned mark indicators [1], [2], [3], [5]\n"
            "     - Section A (MCQs / Competency), Section B (VSA), Section C (SA), Section D (LA), Section E\n"
            "     - Step-wise marking rubrics embedded\n"
            "     - Exportable to print-ready HTML and A4 PDF format.\n\n"
            "========================================================================================\n"
        )
        self.fa_text.insert(tk.END, placeholder)

    def _generate_question_paper_thread(self):
        self.btn_generate_qp.configure(state=tk.DISABLED)
        self.lbl_fa_status.configure(text="⏳ Generating CBSE Question Paper... Please wait.", fg="#f59e0b")

        def run():
            try:
                sub = self.fa_subject_var.get()
                title = self.fa_title_var.get()
                marks = int(self.fa_marks_var.get())
                t_str = self.fa_time_var.get()
                src_mode = self.face_a_source_mode.get()
                pdf_name = self.selected_textbook_pdf_var.get() if src_mode == "textbook_pdf" and self.selected_textbook_pdf_var.get() != "No PDFs Uploaded" else None

                spec = {
                    "phase": "custom",
                    "exam_title": title,
                    "subject": sub,
                    "class_standard": GeminiExamClient.load_config().get("class_level", "Class 8 CBSE"),
                    "time_allowed": t_str,
                    "max_marks": marks,
                    "topics": [f"{sub} Core Concepts and Step Procedures"],
                    "blueprint": {
                        "sec_A": f"{max(2, marks // 8)} MCQs [1M each]",
                        "sec_B": f"{max(2, marks // 10)} VSA [2M each]",
                        "sec_C": f"{max(2, marks // 12)} SA [3M each]",
                        "sec_D": f"{max(1, marks // 20)} LA [5M each]"
                    }
                }

                qp = GeminiExamClient.generate_question_paper(spec, textbook_pdf_name=pdf_name)
                self.active_question_paper = qp
                self.active_exam_id = qp.get("exam_id", "")

                # Update UI in main thread
                self.parent.after(0, lambda: self._on_question_paper_generated(qp))
            except Exception as e:
                self.parent.after(0, lambda: self._on_question_paper_error(str(e)))

        threading.Thread(target=run, daemon=True).start()

    def _on_question_paper_generated(self, qp: Dict[str, Any]):
        self.btn_generate_qp.configure(state=tk.NORMAL)
        self.lbl_fa_status.configure(text=f"✓ Generated: {qp.get('exam_id')} ({qp.get('source_grounding')})", fg="#34d399")

        # Format and display in preview text
        self.fa_text.delete("1.0", tk.END)
        lines = []
        hdr = qp.get("header_block", {})
        lines.append(f"{hdr.get('institution', 'SENTHIL PUBLIC SCHOOL')}".center(88))
        lines.append(f"{hdr.get('exam_title', 'CBSE EXAMINATION')}".center(88))
        lines.append(f"{hdr.get('subject', 'SUBJECT')} • {hdr.get('class_standard', 'CLASS 8')} | Time: {hdr.get('time_allowed', '1.5 Hours')} | Max Marks: {hdr.get('max_marks', 35)}".center(88))
        lines.append("-" * 88)
        lines.append("GENERAL INSTRUCTIONS:")
        for gi in qp.get("general_instructions", []):
            lines.append(f"  • {gi}")
        lines.append("-" * 88 + "\n")

        for sec in qp.get("sections", []):
            lines.append(f"{sec.get('section_name')}: {sec.get('title')}".center(88))
            lines.append("=" * 88)
            for q in sec.get("questions", []):
                q_num = q.get("q_num", "Q")
                marks = q.get("marks", 1)
                m_str = f"[{marks}]"
                q_text = q.get("question_text", "")
                
                # Format with right-aligned marks bracket
                prefix = f"{q_num:>4}.  "
                lines.append(f"{prefix}{q_text:<68} {m_str:>8}")

                if "options" in q and q["options"]:
                    for opt in q["options"]:
                        lines.append(f"       {opt}")

                lines.append("")

        self.fa_text.insert(tk.END, "\n".join(lines))

    def _on_question_paper_error(self, err_msg: str):
        self.btn_generate_qp.configure(state=tk.NORMAL)
        self.lbl_fa_status.configure(text=f"Error: {err_msg}", fg="#f87171")
        messagebox.showerror("Question Paper Generation Error", err_msg)

    def _print_question_paper_html(self):
        if not self.active_question_paper:
            messagebox.showwarning("No Paper", "Please generate a question paper first.")
            return
        html_content = GeminiExamClient.render_question_paper_html(self.active_question_paper)
        out_html_path = os.path.join(QUESTION_PAPERS_DIR, f"{self.active_exam_id}_print_preview.html")
        with open(out_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        webbrowser.open(f"file:///{os.path.abspath(out_html_path).replace(os.sep, '/')}")

    def _export_question_paper_pdf(self):
        if not self.active_question_paper:
            messagebox.showwarning("No Paper", "Please generate a question paper first.")
            return
        out_pdf = os.path.join(QUESTION_PAPERS_DIR, f"{self.active_exam_id}_QUESTION_PAPER.pdf")
        try:
            GeminiExamClient.render_question_paper_pdf(self.active_question_paper, out_pdf)
            if os.path.exists(out_pdf):
                messagebox.showinfo("PDF Exported", f"Question paper PDF successfully generated:\n{out_pdf}")
                if sys.platform == "win32":
                    os.startfile(out_pdf)
        except Exception as e:
            messagebox.showerror("PDF Export Error", f"Failed to generate PDF: {e}")

    def _copy_question_paper_text(self):
        txt = self.fa_text.get("1.0", tk.END).strip()
        if txt:
            self.parent.clipboard_clear()
            self.parent.clipboard_append(txt)
            messagebox.showinfo("Copied", "Question paper text copied to clipboard!")

    # ==========================================
    # SUB-VIEW 3: FACE B - ANSWER SHEET EVALUATOR
    # ==========================================
    def _render_subview_face_b(self, parent):
        pane = tk.PanedWindow(parent, orient=tk.HORIZONTAL, bg=self.colors["bg"], sashrelief=tk.FLAT)
        pane.pack(fill=tk.BOTH, expand=True)

        # Left Column: Upload & Input
        in_frame = tk.Frame(pane, bg="#0e172a", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1, padx=12, pady=10)
        pane.add(in_frame, minsize=320, width=350)

        lbl_hdr = tk.Label(in_frame, text="🔍 ANSWER SHEET EVALUATOR (FACE B)", font=("Segoe UI", 10, "bold"), fg="#f59e0b", bg="#0e172a")
        lbl_hdr.pack(anchor="w", pady=(0, 6))

        # Select Question Paper to Evaluate
        tk.Label(in_frame, text="Select Question Paper to Evaluate:", font=("Segoe UI", 8, "bold"), fg="#38bdf8", bg="#0e172a").pack(anchor="w")
        self.fb_exam_id_var = tk.StringVar(value=self.active_exam_id or "Select Question Paper")
        self.combo_fb_exams = ttk.Combobox(in_frame, textvariable=self.fb_exam_id_var, state="readonly", font=("Segoe UI", 8))
        self.combo_fb_exams.pack(fill=tk.X, pady=(2, 8))
        self._refresh_generated_papers_list()

        # Upload Answer Sheet scans / photos
        tk.Label(in_frame, text="Upload Handwritten Answer Sheet Photos / PDF:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0e172a").pack(anchor="w")
        btn_upload_as = tk.Button(in_frame, text="📁 Browse Answer Sheet Images / PDF...", font=("Segoe UI", 8, "bold"), fg="#38bdf8", bg="#1e293b", relief=tk.FLAT, bd=0, padx=8, pady=4, cursor="hand2", command=self._upload_answer_sheets)
        btn_upload_as.pack(fill=tk.X, pady=(2, 6))

        self.lbl_as_uploaded_status = tk.Label(in_frame, text="No scan uploaded yet.", font=("Segoe UI", 7), fg="#94a3b8", bg="#0e172a", wraplength=300)
        self.lbl_as_uploaded_status.pack(fill=tk.X, pady=(0, 6))

        # Alternative Text / Quick Input Area
        tk.Label(in_frame, text="Or Paste Answer Transcription / Test Text:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0e172a").pack(anchor="w")
        self.fb_input_text = tk.Text(in_frame, height=8, bg="#020617", fg="#f8fafc", font=("Consolas", 8), insertbackground="#f59e0b", padx=6, pady=6)
        self.fb_input_text.pack(fill=tk.BOTH, expand=True, pady=(2, 8))
        self.fb_input_text.insert(tk.END, "Sample Answers:\n1. (b) 25\n2. (a) Photosynthesis\n3. Area of trapezium = 1/2 * (a + b) * h\n   Area = 1/2 * (10 + 20) * 8 = 120 cm^2")

        # Evaluate Button
        self.btn_evaluate = tk.Button(
            in_frame,
            text="🔴 EVALUATE WITH CBSE STEP-MARKING",
            font=("Segoe UI", 9, "bold"),
            fg="#ffffff",
            bg="#b91c1c",
            activeforeground="#ffffff",
            activebackground="#991b1b",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2",
            command=self._evaluate_answer_sheet_thread
        )
        self.btn_evaluate.pack(fill=tk.X, pady=(4, 6))

        self.lbl_eval_status = tk.Label(in_frame, text="Ready to evaluate answer sheet.", font=("Segoe UI", 7), fg="#94a3b8", bg="#0e172a")
        self.lbl_eval_status.pack(fill=tk.X)

        # Right Column: Corrected Soft Copy Viewer
        eval_view_frame = tk.Frame(pane, bg="#0e172a", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1, padx=12, pady=10)
        pane.add(eval_view_frame, minsize=420)

        # Toolbar above evaluation
        eval_tb = tk.Frame(eval_view_frame, bg="#0e172a")
        eval_tb.pack(fill=tk.X, pady=(0, 6))

        tk.Label(eval_tb, text="📝 CORRECTED SOFT COPY & RED-INK ANNOTATIONS", font=("Segoe UI", 9, "bold"), fg="#f8fafc", bg="#0e172a").pack(side=tk.LEFT)

        btn_eval_pdf = tk.Button(eval_tb, text="📄 Export Graded PDF", font=("Segoe UI", 7, "bold"), fg="#ffffff", bg="#0284c7", activebackground="#0369a1", relief=tk.FLAT, bd=0, padx=6, pady=3, cursor="hand2", command=self._export_corrected_copy_pdf)
        btn_eval_pdf.pack(side=tk.RIGHT, padx=3)

        btn_eval_print = tk.Button(eval_tb, text="🖨️ View Soft Copy (HTML)", font=("Segoe UI", 7, "bold"), fg="#0f172a", bg="#38bdf8", activebackground="#0284c7", relief=tk.FLAT, bd=0, padx=8, pady=3, cursor="hand2", command=self._print_corrected_copy_html)
        btn_eval_print.pack(side=tk.RIGHT, padx=3)

        # Scorecard Banner Frame
        self.scorecard_frame = tk.Frame(eval_view_frame, bg="#161f30", bd=1, relief=tk.SOLID, highlightbackground="#38bdf8", highlightthickness=1, padx=10, pady=8)
        self.scorecard_frame.pack(fill=tk.X, pady=(0, 8))

        self.lbl_score_summary = tk.Label(
            self.scorecard_frame,
            text="SCORE: -- / -- (0%) • GRADE: -- • AUDIT: Awaiting Answer Sheet Evaluation",
            font=("Segoe UI", 9, "bold"),
            fg="#f59e0b",
            bg="#161f30"
        )
        self.lbl_score_summary.pack(anchor="w")

        self.lbl_daydreaming_verdict = tk.Label(
            self.scorecard_frame,
            text="Anti-Daydreaming Verdict: Upload answer sheet to verify genuine retention vs superficial study.",
            font=("Segoe UI", 8),
            fg="#cbd5e1",
            bg="#161f30"
        )
        self.lbl_daydreaming_verdict.pack(anchor="w", pady=(2, 0))

        # Text View for Evaluation Breakdown
        text_container = tk.Frame(eval_view_frame, bg="#020617")
        text_container.pack(fill=tk.BOTH, expand=True)

        self.fb_eval_text = tk.Text(
            text_container,
            wrap=tk.WORD,
            bg="#020617",
            fg="#f8fafc",
            font=("Consolas", 9),
            padx=12,
            pady=12,
            bd=0
        )
        sb_fb = ttk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.fb_eval_text.yview)
        self.fb_eval_text.configure(yscrollcommand=sb_fb.set)
        sb_fb.pack(side=tk.RIGHT, fill=tk.Y)
        self.fb_eval_text.pack(fill=tk.BOTH, expand=True)

        self.fb_eval_text.insert(tk.END, "Evaluation results, step-wise marks deductions, and red-ink teacher notes will appear here.")

    def _refresh_generated_papers_list(self):
        files = [f for f in os.listdir(QUESTION_PAPERS_DIR) if f.endswith(".json")]
        ids = [f.replace(".json", "") for f in files]
        self.combo_fb_exams["values"] = ids
        if ids and (not self.active_exam_id or self.active_exam_id not in ids):
            self.fb_exam_id_var.set(ids[0])
        elif self.active_exam_id:
            self.fb_exam_id_var.set(self.active_exam_id)

    def _upload_answer_sheets(self):
        files = filedialog.askopenfilenames(
            title="Select Tharun's Handwritten Answer Sheet Scans / Images / PDF",
            filetypes=[("Image & PDF Files", "*.jpg;*.jpeg;*.png;*.pdf"), ("All Files", "*.*")]
        )
        if files:
            saved_paths = []
            import shutil
            for f in files:
                fname = os.path.basename(f)
                dest = os.path.join(ANSWER_SHEETS_DIR, fname)
                shutil.copy2(f, dest)
                saved_paths.append(dest)
            self.uploaded_answer_files = saved_paths
            self.lbl_as_uploaded_status.configure(text=f"✓ Uploaded {len(saved_paths)} answer sheet file(s).", fg="#34d399")
            messagebox.showinfo("Uploaded", f"Uploaded {len(saved_paths)} answer sheet files to Answer Sheets vault.")

    def _evaluate_answer_sheet_thread(self):
        exam_id = self.fb_exam_id_var.get()
        if not exam_id or exam_id == "Select Question Paper":
            messagebox.showwarning("Select Exam", "Please select a generated question paper to evaluate against.")
            return

        self.btn_evaluate.configure(state=tk.DISABLED)
        self.lbl_eval_status.configure(text="⏳ Evaluating answer sheet with CBSE step-marking rubrics...", fg="#f59e0b")

        def run():
            try:
                # If no files uploaded, write the input text into a temp file for evaluation
                files_to_eval = list(self.uploaded_answer_files)
                if not files_to_eval:
                    txt = self.fb_input_text.get("1.0", tk.END).strip()
                    temp_f = os.path.join(ANSWER_SHEETS_DIR, f"{exam_id}_student_answers_transcript.txt")
                    with open(temp_f, "w", encoding="utf-8") as f:
                        f.write(txt)
                    files_to_eval = [temp_f]

                res = GeminiExamClient.evaluate_answer_sheet(exam_id, files_to_eval)
                self.active_evaluation = res

                self.parent.after(0, lambda: self._on_evaluation_complete(res))
            except Exception as e:
                self.parent.after(0, lambda: self._on_evaluation_error(str(e)))

        threading.Thread(target=run, daemon=True).start()

    def _on_evaluation_complete(self, eval_data: Dict[str, Any]):
        self.btn_evaluate.configure(state=tk.NORMAL)
        self.lbl_eval_status.configure(text="✓ Answer sheet evaluated successfully!", fg="#34d399")

        # Update Scorecard Banner
        scored = eval_data.get("marks_scored", 0)
        total = eval_data.get("max_marks", 35)
        pct = eval_data.get("percentage", 0)
        grade = eval_data.get("cbse_grade", "B1")
        audit = eval_data.get("daydreaming_audit", {})
        verdict = audit.get("verdict", "VERIFIED")

        self.lbl_score_summary.configure(
            text=f"SCORE: {scored} / {total} ({pct:.1f}%) • GRADE: {grade} • AUDIT: {verdict}",
            fg="#10b981" if pct >= 60 else "#f87171"
        )
        self.lbl_daydreaming_verdict.configure(
            text=f"Audit Summary: {audit.get('summary', '')}"
        )

        # Format Detailed Question Evaluations
        lines = []
        lines.append("=" * 88)
        lines.append("                       CBSE TEACHER STEP-WISE MARKING REPORT")
        lines.append(f" Student: {eval_data.get('student_name', 'Tharun')} | Class: {eval_data.get('class_standard', 'Class 8 CBSE')} | Exam ID: {eval_data.get('exam_id')}")
        lines.append("=" * 88 + "\n")

        for q in eval_data.get("question_evaluations", []):
            lines.append(f"QUESTION {q.get('q_num')}: {q.get('question_text')}")
            lines.append(f"Marks Awarded: {q.get('marks_awarded')} / {q.get('max_marks')}")
            lines.append(f"Student Answer: {q.get('student_transcription')}")
            lines.append(f"Expected Answer: {q.get('expected_solution')}")
            lines.append("Step-Wise Breakdown:")
            for sb in q.get("step_breakdown", []):
                lines.append(f"  • {sb}")
            lines.append(f"Red-Ink Teacher Notes: {q.get('red_ink_annotations')}")
            lines.append("-" * 88 + "\n")

        self.fb_eval_text.delete("1.0", tk.END)
        self.fb_eval_text.insert(tk.END, "\n".join(lines))

    def _on_evaluation_error(self, err_msg: str):
        self.btn_evaluate.configure(state=tk.NORMAL)
        self.lbl_eval_status.configure(text=f"Error: {err_msg}", fg="#f87171")
        messagebox.showerror("Evaluation Error", err_msg)

    def _print_corrected_copy_html(self):
        if not self.active_evaluation:
            messagebox.showwarning("No Evaluation", "Please evaluate an answer sheet first.")
            return
        html_content = GeminiExamClient.render_corrected_copy_html(self.active_evaluation)
        exam_id = self.active_evaluation.get("exam_id", "EXAM")
        out_html = os.path.join(CORRECTED_COPIES_DIR, f"{exam_id}_CORRECTED_COPY.html")
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        webbrowser.open(f"file:///{os.path.abspath(out_html).replace(os.sep, '/')}")

    def _export_corrected_copy_pdf(self):
        if not self.active_evaluation:
            messagebox.showwarning("No Evaluation", "Please evaluate an answer sheet first.")
            return
        exam_id = self.active_evaluation.get("exam_id", "EXAM")
        out_pdf = os.path.join(CORRECTED_COPIES_DIR, f"{exam_id}_GRADED_CORRECTED_COPY.pdf")
        try:
            GeminiExamClient.render_corrected_copy_pdf(self.active_evaluation, out_pdf)
            if os.path.exists(out_pdf):
                messagebox.showinfo("PDF Exported", f"Corrected copy PDF generated:\n{out_pdf}")
                if sys.platform == "win32":
                    os.startfile(out_pdf)
        except Exception as e:
            messagebox.showerror("PDF Error", f"Failed to generate corrected PDF: {e}")

    # ==========================================
    # SUB-VIEW 4: CBSE TOPPER MODEL ANSWER GUIDE
    # ==========================================
    def _render_subview_topper(self, parent):
        top_bar = tk.Frame(parent, bg="#0e172a", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1, padx=12, pady=10)
        top_bar.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            top_bar,
            text="⭐ HOW THARUN ANSWERED VS. HOW TO ANSWER FOR MAXIMUM MARKS",
            font=("Segoe UI", 10, "bold"),
            fg="#f59e0b",
            bg="#0e172a"
        ).pack(side=tk.LEFT)

        btn_top_pdf = tk.Button(top_bar, text="📄 Export Topper Guide (PDF)", font=("Segoe UI", 8, "bold"), fg="#ffffff", bg="#0284c7", activebackground="#0369a1", relief=tk.FLAT, bd=0, padx=8, pady=3, cursor="hand2", command=self._export_topper_guide_pdf)
        btn_top_pdf.pack(side=tk.RIGHT, padx=3)

        btn_top_html = tk.Button(top_bar, text="🖨️ View Guide (HTML Print)", font=("Segoe UI", 8, "bold"), fg="#0f172a", bg="#38bdf8", activebackground="#0284c7", relief=tk.FLAT, bd=0, padx=8, pady=3, cursor="hand2", command=self._print_topper_guide_html)
        btn_top_html.pack(side=tk.RIGHT, padx=3)

        # Instructions Banner
        tk.Label(
            parent,
            text="P-E-E-D Protocol: Point • Explain • Evidence/Formula • Diagram/Step  |  Highlights required keywords to underline for 100% marks.",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg=self.colors["bg"],
            pady=4
        ).pack(fill=tk.X)

        # Scrollable comparison container
        container = tk.Frame(parent, bg="#020617")
        container.pack(fill=tk.BOTH, expand=True)

        self.topper_text = tk.Text(
            container,
            wrap=tk.WORD,
            bg="#020617",
            fg="#f8fafc",
            font=("Consolas", 9),
            padx=14,
            pady=14,
            bd=0
        )
        sb_top = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.topper_text.yview)
        self.topper_text.configure(yscrollcommand=sb_top.set)
        sb_top.pack(side=tk.RIGHT, fill=tk.Y)
        self.topper_text.pack(fill=tk.BOTH, expand=True)

        self._render_topper_comparison_text()

    def _render_topper_comparison_text(self):
        self.topper_text.delete("1.0", tk.END)

        if not self.active_evaluation:
            placeholder = (
                "========================================================================================\n"
                "           CBSE TOPPER ANSWER STRUCTURING & MAXIMUM MARKS REFERENCE GUIDE\n"
                "========================================================================================\n\n"
                "  This view compares Tharun's exact written answer against a 100/100 CBSE Topper model.\n\n"
                "  To populate this guide:\n"
                "  1. Generate a question paper in Face A.\n"
                "  2. Evaluate Tharun's answer sheet in Face B.\n"
                "  3. Switch back here to inspect side-by-side answering improvements, including:\n"
                "     - Keywords that must be underlined in blue/pencil\n"
                "     - Correct formula box presentation\n"
                "     - P-E-E-D (Point, Explain, Evidence/Formula, Diagram) protocol\n"
                "     - Specific conceptual slips where marks were dropped\n\n"
                "========================================================================================\n"
            )
            self.topper_text.insert(tk.END, placeholder)
            return

        lines = []
        eval_data = self.active_evaluation
        lines.append("=" * 88)
        lines.append(f" HOW THARUN ANSWERED VS. CBSE TOPPER MODEL ANSWER - {eval_data.get('student_name', 'Tharun')}")
        lines.append(f" Class: {eval_data.get('class_standard', 'Class 8 CBSE')} | Subject: {eval_data.get('subject', 'Mathematics')}")
        lines.append("=" * 88 + "\n")

        for q in eval_data.get("question_evaluations", []):
            comp = q.get("topper_comparison", {})
            kws = ", ".join(comp.get("keywords_to_underline", []))

            lines.append(f"QUESTION {q.get('q_num')}: {q.get('question_text')}")
            lines.append("-" * 88)
            lines.append(f"[THARUN'S WRITTEN ANSWER]")
            lines.append(f"  \"{q.get('student_transcription')}\"")
            lines.append(f"  Daydreaming/Omission Slip: {comp.get('tharun_weakness')}\n")

            lines.append(f"[CBSE TOPPER MODEL ANSWER (100% MARKS)]")
            lines.append(f"  {comp.get('topper_model_answer')}")
            lines.append(f"  Keywords to Underline: [{kws}]")
            lines.append(f"  Presentation Tip: Box final numerical answer with SI unit. Write distinct numbered points.")
            lines.append("=" * 88 + "\n")

        self.topper_text.insert(tk.END, "\n".join(lines))

    def _print_topper_guide_html(self):
        if not self.active_evaluation:
            messagebox.showwarning("No Data", "Please evaluate an answer sheet first to generate model answer comparisons.")
            return
        html_content = GeminiExamClient.render_model_answer_guide_html(self.active_evaluation)
        exam_id = self.active_evaluation.get("exam_id", "EXAM")
        out_html = os.path.join(MODEL_ANSWERS_DIR, f"{exam_id}_TOPPER_MODEL_GUIDE.html")
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        webbrowser.open(f"file:///{os.path.abspath(out_html).replace(os.sep, '/')}")

    def _export_topper_guide_pdf(self):
        if not self.active_evaluation:
            messagebox.showwarning("No Data", "Please evaluate an answer sheet first to generate model answer comparisons.")
            return
        exam_id = self.active_evaluation.get("exam_id", "EXAM")
        out_pdf = os.path.join(MODEL_ANSWERS_DIR, f"{exam_id}_TOPPER_MODEL_GUIDE.pdf")
        try:
            GeminiExamClient.render_model_answer_guide_pdf(self.active_evaluation, out_pdf)
            if os.path.exists(out_pdf):
                messagebox.showinfo("PDF Exported", f"Topper model answer guide PDF generated:\n{out_pdf}")
                if sys.platform == "win32":
                    os.startfile(out_pdf)
        except Exception as e:
            messagebox.showerror("PDF Error", f"Failed to generate Topper guide PDF: {e}")
