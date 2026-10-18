"""
EXAM STUDY LEDGER & SCORE HISTORY ENGINE (SESSION 1/3 CLEAN COMPONENT)
----------------------------------------------------------------------
Clean, pure, decoupled module managing:
1. Subject Study Ledger (Homework, Chapters, Intra-Head Taxonomy)
2. Auto-sync from tharun_diary_format.json & Oct 12-17 Diary
3. Score History & Anti-Daydreaming Focus Verification Tracking
"""

import os
import sys
import json
import datetime
from typing import Dict, Any, List, Optional

from exam_ground_truth_v3 import BASE_DIR, EXAM_SYSTEM_DIR, DIARY_FILE

HOMEWORK_LOGS_DIR = os.path.join(EXAM_SYSTEM_DIR, "01_SUBJECT_HOMEWORK_LOGS")
LEDGER_FILE = os.path.join(HOMEWORK_LOGS_DIR, "subject_study_ledger.json")
SCORE_HISTORY_FILE = os.path.join(HOMEWORK_LOGS_DIR, "exam_score_history.json")


class SubjectStudyLedger:
    """
    Preserves and indexes every logged homework entry and study slab by:
    date, month, week_number (W1-W4), mode (balanced_daily, pre_exam, exam_sprint),
    class_standard (default "Class 8 CBSE"), subject, chapter_topic, task_description.
    """
    INTRA_HEAD_1 = "Head 1: Core Concepts & Principles"
    INTRA_HEAD_2 = "Head 2: Problem Solving & Applications"
    INTRA_HEAD_3 = "Head 3: Visual, Diagrammatic & Orthography"

    @staticmethod
    def load_ledger() -> Dict[str, Any]:
        os.makedirs(HOMEWORK_LOGS_DIR, exist_ok=True)
        if os.path.exists(LEDGER_FILE):
            try:
                with open(LEDGER_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "ledger_metadata": {
                "student_name": "Tharun",
                "current_class": "Class 8 CBSE",
                "school": "Senthil Public School, Dharmapuri",
                "last_updated": datetime.datetime.now().isoformat(),
                "total_entries": 0
            },
            "entries": []
        }

    @staticmethod
    def save_ledger(data: Dict[str, Any]):
        os.makedirs(HOMEWORK_LOGS_DIR, exist_ok=True)
        data.setdefault("ledger_metadata", {})
        data["ledger_metadata"]["last_updated"] = datetime.datetime.now().isoformat()
        data["ledger_metadata"]["total_entries"] = len(data.get("entries", []))
        with open(LEDGER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def categorize_into_intra_heads(cls, subject: str, chapter_topic: str = "", task_description: str = "") -> str:
        """
        Taxonomy Classifier: Organizes homework entries into 3 standardized Intra-Heads:
        - Head 1: Core Concepts, Laws, Formulas, Definitions, Theorems
        - Head 2: Problem Solving, Numericals, Grammar Rules, Step Calculations
        - Head 3: Diagrams, Constructions, Maps, Orthography / Spelling (Tamil/Hindi)
        """
        combined = f"{subject} {chapter_topic} {task_description}".lower()

        # Visual / Diagrammatic / Orthography (Head 3)
        h3_keywords = [
            "diagram", "sketch", "label", "labeled", "drawing", "construction",
            "map", "pointing", "timeline", "flame", "zones", "candle",
            "plant cell", "animal cell", "nitrogen cycle", "circuit",
            "மயங்கொலி", "வரிவடிவம்", "எழுத்துச் சீர்திருத்தம்", "பிழை திருத்தம்",
            "वर्तनी", "मात्रा", "शुद्ध वर्तनी", "letter writing format", "notice"
        ]
        if any(k in combined for k in h3_keywords):
            return cls.INTRA_HEAD_3

        # Problem Solving / Practical Application / Grammar (Head 2)
        h2_keywords = [
            "ex ", "ex:", "exercise", "q1", "q2", "q3", "q4", "solve", "solving",
            "hand-solving", "numerical", "p=f/a", "formula substitution", "calculate",
            "area", "volume", "perimeter", "factorization", "root extraction",
            "இலக்கணம்", "வேற்றுமை", "வல்லினம்", "வினா-விடை",
            "व्याकरण", "संज्ञा", "सर्वनाम", "कारक", "संधि", "समास",
            "grammar", "tenses", "reported speech", "active passive", "derivation"
        ]
        if any(k in combined for k in h2_keywords):
            return cls.INTRA_HEAD_2

        return cls.INTRA_HEAD_1

    @classmethod
    def record_entry(cls, date_str: str, subject: str, chapter_topic: str,
                     task_description: str, duration_mins: int = 30,
                     mode: str = "balanced_daily", week_num: int = None,
                     class_standard: str = "Class 8 CBSE", source: str = "homework_diary") -> Dict[str, Any]:
        ledger = cls.load_ledger()
        try:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            dt = datetime.datetime.now()
            date_str = dt.strftime("%Y-%m-%d")

        month_name = dt.strftime("%B")
        day_name = dt.strftime("%A")
        if week_num is None:
            day_of_month = dt.day
            week_num = min(4, ((day_of_month - 1) // 7) + 1)

        entry_id = f"HL-{date_str.replace('-', '')}-{len(ledger['entries'])+1:03d}"
        intra_head = cls.categorize_into_intra_heads(subject, chapter_topic, task_description)
        entry = {
            "entry_id": entry_id,
            "date": date_str,
            "month": month_name,
            "day_of_week": day_name,
            "week_number": week_num,
            "mode": mode,
            "class_standard": class_standard,
            "subject": subject,
            "chapter_topic": chapter_topic,
            "task_description": task_description,
            "study_duration_mins": duration_mins,
            "intra_head": intra_head,
            "source": source,
            "logged_at": datetime.datetime.now().isoformat()
        }

        existing = [e for e in ledger["entries"] if e.get("date") == date_str and e.get("subject") == subject and e.get("task_description") == task_description]
        if not existing:
            ledger["entries"].append(entry)
            cls.save_ledger(ledger)
        return entry

    @classmethod
    def auto_sync_from_diary_and_portions(cls) -> Dict[str, Any]:
        """Seed and synchronize ledger from tharun_diary_format.json and exam portions."""
        ledger = cls.load_ledger()
        if os.path.exists(DIARY_FILE):
            try:
                with open(DIARY_FILE, "r", encoding="utf-8") as f:
                    diary_data = json.load(f)
                for day_entry in diary_data.get("diary_entries", []):
                    d_str = day_entry.get("date")
                    hw_list = day_entry.get("items") or day_entry.get("homework_tasks") or day_entry.get("homework_items") or []
                    for hw in hw_list:
                        cls.record_entry(
                            date_str=d_str,
                            subject=hw.get("subject", "General"),
                            chapter_topic=hw.get("categorization_reason") or hw.get("chapter", "Homework practice"),
                            task_description=hw.get("task", ""),
                            duration_mins=hw.get("est_mins", 25),
                            source="school_diary"
                        )
            except Exception as e:
                print(f"[SubjectStudyLedger] Warning syncing diary: {e}")
        return cls.load_ledger()

    @classmethod
    def get_week_stats(cls, month: str = "October", week_number: Optional[Any] = None) -> Dict[str, Any]:
        """Summarizes homework entries and unique subjects across Weeks 1 to 4 for the given month."""
        ledger = cls.load_ledger()
        week_data = {
            "all": {"entries_count": 0, "subjects": set()},
            1: {"entries_count": 0, "subjects": set()},
            2: {"entries_count": 0, "subjects": set()},
            3: {"entries_count": 0, "subjects": set()},
            4: {"entries_count": 0, "subjects": set()},
            "monthend": {"entries_count": 0, "subjects": set()}
        }
        total_entries = 0
        for e in ledger.get("entries", []):
            if e.get("month", "").lower() == month.lower():
                w = e.get("week_number", 1)
                subj = e.get("subject", "General")
                if w in week_data:
                    week_data[w]["entries_count"] += 1
                    week_data[w]["subjects"].add(subj)
                week_data["all"]["entries_count"] += 1
                week_data["all"]["subjects"].add(subj)
                week_data["monthend"]["entries_count"] += 1
                week_data["monthend"]["subjects"].add(subj)
                total_entries += 1

        if week_number is not None:
            target = week_number
            if str(target).lower() in ("monthend", "month_end"):
                target = "monthend"
            elif str(target).lower() == "all":
                target = "all"
            else:
                try:
                    target = int(target)
                except Exception:
                    target = "all"
            data = week_data.get(target, {"entries_count": 0, "subjects": set()})
            cnt = data["entries_count"]
            scnt = len(data["subjects"])
            return {
                "count": cnt,
                "entries_count": cnt,
                "subject_count": scnt,
                "subjects_count": scnt,
                "subjects": list(data["subjects"])
            }

        stats: Dict[str, Any] = {"month": month, "total": total_entries}
        for k, v in week_data.items():
            stats[k] = {
                "count": v["entries_count"],
                "entries_count": v["entries_count"],
                "subject_count": len(v["subjects"]),
                "subjects_count": len(v["subjects"])
            }
        return stats


class ScoreHistoryTracker:
    """Tracks cumulative exam scores, percentages, and anti-daydreaming focus verification."""

    @staticmethod
    def load_score_history() -> List[Dict[str, Any]]:
        os.makedirs(HOMEWORK_LOGS_DIR, exist_ok=True)
        if os.path.exists(SCORE_HISTORY_FILE):
            try:
                with open(SCORE_HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    @staticmethod
    def save_score_history(history: List[Dict[str, Any]]):
        os.makedirs(HOMEWORK_LOGS_DIR, exist_ok=True)
        with open(SCORE_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    @classmethod
    def record_score(cls, record: Dict[str, Any]):
        history = cls.load_score_history()
        # Update if exists, else append
        existing = [h for h in history if h.get("exam_id") == record.get("exam_id")]
        if existing:
            existing[0].update(record)
        else:
            history.append(record)
        cls.save_score_history(history)
