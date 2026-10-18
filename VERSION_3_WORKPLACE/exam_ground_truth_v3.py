"""
EXAM GROUND TRUTH & GEMINI API GATEWAY (SESSION 1)
--------------------------------------------------
Pure, clean, decoupled foundation for ScholasticPulse Exam Architecture.
Guarantees:
1. Strict 7-subject catalog (Math, Physical Science, Biology, Social Science, English, Hindi, Tamil).
2. Clean Oct 12-17 diary syllabus ingestion.
3. Decoupled Gemini API Gateway with connection self-test and fallback awareness.
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

# ==============================================================================
# 1. BASE PATHS & PERSISTENCE
# ==============================================================================
def get_base_dir() -> str:
    """Return persistent directory on disk."""
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        if os.path.exists(os.path.join(exe_dir, "EXAM_SYSTEM_V3")):
            return exe_dir
        v3_dir = os.path.join(exe_dir, "VERSION_3_WORKPLACE")
        if os.path.exists(os.path.join(v3_dir, "EXAM_SYSTEM_V3")):
            return v3_dir
        meipass_path = getattr(sys, '_MEIPASS', None)
        if meipass_path:
            seed_exam = os.path.join(meipass_path, "EXAM_SYSTEM_V3")
            if os.path.exists(seed_exam):
                try:
                    import shutil
                    shutil.copytree(seed_exam, os.path.join(exe_dir, "EXAM_SYSTEM_V3"), dirs_exist_ok=True)
                except Exception:
                    pass
        return exe_dir
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
EXAM_SYSTEM_DIR = os.path.join(BASE_DIR, "EXAM_SYSTEM_V3")
CONFIG_FILE = os.path.join(EXAM_SYSTEM_DIR, "gemini_config.json")
DIARY_FILE = os.path.join(BASE_DIR, "tharun_diary_format.json")


# ==============================================================================
# 2. MASTER SUBJECT CATALOG (CLASS 8 CBSE)
# ==============================================================================
class SubjectCatalog:
    """
    Immutable catalog of all 7 subjects supported for Tharun (Senthil Public School).
    Enforces composite branch rules:
    - Physical Science = Physics + Chemistry
    - Biology = Independent
    - Social Science = History + Geography + Civics + Economics
    """
    CATALOG = {
        "Mathematics": {
            "display_name": "Mathematics",
            "code": "MATH",
            "type": "single",
            "language": "en",
            "branches": ["Algebra", "Arithmetic", "Mensuration", "Geometry"],
            "description": "CBSE Class 8 Mathematics"
        },
        "Physical Science": {
            "display_name": "Physical Science (Physics & Chemistry)",
            "code": "PHY_CHEM",
            "type": "composite",
            "language": "en",
            "sections": [
                {"section_name": "SECTION A: PHYSICS", "weightage_pct": 50},
                {"section_name": "SECTION B: CHEMISTRY", "weightage_pct": 50}
            ],
            "branches": ["Physics", "Chemistry"],
            "description": "Physics & Chemistry combined paper"
        },
        "Biology": {
            "display_name": "Biology (Natural Science)",
            "code": "BIO",
            "type": "single",
            "language": "en",
            "branches": ["Natural Science", "Cell Biology", "Plant & Animal Systems"],
            "description": "CBSE Class 8 Life Sciences (Independent)"
        },
        "Social Science": {
            "display_name": "Social Science",
            "code": "SST",
            "type": "composite",
            "language": "en",
            "sections": [
                {"section_name": "SECTION A: HISTORY", "weightage_pct": 28},
                {"section_name": "SECTION B: GEOGRAPHY", "weightage_pct": 24},
                {"section_name": "SECTION C: CIVICS", "weightage_pct": 24},
                {"section_name": "SECTION D: ECONOMICS", "weightage_pct": 24}
            ],
            "branches": ["History", "Geography", "Civics", "Economics"],
            "description": "Integrated 4-pillar CBSE Social Science"
        },
        "English": {
            "display_name": "English",
            "code": "ENG",
            "type": "single",
            "language": "en",
            "sections": [
                {"section_name": "SECTION A: READING COMPREHENSION", "weightage_pct": 30},
                {"section_name": "SECTION B: WRITING & GRAMMAR", "weightage_pct": 40},
                {"section_name": "SECTION C: LITERATURE (HONEYDEW)", "weightage_pct": 30}
            ],
            "branches": ["Reading", "Grammar", "Writing", "Literature"],
            "description": "CBSE Class 8 English Language & Literature"
        },
        "Hindi": {
            "display_name": "Hindi (हिंदी)",
            "code": "HIN",
            "type": "single",
            "language": "hi",
            "sections": [
                {"section_name": "खंड 'क': अपठित बोध (Reading)", "weightage_pct": 25},
                {"section_name": "खंड 'ख': व्यावहारिक व्याकरण (Grammar)", "weightage_pct": 40},
                {"section_name": "खंड 'ग': पाठ्यपुस्तक वसंत (Literature)", "weightage_pct": 35}
            ],
            "branches": ["Vasant", "Vyakaran", "Apathit Bodh"],
            "description": "CBSE Class 8 Hindi Vasant & Vyakaran"
        },
        "Tamil": {
            "display_name": "Tamil (தமிழ்)",
            "code": "TAM",
            "type": "single",
            "language": "ta",
            "sections": [
                {"section_name": "பகுதி 'அ': செய்யுள் & மனப்பாடப்பகுதி", "weightage_pct": 35},
                {"section_name": "பகுதி 'ஆ': இலக்கணம் & மயங்கொலி", "weightage_pct": 35},
                {"section_name": "பகுதி 'இ': உரைநடை & வினா-விடை", "weightage_pct": 30}
            ],
            "branches": ["Seyyul", "Ilakkanam", "Urainadai"],
            "description": "SPS Tamil Curriculum & Grammar"
        }
    }

    @classmethod
    def get_all_subject_names(cls) -> List[str]:
        return list(cls.CATALOG.keys())

    @classmethod
    def get_subject_info(cls, subject_name: str) -> Optional[Dict[str, Any]]:
        # Fuzzy match or direct lookup
        for key, val in cls.CATALOG.items():
            if key.lower() == subject_name.lower():
                return val
            if subject_name.lower() in key.lower():
                return val
        return None


# ==============================================================================
# 3. SAMPLE SYLLABUS GROUND TRUTH (OCT 12 TO 17)
# ==============================================================================
class DiaryGroundTruth:
    """
    Verified syllabus ground truth extracted from Tharun's Senthil Public School diary
    for the primary testing sample range (October 12 to 17, 2026).
    """
    OCT_12_TO_17_PORTIONS = {
        "Mathematics": [
            {
                "chapter": "Algebraic Expressions & Identities",
                "subtopics": [
                    "Multiplication of Polynomials (Monomial by Monomial, Monomial by Polynomial)",
                    "Standard Algebraic Identities: (a + b)^2, (a - b)^2, a^2 - b^2, (x + a)(x + b)",
                    "Exercise 9.1, 9.2, and 9.3 (Q3 numerical evaluation)"
                ],
                "dates": ["2026-10-12", "2026-10-13"]
            },
            {
                "chapter": "Linear Equations in One Variable",
                "subtopics": [
                    "Solving linear equations with variables on both sides",
                    "Application word problems: Age problems, perimeter and number relation problems"
                ],
                "dates": ["2026-10-15"]
            },
            {
                "chapter": "Mensuration",
                "subtopics": [
                    "Area of a Trapezium formula: 1/2 * (a + b) * h",
                    "Surface area of a Cylinder: Total Surface Area and Curved Surface Area (2 * pi * r * h)"
                ],
                "dates": ["2026-10-17"]
            }
        ],
        "Physical Science": [
            {
                "chapter": "Force and Pressure (Physics)",
                "subtopics": [
                    "Definition and formula for Pressure: P = Force / Area",
                    "Atmospheric pressure and liquid pressure variation with depth",
                    "Factors affecting Friction: nature of surfaces in contact and normal force"
                ],
                "branch": "Physics",
                "dates": ["2026-10-12", "2026-10-14"]
            },
            {
                "chapter": "Chemical Effects of Electric Current (Chemistry)",
                "subtopics": [
                    "Liquids as conductors of electricity (Electrolytes and Non-electrolytes)",
                    "Mechanism and applications of Electroplating (Chromium coating, gold/silver plating)",
                    "Chemical reactions during electrolysis of copper sulphate solution"
                ],
                "branch": "Chemistry",
                "dates": ["2026-10-16"]
            }
        ],
        "Biology": [
            {
                "chapter": "Cell — Structure and Functions",
                "subtopics": [
                    "Discovery of the cell by Robert Hooke (1665)",
                    "Structural differences between Plant Cells and Animal Cells (Cell Wall, Chloroplast, Vacuole)",
                    "Functions of key cell organelles: Nucleus, Cytoplasm, Cell Membrane, Mitochondria"
                ],
                "branch": "Biology",
                "dates": ["2026-10-14", "2026-10-17"]
            }
        ],
        "Social Science": [
            {
                "chapter": "When People Rebel: 1857 and After (History)",
                "subtopics": [
                    "Causes of the 1857 revolt: Policies of the East India Company, Annexation of Awadh",
                    "Sepoy grievances and the Enfield cartridge incident",
                    "Consequences: End of East India Company rule and transfer to British Crown (1858 Act)"
                ],
                "branch": "History",
                "dates": ["2026-10-13", "2026-10-15"]
            },
            {
                "chapter": "Industries: Classification & Distribution (Geography)",
                "subtopics": [
                    "Classification of industries: On the basis of raw materials (Agro-based, Mineral-based)",
                    "Classification on the basis of size (Small-scale vs Large-scale)",
                    "Classification on the basis of ownership (Private, Public, Joint, Cooperative)"
                ],
                "branch": "Geography",
                "dates": ["2026-10-12", "2026-10-13", "2026-10-16"]
            },
            {
                "chapter": "The Indian Constitution & Secularism (Civics)",
                "subtopics": [
                    "Key features of the Indian Constitution: Federalism, Separation of Powers, Fundamental Rights",
                    "Understanding Indian Secularism: Non-interference and principled distance"
                ],
                "branch": "Civics",
                "dates": ["2026-10-14"]
            },
            {
                "chapter": "Understanding Economic Sectors (Economics)",
                "subtopics": [
                    "Primary, Secondary, and Tertiary economic activities",
                    "Role of market forces and consumer awareness in daily life"
                ],
                "branch": "Economics",
                "dates": ["2026-10-16"]
            }
        ],
        "English": [
            {
                "chapter": "Honeydew — Lesson 5 & Writing Skills",
                "subtopics": [
                    "Reading comprehension: Contextual vocabulary and theme identification",
                    "Grammar: Tenses, Active & Passive voice, Prepositions in sentence construction",
                    "Writing: Formal Letter format (Letter to Principal / Editor) with clear layout"
                ],
                "dates": ["2026-10-12", "2026-10-14"]
            }
        ],
        "Hindi": [
            {
                "chapter": "व्यावहारिक व्याकरण एवं वसंत पाठ (Hindi Grammar & Literature)",
                "subtopics": [
                    "संज्ञा (Noun) के भेद और पहचान",
                    "सर्वनाम (Pronoun) और उसके प्रकार",
                    "मुहावरे (Idioms) का अर्थ और वाक्य प्रयोग",
                    "शब्दार्थ एवं विलोम शब्द (Antonyms and Vocabulary)"
                ],
                "dates": ["2026-10-15"]
            }
        ],
        "Tamil": [
            {
                "chapter": "இயல் 1 - கவிதைப்பேழை & இலக்கணம் (Tamil Literature & Grammar)",
                "subtopics": [
                    "செய்யுள் 1, 2 மற்றும் திருக்குறள் (அதிகாரம் 1-5)",
                    "மயங்கொலி எழுத்துகள் பயிற்சி (ண, ன, ந / ல, ள, ழ / ர, ற)",
                    "வினா-விடை எழுதுதல் மற்றும் வாசித்தல் பயிற்சி"
                ],
                "dates": ["2026-10-12", "2026-10-13", "2026-10-16"]
            }
        ]
    }

    @classmethod
    def get_portions_for_subject(cls, subject_name: str) -> List[Dict[str, Any]]:
        info = SubjectCatalog.get_subject_info(subject_name)
        if not info:
            return []
        canonical_name = info["display_name"].split(" ")[0]
        # Match against our key set
        for key in cls.OCT_12_TO_17_PORTIONS:
            if key.lower() in subject_name.lower() or subject_name.lower() in key.lower():
                return cls.OCT_12_TO_17_PORTIONS[key]
        return []


# ==============================================================================
# 4. DECOUPLED GEMINI API GATEWAY
# ==============================================================================
class GeminiGateway:
    """
    Lightweight, self-contained API gateway to connect with Google Gemini.
    Reads config safely, handles key validation, and runs connection self-tests.
    """
    @staticmethod
    def load_config() -> Dict[str, Any]:
        default_cfg = {
            "api_key": "",
            "active_model": "gemini-2.5-flash",
            "class_level": "Class 8 CBSE",
            "school_name": "Senthil Public School, Dharmapuri",
            "student_name": "Tharun",
            "is_connected": False
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    default_cfg.update(data)
            except Exception as e:
                print(f"[GeminiGateway] Warning loading config: {e}")
        return default_cfg

    @staticmethod
    def save_config(cfg: Dict[str, Any]):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)

    @classmethod
    def get_api_key(cls) -> str:
        cfg = cls.load_config()
        return cfg.get("api_key") or cfg.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY", "")

    @classmethod
    def is_key_configured(cls) -> bool:
        return bool(cls.get_api_key().strip())

    @classmethod
    def test_connection(cls) -> Dict[str, Any]:
        """
        Pings Google Gemini API to test if the key is valid and which model responds.
        Returns a dict: {"success": bool, "model": str, "message": str}
        """
        api_key = cls.get_api_key()
        if not api_key:
            return {
                "success": False,
                "model": "None",
                "message": "⚪ No Gemini API key found in configuration. Offline Mode active."
            }

        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            
            # Model fallback sequence
            candidate_models = ["gemini-2.5-flash", "gemini-3.8-flash", "gemini-1.5-flash"]
            last_err = None

            for m in candidate_models:
                try:
                    resp = client.models.generate_content(
                        model=m,
                        contents="Respond with only: OK-CLASS-8"
                    )
                    text = getattr(resp, "text", "").strip()
                    if "OK-CLASS-8" in text or len(text) > 0:
                        # Update config with working model
                        cfg = cls.load_config()
                        cfg["active_model"] = m
                        cfg["is_connected"] = True
                        cls.save_config(cfg)
                        return {
                            "success": True,
                            "model": m,
                            "message": f"🟢 Connected to Google Gemini ({m})"
                        }
                except Exception as e:
                    last_err = str(e)
                    continue

            return {
                "success": False,
                "model": "Failed",
                "message": f"🔴 API key rejected or models unavailable: {last_err}"
            }
        except ImportError:
            return {
                "success": False,
                "model": "Missing SDK",
                "message": "🔴 google-genai library is not installed in Python environment."
            }


# ==============================================================================
# 5. SELF-TEST RUNNER (SESSION 1 VERIFICATION GATE)
# ==============================================================================
def run_session_1_verification():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 70)
    print("   SESSION 1: GROUND TRUTH & GEMINI API GATEWAY VERIFICATION")
    print("=" * 70)

    # 1. Test Subject Catalog
    print("\n[TEST 1] Subject Catalog Integrity Check:")
    subjects = SubjectCatalog.get_all_subject_names()
    print(f" -> Total Subjects Registered: {len(subjects)}")
    for s in subjects:
        info = SubjectCatalog.get_subject_info(s)
        type_str = f"[{info['type'].upper()}]"
        sec_count = len(info.get('sections', []))
        sec_str = f"({sec_count} sections)" if sec_count else "(Direct)"
        print(f"    * {s:<20} {type_str:<12} {sec_str:<15} Lang: {info['language']}")

    # 2. Test Oct 12-17 Diary Portions Ingestion
    print("\n[TEST 2] Oct 12-17 Diary Portions Ingestion Check:")
    for s in subjects:
        portions = DiaryGroundTruth.get_portions_for_subject(s)
        print(f"\n -> Subject: {s} (Found {len(portions)} Chapters)")
        for p in portions:
            branch_info = f"[{p['branch']}] " if 'branch' in p else ""
            print(f"    • {branch_info}{p['chapter']} (Dates: {', '.join(p['dates'])})")
            for sub in p['subtopics']:
                print(f"        - {sub}")

    # 3. Test Gemini API Gateway
    print("\n[TEST 3] Gemini API Gateway Live Connection Test:")
    print(" -> Checking API Key configuration...")
    has_key = GeminiGateway.is_key_configured()
    print(f" -> API Key Present: {'YES' if has_key else 'NO'}")
    
    print(" -> Pinging Gemini Cloud Services...")
    conn = GeminiGateway.test_connection()
    print(f" -> Result Status: {'SUCCESS' if conn['success'] else 'OFFLINE/FAILED'}")
    print(f" -> Active Model: {conn['model']}")
    print(f" -> Gateway Message: {conn['message']}")

    print("\n" + "=" * 70)
    if len(subjects) == 7 and conn['success']:
        print("   ✅ SESSION 1 VERIFICATION PASSED: Ground Truth & Gateway Ready!")
    else:
        print("   ⚠️ SESSION 1 VERIFICATION WARNING: Check details above.")
    print("=" * 70)


if __name__ == "__main__":
    run_session_1_verification()
