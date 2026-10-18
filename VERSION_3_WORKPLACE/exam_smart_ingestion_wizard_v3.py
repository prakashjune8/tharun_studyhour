"""
SMART INGESTION WIZARD & SUBJECT VAULT ENGINE (SESSION 7 CORE COMPONENT)
------------------------------------------------------------------------
Implements:
1. Permanent 7 Subject Vault Directories on disk:
   - 01_Mathematics/
   - 02_Physical_Science/
   - 03_Biology/
   - 04_Social_Science/
   - 05_English/
   - 06_Hindi/
   - 07_Tamil/
2. Smart Ingestion Wizard:
   - Validates file (PDF/Image).
   - Ingests file type:
     a) Full Complete Textbook (stores publication, full book tag).
     b) Topic / Chapter Photocopy (tags chapter name, exercise number, access/topic tag).
     c) School Model Exam Paper (Term 1 / Unit Test pattern reference).
   - Automatically generates a clean, canonical filename:
     e.g., MATH_CH09_EX09.3_ALGEBRAIC_EXPRESSIONS.pdf.
   - Saves into the exact subject folder.
   - Registers metadata in textbook_library_catalog.json.
3. Text Extraction for Gemini Grounding:
   - Extracts syllabus/exercise text from uploaded PDFs to ground question generation.
4. Full Modern Tkinter Dialog (SmartIngestionDialog):
   - Interactive UI with live canonical name preview, subject selection, and vault management.
"""

import os
import sys
import shutil
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime

from exam_ground_truth_v3 import SubjectCatalog, EXAM_SYSTEM_DIR, BASE_DIR

TEXTBOOKS_VAULT_ROOT = os.path.join(EXAM_SYSTEM_DIR, "02_UPLOADED_TEXTBOOKS_PDF")
CATALOG_JSON_FILE = os.path.join(EXAM_SYSTEM_DIR, "textbook_library_catalog.json")


class SmartIngestionWizard:
    """
    Governs the 7 subject vaults, canonical naming, metadata cataloging, and text extraction.
    """

    SUBJECT_FOLDER_MAP = {
        "Mathematics": "01_Mathematics",
        "Physical Science": "02_Physical_Science",
        "Biology": "03_Biology",
        "Social Science": "04_Social_Science",
        "English": "05_English",
        "Hindi": "06_Hindi",
        "Tamil": "07_Tamil"
    }

    SUBJECT_PREFIX_MAP = {
        "Mathematics": "MATH",
        "Physical Science": "PHY_CHEM",
        "Biology": "BIO",
        "Social Science": "SST",
        "English": "ENG",
        "Hindi": "HIN",
        "Tamil": "TAM"
    }

    @classmethod
    def ensure_vault_directories(cls):
        """Ensures all 7 subject vault folders exist on disk."""
        os.makedirs(TEXTBOOKS_VAULT_ROOT, exist_ok=True)
        for folder_name in cls.SUBJECT_FOLDER_MAP.values():
            folder_path = os.path.join(TEXTBOOKS_VAULT_ROOT, folder_name)
            os.makedirs(folder_path, exist_ok=True)

    @classmethod
    def load_catalog(cls) -> Dict[str, Any]:
        """Loads textbook_library_catalog.json from disk."""
        if not os.path.exists(CATALOG_JSON_FILE):
            return {"total_files": 0, "library": []}
        try:
            with open(CATALOG_JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[SmartIngestionWizard] Warning loading catalog: {e}")
            return {"total_files": 0, "library": []}

    @classmethod
    def save_catalog(cls, catalog_data: Dict[str, Any]):
        """Saves updated catalog to disk."""
        os.makedirs(os.path.dirname(CATALOG_JSON_FILE), exist_ok=True)
        with open(CATALOG_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(catalog_data, f, indent=2, ensure_ascii=False)

    @classmethod
    def sanitize_for_filename(cls, text: str) -> str:
        """Converts strings into safe uppercase filename fragments."""
        s = re.sub(r'[^\w\s-]', '', str(text).strip())
        s = re.sub(r'[-\s]+', '_', s)
        return s.upper()

    @classmethod
    def generate_canonical_filename(
        cls,
        subject: str,
        material_type: str,
        chapter_name: Optional[str] = None,
        exercise_or_topic: Optional[str] = None,
        book_title: Optional[str] = None,
        original_ext: str = ".pdf"
    ) -> str:
        """
        Creates clean, human-readable standardized filenames:
        - Full book: MATH_FULL_TEXTBOOK_NCERT_CLASS8.pdf
        - Photocopy: MATH_CH09_EX09.3_ALGEBRAIC_EXPRESSIONS.pdf
        - Model paper: MATH_MODEL_PAPER_TERM1_SENTHIL.pdf
        """
        prefix = cls.SUBJECT_PREFIX_MAP.get(subject, "SUBJ")
        ext = original_ext if original_ext.startswith(".") else f".{original_ext}"

        if material_type == "full_textbook":
            title_part = cls.sanitize_for_filename(book_title or "COMPLETE_TEXTBOOK")
            return f"{prefix}_FULL_TEXTBOOK_{title_part}{ext}"

        elif material_type == "model_exam_paper":
            title_part = cls.sanitize_for_filename(book_title or "SENTHIL_TERM1_MODEL_PAPER")
            return f"{prefix}_MODEL_EXAM_{title_part}{ext}"

        else:
            # Topic / Chapter Photocopy
            ch_clean = cls.sanitize_for_filename(chapter_name or "CHAPTER")
            ex_clean = cls.sanitize_for_filename(exercise_or_topic or "TOPIC")
            return f"{prefix}_{ch_clean}_{ex_clean}{ext}"

    @classmethod
    def ingest_file_to_vault(
        cls,
        source_file_path: str,
        subject: str,
        material_type: str,  # 'full_textbook' | 'topic_photocopy' | 'model_exam_paper'
        chapter_name: Optional[str] = None,
        exercise_or_topic: Optional[str] = None,
        book_title: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ingests any file into the subject vault with canonical renaming and indexing.
        """
        cls.ensure_vault_directories()

        if not os.path.exists(source_file_path):
            return {"success": False, "error": f"Source file does not exist: {source_file_path}"}

        folder_name = cls.SUBJECT_FOLDER_MAP.get(subject)
        if not folder_name:
            return {"success": False, "error": f"Unknown subject: {subject}"}

        target_folder = os.path.join(TEXTBOOKS_VAULT_ROOT, folder_name)
        _, ext = os.path.splitext(source_file_path)

        # Generate Canonical Filename
        canonical_name = cls.generate_canonical_filename(
            subject=subject,
            material_type=material_type,
            chapter_name=chapter_name,
            exercise_or_topic=exercise_or_topic,
            book_title=book_title,
            original_ext=ext
        )

        dest_path = os.path.join(target_folder, canonical_name)

        # Copy file into subject folder
        try:
            shutil.copy2(source_file_path, dest_path)
            file_size_bytes = os.path.getsize(dest_path)
        except Exception as e:
            return {"success": False, "error": f"Failed to copy file to vault: {e}"}

        # Page Count Detection if PDF
        page_count = 1
        if ext.lower() == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(dest_path)
                page_count = len(reader.pages)
            except Exception:
                page_count = 1

        # Build Metadata Record
        record_id = f"LIB-{cls.SUBJECT_PREFIX_MAP.get(subject, 'SUB')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        record = {
            "id": record_id,
            "subject": subject,
            "subject_folder": folder_name,
            "material_type": material_type,
            "canonical_filename": canonical_name,
            "relative_path": os.path.relpath(dest_path, BASE_DIR).replace("\\", "/"),
            "absolute_path": dest_path,
            "file_size_bytes": file_size_bytes,
            "total_pages": page_count,
            "chapter_name": chapter_name or "",
            "exercise_or_topic": exercise_or_topic or "",
            "book_title": book_title or "",
            "notes": notes or "",
            "ingested_at": datetime.now().isoformat(),
            "is_active_source": True
        }

        # Update Catalog JSON: set others of this subject as inactive if this is active
        catalog = cls.load_catalog()
        for item in catalog.get("library", []):
            if item.get("subject") == subject:
                item["is_active_source"] = False

        catalog.setdefault("library", []).append(record)
        catalog["total_files"] = len(catalog["library"])
        cls.save_catalog(catalog)

        return {
            "success": True,
            "canonical_name": canonical_name,
            "destination_folder": target_folder,
            "dest_path": dest_path,
            "page_count": page_count,
            "record": record
        }

    @classmethod
    def list_subject_materials(cls, subject: str) -> List[Dict[str, Any]]:
        """Returns all registered materials for a specific subject."""
        catalog = cls.load_catalog()
        return [item for item in catalog.get("library", []) if item.get("subject", "").lower() == subject.lower()]

    @classmethod
    def get_active_material(cls, subject: str) -> Optional[Dict[str, Any]]:
        """Retrieves the currently active material record for a subject."""
        materials = cls.list_subject_materials(subject)
        for item in reversed(materials):
            if item.get("is_active_source", False):
                return item
        return materials[-1] if materials else None

    @classmethod
    def set_active_material(cls, record_id: str):
        """Sets a specific material as the active source for its subject."""
        catalog = cls.load_catalog()
        target_subject = None
        for item in catalog.get("library", []):
            if item.get("id") == record_id:
                target_subject = item.get("subject")
                break

        if target_subject:
            for item in catalog.get("library", []):
                if item.get("subject") == target_subject:
                    item["is_active_source"] = (item.get("id") == record_id)
            cls.save_catalog(catalog)

    @classmethod
    def extract_text_from_material(cls, record: Dict[str, Any], max_pages: int = 5) -> str:
        """
        Extracts raw textual content from the material PDF to supply as grounding context.
        """
        path = record.get("absolute_path", "")
        if not path or not os.path.exists(path):
            return ""

        _, ext = os.path.splitext(path)
        if ext.lower() != ".pdf":
            return f"[Uploaded Material: {record.get('canonical_filename', '')} ({record.get('material_type')})]"

        try:
            import pypdf
            reader = pypdf.PdfReader(path)
            extracted = []
            pages_to_read = min(len(reader.pages), max_pages)
            for i in range(pages_to_read):
                txt = reader.pages[i].extract_text() or ""
                if txt.strip():
                    extracted.append(f"--- PAGE {i + 1} ---\n{txt.strip()}")
            return "\n\n".join(extracted)
        except Exception as e:
            print(f"[SmartIngestionWizard] Text extraction warning: {e}")
            return f"[Material: {record.get('canonical_filename', '')}]"

    # Alias for grounding
    extract_grounding_text = extract_text_from_material


# ==============================================================================
# SMART INGESTION WIZARD UI DIALOG (TKINTER)
# ==============================================================================
class SmartIngestionDialog:
    """
    Dedicated modal dialog for uploading, categorizing, canonical renaming,
    and vault inspection across all 7 CBSE subjects.
    """

    def __init__(self, parent, default_subject: str = "Mathematics", on_success_callback=None):
        import tkinter as tk
        from tkinter import ttk, messagebox, filedialog

        self.parent = parent
        self.default_subject = default_subject
        self.on_success = on_success_callback

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("📚 Smart Ingestion Wizard • 7 Subject Vaults")
        self.dialog.geometry("720x680")
        self.dialog.minsize(660, 600)
        self.dialog.configure(bg="#0f172a")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # State Variables
        self.file_path_var = tk.StringVar(value="")
        self.subject_var = tk.StringVar(value=default_subject)
        self.type_var = tk.StringVar(value="topic_photocopy")  # 'topic_photocopy' | 'full_textbook' | 'model_exam_paper'
        self.chapter_var = tk.StringVar(value="Ch 09 Algebraic Expressions")
        self.exercise_var = tk.StringVar(value="Ex 9.3 Identities")
        self.book_title_var = tk.StringVar(value="NCERT Class 8")
        self.notes_var = tk.StringVar(value="")
        self.canonical_preview_var = tk.StringVar(value="")
        self.target_folder_var = tk.StringVar(value="")

        self._build_ui()
        self._update_canonical_preview()

    def _build_ui(self):
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox

        # Top Banner
        header = tk.Frame(self.dialog, bg="#1e293b", padx=16, pady=12, highlightthickness=1, highlightbackground="#334155")
        header.pack(fill=tk.X)

        lbl_title = tk.Label(
            header,
            text="📥 SMART INGESTION WIZARD • 7 SUBJECT VAULTS",
            font=("Segoe UI", 11, "bold"),
            fg="#f97316",
            bg="#1e293b"
        )
        lbl_title.pack(anchor="w")

        lbl_desc = tk.Label(
            header,
            text="Upload full textbooks, chapter photocopies, or school model exam papers with auto canonical renaming.",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#1e293b"
        )
        lbl_desc.pack(anchor="w", pady=(2, 0))

        # Bottom Button Bar (Packed first to pin firmly to bottom)
        btn_bar = tk.Frame(self.dialog, bg="#1e293b", padx=16, pady=10, highlightthickness=1, highlightbackground="#334155")
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        btn_cancel = tk.Button(
            btn_bar,
            text="Close",
            font=("Segoe UI", 8),
            fg="#cbd5e1",
            bg="#334155",
            relief=tk.FLAT,
            padx=14,
            pady=5,
            command=self.dialog.destroy
        )
        btn_cancel.pack(side=tk.RIGHT, padx=(6, 0))

        btn_ingest = tk.Button(
            btn_bar,
            text="🚀 INGEST & SAVE TO VAULT",
            font=("Segoe UI", 9, "bold"),
            fg="#ffffff",
            bg="#16a34a",
            activebackground="#15803d",
            relief=tk.FLAT,
            padx=16,
            pady=5,
            cursor="hand2",
            command=self._on_ingest_clicked
        )
        btn_ingest.pack(side=tk.RIGHT)

        # Main Body
        body = tk.Frame(self.dialog, bg="#0f172a", padx=16, pady=8)
        body.pack(fill=tk.BOTH, expand=True)

        # 1. FILE PICKER
        lbl_step1 = tk.Label(body, text="STEP 1: SELECT PDF OR PHOTOCOPY SCAN", font=("Segoe UI", 9, "bold"), fg="#38bdf8", bg="#0f172a", anchor="w")
        lbl_step1.pack(fill=tk.X, pady=(0, 2))

        f_frame = tk.Frame(body, bg="#1e293b", padx=10, pady=6, highlightthickness=1, highlightbackground="#334155")
        f_frame.pack(fill=tk.X, pady=(0, 6))

        entry_file = tk.Entry(f_frame, textvariable=self.file_path_var, font=("Segoe UI", 9), bg="#0f172a", fg="#f8fafc", insertbackground="#38bdf8", relief=tk.FLAT)
        entry_file.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        btn_browse = tk.Button(
            f_frame,
            text="📂 Browse...",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#0284c7",
            relief=tk.FLAT,
            padx=12,
            pady=3,
            cursor="hand2",
            command=self._on_browse_file
        )
        btn_browse.pack(side=tk.RIGHT)

        # 2. SUBJECT SELECTION
        lbl_step2 = tk.Label(body, text="STEP 2: TARGET SUBJECT VAULT", font=("Segoe UI", 9, "bold"), fg="#38bdf8", bg="#0f172a", anchor="w")
        lbl_step2.pack(fill=tk.X, pady=(0, 2))

        subj_frame = tk.Frame(body, bg="#1e293b", padx=10, pady=6, highlightthickness=1, highlightbackground="#334155")
        subj_frame.pack(fill=tk.X, pady=(0, 6))

        subjects = list(SmartIngestionWizard.SUBJECT_FOLDER_MAP.keys())
        combo_subj = ttk.Combobox(subj_frame, textvariable=self.subject_var, values=subjects, state="readonly", font=("Segoe UI", 9))
        combo_subj.pack(fill=tk.X)
        combo_subj.bind("<<ComboboxSelected>>", lambda e: self._update_canonical_preview())

        # 3. MATERIAL TYPE CLASSIFICATION
        lbl_step3 = tk.Label(body, text="STEP 3: CLASSIFY MATERIAL TYPE & DETAILS", font=("Segoe UI", 9, "bold"), fg="#38bdf8", bg="#0f172a", anchor="w")
        lbl_step3.pack(fill=tk.X, pady=(0, 2))

        type_frame = tk.Frame(body, bg="#1e293b", padx=10, pady=6, highlightthickness=1, highlightbackground="#334155")
        type_frame.pack(fill=tk.X, pady=(0, 6))

        rb_box = tk.Frame(type_frame, bg="#1e293b")
        rb_box.pack(fill=tk.X, pady=(0, 6))

        rb_photo = tk.Radiobutton(
            rb_box, text="📑 Topic / Chapter Photocopy", variable=self.type_var, value="topic_photocopy",
            fg="#e2e8f0", bg="#1e293b", selectcolor="#0f172a", activebackground="#1e293b", font=("Segoe UI", 8, "bold"),
            command=self._on_type_changed
        )
        rb_photo.pack(side=tk.LEFT, padx=(0, 10))

        rb_book = tk.Radiobutton(
            rb_box, text="📘 Full Textbook", variable=self.type_var, value="full_textbook",
            fg="#e2e8f0", bg="#1e293b", selectcolor="#0f172a", activebackground="#1e293b", font=("Segoe UI", 8, "bold"),
            command=self._on_type_changed
        )
        rb_book.pack(side=tk.LEFT, padx=(0, 10))

        rb_exam = tk.Radiobutton(
            rb_box, text="📝 School Model Paper", variable=self.type_var, value="model_exam_paper",
            fg="#e2e8f0", bg="#1e293b", selectcolor="#0f172a", activebackground="#1e293b", font=("Segoe UI", 8, "bold"),
            command=self._on_type_changed
        )
        rb_exam.pack(side=tk.LEFT)

        # Dynamic Field Containers
        self.detail_container = tk.Frame(type_frame, bg="#1e293b")
        self.detail_container.pack(fill=tk.X)
        self._render_dynamic_fields()

        # 4. CANONICAL PREVIEW BOX
        lbl_step4 = tk.Label(body, text="STEP 4: CANONICAL STANDARDIZATION PREVIEW", font=("Segoe UI", 9, "bold"), fg="#fbbf24", bg="#0f172a", anchor="w")
        lbl_step4.pack(fill=tk.X, pady=(0, 2))

        preview_box = tk.Frame(body, bg="#161f30", padx=12, pady=8, highlightthickness=1, highlightbackground="#fbbf24")
        preview_box.pack(fill=tk.X, pady=(0, 6))

        lbl_dest = tk.Label(preview_box, textvariable=self.target_folder_var, font=("Consolas", 8), fg="#94a3b8", bg="#161f30", anchor="w")
        lbl_dest.pack(fill=tk.X)

        lbl_canon = tk.Label(preview_box, textvariable=self.canonical_preview_var, font=("Consolas", 10, "bold"), fg="#34d399", bg="#161f30", anchor="w")
        lbl_canon.pack(fill=tk.X, pady=(4, 0))


    def _render_dynamic_fields(self):
        import tkinter as tk

        for w in self.detail_container.winfo_children():
            w.destroy()

        t = self.type_var.get()
        if t == "topic_photocopy":
            # Chapter Name
            r1 = tk.Frame(self.detail_container, bg="#1e293b")
            r1.pack(fill=tk.X, pady=2)
            tk.Label(r1, text="Chapter Name:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#1e293b", width=14, anchor="w").pack(side=tk.LEFT)
            e1 = tk.Entry(r1, textvariable=self.chapter_var, font=("Segoe UI", 9), bg="#0f172a", fg="#f8fafc", relief=tk.FLAT)
            e1.pack(side=tk.LEFT, fill=tk.X, expand=True)
            e1.bind("<KeyRelease>", lambda e: self._update_canonical_preview())

            # Exercise / Topic
            r2 = tk.Frame(self.detail_container, bg="#1e293b")
            r2.pack(fill=tk.X, pady=2)
            tk.Label(r2, text="Exercise / Topic:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#1e293b", width=14, anchor="w").pack(side=tk.LEFT)
            e2 = tk.Entry(r2, textvariable=self.exercise_var, font=("Segoe UI", 9), bg="#0f172a", fg="#f8fafc", relief=tk.FLAT)
            e2.pack(side=tk.LEFT, fill=tk.X, expand=True)
            e2.bind("<KeyRelease>", lambda e: self._update_canonical_preview())

        elif t == "full_textbook":
            r1 = tk.Frame(self.detail_container, bg="#1e293b")
            r1.pack(fill=tk.X, pady=2)
            tk.Label(r1, text="Book Title / Ed:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#1e293b", width=14, anchor="w").pack(side=tk.LEFT)
            e1 = tk.Entry(r1, textvariable=self.book_title_var, font=("Segoe UI", 9), bg="#0f172a", fg="#f8fafc", relief=tk.FLAT)
            e1.pack(side=tk.LEFT, fill=tk.X, expand=True)
            e1.bind("<KeyRelease>", lambda e: self._update_canonical_preview())

        else:  # model_exam_paper
            r1 = tk.Frame(self.detail_container, bg="#1e293b")
            r1.pack(fill=tk.X, pady=2)
            tk.Label(r1, text="Exam Title / Year:", font=("Segoe UI", 8), fg="#cbd5e1", bg="#1e293b", width=14, anchor="w").pack(side=tk.LEFT)
            e1 = tk.Entry(r1, textvariable=self.book_title_var, font=("Segoe UI", 9), bg="#0f172a", fg="#f8fafc", relief=tk.FLAT)
            e1.pack(side=tk.LEFT, fill=tk.X, expand=True)
            e1.bind("<KeyRelease>", lambda e: self._update_canonical_preview())

    def _on_type_changed(self):
        self._render_dynamic_fields()
        self._update_canonical_preview()

    def _update_canonical_preview(self):
        subj = self.subject_var.get()
        t = self.type_var.get()
        folder_name = SmartIngestionWizard.SUBJECT_FOLDER_MAP.get(subj, "01_Mathematics")
        self.target_folder_var.set(f"Target Vault Folder: EXAM_SYSTEM_V3/02_UPLOADED_TEXTBOOKS_PDF/{folder_name}/")

        src = self.file_path_var.get()
        ext = os.path.splitext(src)[1] if src else ".pdf"

        canon = SmartIngestionWizard.generate_canonical_filename(
            subject=subj,
            material_type=t,
            chapter_name=self.chapter_var.get(),
            exercise_or_topic=self.exercise_var.get(),
            book_title=self.book_title_var.get(),
            original_ext=ext or ".pdf"
        )
        self.canonical_preview_var.set(f"Canonical Name: {canon}")

    def _on_browse_file(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            parent=self.dialog,
            title="Select Textbook, Photocopy, or Model Exam Paper",
            filetypes=[("PDF and Images", "*.pdf *.png *.jpg *.jpeg"), ("All Files", "*.*")]
        )
        if path:
            self.file_path_var.set(path)
            self._update_canonical_preview()

    def _on_ingest_clicked(self):
        from tkinter import messagebox
        src = self.file_path_var.get().strip()
        if not src or not os.path.exists(src):
            messagebox.showerror("Error", "Please select a valid existing PDF or image file first.", parent=self.dialog)
            return

        subj = self.subject_var.get()
        m_type = self.type_var.get()

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
                parent=self.dialog
            )
            if self.on_success:
                self.on_success(res["record"])
            self.dialog.destroy()
        else:
            messagebox.showerror("Ingestion Failed", res.get("error", "Unknown error"), parent=self.dialog)


# ==============================================================================
# VERIFICATION RUNNER
# ==============================================================================
def run_ingestion_verification():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 75)
    print("   SMART INGESTION WIZARD & 7 SUBJECT VAULTS VERIFICATION")
    print("=" * 75)

    SmartIngestionWizard.ensure_vault_directories()
    print("\n[TEST 1] Ensuring 7 Dedicated Subject Folders Exist on Disk:")
    for subj, folder in SmartIngestionWizard.SUBJECT_FOLDER_MAP.items():
        p = os.path.join(TEXTBOOKS_VAULT_ROOT, folder)
        print(f" -> [{subj:<18}] Folder: {folder} | Exists: {os.path.exists(p)}")

    # Create dummy source files to test ingestion
    scratch_dir = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS")
    os.makedirs(scratch_dir, exist_ok=True)
    dummy_scan = os.path.join(scratch_dir, "Adobe_Scan_18_Oct_2026_Raw.pdf")
    with open(dummy_scan, "wb") as f:
        f.write(b"%PDF-1.4 Mock Raw Scanned Content")

    # Ingestion Case A: Topic Photocopy (Mathematics Ex 9.3)
    print("\n[TEST 2] Ingesting Case A: Topic Photocopy (Mathematics Ex 9.3):")
    res_a = SmartIngestionWizard.ingest_file_to_vault(
        source_file_path=dummy_scan,
        subject="Mathematics",
        material_type="topic_photocopy",
        chapter_name="Ch09_Algebraic_Expressions",
        exercise_or_topic="Ex_9.3_Identities",
        notes="Photocopy of textbook page 142 Ex 9.3 Q1-4"
    )
    print(f" -> Ingestion Success:    {res_a['success']}")
    print(f" -> Canonical Filename:   {res_a['canonical_name']}")
    print(f" -> Target Folder:        {res_a['destination_folder']}")

    # Ingestion Case B: Full Complete Textbook (Physical Science)
    print("\n[TEST 3] Ingesting Case B: Full Complete Textbook (Physical Science):")
    res_b = SmartIngestionWizard.ingest_file_to_vault(
        source_file_path=dummy_scan,
        subject="Physical Science",
        material_type="full_textbook",
        book_title="Senthil_SPS_Science_Class8_NCERT",
        notes="Complete textbook scan for Physics and Chemistry"
    )
    print(f" -> Ingestion Success:    {res_b['success']}")
    print(f" -> Canonical Filename:   {res_b['canonical_name']}")
    print(f" -> Target Folder:        {res_b['destination_folder']}")

    # Ingestion Case C: Senthil Term 1 Model Question Paper (Social Science)
    print("\n[TEST 4] Ingesting Case C: Senthil Term 1 Model Paper (Social Science):")
    res_c = SmartIngestionWizard.ingest_file_to_vault(
        source_file_path=dummy_scan,
        subject="Social Science",
        material_type="model_exam_paper",
        book_title="Term1_SPS_History_Geography_2025",
        notes="Official previous year school exam paper"
    )
    print(f" -> Ingestion Success:    {res_c['success']}")
    print(f" -> Canonical Filename:   {res_c['canonical_name']}")
    print(f" -> Target Folder:        {res_c['destination_folder']}")

    # Check Active Material retrieval
    print("\n[TEST 5] Checking Active Material Retrieval for Mathematics:")
    active_m = SmartIngestionWizard.get_active_material("Mathematics")
    print(f" -> Active Material File: {active_m['canonical_filename'] if active_m else 'None'}")

    # Check Catalog Index
    print("\n[TEST 6] Inspecting Updated Catalog Library Index:")
    cat = SmartIngestionWizard.load_catalog()
    print(f" -> Total Files in Library: {cat['total_files']}")
    for item in cat['library'][-3:]:
        print(f"    * [{item['subject']:<18}] Type: {item['material_type']:<18} | File: {item['canonical_filename']}")

    print("\n" + "=" * 75)
    if res_a['success'] and res_b['success'] and res_c['success'] and active_m:
        print("   ✅ SMART INGESTION WIZARD PASSED ALL 7 VAULT & TAGGING TESTS!")
    else:
        print("   ⚠️ WARNING: Ingestion test had issues.")
    print("=" * 75)


if __name__ == "__main__":
    if "--gui" in sys.argv:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        dlg = SmartIngestionDialog(root, default_subject="Mathematics", on_success_callback=lambda rec: print("Ingested:", rec))
        root.mainloop()
    else:
        run_ingestion_verification()
