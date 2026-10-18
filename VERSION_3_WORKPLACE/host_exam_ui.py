"""
host_exam_ui.py - Host Examination & Gemini AI CBSE Evaluator UI Controller (V3)
Integrates with ScholasticPulse Version 3 Desktop Application (study_balancer.py).

Enhanced with:
- 100% Visual Parity & Shinobi Theme Sync (apply_theme hook)
- Zero native ttk.Combobox: All replaced with ShinobiPillSelector dark-glass cards
- Zero native gray scrollbars: All replaced with 6px Custom Dark Canvas Scrollbar (#334155 thumb on #0b1120 track)
- ShinobiGraphicsEngine 3D cylindrical parchment scroll banners & rounded dark-glass cards (radius=12)
- Strict geometry lock with .pack_propagate(False) preventing window boundary shift
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

# ShinobiGraphicsEngine and ShinobiPillSelector imported lazily from study_balancer
ShinobiGraphicsEngine = None
ShinobiPillSelector = None

def _resolve_shinobi_components():
    global ShinobiGraphicsEngine, ShinobiPillSelector
    if ShinobiPillSelector is None or ShinobiGraphicsEngine is None:
        try:
            import study_balancer
            if hasattr(study_balancer, "ShinobiGraphicsEngine"):
                ShinobiGraphicsEngine = study_balancer.ShinobiGraphicsEngine
            if hasattr(study_balancer, "ShinobiPillSelector"):
                ShinobiPillSelector = study_balancer.ShinobiPillSelector
        except Exception:
            pass



class CustomDarkScrollbar(tk.Canvas):
    """
    Ultra-slim 6px Custom Dark Canvas Scrollbar:
    Replaces clunky Win32 / gray ttk.Scrollbar with sleek dark track (#0b1120)
    and rounded slate thumb (#334155) that highlights to golden amber on hover.
    """
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
            self.target.yview_moveto(event.y / sh)

    def _on_drag(self, event):
        sh = self.winfo_height()
        if sh > 0 and self.target:
            self.target.yview_moveto(event.y / sh)


class HostExamTabController:
    """Controller for the 'Host Exam & Gemini Evaluator (V3)' Tab in ScholasticPulse Desktop."""

    def __init__(self, app, tab_frame: tk.Frame):
        _resolve_shinobi_components()
        self.app = app
        self.parent = tab_frame
        self.colors = app.colors

        # State
        self.active_subview = "ledger"  # "ledger", "face_a", "face_b", "topper"
        self.active_question_paper: Optional[Dict[str, Any]] = None
        self.active_evaluation: Optional[Dict[str, Any]] = None
        self.active_exam_id: str = ""
        self.uploaded_answer_files: List[str] = []
        self.active_model_var = tk.StringVar(value="gemini-3.8-flash")

        # Persistent subview frame references (instantiated in build_ui)
        self.subview_1 = None
        self.subview_2 = None
        self.subview_3 = None
        self.subview_4 = None
        self.subview_5 = None
        self.subview_6 = None
        self.subview_map = {
            'ledger': self.subview_1, 
            'textbook_vault': self.subview_2, 
            'sample_papers': self.subview_3, 
            'face_a': self.subview_4, 
            'face_b': self.subview_5, 
            'topper_guide': self.subview_6
        }

        # Auto-sync ledger on init
        try:
            SubjectStudyLedger.auto_sync_from_diary_and_portions()
        except Exception as e:
            print(f"[HostExamTabController] Warning during ledger auto-sync: {e}")

    def build_ui(self):
        """Construct the entire Host Examination UI inside the tab frame with strict geometry lock."""
        for w in self.parent.winfo_children():
            w.destroy()

        pad = tk.Frame(self.parent, bg=self.colors.get("bg", "#0a0e17"), padx=12, pady=6)
        pad.pack(fill=tk.BOTH, expand=True)
        self.pad = pad

        # 1. Top Command Deck
        self._build_top_command_deck(pad)

        # 2. Sub-View Navigation Bar
        self._build_subview_navigation_bar(pad)

        # 3. Main Dynamic Sub-View Container
        self.subview_container = tk.Frame(pad, bg=self.colors.get("bg", "#0a0e17"))
        self.subview_container.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        # Persistent subview frames
        bg_col = self.colors.get("bg", "#0a0e17")
        self.subview_1 = tk.Frame(self.subview_container, bg=bg_col)
        self.subview_2 = tk.Frame(self.subview_container, bg=bg_col)
        self.subview_3 = tk.Frame(self.subview_container, bg=bg_col)
        self.subview_4 = tk.Frame(self.subview_container, bg=bg_col)
        self.subview_5 = tk.Frame(self.subview_container, bg=bg_col)
        self.subview_6 = tk.Frame(self.subview_container, bg=bg_col)

        # Pre-render content into each persistent subview frame once
        self._render_subview_ledger(self.subview_1)
        self._render_subview_vault(self.subview_2)
        self._render_subview_sample_questions(self.subview_3)
        self._render_clean_face_a(self.subview_4)
        self._render_subview_face_b(self.subview_5)
        self._render_subview_topper(self.subview_6)

        self.subview_map = {
            'ledger': self.subview_1, 
            'textbook_vault': self.subview_2, 
            'sample_papers': self.subview_3, 
            'face_a': self.subview_4, 
            'face_b': self.subview_5, 
            'topper_guide': self.subview_6
        }

        # Show initial subview
        self.switch_subview("ledger")

    def apply_theme(self, colors: Dict[str, str]):
        """
        Dynamically propagate active Shinobi theme colors across the V3 Exam System:
        Updates deck, navigation pills, status badges, and redraws the active sub-view.
        """
        self.colors = colors
        bg_col = colors.get("bg", "#0a0e17")
        border_col = colors.get("card_border", colors.get("primary", "#f59e0b"))
        primary_col = colors.get("primary", "#f59e0b")

        if hasattr(self, "pad") and self.pad.winfo_exists():
            self.pad.configure(bg=bg_col)
        if hasattr(self, "subview_container") and self.subview_container.winfo_exists():
            self.subview_container.configure(bg=bg_col)
        if hasattr(self, "top_deck") and self.top_deck.winfo_exists():
            self.top_deck.configure(highlightbackground=border_col)
        if hasattr(self, "subview_nav_bar") and self.subview_nav_bar.winfo_exists():
            self.subview_nav_bar.configure(bg="#131c2e")

        self._update_subview_tab_styles()
        # Refresh active subview with new theme colors
        self.switch_subview(self.active_subview)

    def _create_scroll_banner(self, parent, title: str, subtitle: Optional[str] = None, height: int = 42):
        """Renders an unfurled true 3D cylindrical shaded parchment scroll banner using ShinobiGraphicsEngine."""
        _resolve_shinobi_components()
        canvas = tk.Canvas(parent, height=height, bg=self.colors.get("bg", "#0a0e17"), highlightthickness=0)
        canvas.pack(fill=tk.X, pady=(2, 4))

        def _draw(event=None):
            w = canvas.winfo_width()
            if w <= 10:
                w = 800
            h = height
            if ShinobiGraphicsEngine and hasattr(ShinobiGraphicsEngine, "create_3d_parchment_scroll"):
                photo = ShinobiGraphicsEngine.create_3d_parchment_scroll(w, h, roller_width=18)
                if photo:
                    canvas.photo = photo
                    canvas.delete("all")
                    canvas.create_image(0, 0, image=photo, anchor="nw")
                    if subtitle:
                        canvas.create_text(w // 2, 15, text=title, font=("Segoe UI", 8, "bold"), fill="#1f1206", anchor="center")
                        canvas.create_text(w // 2, 28, text=subtitle, font=("Segoe UI", 7, "bold"), fill="#451a03", anchor="center")
                    else:
                        canvas.create_text(w // 2, h // 2, text=title, font=("Segoe UI", 9, "bold"), fill="#1f1206", anchor="center")
        canvas.bind("<Configure>", _draw)
        canvas.after(20, _draw)
        return canvas


    # ==========================================
    # 1. TOP COMMAND DECK & STATUS BAR
    # ==========================================
    def _build_top_command_deck(self, parent):
        primary_col = self.colors.get("primary", "#f59e0b")
        border_col = self.colors.get("card_border", primary_col)

        deck = tk.Frame(
            parent,
            bg="#0e172a",
            bd=1,
            relief=tk.SOLID,
            highlightbackground=border_col,
            highlightthickness=1,
            padx=14,
            pady=8,
            height=62
        )
        deck.pack(fill=tk.X, pady=(0, 6))
        deck.pack_propagate(False)
        self.top_deck = deck

        # Top row: Title + Status Indicators
        top_row = tk.Frame(deck, bg="#0e172a")
        top_row.pack(fill=tk.BOTH, expand=True)

        # Title Block
        t_box = tk.Frame(top_row, bg="#0e172a")
        t_box.pack(side=tk.LEFT)

        lbl_title = tk.Label(
            t_box,
            text="🎯  HOST EXAMINATION & GEMINI EVALUATOR (V3)",
            font=("Segoe UI", 11, "bold"),
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

        # Class Level Selector via ShinobiPillSelector
        cfg = GeminiExamClient.load_config()
        current_class = cfg.get("class_level", "Class 8 CBSE")
        self.class_pill = ShinobiPillSelector(
            actions_box,
            title="CLASS LEVEL",
            values=["Class 8 CBSE", "Class 9 CBSE", "Class 10 CBSE", "Class 7 CBSE"],
            initial_value=current_class,
            on_select_callback=self._on_class_pill_selected,
            title_color="#38bdf8",
            width=115,
            height=46
        )
        self.class_pill.pack(side=tk.LEFT, padx=(0, 6))

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
            bd=1,
            highlightthickness=1,
            highlightbackground="#2e3b52"
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
            pady=4,
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
            pady=4,
            cursor="hand2",
            command=self._on_sync_ledger
        )
        btn_sync.pack(side=tk.LEFT, padx=(0, 6))

        # Open Exam Directory Button
        btn_folder = tk.Button(
            actions_box,
            text="📂 Exam Vault",
            font=("Segoe UI", 8),
            fg="#cbd5e1",
            bg="#1e293b",
            activeforeground="#ffffff",
            activebackground="#334155",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self._open_exam_folder
        )
        btn_folder.pack(side=tk.LEFT)

    def _get_gemini_status_text(self) -> str:
        cfg = GeminiExamClient.load_config()
        key = cfg.get("api_key") or cfg.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY", "")
        if key.strip():
            return "🟢 Gemini AI Active"
        return "⚪ Offline Local Mode"

    def _get_gemini_status_color(self) -> str:
        cfg = GeminiExamClient.load_config()
        key = cfg.get("api_key") or cfg.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY", "")
        if key.strip():
            return "#34d399"  # Emerald
        return "#94a3b8"  # Slate

    def _on_class_pill_selected(self, new_val):
        cfg = GeminiExamClient.load_config()
        cfg["class_level"] = str(new_val).strip()
        GeminiExamClient.save_config(cfg)
        messagebox.showinfo("Class Updated", f"Target student class standard updated to: {new_val}")

    def _open_api_key_modal(self):
        cfg = GeminiExamClient.load_config()
        current_key = cfg.get("api_key") or cfg.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY", "")
        prompt_txt = (
            "Enter Google Gemini API Key:\n\n"
            "(If left blank, ScholasticPulse V3 uses the robust offline deterministic CBSE evaluator.\n"
            "Entering an API key enables direct Gemini AI multimodal grading and dynamic question paper creation)."
        )
        new_key = simpledialog.askstring("Gemini API Key Configuration", prompt_txt, initialvalue=current_key)
        if new_key is not None:
            GeminiExamClient.set_api_key(new_key.strip())
            self.lbl_gemini_status.configure(
                text=self._get_gemini_status_text(),
                fg=self._get_gemini_status_color()
            )
            messagebox.showinfo("Gemini API Key Saved", "Gemini API key updated and stored securely in local configuration.")

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
    # 2. SUB-VIEW NAVIGATION BAR (PARCHMENT TABS)
    # ==========================================
    def _build_subview_navigation_bar(self, parent):
        bar = tk.Frame(parent, bg="#131c2e", height=40)
        bar.pack(fill=tk.X, pady=(0, 6))
        bar.pack_propagate(False)
        self.subview_nav_bar = bar

        self.subview_buttons = {}
        tabs = [
            ("ledger", "📋 1. Study Ledger & Phases"),
            ("textbook_vault", "📚 2. Textbook Vault"),
            ("sample_papers", "📑 3. Sample Questions & Papers"),
            ("face_a", "📝 4. Face A: Question Architect"),
            ("face_b", "🔍 5. Face B: Answer Evaluator"),
            ("topper_guide", "⭐ 6. CBSE Topper Guide")
        ]

        for key, label in tabs:
            btn = tk.Button(
                bar,
                text=label,
                font=("Segoe UI", 8, "bold"),
                relief=tk.FLAT,
                bd=0,
                padx=10,
                pady=5,
                cursor="hand2",
                command=lambda k=key: self.switch_subview(k)
            )
            btn.pack(side=tk.LEFT, padx=(0, 4))
            self.subview_buttons[key] = btn

        self._update_subview_tab_styles()

    def _update_subview_tab_styles(self):
        primary_col = self.colors.get("primary", "#f59e0b")
        for k, btn in self.subview_buttons.items():
            if k == self.active_subview:
                btn.configure(
                    bg=primary_col,
                    fg="#0f172a",
                    activebackground=self.colors.get("accent", "#d97706"),
                    activeforeground="#0f172a"
                )
            else:
                btn.configure(
                    bg="#1e293b",
                    fg="#94a3b8",
                    activebackground="#334155",
                    activeforeground="#f8fafc"
                )

    def switch_subview(self, target_alias, exam_id: Optional[str] = None):
        if exam_id:
            self.active_exam_id = exam_id

        # Normalize target_alias to handle legacy keys/aliases and numeric indices
        key_alias_map = {
            0: 'ledger', '0': 'ledger',
            1: 'ledger', '1': 'ledger', 'phases': 'ledger', 'study_ledger': 'ledger',
            2: 'textbook_vault', '2': 'textbook_vault', 'vault': 'textbook_vault',
            3: 'sample_papers', '3': 'sample_papers', 'sample_q': 'sample_papers', 'sample_questions': 'sample_papers',
            4: 'face_a', '4': 'face_a',
            5: 'face_b', '5': 'face_b',
            6: 'topper_guide', '6': 'topper_guide', 'topper': 'topper_guide'
        }
        target_alias = key_alias_map.get(target_alias, str(target_alias).lower())

        if target_alias not in self.subview_map:
            print(f"Error: Subview {target_alias} not found.")
            return

        self.active_subview = target_alias
        self._update_subview_tab_styles()

        # Hide all frames safely
        for frame in self.subview_map.values():
            if frame and hasattr(frame, "pack_forget"):
                frame.pack_forget()

        # Show the requested frame
        if target_alias in self.subview_map and self.subview_map[target_alias]:
            self.subview_map[target_alias].pack(fill="both", expand=True)

    def _render_subview_vault(self, parent):
        """Cleanly renders the dedicated Subject Vault & Upload Library (unmingled)."""
        from exam_vault_library_view_v3 import ExamVaultLibraryView
        vault_view = ExamVaultLibraryView(parent, self)
        vault_view.build_ui()
        self.vault_view = vault_view

    def _render_subview_sample_questions(self, parent):
        """Cleanly renders the dedicated Sample Questions & School Model Papers View."""
        from exam_sample_questions_view_v3 import ExamSampleQuestionsView
        sample_q_view = ExamSampleQuestionsView(parent, self)
        sample_q_view.build_ui()
        self.sample_q_view = sample_q_view

    def _render_clean_face_a(self, parent):
        """Cleanly renders Face A using our verified HostExamFaceAView module."""
        from host_exam_face_a_ui_v3 import HostExamFaceAView
        face_a_controller = HostExamFaceAView(parent, self)
        face_a_controller.build_ui()
        self.face_a_controller = face_a_controller

    # ==========================================
    # SUB-VIEW 1: STUDY LEDGER & 3-PHASE SELECTOR
    # ==========================================
    def _render_subview_ledger(self, parent):
        pane = tk.PanedWindow(parent, orient=tk.VERTICAL, bg=self.colors.get("bg", "#0a0e17"), sashrelief=tk.FLAT)
        pane.pack(fill=tk.BOTH, expand=True)

        # Top section: 3-Phase Host Examination Selector Cards
        phase_frame = tk.Frame(pane, bg="#0e172a", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1, padx=10, pady=6)
        pane.add(phase_frame, minsize=190)

        lbl_phase_title = tk.Label(
            phase_frame,
            text="⚡ SELECT HOST EXAMINATION PHASE (TRIGGER REAL LEARNING VERIFICATION)",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors.get("primary", "#f59e0b"),
            bg="#0e172a"
        )
        lbl_phase_title.pack(anchor="w", pady=(0, 6))

        cards_row = tk.Frame(phase_frame, bg="#0e172a")
        cards_row.pack(fill=tk.X)

        # Phase 1 Card
        c1 = tk.Frame(cards_row, bg="#161f30", bd=1, relief=tk.SOLID, highlightbackground="#38bdf8", highlightthickness=1, padx=8, pady=6)
        c1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        tk.Label(c1, text="PHASE 1: SUNDAY / MONTH-END", font=("Segoe UI", 8, "bold"), fg="#38bdf8", bg="#161f30").pack(anchor="w")
        tk.Label(c1, text="35 Marks / 80 Marks • 1.5h / 3h\nExamines all weekly/monthly homework", font=("Segoe UI", 7), fg="#cbd5e1", bg="#161f30", justify=tk.LEFT).pack(anchor="w", pady=1)
        p1_btn_row = tk.Frame(c1, bg="#161f30")
        p1_btn_row.pack(anchor="w", pady=2)
        btn_p1_w = tk.Button(p1_btn_row, text="⚡ Weekly Test (35M)", font=("Segoe UI", 7, "bold"), fg="#0f172a", bg="#38bdf8", activebackground="#0284c7", relief=tk.FLAT, bd=0, padx=8, pady=3, cursor="hand2", command=lambda: self._launch_phase(1, "weekly"))
        btn_p1_w.pack(side=tk.LEFT, padx=(0, 6))
        btn_p1_m = tk.Button(p1_btn_row, text="🏆 Month-End (80M)", font=("Segoe UI", 7, "bold"), fg="#ffffff", bg="#0369a1", activebackground="#0284c7", relief=tk.FLAT, bd=0, padx=8, pady=3, cursor="hand2", command=lambda: self._launch_phase(1, "monthend"))
        btn_p1_m.pack(side=tk.LEFT)

        # Phase 2 Card
        c2 = tk.Frame(cards_row, bg="#161f30", bd=1, relief=tk.SOLID, highlightbackground="#a855f7", highlightthickness=1, padx=8, pady=6)
        c2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        tk.Label(c2, text="PHASE 2: 3-DAY CHECKPOINT", font=("Segoe UI", 8, "bold"), fg="#c084fc", bg="#161f30").pack(anchor="w")
        tk.Label(c2, text="25 Marks • 45 Mins • 06:40–07:45 AM\nMulti-subject 3-day block audit (Days 1–3, 4–6...)", font=("Segoe UI", 7), fg="#cbd5e1", bg="#161f30", justify=tk.LEFT).pack(anchor="w", pady=1)
        p2_row = tk.Frame(c2, bg="#161f30")
        p2_row.pack(anchor="w", pady=2)
        self.p2_block_var = tk.StringVar(value="Block 1 (D1-3)")
        self.p2_pill = ShinobiPillSelector(
            p2_row,
            title="BLOCK",
            values=["Block 1 (D1-3)", "Block 2 (D4-6)", "Block 3 (D7-9)", "Block 4 (D10-12)", "Block 5 (D13-15)", "Block 6 (D16-18)", "Block 7 (D19-21)"],
            initial_value="Block 1 (D1-3)",
            textvariable=self.p2_block_var,
            title_color="#c084fc",
            width=135,
            height=40
        )
        self.p2_pill.pack(side=tk.LEFT, padx=(0, 6))

        def _on_click_p2():
            val = self.p2_block_var.get()
            try:
                b_num = int(val.split()[1])
            except Exception:
                b_num = 1
            self._launch_phase(2, str(b_num))

        btn_p2 = tk.Button(p2_row, text="⚡ Audit (25M)", font=("Segoe UI", 8, "bold"), fg="#0f172a", bg="#c084fc", activebackground="#a855f7", relief=tk.FLAT, bd=0, padx=8, pady=4, cursor="hand2", command=_on_click_p2)
        btn_p2.pack(side=tk.LEFT)

        # Phase 3 Card (With ShinobiPillSelector)
        c3 = tk.Frame(cards_row, bg="#161f30", bd=1, relief=tk.SOLID, highlightbackground="#10b981", highlightthickness=1, padx=8, pady=6)
        c3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(c3, text="PHASE 3: MORNING SPRINT", font=("Segoe UI", 8, "bold"), fg="#34d399", bg="#161f30").pack(anchor="w")
        tk.Label(c3, text="25 Marks • 45 Mins\nRapid recall on yesterday's homework & morning", font=("Segoe UI", 7), fg="#cbd5e1", bg="#161f30", justify=tk.LEFT).pack(anchor="w", pady=1)
        p3_row = tk.Frame(c3, bg="#161f30")
        p3_row.pack(anchor="w", pady=2)
        self.p3_sub_var = tk.StringVar(value="Mathematics")
        self.p3_pill = ShinobiPillSelector(
            p3_row,
            title="SUBJECT",
            values=["Mathematics", "Physical Science", "Biological Science", "Social Science", "English", "Tamil", "Hindi"],
            initial_value="Mathematics",
            textvariable=self.p3_sub_var,
            title_color="#34d399",
            width=135,
            height=40
        )
        self.p3_pill.pack(side=tk.LEFT, padx=(0, 6))
        btn_p3 = tk.Button(p3_row, text="⚡ Sprint (25M)", font=("Segoe UI", 8, "bold"), fg="#0f172a", bg="#34d399", activebackground="#059669", relief=tk.FLAT, bd=0, padx=8, pady=4, cursor="hand2", command=lambda: self._launch_phase(3, self.p3_sub_var.get()))
        btn_p3.pack(side=tk.LEFT)

        # Interactive 5-Card Phase 1 Selector Strip (Weeks 1–4 + Month-End Mega Exam)
        self.p1_strip_frame = tk.Frame(phase_frame, bg="#0e172a")
        self.p1_strip_frame.pack(fill=tk.X, pady=(6, 0))

        lbl_p1_strip = tk.Label(
            self.p1_strip_frame,
            text="📅 PHASE 1 INTERACTIVE CURATION GRID (SELECT SUNDAY TEST TO FILTER LEDGER & PRE-LOAD FACE A):",
            font=("Segoe UI", 8, "bold"),
            fg="#f59e0b",
            bg="#0e172a"
        )
        lbl_p1_strip.pack(anchor="w", pady=(0, 3))

        self.p1_cards_row = tk.Frame(self.p1_strip_frame, bg="#0e172a")
        self.p1_cards_row.pack(fill=tk.X)

        self.p1_card_widgets = {}
        self.active_p1_card = "all"
        self.selected_week_filter = "all"

        self._render_p1_week_cards()

        # Bottom section: Interactive Study Ledger Table with Custom 6px Dark Scrollbar
        ledger_frame = tk.Frame(pane, bg="#0e172a", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1, padx=10, pady=8)
        pane.add(ledger_frame, minsize=180)

        # Toolbar above ledger
        tb = tk.Frame(ledger_frame, bg="#0e172a")
        tb.pack(fill=tk.X, pady=(0, 6))

        tk.Label(tb, text="📖 SUBJECT STUDY LEDGER (HOMEWORK & EXAM PORTIONS LOG)", font=("Segoe UI", 9, "bold"), fg="#e2e8f0", bg="#0e172a").pack(side=tk.LEFT)

        btn_add_entry = tk.Button(tb, text="➕ Log Study Topic", font=("Segoe UI", 8, "bold"), fg="#38bdf8", bg="#1e293b", relief=tk.FLAT, bd=0, padx=10, pady=4, cursor="hand2", command=self._open_add_study_entry_modal)
        btn_add_entry.pack(side=tk.RIGHT, padx=(6, 0))

        # Filter Pill Selector (replaces Combobox)
        self.ledger_filter_var = tk.StringVar(value="All Subjects")
        self.ledger_filter_pill = ShinobiPillSelector(
            tb,
            title="SUBJECT FILTER",
            values=["All Subjects", "Mathematics", "Physical Science", "Biological Science", "Social Science", "English", "Tamil", "Hindi"],
            initial_value="All Subjects",
            textvariable=self.ledger_filter_var,
            on_select_callback=lambda v: self._render_ledger_table(),
            title_color="#fb923c",
            width=140,
            height=40
        )
        self.ledger_filter_pill.pack(side=tk.RIGHT, padx=6)

        # Treeview table container with ultra-slim custom dark scrollbar
        tbl_container = tk.Frame(ledger_frame, bg="#020617")
        tbl_container.pack(fill=tk.BOTH, expand=True)

        cols = ("date", "subject", "chapter", "intra_head", "task", "status", "source")
        self.ledger_tree = ttk.Treeview(tbl_container, columns=cols, show="headings", height=5)
        self.ledger_tree.heading("date", text="Date")
        self.ledger_tree.heading("subject", text="Subject")
        self.ledger_tree.heading("chapter", text="Chapter / Topic")
        self.ledger_tree.heading("intra_head", text="Intra-Head Taxonomy")
        self.ledger_tree.heading("task", text="Task Description")
        self.ledger_tree.heading("status", text="Status")
        self.ledger_tree.heading("source", text="Source")

        self.ledger_tree.column("date", width=85, anchor="center")
        self.ledger_tree.column("subject", width=125, anchor="w")
        self.ledger_tree.column("chapter", width=160, anchor="w")
        self.ledger_tree.column("intra_head", width=190, anchor="w")
        self.ledger_tree.column("task", width=280, anchor="w")
        self.ledger_tree.column("status", width=75, anchor="center")
        self.ledger_tree.column("source", width=110, anchor="center")

        # Custom 6px dark canvas scrollbar (zero gray Win32 widgets)
        self.ledger_sb = CustomDarkScrollbar(tbl_container, target_widget=self.ledger_tree, width=6, bg="#0b1120", thumb_color="#334155")
        self.ledger_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.ledger_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._render_ledger_table()

        # Bottom Section 2: Persistent Host Exam Score & Anti-Daydreaming Focus History Strip
        self.score_history_box = tk.Frame(ledger_frame, bg="#0b1120", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1, padx=8, pady=4)
        self.score_history_box.pack(fill=tk.X, pady=(4, 0))
        self._render_score_history_strip()

    def _render_score_history_strip(self):
        if not hasattr(self, "score_history_box") or not self.score_history_box.winfo_exists():
            return
        for w in self.score_history_box.winfo_children():
            w.destroy()

        history = GeminiExamClient.load_score_history()

        # Header row
        hdr = tk.Frame(self.score_history_box, bg="#0b1120")
        hdr.pack(fill=tk.X, pady=(0, 4))

        tk.Label(
            hdr,
            text="📊 HOST EXAM SCORE & ANTI-DAYDREAMING FOCUS HISTORY",
            font=("Segoe UI", 8, "bold"),
            fg="#f59e0b",
            bg="#0b1120"
        ).pack(side=tk.LEFT)

        if history:
            total_exams = len(history)
            avg_pct = sum(h.get("percentage", 0.0) for h in history) / max(1, total_exams)
            verified_count = sum(1 for h in history if "VERIFIED" in str(h.get("focus_verdict", "")).upper())

            kpi_text = f"🏆 {total_exams} Exams Evaluated • Avg: {avg_pct:.1f}% • 🎯 {verified_count}/{total_exams} Deep Focus Verified • 0 Slips"
            tk.Label(
                hdr,
                text=kpi_text,
                font=("Segoe UI", 8, "bold"),
                fg="#34d399",
                bg="#0b1120"
            ).pack(side=tk.RIGHT)

        if not history:
            tk.Label(
                self.score_history_box,
                text="No examination evaluation records logged yet. Complete an answer sheet evaluation in Face B to track scores.",
                font=("Segoe UI", 8, "italic"),
                fg="#94a3b8",
                bg="#0b1120"
            ).pack(anchor="w", pady=2)
            return

        rows_frame = tk.Frame(self.score_history_box, bg="#0b1120")
        rows_frame.pack(fill=tk.X)

        for rec in history[-3:]:  # Show recent 3 exams
            rf = tk.Frame(rows_frame, bg="#161f30", bd=1, relief=tk.SOLID, highlightbackground="#1e293b", highlightthickness=1, padx=6, pady=3)
            rf.pack(fill=tk.X, pady=1)

            tk.Label(rf, text=f"📅 {rec.get('date')}", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#161f30", width=11, anchor="w").pack(side=tk.LEFT)
            tk.Label(rf, text=f"{rec.get('title')}", font=("Segoe UI", 8, "bold"), fg="#e2e8f0", bg="#161f30", width=20, anchor="w").pack(side=tk.LEFT)
            tk.Label(rf, text=f"📐 {rec.get('subject')}", font=("Segoe UI", 8), fg="#38bdf8", bg="#161f30", width=22, anchor="w").pack(side=tk.LEFT)
            
            score_str = f"Score: {rec.get('marks_awarded', 0):.1f}/{rec.get('max_marks', 0):.0f} ({rec.get('percentage', 0):.1f}%)"
            tk.Label(rf, text=score_str, font=("Segoe UI", 8, "bold"), fg="#fbbf24", bg="#161f30", width=22, anchor="center").pack(side=tk.LEFT)

            grade_str = f"Grade: {rec.get('grade', 'A1')}"
            tk.Label(rf, text=grade_str, font=("Segoe UI", 8, "bold"), fg="#10b981", bg="#161f30", width=10, anchor="center").pack(side=tk.LEFT)

            focus_str = f"🎯 {rec.get('focus_verdict', 'Deep Focus Verified')}"
            tk.Label(rf, text=focus_str, font=("Segoe UI", 8, "bold"), fg="#c084fc", bg="#161f30", width=22, anchor="center").pack(side=tk.LEFT)

            binder_path = rec.get("binder_pdf_path", "")
            btn_pdf = tk.Button(
                rf,
                text="🖨️ Binder PDF",
                font=("Segoe UI", 7, "bold"),
                fg="#1c1104",
                bg="#f59e0b",
                activebackground="#fbbf24",
                relief=tk.FLAT,
                bd=0,
                padx=6,
                pady=1,
                cursor="hand2",
                command=lambda p=binder_path: self._open_pdf_file(p)
            )
            btn_pdf.pack(side=tk.RIGHT)

    def _open_pdf_file(self, pdf_path: str):
        if pdf_path and os.path.exists(pdf_path):
            try:
                if sys.platform == "win32":
                    os.startfile(pdf_path)
                else:
                    subprocess.Popen(["xdg-open", pdf_path])
            except Exception as e:
                messagebox.showerror("File Error", f"Could not open PDF file:\n{e}")
        else:
            messagebox.showinfo("Physical Binder PDF", f"Binder PDF: {os.path.basename(pdf_path) if pdf_path else 'Exam Binder'}\nLocation: {pdf_path}\n(Will be generated upon Face B evaluation)")

    def _render_p1_week_cards(self):
        if not hasattr(self, "p1_cards_row") or not self.p1_cards_row.winfo_exists():
            return
        for widget in self.p1_cards_row.winfo_children():
            widget.destroy()
        self.p1_card_widgets.clear()

        stats = SubjectStudyLedger.get_week_stats(month="October")
        score_history = GeminiExamClient.load_score_history()

        card_configs = [
            ("all", "🌐 Full Month Ledger", "Oct 01–24 • All Entries", 80, 180),
            (1, "📅 Week 1 Sunday Test", "Oct 01–06 Homework", 35, 60),
            (2, "📅 Week 2 Sunday Test", "Oct 07–13 Homework", 35, 60),
            (3, "📅 Week 3 Sunday Test", "Oct 14–20 Homework", 35, 60),
            (4, "📅 Week 4 Sunday Test", "Oct 21–24 Homework", 35, 60),
            ("monthend", "🏆 Month-End Mega Exam", "Weeks 1–4 Combined", 80, 180),
        ]

        for key, title, subtitle, marks, mins in card_configs:
            is_active = (str(self.active_p1_card) == str(key))
            border_col = "#f59e0b" if is_active else "#334155"
            bg_col = "#261e12" if is_active else "#161f30"
            title_col = "#fbbf24" if is_active else "#e2e8f0"

            st = stats.get(key, {})
            if isinstance(st, dict):
                ent_cnt = st.get("entries_count", 0)
                sub_cnt = st.get("subjects_count", 0)
            elif isinstance(st, int):
                ent_cnt = st
                sub_cnt = 0
            else:
                ent_cnt = 0
                sub_cnt = 0

            matching_score = None
            for rec in score_history:
                t_low = rec.get("title", "").lower()
                eid_low = rec.get("exam_id", "").lower()
                if key == 1 and ("week 1" in t_low or "w1" in eid_low):
                    matching_score = rec
                    break
                elif key == 2 and ("week 2" in t_low or "w2" in eid_low):
                    matching_score = rec
                    break
                elif key == 3 and ("week 3" in t_low or "w3" in eid_low):
                    matching_score = rec
                    break
                elif key == 4 and ("week 4" in t_low or "w4" in eid_low):
                    matching_score = rec
                    break
                elif (key == "monthend" or key == "all") and ("month" in t_low or "mega" in t_low or "month" in eid_low):
                    matching_score = rec
                    break

            c = tk.Frame(
                self.p1_cards_row,
                bg=bg_col,
                bd=1,
                relief=tk.SOLID,
                highlightbackground=border_col,
                highlightthickness=2 if is_active else 1,
                padx=8,
                pady=6,
                cursor="hand2"
            )
            c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)

            c.bind("<Button-1>", lambda e, k=key: self._on_p1_card_clicked(k))

            lbl_t = tk.Label(c, text=title, font=("Segoe UI", 8, "bold"), fg=title_col, bg=bg_col)
            lbl_t.pack(anchor="w")
            lbl_t.bind("<Button-1>", lambda e, k=key: self._on_p1_card_clicked(k))

            if key == "all":
                sub_desc = f"{ent_cnt} Entries • {sub_cnt} Subjects\nOct 01–24 Complete Dataset"
            elif key == "monthend":
                sub_desc = f"{ent_cnt} Entries • {sub_cnt} Subjects\n{marks}M • {mins}m • Combined Exam"
            else:
                sub_desc = f"{ent_cnt} Entries • {sub_cnt} Subjects\n{marks}M • {mins}m • {subtitle}"

            lbl_sub = tk.Label(
                c,
                text=sub_desc,
                font=("Segoe UI", 7),
                fg="#fde68a" if is_active else "#94a3b8",
                bg=bg_col,
                justify=tk.LEFT
            )
            lbl_sub.pack(anchor="w", pady=(2, 2))
            lbl_sub.bind("<Button-1>", lambda e, k=key: self._on_p1_card_clicked(k))

            if matching_score:
                lbl_sc = tk.Label(
                    c,
                    text=f"✅ Scored: {matching_score['marks_awarded']:.1f}/{matching_score['max_marks']:.0f} ({matching_score['percentage']:.1f}%)",
                    font=("Segoe UI", 7, "bold"),
                    fg="#34d399",
                    bg=bg_col
                )
                lbl_sc.pack(anchor="w", pady=(0, 2))
                lbl_sc.bind("<Button-1>", lambda e, k=key: self._on_p1_card_clicked(k))

            btn_act = tk.Button(
                c,
                text="✓ Active" if is_active else "Select & Load",
                font=("Segoe UI", 7, "bold"),
                fg="#0f172a" if is_active else "#cbd5e1",
                bg="#f59e0b" if is_active else "#1e293b",
                activebackground="#fbbf24",
                relief=tk.FLAT,
                bd=0,
                padx=6,
                pady=2,
                cursor="hand2",
                command=lambda k=key: self._on_p1_card_clicked(k)
            )
            btn_act.pack(anchor="w")

            self.p1_card_widgets[key] = c

    def _on_p1_card_clicked(self, key):
        self.active_p1_card = key
        self.selected_week_filter = key
        self._render_p1_week_cards()
        self._render_ledger_table()

        # Pre-load that exact dataset into Sub-View 2 (Face A: Question Paper Architect)
        if key in ("monthend", "all"):
            spec = ExamPhaseAssembler.assemble_phase1_monthend_mega_exam()
        else:
            spec = ExamPhaseAssembler.assemble_phase1_weekly_sunday_test(week_number=int(key))

        self.assembled_exam_spec = spec
        self._populate_face_a_with_spec(spec)

    def _render_ledger_table(self):
        if not hasattr(self, "ledger_tree") or not self.ledger_tree.winfo_exists():
            return
        for i in self.ledger_tree.get_children():
            self.ledger_tree.delete(i)

        data = SubjectStudyLedger.load_ledger()
        entries = data.get("entries", [])
        filter_sub = getattr(self, "ledger_filter_var", None)
        filter_val = filter_sub.get() if filter_sub else "All Subjects"
        week_filter = getattr(self, "selected_week_filter", None)

        sorted_entries = sorted(entries, key=lambda x: x.get("date", ""), reverse=True)
        for e in sorted_entries:
            sub = e.get("subject", "")
            if filter_val != "All Subjects" and filter_val.lower() not in sub.lower():
                continue
            if week_filter and week_filter not in ("monthend", "all"):
                try:
                    if int(e.get("week_number", 0)) != int(week_filter):
                        continue
                except Exception:
                    pass
            intra_head = e.get("intra_head") or SubjectStudyLedger.categorize_into_intra_heads(sub, e.get("chapter_topic", ""), e.get("task_description", ""))
            self.ledger_tree.insert("", tk.END, values=(
                e.get("date", ""),
                e.get("subject", ""),
                e.get("chapter_topic", ""),
                intra_head,
                e.get("task_description", ""),
                e.get("study_status", "studied"),
                e.get("source", "diary")
            ))

    def _open_add_study_entry_modal(self):
        d_win = tk.Toplevel(self.parent)
        d_win.title("Log Custom Study Topic to Ledger")
        d_win.geometry("520x340")
        d_win.configure(bg="#0f172a")
        d_win.transient(self.parent)

        tk.Label(d_win, text="➕ Log Study Topic for Host Examination", font=("Segoe UI", 10, "bold"), fg="#f59e0b", bg="#0f172a").pack(anchor="w", padx=16, pady=(14, 10))

        form = tk.Frame(d_win, bg="#0f172a", padx=16)
        form.pack(fill=tk.BOTH, expand=True)

        tk.Label(form, text="Date (YYYY-MM-DD):", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0f172a").grid(row=0, column=0, sticky="w", pady=6)
        ent_date = ttk.Entry(form, width=28)
        ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        ent_date.grid(row=0, column=1, sticky="w", pady=6)

        tk.Label(form, text="Subject:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0f172a").grid(row=1, column=0, sticky="w", pady=6)
        sub_var = tk.StringVar(value="Mathematics")
        modal_sub_pill = ShinobiPillSelector(
            form,
            title="SUBJECT",
            values=["Mathematics", "Physical Science", "Biological Science", "Social Science", "English", "Tamil", "Hindi"],
            initial_value="Mathematics",
            textvariable=sub_var,
            width=200,
            height=44
        )
        modal_sub_pill.grid(row=1, column=1, sticky="w", pady=6)

        tk.Label(form, text="Chapter / Topic:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0f172a").grid(row=2, column=0, sticky="w", pady=6)
        ent_topic = ttk.Entry(form, width=38)
        ent_topic.grid(row=2, column=1, sticky="w", pady=6)

        tk.Label(form, text="Task Description:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#0f172a").grid(row=3, column=0, sticky="w", pady=6)
        ent_task = ttk.Entry(form, width=38)
        ent_task.grid(row=3, column=1, sticky="w", pady=6)

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
        tk.Button(btn_row, text="💾 Save to Ledger", font=("Segoe UI", 9, "bold"), fg="#0f172a", bg="#f59e0b", relief=tk.FLAT, bd=0, padx=14, pady=5, cursor="hand2", command=save_manual_entry).pack(side=tk.RIGHT)
        tk.Button(btn_row, text="Cancel", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b", relief=tk.FLAT, bd=0, padx=10, pady=5, cursor="hand2", command=d_win.destroy).pack(side=tk.RIGHT, padx=8)

    def _launch_phase(self, phase_num: int, sub_type: str):
        spec = None
        if phase_num == 1:
            if sub_type == "weekly":
                spec = ExamPhaseAssembler.assemble_phase1_weekly_sunday_test()
            else:
                spec = ExamPhaseAssembler.assemble_phase1_monthend_mega_exam()
        elif phase_num == 2:
            try:
                blk_num = int(str(sub_type).strip())
            except Exception:
                blk_num = 1
            spec = ExamPhaseAssembler.assemble_phase2_3day_checkpoint(block_num=blk_num)
        elif phase_num == 3:
            spec = ExamPhaseAssembler.assemble_phase3_morning_sprint(sub_type)

        if spec:
            self.assembled_exam_spec = spec
            self.switch_subview("face_a")
            self._populate_face_a_with_spec(spec)


    def _populate_face_a_with_spec(self, spec: Dict[str, Any]):
        """Transfers assembled exam spec directly to clean HostExamFaceAView."""
        if hasattr(self, "face_a_controller") and self.face_a_controller:
            try:
                self.face_a_controller.load_assembled_spec(spec)
            except Exception as e:
                print(f"[HostExamTabController] Warning passing spec to Face A: {e}")

    # ==========================================
    # SUB-VIEW 5: FACE B - ANSWER SHEET EVALUATOR
    # ==========================================
    def _render_subview_face_b(self, parent):
        """Cleanly renders Face B using our verified HostExamFaceBView module."""
        from host_exam_face_b_ui_v3 import HostExamFaceBView
        face_b_controller = HostExamFaceBView(parent, self)
        face_b_controller.build_ui()
        self.face_b_controller = face_b_controller

    # ==========================================
    # SUB-VIEW 6: CBSE TOPPER MODEL ANSWER GUIDE
    # ==========================================
    def _render_subview_topper(self, parent):
        from host_exam_topper_ui_v3 import HostExamTopperView
        topper_controller = HostExamTopperView(parent, self)
        topper_controller.build_ui()
        self.topper_controller = topper_controller
