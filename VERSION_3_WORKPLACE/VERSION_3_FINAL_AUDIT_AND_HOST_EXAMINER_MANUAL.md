# SCHOLASTICPULSE VERSION 3 (V3)
## Master Architectural Audit & Host Examiner Operations Manual

---

### Executive Overview & Purpose
**ScholasticPulse Version 3 (V3)** elevates Tharun's study companion into an institutional-grade **CBSE Host Examination & Anti-Daydreaming Assessment System**. Designed specifically for **Senthil Public School, Dharmapuri (Class 8 CBSE)**, V3 empowers Tharun's father to act as the Chief Host Examiner—verifying genuine academic retention, rooting out superficial rote reading, and converting exam mistakes into permanent mastery.

---

## PART 1: MASTER ARCHITECTURAL AUDIT CHECKLIST

| Stage | Module / Component | Verification Status | Architectural Details & Guarantees |
| :--- | :--- | :---: | :--- |
| **Stage 0** | **V2 Fail-Safe Lock & Isolation** | **VERIFIED (100% UNTOUCHED)** | `VERSION_2_WORKPLACE/` has zero altered, renamed, or deleted files. `dist/ScholasticPulse_V2.exe` preserved. |
| **Stage 1** | **5 CBSE Expert Skills & Rubrics** | **VERIFIED** | Located in `EXAM_SYSTEM_V3/00_AGENT_SKILLS_AND_RUBRICS/`. Grounded in CBSE Class 8 curricula (`skill_01` to `skill_05`). |
| **Stage 2** | **EXAM_SYSTEM_V3 Storage Tree** | **VERIFIED** | 7 dedicated isolated folders for homework logs, textbooks, question papers, evaluated answer scripts, model guides, and score history. |
| **Stage 3** | **3-Phase Exam Assembler & 5-Card Selector** | **VERIFIED** | Sub-View 1 features interactive 5-card grid (Weeks 1–4 Sunday Tests + Month-End Mega Exam) with live entry counts, subjects, and score badges. |
| **Stage 4** | **Face A: Question Paper Architect** | **VERIFIED** | Supports Specified Textbook Chapter PDF with low-character (<100 char/page) OCR / Gemini Multimodal vision fallback + General CBSE blueprint mode. |
| **Stage 5** | **Face B: Answer Sheet Evaluator & Binder** | **VERIFIED** | Evaluates handwritten scans, applies CBSE step marking (+0.5M/-0.5M), synthesizes Red-Ink Teacher Soft Copy & Topper P-E-E-D guide, syncs mistakes to `student_error_bank.json`. |
| **Stage 6** | **High-DPI UI & Indic Unicode PDF Fonts** | **VERIFIED** | 3D parchment scroll banners, `ShinobiPillSelector` pills, ReportLab Indic rendering using `ARIALUNI.TTF` and `Nirmala.ttc` (Tamil, Hindi, Math symbols). |
| **Stage 7** | **Persistent Exam Score History** | **VERIFIED** | `exam_score_history.json` tracks cumulative exam dates, marks, percentage, grade, and focus verdicts, isolated from PyInstaller `_MEIPASS`. |

---

## PART 2: STEP-BY-STEP HOST EXAMINER GUIDE FOR THARUN'S FATHER

### Section A: One-Time Google Gemini AI Setup
1. **Launch the Application**:
   - Double-click `ScholasticPulse_V3.exe` (located in root `dist/` or `VERSION_3_WORKPLACE/`).
2. **Configure API Key**:
   - Navigate to the **🎯 Host Exam & AI** tab.
   - Click the **"🔑 Set Gemini API Key"** button in the top action bar.
   - Paste your Google Gemini API key into the prompt dialog and click OK.
   - The status indicator in the top right will switch to **🟢 Gemini AI Active**.
3. **Offline Mode Fail-Safe**:
   - If no API key is provided or the computer is offline, the status will show **⚪ Offline Local Mode**. ScholasticPulse will automatically utilize its built-in deterministic CBSE evaluation engine without failing.

---

### Section B: Conducting Phase 1 (Sunday Weekly Tests & Month-End Mega Exam)
> **Goal**: Verify thorough, deep recall of all homework logged Monday through Saturday.

1. **Open Sub-View 1 (`Study Ledger & 3-Phase Selector`)**:
   - Review Tharun's logged homework entries in the Subject Study Ledger.
2. **Select the Examination Card**:
   - Click one of the 5 interactive cards:
     * **Card 1**: `📅 Week 1 Sunday Test` (35 Marks, 1.5 Hours)
     * **Card 2**: `📅 Week 2 Sunday Test` (35 Marks, 1.5 Hours)
     * **Card 3**: `📅 Week 3 Sunday Test` (35 Marks, 1.5 Hours)
     * **Card 4**: `📅 Week 4 Sunday Test` (35 Marks, 1.5 Hours)
     * **Card 5**: `🏆 Month-End Mega Exam` (80 Marks, 3 Hours)
   - The selected card highlights in glowing Amber-Gold (`#f59e0b`), filters the preview ledger to that week's syllabus, and pre-loads the dataset into **Face A**.
3. **Generate and Print the Question Paper**:
   - Switch to **Sub-View 2 (Face A: Question Paper Architect)**.
   - Click **"⚡ Generate CBSE Question Paper"**.
   - Review the question breakdown across Sections A, B, C, D, and E.
   - Click **"🖨️ Print Question Paper"** to print a hard copy for Tharun.
4. **Conduct the Test**:
   - Hand Tharun the printed question paper and unruled lined paper.
   - Set the countdown timer (1.5 hours for weekly, 3 hours for month-end).
   - Ensure complete silence and strictly zero reference to textbooks or notes.

---

### Section C: Conducting Phase 2 (3-Day Pre-Exam Checkpoint Test)
> **Goal**: Stop superficial cramming during the 21-day Pre-Exam revision cycle.

1. **Trigger Condition**:
   - Automatically suggested when Pre-Exam Planner is set to **Day 3, 6, 9, 12, 15, 18, or 21**.
   - A glowing purple badge appears in the top header: `🎯 DAY X CHECKPOINT EXAM DUE`.
2. **Conducting the Test**:
   - Click the top header badge to jump directly into the Phase 2 test suite.
   - Total Marks: **25 Marks** | Duration: **1 Hour**.
   - Questions test formulas and definitions covered during the last 3 days of revision.

---

### Section D: Conducting Phase 3 (Morning Exam Eve Home Sprint Test)
> **Goal**: Rapid confidence warm-up on exam morning without inducing anxiety.

1. **Trigger Condition**:
   - Active on the morning of a school exam (before 12:00 PM).
   - A glowing emerald badge appears in the top header: `MORNING SPRINT DUE: [SUBJECT]`.
2. **Conducting the Test**:
   - Click the header badge to open the Phase 3 sprint module.
   - Total Marks: **25 Marks** | Duration: **45 Minutes**.
   - Rapid-fire MCQs, assertion-reasons, and 2-mark definitions.

---

### Section E: Uploading Answer Sheets & Step-Marking Evaluation (Face B)
1. **Digitize Tharun's Answer Script**:
   - Take photos or scan Tharun's handwritten answer sheets using your phone or desktop scanner (JPG, PNG, or PDF).
2. **Upload into Sub-View 3 (Face B)**:
   - Click **"📂 Upload Tharun's Handwritten Answer Sheets"** and select the image/PDF files.
3. **Execute Evaluation**:
   - Click **"🔍 Run CBSE Step-Marking Evaluation"**.
   - ScholasticPulse analyzes each question:
     * Transcribes Tharun's handwritten steps.
     * Compares against the expected CBSE marking scheme.
     * Applies step-by-step mark additions (+1.0M, +0.5M) and deductions (-0.5M for missing SI units, formula omissions, or orthography slips).
     * Annotates a **Red-Ink Teacher Correction Note** for every lost mark.
     * Issues an **Anti-Daydreaming Audit Verdict** (`Deep Focus Verified`, `Partial Attention`, or `Daydreaming Alert`).
4. **Automatic Error Bank Registration**:
   - Any question where Tharun lost marks is automatically extracted and logged into `student_error_bank.json` with its trap category, specific slip, and corrective action.

---

### Section F: Printing the 1-Click Physical Binder PDF & Score History
1. **Open Sub-View 4 (`Topper Model Answer Guide`)**:
   - Review the side-by-side comparison:
     * **Left**: *"How Tharun Answered & Why Marks Were Deducted"*
     * **Right**: *"How a CBSE Topper Answers for 100/100 Full Marks"*
2. **Export Physical Binder PDF**:
   - Click the prominent gold button: **"🖨️ Export Complete Exam & Topper Binder PDF"**.
   - Generates a unified ReportLab PDF containing:
     * **Part 1**: Graded scorecard, red-ink annotations, and anti-daydreaming verdict.
     * **Part 2**: Side-by-side topper comparison benchmarked against official CBSE marking schemes.
     * **Part 3**: P-E-E-D 5-point presentation guide and mandatory underline keywords checklist.
   - Print this PDF and place it into Tharun's physical study binder.
3. **Review Score History**:
   - Return to **Sub-View 1** to inspect the **Host Exam Score & Focus History** table.
   - Completed cards will display green verification pills (e.g., `✅ Scored: 29/35 (82.8%)`).

---
*End of ScholasticPulse V3 Operations Manual. Senthil Public School, Dharmapuri CBSE Academic Framework.*
