"""
user_guide_ui.py - ScholasticPulse Interactive Native User Manual & Help Hub
Displays the comprehensive 7-Unit documentation directly inside the desktop app.
Features:
- Left 260px Navigation Sidebar with 7 Units + Master Overview
- Interactive Chapter Reader with KaTeX-like headings, bullet points, and code blocks
- Search bar across all manual sections
- Full visual parity with the Shinobi theme
"""

import os
import sys
import re
import tkinter as tk
from tkinter import ttk, messagebox


def get_documentation_dir() -> str:
    """Finds the DOCUMENTATION directory across frozen and script environments."""
    candidates = [
        os.path.join(os.getcwd(), "DOCUMENTATION"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "DOCUMENTATION"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "DOCUMENTATION"),
    ]
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        candidates.insert(0, os.path.join(exe_dir, "DOCUMENTATION"))
        candidates.insert(1, os.path.join(exe_dir, "VERSION_3_WORKPLACE", "DOCUMENTATION"))
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            candidates.append(os.path.join(meipass, "DOCUMENTATION"))

    for p in candidates:
        if os.path.exists(p) and os.path.isdir(p):
            return p
    return ""


class UserGuideModal:
    """Interactive Native User Guide Reader for ScholasticPulse."""

    UNITS = [
        ("📖 Master Overview", "SCHOLASTICPULSE_COMPLETE_USER_MANUAL.md", "Complete Master Manual (Units 1-7)"),
        ("Unit 1: Command Deck", "UNIT_1_SYSTEM_LAUNCH_AND_COMMAND_DECK.md", "Launch, Title Bar, Command Matrix"),
        ("Unit 2: Timetable & Sleep", "UNIT_2_TIMETABLE_AND_BEDTIME_GUARD.md", "Slab Balancer, Focus Timer, Curfew"),
        ("Unit 3: Diary Ingestion", "UNIT_3_DIARY_INGESTION_AND_AUTO_BALANCER.md", "OCR, Tasks, Bag Reminders"),
        ("Unit 4: Host Exam Suite", "UNIT_4_HOST_EXAM_AND_3PHASE_AGGREGATOR.md", "Study Ledger, 3-Phase Pipeline"),
        ("Unit 5: Question Architect", "UNIT_5_EXAM_VAULTS_AND_QUESTION_ARCHITECT.md", "Vaults, Face A Studio, Time Dial"),
        ("Unit 6: Evaluation & Binder", "UNIT_6_EVALUATION_TOPPER_GUIDE_AND_BINDER.md", "Vision OCR, CBSE 4-Tier, PDF Binder"),
        ("Unit 7: Analytics & Glider", "UNIT_7_ANALYTICS_AUDIT_AND_GLIDER_HELP.md", "Time Audit, Glider Map, Diagnostics"),
    ]

    def __init__(self, parent, target_unit_idx=0):
        self.parent = parent
        self.doc_dir = get_documentation_dir()
        self.active_unit_idx = target_unit_idx
        self.current_content = ""
        self.nav_buttons = []

        self.top = tk.Toplevel(parent)
        self.top.title("📖 ScholasticPulse User Guide & Knowledge Hub")
        self.top.geometry("1080x740")
        self.top.minsize(850, 580)
        self.top.configure(bg="#070b14")

        self.top.transient(parent)
        self.top.lift()
        self.top.deiconify()
        self.top.focus_force()

        if sys.platform == "win32":
            try:
                import ctypes
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                hwnd = ctypes.windll.user32.GetParent(self.top.winfo_id()) or self.top.winfo_id()
                val = ctypes.c_int(1)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(val), ctypes.sizeof(val))
            except Exception:
                pass

        self._build_ui()
        self._select_unit(self.active_unit_idx)

    def _build_ui(self):
        # 1. Header Bar
        hdr = tk.Frame(self.top, bg="#0f172a", padx=16, pady=10, highlightthickness=1, highlightbackground="#38bdf8")
        hdr.pack(fill=tk.X)

        title_box = tk.Frame(hdr, bg="#0f172a")
        title_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            title_box,
            text="📖 SCHOLASTICPULSE — OFFICIAL USER MANUAL & KNOWLEDGE HUB",
            font=("Segoe UI", 12, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="Exhaustive Reference Manual • Class 8 CBSE Architecture, Timetable Rules & AI Examination Suite",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#0f172a"
        ).pack(anchor="w", pady=(1, 0))

        tk.Button(
            hdr,
            text="✕ Close Guide",
            font=("Segoe UI", 8, "bold"),
            bg="#2a1215",
            fg="#fca5a5",
            activebackground="#7f1d1d",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.top.destroy
        ).pack(side=tk.RIGHT)

        # 2. Search Bar
        search_strip = tk.Frame(self.top, bg="#1e293b", padx=16, pady=8)
        search_strip.pack(fill=tk.X)

        tk.Label(
            search_strip,
            text="🔍 Search Manual:",
            font=("Segoe UI", 9, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._filter_text())
        self.search_entry = tk.Entry(
            search_strip,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bg="#0f172a",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            relief=tk.FLAT,
            width=32
        )
        self.search_entry.pack(side=tk.LEFT, ipady=3)

        tk.Button(
            search_strip,
            text="Reset",
            command=lambda: self.search_var.set(""),
            font=("Segoe UI", 8, "bold"),
            bg="#334155",
            fg="#f8fafc",
            relief=tk.FLAT,
            padx=8
        ).pack(side=tk.LEFT, padx=6)

        # 3. Main Split View (Left Sidebar + Right Text Content)
        main_frame = tk.Frame(self.top, bg="#070b14", padx=12, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Sidebar (260px)
        sidebar = tk.Frame(main_frame, bg="#0b1120", width=260, highlightthickness=1, highlightbackground="#1e293b")
        sidebar.pack_propagate(False)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        tk.Label(
            sidebar,
            text="CHAPTER UNITS",
            font=("Segoe UI", 8, "bold"),
            fg="#38bdf8",
            bg="#0b1120",
            anchor="w",
            padx=10,
            pady=8
        ).pack(fill=tk.X)

        for idx, (title, filename, subtitle) in enumerate(self.UNITS):
            btn = tk.Button(
                sidebar,
                text=f"{title}\n{subtitle}",
                font=("Segoe UI", 8),
                justify=tk.LEFT,
                anchor="w",
                bg="#0f172a",
                fg="#cbd5e1",
                activebackground="#0c2540",
                activeforeground="#38bdf8",
                relief=tk.FLAT,
                bd=0,
                highlightthickness=1,
                highlightbackground="#1e293b",
                padx=10,
                pady=6,
                cursor="hand2",
                command=lambda i=idx: self._select_unit(i)
            )
            btn.pack(fill=tk.X, padx=6, pady=2)
            self.nav_buttons.append(btn)

        # Right Content View
        content_frame = tk.Frame(main_frame, bg="#0b1120", highlightthickness=1, highlightbackground="#1e293b")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.text_widget = tk.Text(
            content_frame,
            wrap=tk.WORD,
            bg="#0b1120",
            fg="#e2e8f0",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=18,
            pady=16,
            spacing1=3,
            spacing3=4
        )
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)

        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Typography tags
        self.text_widget.tag_configure("h1", font=("Segoe UI", 13, "bold"), foreground="#38bdf8", spacing3=6)
        self.text_widget.tag_configure("h2", font=("Segoe UI", 11, "bold"), foreground="#facc15", spacing3=4)
        self.text_widget.tag_configure("h3", font=("Segoe UI", 10, "bold"), foreground="#a5b4fc", spacing3=2)
        self.text_widget.tag_configure("bold_lead", font=("Segoe UI", 10, "bold"), foreground="#fb923c")
        self.text_widget.tag_configure("code_block", font=("Consolas", 9), background="#070b14", foreground="#38bdf8")
        self.text_widget.tag_configure("divider", foreground="#334155")
        self.text_widget.tag_configure("highlight", background="#0284c7", foreground="#ffffff")

    def _select_unit(self, idx: int):
        self.active_unit_idx = idx
        for i, btn in enumerate(self.nav_buttons):
            if i == idx:
                btn.configure(bg="#0c2540", fg="#38bdf8", highlightbackground="#38bdf8")
            else:
                btn.configure(bg="#0f172a", fg="#cbd5e1", highlightbackground="#1e293b")

        _, filename, _ = self.UNITS[idx]
        file_path = os.path.join(self.doc_dir, filename) if self.doc_dir else ""
        if not os.path.exists(file_path):
            # Try parent directory fallback
            file_path = os.path.join(os.getcwd(), filename)
            if not os.path.exists(file_path):
                file_path = os.path.join(os.getcwd(), "DOCUMENTATION", filename)

        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.current_content = f.read()
            except Exception as e:
                self.current_content = f"Error reading {filename}: {e}"
        else:
            self.current_content = f"File not found: {filename}\nPlease ensure the DOCUMENTATION folder is present."

        self._render_text(self.current_content)

    def _render_text(self, raw_md: str):
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)

        in_code = False
        for line in raw_md.split("\n"):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code = not in_code
                continue

            if in_code:
                self.text_widget.insert(tk.END, line + "\n", "code_block")
            elif stripped.startswith("# "):
                self.text_widget.insert(tk.END, "\n" + stripped[2:] + "\n", "h1")
            elif stripped.startswith("## "):
                self.text_widget.insert(tk.END, "\n" + stripped[3:] + "\n", "h2")
            elif stripped.startswith("### "):
                self.text_widget.insert(tk.END, "\n" + stripped[4:] + "\n", "h3")
            elif stripped.startswith("#### "):
                self.text_widget.insert(tk.END, "  " + stripped[5:] + "\n", "h3")
            elif stripped.startswith("* **"):
                parts = line.split("**", 2)
                if len(parts) >= 3:
                    self.text_widget.insert(tk.END, "  • ", "bold_lead")
                    self.text_widget.insert(tk.END, parts[1] + ": ", "bold_lead")
                    self.text_widget.insert(tk.END, parts[2].strip() + "\n")
                else:
                    self.text_widget.insert(tk.END, line + "\n")
            elif stripped.startswith("---"):
                self.text_widget.insert(tk.END, "─" * 70 + "\n", "divider")
            else:
                self.text_widget.insert(tk.END, line + "\n")

        self.text_widget.configure(state=tk.DISABLED)

    def _filter_text(self):
        query = self.search_var.get().strip().lower()
        if not query:
            self._render_text(self.current_content)
            return

        # Simple filter: render only lines containing query with surrounding context
        lines = self.current_content.split("\n")
        matched = []
        for i, l in enumerate(lines):
            if query in l.lower():
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                matched.extend(lines[start:end])
                matched.append("---")

        if matched:
            self._render_text("\n".join(matched))
        else:
            self.text_widget.configure(state=tk.NORMAL)
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert(tk.END, f"\n  No matches found for '{query}' in this unit.\n  Try selecting another unit on the left sidebar.", "h3")
            self.text_widget.configure(state=tk.DISABLED)


def open_user_guide(parent, unit_idx=0):
    """Entry point function to launch the User Guide modal."""
    return UserGuideModal(parent, target_unit_idx=unit_idx)
