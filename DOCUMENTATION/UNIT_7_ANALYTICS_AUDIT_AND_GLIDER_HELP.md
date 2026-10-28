# UNIT 7: ANALYTICS, TIME AUDIT LEDGER & GLIDER IN-APP HELP SYSTEM

> **System Target**: ScholasticPulse – Tharun's Habit & Time Management Architect (Class 8 CBSE)  
> **Module Scope**: Historical time variance audit ledger, parental representation charts, native Glider Help & App Map system, and error diagnostic bridge.  
> **Integration Mode**: Direct In-App Documentation Hub & Standalone Master User Manual.

---

## ## 7.1 Historical Time Variance & Friction Audit Ledger

ScholasticPulse maintains a permanent, independent audit ledger of every timetable deviation, timer extension, and friction cause. This ensures that time management improves empirically over time rather than through guesswork.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 📊 TIME VARIANCE & COGNITIVE FRICTION AUDIT (time_extension_audit.json)                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  DATE       | SUBJECT     | PLANNED | ACTUAL | VARIANCE | PEDAGOGICAL CAUSE            │
│  ───────────┼─────────────┼─────────┼────────┼──────────┼──────────────────────────────│
│  2026-10-18 | Mathematics | 25 Mins | 35 Mins| +10 Mins | Long division decimal slips  │
│  2026-10-17 | Science     | 20 Mins | 25 Mins| +5 Mins  | Ray diagram arrow omissions  │
│  2026-10-16 | Tamil       | 20 Mins | 30 Mins| +10 Mins | ழ/ள/ல orthography rewrites   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### ### 7.1.1 Time Variance Audit File (`time_extension_audit.json`) Tracking & Causes
* **Purpose**: Records every instance where Tharun requested extra time on a homework task, logging the date, planned vs actual minutes, and the underlying pedagogical reason.
* **Workflow**:
  1. Whenever Tharun clicks `+5m` or `+10m` on the Focus Timer, the application prompts for or tags the friction cause.
  2. The record is written to `time_extension_audit.json` on disk.
  3. The schedule balancer analyzes these logs: if Mathematics consistently overruns by 10 minutes on Tuesday evenings, future Tuesday schedules automatically adjust initial allocations to maintain equilibrium.

---

### ### 7.1.2 Parental Representation & 7-Day / 30-Day Subject Balance Charts
* **Purpose**: Provides visual verification that all 7 CBSE subjects receive appropriate attention over a 7-day rolling week and a 30-day month.
* **Workflow**:
  1. From the top bar, click **`📖 Guides ▾`** ➔ **`Parent Representation & Balance Audit`** (or click the **`📊 Digest`** tile).
  2. Review the subject distribution progress bars:
     * **Mathematics**: Target 100% daily adherence (daily hand-solving).
     * **Physical Science & Biological Science**: Target 50% split (alternating days).
     * **Social Science**: Target 40–50% evening reading coverage.
     * **Languages (Tamil, Hindi, English)**: Target daily morning and evening clinic intervals.
  3. Verify that no single subject dominates the schedule at the expense of others.

---

## ## 7.2 The Native Glider Help & App Map System

The Glider Help system is an interactive architecture directory built directly into the desktop user interface. It provides instant access to system documentation, component explanations, and one-click troubleshooting assistance.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 🧭 SCHOLASTICPULSE GLIDER — INTERACTIVE ARCHITECTURE MAP                               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  🔍 Search Component: [ [#12]                                      ] [ Reset ]        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  [#12] 10:00 PM Bedtime Guard & Buffer Trimming                                        │
│  • Simple English: An unskippable safety rule that automatically shortens breaks and   │
│    moves non-urgent reading to morning, guaranteeing Tharun sleeps by 10:00 PM.        │
│  • Input: Time extension signals from [#11] (Live Focus Timer).                        │
│  • Output: Re-balanced schedule with deferred morning slots; audit records.            │
│  • Direct Links: Connected to [#10] (Schedule Balancer) and [#13] (Audit Ledger).      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### ### 7.2.1 The Top Header **🧭 Glider Map** Button & **`📖 Guides ▾`** Dropdown Menu Entry
* **Purpose**: Provides two easy entry points to launch the Glider Help window from anywhere in the application.
* **Workflow**:
  * **Option A (Direct Header Button)**: Click the glowing blue button **`🧭 Glider Map`** on the top header bar (located right next to **`📅 October ▾`**).
  * **Option B (Guides Flyout Menu)**: Click the **`📖 Guides ▾`** card in the command deck, and select the top item: **`🧭 Glider Help / App Map`**.
  * Both options immediately bring the **Glider Help & Architecture Map** window to the front.

---

### ### 7.2.2 The Interactive Glider Knowledge Window & Real-Time Keyword Search Bar (`[#01]`–`[#25]`)
* **Purpose**: Allows instant searching and browsing across all 25 system components without leafing through long documents.
* **Workflow**:
  1. Once the Glider Help window opens, locate the search bar at the top: **`🔍 Search Component (e.g. [#15] or Ledger):`**.
  2. Type any component tag (e.g., `[#08]`) or a plain-English keyword (e.g., `Timer`, `Bedtime`, `Math`, `OCR`, `Binder`).
  3. The view instantly filters to display matching components in real time.
  4. Each component card clearly outlines:
     * **Simple English**: Plain-English explanation of what the component does.
     * **Input**: Where the data comes from.
     * **Output / Destination**: Where the data goes.
     * **Direct Links**: Upstream and downstream component tags.
  5. Click **`Reset`** to clear the search bar and view all 25 components in chronological order.

---

### ### 7.2.3 The Error Bridge Architecture (Automated Diagnostics with One-Click Component Help Links)
* **Purpose**: Eliminates confusion if an operation encounters an issue (e.g., missing file, corrupted image, or network drop) by linking the error dialog directly to the relevant Glider Help component.
* **Workflow**:
  1. If an operation fails, the application catches the error and surfaces the **Glider Error Bridge Dialog**:  
     *“Could not parse syllabus PDF: [Details]  
     [Location: Component [#06]]  
     Would you like to open Glider Help to see what this component connects to?”*
  2. If the user clicks **`Yes`**:
     * The Glider Help window opens automatically.
     * The search bar is pre-filled with the component tag (e.g., `[#06]`).
     * The screen displays the exact purpose, expected input format, and downstream links for that component, showing the user how to fix the issue.
  3. If the user clicks **`No`**, the dialog dismisses normally.

---

## ## 7.3 Master Component Tag Cross-Reference Index (`[#01]` – `[#25]`)

For rapid reference during maintenance or system discussions, use this unified index:

| Tag | Component Name | Primary File / Location | Manual Chapter |
|---|---|---|---|
| `[#01]` | Textbook & School Model PDFs | `EXAM_SYSTEM_V3/02_TEXTBOOKS/` | Unit 5.1 |
| `[#02]` | Syllabus Sheets (Term 1) | Teacher circulars / PDFs | Unit 3.1 |
| `[#03]` | Diary Photos / Docs / Scans | Phone camera photos / handbook | Unit 3.1 |
| `[#04]` | Manual Quick-Add Diary UI | Tab 1 Quick-Add Form | Unit 3.1 |
| `[#05]` | PDF Vault Library | `EXAM_SYSTEM_V3/` | Unit 5.1 |
| `[#06]` | Exam Portion Parser | `exam_portion_parser.py` | Unit 4.1 |
| `[#07]` | Portion Database | `tharun_exam_portions.json` | Unit 4.1 |
| `[#08]` | Universal Diary Importer | `diary_importer.py` (WinOCR) | Unit 3.1 |
| `[#09]` | Master Diary Database | `tharun_diary_format.json` | Unit 3.1 |
| `[#10]` | Dynamic Schedule Balancer | `study_balancer.py` (Tab 0 & 1) | Unit 2.1 |
| `[#11]` | Live Pomodoro Focus Timer | Tab 0 Focus Clock HUD | Unit 2.2 |
| `[#12]` | 10:00 PM Bedtime Guard | Cascading Hierarchy Engine | Unit 2.3 |
| `[#13]` | Time Variance Audit Ledger | `time_extension_audit.json` | Unit 7.1 |
| `[#14]` | Shinobi Theme & Voice Engine | `assets/naruto/`, `generate_naruto_audio.py` | Unit 1.2 |
| `[#15]` | Subject Study Ledger Engine | `exam_study_ledger_v3.py` | Unit 4.1 |
| `[#16]` | Intra-Head Cognitive Ledger | `subject_study_ledger.json` | Unit 4.1 |
| `[#17]` | 3-Phase Aggregation Pipeline | `exam_phase_assembler_v3.py` | Unit 4.2 |
| `[#18]` | Face A Generator Studio | `host_exam_face_a_ui_v3.py` | Unit 5.2 |
| `[#19]` | Smart Time Dial | 5m / 10m / 20m / 35m Slider | Unit 5.2 |
| `[#20]` | Gemini Flash API & Local Fallback | Gemini 2.5 Flash / Rule Engine | Unit 5.2 |
| `[#21]` | Printable QP & Ruled Booklet PDF | `exam_print_studio_v3.py` | Unit 5.2 |
| `[#22]` | Student Answer Sheet Ingestion | Tab 2 Subview 5 | Unit 6.1 |
| `[#23]` | CBSE 4-Tier Step Evaluator | `exam_evaluator_v3.py` | Unit 6.2 |
| `[#24]` | Student Error Bank | `student_error_bank.json` | Unit 1.2 & 6.2 |
| `[#25]` | Topper Guide & Physical Binder PDF | `host_exam_topper_ui_v3.py` | Unit 6.3 |
