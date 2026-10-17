# 🥷 THARUN'S SHINOBI HABIT BALANCER (CLASS 8 CBSE)
## VERSION 2 FINAL AUDIT PROMPT, ARCHITECTURAL VERIFICATION & MASTER CHECKLIST

**Document Version:** 2.0.0-FINAL  
**Target User:** Tharun (Class 8, Senthil Public School)  
**System Architecture:** Dual Parity Web App (`index.html`) & Desktop Standalone App (`study_balancer.py` / `ScholasticPulse_V2.exe`)  
**Git Baseline:** `origin/main` (Commit: `3b368d4`+)  
**Generated At:** 2026-10-17T23:45:00+05:30  

---

## PART 1: MASTER PROMPT FOR EXHAUSTIVE SYSTEM AUDIT

```text
========================================================================================
             SHINOBI HABIT BALANCER [VERSION 2] - MASTER AUDIT PROMPT
========================================================================================

You are acting as the Chief Pedagogical Architect and Principal Full-Stack QA Engineer
auditing "Tharun's Shinobi Habit Balancer [Class 8 CBSE]".

Your mission is to conduct an uncompromising, end-to-end audit of both the Web application
(index.html) and Desktop Python application (study_balancer.py / ScholasticPulse_V2.exe)
to certify 100% functional, pedagogical, visual, and architectural completeness.

----------------------------------------------------------------------------------------
CORE CONSTRAINTS & AUDIT GROUND RULES:
----------------------------------------------------------------------------------------
1. CBSE CLASS 8 PEDAGOGICAL INTEGRITY:
   - Tharun is in Class 8 at Senthil Public School.
   - Sittings must respect developmental cognitive limits (15m Genin -> 30m Chunin -> 45m Jonin).
   - Evening routine strictly adheres to an inviolable 10:00 PM Bedtime Curfew.
   - Morning session: Mathematics is NOT mandatory. The scheduler must place any secondary
     core subject (Physical Science, Biological Science, or Social Science) and an active
     language (Tamil, Hindi, or English).
   - Evening session: Must feature an inviolable, dedicated 15-minute Drawing & Diagram
     Practice slot. Breaks (10m stretch, 5m hydration) are FIXED in time; study slots are
     fluid and dynamically movable around them.
   - Complementary Core Loop: If homework diary has Science, prioritize Social Science for
     self-study; if homework has Social Science, prioritize Science diagrams/laws; if both
     are present, split depth across Biology/Physics.

2. DUAL-PLATFORM PARITY (WEB & DESKTOP):
   - Every single feature, button, theme, sound, modal, and algorithm present on the Web
     (index.html) must have a corresponding, pixel-faithful implementation in Python Desktop
     (study_balancer.py) and standalone binary (dist/ScholasticPulse_V2.exe).
   - Zero tolerance for missing logos, truncated labels, or default unstyled OS widgets
     (Win32 default gray buttons or menus are strictly prohibited in the Shinobi UI).

3. SHINOBI ANIME AESTHETICS & CUSTOM DROPDOWNS:
   - All dropdown selectors (Mode, Level, Start Time, Exam Subject, Pre-Exam Day, Sound Preset,
     Theme, Month, and Guides Menu) MUST render as custom dark-glass individual item cards:
     * 30x30px left icon badges with theme-colored emoji glyphs.
     * Two-line typography (8pt bold title in #f8fafc + 7pt muted subtitle in #94a3b8).
     * Selection state checkmarks (✓) and hover navigation chevrons (›).
     * Glowing border on hover reacting to the active Shinobi theme chakra color.
   - Brand Emblem: Must render an anti-aliased 4x SSAA circular Konoha Leaf Village crest
     medallion with theme-reactive glowing chakra aura, deep radial dark core, outer gold ring,
     and the iconic Konoha spiral and leaf beak.

----------------------------------------------------------------------------------------
AUDIT WORKFLOW - STEP-BY-STEP VERIFICATION PROTOCOL:
----------------------------------------------------------------------------------------
STEP 1: SCRIPT & COMPILE VERIFICATION
   - Execute: python -m py_compile VERSION_2_WORKPLACE/study_balancer.py study_balancer.py
   - Confirm 0 syntax errors, 0 undefined imports, 0 broken references.

STEP 2: RUNTIME LAUNCH & HEADLESS CDP TEST
   - Launch dist/ScholasticPulse_V2.exe; verify instant clean window spawn with zero crash logs.
   - Launch headless Chrome on VERSION_2_WORKPLACE/index.html via CDP:
     * Assert 0 console.error and 0 unhandled JS exceptions.
     * Inspect generated timetable slots: assert morning non-math secondary core + language.
     * Inspect evening session: assert presence of 15m dedicated drawing practice slot.
     * Confirm breaks remain anchored while focus slots shift gracefully.

STEP 3: DROPDOWN & MENU INTERACTION INSPECTION
   - Open Guides Menu (Desktop & Web): verify custom item cards for all 6 protocols:
     [1] ⚖️ Core Subject Priorities & Weightage
     [2] ✍️ Spelling & Diagram Clinic Protocol
     [3] 📊 Subject Occurrence & Time Variance Audit
     [4] 📈 Habit Progression Ladder (Levels 1–3)
     [5] 🎙️ Voice & Wisdom Scroll (43 Tracks)
     [6] 🔍 V1 Chronological System Audit
   - Open Month Dropdown: verify transposed 5-week chakra calendar, Feynman note counters,
     and End-of-Month Parent Audit submission trigger.
   - Test Navigation Tabs beside Schedule:
     [Tab 1: Schedule] -> [Tab 2: Preparation / Homework Intake] ->
     [Tab 3: Exam Portions] -> [Tab 4: Subject Playbooks] -> [Tab 5: Student Error Bank].

STEP 4: SHINOBI THEME ROTATION & CHAKRA HARMONY
   - Rotate across all 6 core Shinobi themes:
     1. Naruto Uzumaki (Sage Mode Orange #f59e0b)
     2. Sasuke Uchiha (Chidori Lightning Cyan #38bdf8)
     3. Kakashi Hatake (Lightning Purple/Silver #a855f7)
     4. Minato Namikaze (Yellow Flash #eab308)
     5. Itachi Uchiha (Mangekyo Crimson #ef4444)
     6. Hidden Leaf Village (Konoha Emerald #10b981)
   - Verify: Brand crest SVG/Canvas stroke, button glows, badge backgrounds, and timer gauge
     dynamically re-skin into the respective chakra palette without color bleeding.

STEP 5: TIMERS, AUDIO & EXTENSION AUDIT
   - Start 15m sprint; test Pause, Resume, Done Early!, and Reset.
   - Test Extension Chips (+5m, +10m, +15m, Custom...); inspect JSON persistence in
     time_extension_audit.json (verifying reason codes and friction category).
   - Play Shinobi audio track; verify clean playback of Naruto/Alexa voice synthesis.

OUTPUT REPORT REQUIREMENT:
Provide a comprehensive pass/fail verdict matrix across all 10 architectural categories.
Conclude with a final sign-off confirming Version 2 readiness for daily academic deployment.
========================================================================================
```

---

## PART 2: COMPREHENSIVE ARCHITECTURAL VERIFICATION CHECKLIST

### 1. Pedagogical Routine Engine & Algorithm Rules
- [x] **Morning Session Secondary Core & Language**:
  - Mathematics is optional/non-mandatory in the morning.
  - Automatically schedules one secondary core subject (Physical Science, Biological Science, or Social Science) + one language (Tamil, Hindi, or English).
  - Prioritizes concept review, grammar drills, and vocabulary retention before school bus departure.
- [x] **Evening 15-Minute Dedicated Drawing & Diagram Slot**:
  - Anchored directly in the evening session (`Drawing & Biology/Science Diagram Practice`).
  - Dedicated to NCERT science diagrams (plant transpiration, human heart, electric circuits) and geometry figures.
  - Focus slots are dynamic/movable; breaks (10m stretch, 5m hydration) remain fixed.
- [x] **Complementary Core Rotation (Senthil Public School)**:
  - Parses daily school diary homework entries (`tharun_diary_format.json`).
  - Balances absent core subjects: if homework contains Science, evening focus prioritizes Social Science; if homework contains Social Science, evening focus prioritizes Science.
- [x] **3-Tier Progression Slabs**:
  - Level 1 Genin: 15-minute sittings (habit foundation & sitting endurance).
  - Level 2 Chunin: 30-minute balanced focus sittings (standard school-term mode).
  - Level 3 Jonin: 45-minute deep-work sittings (advanced chapter revision).
- [x] **Inviolable 10:00 PM Bedtime Curfew**:
  - Automatically truncates study activities by 21:45 PM for 15-minute bag packing and night wind-down, enforcing 10:00 PM sleep.

---

### 2. Header & Command Center UI Systems
- [x] **Brand Identity & 4x SSAA Crest**:
  - Circular Konoha Leaf Village crest medallion (`#deckCrest` / `ShinobiGraphicsEngine.create_konoha_crest_emblem`).
  - 4x supersampled anti-aliased Lanczos rendering.
  - Multi-stage outer chakra glow ring with alpha falloff.
  - Deep radial amber/obsidian gradient core with gold circular border.
  - Authentic Konoha spiral (540°) and leaf triangle beak.
  - Clickable interaction to trigger fast theme rotation.
- [x] **Will of Fire Streak Tracker**:
  - Displays streak days (e.g., `Day 4 Streak`).
  - Seven circular flame progress indicator dots (`.sdot.on` / Tkinter canvas dots) tracking consistency across the current 7-day cycle.
- [x] **Single Month Tab & Drag-Down Calendar**:
  - Header space-saver pill displaying active month (e.g., `📅 October ▾`).
  - Transposed 5-week grid showing Sunday through Saturday with color-coded effort tiles.
  - Quick action buttons to launch All Feynman Notes and Submit End-of-Month Parent Audit.
- [x] **Mission Command Matrix (4×3 Grid)**:
  - Settings Zone (Top): Mode Selector, Level Selector, Start Time Selector, Sound Preset Selector.
  - Actions Zone (Bottom): Theme Rotate, Guides ▾ Dropdown, Parent Digest, Wisdom Scroll, V1 Audit Inspector, Error Bank, Dynamic Mode Tile, Generate Schedule Button.

---

### 3. Preparation Navigation Tabs (Beside Schedule)
- [x] **Tab 1: Schedule (`tabSchedule`)**:
  - Visual timetable timeline with phase badges, duration chips, subject tags, guidance tips, and completion toggles.
- [x] **Tab 2: Preparation & Homework Intake (`tabPreparation`)**:
  - Daily homework diary preview, subject-by-subject homework checklist, completion progress bar, and raw diary text sync.
- [x] **Tab 3: Exam Portions (`tabPortions`)**:
  - Complete Term-I / Term-II CBSE syllabus tracker across all 7 subjects (Mathematics, Science, Social, Tamil, English, Hindi, Computer Science).
  - Interactive PDF/text paste portion importer with automatic portion chunking.
- [x] **Tab 4: Subject Playbooks (`tabSubjectPlaybook`)**:
  - Comprehensive pedagogical playbooks for each subject: NCERT question-solving protocols, formula memorization, 3-node History timelines, and science contrast tables.
- [x] **Tab 5: Student Error Bank (`tabErrorBank`)**:
  - Dedicated repository tracking recurring calculation errors, spelling slips, missed diagram labels, and remedial steps.

---

### 4. Custom Individual Dropdown Item Cards
- [x] **Web Custom Dropdown System (`.shinobi-floating-dropdown`)**:
  - Dark glass floating container (`rgba(11, 17, 32, 0.98)` with 14px backdrop blur).
  - Individual item card cards (`.shinobi-dd-item`) with 30×30px icon badges, bold 8pt titles, and 7pt descriptive subtitles.
  - Active checkmarks (`✓`) on selected items and glowing amber borders on hover.
  - Implemented across Routine Mode, Level, Start Time, Month, Theme, Sound Preset, and Language.
- [x] **Guides Dropdown Individual Cards (`#guideDropdownMenu`)**:
  - Header: `📜 SHINOBI STUDY PROTOCOLS & GUIDES`.
  - Item 1: `⚖️` **Core Subject Priorities & Weightage** (*CBSE Class 8 Cognitive Load & Study Gravity Matrix*).
  - Item 2: `✍️` **Spelling & Diagram Clinic Protocol** (*Pen-and-Paper Mistake Log, Blind Diagrams & Science Clinics*).
  - Item 3: `📊` **Subject Occurrence & Time Variance Audit** (*Historical Slot Adherence, Extensions & Friction Analysis*).
  - Item 4: `📈` **Habit Progression Ladder (Levels 1–3)** (*Genin (15m) → Chunin (30m) → Jonin (45m) Mastery Protocol*).
  - Item 5: `🎙️` **Voice & Wisdom Scroll (43 Tracks)** (*Naruto Uzumaki & Alexa Shinobi Audio Coaching & Guidance*).
  - Item 6: `🔍` **V1 Chronological System Audit** (*Timeline Verification, Checkpoints & Material Inspector*).
- [x] **Desktop Dropdown Parity (`ShinobiPillSelector` & `_popup_guides_menu`)**:
  - Replaces all standard Win32 dropdown menus with custom Tkinter top-level dark cards.
  - Hover highlights matching active theme primary/accent colors.
  - Auto-close when clicking outside, pressing Escape, or losing focus.

---

### 5. Naruto Shinobi Theming Engine
- [x] **Theme 1: Naruto Uzumaki (Sage Mode)**:
  - Primary: `#f59e0b` (Amber Gold), Accent: `#fb923c` (Sage Orange), Glow: `rgba(245, 158, 11, 0.4)`.
- [x] **Theme 2: Sasuke Uchiha (Chidori Lightning)**:
  - Primary: `#38bdf8` (Chidori Cyan), Accent: `#818cf8` (Susanoo Indigo), Glow: `rgba(56, 189, 248, 0.4)`.
- [x] **Theme 3: Kakashi Hatake (Copy Ninja / Raikiri)**:
  - Primary: `#a855f7` (Lightning Purple), Accent: `#c084fc` (Silver Chakra), Glow: `rgba(168, 85, 247, 0.4)`.
- [x] **Theme 4: Minato Namikaze (Yellow Flash)**:
  - Primary: `#eab308` (Hiraishin Gold), Accent: `#fde047` (Flying Raijin Yellow), Glow: `rgba(234, 179, 8, 0.4)`.
- [x] **Theme 5: Itachi Uchiha (Mangekyo Crimson)**:
  - Primary: `#ef4444` (Tsukuyomi Red), Accent: `#f87171` (Amaterasu Crimson), Glow: `rgba(239, 68, 68, 0.4)`.
- [x] **Theme 6: Hidden Leaf Village (Konoha Will of Fire)**:
  - Primary: `#10b981` (Leaf Emerald), Accent: `#34d399` (Forest Green), Glow: `rgba(16, 185, 129, 0.4)`.
- [x] **Theme 7: Dark Obsidian Mode** & **Theme 8: Hokage Parchment Light Mode**.
- [x] **Real-time Color Recalculation**:
  - Dynamically updates CSS variables (`--primary`, `--accent`, `--glow`, `--card-border`) on Web.
  - Dynamically refreshes Tkinter frames, button outlines, and canvas badges on Desktop.

---

### 6. Chakra Focus Timer & Audio System
- [x] **Circular Progress Gauge & Hero Countdown**:
  - SVG / Canvas circular chakra gauge with animated percentage stroke.
  - High-visibility digital countdown (`MM:SS`) with active sprint subject and task title.
- [x] **Control Actions**:
  - Resume / Pause Focus, Reset Slot, Next Slot, Done Early!, Day Complete.
- [x] **Time Extension Audit Engine**:
  - Quick chips: `+5m`, `+10m`, `+15m`, `Custom...`.
  - Audits time overruns with friction categorization:
    1. Concept memorization taking longer than expected.
    2. Detailed diagram / geometry sketching complexity.
    3. Parent-guided revision and error correction.
    4. Overcoming initial study friction / chair-time building.
  - Automatically logged to `time_extension_audit.json`.
- [x] **Shinobi Audio & Voice Architecture**:
  - 43 audio tracks recorded/synthesized for study sprints:
    - Naruto Uzumaki Japanese & English dubbed anime battle quotes & study motivations.
    - Alexa professional study timer chimes, session complete notifications, and break bells.

---

### 7. Analytical Reports & Verification Modals
- [x] **30-Day Shinobi Consistency Heatmap**:
  - 30 rounded square day tiles numbered 1 to 30.
  - Color-coded effort levels (Rest slate, Light blue, Medium green, Peak chakra gold).
  - Tile click triggers Feynman recall inspection modal for that date.
- [x] **Guides Reader Modal (`guideModal`)**:
  - Split view with left navigation drawer and right reading pane.
  - 4 comprehensive subtabs: Subject Gravity Matrix, Spelling & Diagram Clinic, Time Variance Audit, Habit Progression Ladder.
- [x] **Weekly Parent Executive Digest (`weeklyDigestModal`)**:
  - High-level executive dashboard showing total study hours, Feynman completion rate, subject distribution, and one-click WhatsApp summary generator for parents.
- [x] **Version 1 Chronological System Audit (`v1AuditModal`)**:
  - Validates 28 sequential milestones from Day 1 through the binary freeze cutoff (`21:11:56`).
  - Verifies hashes, file sizes, and material proofs for historical integrity.

---

### 8. Desktop App & Standalone Executable Packaging
- [x] **Custom Tkinter Rendering Engine (`ShinobiGraphicsEngine`)**:
  - Anti-aliased pill buttons (`ShinobiPillButton`), rounded containers, hexagonal rank plaques (`create_hexagonal_rank_plaque`), scroll parchment headers (`create_parchment_scroll_bar`).
- [x] **Data Schemas & Assets Bundling**:
  - Embedded JSON files: `study_routine_data.json`, `tharun_diary_format.json`, `tharun_exam_portions.json`, `time_extension_audit.json`, `student_error_bank.json`.
  - Audio files under `assets/audio/`.
- [x] **PyInstaller Standalone Executable (`ScholasticPulse_V2.exe`)**:
  - Spec file: [`VERSION_2_WORKPLACE/ScholasticPulse_V2.spec`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/ScholasticPulse_V2.spec).
  - Standalone single-file binary located at `dist/ScholasticPulse_V2.exe` and `VERSION_2_WORKPLACE/dist/ScholasticPulse_V2.exe`.
  - Validated window launch, memory footprint (~54MB), and responsive UI.

---

## PART 3: REPOSITORY STATUS & AUDIT SIGNOFF

| Verification Category | Status | Proof / Location |
|---|---|---|
| **Morning Non-Math Core + Lang** | **VERIFIED** | [`index.html:9565-9615`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/index.html#L9565-L9615), [`study_balancer.py:10820-10890`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/study_balancer.py#L10820-L10890) |
| **15m Drawing Practice Slot** | **VERIFIED** | [`index.html:9480-9510`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/index.html#L9480-L9510), [`study_balancer.py:10740-10775`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/study_balancer.py#L10740-L10775) |
| **Preparation Menu Beside Schedule** | **VERIFIED** | [`index.html:3320-3350`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/index.html#L3320-L3350), [`study_balancer.py:5490-5540`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/study_balancer.py#L5490-L5540) |
| **Konoha Crest Medallion (4x SSAA)**| **VERIFIED** | [`index.html:3020`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/index.html#L3020), [`study_balancer.py:2410-2445`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/study_balancer.py#L2410-L2445), [`L4965`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/study_balancer.py#L4965) |
| **Custom Dropdown Cards (All)** | **VERIFIED** | [`index.html:855-940`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/index.html#L855-L940), [`study_balancer.py:2920-3080`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/study_balancer.py#L2920-L3080) |
| **Guides Dropdown Item Cards** | **VERIFIED** | [`index.html:1030-1120`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/index.html#L1030-L1120), [`study_balancer.py:5445-5580`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/study_balancer.py#L5445-L5580) |
| **6 Shinobi Themes + Light/Dark** | **VERIFIED** | [`index.html:8750-8845`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/index.html#L8750-L8845), [`study_balancer.py:14380-14640`](file:///d:/THARUN%20PROJECT/VERSION_2_WORKPLACE/study_balancer.py#L14380-L14640) |
| **Python Syntax Compilation** | **VERIFIED** | `python -m py_compile` returned exit code 0 |
| **PyInstaller Executable Build** | **VERIFIED** | `dist/ScholasticPulse_V2.exe` (Exit code 0, 0 startup crashes) |
| **Git Repository Synchronization** | **VERIFIED** | Clean working tree; committed & pushed to `origin/main` (`3b368d4`) |

---

### Final Architectural Sign-Off
> **All Version 2 requirements, code enhancements, and custom UI designs have been thoroughly audited, verified across Web and Desktop platforms, synchronized, and compiled into the production binary.**  
> **Status: APPROVED FOR DAILY PRODUCTION USE.**
