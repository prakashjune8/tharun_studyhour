"""
NO-HOMEWORK DAY & WEAK-SUBJECT HEALING ENGINE (SESSION 3 EXTENSION)
------------------------------------------------------------------
Implements:
1. "No School Homework Today" handler in student diary format.
2. Error Bank analyzer that ranks subjects by mistake count & weakness.
3. Weak-Subject Evening Study Session logger.
4. Next-morning 6:45 AM "Weak-Subject Mastery Sprint" paper assembler.
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from exam_ground_truth_v3 import SubjectCatalog, BASE_DIR
from exam_phase_assembler_v3 import ExamSpecAssembler

DIARY_FILE = os.path.join(BASE_DIR, "tharun_diary_format.json")
ERROR_BANK_FILE = os.path.join(BASE_DIR, "student_error_bank.json")


class WeakSubjectHealingEngine:
    """
    Handles days with zero homework, ranking subjects by past mistakes
    and turning morning 6:45 AM tests into targeted Weak-Subject Mastery Sprints.
    """

    @classmethod
    def load_error_bank(cls) -> List[Dict[str, Any]]:
        """Loads all recorded student mistakes from student_error_bank.json."""
        if not os.path.exists(ERROR_BANK_FILE):
            return []
        try:
            with open(ERROR_BANK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WeakSubjectHealing] Warning loading error bank: {e}")
            return []

    @classmethod
    def analyze_weak_subjects(cls) -> List[Dict[str, Any]]:
        """
        Analyzes the error bank and ranks all subjects by mistake count and urgency.
        Returns a sorted list of weak subjects with recommended focus areas.
        """
        errors = cls.load_error_bank()
        counts: Dict[str, Dict[str, Any]] = {}

        for err in errors:
            subj = err.get("subject", "General")
            occ = err.get("occurrences", 1)
            cat = err.get("category", "General Mistake")
            trap = err.get("trap_word", "")

            if subj not in counts:
                counts[subj] = {
                    "subject": subj,
                    "total_errors": 0,
                    "top_categories": set(),
                    "sample_traps": []
                }
            counts[subj]["total_errors"] += occ
            counts[subj]["top_categories"].add(cat)
            if trap:
                counts[subj]["sample_traps"].append(trap)

        # Convert to list and sort descending by error count
        ranked = []
        for s, d in counts.items():
            ranked.append({
                "subject": s,
                "total_errors": d["total_errors"],
                "focus_categories": list(d["top_categories"])[:3],
                "sample_traps": d["sample_traps"][:3],
                "urgency": "HIGH" if d["total_errors"] >= 10 else ("MEDIUM" if d["total_errors"] >= 3 else "LOW")
            })
        ranked.sort(key=lambda x: x["total_errors"], reverse=True)
        return ranked

    @classmethod
    def mark_no_homework_day(
        cls,
        date_str: str,
        chosen_weak_subject: str,
        student_notes: str = "Self-study weak areas from past test error bank"
    ) -> Dict[str, Any]:
        """
        Records in the student diary that date_str had NO school homework,
        and logs the chosen weak subject for targeted evening study.
        """
        ranked = cls.analyze_weak_subjects()
        weak_info = next((r for r in ranked if r["subject"].lower() == chosen_weak_subject.lower()), None)
        focus_areas = weak_info["focus_categories"] if weak_info else ["Core concept review & past test paper corrections"]

        record = {
            "date": date_str,
            "is_no_homework_day": True,
            "chosen_weak_subject": chosen_weak_subject,
            "focus_areas": focus_areas,
            "student_notes": student_notes,
            "logged_at": datetime.now().isoformat()
        }

        # Update or record in diary file
        try:
            diary_data = {"diary_entries": []}
            if os.path.exists(DIARY_FILE):
                with open(DIARY_FILE, "r", encoding="utf-8") as f:
                    diary_data = json.load(f)

            entries = diary_data.get("diary_entries", [])
            # Find if day exists
            existing_day = next((e for e in entries if e.get("date") == date_str), None)
            if not existing_day:
                existing_day = {
                    "date": date_str,
                    "display_date": datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y"),
                    "items": []
                }
                entries.append(existing_day)

            existing_day["no_homework_flag"] = True
            existing_day["weak_subject_focus"] = record

            # Add study item so daily habit streak stays preserved!
            existing_day["items"].append({
                "subject": chosen_weak_subject,
                "code": chosen_weak_subject[:4],
                "task": f"Error Bank Mastery: {', '.join(focus_areas[:2])}",
                "task_type": "error_bank_healing",
                "est_mins": 35,
                "completed": True,
                "raw_source": f"No Homework Day: Strengthening {chosen_weak_subject} weak spots"
            })

            diary_data["diary_entries"] = entries
            with open(DIARY_FILE, "w", encoding="utf-8") as f:
                json.dump(diary_data, f, indent=2, ensure_ascii=False)

            return {"success": True, "record": record}
        except Exception as e:
            return {"success": False, "error": str(e), "record": record}

    @classmethod
    def assemble_weak_subject_morning_sprint(
        cls,
        date_str: str,
        subject: str,
        focus_areas: List[str]
    ) -> Dict[str, Any]:
        """
        Assembles a tailored 15-minute morning sprint paper targeting the student's weak spots.
        """
        topics = [
            {
                "chapter": f"Targeted Error Bank Healing: {subject}",
                "subtopics": focus_areas or ["Fundamental formula recall and sign error elimination"]
            }
        ]
        return ExamSpecAssembler.assemble_individual_paper_spec(
            subject=subject,
            mode="balanced_daily",
            exam_type="daily_recall",
            exam_date=date_str,
            topics=topics
        )


# ==============================================================================
# VERIFICATION RUNNER
# ==============================================================================
def run_healing_verification():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 75)
    print("   NO-HOMEWORK DAY & WEAK-SUBJECT ERROR BANK HEALING VERIFICATION")
    print("=" * 75)

    # 1. Test Error Bank Analysis & Subject Ranking
    print("\n[TEST 1] Analyzing Student Error Bank to Rank Weak Subjects:")
    ranked = WeakSubjectHealingEngine.analyze_weak_subjects()
    print(f" -> Found {len(ranked)} Subjects with Historical Mistake Records:")
    for r in ranked:
        print(f"    * [{r['urgency']:<6}] {r['subject']:<18} ({r['total_errors']} Mistakes Logged)")
        print(f"        └─ Weak Categories: {', '.join(r['focus_categories'])}")

    # 2. Simulate User Clicking "No Homework Today" and Choosing Top Weak Subject (Physical Science)
    top_subject = ranked[0]["subject"] if ranked else "Mathematics"
    test_date = "2026-10-19"
    print(f"\n[TEST 2] Simulating 'No Homework Day' for Date: {test_date}")
    print(f" -> Student Selects Recommended Top Weak Subject: {top_subject}")
    res = WeakSubjectHealingEngine.mark_no_homework_day(
        date_str=test_date,
        chosen_weak_subject=top_subject,
        student_notes="Review SI units in pressure calculations and negative signs in math"
    )
    print(f" -> Log Status: {'SUCCESS' if res['success'] else 'FAILED'}")
    print(f" -> Scheduled Focus: {res['record']['focus_areas']}")

    # 3. Test Generating the Next Morning's 6:45 AM Weak-Subject Mastery Sprint
    print(f"\n[TEST 3] Generating Next Morning 6:45 AM Weak-Subject Mastery Paper:")
    sprint_paper = WeakSubjectHealingEngine.assemble_weak_subject_morning_sprint(
        date_str=test_date,
        subject=top_subject,
        focus_areas=res['record']['focus_areas']
    )
    print(f" -> Generated Paper ID:  {sprint_paper['exam_id']}")
    print(f" -> Target Subject:      {sprint_paper['subject']}")
    print(f" -> Dynamic Time & Mark: {sprint_paper['time_allowed_mins']} Mins | {sprint_paper['max_marks']} Marks")
    print(f" -> Paper Title:         {sprint_paper['exam_title']}")
    for s in sprint_paper['sections']:
        print(f"    └─ {s['section_name']} ({s['allocated_marks']} Marks)")

    print("\n" + "=" * 75)
    if res['success'] and sprint_paper['exam_id']:
        print("   ✅ NO-HOMEWORK DAY HEALING ENGINE PASSED ALL TESTS!")
    else:
        print("   ⚠️ WARNING: Check healing engine output above.")
    print("=" * 75)


if __name__ == "__main__":
    run_healing_verification()
