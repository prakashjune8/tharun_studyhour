"""
SAMPLE QUESTIONS & SCHOOL MODEL PAPERS ENGINE (SESSION 7 CORE COMPONENT)
-------------------------------------------------------------------------
Implements:
1. Dedicated permanent vault for School Sample Questions & Model Papers:
   EXAM_SYSTEM_V3/02_SCHOOL_MODEL_PAPERS_PDF/
   - 01_Mathematics/
   - 02_Physical_Science/
   - 03_Biology/
   - 04_Social_Science/
   - 05_English/
   - 06_Hindi/
   - 07_Tamil/
2. Canonical Standardization:
   e.g., MATH_SAMPLE_Q_TERM1_SENTHIL_2025.pdf
3. Metadata Indexing:
   school_sample_questions_catalog.json
4. Text Extraction for Style Reference in Question Generation.
"""

import os
import sys
import shutil
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime

from exam_ground_truth_v3 import SubjectCatalog, EXAM_SYSTEM_DIR, BASE_DIR

MODEL_PAPERS_VAULT_ROOT = os.path.join(EXAM_SYSTEM_DIR, "02_SCHOOL_MODEL_PAPERS_PDF")
SAMPLE_CATALOG_JSON_FILE = os.path.join(EXAM_SYSTEM_DIR, "school_sample_questions_catalog.json")


class SampleQuestionsEngine:
    """
    Manages the dedicated vault for school sample questions and model exam papers.
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
        """Ensures all 7 subject model paper folders exist on disk."""
        os.makedirs(MODEL_PAPERS_VAULT_ROOT, exist_ok=True)
        for folder_name in cls.SUBJECT_FOLDER_MAP.values():
            folder_path = os.path.join(MODEL_PAPERS_VAULT_ROOT, folder_name)
            os.makedirs(folder_path, exist_ok=True)

    @classmethod
    def load_catalog(cls) -> Dict[str, Any]:
        """Loads school_sample_questions_catalog.json from disk."""
        if not os.path.exists(SAMPLE_CATALOG_JSON_FILE):
            return {"total_files": 0, "sample_papers": []}
        try:
            with open(SAMPLE_CATALOG_JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[SampleQuestionsEngine] Warning loading catalog: {e}")
            return {"total_files": 0, "sample_papers": []}

    @classmethod
    def save_catalog(cls, catalog_data: Dict[str, Any]):
        """Saves updated catalog to disk."""
        os.makedirs(os.path.dirname(SAMPLE_CATALOG_JSON_FILE), exist_ok=True)
        with open(SAMPLE_CATALOG_JSON_FILE, "w", encoding="utf-8") as f:
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
        exam_category: str,  # 'term_1_model' | 'periodic_test' | 'unit_test' | 'annual_model'
        paper_title: str,
        original_ext: str = ".pdf"
    ) -> str:
        """
        Creates clean, human-readable standardized filenames for sample questions:
        e.g., MATH_SAMPLE_Q_TERM1_SENTHIL_2025.pdf
        """
        prefix = cls.SUBJECT_PREFIX_MAP.get(subject, "SUBJ")
        ext = original_ext if original_ext.startswith(".") else f".{original_ext}"

        cat_tag_map = {
            "term_1_model": "TERM1",
            "periodic_test": "PERIODIC_TEST",
            "unit_test": "UNIT_TEST",
            "annual_model": "ANNUAL_MODEL"
        }
        tag = cat_tag_map.get(exam_category, "SAMPLE")
        title_part = cls.sanitize_for_filename(paper_title or "SCHOOL_PAPER")
        return f"{prefix}_SAMPLE_Q_{tag}_{title_part}{ext}"

    @classmethod
    def ingest_sample_paper(
        cls,
        source_file_path: str,
        subject: str,
        exam_category: str,
        paper_title: str,
        total_marks: int = 80,
        time_mins: int = 180,
        school_name: str = "Senthil Public School",
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ingests a sample question paper into the dedicated subject model papers vault.
        """
        cls.ensure_vault_directories()

        if not os.path.exists(source_file_path):
            return {"success": False, "error": f"Source file does not exist: {source_file_path}"}

        folder_name = cls.SUBJECT_FOLDER_MAP.get(subject)
        if not folder_name:
            return {"success": False, "error": f"Unknown subject: {subject}"}

        target_folder = os.path.join(MODEL_PAPERS_VAULT_ROOT, folder_name)
        _, ext = os.path.splitext(source_file_path)

        canonical_name = cls.generate_canonical_filename(
            subject=subject,
            exam_category=exam_category,
            paper_title=paper_title,
            original_ext=ext
        )

        dest_path = os.path.join(target_folder, canonical_name)

        try:
            shutil.copy2(source_file_path, dest_path)
            file_size_bytes = os.path.getsize(dest_path)
        except Exception as e:
            return {"success": False, "error": f"Failed to copy file to model vault: {e}"}

        page_count = 1
        if ext.lower() == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(dest_path)
                page_count = len(reader.pages)
            except Exception:
                page_count = 1

        record_id = f"SMP-{cls.SUBJECT_PREFIX_MAP.get(subject, 'SUB')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        record = {
            "id": record_id,
            "subject": subject,
            "subject_folder": folder_name,
            "exam_category": exam_category,
            "paper_title": paper_title,
            "canonical_filename": canonical_name,
            "relative_path": os.path.relpath(dest_path, BASE_DIR).replace("\\", "/"),
            "absolute_path": dest_path,
            "file_size_bytes": file_size_bytes,
            "total_pages": page_count,
            "total_marks": total_marks,
            "time_mins": time_mins,
            "school_name": school_name,
            "notes": notes or "",
            "uploaded_at": datetime.now().isoformat(),
            "is_active_style_reference": True
        }

        # Update Catalog JSON
        catalog = cls.load_catalog()
        for item in catalog.get("sample_papers", []):
            if item.get("subject") == subject:
                item["is_active_style_reference"] = False

        catalog.setdefault("sample_papers", []).append(record)
        catalog["total_files"] = len(catalog["sample_papers"])
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
    def list_subject_sample_papers(cls, subject: str) -> List[Dict[str, Any]]:
        """Returns all sample question papers for a specific subject."""
        catalog = cls.load_catalog()
        return [item for item in catalog.get("sample_papers", []) if item.get("subject", "").lower() == subject.lower()]

    @classmethod
    def get_active_style_reference(cls, subject: str) -> Optional[Dict[str, Any]]:
        """Retrieves the active sample question paper for style referencing."""
        papers = cls.list_subject_sample_papers(subject)
        for item in reversed(papers):
            if item.get("is_active_style_reference", False):
                return item
        return papers[-1] if papers else None

    @classmethod
    def set_active_style_reference(cls, record_id: str):
        """Sets a specific sample question paper as the active style reference."""
        catalog = cls.load_catalog()
        target_subject = None
        for item in catalog.get("sample_papers", []):
            if item.get("id") == record_id:
                target_subject = item.get("subject")
                break

        if target_subject:
            for item in catalog.get("sample_papers", []):
                if item.get("subject") == target_subject:
                    item["is_active_style_reference"] = (item.get("id") == record_id)
            cls.save_catalog(catalog)

    @classmethod
    def extract_text_from_sample_paper(cls, record: Dict[str, Any], max_pages: int = 4) -> str:
        """Extracts text from the sample question paper to feed into the Question Architect."""
        path = record.get("absolute_path", "")
        if not path or not os.path.exists(path):
            return ""

        _, ext = os.path.splitext(path)
        if ext.lower() != ".pdf":
            return f"[Sample Question Paper: {record.get('canonical_filename', '')}]"

        try:
            import pypdf
            reader = pypdf.PdfReader(path)
            extracted = []
            pages_to_read = min(len(reader.pages), max_pages)
            for i in range(pages_to_read):
                txt = reader.pages[i].extract_text() or ""
                if txt.strip():
                    extracted.append(f"--- SAMPLE PAPER PAGE {i + 1} ---\n{txt.strip()}")
            return "\n\n".join(extracted)
        except Exception as e:
            print(f"[SampleQuestionsEngine] Text extraction warning: {e}")
            return f"[Sample Paper: {record.get('canonical_filename', '')}]"
