# UNIT 5: EXAM VAULTS & QUESTION PAPER ARCHITECT (FACE A)

> **System Target**: ScholasticPulse – Tharun's Habit & Time Management Architect (Class 8 CBSE)  
> **Module Scope**: Textbook vault, school model papers repository, Face A question paper generator studio, smart time dial, KaTeX preview, and blank answer booklets.  
> **Integration Mode**: Direct In-App Documentation Hub & Standalone Master User Manual.

---

## ## 5.1 Subviews 2 & 3: Dedicated Textbook & Sample Papers Vaults

The Examination Vaults provide a local, offline digital library of Tharun's official study materials. By indexing textbooks and teacher question papers, generated tests faithfully emulate the phrasing, vocabulary, and difficulty of Senthil Public School exams.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 📂 EXAM SYSTEM VAULT LIBRARY (EXAM_SYSTEM_V3)                                          │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  [ Subview 2: Textbook Vault ]           [ Subview 3: School Sample Papers Vault ]     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  • NCERT Class 8 Mathematics (Ex 9.1 - 9.3)  • SPS Term 1 Model Question Paper (Maths) │
│  • NCERT Class 8 Science (Ch 4, 5, 8, 11)   • Senthil Midterm Revision Unit Tests      │
│  • Samacheer Kalvi Tamil Textbook (இயல் 1-3) • CBSE Official Class 8 Sample Bank       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### ### 5.1.1 Ingested NCERT Textbook Chapters & Page Indexing
* **Purpose**: Stores official textbook PDFs (`EXAM_SYSTEM_V3/02_UPLOADED_TEXTBOOKS_PDF`). Chunks and indexes exercise questions so the question paper generator can draw directly from textbook problems.
* **Workflow**:
  1. Open Subview 2 (**Textbook Vault**).
  2. Inspect the catalog of uploaded textbooks (Mathematics, Science, Social Science, Tamil, Hindi, English).
  3. Click **`➕ Ingest New Textbook Chapter`** to upload a new NCERT PDF.
  4. The engine extracts exercise questions, example problems, and chapter summaries, making them available to Face A.

---

### ### 5.1.2 Senthil Public School Model Papers Repository & Teacher Phrasing Analysis
* **Purpose**: Houses teacher-prepared term question papers (`EXAM_SYSTEM_V3/02_SCHOOL_MODEL_PAPERS_PDF`). Analyzes how Senthil Public School teachers phrase questions (e.g., standard phrasing like *"State the reason why..."* or *"Find the value of $x$ and verify your answer"*).
* **Workflow**:
  1. Open Subview 3 (**Sample Papers Vault**).
  2. Review historical test papers uploaded for Tharun's class.
  3. When Face A generates an exam, it cross-references these papers to ensure that generated tests feel familiar and school-aligned.

---

## ## 5.2 Subview 4: Face A – Question Paper Architect

Subview 4 houses the **Face A Question Paper Architect** (`host_exam_face_a_ui_v3.py`). It provides a control deck for generating customized CBSE question papers.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 📝 FACE A: QUESTION PAPER ARCHITECT STUDIO                                              │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  Subject: [ Mathematics ▾ ]             Mode: (●) Syllabus Blueprint   (○) PDF Ground  │
│                                                                                        │
│  SMART TIME DIAL:                                                                      │
│  [ 5m Rapid (5M) ]  [ 10m Express (10M) ]  [ 20m Standard (15M) ]  [ 35m Full (25M) ]  │
│                                                                                        │
│  [ 🟢 Gemini 2.5 Flash Active ]                 [ ⚡ Generate Question Paper ]          │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  STUDIO PREVIEW:                                                                       │
│  [ 🖨️ Live KaTeX Print Preview ]   [ 📄 Export Question PDF ]   [ 📝 Blank Booklet PDF ]│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### ### 5.2.1 The **Smart Time & Intensity Dial**
* **Purpose**: A single 4-stop slider configuring test duration, total marks, and cognitive intensity with one click:
* **Available Dial Settings**:
  * **5m Rapid Sprint (5 Marks, 3 Questions)**: 3 quick objective/formula recall questions for a fast mental warm-up.
  * **10m Express Checkpoint (10 Marks, 5 Questions)**: 2 objective + 3 short application questions.
  * **20m Standard Test (15 Marks, 7 Questions)**: Standard daily test covering 1 long problem, 4 short problems, and 2 definitions.
  * **35m Comprehensive Sitting (25 Marks, 10 Questions)**: Full-scale formal test covering multi-step problems, diagrams, and proofs.

---

### ### 5.2.2 Grounding Modes: Curriculum Blueprint vs Uploaded School PDF Text
* **Purpose**: Selects the knowledge source for test generation:
* **Workflow**:
  1. Choose between the two grounding radio buttons:
     * **Mode 1: Curriculum Blueprint Mode**: Uses CBSE syllabus portion maps (`tharun_exam_portions.json`) to balance questions proportionally across term chapters.
     * **Mode 2: Uploaded School PDF Mode**: Extracts raw text from an uploaded teacher handout, generating questions directly derived from school worksheets.

---

### ### 5.2.3 Google Gemini 2.5 Flash API Gateway & Zero-Lag Local Heuristic Fallback
* **Purpose**: Guarantees fast, reliable test paper generation whether internet is connected or completely offline.
* **Workflow**:
  1. Click **`⚡ Generate Question Paper`**.
  2. If an API key is configured and internet is live:
     * The app sends a prompt payload to **Google Gemini 2.5 Flash**.
     * The model crafts an authentic CBSE paper formatted into clean JSON with questions, mark allocations, and model answer rubrics.
  3. If offline or no internet:
     * The **Zero-Lag Local Fallback Engine** takes over instantaneously.
     * It generates a complete, mathematically verified question paper from local question banks with zero lag and zero application crash.

---

### ### 5.2.4 Printable Question Paper Studio & KaTeX Math Rendering Preview
* **Purpose**: Provides instant screen preview and professional PDF export.
* **Workflow**:
  1. Once generated, inspect the **Live KaTeX Preview** on screen. All mathematical equations ($\frac{a}{b}$, $\sqrt{x}$, $x^2$) render in textbook-quality typography.
  2. Click **`📄 Export Question PDF`** to create a printable PDF formatted with official school examination headers, time limits, and instructions.

---

### ### 5.2.5 The 75/25 Workspace Blank Answer Booklet PDF Generation
* **Purpose**: Generates a physical lined answer booklet with a dedicated calculation column, enforcing neat handwriting and proper rough work.
* **Workflow**:
  1. Click **`📝 Blank Booklet PDF`**.
  2. The **Exam Print Studio** (`exam_print_studio_v3.py`) generates a multi-page printable PDF:
     * **Header**: Student Name (Tharun), Class 8, Roll Number, Date, Max Marks.
     * **Ruling**: Clean 8mm horizontal ruling lines.
     * **The 75/25 Layout**: The left 75% of each page is reserved for formal step-by-step solving; the right 25% is partitioned by a vertical red margin specifically for **Rough Working & Calculations**.
  3. Print the booklet and hand it to Tharun to solve with pen and paper under timed conditions.
