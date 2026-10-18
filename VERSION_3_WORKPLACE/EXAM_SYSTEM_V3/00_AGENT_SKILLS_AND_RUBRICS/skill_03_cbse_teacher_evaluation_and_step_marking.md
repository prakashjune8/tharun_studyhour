# SKILL 03: CBSE TEACHER EVALUATION & STEP-MARKING STANDARDS
## Official Spot-Evaluation Rubrics for Class 8 (Adaptable to Secondary & Senior Secondary)

**Document Code:** `SKILL-V3-03`  
**System Location:** `D:\THARUN PROJECT\VERSION_3_WORKPLACE\EXAM_SYSTEM_V3\00_AGENT_SKILLS_AND_RUBRICS\skill_03_cbse_teacher_evaluation_and_step_marking.md`  
**Standards Compliance:** CBSE Examination Manual for Evaluators, Spot-Evaluation Marking Directives  
**Target Student:** Tharun (Class 8 CBSE, Senthil Public School, Dharmapuri)  

---

### 1. CORE EVALUATION DOCTRINE OF CBSE TEACHERS

When correcting an answer script, an evaluator operates under three non-negotiable principles:
1. **Positive Marking**: Award marks for every scientifically, mathematically, or factually correct component written by the student. Do not penalize with arbitrary negative marks unless explicitly stipulated.
2. **Concept Over Verbatim Phrasing**: Do not demand rote replication of textbook sentences. If the core concept, technical keyword, or mechanism is correctly articulated using alternative valid terminology, award full marks.
3. **Step-Wise Fragmentation**: Never award a composite "0 out of 3" or "3 out of 3" without visibly breaking down where each fractional mark was gained or forfeited.

---

### 2. STEP-WISE MARKING RUBRIC FOR NUMERICALS (MATHS & SCIENCE)

Every numerical question in Mathematics or Physics/Chemistry is evaluated across four distinct cognitive stages:

#### Standard 3-Mark Numerical Breakdown:
| Step Stage | Operational Criterion | Mark Weight | Penalty on Error |
|:---|:---|:---:|:---|
| **Step 1: Given Data & Symbols** | Writing given values with correct variables and signs ($u, v, f, m, a, t$) | `0.5 Mark` | Omitting given data loses $0.5\text{M}$ |
| **Step 2: Formula & Principle** | Stating the governing equation in its standard form before numerical substitution | `0.5 Mark` | Incorrect formula results in $0$ for entire subsequent calculation |
| **Step 3: Substitution & Calculation** | Plugging numbers with proper sign conventions and executing algebraic operations | `1.0 Mark` | Arithmetic error with correct method loses only $0.5\text{M}$ (error carried forward principle) |
| **Step 4: Final Result & S.I. Unit** | Boxed/underlined final numerical value accompanied by mandatory SI unit ($\text{N}, \text{J}, \text{m/s}^2, \text{Pa}, \text{cm}^3$) | `1.0 Mark` | **Omitting SI unit or writing wrong unit loses $0.5\text{M}$ immediately!** |

#### Standard 5-Mark Multi-Stage Numerical Breakdown:
- **Given Data & Free-Body/Circuit Diagram**: `1.0 Mark`
- **Primary Formula & Derivation Step**: `1.5 Marks`
- **Intermediate Calculation Stage**: `1.0 Mark`
- **Final Numerical Solution + Statement + SI Unit**: `1.5 Marks`

---

### 3. VALUE-POINT EVALUATION IN THEORY QUESTIONS

For theoretical, conceptual, and descriptive questions, marks are awarded by counting **distinct, non-overlapping value points**:

#### Formula for Theory Marking:
$$\text{Marks Awarded} = \sum (\text{Valid Value Points}) \times (\text{Point Weight})$$

- **1-Mark Question**: Requires 1 distinct core definition or keyword.
- **2-Mark Question**: Requires **2 distinct value points** (or 4 sub-points of $0.5\text{M}$ each).
- **3-Mark Question**: Requires **3 distinct value points** (or 6 sub-points of $0.5\text{M}$ each).
- **5-Mark Question**: Requires **5 distinct value points** (or structured 3M explanation + 2M diagram/example).

#### Keyword Identification Protocol:
Evaluators look for mandatory NCERT technical vocabulary. If a student writes a paragraph explaining a concept in informal conversational language without the technical term, partial marks must be deducted:
- *Science Example*: In discussing cell division, writing "the cell cuts itself in two" instead of using the term **"binary fission"** loses $0.5\text{M}$.
- *Social Science Example*: In discussing 1857, writing "soldiers were forced to bite animal fat cartridges" without mentioning **"Enfield rifle cartridges greased with cow and pig fat violating religious sentiments"** loses keyword credit.

---

### 4. DIAGRAM EVALUATION & LABELING PROTOCOL

In Biology, Physics, and Geography, diagrams are graded as analytical constructs:

| Evaluation Component | Maximum Marks Allocation | Teacher Correction Standard |
|:---|:---:|:---|
| **Accurate Outline / Form** | `1.0 Mark` | Proportionate, clean, recognizable shape |
| **Directional Arrows / Rays** | `0.5 Mark` | For optics (incident/reflected rays) or flowcharts (blood circulation). **No arrows = 0 Marks for ray paths!** |
| **Correct Scientific Labels** | `0.5 Mark per label` | Typically 4 labels required for 2M, or 6 labels for 3M |
| **Neatness & Straight Rule Lines** | `0.5 Mark` | Label lines drawn horizontally with a ruler without crossing each other |

---

### 5. LANGUAGE EVALUATION CRITERIA (ENGLISH, TAMIL, HINDI)

Language answers are assessed across three orthogonal dimensions:

#### A. Writing Tasks (Letters, Paragraphs, Notices):
1. **Format (`1.0 Mark`)**: Sender address, date, receiver designation, subject, salutation, subscription.
2. **Content (`2.0 Marks`)**: Logical sequencing, completeness of prompt details, cause-and-effect development.
3. **Accuracy & Expression (`1.0 Mark`)**: Grammar, spelling, sentence variety, punctuation, appropriate tone.

#### B. Language Penalty Caps:
- **Spelling Mistakes**: Deduct $0.5\text{M}$ for every 2 major spelling errors (capped at a maximum penalty of $1.5\text{M}$ in a 5M question).
- **Tamil Specific**: Evaluators strictly penalize confusion between 'ண', 'ன', 'ந' and 'ல', 'ள', 'ழ'. Each persistent confusion point receives red-ink flagging.
- **Hindi Specific**: Evaluators flag 'मात्रा' errors (इ vs ई, उ vs ऊ), शिरोरेखा omission, and 'ण' vs 'न' spelling errors.

---

### 6. RED-INK ANNOTATION SYSTEM (FACE B SOFT-COPY GRADING)

The AI Evaluator (Gemini Face B) must output corrections utilizing standardized red-ink academic annotation symbols:

| Annotation Tag | Visual Indicator | Meaning / Teacher Remark |
|:---|:---:|:---|
| `[✓ +X.X]` | **Green/Red Checkmark** | Point accepted; marks awarded for valid step/keyword |
| `[✗ -X.X]` | **Red Cross** | Factually incorrect statement, wrong formula, or arithmetic slip |
| `[▲ KEYWORD MISSING]` | **Red Caret** | Concept understood but mandatory scientific/technical term omitted |
| `[UNIT MISSING -0.5]` | **Red Underline** | Numerical result is correct but SI unit is missing or wrong |
| `[STEP OMITTED]` | **Red Bracket** | Direct jump to final answer without showing working step |
| `[VAGUE PHRASING]` | **Wavy Underline** | Colloquial language used instead of academic prose |

---

### 7. MASTER SCORECARD & RESULT MATRIX

Every corrected script generated in `EXAM_SYSTEM_V3/05_CORRECTED_SOFT_COPIES/` must conclude with a structured evaluation summary:

```text
========================================================================================
                      CBSE SPOT EVALUATION SCORECARD - CLASS 8
========================================================================================
STUDENT NAME: Tharun                                    EXAM PHASE: Sunday Weekly Test
SUBJECT: Mathematics (Ganita Prakash)                   DATE OF EVALUATION: 18-Oct-2026
MAXIMUM MARKS: 35.0                                     MARKS SCORED: 31.5 / 35.0 (90.0%)
GRADE: A1 (Outstanding Mastery)                         STATUS: DAYDREAMING DISPROVED (VERIFIED)
----------------------------------------------------------------------------------------
SECTION-WISE PERFORMANCE BREAKDOWN:
  - SECTION A (MCQs / Recall):         5.0 /  5.0  (100%) - Flawless concept recognition
  - SECTION B (Very Short Answers):     5.5 /  6.0  ( 92%) - Minor step jump in Q7
  - SECTION C (Short Answers):          8.0 /  9.0  ( 89%) - Unit missing in Q10 (-0.5M)
  - SECTION D (Long Answers & Case):   13.0 / 15.0  ( 87%) - Incomplete reasoning in Q13(b)
----------------------------------------------------------------------------------------
CRITICAL TEACHER REMARKS:
1. Strong formula retention; algebraic identity manipulation is accurate.
2. Mandatory Fix: Always write the SI unit next to the final answer box (cost Tharun 0.5M in Q10).
3. In 5-mark proofs, write formal "Given", "To Prove", and "Proof" headers to prevent step loss.
========================================================================================
```
