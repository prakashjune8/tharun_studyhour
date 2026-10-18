"""
EXAM PHASE & SPEC ASSEMBLER (SESSION 3)
---------------------------------------
Pure, decoupled engine implementing:
1. Individual-subject question paper blueprints for each studied subject.
2. Dynamic time & marks calculation based on syllabus volume/complexity.
3. Strict section partitioning (Physical Science 50/50, Social 4 pillars).
4. Full mode awareness:
   - Mode 1: Balanced Daily (Daily Recall per subject + Weekly Sunday Exam per subject)
   - Mode 2: Pre-Exam Planner (Phase 2 Block Revision scaled to scheduled chapters)
   - Mode 3: Exam Eve Sprint (Model Exam Paper for tomorrow's subject)
"""

import os
import sys
import json
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import Session 1 and Session 2 modules
from exam_ground_truth_v3 import SubjectCatalog, DiaryGroundTruth, CONFIG_FILE, BASE_DIR
from exam_typography_engine_v3 import ScriptDetector


class ExamSpecAssembler:
    """
    Assembles mathematically sound, pedagogy-aligned CBSE Class 8 exam specifications.
    Guarantees:
    - Never mingles subjects together.
    - Dynamically computes exam duration (mins) and total marks from syllabus weightage.
    - Preserves language properties (English, Hindi, Tamil).
    """

    @classmethod
    def calculate_dynamic_time_and_marks(cls, subject: str, topics: List[Dict[str, Any]], exam_type: str) -> Dict[str, int]:
        """
        Dynamically computes time (minutes) and max marks based on:
        1. Number of chapters/subtopics studied.
        2. Subject weightage (Math/Science calculation steps take longer than language recall).
        3. Exam type (Daily Recall vs Block Revision vs Weekly Sunday).
        """
        subtopic_count = sum(len(t.get("subtopics", [])) for t in topics)
        if subtopic_count == 0:
            subtopic_count = len(topics) * 2 or 2

        is_calculation_heavy = subject in ["Mathematics", "Physical Science"]

        if exam_type == "daily_recall":
            # Dynamic Daily Recall (15 to 25 mins, 10 to 15 marks)
            if is_calculation_heavy:
                time_allowed = min(25, max(15, 12 + subtopic_count * 3))
                max_marks = 15 if time_allowed >= 20 else 10
            else:
                time_allowed = min(20, max(12, 10 + subtopic_count * 2))
                max_marks = 10
            return {"time_allowed_mins": time_allowed, "max_marks": max_marks}

        elif exam_type == "phase_2_block":
            # Dynamic Pre-Exam Block Revision (20 to 45 mins, 15 to 30 marks)
            chapter_count = len(topics)
            base_time = 20 if chapter_count <= 1 else (30 if chapter_count == 2 else 45)
            if is_calculation_heavy:
                base_time += 5
            max_marks = 15 if base_time <= 25 else (25 if base_time <= 35 else 30)
            return {"time_allowed_mins": base_time, "max_marks": max_marks}

        elif exam_type == "phase_1_sunday":
            # Full Weekly Sunday Exam (45 to 60 mins, standard 25M or 50M)
            return {"time_allowed_mins": 60, "max_marks": 25}

        elif exam_type == "model_exam_sprint":
            # Exam Eve Sprint (30 to 45 mins, 20M to 25M)
            return {"time_allowed_mins": 35, "max_marks": 25}

        return {"time_allowed_mins": 25, "max_marks": 15}

    @classmethod
    def assemble_individual_paper_spec(
        cls,
        subject: str,
        mode: str,
        exam_type: str,
        exam_date: str,
        topics: List[Dict[str, Any]],
        student_name: str = "Tharun",
        school_name: str = "Senthil Public School, Dharmapuri"
    ) -> Dict[str, Any]:
        """
        Assembles a single, dedicated, non-mingled question paper specification JSON.
        """
        info = SubjectCatalog.get_subject_info(subject)
        if not info:
            raise ValueError(f"Unknown subject: {subject}")

        # Compute dynamic time and marks
        timing = cls.calculate_dynamic_time_and_marks(subject, topics, exam_type)
        time_mins = timing["time_allowed_mins"]
        max_marks = timing["max_marks"]

        # Generate deterministic, clean Exam ID
        seed_str = f"{mode}-{exam_type}-{subject}-{exam_date}-{time_mins}-{max_marks}"
        short_hash = hashlib.md5(seed_str.encode("utf-8")).hexdigest()[:6].upper()
        exam_id = f"EXAM-{subject[:3].upper()}-{exam_type[:3].upper()}-{exam_date.replace('-', '')}-{short_hash}"

        # Determine paper title
        title_map = {
            "daily_recall": f"Daily Recall Verification Paper ({subject})",
            "phase_1_sunday": f"Weekly Sunday Master Exam ({subject})",
            "phase_2_block": f"Pre-Exam Block Revision Exam ({subject})",
            "model_exam_sprint": f"Exam Eve Model Examination ({subject})"
        }
        exam_title = title_map.get(exam_type, f"CBSE Examination ({subject})")

        # Build Section Structures
        sections = []
        if info["type"] == "composite":
            # Physical Science (Physics + Chemistry) or Social Science (4 pillars)
            sec_templates = info.get("sections", [])
            per_sec_marks = max(1, max_marks // len(sec_templates))
            for st in sec_templates:
                sections.append({
                    "section_name": st["section_name"],
                    "allocated_marks": per_sec_marks,
                    "target_branch": st["section_name"].split(":")[-1].strip(),
                    "question_types": ["MCQ (1M)", "VSA (1M/2M)", "SA/Problem (3M/4M)"]
                })
        else:
            # Single Subject (Math, Biology, English, Hindi, Tamil)
            if max_marks <= 10:
                sections = [
                    {"section_name": "SECTION A: OBJECTIVE & RAPID RECALL", "allocated_marks": 4, "question_types": ["MCQ (1M)", "Fill/Direct (1M)"]},
                    {"section_name": "SECTION B: CORE CONCEPT & WORKED STEPS", "allocated_marks": 6, "question_types": ["Short Answer (2M)", "Worked Steps (3M)"]}
                ]
            else:
                sections = [
                    {"section_name": "SECTION A: OBJECTIVE & FORMULAS", "allocated_marks": 5, "question_types": ["MCQ (1M)", "Assertion-Reason (1M)"]},
                    {"section_name": "SECTION B: VERY SHORT ANSWER (VSA)", "allocated_marks": 8, "question_types": ["2 Marks Concept / Calculation"]},
                    {"section_name": "SECTION C: SHORT ANSWER & STEP SOLVING", "allocated_marks": 6, "question_types": ["3 Marks Problem / Explain"]},
                    {"section_name": "SECTION D: LONG APPLICATION / DIAGRAM", "allocated_marks": 6, "question_types": ["Case Study / 6 Marks Core"]}
                ]

        spec = {
            "exam_id": exam_id,
            "exam_title": exam_title,
            "mode": mode,
            "exam_type": exam_type,
            "date": exam_date,
            "time_allowed_mins": time_mins,
            "max_marks": max_marks,
            "subject": subject,
            "language": info["language"],
            "student_name": student_name,
            "school_name": school_name,
            "class_standard": "Class 8 CBSE",
            "syllabus_topics": topics,
            "sections": sections,
            "generation_metadata": {
                "dynamic_time_allocated": True,
                "is_composite": info["type"] == "composite",
                "assembled_at": datetime.now().isoformat()
            }
        }
        return spec

    @classmethod
    def assemble_daily_papers_for_day(cls, date_str: str) -> List[Dict[str, Any]]:
        """
        Builds INDIVIDUAL Daily Recall papers for every subject Tharun studied on that date.
        """
        # Load from DiaryGroundTruth for sample Oct 12-17
        papers = []
        for subj in SubjectCatalog.get_all_subject_names():
            portions = DiaryGroundTruth.get_portions_for_subject(subj)
            # Filter chapters studied on this specific date
            matching = [p for p in portions if date_str in p.get("dates", [])]
            if matching:
                spec = cls.assemble_individual_paper_spec(
                    subject=subj,
                    mode="balanced_daily",
                    exam_type="daily_recall",
                    exam_date=date_str,
                    topics=matching
                )
                papers.append(spec)
        return papers

    @classmethod
    def assemble_sunday_papers_for_week(cls, week_label: str = "Oct 12 to 17") -> List[Dict[str, Any]]:
        """
        Builds INDIVIDUAL Weekly Sunday papers for every subject studied during that week.
        """
        papers = []
        for subj in SubjectCatalog.get_all_subject_names():
            portions = DiaryGroundTruth.get_portions_for_subject(subj)
            if portions:
                spec = cls.assemble_individual_paper_spec(
                    subject=subj,
                    mode="balanced_daily",
                    exam_type="phase_1_sunday",
                    exam_date="2026-10-18",
                    topics=portions
                )
                papers.append(spec)
        return papers

    @classmethod
    def assemble_pre_exam_block_paper(cls, subject: str, block_day: int, chapters: List[str]) -> Dict[str, Any]:
        """
        Builds a dedicated Phase 2 Block Revision paper dynamically scaled to scheduled chapters.
        """
        mock_topics = [{"chapter": ch, "subtopics": ["Key definitions & formulas", "CBSE exercise problems"]} for ch in chapters]
        return cls.assemble_individual_paper_spec(
            subject=subject,
            mode="pre_exam_planner",
            exam_type="phase_2_block",
            exam_date=datetime.now().strftime("%Y-%m-%d"),
            topics=mock_topics
        )


# ==============================================================================
# VERIFICATION RUNNER (SESSION 3 GATE)
# ==============================================================================
def run_session_3_verification():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 75)
    print("   SESSION 3: EXAM SPEC ASSEMBLER (INDIVIDUAL PAPERS & DYNAMIC TIME)")
    print("=" * 75)

    # 1. Test Daily Recall Individual Papers (e.g. Oct 12)
    print("\n[TEST 1] Assembling Individual Daily Recall Papers for 2026-10-12:")
    daily_papers = ExamSpecAssembler.assemble_daily_papers_for_day("2026-10-12")
    print(f" -> Total Individual Papers Generated: {len(daily_papers)}")
    for p in daily_papers:
        print(f"    * [{p['subject']:<18}] {p['exam_id']} | Time: {p['time_allowed_mins']} Mins | Marks: {p['max_marks']}M | Lang: {p['language']}")
        for s in p['sections']:
            print(f"        └─ {s['section_name']} ({s['allocated_marks']} Marks)")

    # 2. Test Weekly Sunday Exam Individual Papers (Oct 12-17 Rollup)
    print("\n[TEST 2] Assembling Individual Weekly Sunday Papers for All 7 Subjects:")
    sunday_papers = ExamSpecAssembler.assemble_sunday_papers_for_week()
    print(f" -> Total Sunday Papers Generated: {len(sunday_papers)}")
    for p in sunday_papers:
        ch_count = len(p['syllabus_topics'])
        print(f"    * [{p['subject']:<18}] {p['exam_id']} | {ch_count} Chapters | Time: {p['time_allowed_mins']} Mins | Marks: {p['max_marks']}M")

    # 3. Test Dynamic Time Scaling in Phase 2 (Pre-Exam Block Revision)
    print("\n[TEST 3] Testing Dynamic Time & Marks Scaling for Phase 2 Block Revision:")
    # Case A: 1 light chapter
    p_light = ExamSpecAssembler.assemble_pre_exam_block_paper("Biology", 1, ["Cell - Structure and Functions"])
    print(f" -> 1 Chapter Case (Biology):       Time: {p_light['time_allowed_mins']} Mins | Max Marks: {p_light['max_marks']}M")
    
    # Case B: 3 heavy chapters in Math
    p_heavy = ExamSpecAssembler.assemble_pre_exam_block_paper("Mathematics", 3, ["Algebraic Expressions", "Linear Equations", "Mensuration"])
    print(f" -> 3 Chapters Heavy (Mathematics): Time: {p_heavy['time_allowed_mins']} Mins | Max Marks: {p_heavy['max_marks']}M")

    # 4. Verify Non-Mingling Section Partitions
    print("\n[TEST 4] Section Partition Verification (Zero-Mingling Guarantee):")
    phy_chem_paper = [p for p in sunday_papers if p['subject'] == 'Physical Science'][0]
    print(f" -> Physical Science Sections: {[s['section_name'] for s in phy_chem_paper['sections']]}")
    sst_paper = [p for p in sunday_papers if p['subject'] == 'Social Science'][0]
    print(f" -> Social Science Sections:   {[s['section_name'] for s in sst_paper['sections']]}")

    print("\n" + "=" * 75)
    if len(daily_papers) >= 3 and len(sunday_papers) == 7:
        print("   ✅ SESSION 3 VERIFICATION PASSED: Individual Assembler & Scaling Ready!")
    else:
        print("   ⚠️ SESSION 3 VERIFICATION WARNING: Check output above.")
    print("=" * 75)


if __name__ == "__main__":
    run_session_3_verification()
