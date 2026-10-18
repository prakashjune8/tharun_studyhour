# SCHOLASTICPULSE: CHRONOLOGICAL PROJECT EVOLUTION & MASTER ARCHITECTURE SUMMARY (V1 → V2 → V3)

> **Document Version**: 3.0.0-MASTER  
> **Target Audience**: Chief Architect, Pedagogical Systems Reviewers, Engineering Stakeholders  
> **Project**: ScholasticPulse (Tharun's Shinobi Habit Balancer & CBSE AI Examination Suite)  
> **Student**: Tharun (Class 8 CBSE, Senthil Public School, Dharmapuri)  
> **Generated At**: 2026-10-19T01:10:00+05:30  

---

## EXECUTIVE TABLE OF CONTENTS
1. [Version 1 (V1): The Baseline Foundation](#1-version-1-v1-the-baseline-foundation)
2. [Version 2 (V2): The Shinobi Architecture & Fail-Safe Hardening](#2-version-2-v2-the-shinobi-architecture--fail-safe-hardening)
3. [Version 3 (V3): The Anti-Daydreaming Host Exam & AI Evaluator](#3-version-3-v3-the-anti-daydreaming-host-exam--ai-evaluator)
4. [Technical Stack, Directory Isolation & Binary Specifications](#4-technical-stack-directory-isolation--binary-specifications)
5. [Chronological Feature Comparison Matrix](#5-chronological-feature-comparison-matrix)

---

## 1. VERSION 1 (V1): THE BASELINE FOUNDATION

### 1.1 Original Core Problem Solved
Prior to the inception of ScholasticPulse, daily after-school study for Class 8 was uncalibrated. Homework tasks assigned in the school diary were often tackled erratically without accounting for:
- Uneven fatigue levels after school transit.
- Cognitive overload caused by cramming math calculations late at night.
- Imbalance across the 7 CBSE subjects (Mathematics, Physical Science, Biological Science, Social Science, English, Hindi, and Tamil).
- Lack of audit tracking for time extensions and uncompleted homework slips.

**Version 1** established the initial proof-of-concept by introducing:
- A rudimentary timetable balancer that ingested school diary entries.
- Static evening schedule allocation starting at 7:00 PM.
- A basic countdown study timer with desktop sound beeps.
- Primitive student error logging for arithmetic mistakes.

### 1.2 Initial UI Framework & Architecture
- **GUI Engine**: Monolithic Python `tkinter` script (`VERSION_1_WORKPLACE/study_balancer.py`, ~625 KB, ~12,400 lines).
- **Web Prototype**: Companion single-file HTML/JS document (`VERSION_1_WORKPLACE/index.html`, ~545 KB).
- **Visual Design**: Standard OS-rendered Tkinter widgets (`tk.Entry`, `ttk.Combobox`, `tk.Listbox`) using standard Windows 98/2000-style bevels and basic color accents.
- **Diary Parsing Engine** (`diary_importer.py`): Basic regex and prefix matching (`Math:`, `Phy:`, `Tamil:`) capable of parsing simple single-column text inputs.
- **Portion Tracking** (`exam_portion_parser.py`): Ingested PDF syllabus sheets using early `pypdf` extraction.

### 1.3 Primitive JSON Storage & Structural Vulnerabilities
In Version 1, data persistence was implemented via basic `open(filename, "r")` and `open(filename, "w")` calls targeting relative paths in the current working directory:
- `study_routine_data.json` (~6.5 KB): Saved active subjects, routine timers, and streak counts.
- `tharun_diary_format.json` (~6.4 KB): Contained a preliminary 3-date seed (`2026-10-06`, `07`, `08`).
- `student_error_bank.json` (~2.7 KB): Stored manual error notes without automated rubric association.
- `time_extension_audit.json` (~8.6 KB): Logged timestamped button clicks for timer extensions.

#### Critical V1 Architectural Flaws:
1. **The PyInstaller `_MEIPASS` Data Loss Bug**: When compiled into a standalone executable (`ScholasticPulse_V1.exe`, ~43.2 MB), files packaged with the binary were unpacked into Windows' temporary directory (`%TEMP%\_MEIxxxxxx`). When the application saved user data, it wrote into this temporary folder. Upon closing the app, Windows cleaned up the directory, **completely wiping the student's study logs and streaks**.
2. **Window Sizing & DPI Drift**: Standard Tkinter geometry caused UI elements to clip or overflow on higher DPI displays (125%–150% Windows scaling).
3. **Fragile Subject Parsing**: Lacked intelligent multi-language recognition for Tamil script or Hindi Devanagari, frequently dropping non-Latin text.

---

## 2. VERSION 2 (V2): THE SHINOBI ARCHITECTURE & FAIL-SAFE HARDENING

Preserved permanently as an inviolable reboot checkpoint in `D:\THARUN PROJECT\VERSION_2_WORKPLACE\`.

### 2.1 Strict Pedagogical Constraints Introduced
Version 2 transformed the utility tool into an ironclad pedagogical framework tailored specifically to Class 8 cognitive development at Senthil Public School:

1. **Inviolable 10:00 PM Bedtime Curfew**:
   - The scheduler enforces a strict ceiling: no study session can extend beyond 10:00 PM under any circumstances to safeguard adolescent sleep architecture.
2. **Morning Rollover Protocol (6:45 AM – 7:15 AM)**:
   - Mathematics is strictly prohibited in the morning session.
   - The scheduler automatically slots a secondary core subject (Physical Science, Biological Science, or Social Science) paired with a high-focus language retention drill (Tamil or Hindi).
3. **Cognitive Tier Sittings (Genin → Chunin → Jonin)**:
   - Level 1 (**Genin**): 15-minute ultra-focused sprints with 5-minute active recovery (designed for fatigue days).
   - Level 2 (**Chunin**): 30-minute balanced intervals (standard daily equilibrium).
   - Level 3 (**Jonin**): 45-minute deep-work blocks (reserved for pre-exam weekends).
4. **Mandatory 15-Minute Drawing & Diagram Practice**:
   - An unskippable evening slot dedicated to physical diagrammatic mastery (ray optics, cell anatomy, circuit diagrams, map plotting).
5. **Complementary Core Loop**:
   - If the school diary assigns Science homework, the scheduler automatically prioritizes Social Science for self-study to maintain dual-core equilibrium.

### 2.2 The Shinobi Graphics Engine Overhaul
Version 2 discarded default OS chrome in favor of a bespoke, anime-inspired aesthetic designed to motivate an 8th-grade student:

* **8 Dynamic Chakra Theme Palettes**:
  1. `naruto_sage`: Deep indigo-navy background (`#0a0e17`), warm card base (`#151c2e`), glowing Sage orange border (`#f97316`), bright gold accent (`#facc15`).
  2. `sasuke_chidori`: Dark lightning slate (`#070d18`), cyan chakra borders (`#38bdf8`), vibrant lightning core (`#0284c7`).
  3. `kakashi_hatake`: Muted ninja tactical gray-navy, Raikiri purple highlights (`#a855f7`).
  4. `minato_flash`: Yellow-flash lightning amber and rapid sprint highlights.
  5. `itachi_uchiha`: Crimson sharingan accents (`#ef4444`) on dark obsidian.
  6. `leaf_village`: Forest green chakra vitality accents (`#22c55e`).
  7. `dark`: Neutral dark glassmorphic UI.
  8. `light`: High-contrast daytime study theme.
* **4x SSAA Anti-Aliased Konoha Leaf Crest**:
  - Dynamically drawn on a Tkinter `Canvas` with an outer gold metallic ring, dark radial core, and glowing chakra aura.
* **3D Parchment Scroll Tabs & UI Deck**:
  - Main navigation tabs styled as rolled ninja scrolls with red ribbon ends and subtle paper textures.
  - Bespoke `ShinobiPillSelector` replacing unstyled dropdowns with two-line micro-cards (30×30px emoji icons, 8pt bold header, 7pt subtitle).
* **30-Day Consistency Heatmap**:
  - 2×2 weekly calendar matrix tracking consistency streaks, Feynman recall archives, and study time variance.

### 2.3 The Dual-Path PyInstaller JSON Isolation Strategy
To completely eliminate the V1 data-loss bug, Version 2 introduced the **Dual-Path Resolution Engine** (`get_persistent_data_path()`):

```python
def get_persistent_data_path(filename: str) -> str:
    """
    Precision Dual-Path Resolution for Mutable JSON Databases:
    - Never resolves against sys._MEIPASS (ephemeral extraction directory).
    - In frozen binary mode, strictly resolves to the persistent executable directory on disk.
    - If running frozen and file does not exist yet, copies bundled seed template from _MEIPASS.
    - If running as Python script, resolves to script directory.
    """
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(os.path.abspath(sys.executable))
        target_path = os.path.join(base_dir, filename)
        if os.path.exists(target_path):
            return target_path
        parent_dir = os.path.dirname(base_dir)
        parent_target = os.path.join(parent_dir, filename)
        if os.path.exists(parent_target):
            return parent_target
        meipass_path = getattr(sys, '_MEIPASS', None)
        if meipass_path:
            seed_file = os.path.join(meipass_path, filename)
            if os.path.exists(seed_file):
                try:
                    if os.path.isdir(seed_file):
                        shutil.copytree(seed_file, target_path, dirs_exist_ok=True)
                    else:
                        shutil.copy2(seed_file, target_path)
                except Exception:
                    pass
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
```

---

## 3. VERSION 3 (V3): THE ANTI-DAYDREAMING HOST EXAM & AI EVALUATOR

Housed in `D:\THARUN PROJECT\VERSION_3_WORKPLACE\`.

Version 3 represents the quantum leap from **passive timetable planning** to **active cognitive retention & automated assessment**.

```
┌────────────────────────────────────────────────────────────────────────┐
│               SCHOLASTICPULSE V3 ARCHITECTURAL PIPELINE                │
└────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌───────────────────────┐      ┌────────────────────────┐
│  Tab 1: School Diary  │ ───► │  Tab 0: Daily Schedule │
│  (12-Day HW Ingestion)│      │  (Morning/Evening Slabs│
└───────────────────────┘      └────────────────────────┘
          │
          ▼
┌────────────────────────────────────────────────────────────────────────┐
│             Tab 2: HOST EXAMINATION & GEMINI EVALUATOR V3              │
├────────────────────────────────────────────────────────────────────────┤
│  Subview 1: Study Ledger & Phases (Full Month Oct 1–24 + W1–W4)        │
│  Subview 2: Dedicated Textbook Vault (Uploaded NCERT/Photocopy PDFs)   │
│  Subview 3: School Sample Papers Vault (Senthil SPS Model References)  │
│  Subview 4: Face A - Question Paper Architect (Blueprint/PDF -> QP)    │
│  Subview 5: Face B - Answer Sheet Evaluator (Multimodal Vision OCR)     │
│  Subview 6: CBSE Topper Guide & Step-Marking (P-E-E-D Model & Binder)  │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.1 The 3-Phase Host Examination Engine
1. **Phase 1: Comprehensive Weekly Sunday & Month-End Examination**:
   - **Weekly Sunday Test**: Aggregates Monday–Saturday homework entries (35 Marks, 60 Mins).
   - **Month-End Mega Exam**: Combines Weeks 1–4 across all 7 subjects (80 Marks, 180 Mins) matching official CBSE Term 1 format.
2. **Phase 2: Pre-Exam 3-Day Checkpoint Examination**:
   - Mathematical modulo trigger (`Day % 3 == 0`).
   - Aggregates the preceding 3 days of study blocks into targeted 25-mark audit checks to ensure long-term retention before moving to new units.
3. **Phase 3: Exam Eve Morning Retention Sprint**:
   - Executed between **06:40 AM and 07:15 AM** on the morning of a school exam.
   - 25 Marks, 35–45 Mins: Focuses exclusively on high-yield definitions, mathematical formulas, and core diagrammatic labeling.

### 3.2 Subview 1: The 3-Tier Intra-Head Study Ledger (`exam_study_ledger_v3.py`)
Indexes every homework task into a 3-tier cognitive taxonomy:
- **Head 1**: *Core Concepts & Principles* (Theories, laws, grammatical rules).
- **Head 2**: *Problem Solving & Applications* (Numerical calculations, step algebra, translation).
- **Head 3**: *Visual, Diagrammatic & Orthography* (Scientific drawings, circuits, handwriting neatness).
- **Master Curation Strip**:
  - `🌐 Full Month Ledger`: Displays all 68 entries across 24 dates (Oct 01–24).
  - Individual week filters: Week 1 (Oct 1–6), Week 2 (Oct 7–13), Week 3 (Oct 14–20), Week 4 (Oct 21–24).

### 3.3 Face A: Question Paper Architect (`host_exam_face_a_ui_v3.py`)
- **Dual Grounding Modes**:
  1. *Curriculum Blueprint Mode*: Generates questions using NCERT syllabus portion maps.
  2. *Uploaded School PDF Mode*: Extracts raw text via `pypdf` / `winocr` from teacher photocopies and school model exam papers to emulate teacher questioning phrasing.
- **Smart Time Dial**:
  - Slider options: 5m Rapid (5M), 10m Express (10M), 20m Standard (15M), 35m Comprehensive (25M).
- **Live Output Studio**:
  - Instant KaTeX-rendered responsive HTML preview.
  - Printable **Blank Answer Booklet PDF** with student identification headers and calibrated ruling lines for handwritten working steps.

### 3.4 Face B: Answer Sheet Evaluator & Vision OCR (`host_exam_face_b_ui_v3.py`)
- **Multimodal Gemini Vision OCR Engine** (`exam_vision_ocr_engine_v3.py`):
  - Ingests scanned handwritten student answer sheets (`.txt`, `.pdf`, `.png`).
  - Transcribes messy handwriting and mathematical formulas with 95%+ confidence.
  - Aligns transcribed student responses directly with official model answers.
  - **Zero-Lag Offline Fallback**: High-accuracy local parser guaranteeing zero application crash if internet drops.
- **CBSE 4-Tier Step-Marking**:
  - Method (M), Accuracy (A), Formulation (F), and Final Unit Box.
  - Auto-syncs errors to `student_error_bank.json` and score history to `subject_study_ledger.json`.

### 3.5 Subview 6: CBSE Topper Guide & Physical Binder PDF (`host_exam_topper_ui_v3.py`)
- **P-E-E-D 100/100 Reference Model**:
  - **P**oint: State the fundamental rule or theorem.
  - **E**xplanation: Provide the step-by-step mathematical reasoning.
  - **E**xample: Show the complete arithmetic calculation.
  - **D**iagram / Unit Box: Draw the labeled diagram and frame the final answer with units.
- **ReportLab Indic Unicode Typography Pipeline** (`exam_typography_engine_v3.py`):
  - Uses native Windows TrueType fonts (`ARIALUNI.TTF` / `Nirmala.ttc`).
  - Full native rendering for Tamil script (`தமிழ் வினாத்தாள்`) and Hindi Devanagari (`हिंदी प्रश्न-पत्र`).
  - **1-Click Physical Binder PDF**: Combines Question Paper, Graded Answer Sheet with Red-Ink Annotations, and Topper Model Guide into a single printable exam archive.

---

## 4. TECHNICAL STACK, DIRECTORY ISOLATION & BINARY SPECIFICATIONS

### 4.1 Directory Isolation & Safeguard Hierarchy
```
D:\THARUN PROJECT\
│
├── ScholasticPulse_V3.exe                  # Standalone Windows Executable (Production Release)
├── tharun_diary_format.json               # Master 12-Day School Diary Database (Oct 06–19)
├── study_routine_data.json                # User preferences, streak, active date
├── tharun_exam_portions.json              # Syllabus & Term 1 exam portion breakdown
├── student_error_bank.json                # Historical student mistakes & remediation
├── time_extension_audit.json              # Focus timer extension audit log
│
├── dist\                                  # Release Mirror
│   ├── ScholasticPulse_V3.exe             # 78.2 MB Standalone PyInstaller Binary
│   └── (Database Mirrors)
│
├── VERSION_1_WORKPLACE\                   # ARCHIVE: Baseline V1 Proof-of-Concept
│   └── (study_balancer.py 625 KB, ScholasticPulse_V1.exe 43.2 MB)
│
├── VERSION_2_WORKPLACE\                   # UNTOUCHABLE SAFE RESET: Shinobi Anime Edition
│   ├── study_balancer.py                  # 826 KB (Shinobi Engine, 8 themes, dual-path isolation)
│   ├── index.html                         # 731 KB (Web Parity Edition)
│   └── dist\ScholasticPulse_V2.exe        # 61.5 MB (Certified Stable Fallback)
│
└── VERSION_3_WORKPLACE\                   # ACTIVE PRODUCTION: Host Exam & AI Evaluator
    ├── study_balancer.py                  # 734 KB (Main GUI Entry Point, 14,773 lines)
    ├── host_exam_ui.py                    # 46.7 KB (Master Exam Controller & Subview Router)
    ├── host_exam_face_a_ui_v3.py          # 41.2 KB (Face A Question Paper Architect UI)
    ├── host_exam_face_b_ui_v3.py          # 36.8 KB (Face B Answer Sheet Evaluator UI)
    ├── host_exam_topper_ui_v3.py          # 29.5 KB (Topper Model Guide & Binder UI)
    ├── exam_vault_library_view_v3.py      # 33.4 KB (Textbook Vault UI)
    ├── exam_sample_questions_view_v3.py   # 31.8 KB (Sample Papers Vault UI)
    ├── exam_ground_truth_v3.py            # 20.1 KB (CBSE Catalog & Gemini Gateway)
    ├── exam_study_ledger_v3.py            # 11.2 KB (Study Ledger & Score History)
    ├── exam_question_architect_v3.py      # 28.8 KB (CBSE Question Generator Engine)
    ├── exam_evaluator_v3.py               # 33.2 KB (Step-Wise Marking & Evaluator)
    ├── exam_print_studio_v3.py            # 27.3 KB (ReportLab PDF & HTML Print Studio)
    ├── exam_vision_ocr_engine_v3.py       # 18.5 KB (Multimodal Vision OCR Engine)
    ├── exam_typography_engine_v3.py       # 14.3 KB (Windows Indic TrueType Font Registry)
    ├── diary_importer.py                  # 19.8 KB (Universal Diary Ingestion Engine)
    ├── schedule_engine.py                 # 22.4 KB (Timetable Balancing Engine)
    ├── shinobi_ui.py                      # 16.5 KB (Custom UI Components)
    ├── ScholasticPulse_V3.spec            # PyInstaller Specification
    └── EXAM_SYSTEM_V3\                    # Decoupled Examination Data Repository
```

### 4.2 PyInstaller Binary Specifications

| Metric | Version 1 (V1) | Version 2 (V2) | Version 3 (V3) |
| :--- | :--- | :--- | :--- |
| **Executable Name** | `ScholasticPulse_V1.exe` | `ScholasticPulse_V2.exe` | `ScholasticPulse_V3.exe` |
| **Binary Size** | ~43.2 MB | ~61.5 MB | **78.2 MB (78,261,782 bytes)** |
| **Python Version** | Python 3.14.0rc2 | Python 3.14.0rc2 | **Python 3.14.0rc2** |
| **Window Subsystem** | Windows GUI (`console=False`) | Windows GUI (`console=False`) | **Windows GUI (`console=False`)** |
| **Core Libraries** | `tkinter`, `PIL` | `tkinter`, `PIL`, `pywinstyles` | `tkinter`, `PIL`, `pywinstyles`, `google.genai`, `reportlab`, `pypdf`, `pypdfium2` |
| **Bundled Data** | `assets/` | `assets/`, JSON seeds | `assets/`, `EXAM_SYSTEM_V3/`, JSON databases |
| **Hidden Imports** | 5 imports | 12 imports | **35 imports** (all decoupled sub-engines) |
| **Persistence Safety** | ❌ Ephemeral (`_MEIPASS` risk) | ✅ Dual-Path Protected | ✅ **Dual-Path Protected + Directory Tree Seeding** |

---

## 5. CHRONOLOGICAL FEATURE COMPARISON MATRIX

| Feature Category | Version 1 (V1 Baseline) | Version 2 (V2 Shinobi) | Version 3 (V3 Host Exam & AI) |
| :--- | :--- | :--- | :--- |
| **Design Aesthetic** | Default Tkinter gray bevels | Shinobi Anime (8 Palettes, Konoha Crest, Scroll Tabs) | Shinobi Anime + Modern Dark Glass Host Exam Suite |
| **Bedtime Enforcement** | Soft recommendation | Inviolable 10:00 PM Bedtime Curfew | Inviolable 10:00 PM Curfew + Morning Retention Alerts |
| **Cognitive Slabs** | Static study slots | 15m (Genin), 30m (Chunin), 45m (Jonin) | 15m/30m/45m Slabs + Smart Time Dial (5m–60m) |
| **School Diary Ingestion** | Basic single-entry regex | S1–S4 Photo & PDF Ingestion | Dual-Date Page Splitting (Oct 14 vs 15) + Full 12 Days |
| **Study Ledger** | Basic text list | 30-Day Heatmap & Streak Matrix | 3-Tier Intra-Head Taxonomy (68 Entries, Oct 01–24) |
| **Exam Capabilities** | Static syllabus text view | Syllabus tracking by chapter | 3-Phase Engine (Sunday 35M, Month-End 80M, Eve 25M) |
| **Question Paper Studio** | ❌ None | ❌ None | Face A: Vector PDF + KaTeX HTML + Blank Booklets |
| **Answer Sheet Grading** | ❌ None | ❌ None | Face B: Gemini Vision OCR + Local Fallback Engine |
| **CBSE Rubrics** | ❌ None | ❌ None | Step-marking (Method, Accuracy, Formulation, Unit Box) |
| **Model Answers** | ❌ None | ❌ None | P-E-E-D 100/100 Topper Reference Guides |
| **Multi-Language PDF** | ❌ English only | ❌ English only | ReportLab Indic TrueType (`ARIALUNI.TTF` / `Nirmala`) |
| **Physical Binder Export** | ❌ None | ❌ None | 1-Click All-in-One Printable Exam Binder PDF |
| **Offline Reliability** | Offline only (no AI) | Offline only (no AI) | Hybrid AI: Gemini Cloud + Zero-Crash Local Engine |
| **Packaging Persistence** | ⚠️ Broken (`_MEIPASS` wipe) | ✅ Secured via `get_persistent_data_path` | ✅ Secured Dual-Path with Recursive Directory Seeding |

---
*End of Master Summary Document. Preserved permanently in `D:\THARUN PROJECT\SCHOLASTICPULSE_V1_V2_V3_MASTER_SUMMARY.md`.*
