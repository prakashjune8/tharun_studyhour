"""
glider_help_ui.py - ScholasticPulse Glider Help & App Map Module
Dedicated non-intrusive viewer for SCHOLASTICPULSE_MASTER_FLOWCHART_AND_COMPONENT_DIRECTORY.md
"""

import os
import sys
import re
import tkinter as tk
from tkinter import ttk, messagebox


def find_master_directory_file():
    """Locates the master directory markdown file across known paths."""
    candidates = [
        # Check current working directory & parent
        os.path.join(os.getcwd(), "SCHOLASTICPULSE_MASTER_FLOWCHART_AND_COMPONENT_DIRECTORY.md"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "SCHOLASTICPULSE_MASTER_FLOWCHART_AND_COMPONENT_DIRECTORY.md"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SCHOLASTICPULSE_MASTER_FLOWCHART_AND_COMPONENT_DIRECTORY.md"),
        # AppData artifact directory fallback
        os.path.expandvars(r"%USERPROFILE%\.gemini\antigravity\brain\24918a16-6eeb-49c0-836e-d5754e83a424\SCHOLASTICPULSE_MASTER_FLOWCHART_AND_COMPONENT_DIRECTORY.md")
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


class GliderHelpWindow:
    """Dedicated modal window displaying the Master Plan & Component Directory."""

    def __init__(self, parent, target_tag=None):
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title("🧭 ScholasticPulse Glider - Master Map & Directory")
        self.top.geometry("920x680")
        self.top.minsize(700, 500)
        # Window properties & bring to front safely
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

        self.components = []  # List of dicts: {'tag': '[#01]', 'title': '...', 'content': '...'}
        self.raw_text = ""
        self._load_markdown_data()

        self._build_ui()

        if target_tag:
            self.search_var.set(target_tag)
            self._apply_filter()

    def _load_markdown_data(self):
        file_path = find_master_directory_file()
        if not file_path or not os.path.exists(file_path):
            self.raw_text = (
                "Master Directory file could not be found.\n\n"
                "Please place SCHOLASTICPULSE_MASTER_FLOWCHART_AND_COMPONENT_DIRECTORY.md in the project directory."
            )
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.raw_text = f.read()

            # Parse out individual component cards [#01] to [#25]
            pattern = re.compile(
                r"(####\s*`?(\[#\d+\])`?\s*([^\n]+))\n(.*?)(?=(?:####\s*`?\[#\d+\]`?)|(?:\n---)|(?:\Z))",
                re.DOTALL
            )
            matches = pattern.findall(self.raw_text)

            for header, tag, title, body in matches:
                self.components.append({
                    "tag": tag.strip(),
                    "title": title.strip(),
                    "full_title": f"{tag.strip()} {title.strip()}",
                    "body": body.strip()
                })
        except Exception as e:
            self.raw_text = f"Error reading Master Directory: {e}"

    def _build_ui(self):
        # 1. Header Banner
        header_frame = tk.Frame(self.top, bg="#0f172a", height=60, padx=16, pady=10)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header_frame,
            text="🧭 ScholasticPulse Glider — Interactive Architecture Map",
            font=("Segoe UI", 13, "bold"),
            bg="#0f172a",
            fg="#f8fafc"
        )
        title_lbl.pack(side=tk.LEFT)

        subtitle_lbl = tk.Label(
            header_frame,
            text="Components [#01] through [#25]",
            font=("Segoe UI", 9),
            bg="#0f172a",
            fg="#94a3b8"
        )
        subtitle_lbl.pack(side=tk.LEFT, padx=12)

        # 2. Search Bar Bar
        search_frame = tk.Frame(self.top, bg="#1e293b", padx=16, pady=8)
        search_frame.pack(fill=tk.X, side=tk.TOP)

        s_lbl = tk.Label(
            search_frame,
            text="🔍 Search Component (e.g. [#15] or Ledger):",
            font=("Segoe UI", 9, "bold"),
            bg="#1e293b",
            fg="#e2e8f0"
        )
        s_lbl.pack(side=tk.LEFT, padx=(0, 8))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._apply_filter())
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bg="#0f172a",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            relief=tk.FLAT,
            width=28
        )
        self.search_entry.pack(side=tk.LEFT, ipady=3)

        clr_btn = tk.Button(
            search_frame,
            text="Reset",
            command=lambda: self.search_var.set(""),
            font=("Segoe UI", 8, "bold"),
            bg="#334155",
            fg="#f8fafc",
            relief=tk.FLAT,
            padx=8
        )
        clr_btn.pack(side=tk.LEFT, padx=6)

        # 3. Main Content Display Area
        content_frame = tk.Frame(self.top, bg="#0b1120", padx=16, pady=10)
        content_frame.pack(fill=tk.BOTH, expand=True)

        self.text_widget = tk.Text(
            content_frame,
            wrap=tk.WORD,
            bg="#0f172a",
            fg="#e2e8f0",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=16,
            pady=14,
            spacing1=3,
            spacing3=4
        )
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)

        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Style Tags
        self.text_widget.tag_configure("tag_badge", font=("Segoe UI", 11, "bold"), foreground="#38bdf8")
        self.text_widget.tag_configure("tag_title", font=("Segoe UI", 11, "bold"), foreground="#facc15")
        self.text_widget.tag_configure("bullet_label", font=("Segoe UI", 10, "bold"), foreground="#a5b4fc")
        self.text_widget.tag_configure("divider", foreground="#334155")

        self._render_components(self.components)

    def _render_components(self, comp_list):
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)

        if not comp_list:
            if not self.components:
                self.text_widget.insert(tk.END, self.raw_text)
            else:
                self.text_widget.insert(
                    tk.END,
                    "\n  No components found matching your search.\n  Try typing a tag like '[#12]' or keyword like 'Timer'."
                )
            self.text_widget.configure(state=tk.DISABLED)
            return

        for c in comp_list:
            self.text_widget.insert(tk.END, f"{c['tag']} ", "tag_badge")
            self.text_widget.insert(tk.END, f"{c['title']}\n", "tag_title")

            for line in c["body"].split("\n"):
                line_str = line.strip()
                if not line_str:
                    continue
                if line_str.startswith("* **"):
                    parts = line_str.split("**", 2)
                    if len(parts) >= 3:
                        self.text_widget.insert(tk.END, f"  • {parts[1]}: ", "bullet_label")
                        self.text_widget.insert(tk.END, f"{parts[2].strip()}\n")
                    else:
                        self.text_widget.insert(tk.END, f"  {line_str}\n")
                else:
                    self.text_widget.insert(tk.END, f"  {line_str}\n")

            self.text_widget.insert(tk.END, "\n" + "─" * 70 + "\n\n", "divider")

        self.text_widget.configure(state=tk.DISABLED)

    def _apply_filter(self):
        query = self.search_var.get().strip().lower()
        if not query:
            self._render_components(self.components)
            return

        filtered = [
            c for c in self.components
            if query in c["tag"].lower() or query in c["title"].lower() or query in c["body"].lower()
        ]
        self._render_components(filtered)


def show_error_with_glider_link(parent, title, error_message, component_tag):
    """
    Shows an error message box with a prompt to open Glider Help for that component.
    """
    full_msg = f"{error_message}\n\n[Location: Component {component_tag}]\n\nWould you like to open Glider Help to see what this component connects to?"
    if messagebox.askyesno(title, full_msg, icon=messagebox.ERROR, parent=parent):
        GliderHelpWindow(parent, target_tag=component_tag)


def open_glider_help(parent, target_tag=None):
    """Entry point to launch the Glider Help window."""
    return GliderHelpWindow(parent, target_tag=target_tag)
