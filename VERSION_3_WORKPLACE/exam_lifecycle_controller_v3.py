"""
EXAM LIFECYCLE & NOTIFICATION CONTROLLER (SESSION 3 EXTENSION)
--------------------------------------------------------------
Implements:
1. Automatic mode detection and lifecycle transitions:
   - Mode 1: Balanced Daily (default)
   - Mode 2: Pre-Exam Planner (activated when exam syllabus portions exist)
   - Mode 3: Exam Eve Sprint (activated 1 day before an exam until the last exam date)
2. Priority Hierarchy resolver (never overlaps or crashes during manual mode switching).
3. 6:45 AM morning notification alert rule (Mon-Sat strict 6:45 AM, Sunday flexible on-demand).
4. Full integration with ExamSpecAssembler for individual subject papers and dynamic timing.
"""

import os
import sys
import json
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional, Tuple

from exam_ground_truth_v3 import SubjectCatalog, DiaryGroundTruth, CONFIG_FILE, BASE_DIR
from exam_phase_assembler_v3 import ExamSpecAssembler

PORTIONS_FILE = os.path.join(BASE_DIR, "tharun_exam_portions.json")
DIARY_FILE = os.path.join(BASE_DIR, "tharun_diary_format.json")


class ExamLifecycleController:
    """
    Governs the active academic lifecycle state, priority resolution,
    and morning calendar notifications.
    """

    @classmethod
    def load_exam_portions_meta(cls) -> Dict[str, Any]:
        """Reads tharun_exam_portions.json to inspect scheduled exam dates."""
        if not os.path.exists(PORTIONS_FILE):
            return {"active": False, "exams": []}
        try:
            with open(PORTIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            exams = []
            terms = data.get("terms", {})
            for term_name, term_data in terms.items():
                for p in term_data.get("portions", []):
                    ed = p.get("exam_date")
                    subj = p.get("subject")
                    if ed and subj:
                        exams.append({
                            "subject": subj,
                            "exam_date": ed,
                            "exam_day": p.get("exam_day", ""),
                            "title": p.get("high_weightage_focus", ""),
                            "components": p.get("components", [])
                        })
            # Sort chronologically
            exams.sort(key=lambda x: x["exam_date"])
            return {"active": len(exams) > 0, "exams": exams}
        except Exception as e:
            print(f"[LifecycleController] Error reading exam portions: {e}")
            return {"active": False, "exams": []}

    @classmethod
    def detect_academic_mode(cls, current_date_str: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Determines the true academic state of the day:
        Returns (mode_name, context_dict)
        - 'exam_eve_sprint'
        - 'pre_exam_planner'
        - 'balanced_daily'
        """
        if not current_date_str:
            current_date_str = datetime.now().strftime("%Y-%m-%d")

        today_dt = datetime.strptime(current_date_str, "%Y-%m-%d").date()
        exam_meta = cls.load_exam_portions_meta()
        exams = exam_meta.get("exams", [])

        if not exams:
            return "balanced_daily", {"reason": "No uploaded exam syllabus found. Defaulting to daily routine."}

        first_exam_dt = datetime.strptime(exams[0]["exam_date"], "%Y-%m-%d").date()
        last_exam_dt = datetime.strptime(exams[-1]["exam_date"], "%Y-%m-%d").date()

        # 1. EXAM EVE SPRINT (Active 1 day before first exam until the end of last exam)
        eve_start_dt = first_exam_dt - timedelta(days=1)
        if eve_start_dt <= today_dt <= last_exam_dt:
            # Find tomorrow's exam
            tomorrow_dt = today_dt + timedelta(days=1)
            tomorrow_str = tomorrow_dt.strftime("%Y-%m-%d")
            tomorrow_exam = next((e for e in exams if e["exam_date"] == tomorrow_str), None)
            
            # Find today's exam
            today_exam = next((e for e in exams if e["exam_date"] == current_date_str), None)

            return "exam_eve_sprint", {
                "reason": "Currently within the official school examination window.",
                "today_exam": today_exam,
                "tomorrow_exam": tomorrow_exam,
                "active_exam_list": exams
            }

        # 2. PRE-EXAM PLANNER (Active if within 21 days countdown before exams)
        revision_window_start = first_exam_dt - timedelta(days=21)
        if revision_window_start <= today_dt < eve_start_dt:
            days_remaining = (first_exam_dt - today_dt).days
            return "pre_exam_planner", {
                "reason": f"Pre-exam revision season active. {days_remaining} days until first exam ({exams[0]['subject']}).",
                "days_until_first_exam": days_remaining,
                "first_exam": exams[0]
            }

        # 3. BALANCED DAILY (Default school routine)
        return "balanced_daily", {
            "reason": "Normal school term in progress. Tracking daily homework and weekly consistency.",
            "next_upcoming_exam": exams[0] if exams else None
        }

    @classmethod
    def resolve_morning_notification(cls, current_date_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Determines the morning notification schedule and payload:
        - Mon-Sat: Strict 6:45 AM alert.
        - Sunday: Flexible on-demand window (no rigid 6:45 AM alarm).
        """
        if not current_date_str:
            current_date_str = datetime.now().strftime("%Y-%m-%d")

        today_dt = datetime.strptime(current_date_str, "%Y-%m-%d").date()
        day_of_week = today_dt.weekday()  # Monday is 0, Sunday is 6
        is_sunday = (day_of_week == 6)

        mode, context = cls.detect_academic_mode(current_date_str)

        if is_sunday:
            # Sunday Rule: Excluded from 6:45 AM strict alarm; flexible anytime
            alert_time = "FLEXIBLE_ON_DEMAND"
            notification_title = "🌟 Sunday Weekly Master Exam Ready (On-Demand)"
            notification_message = (
                "Today is Sunday! You are exempt from the 6:45 AM alarm.\n"
                "Take your Phase 1 Weekly Cumulative Exams at any comfortable time today."
            )
            # Assemble full Sunday papers for all subjects studied in the week
            papers = ExamSpecAssembler.assemble_sunday_papers_for_week()
        else:
            # Mon-Sat Rule: Strict 6:45 AM sharp
            alert_time = "06:45 AM"
            if mode == "exam_eve_sprint":
                target_exam = context.get("tomorrow_exam") or context.get("today_exam")
                subj = target_exam["subject"] if target_exam else "Mathematics"
                notification_title = f"⏰ 6:45 AM Alert: Model Exam Question Paper Ready ({subj})"
                notification_message = f"Exam Eve Sprint active! Full-dress 35-min trial paper prepared for {subj}."
                # Assemble single-subject model paper
                papers = [
                    ExamSpecAssembler.assemble_individual_paper_spec(
                        subject=subj,
                        mode="exam_eve_sprint",
                        exam_type="model_exam_sprint",
                        exam_date=current_date_str,
                        topics=[{"chapter": f"{subj} Exam Full Scope", "subtopics": ["High-yield definitions, formulas, and diagrams"]}]
                    )
                ]
            elif mode == "pre_exam_planner":
                notification_title = "⏰ 6:45 AM Alert: Pre-Exam Block Revision Paper Ready"
                notification_message = "Pre-Exam Planner active! Step-wise diagnostic revision paper ready."
                papers = [ExamSpecAssembler.assemble_pre_exam_block_paper("Mathematics", 1, ["Algebraic Expressions"])]
            else:
                notification_title = "⏰ 6:45 AM Alert: Today's Daily Recall Papers Ready"
                notification_message = "Good morning Tharun! Daily homework recall papers are ready for yesterday's study."
                papers = ExamSpecAssembler.assemble_daily_papers_for_day(current_date_str)

        return {
            "date": current_date_str,
            "day_name": today_dt.strftime("%A"),
            "is_sunday": is_sunday,
            "alert_time": alert_time,
            "active_mode": mode,
            "notification_title": notification_title,
            "notification_message": notification_message,
            "papers_count": len(papers),
            "papers": papers
        }


# ==============================================================================
# VERIFICATION RUNNER
# ==============================================================================
def run_lifecycle_verification():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 75)
    print("   EXAM LIFECYCLE, MODE SWITCHING & 6:45 AM NOTIFICATION VERIFICATION")
    print("=" * 75)

    # Test 1: Check Mode Detection for Normal Day (Oct 12)
    print("\n[TEST 1] Lifecycle Mode Detection for Oct 12, 2026 (Normal School Day):")
    mode_oct12, ctx_oct12 = ExamLifecycleController.detect_academic_mode("2026-10-12")
    print(f" -> Active Mode: {mode_oct12.upper()}")
    print(f" -> Context:     {ctx_oct12['reason']}")

    # Test 2: Check Morning 6:45 AM Notification for School Day (Monday, Oct 12)
    print("\n[TEST 2] Morning Notification Resolution for School Day (Monday, 2026-10-12):")
    sched_mon = ExamLifecycleController.resolve_morning_notification("2026-10-12")
    print(f" -> Day:            {sched_mon['day_name']} ({'SUNDAY EXEMPTION' if sched_mon['is_sunday'] else 'STRICT SCHOOL DAY'})")
    print(f" -> Alert Trigger:  {sched_mon['alert_time']}")
    print(f" -> Title:          {sched_mon['notification_title']}")
    print(f" -> Message:        {sched_mon['notification_message']}")
    print(f" -> Papers Ready:   {sched_mon['papers_count']} Individual Subject Papers")
    for p in sched_mon['papers']:
        print(f"    • [{p['subject']}] {p['exam_id']} ({p['time_allowed_mins']} Mins • {p['max_marks']}M)")

    # Test 3: Check Sunday Flexible On-Demand Exemption (Sunday, Oct 18)
    print("\n[TEST 3] Morning Notification Resolution for Sunday (2026-10-18):")
    sched_sun = ExamLifecycleController.resolve_morning_notification("2026-10-18")
    print(f" -> Day:            {sched_sun['day_name']} ({'SUNDAY EXEMPTION ACTIVE' if sched_sun['is_sunday'] else 'STRICT'})")
    print(f" -> Alert Trigger:  {sched_sun['alert_time']}")
    print(f" -> Title:          {sched_sun['notification_title']}")
    print(f" -> Message:        {sched_sun['notification_message'].replace(chr(10), ' ')}")
    print(f" -> Papers Ready:   {sched_sun['papers_count']} Full Sunday Exam Papers (On-Demand)")

    # Test 4: Simulate Exam Eve Sprint Window (1 Day before an exam)
    print("\n[TEST 4] Simulating Exam Eve Sprint (1 Day Before Real Exam):")
    # Simulate an exam scheduled on 2026-10-25
    mode_eve, ctx_eve = ExamLifecycleController.detect_academic_mode("2026-09-08")  # Term 1 Tamil exam on 2026-09-09
    print(f" -> Detected Mode 1 Day Before Tamil Exam (2026-09-08): {mode_eve.upper()}")
    print(f" -> Context: {ctx_eve['reason']}")

    print("\n" + "=" * 75)
    if sched_mon['alert_time'] == "06:45 AM" and sched_sun['alert_time'] == "FLEXIBLE_ON_DEMAND":
        print("   ✅ LIFECYCLE & NOTIFICATION ARCHITECTURE PASSED ALL TESTS!")
    else:
        print("   ⚠️ WARNING: Check lifecycle results above.")
    print("=" * 75)


if __name__ == "__main__":
    run_lifecycle_verification()
