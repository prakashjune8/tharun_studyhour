"""
EXAM ENGINE V3 — UNIFIED MODULAR FACADE (SESSION 1 TO 7 CLEAN RE-WRITE)
=======================================================================
Replaces the old legacy monolith with a lightweight, decoupled facade.
All operations are routed cleanly to their specialized engines:
- Subject Catalog & Decoupled Gateway: exam_ground_truth_v3.py (Session 1)
- Multilingual Typography: exam_typography_engine_v3.py (Session 2)
- 3-Phase Spec Assembler: exam_phase_assembler_v3.py (Session 3)
- Math & Fraction Engine: exam_math_fraction_engine_v3.py (Session 4)
- Zero-Hallucination Architect: exam_question_architect_v3.py (Session 4/7)
- Print Studio & Blank Workspace: exam_print_studio_v3.py (Session 5)
- Subject Vault & Smart Ingestion: exam_smart_ingestion_wizard_v3.py (Session 7)
- School Model Papers Engine: exam_sample_questions_engine_v3.py (Session 7)
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from exam_ground_truth_v3 import (
    BASE_DIR,
    EXAM_SYSTEM_DIR,
    CONFIG_FILE,
    DIARY_FILE,
    SubjectCatalog,
    DiaryGroundTruth,
    GeminiGateway
)
from exam_study_ledger_v3 import SubjectStudyLedger, ScoreHistoryTracker
from exam_phase_assembler_v3 import ExamSpecAssembler
from exam_question_architect_v3 import QuestionArchitectV3
from exam_print_studio_v3 import ExamPrintStudioV3
from exam_smart_ingestion_wizard_v3 import SmartIngestionWizard, TEXTBOOKS_VAULT_ROOT
from exam_sample_questions_engine_v3 import SampleQuestionsEngine, MODEL_PAPERS_VAULT_ROOT

# Directory constants for backward compatibility
HOMEWORK_LOGS_DIR = os.path.join(EXAM_SYSTEM_DIR, "01_SUBJECT_HOMEWORK_LOGS")
TEXTBOOKS_PDF_DIR = os.path.join(EXAM_SYSTEM_DIR, "02_UPLOADED_TEXTBOOKS_PDF")
QUESTION_PAPERS_DIR = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS")
ANSWER_SHEETS_DIR = os.path.join(EXAM_SYSTEM_DIR, "04_UPLOADED_ANSWER_SHEETS")
CORRECTED_COPIES_DIR = os.path.join(EXAM_SYSTEM_DIR, "05_CORRECTED_SOFT_COPIES")
MODEL_ANSWERS_DIR = os.path.join(EXAM_SYSTEM_DIR, "06_MODEL_ANSWER_REFERENCES")
SKILLS_DIR = os.path.join(EXAM_SYSTEM_DIR, "00_AGENT_SKILLS_AND_RUBRICS")


class ExamPhaseAssembler:
    """Delegates phase assembly to ExamSpecAssembler."""

    @classmethod
    def assemble_phase1_weekly_sunday_test(cls, week_number: int = 3, month: str = "October") -> Dict[str, Any]:
        papers = ExamSpecAssembler.assemble_sunday_papers_for_week(f"{month} Week {week_number}")
        total_m = sum(p.get("max_marks", 25) for p in papers) if papers else 35
        return {
            "phase": "Phase 1: Comprehensive Weekly Sunday Examination",
            "week_number": week_number,
            "month": month,
            "total_marks": total_m,
            "duration_mins": 60,
            "papers": papers
        }

    @classmethod
    def assemble_phase1_monthend_mega_exam(cls, month: str = "October") -> Dict[str, Any]:
        return {
            "phase": "Phase 1: Month-End Mega Examination",
            "month": month,
            "total_marks": 80,
            "duration_mins": 180,
            "sections": ["Section A: Math Core", "Section B: Science", "Section C: Social", "Section D: Languages"]
        }

    @classmethod
    def assemble_phase2_3day_checkpoint(cls, block_num: int = 1) -> Dict[str, Any]:
        paper = ExamSpecAssembler.assemble_pre_exam_block_paper("Mathematics", block_num * 3, ["Algebraic Expressions", "Linear Equations"])
        return {
            "phase": "Phase 2: Pre-Exam 3-Day Checkpoint Examination",
            "block_num": block_num,
            "total_marks": 25,
            "duration_mins": 60,
            "paper": paper
        }

    @classmethod
    def assemble_phase3_morning_sprint(cls, subject: str = "Mathematics") -> Dict[str, Any]:
        today_str = datetime.now().strftime("%Y-%m-%d")
        return ExamSpecAssembler.assemble_individual_paper_spec(
            subject=subject,
            mode="exam_eve_sprint",
            exam_type="morning_sprint",
            exam_date=today_str,
            topics=[{"chapter": f"{subject} High-Yield Core", "subtopics": ["Definitions", "Formulas", "Diagrams"]}]
        )


class GeminiExamClient:
    """
    Unified client facade routing generation, configuration, and print studio exports.
    """

    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        return GeminiGateway.load_config()

    @classmethod
    def save_config(cls, cfg: Dict[str, Any]):
        GeminiGateway.save_config(cfg)

    @classmethod
    def set_api_key(cls, key: str):
        cfg = cls.load_config()
        cfg["api_key"] = key.strip()
        cls.save_config(cfg)

    @classmethod
    def load_score_history(cls) -> List[Dict[str, Any]]:
        return ScoreHistoryTracker.load_score_history()

    @classmethod
    def record_score_history(cls, record: Dict[str, Any]):
        ScoreHistoryTracker.record_score(record)

    @classmethod
    def generate_question_paper(
        cls,
        spec: Dict[str, Any],
        textbook_pdf_name: Optional[str] = None,
        sample_question_paper_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Routes directly to QuestionArchitectV3 with zero hallucination and ground truth isolation."""
        paper = QuestionArchitectV3.generate_question_paper(
            spec=spec,
            textbook_pdf_name=textbook_pdf_name,
            sample_question_paper_id=sample_question_paper_id
        )

        exam_id = spec.get("exam_id") or paper.get("exam_id") or paper.get("metadata", {}).get("exam_id") or "TEST_EXAM_V3"
        paper["exam_id"] = exam_id
        if "metadata" in paper:
            paper["metadata"]["exam_id"] = exam_id

        os.makedirs(QUESTION_PAPERS_DIR, exist_ok=True)
        qp_file = os.path.join(QUESTION_PAPERS_DIR, f"{exam_id}.json")
        with open(qp_file, "w", encoding="utf-8") as f:
            json.dump(paper, f, indent=2, ensure_ascii=False)

        return paper

    @classmethod
    def render_question_paper_html(cls, qp_data: Dict[str, Any]) -> str:
        return ExamPrintStudioV3.render_question_paper_html(qp_data)

    @classmethod
    def render_question_paper_pdf(cls, qp_data: Dict[str, Any], output_path: str) -> str:
        filename = os.path.basename(output_path)
        inferred_id = filename.replace("_QUESTION_PAPER.pdf", "").replace(".pdf", "").strip()
        exam_id = inferred_id or qp_data.get("exam_id") or qp_data.get("metadata", {}).get("exam_id")
        if exam_id:
            qp_file = os.path.join(QUESTION_PAPERS_DIR, f"{exam_id}.json")
            try:
                with open(qp_file, "w", encoding="utf-8") as f:
                    json.dump(qp_data, f, indent=2, ensure_ascii=False)
            except Exception:
                pass
        return ExamPrintStudioV3.render_question_paper_pdf(qp_data, output_path)

    @classmethod
    def render_blank_answer_sheet_pdf(cls, qp_data: Dict[str, Any], output_path: str) -> str:
        return ExamPrintStudioV3.render_blank_answer_booklet_pdf(qp_data, output_path)

    @classmethod
    def evaluate_answer_sheet(cls, exam_id: str, files: Optional[List[str]] = None) -> Dict[str, Any]:
        """Routes answer ingestion and step-wise grading to VisionOCREngineV3 and CBSEEvaluatorV3."""
        from exam_vision_ocr_engine_v3 import VisionOCREngineV3
        from exam_evaluator_v3 import CBSEEvaluatorV3

        if files and len(files) > 0:
            VisionOCREngineV3.extract_and_align_responses(exam_id, files[0])

        return CBSEEvaluatorV3.evaluate_exam(exam_id)

    @classmethod
    def render_corrected_copy_html(cls, eval_res: Dict[str, Any]) -> str:
        from exam_evaluator_v3 import CBSEEvaluatorV3
        return CBSEEvaluatorV3.render_graded_html(eval_res)

    @classmethod
    def render_corrected_copy_pdf(cls, eval_res: Dict[str, Any], output_path: str) -> str:
        from exam_evaluator_v3 import CBSEEvaluatorV3
        return CBSEEvaluatorV3.render_graded_pdf(eval_res, output_path)

    @classmethod
    def render_model_answer_guide_html(cls, eval_res: Dict[str, Any]) -> str:
        from exam_evaluator_v3 import CBSEEvaluatorV3
        return CBSEEvaluatorV3.render_topper_guide_html(eval_res)

    @classmethod
    def render_model_answer_guide_pdf(cls, eval_res: Dict[str, Any], output_path: str) -> str:
        from exam_evaluator_v3 import CBSEEvaluatorV3
        return CBSEEvaluatorV3.render_topper_guide_pdf(eval_res, output_path)


# ==============================================================================
# VERIFICATION & SYSTEM FACADE HELPERS
# ==============================================================================
ERROR_BANK_FILE = os.path.join(BASE_DIR, "student_error_bank.json")
SCORE_HISTORY_FILE = os.path.join(HOMEWORK_LOGS_DIR, "exam_score_history.json")


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts raw text from a PDF file using pypdf."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text.strip()
    except Exception:
        return ""


def is_scanned_pdf(pdf_path: str) -> bool:
    """Returns True if the PDF has very little extractable text, indicating a scanned image."""
    txt = extract_text_from_pdf(pdf_path)
    return len(txt.strip()) < 100


def sync_eval_errors_to_error_bank(eval_res: Dict[str, Any]) -> int:
    """Syncs mistakes from evaluation into student_error_bank.json."""
    from exam_evaluator_v3 import CBSEEvaluatorV3
    CBSEEvaluatorV3._sync_to_error_bank(eval_res)
    if os.path.exists(ERROR_BANK_FILE):
        try:
            with open(ERROR_BANK_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            items = data if isinstance(data, list) else data.get("errors", [])
            return len(items)
        except Exception:
            pass
    return 1


def render_unified_binder_pdf(eval_res: Dict[str, Any], output_path: str):
    """Merges Question Paper, Graded Answer Sheet, and Topper Guide into a single physical binder PDF."""
    from exam_evaluator_v3 import CBSEEvaluatorV3
    exam_id = eval_res.get("exam_id", "EXAM")
    qp_pdf = os.path.join(QUESTION_PAPERS_DIR, f"{exam_id}_QUESTION_PAPER.pdf")
    corr_pdf = os.path.join(CORRECTED_COPIES_DIR, f"{exam_id}_CORRECTED_COPY.pdf")
    topper_pdf = os.path.join(MODEL_ANSWERS_DIR, f"{exam_id}_TOPPER_MODEL_GUIDE.pdf")

    sources = []
    for p in [qp_pdf, corr_pdf, topper_pdf]:
        if os.path.exists(p) and os.path.getsize(p) > 500:
            sources.append(p)

    if sources:
        try:
            from pypdf import PdfWriter
            merger = PdfWriter()
            for s in sources:
                merger.append(s)

            import time
            pdf_path = output_path
            try:
                merger.write(pdf_path)
            except PermissionError:
                fallback_path = pdf_path.replace(".pdf", f"_{int(time.time())}.pdf")
                merger.write(fallback_path)
                pdf_path = fallback_path
                print(f"Original file locked. Saved fallback as {fallback_path}")
            merger.close()
            return pdf_path
        except Exception as e:
            print(f"[ExamEngineV3] PdfWriter notice: {e}")

    # Fallback if merger not available
    return CBSEEvaluatorV3.render_graded_pdf(eval_res, output_path)


def load_score_history() -> List[Dict[str, Any]]:
    return ScoreHistoryTracker.load_score_history()


def record_exam_score_history(eval_res: Dict[str, Any], binder_pdf_path: str = "") -> Dict[str, Any]:
    rec = {
        "exam_id": eval_res.get("exam_id", ""),
        "subject": eval_res.get("subject", ""),
        "percentage": eval_res.get("percentage", 0),
        "grade": eval_res.get("grade", ""),
        "marks_scored": eval_res.get("marks_scored", 0),
        "max_marks": eval_res.get("max_marks", 0),
        "focus_verdict": eval_res.get("daydreaming_audit", {}).get("verdict", "Optimal"),
        "recorded_at": datetime.now().isoformat(),
        "binder_pdf_path": binder_pdf_path
    }
    ScoreHistoryTracker.record_score(rec)
    return rec
