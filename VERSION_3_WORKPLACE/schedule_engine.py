# Tharun Pedagogical Routine Balancer & Subject Representation Tracker
import os
import sys
import json
import re
from datetime import datetime, timedelta

def get_engine_data_path(filename):
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(os.path.abspath(sys.executable))
        target_path = os.path.join(base_dir, filename)
        if os.path.exists(target_path):
            return target_path
        parent_dir = os.path.dirname(base_dir)
        parent_target = os.path.join(parent_dir, filename)
        if os.path.exists(parent_target):
            return parent_target
        return target_path
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        target_path = os.path.join(base_dir, filename)
        if os.path.exists(target_path):
            return target_path
        cwd_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(cwd_path):
            return cwd_path
        return target_path

SUBJECT_AUDIT_FILE = get_engine_data_path("subject_representation_audit.json")
LEDGER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EXAM_SYSTEM_V3", "01_SUBJECT_HOMEWORK_LOGS", "subject_study_ledger.json")

EXECUTION_LEVELS = {
    1: {
        "title": "Level 1: 🔰 Genin Academy ('Sit & Finish' Chair-Time)",
        "badge": "🔰 Genin: Habit Foundation",
        "focus": "Building Tharun's ability to sit at the desk for the set duration without distraction, complete homework first, and do 1 core subject practice.",
        "target_hours_eve": 2.25,
        "target_hours_morn": 1.5,
        "eve_start": "19:00",
        "eve_end": "21:15",
        "morn_start": "06:00",
        "morn_end": "07:30",
        "break_duration": 10,
        "pomodoro_duration": 30
    },
    2: {
        "title": "Level 2: ⚡ Chunin Shinobi (Maths Solving + Diagrams + Language Clinic)",
        "badge": "⚡ Chunin: Balanced Rhythm",
        "focus": "Firm daily habit: Homework clearance + Daily Maths problem solving + 1 Science/Social diagram retention + Morning Language writing & spelling clinic.",
        "target_hours_eve": 3.0,
        "target_hours_morn": 1.5,
        "eve_start": "19:00",
        "eve_end": "22:00",
        "morn_start": "06:00",
        "morn_end": "07:30",
        "break_duration": 10,
        "pomodoro_duration": 40
    },
    3: {
        "title": "Level 3: 🔥 Jonin / Hokage (Autonomous Time Management & Peak Flow)",
        "badge": "🔥 Jonin / Hokage: Peak Mastery",
        "focus": "Full high-efficiency flow: Deep analytical solving, blind diagram reproduction, timed writing without spelling errors, self-driven time management.",
        "target_hours_eve": 3.0,
        "target_hours_morn": 1.5,
        "eve_start": "19:00",
        "eve_end": "22:00",
        "morn_start": "06:00",
        "morn_end": "07:30",
        "break_duration": 8,
        "pomodoro_duration": 45
    }
}



CANONICAL_SUBDIVISIONS = {
    "Mathematics": {
        "parent": "Mathematics",
        "category": "core",
        "is_math": True,
        "badge": "📐 Math Core",
        "guidance": "Maths Problem Solving: Step-by-step textbook exercises, algebra, geometries & proof practice.",
        "diagram_target": "Geometric Proofs & Coordinate Graphs"
    },
    "Physics": {
        "parent": "Physical Science",
        "category": "science",
        "is_math": False,
        "badge": "⚡ Physical Science (Physics)",
        "guidance": "Physics Concepts: Force, pressure, sound, friction, light reflection/refraction laws & ray diagrams.",
        "diagram_target": "Ray Optics / Electric Circuits"
    },
    "Chemistry": {
        "parent": "Physical Science",
        "category": "science",
        "is_math": False,
        "badge": "⚗️ Physical Science (Chemistry)",
        "guidance": "Chemistry Concepts: Synthetic fibres, metals/non-metals, combustion & flame, chemical reactions.",
        "diagram_target": "Chemical Apparatus & Reaction Flowcharts"
    },
    "Biology": {
        "parent": "Biological Science",
        "category": "science",
        "is_math": False,
        "badge": "🔬 Biological Science (Biology)",
        "guidance": "Biology Concepts: Cell structure & functions, microorganisms, reproduction in animals & life cycles.",
        "diagram_target": "Plant/Animal Cells & Microorganisms"
    },
    "History": {
        "parent": "Social Science",
        "category": "social",
        "is_math": False,
        "badge": "📜 Social Science (History)",
        "guidance": "History Timelines: Modern Indian history, timelines, revolt of 1857, trade to territory & cause-effect analysis.",
        "diagram_target": "Historical Timelines & Trade Routes"
    },
    "Geography": {
        "parent": "Social Science",
        "category": "social",
        "is_math": False,
        "badge": "🌍 Social Science (Geography)",
        "guidance": "Geography Concepts: Resources, agriculture, industries, soil profiles, climate zones & map plotting.",
        "diagram_target": "India Map Plotting & Soil Horizons"
    },
    "Civics": {
        "parent": "Social Science",
        "category": "social",
        "is_math": False,
        "badge": "⚖️ Social Science (Civics)",
        "guidance": "Civics Concepts: Indian Constitution, secularism, parliament, judiciary & fundamental rights.",
        "diagram_target": "Governance Organs & Parliamentary Structure"
    },
    "Tamil": {
        "parent": "Tamil",
        "category": "language",
        "is_math": False,
        "badge": "✍️ தமிழ் பயிர்ச்சி",
        "guidance": "Tamil Clinic: 'ழ, ள, ல' மற்றும் 'ண, ந, ன' ஒலி வேறுபாடுகள், செய்யுள் வரிகள் & சொந்த நடை வாக்கியங்கள்.",
        "diagram_target": "Tamil Mind-Map & Grammar Tree"
    },
    "English": {
        "parent": "English",
        "category": "language",
        "is_math": False,
        "badge": "✍️ English Clinic",
        "guidance": "English Clinic: Grammar, vocabulary, error bank correction, reading comprehension & expressive writing.",
        "diagram_target": "Grammar Flowcharts & Concept Maps"
    },
    "Hindi": {
        "parent": "Hindi",
        "category": "language",
        "is_math": False,
        "badge": "✍️ हिंदी अभ्यास",
        "guidance": "Hindi Clinic: वर्तनी सुधार (मात्राएँ ि/ी, ु/ू), व्याकरण अभ्यास और स्वतंत्र लेखन।",
        "diagram_target": "Hindi Vocabulary Trees & Sentence Frames"
    }
}

class SubjectRepresentationTracker:
    """
    Maintains exhaustive audit logs of subject and internal subdivision representation
    across 7-day and 30-day windows to enforce equal representation and parent verification.
    """
    def __init__(self, audit_file_path=None, ledger_file_path=None):
        self.audit_file_path = audit_file_path
        self.ledger_file_path = ledger_file_path
        self.audit_data = {
            "metadata": {
                "student": "Tharun",
                "class": "Class 8 CBSE",
                "school": "Senthil Public School, Dharmapuri",
                "last_updated": datetime.now().isoformat(),
                "total_events": 0
            },
            "history": []
        }
        self.load()

    def load(self):
        if self.audit_file_path and os.path.exists(self.audit_file_path):
            try:
                with open(self.audit_file_path, "r", encoding="utf-8") as f:
                    self.audit_data = json.load(f)
                    return
            except Exception as e:
                print(f"Error reading audit file {self.audit_file_path}: {e}")

        # Pre-seed from historical subject_study_ledger.json if available
        if self.ledger_file_path and os.path.exists(self.ledger_file_path):
            try:
                with open(self.ledger_file_path, "r", encoding="utf-8") as f:
                    ledger = json.load(f)
                entries = ledger.get("entries", [])
                for e in entries:
                    sub = e.get("subject", "")
                    task = e.get("chapter_topic", "") + " " + e.get("task_description", "")
                    sd = self.detect_subdivision(sub, task)
                    self.audit_data["history"].append({
                        "date": e.get("date", "2026-10-06"),
                        "slot_type": "homework",
                        "subdivision": sd,
                        "parent": CANONICAL_SUBDIVISIONS.get(sd, {}).get("parent", sub),
                        "duration_mins": e.get("study_duration_mins", 25)
                    })
                self.audit_data["metadata"]["total_events"] = len(self.audit_data["history"])
                self.save()
            except Exception as e:
                print(f"Error seeding representation audit from ledger: {e}")

    def save(self):
        if not self.audit_file_path:
            return
        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.audit_file_path)), exist_ok=True)
            with open(self.audit_file_path, "w", encoding="utf-8") as f:
                json.dump(self.audit_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving representation audit data: {e}")

    @staticmethod
    def detect_subdivision(sub_str, task_str=""):
        txt = (sub_str + " " + task_str).lower()
        if "math" in txt:
            return "Mathematics"
        if "physic" in txt or "phy" in txt:
            return "Physics"
        if "chem" in txt:
            return "Chemistry"
        if "bio" in txt:
            return "Biology"
        if "his" in txt:
            return "History"
        if "geo" in txt:
            return "Geography"
        if "civic" in txt or "pol" in txt:
            return "Civics"
        if "tamil" in txt or "தமிழ்" in txt:
            return "Tamil"
        if "hindi" in txt or "हिंदी" in txt:
            return "Hindi"
        if "eng" in txt:
            return "English"
        if "sci" in txt:
            return "Physics"
        if "social" in txt or "sst" in txt:
            return "History"
        return "Mathematics"

    def get_counts(self, days=7):
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        counts = {k: 0 for k in CANONICAL_SUBDIVISIONS}
        for ev in self.audit_data.get("history", []):
            ev_date = ev.get("date", "")
            if not ev_date or ev_date >= cutoff_date:
                sd = ev.get("subdivision")
                if sd in counts:
                    counts[sd] += 1
        return counts

    def pick_balanced_candidate(self, candidate_subdivisions, exclude_subdivisions=None, days=7):
        if exclude_subdivisions is None:
            exclude_subdivisions = set()
        valid_candidates = [c for c in candidate_subdivisions if c not in exclude_subdivisions]
        if not valid_candidates:
            valid_candidates = candidate_subdivisions

        counts = self.get_counts(days=days)
        # Sort ascending by count (lowest count first = highest deficit/starvation priority)
        sorted_candidates = sorted(valid_candidates, key=lambda c: (counts.get(c, 0), c))
        return sorted_candidates[0]

    def record_event(self, date_str, slot_type, subdivision, duration_mins):
        self.audit_data["history"].append({
            "date": date_str,
            "slot_type": slot_type,
            "subdivision": subdivision,
            "parent": CANONICAL_SUBDIVISIONS.get(subdivision, {}).get("parent", subdivision),
            "duration_mins": duration_mins
        })
        self.audit_data["metadata"]["total_events"] = len(self.audit_data["history"])
        self.audit_data["metadata"]["last_updated"] = datetime.now().isoformat()
        self.save()


class DailyExamSubjectRotator:
    """
    Governs automated cyclical subject rotation for the 6:45 AM Host Exam slot.
    Follows pedagogical rotation rules:
    1. Priority 1 (Yesterday's Diary Homework):
       If yesterday had homework in core subjects, rotate among those subjects
       so Tharun's 6:45 AM exam directly verifies yesterday's retention.
    2. Priority 2 (Weak Subject / Error Bank Elevate):
       If student has uncorrected errors in student_error_bank.json for a subject,
       that subject gets priority elevation.
    3. Priority 3 (Default Weekly Day-of-Week Cycle):
       - Monday: Mathematics
       - Tuesday: Physical Science (Physics/Chemistry)
       - Wednesday: Biological Science (Biology)
       - Thursday: Social Science (History/Geography/Civics)
       - Friday: Tamil
       - Saturday: English / Hindi
       - Sunday: Exempt from strict 6:45 AM alarm (Flexible On-Demand Master Exam)
    """

    WEEKDAY_ROTATION = {
        0: "Mathematics",        # Monday
        1: "Physical Science",   # Tuesday
        2: "Biological Science", # Wednesday
        3: "Social Science",     # Thursday
        4: "Tamil",              # Friday
        5: "English",            # Saturday
        6: "Sunday Master Exam"  # Sunday
    }

    @classmethod
    def pick_morning_exam_subject(cls, target_date=None, diary_items=None) -> Tuple[str, str, bool]:
        """
        Returns (subject_name, selection_reason, is_sunday).
        """
        if not target_date:
            target_date = datetime.now().strftime("%Y-%m-%d")

        try:
            dt = datetime.strptime(target_date, "%Y-%m-%d")
        except Exception:
            dt = datetime.now()

        weekday = dt.weekday()
        is_sunday = (weekday == 6)

        if is_sunday:
            return ("Sunday Weekly Master Exam", "Sunday rule: Flexible on-demand timing (exempt from 6:45 AM alarm)", True)

        # 1. Check yesterday's diary homework
        yesterday_dt = dt - timedelta(days=1)
        yesterday_str = yesterday_dt.strftime("%Y-%m-%d")

        hw_subjects = []
        diary_path = get_engine_data_path("tharun_diary_format.json")
        if os.path.exists(diary_path):
            try:
                with open(diary_path, "r", encoding="utf-8") as f:
                    d_data = json.load(f)
                for ent in d_data.get("diary_entries", []):
                    if ent.get("date") == yesterday_str:
                        for it in ent.get("items", ent.get("subjects", [])):
                            s_name = it.get("subject", "")
                            if s_name and s_name not in hw_subjects:
                                hw_subjects.append(s_name)
            except Exception:
                pass

        # If diary_items is provided and represents today/yesterday, inspect them
        if not hw_subjects and diary_items:
            for it in diary_items:
                s_name = it.get("subject") if isinstance(it, dict) else getattr(it, "subject", "")
                if s_name and s_name not in hw_subjects:
                    hw_subjects.append(s_name)

        # Filter for core candidates from yesterday's homework
        core_hw = [s for s in hw_subjects if s in ["Mathematics", "Physical Science", "Biological Science", "Social Science", "Physics", "Chemistry", "Biology", "History", "Geography"]]

        # Check Weak Subjects from student_error_bank.json
        error_bank_path = get_engine_data_path("student_error_bank.json")
        weak_subjects = []
        if os.path.exists(error_bank_path):
            try:
                with open(error_bank_path, "r", encoding="utf-8") as f:
                    eb = json.load(f)
                err_list = eb if isinstance(eb, list) else eb.get("errors", [])
                for item in err_list:
                    if not item.get("mastered", False):
                        sub = item.get("subject")
                        if sub and sub not in weak_subjects:
                            weak_subjects.append(sub)
            except Exception:
                pass

        # Align yesterday's core subjects with weekly rhythm cycle
        target_weekday_subj = cls.WEEKDAY_ROTATION.get(weekday, "Mathematics")
        for s in hw_subjects:
            if target_weekday_subj.lower() in s.lower() or s.lower() in target_weekday_subj.lower():
                return (s, f"Rotated for today's {dt.strftime('%A')} focus from yesterday's homework ({yesterday_str})", False)

        # If weak subjects exist and were in yesterday's homework, prioritize them
        for s in core_hw:
            if any(ws.lower() in s.lower() for ws in weak_subjects):
                return (s, f"Prioritized from yesterday's homework ({yesterday_str}) & active Error Bank weak subject drill", False)

        # If yesterday had core homework, pick dynamically using rotating offset
        if core_hw:
            rot_idx = (weekday + dt.day) % len(core_hw)
            chosen_s = core_hw[rot_idx]
            return (chosen_s, f"Cyclical rotation across yesterday's homework ({yesterday_str})", False)

        # If weak subjects exist, pick top weak subject
        if weak_subjects:
            return (weak_subjects[0], "Selected from Error Bank priority (weak subject active reinforcement drill)", False)

        # Fallback to weekday rotation cycle
        default_subj = cls.WEEKDAY_ROTATION.get(weekday, "Mathematics")
        day_name = dt.strftime("%A")
        return (default_subj, f"Weekly cyclical rotation ({day_name} core exam slot)", False)


PRE_EXAM_21_DAYS = [
    {
        "day": 1,
        "phase": 1,
        "phase_name": "Phase 1: Portion Completion & Foundation",
        "title": "Tamil Poetry & Math Rational Numbers",
        "focus_core": "Mathematics",
        "core_topic": "Ch-1 Rational Numbers (Ex 1.4, pp.25-32)",
        "focus_second": "Tamil",
        "second_topic": "செய்யுள் (தமிழ்மொழி வாழ்த்து, மரபு, ஓடை) & வினா-விடை",
        "guidance_core": "Solve rational operations on number line and closure/associative properties by hand on rough paper.",
        "guidance_second": "Recite 3 poems with rhythm, answer line-by-line questions without guidebook.",
        "morning_task": "Rational number operations speed test + Tamil கடின சொற்கள் (ழ, ள, ல) error check."
    },
    {
        "day": 2,
        "phase": 1,
        "phase_name": "Phase 1: Portion Completion & Foundation",
        "title": "Physical Science (Refraction) & Tamil Thirukkural",
        "focus_core": "Physical Science",
        "core_topic": "Physics Ln-1 Refraction of Light (pp.7-24)",
        "focus_second": "Tamil",
        "second_topic": "திருக்குறள் (1-10) மனப்பாடப் பகுதி & பொருள் அறிதல்",
        "guidance_core": "Understand laws of refraction, refractive index formula, and real vs apparent depth.",
        "guidance_second": "Write Thirukkural 1 to 10 twice on rough paper from memory. Check punctuation and சீர்/அசை.",
        "morning_task": "Write all 10 Thirukkural without peeking + Snell's law formula flash review."
    },
    {
        "day": 3,
        "phase": 1,
        "phase_name": "Phase 1: Portion Completion & Foundation",
        "title": "Social Science (1857 Revolt) & Math Squares & Cubes",
        "focus_core": "Mathematics",
        "core_topic": "Ch-2 Squares/Square Roots & Cubes (Ex 2.2, 2.5, pp.47, 58-64)",
        "focus_second": "Social Science",
        "second_topic": "History Ln-3 The Revolt of 1857 (pp.37-53)",
        "guidance_core": "Hand-solve square roots by long division method and cube roots by prime factorization.",
        "guidance_second": "Draft 5-point structured answers for causes of 1857 Revolt (Political, Military, Religious).",
        "morning_task": "Memorize squares up to 30 and cubes up to 15 + Revolt 1857 timeline recall."
    },
    {
        "day": 4,
        "phase": 1,
        "phase_name": "Phase 1: Portion Completion & Foundation",
        "title": "Biological Science (Heart & Circulation) & English Grammar",
        "focus_core": "Biological Science",
        "core_topic": "Ln-1 Transportation in Animals (pp.7-20)",
        "focus_second": "English",
        "second_topic": "Grammar Ch 1-3 (Parts of Speech, Countable/Uncountable, Articles)",
        "guidance_core": "Draw internal structure of human heart, label 4 chambers, valves, and double circulation path.",
        "guidance_second": "Solve 15 exercises on article rules (a/an/the) and countable/uncountable nouns.",
        "morning_task": "Blind redrawing of Human Heart diagram + 10 articles test."
    },
    {
        "day": 5,
        "phase": 1,
        "phase_name": "Phase 1: Portion Completion & Foundation",
        "title": "Hindi Lessons 1-2 & Math Ratio & Proportion",
        "focus_core": "Mathematics",
        "core_topic": "Ch-3 Ratio and Proportion (pp.67-84)",
        "focus_second": "Hindi",
        "second_topic": "Ln-1 Hindusthan Hamara & Ln-2 Pariksha (pp.8-21)",
        "guidance_core": "Solve unitary method and direct/inverse proportion word problems by hand.",
        "guidance_second": "Read stories carefully, write word meanings (शब्दार्थ), and answer short questions in Hindi.",
        "morning_task": "Ratio proportion word problem sprint + Hindi spelling Error Bank test."
    },
    {
        "day": 6,
        "phase": 1,
        "phase_name": "Phase 1: Portion Completion & Foundation",
        "title": "Physical Science (Atom Structure I) & Social Resources",
        "focus_core": "Physical Science",
        "core_topic": "Chemistry Ln-1 Structure of the Atom I (pp.7-24)",
        "focus_second": "Social Science",
        "second_topic": "Geography Ln-1 Resources & Ln-2 Land, Soil, Water (pp.3-44)",
        "guidance_core": "Thomson plum pudding model, Rutherford alpha scattering experiment, atomic number and mass number.",
        "guidance_second": "Differentiate renewable vs non-renewable resources, soil profile layers, and water conservation.",
        "morning_task": "Subatomic particles table (p, n, e charges & masses) + Soil conservation points."
    },
    {
        "day": 7,
        "phase": 1,
        "phase_name": "Phase 1: Portion Completion & Foundation",
        "title": "Week 1 Consolidation & Active Blurting Review",
        "focus_core": "Mathematics & Science",
        "core_topic": "Week 1 Problem Solving Review & Formula Retention",
        "focus_second": "Tamil & Hindi",
        "second_topic": "Thirukkural Recitation & Hindi Spelling Error Bank",
        "guidance_core": "Blurting test: On a blank paper, write down every formula, definition, and diagram from Days 1-6.",
        "guidance_second": "Verify weak points from textbook. Re-attempt any sums answered incorrectly during the week.",
        "morning_task": "Full formula blurting sheet without looking at any notebook."
    },
    {
        "day": 8,
        "phase": 2,
        "phase_name": "Phase 2: High-Weight Concepts & Blind Testing",
        "title": "Math Shapes & Tamil Prose (தமிழர் மருத்துவம்)",
        "focus_core": "Mathematics",
        "core_topic": "Ch-4 Understanding Shapes (pp.87-110)",
        "focus_second": "Tamil",
        "second_topic": "உரைநடை இயல் 1-3 (வரிவடிவ வளர்ச்சி, நிலம் பொது, தமிழர் மருத்துவம்)",
        "guidance_core": "Polygon angle sum formula (n-2)×180°, quadrilateral classifications, diagonal properties.",
        "guidance_second": "Write 5-mark answers on தமிழர் மருத்துவம் and நிலம் பொது in your own sentences.",
        "morning_task": "Shape angle sum calculations + Tamil prose keywords retention."
    },
    {
        "day": 9,
        "phase": 2,
        "phase_name": "Phase 2: High-Weight Concepts & Blind Testing",
        "title": "Biological Science (Plants Xylem/Phloem) & Hindi Writing",
        "focus_core": "Biological Science",
        "core_topic": "Ln-2 Transportation in Plants (pp.30-41)",
        "focus_second": "Hindi",
        "second_topic": "General Writing: Vigyapan Lekhan & Chitra Varnan (pp.6-17)",
        "guidance_core": "Blind diagram of xylem and phloem, explain transpiration pull, root hair absorption, and translocation.",
        "guidance_second": "Draft 1 neat Advertisement box (विज्ञापन) and 1 Picture description (चित्र वर्णन) paragraph.",
        "morning_task": "Blind redrawing of Plant Vascular Bundle (Xylem/Phloem) + Hindi Vigyapan layout."
    },
    {
        "day": 10,
        "phase": 2,
        "phase_name": "Phase 2: High-Weight Concepts & Blind Testing",
        "title": "Physical Science (Lenses & Rays) & Social Agriculture",
        "focus_core": "Physical Science",
        "core_topic": "Physics Ln-2 Lenses (pp.35-51)",
        "focus_second": "Social Science",
        "second_topic": "Geography Ln-3 Agriculture (pp.45-65)",
        "guidance_core": "Draw 6 ray diagrams for convex lens (object at 2F, between F and 2F, etc.), lens formula and power.",
        "guidance_second": "Subsistence vs commercial agriculture, conditions for Rice, Wheat, Cotton, Tea crops.",
        "morning_task": "Convex lens 6 ray diagrams quick sketch + Crop distribution check."
    },
    {
        "day": 11,
        "phase": 2,
        "phase_name": "Phase 2: High-Weight Concepts & Blind Testing",
        "title": "Math Data Handling & English Literature",
        "focus_core": "Mathematics",
        "core_topic": "Ch-5 Data Handling (pp.113-134)",
        "focus_second": "English",
        "second_topic": "Literature (Historic Delhi, Entertainment, The Letter A pp.12-42)",
        "guidance_core": "Draw bar graphs, double bar graphs, pie charts (central angle calculations), and probability problems.",
        "guidance_second": "Draft character sketches and theme-based answers in own words without guidebook clichés.",
        "morning_task": "Pie chart central angle formula + English character sketches keywords."
    },
    {
        "day": 12,
        "phase": 2,
        "phase_name": "Phase 2: High-Weight Concepts & Blind Testing",
        "title": "Biological Science (Neuron/Brain) & Tamil Grammar (யாப்பு)",
        "focus_core": "Biological Science",
        "core_topic": "Ln-3 Control and Coordination (pp.52-63)",
        "focus_second": "Tamil",
        "second_topic": "இலக்கணம் (எழுத்துகளின் பிறப்பு, வினைமுற்று, எச்சம், யாப்பு)",
        "guidance_core": "Blind diagram of Neuron, reflex arc pathway, cerebrum/cerebellum/medulla functions, endocrine glands.",
        "guidance_second": "Practice grammar exercises: identify வினைமுற்று vs பெயரெச்சம்/வினையெச்சம், யாப்பு உறுப்புகள் (எழுத்து, அசை, சீர்).",
        "morning_task": "Blind redrawing of Neuron & Reflex Arc + Tamil இலக்கண விதிகள் recall."
    },
    {
        "day": 13,
        "phase": 2,
        "phase_name": "Phase 2: High-Weight Concepts & Blind Testing",
        "title": "High-Weight Math (Sets & Functions) & Chemistry Periodic Table",
        "focus_core": "Mathematics",
        "core_topic": "Ch-6 Sets & Ch-7 Functions (pp.137-172)",
        "focus_second": "Physical Science",
        "second_topic": "Chemistry Ln-3 Periodic Properties (pp.66-78)",
        "guidance_core": "Set representations, union, intersection, difference, Venn diagrams, function domain/range/codomain.",
        "guidance_second": "Modern periodic law, periodic trends across periods and down groups (valency, atomic radius, metallic nature).",
        "morning_task": "Venn diagram shading rules + Function mappings check + Periodic trends recall."
    },
    {
        "day": 14,
        "phase": 2,
        "phase_name": "Phase 2: High-Weight Concepts & Blind Testing",
        "title": "Week 2 Blind Test Sprint (Science Diagrams & Math Formulas)",
        "focus_core": "Science & Mathematics",
        "core_topic": "Full Blind Retrieval Sprint: Heart, Neuron, Lenses, Atom Models",
        "focus_second": "Languages & Social",
        "second_topic": "Thirukkural 1-10 + Hindi 1-25 Sentences + Constitution Preamble",
        "guidance_core": "Redraw all 4 high-weight diagrams with zero reference. Grade labels with red pen. Solve 5 tough math sums.",
        "guidance_second": "Self-test on languages: write 10 Thirukkural without error, recite Hindi sentences 1-25.",
        "morning_task": "Master blind drawing sheet + 10-minute all-formula memory checkpoint."
    },
    {
        "day": 15,
        "phase": 3,
        "phase_name": "Phase 3: Mock Drills & Reverse Countdown",
        "title": "High-Weight Math (Matrices Hand-Solving) & Hindi Lab",
        "focus_core": "Mathematics",
        "core_topic": "Ch-8 Matrices (pp.175-189)",
        "focus_second": "Hindi",
        "second_topic": "Language Lab & Spoken Sentences 1-25 (pp.2-10, 20-21)",
        "guidance_core": "Matrix order (m×n), types of matrices, matrix addition, subtraction, scalar multiplication by hand.",
        "guidance_second": "Recite and write Hindi spoken sentences 1-25, practice self-introduction dialog (अपना परिचय).",
        "morning_task": "Matrix addition/multiplication speed test + Hindi spoken sentences recall."
    },
    {
        "day": 16,
        "phase": 3,
        "phase_name": "Phase 3: Mock Drills & Reverse Countdown",
        "title": "Bio (Reproduction) & Social 1857 Map Work",
        "focus_core": "Biological Science",
        "core_topic": "Ln-4 Animal Reproduction (pp.73-87)",
        "focus_second": "Social Science",
        "second_topic": "Civics Ln-1 Constitution & Map Work (1857 Centers, Soil, Crops)",
        "guidance_core": "Asexual reproduction diagrams (Amoeba binary fission, Hydra budding), sexual reproduction stages, metamorphosis.",
        "guidance_second": "Mark 1857 Revolt centers (Delhi, Meerut, Jhansi, Kanpur) on India outline map; review Constitution preamble.",
        "morning_task": "Amoeba fission & Hydra budding diagrams + India map centers check."
    },
    {
        "day": 17,
        "phase": 3,
        "phase_name": "Phase 3: Mock Drills & Reverse Countdown",
        "title": "English Composition Sprint & Physics Static Electricity",
        "focus_core": "English",
        "core_topic": "Composition: Formal/Informal Letter, Story & Article (pp.6-17)",
        "focus_second": "Physical Science",
        "second_topic": "Physics Ln-3 Static Electricity & Chem Atom II (pp.36-55, 61-77)",
        "guidance_core": "Draft 1 Formal Letter to Principal and 1 Article with proper title, layout, and paragraph breaks.",
        "guidance_second": "Electroscope working, charging by induction, Bohr model electron configuration (2,8,8 rule).",
        "morning_task": "Formal letter layout flash review + Electron shell configurations check."
    },
    {
        "day": 18,
        "phase": 3,
        "phase_name": "Phase 3: Mock Drills & Reverse Countdown",
        "title": "English Grammar Master Drill & Social Full Revision",
        "focus_core": "English",
        "core_topic": "Grammar Master Sprint: Tenses, Modals, Gerunds (pp.32-70)",
        "focus_second": "Social Science",
        "second_topic": "Complete Review: History, Geography, Civics 5-Markers",
        "guidance_core": "Rapid solve 25 mixed grammar questions; test present/past/future tense conversions and modals.",
        "guidance_second": "Review 5-point summaries for Company Power, Rural Life, Revolt 1857, and Constitution.",
        "morning_task": "English tenses conversion matrix + Civics fundamental rights recall."
    },
    {
        "day": 19,
        "phase": 3,
        "phase_name": "Phase 3: Mock Drills & Reverse Countdown",
        "title": "Reverse Alignment: Tamil & Maths Full Revision",
        "focus_core": "Tamil",
        "core_topic": "Complete Term-I Portion (செய்யுள், உரைநடை, துணைப்பாடம், கடிதம்/கட்டுரை)",
        "focus_second": "Mathematics",
        "second_topic": "8 Chapters Formula Flashcards & high-probability sums",
        "guidance_core": "Check all Tamil question answers; write 1 essay on பொதுக் கட்டுரை without assistance.",
        "guidance_second": "Quick solve 1 sum from each of the 8 Math chapters (Rational to Matrices).",
        "morning_task": "Tamil Thirukkural 1-10 + Math all-chapter formula flashcards."
    },
    {
        "day": 20,
        "phase": 3,
        "phase_name": "Phase 3: Mock Drills & Reverse Countdown",
        "title": "Pre-Exam Mock Sprint: Tamil (Exam 09.09) Simulated Paper",
        "focus_core": "Tamil",
        "core_topic": "1.5-Hour Mock Question Paper Solving (Question Bank & Workbook)",
        "focus_second": "Tamil",
        "second_topic": "திருக்குறள் 1-10 Perfect Recitation & வினா-விடை Speed Writing",
        "guidance_core": "Sit in quiet room with exam clock. Answer entire question paper with neat handwriting.",
        "guidance_second": "Cross-check spelling errors in Error Bank notebook. Zero late-night reading.",
        "morning_task": "Tamil Error Bank words test (ழ, ள, ல, ண, ந, ன) + calm mindset."
    },
    {
        "day": 21,
        "phase": 3,
        "phase_name": "Phase 3: Mock Drills & Reverse Countdown",
        "title": "Final Pre-Exam Eve: Tamil Exam Eve Mastery & Mindset Lock",
        "focus_core": "Tamil",
        "core_topic": "Final High-Yield Revision (Thirukkural, Grammar Rules, Key Prose Qs)",
        "focus_second": "Exam Hall Kit Audit & Restful Sleep",
        "second_topic": "Pack Hall Ticket, 2 Pens, Pencil, Eraser, Scale",
        "guidance_core": "Light review only! No new topics. Verify Exam Hall kit (pens, pencil, hall ticket).",
        "guidance_second": "Inviolable 10:00 PM sleep! Neocortical memory consolidation guarantees peak focus tomorrow!",
        "morning_task": "Formula & poem visual glance only. Confident departure for exam hall!"
    }
]


def build_dynamic_pre_exam_roadmap(total_days=21, portions_data=None):
    """
    Dynamically generates an optimal, phased Pre-Exam preparation roadmap
    for ANY duration (e.g. 7-day sprint, 10-day crash, 14-day mid-term, 21-day standard, 28-day comprehensive).
    Adapts according to teachers' variable announcement timelines and exam date proximity.
    """
    total_days = max(3, min(45, int(total_days)))
    if total_days == 21 and not portions_data:
        return PRE_EXAM_21_DAYS

    core_cycle = [
        ("Mathematics", "Ch-1 Rational Numbers & Squares", "Tamil", "செய்யுள் & திருக்குறள் (1-10)", "Math speed-sums + Thirukkural error check"),
        ("Physical Science", "Physics: Refraction & Lenses", "Social Science", "History: Revolt of 1857 Causes", "Lens ray diagrams + 1857 timeline recall"),
        ("Mathematics", "Ch-3 Ratio, Shapes & Mensuration", "English", "Grammar (Tenses, Articles, Modals)", "Formula sheet blurting + 10 articles test"),
        ("Biological Science", "Heart Circulation & Neurons", "Hindi", "Lessons 1-4 & Vigyapan Lekhan", "Blind Human Heart diagram + Hindi spelling test"),
        ("Mathematics", "Ch-5 Data Handling, Sets & Functions", "Social Science", "Geography: Resources & Agriculture", "Sets Venn diagram solving + Map pointing"),
        ("Physical Science", "Chemistry: Structure of Atom & Periodic", "Tamil", "உரைநடை & இலக்கணம் (எழுத்துகளின் பிறப்பு)", "Atomic models sketch + Tamil grammar recall"),
        ("Biological Science", "Plant Circulation (Xylem/Phloem) & Growth", "English", "Composition & Literature Question-Answers", "Plant vascular bundle sketch + Formal letter draft")
    ]

    roadmap = []
    for d in range(1, total_days + 1):
        if total_days <= 7:
            phase = 1 if d <= max(1, total_days // 2) else 2
            phase_name = "Phase 1: Rapid Portion Blitz & Formula Lock" if phase == 1 else "Phase 2: Active Recall & Mock Tests"
        elif total_days <= 16:
            phase = 1 if d <= (total_days // 2) else 2
            phase_name = "Phase 1: Portion Mastery & Foundation" if phase == 1 else "Phase 2: Blind Tests & High-Weight Blitz"
        else:
            p1_end = total_days // 3
            p2_end = (2 * total_days) // 3
            if d <= p1_end:
                phase = 1
                phase_name = "Phase 1: Portion Completion & Foundation"
            elif d <= p2_end:
                phase = 2
                phase_name = "Phase 2: High-Weight Concepts & Blind Testing"
            else:
                phase = 3
                phase_name = "Phase 3: Mock Papers & Active Blurting"

        if d == total_days:
            title = "Final Pre-Exam Confidence Run & Sleep Protocol"
            focus_core = "Mathematics & Science"
            core_topic = "Formula Lock & Mistake Diary Review"
            focus_sec = "Languages"
            sec_topic = "Spelling Bank & Active Recall"
            morn = "Final active blurting sheet + 10:00 PM sleep boundary lock"
            g_core = "Review error log and key formulas without cramming."
            g_sec = "Spelling accuracy and calm mental priming."
        elif d == total_days - 1 and total_days >= 5:
            title = "Full Exam Simulation & Timed Mock Papers"
            focus_core = "Mathematics"
            core_topic = "Timed 2.5-hour Question Paper Hand-Solving"
            focus_sec = "Science"
            sec_topic = "Blind Diagram Test & Definitions"
            morn = "Timed paper simulation on lined paper"
            g_core = "Strict timed conditions, handwriting speed, and step presentation."
            g_sec = "Blind diagram accuracy without guidebook help."
        else:
            item = core_cycle[(d - 1) % len(core_cycle)]
            focus_core = item[0]
            core_topic = item[1]
            focus_sec = item[2]
            sec_topic = item[3]
            morn = item[4]
            title = f"{focus_core} & {focus_sec}"
            g_core = f"Deep hand practice and problem solving on {core_topic}."
            g_sec = f"Active self-writing and memorization for {sec_topic}."

        roadmap.append({
            "day": d,
            "phase": phase,
            "phase_name": phase_name,
            "title": title,
            "focus_core": focus_core,
            "core_topic": core_topic,
            "focus_second": focus_sec,
            "second_topic": sec_topic,
            "guidance_core": g_core,
            "guidance_second": g_sec,
            "morning_task": morn
        })

    return roadmap


# Pre-configured diary entries matching Tharun's Senthil Public School diary


class TharunScheduleBalancer:
    """
    Pedagogical Routine Balancer for Tharun:
    - Accepts Senthil Public School Diary entries for any chosen date
    - Dynamically generates AT MOST 1 OR 2 HOMEWORK SLOTS as strictly requested
    - Allocates time specifically for each subject indicated
    - Daily Core 1: Mathematics Problem Solving
    - Core 2: Science / Social Science Diagram & Concept Memory
    - Morning: Core Concept Active Recall + Language Clinic (Tamil / English / Hindi)
    """

    _rep_tracker = None

    @classmethod
    def get_representation_tracker(cls):
        if cls._rep_tracker is None:
            cls._rep_tracker = SubjectRepresentationTracker(SUBJECT_AUDIT_FILE, LEDGER_FILE)
        return cls._rep_tracker

    @classmethod
    def generate_schedule(cls, subjects, diary_items, current_level=2, selected_language="English (Language)", exam_mode=False, exam_subject="Mathematics", start_time_str="19:00", pre_exam_mode=False, pre_exam_day=1, pre_exam_duration_days=21, bedtime_rollovers=None, target_date=None):
        lvl = EXECUTION_LEVELS.get(current_level, EXECUTION_LEVELS[2])

        if pre_exam_mode:
            return cls._generate_pre_exam_prep_schedule(subjects, day_num=pre_exam_day, current_level=current_level, start_time_str=start_time_str, duration_days=pre_exam_duration_days)

        if exam_mode:
            return cls._generate_exam_sprint_schedule(subjects, diary_items, exam_subject, lvl, start_time_str=start_time_str)

        evening_slots = []
        morning_slots = []

        sub_math = next((s for s in subjects if "math" in s["name"].lower()), {"name": "Mathematics", "gravity": 3})
        sub_phy_sci = next((s for s in subjects if "physical" in s["name"].lower() or ("phy" in s["name"].lower() and "bio" not in s["name"].lower())), None)
        if not sub_phy_sci:
            sub_phy_sci = next((s for s in subjects if "sci" in s["name"].lower() and "bio" not in s["name"].lower()), {"name": "Physical Science", "gravity": 3})
        sub_bio_sci = next((s for s in subjects if "bio" in s["name"].lower()), {"name": "Biological Science", "gravity": 3})
        sub_sci = sub_phy_sci
        sub_sst = next((s for s in subjects if "social" in s["name"].lower() or "sst" in s["name"].lower()), {"name": "Social Science", "gravity": 2})
        sub_tamil = next((s for s in subjects if "tamil" in s["name"].lower() or "தமிழ்" in s["name"].lower()), {"name": "Tamil", "gravity": 2})
        sub_eng = next((s for s in subjects if "eng" in s["name"].lower()), {"name": "English", "gravity": 2})
        sub_hindi = next((s for s in subjects if "hindi" in s["name"].lower() or "हिंदी" in s["name"].lower()), {"name": "Hindi", "gravity": 2})

        # Bag pack reminders (e.g., Bring science lab manual)
        bag_reminders = [it["task"] for it in diary_items if it.get("task_type") == "bag_pack"]

        try:
            cur_time = datetime.strptime(start_time_str, "%H:%M")
        except Exception:
            cur_time = datetime.strptime(lvl["eve_start"], "%H:%M")

        target_mins = int(lvl["target_hours_eve"] * 60)
        eve_end_time = cur_time + timedelta(minutes=target_mins)

        # Determine phase descriptor based on starting hour
        if cur_time.hour < 12:
            phase_label = "Holiday Morning Focus"
        elif cur_time.hour < 17:
            phase_label = "Afternoon Focus"
        else:
            phase_label = "Evening Focus"

        # -------------------------------------------------------------
        # PHASE 0: AFTER-SCHOOL TRANSITION & CHILL ZONE (5:40 - 6:30 PM)
        # -------------------------------------------------------------
        # Inviolable parental rule: Protect the 5:40 - 6:30 PM gap from TV distraction
        if cur_time.hour >= 17:
            transition_slot = {
                "phase": "Evening Transition",
                "start": "05:40 PM",
                "end": "06:30 PM",
                "duration_mins": 50,
                "title": "Unplugged Chill Zone & Physical Reset",
                "subject": "Transition & Sensory Reset",
                "type": "prep",
                "badge": "🧘 Chill Zone (50m)",
                "guidance": (
                    "Mandatory After-School Transition Protocol (5:40 - 6:30 PM):\n"
                    "1. 5:40–6:00 PM: Warm shower, fresh clothes & evening snack (resets sensory fatigue).\n"
                    "2. 6:00–6:30 PM: Unplugged Chill Zone (Zero TV/screens! Rest eyes, hydrate, listen to music).\n"
                    "💡 Inviolable Rule: No TV before study! TV is earned after 8:45 PM."
                ),
                "is_completed": False
            }
            evening_slots.append(transition_slot)

        # -------------------------------------------------------------
        # PHASE 1: EVENING STUDY PLAN (Multi-Subject Core Efficiency Slabs)
        # -------------------------------------------------------------
        # Include ALL diary homework items so subjects are faithfully scheduled in the timetable!
        study_hw_items = [it for it in diary_items if it.get("task_type") != "bag_pack"]
        hw_sub_texts = [(it.get("subject", "") + " " + it.get("code", "")).lower() for it in study_hw_items]
        hw_has_math = any("math" in t for t in hw_sub_texts)
        hw_has_phy = any(any(k in t for k in ["phy", "physics", "chem", "chemistry", "physical"]) for t in hw_sub_texts)
        hw_has_bio = any(any(k in t for k in ["bio", "biology", "biological"]) for t in hw_sub_texts)
        hw_has_sci = hw_has_phy or hw_has_bio or any("sci" in t for t in hw_sub_texts)
        hw_has_sst = any(any(k in t for k in ["social", "sst", "his", "history", "geo", "geography", "civic"]) for t in hw_sub_texts)
        hw_has_tamil = any(any(k in t for k in ["tamil", "தமிழ்"]) for t in hw_sub_texts)
        hw_has_eng = any(any(k in t for k in ["eng", "english"]) for t in hw_sub_texts)
        hw_has_hin = any(any(k in t for k in ["hindi", "हिंदी"]) for t in hw_sub_texts)

        if study_hw_items:
            # Sort items by cognitive category to enable effective interleaving:
            # 1: Mathematics (highest cognitive demand first)
            # 2: Language (Tamil / English - shifts from numbers to words for cognitive reset)
            # 3: Science (Physics / Chemistry / Biology - concepts, equations & diagrams)
            # 4: Social Science (History / Geography - reading & timelines)
            # 5: Other tasks
            def get_sub_category_priority(item):
                sub_str = (item.get("subject", "") + " " + item.get("code", "")).lower()
                if "math" in sub_str:
                    return 1
                if any(k in sub_str for k in ["tamil", "தமிழ்", "eng", "hindi", "language"]):
                    return 2
                if any(k in sub_str for k in ["sci", "phy", "chem", "bio"]):
                    return 3
                if any(k in sub_str for k in ["social", "sst", "his", "geo", "civic"]):
                    return 4
                return 5

            sorted_hw_items = sorted(study_hw_items, key=get_sub_category_priority)

            for idx, item in enumerate(sorted_hw_items):
                is_done = item.get("completed", False)
                sub_name = item.get("subject", "General")
                code_name = item.get("code", sub_name[:4])
                task_text = item.get("task", "")
                est_mins = max(10, item.get("est_mins", 20))
                sub_str = (sub_name + " " + code_name).lower()
                is_math = "math" in sub_str
                is_science = any(k in sub_str for k in ["sci", "phy", "chem", "bio"])
                is_social = any(k in sub_str for k in ["social", "sst", "his", "geo", "civic"])
                is_core = is_math or is_science or is_social
                is_lang = any(k in sub_str for k in ["tamil", "தமிழ்", "eng", "hindi", "language"])

                done_badge_prefix = "✅ Done · " if is_done else ""
                done_title_prefix = "✅ [Done] " if is_done else ""

                # Core Subject Efficiency Splitting:
                # 1. Mathematics is clubbed into a single 30 min focused slot (no split)
                if is_math:
                    math_slot_mins = 30
                    end_math = cur_time + timedelta(minutes=math_slot_mins)
                    math_title = f"{done_title_prefix}Core Math: {task_text}" if task_text else f"{done_title_prefix}Core Math Problem Solving"
                    evening_slots.append({
                        "phase": f"{phase_label}: {sub_name}",
                        "start": cur_time.strftime("%I:%M %p"),
                        "end": end_math.strftime("%I:%M %p"),
                        "duration_mins": math_slot_mins,
                        "title": math_title,
                        "subject": sub_name,
                        "type": "homework",
                        "badge": f"{done_badge_prefix}📐 Math Core",
                        "guidance": "Core Math Problem Solving: 30-minute dedicated focused solving block. Focus 100% on formulas, step-by-step layout, and working textbook questions carefully on copy without skipping intermediate calculations.",
                        "is_completed": is_done
                    })
                    cur_time = end_math

                # 2. Science & Social Science Core Splitting (if >= 25 mins)
                elif (is_science or is_social) and est_mins >= 25:
                    half1 = max(12, est_mins // 2)
                    half2 = est_mins - half1

                    # Slab 1: Core Concept / Step-by-Step Theory Sprint
                    end1 = cur_time + timedelta(minutes=half1)
                    if is_science:
                        spec_icon = "⚡" if "phy" in sub_str else ("⚗️" if "chem" in sub_str else "🔬")
                        badge1 = f"{done_badge_prefix}{spec_icon} Science Core (Sprint 1)"
                        title1 = f"{done_title_prefix}Core Science Sprint 1: {sub_name} - {task_text} (Theory & Concepts)"
                        guidance1 = f"Core Science Efficiency Sprint 1: Deep concept understanding, law/formula review, and active reading of key definitions before writing answers."
                    else:
                        badge1 = f"{done_badge_prefix}🌍 Social Core (Sprint 1)"
                        title1 = f"{done_title_prefix}Core Social Sprint 1: {sub_name} - {task_text} (Timeline & Analysis)"
                        guidance1 = f"Core Social Efficiency Sprint 1: Understand sequence of events, key dates, geography maps, and causes/effects in textbook."

                    evening_slots.append({
                        "phase": f"{phase_label}: {sub_name} (Slab 1/2)",
                        "start": cur_time.strftime("%I:%M %p"),
                        "end": end1.strftime("%I:%M %p"),
                        "duration_mins": half1,
                        "title": title1,
                        "subject": sub_name,
                        "type": "homework",
                        "badge": badge1,
                        "guidance": guidance1,
                        "is_completed": is_done
                    })
                    cur_time = end1

                    # Micro-Break between the two split slabs (4 mins)
                    micro_break_dur = 4
                    end_mbrk = cur_time + timedelta(minutes=micro_break_dur)
                    evening_slots.append({
                        "phase": f"{phase_label} Micro-Rest",
                        "start": cur_time.strftime("%I:%M %p"),
                        "end": end_mbrk.strftime("%I:%M %p"),
                        "duration_mins": micro_break_dur,
                        "title": f"Chakra Recharge ({sub_name} Micro-Break)",
                        "subject": "Rest & Posture",
                        "type": "break",
                        "badge": f"☕ Micro-Rest ({micro_break_dur}m)",
                        "guidance": "Put the pen down! Shake out wrist and fingers, take 3 deep belly breaths, sip water before Sprint 2.",
                        "is_completed": is_done
                    })
                    cur_time = end_mbrk

                    # Slab 2: Problem Solving Completion / Accuracy Verification / Diagrams
                    end2 = cur_time + timedelta(minutes=half2)
                    if is_science:
                        spec_icon = "⚡" if "phy" in sub_str else ("⚗️" if "chem" in sub_str else "🔬")
                        badge2 = f"{done_badge_prefix}{spec_icon} Science Core (Sprint 2)"
                        title2 = f"{done_title_prefix}Core Science Sprint 2: {sub_name} - {task_text} (Diagrams & Q&A)"
                        guidance2 = "Core Science Efficiency Sprint 2: Sketch and label diagrams accurately from memory, and write precise point-wise answers."
                    else:
                        badge2 = f"{done_badge_prefix}🌍 Social Core (Sprint 2)"
                        title2 = f"{done_title_prefix}Core Social Sprint 2: {sub_name} - {task_text} (Answer Framing)"
                        guidance2 = "Core Social Efficiency Sprint 2: Frame structured point-wise answers in your own words. Understanding > rote copying."

                    evening_slots.append({
                        "phase": f"{phase_label}: {sub_name} (Slab 2/2)",
                        "start": cur_time.strftime("%I:%M %p"),
                        "end": end2.strftime("%I:%M %p"),
                        "duration_mins": half2,
                        "title": title2,
                        "subject": sub_name,
                        "type": "homework",
                        "badge": badge2,
                        "guidance": guidance2,
                        "is_completed": is_done
                    })
                    cur_time = end2

                elif is_lang and est_mins >= 25:
                    # Language efficiency split: Writing + Spelling Clinic
                    half1 = 15
                    half2 = est_mins - half1
                    end1 = cur_time + timedelta(minutes=half1)
                    evening_slots.append({
                        "phase": f"{phase_label}: {sub_name} (Writing)",
                        "start": cur_time.strftime("%I:%M %p"),
                        "end": end1.strftime("%I:%M %p"),
                        "duration_mins": half1,
                        "title": f"{done_title_prefix}Language Writing: {sub_name} - {task_text}",
                        "subject": sub_name,
                        "type": "homework",
                        "badge": f"{done_badge_prefix}✍️ Language (Writing)",
                        "guidance": f"Focus on neat handwriting and structured expression: {task_text}.",
                        "is_completed": is_done
                    })
                    cur_time = end1

                    micro_break_dur = 3
                    end_mbrk = cur_time + timedelta(minutes=micro_break_dur)
                    evening_slots.append({
                        "phase": f"{phase_label} Micro-Rest",
                        "start": cur_time.strftime("%I:%M %p"),
                        "end": end_mbrk.strftime("%I:%M %p"),
                        "duration_mins": micro_break_dur,
                        "title": f"Eye Rest ({sub_name})",
                        "subject": "Rest",
                        "type": "break",
                        "badge": f"☕ Micro-Rest ({micro_break_dur}m)",
                        "guidance": "Rest eyes away from the page, stretch neck and shoulders.",
                        "is_completed": is_done
                    })
                    cur_time = end_mbrk

                    end2 = cur_time + timedelta(minutes=half2)
                    lang_guidance = (
                        "Tamil Spelling Clinic: Check letters with similar sounds (ழ, ள, ல, ண, ந, ன, ற, ர). Correct mistakes immediately!"
                        if "tamil" in sub_str or "தமிழ்" in sub_str else
                        "Spelling & Grammar Check: Re-read your written answers to catch spelling slips and punctuation errors."
                    )
                    evening_slots.append({
                        "phase": f"{phase_label}: {sub_name} (Clinic)",
                        "start": cur_time.strftime("%I:%M %p"),
                        "end": end2.strftime("%I:%M %p"),
                        "duration_mins": half2,
                        "title": f"{done_title_prefix}Language Spelling Clinic: {sub_name} (Accuracy Check)",
                        "subject": sub_name,
                        "type": "homework",
                        "badge": f"{done_badge_prefix}🔍 Language Clinic",
                        "guidance": lang_guidance,
                        "is_completed": is_done
                    })
                    cur_time = end2

                else:
                    # Single dedicated focused slab for this subject
                    end_hw = cur_time + timedelta(minutes=est_mins)
                    if is_math:
                        badge = f"{done_badge_prefix}📐 Math Core (Sprint)"
                        title = f"{done_title_prefix}Core Math Sprint: {task_text}"
                        guidance = f"Maths problem solving: {task_text}. Solve step-by-step on copy."
                    elif is_science:
                        spec_icon = "⚡" if "phy" in sub_str else ("⚗️" if "chem" in sub_str else "🔬")
                        badge = f"{done_badge_prefix}{spec_icon} Science Core"
                        title = f"{done_title_prefix}Core Science: {sub_name} - {task_text}"
                        guidance = f"Science concept & question mastery: {task_text}. Active recall of keywords."
                    elif is_social:
                        badge = f"{done_badge_prefix}🌍 Social Core"
                        title = f"{done_title_prefix}Core Social: {sub_name} - {task_text}"
                        guidance = f"Social science task: {task_text}. Focus on timelines, maps, and concepts."
                    elif is_lang:
                        badge = f"{done_badge_prefix}✍️ Language Clinic"
                        title = f"{done_title_prefix}Language Clinic: {sub_name} - {task_text}"
                        guidance = f"Language task: {task_text}. Focus on neat handwriting, zero spelling errors."
                    else:
                        badge = f"{done_badge_prefix}📝 School Diary HW"
                        title = f"{done_title_prefix}Diary Task: {sub_name} - {task_text}"
                        guidance = f"School diary task: {task_text}."

                    evening_slots.append({
                        "phase": f"{phase_label}: {sub_name}",
                        "start": cur_time.strftime("%I:%M %p"),
                        "end": end_hw.strftime("%I:%M %p"),
                        "duration_mins": est_mins,
                        "title": title,
                        "subject": sub_name,
                        "type": "homework",
                        "badge": badge,
                        "guidance": guidance,
                        "is_completed": is_done
                    })
                    cur_time = end_hw

                # Inter-Subject Restorative Break (between different subjects)
                is_last_item = (idx == len(sorted_hw_items) - 1)
                brk_dur = lvl["break_duration"] if is_last_item else min(7, lvl["break_duration"])
                brk_end = cur_time + timedelta(minutes=brk_dur)
                brk_title = "Diary HW Clearance Break" if is_last_item else f"Rest & Reset: Post-{sub_name}"
                brk_guidance = (
                    "All school diary homework is 100% complete! Stand up, stretch, hydrate, and prepare for Daily Core Practice."
                    if is_last_item else
                    f"Great job finishing {sub_name}! Stand up, hydrate, and clear your mind before the next subject."
                )
                evening_slots.append({
                    "phase": f"{phase_label} Rest",
                    "start": cur_time.strftime("%I:%M %p"),
                    "end": brk_end.strftime("%I:%M %p"),
                    "duration_mins": brk_dur,
                    "title": brk_title,
                    "subject": "Rest & Hydrate",
                    "type": "break",
                    "badge": f"☕ Rest ({brk_dur}m)",
                    "guidance": brk_guidance,
                    "is_completed": is_done
                })
                cur_time = brk_end

        winddown_mins = 15 if current_level == 1 else 10
        study_cutoff = eve_end_time - timedelta(minutes=winddown_mins)
        available_study_mins = max(0, int((study_cutoff - cur_time).total_seconds() / 60))

        # -------------------------------------------------------------
        # PHASE 1 & 2: DYNAMIC LEVEL TIME SCALING & SUBDIVISION ROTATION
        # -------------------------------------------------------------
        # Rule 1 & 2: Homework completed above. If homework had Mathematics,
        # mandatory maths condition is satisfied.
        # Rule 3: Left-out subjects (not present in homework) get top priority for study!
        # Rule 4: Dedicated 15-minute special session for diagram practice of any subject.
        # Level 1 (Genin): 1 Core Study slot (25-30m) + 15m diagram session (ends 21:15).
        # Level 2 (Chunin) & Level 3 (Jonin): Time extends to 22:00! Remaining time is allocated
        # as an EXTRA core subject in the evening only (Core 1 + Extra Core 2).
        # Morning session remains 100% untouched and static across all levels!
        tracker = cls.get_representation_tracker()

        # Identify detected subdivisions and languages in today's homework
        hw_detected_subdivisions = set()
        hw_detected_languages = set()
        for it in study_hw_items:
            s_n = it.get("subject", "")
            t_t = it.get("task", "")
            sd = tracker.detect_subdivision(s_n, t_t)
            c_meta = CANONICAL_SUBDIVISIONS.get(sd, {})
            cat = c_meta.get("category", "")
            if cat in ["core", "science", "social"]:
                hw_detected_subdivisions.add(sd)
            elif cat == "language":
                hw_detected_languages.add(sd)

        # Core Candidates: Mathematics, Physics, Chemistry, Biology, History, Geography, Civics
        all_core_subdivisions = ["Mathematics", "Physics", "Chemistry", "Biology", "History", "Geography", "Civics"]
        absent_core_subdivisions = [c for c in all_core_subdivisions if c not in hw_detected_subdivisions]

        # Rule 2: Mandatory mathematics condition (100% daily representation)
        evening_core_1 = None
        if not hw_has_math:
            evening_core_1 = "Mathematics"
        elif absent_core_subdivisions:
            evening_core_1 = tracker.pick_balanced_candidate(absent_core_subdivisions, days=7)
        else:
            evening_core_1 = tracker.pick_balanced_candidate(all_core_subdivisions, days=7)

        scheduled_evening_subdivisions = {evening_core_1}

        # Available time for Academic Core Study (minus 15 mins for Rule 4 Diagram practice)
        diagram_mins = 15
        academic_study_mins = max(0, available_study_mins - diagram_mins)

        if current_level == 1 or academic_study_mins < 45:
            # Level 1: Exactly ONE core subject in the evening
            c1_dur = min(30, max(20, academic_study_mins))
            if c1_dur > 0:
                c1_end = cur_time + timedelta(minutes=c1_dur)
                c1_meta = CANONICAL_SUBDIVISIONS.get(evening_core_1, {})
                evening_slots.append({
                    "phase": f"{phase_label}: Core Study",
                    "start": cur_time.strftime("%I:%M %p"),
                    "end": c1_end.strftime("%I:%M %p"),
                    "duration_mins": c1_dur,
                    "title": f"Evening Core Study: {evening_core_1}",
                    "subject": c1_meta.get("parent", evening_core_1),
                    "subdivision": evening_core_1,
                    "type": "study",
                    "badge": c1_meta.get("badge", "📐 Core Study"),
                    "guidance": f"Core Concept Study ({evening_core_1}): Priority given to subject absent from homework. {c1_meta.get('guidance', '')}",
                    "is_completed": False
                })
                cur_time = c1_end

                # Restorative break between core study and diagram practice
                if lvl.get("break_duration", 0) > 0:
                    brk_c_end = cur_time + timedelta(minutes=min(5, lvl["break_duration"]))
                    evening_slots.append({
                        "phase": f"{phase_label} Rest",
                        "start": cur_time.strftime("%I:%M %p"),
                        "end": brk_c_end.strftime("%I:%M %p"),
                        "duration_mins": min(5, lvl["break_duration"]),
                        "title": "Mind Reset Interval",
                        "subject": "Posture & Water",
                        "type": "break",
                        "badge": f"☕ Rest ({min(5, lvl['break_duration'])}m)",
                        "guidance": "Rest eyes, stand up and stretch before the 15-minute diagram practice session.",
                        "is_completed": False
                    })
                    cur_time = brk_c_end

        else:
            # Level 2 & 3: Extends time! Remaining time is allocated as an EXTRA core subject in evening only!
            c1_dur = 35 if current_level == 2 else 40
            c2_dur = 30 if current_level == 2 else 35
            if c1_dur + c2_dur + 5 > academic_study_mins:
                c1_dur = max(20, (academic_study_mins - 5) // 2)
                c2_dur = max(20, (academic_study_mins - 5) - c1_dur)

            # Slot 1: Evening Core 1
            c1_end = cur_time + timedelta(minutes=c1_dur)
            c1_meta = CANONICAL_SUBDIVISIONS.get(evening_core_1, {})
            evening_slots.append({
                "phase": f"{phase_label}: Core 1 Study",
                "start": cur_time.strftime("%I:%M %p"),
                "end": c1_end.strftime("%I:%M %p"),
                "duration_mins": c1_dur,
                "title": f"Evening Core 1 Study: {evening_core_1}",
                "subject": c1_meta.get("parent", evening_core_1),
                "subdivision": evening_core_1,
                "type": "study",
                "badge": c1_meta.get("badge", "📐 Core 1"),
                "guidance": f"Core 1 Priority Concept Mastery ({evening_core_1}): {c1_meta.get('guidance', '')}",
                "is_completed": False
            })
            cur_time = c1_end

            # Micro-rest between Core 1 and Extra Core 2
            brk_inter = 5
            brk_end = cur_time + timedelta(minutes=brk_inter)
            evening_slots.append({
                "phase": f"{phase_label} Rest",
                "start": cur_time.strftime("%I:%M %p"),
                "end": brk_end.strftime("%I:%M %p"),
                "duration_mins": brk_inter,
                "title": "Inter-Core Focus Shift Break",
                "subject": "Rest",
                "type": "break",
                "badge": f"☕ Rest ({brk_inter}m)",
                "guidance": "Cognitive palette cleanser: Take 3 slow belly breaths, hydrate, and prepare for Extra Core Subject 2.",
                "is_completed": False
            })
            cur_time = brk_end

            # Pick Extra Core 2 (apart from homework AND distinct from Core 1, least represented)
            c2_candidates = [c for c in all_core_subdivisions if c not in hw_detected_subdivisions and c not in scheduled_evening_subdivisions]
            if not c2_candidates:
                c2_candidates = [c for c in all_core_subdivisions if c not in scheduled_evening_subdivisions]
            evening_core_2 = tracker.pick_balanced_candidate(c2_candidates, days=7)
            scheduled_evening_subdivisions.add(evening_core_2)

            # Slot 2: Evening Extra Core 2
            c2_end = cur_time + timedelta(minutes=c2_dur)
            c2_meta = CANONICAL_SUBDIVISIONS.get(evening_core_2, {})
            evening_slots.append({
                "phase": f"{phase_label}: Extra Core 2 Study",
                "start": cur_time.strftime("%I:%M %p"),
                "end": c2_end.strftime("%I:%M %p"),
                "duration_mins": c2_dur,
                "title": f"Evening Extra Core 2 Study: {evening_core_2} (Level {current_level} Extension)",
                "subject": c2_meta.get("parent", evening_core_2),
                "subdivision": evening_core_2,
                "type": "study",
                "badge": c2_meta.get("badge", "⚡ Extra Core 2"),
                "guidance": f"Level {current_level} Evening Extension: Extra non-homework core subject practice ({evening_core_2}). {c2_meta.get('guidance', '')}",
                "is_completed": False
            })
            cur_time = c2_end

            # Rest before diagram practice
            brk_d_end = cur_time + timedelta(minutes=5)
            evening_slots.append({
                "phase": f"{phase_label} Rest",
                "start": cur_time.strftime("%I:%M %p"),
                "end": brk_d_end.strftime("%I:%M %p"),
                "duration_mins": 5,
                "title": "Pre-Diagram Posture Reset",
                "subject": "Rest",
                "type": "break",
                "badge": "☕ Rest (5m)",
                "guidance": "Rest eyes, stand up and stretch before the 15-minute diagram practice session.",
                "is_completed": False
            })
            cur_time = brk_d_end

        # Rule 4: Inviolable 15-minute special session for diagram practice of any subject
        diagram_candidates = ["Physics", "Chemistry", "Biology", "Geography", "History", "Civics"]
        diagram_sub = tracker.pick_balanced_candidate(diagram_candidates, days=14)
        diag_meta = CANONICAL_SUBDIVISIONS.get(diagram_sub, {})
        end_draw = cur_time + timedelta(minutes=diagram_mins)
        evening_slots.append({
            "phase": f"{phase_label}: Diagram Practice",
            "start": cur_time.strftime("%I:%M %p"),
            "end": end_draw.strftime("%I:%M %p"),
            "duration_mins": diagram_mins,
            "title": f"Special 15m Session: Diagram Practice ({diagram_sub})",
            "subject": "Drawing Practice",
            "subdivision": diagram_sub,
            "type": "study",
            "badge": "🎨 Diagram Practice (15m)",
            "guidance": f"Rule 4 Inviolable Session: 15-minute special diagram & sketch practice ({diagram_sub}). Focus: {diag_meta.get('diagram_target', 'Neat sketches and labels')}.",
            "is_completed": False
        })
        cur_time = end_draw

        # Wind-down & Bag Pack
        winddown_guidance = "Pack school bag according to tomorrow's timetable. Put morning revision copy on desk."
        if bag_reminders:
            winddown_guidance += f" ⚠️ SPECIAL DIARY NOTICE: {', '.join(bag_reminders)}!"

        winddown_start = cur_time if cur_time >= study_cutoff else study_cutoff
        winddown_end = winddown_start + timedelta(minutes=winddown_mins)

        bedtime_dt = datetime.strptime("22:00", "%H:%M")
        if winddown_end < bedtime_dt:
            free_hours = round((bedtime_dt - winddown_end).total_seconds() / 3600, 1)
            winddown_guidance += f" 🎉 FINISHED EARLY AT {winddown_end.strftime('%I:%M %p')}! Earned {free_hours} hours of guilt-free relaxation, hobbies & family time before 10:00 PM bedtime!"

        evening_slots.append({
            "phase": f"{phase_label} Wind-down",
            "start": winddown_start.strftime("%I:%M %p"),
            "end": winddown_end.strftime("%I:%M %p"),
            "duration_mins": winddown_mins,
            "title": "Desk Reset, Bag Packing & Early Finish Celebration",
            "subject": "Routine Habit",
            "type": "winddown",
            "badge": "🌙 Wind-down" if cur_time.hour >= 17 else "🏆 Early Finish!",
            "guidance": winddown_guidance
        })

        # -------------------------------------------------------------
        # RULES 5, 6, 7: MORNING STUDY PLAN (STATIC & UNTOUCHED ACROSS LEVELS)
        # -------------------------------------------------------------
        # Rule 5: A second core subject which is NOT taken in the evening is present in the morning,
        # along with one language. That language has to be non-repeated (not in homework).
        # Rule 6: What evening session homework contains should NOT be repeated in the morning.
        # Rule 7: Any one of the languages can be taken. If 3 languages are in the homework itself,
        # then in the morning session do NOT concentrate on language; take TWO core subjects in morning!
        # The morning session is untouched and remains static (06:00 - 07:30) across Level 1, 2, and 3.
        # Determine active date for rotation
        if not target_date:
            for it in (diary_items or []):
                if isinstance(it, dict) and it.get("date"):
                    target_date = it.get("date")
                    break
        if not target_date:
            target_date = datetime.now().strftime("%Y-%m-%d")

        m_cur = datetime.strptime("06:00", "%H:%M")
        m_end_target = datetime.strptime("07:30", "%H:%M")

        # Slot 1: Morning Wake-Up & Hydration (06:00 AM – 06:15 AM: 15 mins)
        boot_mins = 15
        b_end = m_cur + timedelta(minutes=boot_mins)
        morning_slots.append({
            "phase": "Morning Wake-Up",
            "start": m_cur.strftime("%I:%M %p"),
            "end": b_end.strftime("%I:%M %p"),
            "duration_mins": boot_mins,
            "title": "Alertness Activation & Hydration",
            "subject": "Morning Warmup",
            "type": "prep",
            "badge": "🌅 Wake-up (15m)",
            "guidance": "Splash cool water on face, drink 1-2 glasses of warm water, gentle stretching. Zero devices."
        })
        m_cur = b_end

        # Bedtime Overrun Rollover (if any)
        if bedtime_rollovers:
            for ro in bedtime_rollovers:
                ro_dur = ro.get("truncated_mins", 15)
                ro_end = m_cur + timedelta(minutes=ro_dur)
                ro_sub = ro.get("subject", "Core Subject")
                ro_title = ro.get("title", "Evening Homework Review")
                morning_slots.append({
                    "phase": "Morning Priming Window",
                    "start": m_cur.strftime("%I:%M %p"),
                    "end": ro_end.strftime("%I:%M %p"),
                    "duration_mins": ro_dur,
                    "title": f"Morning Recall Priority: {ro_sub} ({ro_title})",
                    "subject": ro_sub,
                    "type": "rollover",
                    "is_rollover": True,
                    "badge": "🌅 Morning Recall Priority (Overrun Rollover)",
                    "guidance": f"Overrun rollover from 10:00 PM Bedtime Protection: Complete remaining {ro_dur}m high-focus review for {ro_sub} before school today!"
                })
                m_cur = ro_end

        # Select Morning Core 1: Secondary core NOT taken in evening (HW or Evening Core Study)
        all_evening_subdivisions = set(hw_detected_subdivisions) | scheduled_evening_subdivisions
        morn_core_candidates = [c for c in all_core_subdivisions if c not in all_evening_subdivisions]
        if not morn_core_candidates:
            morn_core_candidates = [c for c in all_core_subdivisions if c not in scheduled_evening_subdivisions]
        if not morn_core_candidates:
            morn_core_candidates = all_core_subdivisions

        morning_core_1 = tracker.pick_balanced_candidate(morn_core_candidates, days=7)
        mc1_meta = CANONICAL_SUBDIVISIONS.get(morning_core_1, {})

        # Slot 2: Morning Core Primer (06:15 AM – 06:45 AM: 30 mins)
        cm1_dur = 30
        cm1_end = m_cur + timedelta(minutes=cm1_dur)
        morning_slots.append({
            "phase": "Morning Core Primer",
            "start": m_cur.strftime("%I:%M %p"),
            "end": cm1_end.strftime("%I:%M %p"),
            "duration_mins": cm1_dur,
            "title": f"Morning Active Core Primer: {morning_core_1}",
            "subject": mc1_meta.get("parent", morning_core_1),
            "subdivision": morning_core_1,
            "type": "revision",
            "badge": mc1_meta.get("badge", "🌅 Core Recall"),
            "guidance": f"Rule 5 & 6 Non-Repeated Core ({morning_core_1}) Active Primer: Review key formulas, definitions, and mental proofs before writing today's exam.",
            "is_completed": False
        })
        m_cur = cm1_end

        # Slot 3: DEDICATED 6:45 AM HOST EXAM SLOT (06:45 AM – 07:05 AM: 20 mins)
        exam_subj, rot_reason, is_sun = DailyExamSubjectRotator.pick_morning_exam_subject(target_date, diary_items)
        exam_dur = 20
        e_end = m_cur + timedelta(minutes=exam_dur)

        if is_sun:
            morning_slots.append({
                "phase": "Sunday Master Exam Window",
                "start": "FLEXIBLE",
                "end": "ON-DEMAND",
                "duration_mins": 60,
                "title": "🌟 Sunday Master Exam: Flexible On-Demand Window (Exempt from 6:45 AM Alarm)",
                "subject": "🌟 Sunday Master Exam",
                "type": "study",
                "badge": "🌟 Sunday Master Exam",
                "guidance": "Today is Sunday! You are exempt from the 6:45 AM alarm. Take your weekly cumulative master exam at any comfortable time today.",
                "is_completed": False
            })
        else:
            morning_slots.append({
                "phase": "Morning Host Exam Window",
                "start": m_cur.strftime("%I:%M %p"),
                "end": e_end.strftime("%I:%M %p"),
                "duration_mins": exam_dur,
                "title": f"🎯 6:45 AM Host Exam: Daily Recall & Step Solving ({exam_subj})",
                "subject": f"🎯 Host Exam: {exam_subj}",
                "type": "study",
                "badge": f"🎯 6:45 AM Exam ({exam_subj})",
                "guidance": f"Strict 20-min Morning Host Exam on {exam_subj}. 100% blind solving on unlined paper. Show all derivation steps, box final numeric values, and write SI units. [Rotation Source: {rot_reason}]",
                "is_completed": False
            })
        m_cur = e_end

        # Slot 4: Post-Exam Break & Hydration Reset (07:05 AM – 07:10 AM: 5 mins)
        brk_dur = 5
        b_end2 = m_cur + timedelta(minutes=brk_dur)
        morning_slots.append({
            "phase": "Morning Rest",
            "start": m_cur.strftime("%I:%M %p"),
            "end": b_end2.strftime("%I:%M %p"),
            "duration_mins": brk_dur,
            "title": "Post-Exam Respite & Breath Reset",
            "subject": "Rest",
            "type": "break",
            "badge": "☕ Break (5m)",
            "guidance": "Stand up, stretch your back, take 5 slow deep breaths, take a sip of water."
        })
        m_cur = b_end2

        # Slot 5: Morning Language Clinic & Error Bank Drill (07:10 AM – 07:25 AM: 15 mins)
        hw_all_3_langs = (len(hw_detected_languages) >= 3 or ("Tamil" in hw_detected_languages and "English" in hw_detected_languages and "Hindi" in hw_detected_languages))
        if hw_all_3_langs:
            morn_core_candidates_2 = [c for c in morn_core_candidates if c != morning_core_1]
            if not morn_core_candidates_2:
                morn_core_candidates_2 = [c for c in all_core_subdivisions if c != morning_core_1 and c not in scheduled_evening_subdivisions]
            if not morn_core_candidates_2:
                morn_core_candidates_2 = [c for c in all_core_subdivisions if c != morning_core_1]
            morning_core_2 = tracker.pick_balanced_candidate(morn_core_candidates_2, days=7)
            mc2_meta = CANONICAL_SUBDIVISIONS.get(morning_core_2, {})
            lang_dur = 15
            lang_end = m_cur + timedelta(minutes=lang_dur)
            morning_slots.append({
                "phase": "Morning Core 2 Recall",
                "start": m_cur.strftime("%I:%M %p"),
                "end": lang_end.strftime("%I:%M %p"),
                "duration_mins": lang_dur,
                "title": f"Morning Core 2 Recall: {morning_core_2} (3-Lang HW Override)",
                "subject": mc2_meta.get("parent", morning_core_2),
                "subdivision": morning_core_2,
                "type": "revision",
                "badge": mc2_meta.get("badge", "🌅 Core 2 Recall"),
                "guidance": f"Rule 7 Active: 3 languages were already in homework. Second core {morning_core_2} takes 15m review focus!",
                "is_completed": False
            })
            m_cur = lang_end
        else:
            all_langs = ["Tamil", "English", "Hindi"]
            candidate_langs = [l for l in all_langs if l not in hw_detected_languages]
            if not candidate_langs:
                candidate_langs = all_langs

            chosen_lang = candidate_langs[0]
            for cl in candidate_langs:
                if cl.lower() in selected_language.lower():
                    chosen_lang = cl
                    break
            else:
                chosen_lang = tracker.pick_balanced_candidate(candidate_langs, days=7)

            l_meta = CANONICAL_SUBDIVISIONS.get(chosen_lang, {})
            lang_dur = 15
            lang_end = m_cur + timedelta(minutes=lang_dur)
            morning_slots.append({
                "phase": "Morning Language Clinic",
                "start": m_cur.strftime("%I:%M %p"),
                "end": lang_end.strftime("%I:%M %p"),
                "duration_mins": lang_dur,
                "title": f"Language Error Bank & Clinic: {chosen_lang} (Non-Repeated)",
                "subject": chosen_lang,
                "subdivision": chosen_lang,
                "type": "revision",
                "badge": l_meta.get("badge", "✍️ Language Clinic"),
                "guidance": f"Rule 5 & 7 Non-Repeated Language Clinic ({chosen_lang}): Write 5 high-risk words from Error Bank copy. Review 3 key definitions and check handwriting layout.",
                "is_completed": False
            })
            m_cur = lang_end

        # Slot 6: School Readiness Wind-down (07:25 AM – 07:30 AM: 5 mins)
        morning_slots.append({
            "phase": "School Ready",
            "start": m_cur.strftime("%I:%M %p"),
            "end": m_end_target.strftime("%I:%M %p"),
            "duration_mins": max(5, int((m_end_target - m_cur).total_seconds() / 60)),
            "title": "School Readiness Audit & Confidence Boost",
            "subject": "Ready for School",
            "type": "winddown",
            "badge": "🎒 School Ready (5m)",
            "guidance": "Pack evaluated morning test sheet into study binder. Double check stationery pouch, diary, homework copies, and water bottle. Depart for Senthil Public School with high energy and confidence!"
        })

        return evening_slots, morning_slots

    @classmethod
    def _generate_exam_sprint_schedule(cls, subjects, pending_items, exam_subject, lvl, start_time_str="19:00"):
        evening_slots = []
        morning_slots = []

        try:
            cur_time = datetime.strptime(start_time_str, "%H:%M")
        except Exception:
            cur_time = datetime.strptime("19:00", "%H:%M")

        exam_guidance = cls._get_exam_guidance(exam_subject)

        hw_exam = [it for it in pending_items if exam_subject.lower() in it.get("subject", "").lower() and it.get("task_type") != "bag_pack"]
        hw_other = [it for it in pending_items if exam_subject.lower() not in it.get("subject", "").lower() and it.get("task_type") != "bag_pack"]
        bag_reminders = [it["task"] for it in pending_items if it.get("task_type") == "bag_pack"]

        # Phase descriptor
        if cur_time.hour < 12:
            phase_prefix = "Holiday Morning Exam Sprint"
        elif cur_time.hour < 17:
            phase_prefix = "Afternoon Exam Sprint"
        else:
            phase_prefix = "Evening Exam Sprint"

        # If there are other non-exam homework items, give a quick clearance slot
        if hw_other:
            dur_hw = min(30, sum(it.get("est_mins", 15) for it in hw_other))
            end_hw = cur_time + timedelta(minutes=dur_hw)
            other_subs = ", ".join(list(dict.fromkeys(it["subject"] for it in hw_other)))
            evening_slots.append({
                "phase": f"{phase_prefix}: Pre-Flight Clearance",
                "start": cur_time.strftime("%I:%M %p"),
                "end": end_hw.strftime("%I:%M %p"),
                "duration_mins": dur_hw,
                "title": f"Pre-Exam HW Clearance: {other_subs}",
                "subject": other_subs,
                "type": "homework",
                "badge": "⚡ Quick Clearance",
                "guidance": "Quickly clear non-exam school diary items so your focus tonight is 100% dedicated to tonight's exam subject!"
            })
            cur_time = end_hw
            brk_end = cur_time + timedelta(minutes=5)
            evening_slots.append({
                "phase": f"{phase_prefix} Rest",
                "start": cur_time.strftime("%I:%M %p"),
                "end": brk_end.strftime("%I:%M %p"),
                "duration_mins": 5,
                "title": "Exam Focus Transition Break",
                "subject": "Clear Desk",
                "type": "break",
                "badge": "☕ Rest (5m)",
                "guidance": "Clear all unrelated books off the desk. Keep only textbook, rough copy, and pen for tonight's exam!"
            })
            cur_time = brk_end

        # Stage 1: High-Weight Concept Mastery & Active Hand-Solving (50 mins)
        stage1_dur = 50
        s1_end = cur_time + timedelta(minutes=stage1_dur)
        hw_sub_task = f" (Includes diary task: {hw_exam[0]['task']})" if hw_exam else ""
        evening_slots.append({
            "phase": f"{phase_prefix}: Stage 1",
            "start": cur_time.strftime("%I:%M %p"),
            "end": s1_end.strftime("%I:%M %p"),
            "duration_mins": stage1_dur,
            "title": f"Stage 1: High-Weight Concept Mastery & Solving: {exam_subject}",
            "subject": exam_subject,
            "type": "study",
            "badge": "🔥 Stage 1: Deep Solving",
            "guidance": f"{exam_guidance['stage1']}{hw_sub_task}"
        })
        cur_time = s1_end

        # Rest Break 1 (10 mins)
        brk1_end = cur_time + timedelta(minutes=10)
        evening_slots.append({
            "phase": f"{phase_prefix} Rest",
            "start": cur_time.strftime("%I:%M %p"),
            "end": brk1_end.strftime("%I:%M %p"),
            "duration_mins": 10,
            "title": "Post-Solving Cognitive Reset Break",
            "subject": "Rest & Eye Palming",
            "type": "break",
            "badge": "☕ Rest (10m)",
            "guidance": "Step away from the desk! Palming exercise for eyes: rub palms together, place gently over closed eyes. Drink water."
        })
        cur_time = brk1_end

        # Stage 2: Active Recall & The 'Blind Test' Protocol (50 mins)
        stage2_dur = 50
        s2_end = cur_time + timedelta(minutes=stage2_dur)
        evening_slots.append({
            "phase": f"{phase_prefix}: Stage 2",
            "start": cur_time.strftime("%I:%M %p"),
            "end": s2_end.strftime("%I:%M %p"),
            "duration_mins": stage2_dur,
            "title": f"Stage 2: Active Recall & Blind Test: {exam_subject}",
            "subject": exam_subject,
            "type": "study",
            "badge": "🧠 Stage 2: Blind Recall",
            "guidance": exam_guidance["stage2"]
        })
        cur_time = s2_end

        # Rest Break 2 (10 mins)
        brk2_end = cur_time + timedelta(minutes=10)
        evening_slots.append({
            "phase": f"{phase_prefix} Rest",
            "start": cur_time.strftime("%I:%M %p"),
            "end": brk2_end.strftime("%I:%M %p"),
            "duration_mins": 10,
            "title": "Pre-Drill Oxygen Recharge Break",
            "subject": "Movement & Posture",
            "type": "break",
            "badge": "☕ Rest (10m)",
            "guidance": "Stretch your shoulders and spine. Take 5 slow diaphragmatic breaths. Brain is ready for final rapid review!"
        })
        cur_time = brk2_end

        # Stage 3: Rapid-Fire Question Bank & Formula Drill (35 mins)
        stage3_dur = 35
        s3_end = cur_time + timedelta(minutes=stage3_dur)
        evening_slots.append({
            "phase": f"{phase_prefix}: Stage 3",
            "start": cur_time.strftime("%I:%M %p"),
            "end": s3_end.strftime("%I:%M %p"),
            "duration_mins": stage3_dur,
            "title": f"Stage 3: Rapid Question Drill & Glossary: {exam_subject}",
            "subject": exam_subject,
            "type": "study",
            "badge": "⚡ Stage 3: Speed Drill",
            "guidance": exam_guidance["stage3"]
        })
        cur_time = s3_end

        # Stage 4: Exam Kit Audit & Sleep Transition (15 mins)
        s4_end = cur_time + timedelta(minutes=15)
        bag_txt = f" • SPECIAL REMINDER: {', '.join(bag_reminders)}" if bag_reminders else ""
        bedtime_dt = datetime.strptime("22:00", "%H:%M")
        leisure_txt = ""
        if s4_end < bedtime_dt:
            free_h = round((bedtime_dt - s4_end).total_seconds() / 3600, 1)
            leisure_txt = f" 🎉 EXAM PREPARATION COMPLETE AT {s4_end.strftime('%I:%M %p')}! Earned {free_h} hours of guilt-free relaxation and family time before 10:00 PM bedtime. Sleep locks memory in!"

        evening_slots.append({
            "phase": f"{phase_prefix}: Exam Readiness",
            "start": cur_time.strftime("%I:%M %p"),
            "end": s4_end.strftime("%I:%M %p"),
            "duration_mins": 15,
            "title": "Exam Hall Kit Audit & Rest Transition",
            "subject": "Exam Kit Check",
            "type": "prep",
            "badge": "🎒 Kit Audit",
            "guidance": f"Pack Exam Hall Kit: Hall ticket / ID card, 2 working pens, sharpened pencil, eraser, long scale, geometry box{bag_txt}. Desk cleared with morning formula sheet ready.{leisure_txt} Bedtime at 10:00 PM is INVIOLABLE (sleep locks memory in!)."
        })

        # -------------------------------------------------------------
        # MORNING EXAM SPRINT RESERVED WINDOW (6:40 AM – 7:45 AM)
        # -------------------------------------------------------------
        morning_slots.append({
            "phase": "Phase 3 Morning Exam Sprint",
            "start": "06:40 AM",
            "end": "07:45 AM",
            "duration_mins": 65,
            "title": f"⚡ RESERVED FOR HOST EXAM: MORNING SPRINT ({exam_subject.upper()})",
            "subject": f"⚡ Host Exam: {exam_subject}",
            "type": "study",
            "badge": f"⚡ Sprint ({exam_subject})",
            "guidance": f"Reserved Morning Exam Session (06:40 AM – 07:45 AM). Rapid warm-up sprint before school exam: 20-25 Marks. 45 mins writing + 10 mins verification + 5 mins submission. Activates peak exam focus before walking into school hall!",
            "is_completed": False
        })

        morning_slots.append({
            "phase": "Morning Dispatch",
            "start": "07:45 AM",
            "end": "08:00 AM",
            "duration_mins": 15,
            "title": "Exam Kit Final Audit, Breakfast & School Departure",
            "subject": "School Ready",
            "type": "prep",
            "badge": "🏆 School Departure",
            "guidance": "Final check of Exam Hall Kit (pens, geometry box, hall ticket). Wholesome breakfast. Affirmation: 'I am prepared and calm!' Depart for school examination hall with supreme confidence!",
            "is_completed": False
        })

        return evening_slots, morning_slots

    @classmethod
    def _generate_pre_exam_prep_schedule(cls, subjects, day_num=1, current_level=2, start_time_str="19:00", duration_days=21):
        roadmap = build_dynamic_pre_exam_roadmap(duration_days)
        day_idx = max(0, min(len(roadmap) - 1, day_num - 1))
        day_data = roadmap[day_idx]
        lvl = EXECUTION_LEVELS.get(current_level, EXECUTION_LEVELS[2])

        evening_slots = []
        morning_slots = []

        try:
            cur_time = datetime.strptime(start_time_str, "%H:%M")
        except Exception:
            cur_time = datetime.strptime("19:00", "%H:%M")

        phase_prefix = f"Pre-Exam Day {day_data['day']}"

        # Slot 1: Core Subject High-Weight Concept & Problem Solving (45 mins)
        s1_end = cur_time + timedelta(minutes=45)
        evening_slots.append({
            "phase": f"{phase_prefix}: Core Focus",
            "start": cur_time.strftime("%I:%M %p"),
            "end": s1_end.strftime("%I:%M %p"),
            "duration_mins": 45,
            "title": f"Block 1: {day_data['focus_core']} ({day_data['core_topic']})",
            "subject": day_data["focus_core"],
            "type": "study",
            "badge": "🔥 Core Mastery (45m)",
            "guidance": f"Core Focus: {day_data['guidance_core']} Focus on active pen-on-paper working and concept clarity."
        })
        cur_time = s1_end

        # Break 1 (10 mins)
        b1_end = cur_time + timedelta(minutes=10)
        evening_slots.append({
            "phase": f"{phase_prefix} Rest",
            "start": cur_time.strftime("%I:%M %p"),
            "end": b1_end.strftime("%I:%M %p"),
            "duration_mins": 10,
            "title": "Movement & Oxygen Recharge Break",
            "subject": "Physical Reset",
            "type": "break",
            "badge": "☕ Rest (10m)",
            "guidance": "Step away from study desk! Rub palms over eyes (eye palming), drink water, stretch shoulders and spine."
        })
        cur_time = b1_end

        # Slot 2: Language / Humanities / Concept Retention (45 mins)
        s2_end = cur_time + timedelta(minutes=45)
        evening_slots.append({
            "phase": f"{phase_prefix}: Second Subject",
            "start": cur_time.strftime("%I:%M %p"),
            "end": s2_end.strftime("%I:%M %p"),
            "duration_mins": 45,
            "title": f"Block 2: {day_data['focus_second']} ({day_data['second_topic']})",
            "subject": day_data["focus_second"],
            "type": "study",
            "badge": "📖 Second Focus (45m)",
            "guidance": f"Secondary Subject Focus: {day_data['guidance_second']} Self-writing, textbook reading, and error reduction."
        })
        cur_time = s2_end

        # Break 2 (10 mins)
        b2_end = cur_time + timedelta(minutes=10)
        evening_slots.append({
            "phase": f"{phase_prefix} Rest",
            "start": cur_time.strftime("%I:%M %p"),
            "end": b2_end.strftime("%I:%M %p"),
            "duration_mins": 10,
            "title": "Hydration & Cognitive Consolidation Break",
            "subject": "Hydrate & Relax",
            "type": "break",
            "badge": "☕ Rest (10m)",
            "guidance": "Drink water. Light breathing. Let the learned material consolidate in your working memory."
        })
        cur_time = b2_end

        # Slot 3: Active Recall, Blind Retrieval & Question Practice (35 mins)
        s3_end = cur_time + timedelta(minutes=35)
        evening_slots.append({
            "phase": f"{phase_prefix}: Active Recall",
            "start": cur_time.strftime("%I:%M %p"),
            "end": s3_end.strftime("%I:%M %p"),
            "duration_mins": 35,
            "title": f"Block 3: Active Retrieval & Exercise Practice ({day_data['title']})",
            "subject": f"{day_data['focus_core']} & {day_data['focus_second']}",
            "type": "study",
            "badge": "🧠 Active Retrieval (35m)",
            "guidance": "Close the book! Redraw diagrams or write key formula steps on blank rough paper. Solve 3 textbook exercise questions from memory."
        })
        cur_time = s3_end

        # Special 15-Minute Dedicated Drawing Practice Slot
        draw_dur = 15
        end_draw = cur_time + timedelta(minutes=draw_dur)
        evening_slots.append({
            "phase": f"{phase_prefix}: Drawing & Art",
            "start": cur_time.strftime("%I:%M %p"),
            "end": end_draw.strftime("%I:%M %p"),
            "duration_mins": draw_dur,
            "title": "Special Drawing Practice: Science Diagrams & Visual Recall",
            "subject": "Drawing Practice",
            "type": "study",
            "badge": "🎨 Drawing (15m)",
            "guidance": (
                "Special Drawing Practice (15m): Dedicated sketching & drawing block. Practice neat pencil line work, scientific diagrams (e.g. eye, ray diagrams, cells), map sketching, or freeform artistic drawing to relax and sharpen fine-motor precision."
            ),
            "is_completed": False
        })
        cur_time = end_draw

        # Slot 4: Portion Tracker Update, Desk Audit & Sleep Lock (15 mins)
        s4_end = cur_time + timedelta(minutes=15)
        bedtime_dt = datetime.strptime("22:00", "%H:%M")
        leisure_txt = ""
        if s4_end < bedtime_dt:
            free_h = round((bedtime_dt - s4_end).total_seconds() / 3600, 1)
            leisure_txt = f" 🎉 PRE-EXAM PREPARATION COMPLETE AT {s4_end.strftime('%I:%M %p')}! Earned {free_h} hours of free relaxation before 10:00 PM bedtime."

        evening_slots.append({
            "phase": f"{phase_prefix}: Wrap-Up",
            "start": cur_time.strftime("%I:%M %p"),
            "end": s4_end.strftime("%I:%M %p"),
            "duration_mins": 15,
            "title": "Portion Tracker Check & 10:00 PM Sleep Lock",
            "subject": "Tracker Audit",
            "type": "prep",
            "badge": "🎒 Tracker Audit",
            "guidance": f"Tick off completed chapters in the 'Exam Portions & Tracker' tab. Pack school bag.{leisure_txt} Inviolable 10:00 PM sleep (locks neural pathways!)."
        })

        # Check if today is a 4th Day Morning Checkpoint Exam Day
        # Checkpoint blocks: Days 1-3 -> Exam on Day 4 Morning
        #                    Days 4-6 -> Exam on Day 7 Morning
        #                    Days 7-9 -> Exam on Day 10 Morning
        #                    Days 10-12 -> Exam on Day 13 Morning
        #                    Days 13-15 -> Exam on Day 16 Morning
        #                    Days 16-18 -> Exam on Day 19 Morning
        #                    Days 19-21 -> Exam on Day 22 Morning
        is_checkpoint_exam_day = (day_num > 1 and (day_num - 1) % 3 == 0)
        if is_checkpoint_exam_day:
            prev_start = day_num - 3
            prev_end = day_num - 1
            morning_slots.append({
                "phase": "Morning Active Priming",
                "start": "06:15 AM",
                "end": "06:45 AM",
                "duration_mins": 30,
                "title": f"Morning Checkpoint Primer: Days {prev_start}–{prev_end} Formulas",
                "subject": "Checkpoint Primer",
                "type": "prep",
                "badge": "🌅 Priming (30m)",
                "guidance": "Final mental scan of formulas, laws, and diagram blueprints before writing today's 3-day Checkpoint Exam."
            })
            morning_slots.append({
                "phase": "Phase 2 Checkpoint Exam Window",
                "start": "06:45 AM",
                "end": "07:45 AM",
                "duration_mins": 60,
                "title": f"🎯 RESERVED FOR HOST EXAM: 3-DAY CHECKPOINT (DAYS {prev_start}–{prev_end} AUDIT)",
                "subject": "🎯 Host Exam: Checkpoint",
                "type": "study",
                "badge": f"📝 25M Checkpoint (60m)",
                "guidance": f"Reserved Morning Exam Session (06:45 AM – 07:45 AM). Strict 25-Mark Checkpoint Exam testing subjects studied across Days {prev_start} to {prev_end}. 45 mins writing + 10 mins verification + 5 mins submission. Box final answers and write SI units!",
                "is_completed": False
            })
            morning_slots.append({
                "phase": "Morning Dispatch",
                "start": "07:45 AM",
                "end": "08:00 AM",
                "duration_mins": 15,
                "title": "Breakfast & School Departure",
                "subject": "School Ready",
                "type": "prep",
                "badge": "🏆 School Departure",
                "guidance": "Nutritious breakfast. Pack evaluated test sheet in study binder. Depart for Senthil Public School with high energy and confidence!",
                "is_completed": False
            })
        else:
            morning_slots.append({
                "phase": "Morning Priming Window",
                "start": "06:15 AM",
                "end": "06:45 AM",
                "duration_mins": 30,
                "title": f"Morning Active Priming: {day_data['title']}",
                "subject": day_data["focus_core"],
                "type": "study",
                "badge": "🌅 Priming Window",
                "guidance": f"Morning Recall: {day_data['morning_task']} Zero new reading! Only verify flashcards, formulas, and redraw diagrams."
            })
            morning_slots.append({
                "phase": "Morning Host Exam Window",
                "start": "06:45 AM",
                "end": "07:05 AM",
                "duration_mins": 20,
                "title": f"🎯 6:45 AM Host Exam: Pre-Exam Step Solving ({day_data['focus_core']})",
                "subject": f"🎯 Host Exam: {day_data['focus_core']}",
                "type": "study",
                "badge": f"🎯 6:45 AM Exam ({day_data['focus_core']})",
                "guidance": "Strict 20-min Morning Host Exam. 100% blind solving on unlined paper. Show all steps, box final numeric values, and write SI units.",
                "is_completed": False
            })
            morning_slots.append({
                "phase": "Morning Post-Exam Break",
                "start": "07:05 AM",
                "end": "07:10 AM",
                "duration_mins": 5,
                "title": "Post-Exam Respite & Breath Reset",
                "subject": "Rest",
                "type": "break",
                "badge": "☕ Break (5m)",
                "guidance": "Stand up, stretch your back, take 5 slow deep breaths, take a sip of water."
            })
            morning_slots.append({
                "phase": "Morning Language Clinic",
                "start": "07:10 AM",
                "end": "07:25 AM",
                "duration_mins": 15,
                "title": f"Language Error Bank & Recall: {day_data['focus_second']}",
                "subject": day_data["focus_second"],
                "type": "study",
                "badge": "⚡ Error Bank Clinic",
                "guidance": f"Write 5 high-risk words from Error Bank copy ({day_data['focus_second']}). Review 3 key definitions."
            })
            morning_slots.append({
                "phase": "Morning Dispatch",
                "start": "07:25 AM",
                "end": "07:30 AM",
                "duration_mins": 5,
                "title": "Daily Shinobi Mindset & School Departure",
                "subject": "Positive Mindset",
                "type": "prep",
                "badge": "🏆 Confident Dispatch",
                "guidance": "Final bag check: Diary, books, stationery. Nutritious breakfast. Depart for school with confidence!"
            })

        return evening_slots, morning_slots

    @classmethod
    def _get_exam_guidance(cls, subject_name):
        sub_lower = subject_name.lower()
        if "tamil" in sub_lower:
            return {
                "stage1": "செய்யுள் & உரைநடை வினா-விடை: இயல் 1, 2, 3 உரைநடை வினாக்களுக்குச் சொந்த நடையில் பிழையின்றி விடையளித்துப் பழகு (நிலம் பொது, தமிழர் மருத்துவம், தமிழ் வரிவடிவ வளர்ச்சி).",
                "stage2": "திருக்குறள் (1-10) மனப்பாடப் பகுதி: மனப்பாடப் பகுதி திருக்குறள் 1 முதல் 10 வரை முழுமையாகப் பார்க்காமல் எழுதி, சீர் மற்றும் அசை அமைப்பைச் சரிபார்!",
                "stage3": "இலக்கணம் & பொதுப்பகுதி: எழுத்துகளின் பிறப்பு, வினைமுற்று, எச்சம், யாப்பு இலக்கணம் விதிகள் மற்றும் கடிதம்/கட்டுரை படிவங்களை மீள்பார்வை செய்.",
                "morning1": "திருக்குறள் 1-10 நினைவூட்டல்: கடினமான சொற்கள் (ழ, ள, ல, ண, ந, ன) பிழை திருத்த நோட்டுப் புத்தகம் வழி சரிபார்த்தல்.",
                "morning2": "அமைதியான வாசிப்பு & கையெழுத்து விழிப்புணர்வு: வினாத்தாளை முழுமையாக 5 நிமிடம் வாசித்தல், தலைப்புகள் இட்டுத் தெளிவாக எழுதுதல்."
            }
        elif "math" in sub_lower:
            return {
                "stage1": "High-Weight Chapter Solving (Ch 6 Sets, Ch 7 Functions, Ch 8 Matrices): Solve 8-10 textbook problems by hand on paper. Verify Set Venn diagrams, matrix dimensions, and function mappings!",
                "stage2": "Timed 5-Sum Sprint (Ch 1 Rational, Ch 2 Squares/Cubes, Ch 3 Ratio): Solve 5 problems without looking at solutions. Long division square roots, cube estimation, and proportion steps.",
                "stage3": "Understanding Shapes & Data Handling (Ch 4 & 5): Angle sum properties, polygon formulas, bar graphs/pie charts reading, and formula sheet revision.",
                "morning1": "Formula & Identity Priming: Write down all formulas (Set laws, matrix addition rules, powers/roots, shape interior angle formulas) from memory on blank paper.",
                "morning2": "Calm Mental Warm-up: Check 3 basic calculation checks. Avoid rushing. Double check calculations during exam."
            }
        elif "phy" in sub_lower:
            return {
                "stage1": "Physics Ray Diagrams & Chemistry Models: Practice 6 convex lens ray diagrams (Ln-2 Lenses) and Snell's law. Draw Bohr-Rutherford atomic structures (K,L,M,N shells). Apply P-E-E-D answering: Subheading ➔ Keyword in own words ➔ Formula/Ray sketch box.",
                "stage2": "Active Recall Blurting Sprint: Close book! Blurt definitions of refractive index, focal length, electrostatic induction, and periodic trends onto rough paper. Check missing keywords with red pencil.",
                "stage3": "SI Units, Definitions & 1-Mark Quick Fire: Definitions of refractive index, focal length, electrostatic force, isotopes/isobars, and textbook chapter-end questions.",
                "morning1": "Visual Diagram Priming: Quick review of lens ray diagrams and atomic shells configuration (K, L, M, N). Zero new reading!",
                "morning2": "SI Units & Laws Rapid Recall: Review Snell's law, lens formula conventions, and charge conservation."
            }
        elif "bio" in sub_lower:
            return {
                "stage1": "Blind Diagram Protocol (High Diagram Weight!): Draw and label strictly from memory: Human Heart (4 chambers, valves Ln-1), Neuron & Reflex Arc (Ln-3), Plant Xylem/Phloem bundle (Ln-2). Practice neat unilateral labeling.",
                "stage2": "Function-Structure Pairing & P-E-E-D Answering: Pair structure with function (Valves ➔ prevent backflow; Xylem ➔ water transport). Frame 5-mark answers with Subheadings ➔ Own words with keywords ➔ Labeled diagram box.",
                "stage3": "Key Biological Terms & Differences Table: Arteries vs Veins, Xylem vs Phloem, Sensory vs Motor neurons, Asexual vs Sexual reproduction (3-column comparison tables).",
                "morning1": "Visual Diagram Priming: Rapid visual scan of the 4 key diagrams (Heart, Brain/Neuron, Plant Stem section, Flower/Reproductive system).",
                "morning2": "Terminology Rapid Fire: Review scientific terms, definitions, and functions of organs."
            }
        elif "social" in sub_lower or "sst" in sub_lower:
            return {
                "stage1": "5-Mark Historical & Civics P-E-E-D Answers: Frame 1857 Revolt causes and Constitution features using P-E-E-D: Point (Bold Subheading) ➔ Explanation in own words with textbook keywords ➔ Evidence (dates/names) ➔ Flow-Tree box!",
                "stage2": "Cause-Event-Consequence Trees & Map Pinning: Draw 3-box vertical flowcharts (Causes ➔ Outbreak ➔ Consequences). Mark 1857 revolt centers (Meerut, Delhi, Kanpur, Jhansi) with colored dots on outline map.",
                "stage3": "Timelines, Key Dates & Objective Drill: Rapid review of historical timeline milestones, constitutional terms, and 1-mark fill in the blanks / MCQs.",
                "morning1": "Map Pointing & Timeline Flash Review: 5-minute visual scan of India map centers and revolt dates.",
                "morning2": "Structured Point Strategy: Plan subheadings and bullet points for 5-mark long answers."
            }
        elif "hindi" in sub_lower:
            return {
                "stage1": "Lessons 1, 2, 3, 4, 7 & Meaning/Question Bank: Pariksha, Himalaya ke ped, Jal Chakra, Mann me hai vishwas question-answers and word meanings.",
                "stage2": "General Writing & Language Lab: Practice Vigyapan Lekhan (Advertisement), Chitra Varnan (Picture description), Paragraph, and Spoken Sentences 1-25.",
                "stage3": "Error Bank & Matra Clinic: Test 20 tricky Hindi matras (इ/ई, उ/ऊ, अनुस्वार/अनुनासिक) by hand. Classwork question bank review.",
                "morning1": "Language Lab & Spoken 1-25 Sentences: Rapid scan of introduction sentences, greetings, and lab phrases.",
                "morning2": "Format Review: Neat layout for Advertisement box and Picture description paragraph."
            }
        elif "english" in sub_lower or "eng" in sub_lower:
            return {
                "stage1": "Literature Long Questions & Themes: 6 chapters (Tales of Historic Delhi, Entertainment, The Letter A, Frosty, Kitemaker, The Value). Write character sketches and moral themes in own words.",
                "stage2": "Formal Writing Formats: Practice 1 Formal Letter / Informal Letter, 1 Article, and 1 Story Writing with correct headings, salutations, and neat paragraph breaks.",
                "stage3": "Grammar Master Sprint (8 Chapters): Parts of speech, Countable/Uncountable, Articles, Present/Past/Future tenses, Infinitives/Gerunds/Participles, and Modals exercises.",
                "morning1": "Grammar Rules & Writing Formats Scan: Review letter layout, article title rules, and modal verbs usage.",
                "morning2": "Proofreading Strategy: Leave 10 minutes at the end of the exam to check tense consistency and punctuation."
            }
        else:
            return {
                "stage1": "High-Weight Concept Mastery: Hand-solve problems and write structured answers in own words.",
                "stage2": "Active Recall & Blind Test: Test key diagrams, definitions, and formulas strictly from memory.",
                "stage3": "Rapid-Fire Drill: Review definitions, units, and glossary bullet points.",
                "morning1": "Visual & Formula Priming: Quick scan of summary flashcards and error notes.",
                "morning2": "Calm Mindset: Breathe deeply. Double check each answer before submission."
            }

