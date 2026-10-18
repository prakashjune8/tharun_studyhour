"""
host_exam_topper_ui_v3.py - CBSE Topper Model Answer Guide & Evaluation Desktop UI (V3)
-----------------------------------------------------------------------------------------
Interactive Desktop View for Step 7:
1. Renders the official CBSE step-wise evaluated score card and red-ink soft copy.
2. Side-by-side comparative analysis of Tharun's responses vs. CBSE 100/100 Topper scripts.
3. Displays P-E-E-D protocol (Point -> Explanation -> Example -> Derivation/Diagram Box).
4. Direct launch buttons for Graded Soft Copy HTML/PDF and Topper Model Guide HTML/PDF.
"""

import os
import sys
import json
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Optional

if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from exam_evaluator_v3 import CBSEEvaluatorV3, CORRECTED_COPIES_DIR, TOPPER_GUIDES_DIR
from host_exam_face_b_ui_v3 import CustomDarkScrollbar


class HostExamTopperView:
    """
    Step 7 Desktop UI: CBSE AI Evaluator & 100/100 Topper Model Guide.
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

        self.available_evaluations = self._list_available_evaluations()
        active_id = getattr(controller, "active_exam_id", None)
        if active_id and active_id in self.available_evaluations:
            default_val = active_id
        else:
            default_val = self.available_evaluations[0] if self.available_evaluations else ""
        self.selected_exam_var = tk.StringVar(value=default_val)
        self.active_tab = "graded"  # "graded" or "topper"
        self.active_record: Optional[Dict[str, Any]] = None

    def _list_available_evaluations(self) -> List[str]:
        """Lists exam IDs with available evaluations, newest first."""
        exams = []
        if os.path.exists(CORRECTED_COPIES_DIR):
            files = [fn for fn in os.listdir(CORRECTED_COPIES_DIR) if fn.endswith("_evaluation.json")]
            files.sort(key=lambda fn: os.path.getmtime(os.path.join(CORRECTED_COPIES_DIR, fn)), reverse=True)
            for fn in files:
                eid = fn.replace("_evaluation.json", "")
                exams.append(eid)
        if not exams:
            # Fallback to current verified exam
            exams = ["EXAM-MAT-DAI-20261018-664F52"]
        return exams

    def build_ui(self):
        """Constructs the high-definition Topper & Evaluator UI."""
        active_id = getattr(self.controller, "active_exam_id", None)
        if active_id and active_id in self.available_evaluations:
            self.selected_exam_var.set(active_id)

        for w in self.parent.winfo_children():
            w.destroy()

        container = tk.Frame(self.parent, bg=self.colors.get("bg", "#0a0e17"), padx=14, pady=10)
        container.pack(fill=tk.BOTH, expand=True)

        # -------------------------------------------------------------
        # TOP HEADER: KPI BANNER & EXAM SELECTOR
        # -------------------------------------------------------------
        hdr = tk.Frame(container, bg="#131c2e", padx=16, pady=10, relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground=self.colors.get("card_border", "#334155"))
        hdr.pack(fill=tk.X, pady=(0, 8))

        row1 = tk.Frame(hdr, bg="#131c2e")
        row1.pack(fill=tk.X)

        tk.Label(
            row1,
            text="⭐ STEP 7: CBSE AI EVALUATION & 100/100 TOPPER MODEL GUIDE",
            font=("Segoe UI", 11, "bold"),
            fg="#fbbf24",
            bg="#131c2e"
        ).pack(side=tk.LEFT)

        # Right Action Buttons
        btn_box = tk.Frame(row1, bg="#131c2e")
        btn_box.pack(side=tk.RIGHT)

        tk.Button(
            btn_box,
            text="📄 View Graded Copy (HTML)",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#dc2626",
            activebackground="#b91c1c",
            relief=tk.FLAT,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self._open_graded_html
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            btn_box,
            text="🏆 View Topper Guide (HTML)",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#059669",
            activebackground="#047857",
            relief=tk.FLAT,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self._open_topper_html
        ).pack(side=tk.LEFT, padx=3)

        # Row 2: Exam Selector & KPI Pill
        row2 = tk.Frame(hdr, bg="#131c2e")
        row2.pack(fill=tk.X, pady=(8, 0))

        tk.Label(row2, text="Select Evaluated Exam:", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#131c2e").pack(side=tk.LEFT)
        combo = ttk.Combobox(row2, textvariable=self.selected_exam_var, values=self.available_evaluations, state="readonly", width=36)
        combo.pack(side=tk.LEFT, padx=(6, 14))
        combo.bind("<<ComboboxSelected>>", lambda e: self.load_and_render_evaluation())

        self.lbl_score_kpi = tk.Label(
            row2,
            text="🏆 SCORE: 17 / 17 MARKS (100.0%) • A1 EXEMPLARY",
            font=("Segoe UI", 9, "bold"),
            fg="#10b981",
            bg="#064e3b",
            padx=10,
            pady=2
        )
        self.lbl_score_kpi.pack(side=tk.LEFT)

        self.lbl_verdict = tk.Label(
            hdr,
            text="CBSE Senior Examiner Verdict: Flawless mathematical derivations, explicit formula definitions, and correct units.",
            font=("Segoe UI", 8, "italic"),
            fg="#cbd5e1",
            bg="#131c2e"
        )
        self.lbl_verdict.pack(anchor="w", pady=(6, 0))

        # -------------------------------------------------------------
        # TAB SELECTOR: GRADED SCRIPT vs TOPPER GUIDE
        # -------------------------------------------------------------
        tab_bar = tk.Frame(container, bg="#0a0e17")
        tab_bar.pack(fill=tk.X, pady=(0, 6))

        self.btn_tab_graded = tk.Button(
            tab_bar,
            text="🔴 Red-Ink Graded Answer Script (Tharun)",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#dc2626",
            activebackground="#b91c1c",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self._switch_tab("graded")
        )
        self.btn_tab_graded.pack(side=tk.LEFT, padx=(0, 4))

        self.btn_tab_topper = tk.Button(
            tab_bar,
            text="🏆 CBSE 100/100 Topper Reference Model (P-E-E-D)",
            font=("Segoe UI", 8, "bold"),
            fg="#94a3b8",
            bg="#1e293b",
            activebackground="#334155",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self._switch_tab("topper")
        )
        self.btn_tab_topper.pack(side=tk.LEFT)

        # -------------------------------------------------------------
        # SCROLLABLE WORKSPACE FOR QUESTION CARDS
        # -------------------------------------------------------------
        canvas_frame = tk.Frame(container, bg="#090d16", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="#090d16", highlightthickness=0, bd=0)
        self.scrollbar = CustomDarkScrollbar(canvas_frame, target_widget=self.canvas, width=6, bg="#0b1120", thumb_color="#334155")
        self.cards_inner = tk.Frame(self.canvas, bg="#090d16")

        self.cards_window = self.canvas.create_window((0, 0), window=self.cards_inner, anchor="nw")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.cards_inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.cards_window, width=e.width))

        # Initial load
        self.load_and_render_evaluation()

    def _switch_tab(self, tab_key: str):
        self.active_tab = tab_key
        if tab_key == "graded":
            self.btn_tab_graded.configure(bg="#dc2626", fg="#ffffff")
            self.btn_tab_topper.configure(bg="#1e293b", fg="#94a3b8")
        else:
            self.btn_tab_graded.configure(bg="#1e293b", fg="#94a3b8")
            self.btn_tab_topper.configure(bg="#059669", fg="#ffffff")
        self._render_cards()

    def load_and_render_evaluation(self):
        """Loads evaluation record from JSON or runs CBSEEvaluatorV3."""
        exam_id = self.selected_exam_var.get()
        if not exam_id:
            return

        eval_file = os.path.join(CORRECTED_COPIES_DIR, f"{exam_id}_evaluation.json")
        if not os.path.exists(eval_file):
            try:
                self.active_record = CBSEEvaluatorV3.evaluate_exam(exam_id)
            except Exception as e:
                messagebox.showerror("Evaluation Error", f"Could not evaluate {exam_id}: {e}")
                return
        else:
            with open(eval_file, "r", encoding="utf-8") as f:
                self.active_record = json.load(f)

        # Update KPI Header
        if self.active_record:
            import html
            awd = self.active_record.get("total_marks_awarded", 0)
            poss = self.active_record.get("total_marks_possible", 0)
            pct = self.active_record.get("percentage", 100)
            grd = self.active_record.get("grade", "A1")
            verdict = html.unescape(self.active_record.get('evaluator_verdict', ''))
            self.lbl_score_kpi.configure(text=f"🏆 SCORE: {awd} / {poss} MARKS ({pct}%) • {grd}")
            self.lbl_verdict.configure(text=f"CBSE Senior Examiner Verdict: {verdict}")

        self._render_cards()

    def _render_cards(self):
        """Renders the question cards according to active tab."""
        import html
        for w in self.cards_inner.winfo_children():
            w.destroy()

        if not self.active_record:
            return

        for q in self.active_record.get("step_breakdown", []):
            card = tk.Frame(self.cards_inner, bg="#131c2e", bd=1, relief=tk.SOLID, highlightbackground="#334155", highlightthickness=1, padx=12, pady=10)
            card.pack(fill=tk.X, padx=10, pady=(0, 10))

            # Header row
            q_hdr = tk.Frame(card, bg="#131c2e")
            q_hdr.pack(fill=tk.X, pady=(0, 6))

            q_txt_clean = html.unescape(q.get("question_text", ""))
            tk.Label(
                q_hdr,
                text=f"{q['question_number']}. {q_txt_clean}",
                font=("Segoe UI", 9, "bold"),
                fg="#f8fafc",
                bg="#131c2e",
                wraplength=840,
                justify=tk.LEFT
            ).pack(side=tk.LEFT)

            score_tag = f"✔ {q['awarded_marks']} / {q['max_marks']}M"
            tk.Label(
                q_hdr,
                text=score_tag,
                font=("Segoe UI", 8, "bold"),
                fg="#10b981",
                bg="#064e3b",
                padx=8,
                pady=2
            ).pack(side=tk.RIGHT)

            if self.active_tab == "graded":
                # Tharun's evaluated answer script
                ans_box = tk.Frame(card, bg="#0d1522", bd=1, relief=tk.SOLID, highlightbackground="#2563eb", highlightthickness=1, padx=10, pady=8)
                ans_box.pack(fill=tk.X, pady=(0, 6))

                student_ans_clean = html.unescape(q.get("student_response", ""))
                tk.Label(ans_box, text="✍️ THARUN'S EVALUATED ANSWER SCRIPT:", font=("Segoe UI", 8, "bold"), fg="#60a5fa", bg="#0d1522").pack(anchor="w", pady=(0, 3))
                tk.Label(ans_box, text=student_ans_clean, font=("Consolas", 8), fg="#e2e8f0", bg="#0d1522", justify=tk.LEFT, wraplength=860).pack(anchor="w")

                # Step-wise Rubric Breakdown & Red-Ink Notes
                rubric_box = tk.Frame(card, bg="#2a1215", bd=1, relief=tk.SOLID, highlightbackground="#dc2626", highlightthickness=1, padx=10, pady=8)
                rubric_box.pack(fill=tk.X)

                tk.Label(rubric_box, text="🔴 CBSE STEP-WISE MARKING RUBRIC & RED-INK ANNOTATIONS:", font=("Segoe UI", 8, "bold"), fg="#f87171", bg="#2a1215").pack(anchor="w", pady=(0, 4))

                for s in q.get("step_annotations", []):
                    s_row = tk.Frame(rubric_box, bg="#2a1215")
                    s_row.pack(fill=tk.X, pady=1)
                    step_txt_clean = html.unescape(s.get("step", ""))
                    tk.Label(s_row, text=f"✔ {step_txt_clean}", font=("Segoe UI", 8), fg="#fecdd3", bg="#2a1215").pack(side=tk.LEFT)
                    tk.Label(s_row, text=f"+{s['awarded']} / {s['rubric_mark']}M", font=("Segoe UI", 8, "bold"), fg="#fbbf24", bg="#2a1215").pack(side=tk.RIGHT)

                fb_clean = html.unescape(q.get('evaluator_feedback', ''))
                tk.Label(rubric_box, text=f"Examiner Note: {fb_clean}", font=("Segoe UI", 8, "italic"), fg="#34d399", bg="#2a1215").pack(anchor="w", pady=(4, 0))

            else:
                # 🏆 CBSE 100/100 Topper Reference Model
                topper_box = tk.Frame(card, bg="#0a251b", bd=1, relief=tk.SOLID, highlightbackground="#10b981", highlightthickness=1, padx=10, pady=8)
                topper_box.pack(fill=tk.X, pady=(0, 6))

                model_ans_clean = html.unescape(q.get("model_answer", ""))
                tk.Label(topper_box, text="🏆 CBSE 100/100 TOPPER PRESENTATION (P-E-E-D PROTOCOL):", font=("Segoe UI", 8, "bold"), fg="#34d399", bg="#0a251b").pack(anchor="w", pady=(0, 3))
                tk.Label(topper_box, text=model_ans_clean, font=("Consolas", 8), fg="#e2e8f0", bg="#0a251b", justify=tk.LEFT, wraplength=860).pack(anchor="w")

                scheme_box = tk.Frame(card, bg="#1e293b", bd=1, relief=tk.SOLID, highlightbackground="#f59e0b", highlightthickness=1, padx=10, pady=6)
                scheme_box.pack(fill=tk.X)
                scheme_clean = html.unescape(q.get("marking_scheme", ""))
                tk.Label(scheme_box, text=f"🎯 Marking Scheme: {scheme_clean}", font=("Segoe UI", 8), fg="#fbbf24", bg="#1e293b").pack(anchor="w")

    def _open_graded_html(self):
        eid = self.selected_exam_var.get()
        p = os.path.join(CORRECTED_COPIES_DIR, f"{eid}_CORRECTED_COPY.html")
        if os.path.exists(p):
            webbrowser.open(p)
        else:
            messagebox.showinfo("File Not Found", f"Graded copy not found: {p}")

    def _open_topper_html(self):
        eid = self.selected_exam_var.get()
        p = os.path.join(TOPPER_GUIDES_DIR, f"{eid}_TOPPER_MODEL_GUIDE.html")
        if os.path.exists(p):
            webbrowser.open(p)
        else:
            messagebox.showinfo("File Not Found", f"Topper guide not found: {p}")
