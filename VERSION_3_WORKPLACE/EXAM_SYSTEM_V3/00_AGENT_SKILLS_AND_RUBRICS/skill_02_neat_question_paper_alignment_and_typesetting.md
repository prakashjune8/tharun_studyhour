# SKILL 02: NEAT QUESTION PAPER ALIGNMENT & TYPESETTING BLUEPRINT
## Institutional Page Geometry, Mathematical Notation & Universal Print Specifications

**Document Code:** `SKILL-V3-02`  
**System Location:** `D:\THARUN PROJECT\VERSION_3_WORKPLACE\EXAM_SYSTEM_V3\00_AGENT_SKILLS_AND_RUBRICS\skill_02_neat_question_paper_alignment_and_typesetting.md`  
**Standards Compliance:** CBSE Board Paper Layout Conventions, ISO A4 Standards, High-DPI Print Grid  
**Target Student:** Tharun (Class 8 CBSE, Senthil Public School, Dharmapuri)  

---

### 1. PAGE GEOMETRY & TYPOGRAPHIC HIERARCHY (A4 STANDARD)

Every generated question paper must render identically across the in-app Web viewer, desktop preview, and printed physical hard copy:
- **Paper Size**: Standard ISO A4 ($210\text{ mm} \times 297\text{ mm}$).
- **Margins**:
  - Top: $16\text{ mm}$ ($45\text{ pt}$)
  - Bottom: $16\text{ mm}$ ($45\text{ pt}$)
  - Left: $18\text{ mm}$ ($51\text{ pt}$) — provides gutter for paper clip / binder punching.
  - Right: $16\text{ mm}$ ($45\text{ pt}$).
- **Body Font Family**: `"Times New Roman", "DejaVu Serif", "STIX Two Text", serif` for official academic layout; `"Segoe UI", "Arial", sans-serif` for clean high-DPI monitor reading.
- **Base Font Size**: $10.5\text{ pt}$ on $14\text{ pt}$ line leading.

---

### 2. INSTITUTIONAL HEADER BLOCK & METADATA GRID

The top of every question paper must feature a standardized 4-tier institutional block:

```text
+--------------------------------------------------------------------------------------------------+
|                            SENTHIL PUBLIC SCHOOL - DHARMAPURI                                    |
|                        AFFILIATED TO CBSE, NEW DELHI (AFFL. NO. 1930248)                         |
|                    SCHOLASTIC ACADEMIC EVALUATION & HOST EXAMINATION SYSTEM                      |
+--------------------------------------------------------------------------------------------------+
|  EXAM PHASE: [SUNDAY WEEKLY TEST / MONTH-END MEGA / 3-DAY CHECKPOINT / MORNING SPRINT]           |
|  CLASS: CLASS 8 (CBSE)                                            DATE: DD-MM-YYYY               |
|  SUBJECT: [MATHEMATICS / SCIENCE / SOCIAL / LANGUAGES]            ROLL NO: ....................  |
|  TIME ALLOWED: [45 MINS / 60 MINS / 120 MINS]                     MAXIMUM MARKS: [25 / 35 / 80]  |
+--------------------------------------------------------------------------------------------------+
```

#### Exact HTML / CSS Construction:
```html
<div class="exam-header-block">
  <div class="inst-title">SENTHIL PUBLIC SCHOOL, DHARMAPURI</div>
  <div class="inst-subtitle">CBSE ACADEMIC AFFILIATION NO. 1930248 • HOST EXAMINATION SYSTEM</div>
  <div class="exam-type-pill">HOST-CONDUCTED ACADEMIC RETENTION & ANTI-DAYDREAMING TEST</div>
  
  <div class="exam-meta-grid">
    <div class="meta-cell text-left"><strong>CLASS:</strong> CLASS 8 (CBSE)</div>
    <div class="meta-cell text-center"><strong>SUBJECT:</strong> <span class="sub-name">MATHEMATICS</span></div>
    <div class="meta-cell text-right"><strong>DATE:</strong> 18-OCT-2026</div>
    <div class="meta-cell text-left"><strong>TIME ALLOWED:</strong> 60 MINUTES</div>
    <div class="meta-cell text-center"><strong>PHASE:</strong> WEEK 3 SUNDAY TEST</div>
    <div class="meta-cell text-right"><strong>MAX. MARKS:</strong> 35 MARKS</div>
  </div>
</div>
```

---

### 3. GENERAL INSTRUCTIONS ACCREDITATION BOX

Directly beneath the header grid sits the boxed **General Instructions**:
- Enclosed in a crisp border with padding.
- Numbered explicitly with bold keywords:

```text
+--------------------------------------------------------------------------------------------------+
| GENERAL INSTRUCTIONS:                                                                            |
| 1. Read all questions carefully before attempting.                                               |
| 2. This question paper consists of 15 questions divided into 4 Sections: A, B, C, and D.         |
| 3. Section A (Q1 to Q5) contains Multiple Choice Questions carrying 1 mark each.                |
| 4. Section B (Q6 to Q8) contains Very Short Answer questions carrying 2 marks each.             |
| 5. Section C (Q9 to Q11) contains Short Answer questions carrying 3 marks each.                 |
| 6. Section D (Q12 to Q14) contains Long Answer & Case-Based questions carrying 5 marks each.     |
| 7. All questions are compulsory. Internal choices are provided in selected questions.            |
| 8. Step-wise calculations, formulas, and SI units are mandatory for numerical questions.         |
| 9. Rough work must be done on the dedicated margin on the right side of the answer sheet.        |
+--------------------------------------------------------------------------------------------------+
```

---

### 4. RIGID RIGHT-ALIGNED MARK BRACKET SPECIFICATION

- Every question and sub-part must position its mark allocation flush against the right-hand margin.
- Brackets must be bracketed Arabic integers: `[1]`, `[2]`, `[3]`, `[4]`, or `[5]`.
- For multi-part questions, sub-part marks must be indented and right-aligned:

```text
Q.12  (a) State the Law of Conservation of Energy with an example.                     [2]
      (b) A boy applies a horizontal force of 25 N to drag a 10 kg wooden crate across
          a classroom floor through a distance of 4 meters. Calculate the work done.    [2]
      (c) What happens to the work done if the force is applied perpendicular to the
          direction of motion? Explain.                                                [1]
```

#### CSS Flexbox Implementation:
```css
.question-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  page-break-inside: avoid;
}
.question-body {
  flex: 1;
  padding-right: 16px;
  text-align: justify;
}
.question-marks {
  font-weight: bold;
  white-space: nowrap;
  min-width: 32px;
  text-align: right;
  font-family: monospace;
}
```

---

### 5. SUB-QUESTION INDENTATION & BULLET HIERARCHY

To prevent nested text from spilling under question numbers, a strict hanging indentation grid is enforced:
- **Top-Level Question Number**: `Q.1`, `Q.2`, `Q.14` (Bold, Hanging indent `28px`).
- **First Sub-Part Level**: `(a)`, `(b)`, `(c)` (Indented by `36px`).
- **Second Sub-Part Level**: `(i)`, `(ii)`, `(iii)` (Indented by `54px`).
- **MCQ Option Grid**:
  - Horizontal 4-column row for short options:
    ```text
    (a) 10 N               (b) 20 N               (c) 30 N               (d) 40 N
    ```
  - Vertical indented stack for descriptive options:
    ```text
    (a) Friction increases with the increase in surface roughness.
    (b) Friction is completely independent of the normal reaction force.
    (c) Rolling friction is always greater than static friction.
    (d) Fluid friction can never be minimized by streamlining.
    ```

---

### 6. MATHEMATICAL FORMULAS, CHEMICAL EQUATIONS & TABLES

1. **Mathematical Equations**:
   - Clean formatting for algebraic expressions: $x^2 + 5x + 6 = 0$, $\frac{a}{b} = \frac{c}{d}$.
   - Centered derivations with clean SI unit definitions.
2. **Data Tables & Observation Grids**:
   - Solid borders, distinct headers, centered numerical data.
3. **Internal Choice ("OR") Separator**:
   ```text
   --------------------------------- OR ---------------------------------
   ```

---

### 7. DUAL EXPORT SPECIFICATIONS (HTML & REPORTLAB PDF)
- **HTML Print Studio**: Clean `@media print` rules removing UI buttons, headers, and nav bars.
- **ReportLab PDF Engine**: Vector-sharp, perfectly aligned A4 document generation with consistent font styles and zero wrapping artifacts.
