# UNIT 4: TAB 2 – HOST EXAMINATION SUITE & CBSE 3-PHASE AGGREGATOR

> **System Target**: ScholasticPulse – Tharun's Habit & Time Management Architect (Class 8 CBSE)  
> **Module Scope**: The 3-tier intra-head study ledger, master curation strip, weekly filters, and the 3-phase automated examination aggregation pipeline.  
> **Integration Mode**: Direct In-App Documentation Hub & Standalone Master User Manual.

---

## ## 4.1 Subview 1: The 3-Tier Intra-Head Study Ledger

Subview 1 of Tab 2 houses the **Subject Study Ledger** (`exam_study_ledger_v3.py`). It acts as the intelligent bridge connecting daily completed homework with upcoming CBSE examinations. Every completed study slab is automatically classified into an exact cognitive taxonomy.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 📚 SUBVIEW 1: MASTER SUBJECT STUDY LEDGER & 3-TIER COGNITIVE TAXONOMY                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  [ 🌐 Full Month (68) ]  [ Week 1 (Oct 1-6) ]  [ Week 2 (Oct 7-13) ]  [ Week 3 ] [ W4 ]│
├────────────────────────────────────────────────────────────────────────────────────────┤
│  DATE       | SUBJECT     | CHAPTER / TOPIC                   | INTRA-HEAD CLASSIFIER  │
│  ───────────┼─────────────┼───────────────────────────────────┼──────────────────────  │
│  2026-10-17 | Mathematics | Mensuration: Cylinder & Trapezium | Head 2: Problem Solving│
│  2026-10-17 | Science     | Chemical Effects of Current       | Head 1: Core Concepts  │
│  2026-10-16 | Tamil       | இயல் - 1 இலக்கணம் (எழுத்து வகை)   | Head 3: Orthography    │
│  2026-10-15 | Social Sci  | Judiciary & Indian Constitution   | Head 1: Core Concepts  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### ### 4.1.1 Cognitive Taxonomy Categorization

Every study entry is categorized into one of three certified **Intra-Heads**:

#### #### 4.1.1.1 **Head 1: Core Concepts & Principles** (Theories, Laws, Definitions)
* **Purpose**: Identifies conceptual foundation knowledge. Triggered by keywords: `concept`, `rule`, `definition`, `law`, `reading`, `theory`, `learn`, `memorize`.
* **Exam Application**: In Phase 1 and Phase 3 exams, Head 1 units generate 1-mark objective questions, assertion-reasoning pairs, and 2-mark scientific definitions.

#### #### 4.1.1.2 **Head 2: Problem Solving & Applications** (Calculations, Exercises, Formula Steps)
* **Purpose**: Identifies active hand-solving units. Triggered by keywords: `exercise`, `solve`, `questions`, `ex:`, `sums`, `ch-`, `written`, `practice`.
* **Exam Application**: In exams, Head 2 units generate multi-step mathematical problems, algebraic equations, and numerical physics calculations requiring step-by-step working.

#### #### 4.1.1.3 **Head 3: Visual, Diagrammatic & Orthography** (Diagrams, Map Skills, Spelling)
* **Purpose**: Identifies spatial and orthographic skills. Triggered by keywords: `diagram`, `drawing`, `activity`, `map`, `handwriting`, `spelling`, `chart`.
* **Exam Application**: Generates labeled anatomical diagram questions, ray tracing, circuit construction, and language spelling remediation questions.

---

### ### 4.1.2 Master Curation Strip & Filtering

#### #### 4.1.2.1 **🌐 Full Month Ledger View** (All 68 Entries Across Oct 01–24)
* **Purpose**: Provides a macro overview of all academic study completed during the active month.
* **Workflow**:
  1. Click the first button on the curation strip: **`🌐 Full Month Ledger`**.
  2. The table loads all 68+ study entries logged from October 1 through October 24.
  3. Inspect the total syllabus coverage, verifying that all 7 CBSE subjects have received balanced attention.

#### #### 4.1.2.2 Weekly Filter Tabs: Week 1, Week 2, Week 3, Week 4
* **Purpose**: Allows granular inspection of specific weekly study cycles.
* **Workflow**:
  1. Click any weekly pill button:
     * **`Week 1 (Oct 1–6)`**: Baseline foundation homework.
     * **`Week 2 (Oct 7–13)`**: Pre-midterm units and diagram practice.
     * **`Week 3 (Oct 14–20)`**: Core geometry, mensuration, and physics revision.
     * **`Week 4 (Oct 21–24)`**: Final exam syllabus consolidation.
  2. The table filters immediately to display only study entries completed within those selected calendar dates.

---

## ## 4.2 The 3-Phase Host Examination Pipeline

The **Exam Phase Assembler** (`exam_phase_assembler_v3.py`) aggregates ledger data into three automated, pedagogically distinct exam formats:

```
[ Intra-Head Study Ledger Database ]
                  │
  ┌───────────────┼───────────────┐
  ▼               ▼               ▼
[ PHASE 1 ]     [ PHASE 2 ]     [ PHASE 3 ]
Weekly Sunday   Pre-Exam 3-Day  Exam Eve Morning
Test (35M/60m)  Checkpoint (25M)Sprint (25M/35m)
& Month-End     (Day % 3 == 0)  (06:40-07:15 AM)
Mega Exam (80M)
```

---

### ### 4.2.1 **Phase 1**: Weekly Sunday Test (35M, 60m) & Month-End Mega Exam (80M, 180m)
* **Purpose**: Replicates formal CBSE examination sittings to build Tharun's exam endurance and time management.
* **Weekly Sunday Test Specifications**:
  * **Scope**: Aggregates the 6 preceding days of homework (Monday through Saturday).
  * **Structure**: 35 Total Marks, 60 Minutes duration.
  * **Sections**:
    * Section A: Objective & Core Definitions (10 Marks).
    * Section B: Short Answer Problem Solving (15 Marks).
    * Section C: Comprehensive Long Problem / Diagram (10 Marks).
* **Month-End Mega Exam Specifications**:
  * **Scope**: Combines all 4 weeks of the month across all 7 subjects (Oct 01–24).
  * **Structure**: Official CBSE Term 1 blueprint: 80 Total Marks, 180 Minutes (3 Hours).
  * **Partitioning**:
    * Section A: Mathematics Core Hand-Solving (20 Marks).
    * Section B: Science (Physics 10M, Biology 10M).
    * Section C: Social Science (History, Civics, Geography 20M).
    * Section D: Languages (Tamil 10M, Hindi 5M, English 5M).

---

### ### 4.2.2 **Phase 2**: Pre-Exam 3-Day Checkpoint Examination (`Day % 3 == 0`, 25M)
* **Purpose**: Anti-forgetting checkpoint based on Ebbinghaus' spaced repetition curve. Triggered every 3 days (`Day % 3 == 0`) to test retention before the student moves to new chapters.
* **Workflow & Specifications**:
  * **Modulo Trigger**: Automatically calculates the 3-day block window:
    $$\text{Start Day} = (\text{block} - 1) \times 3 + 1, \quad \text{End Day} = \text{block} \times 3$$
  * **Structure**: 25 Total Marks, 45 Minutes duration.
  * **Focus**: Targeted audit of the specific formulas, laws, and exercises practiced during those exact 3 days.

---

### ### 4.2.3 **Phase 3**: Exam Eve Morning Retention Sprint (06:40 AM – 07:15 AM, 25M)
* **Purpose**: Executed on the morning of a school exam between **06:40 AM and 07:15 AM**. Acts as a high-yield mental primer before Tharun boards the school bus.
* **Workflow & Specifications**:
  * **Structure**: 25 Total Marks, 35 Minutes duration.
  * **Content**: 100% focused on high-yield recall:
    * 5 Essential Mathematical Formulas.
    * 5 Crucial Scientific Laws & Definitions.
    * 2 Blind Diagram Outlines with proper labeling.
    * Zero heavy calculations; strictly designed to stimulate cognitive recall and boost confidence before entering the school hall.
