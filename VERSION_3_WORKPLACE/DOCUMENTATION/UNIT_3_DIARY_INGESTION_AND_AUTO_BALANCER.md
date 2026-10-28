# UNIT 3: TAB 1 – SCHOOL DIARY HOMEWORK INGESTION & AUTO-BALANCING ENGINE

> **System Target**: ScholasticPulse – Tharun's Habit & Time Management Architect (Class 8 CBSE)  
> **Module Scope**: School diary ingestion, multi-format OCR parser (photos, Word, PDF, text), permanent task retention, and bag audit.  
> **Integration Mode**: Direct In-App Documentation Hub & Standalone Master User Manual.

---

## ## 3.1 Universal Multi-Format Diary Ingestion

Tab 1 (**School Diary**) provides a streamlined, 100% offline data entry pipeline that accepts Tharun's homework from Senthil Public School in any available format. It eliminates manual data entry friction while guaranteeing that every assigned task is parsed into structured data.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 📖 SCHOOL DIARY HOMEWORK INGESTION & OCR ENGINE                                         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  [ 📸 Upload Diary Photo / Scan ]   [ 📄 Upload Word / PDF ]   [ 📝 Manual Quick-Add ]  │
│                                                                                        │
│  Selected Date: [ 07/10/2026 ▾ ]                     Total Tasks Ingested: 4 Items     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  1. 🧮 Mathematics | Ch-7 Junction for UT | Written | 30 Mins       [✅ Done] [✏️] [🗑️]│
│  2. 🌐 Tamil       | இயல் - 1 குரு - 1, 2  | Written | 25 Mins       [✅ Done] [✏️] [🗑️]│
│  3. 🔬 Biology     | Ch-5 Q7-a,b          | Written | 15 Mins       [✅ Done] [✏️] [🗑️]│
│  4. 🧪 Chemistry   | Pg 12 Revision Zone  | Reading | 15 Mins       [✅ Done] [✏️] [🗑️]│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### ### 3.1.1 **📸 Upload Diary Photo / Scan** (Windows Native Offline WinOCR Engine)
* **Purpose**: Allows parents or Tharun to take a smartphone photo of the school diary handbook page and upload it directly. The native Windows OCR engine extracts handwritten and printed text with zero internet connection.
* **Workflow**:
  1. Click the button labeled **`📸 Upload Diary Photo / Scan`**.
  2. A Windows file selection dialog appears. Select any image file (`.jpg`, `.jpeg`, `.png`, `.bmp`).
  3. The internal **Universal Diary Importer** (`diary_importer.py`) executes:
     * It runs native Windows OCR (`winocr`) to recognize lines of text.
     * It auto-corrects orientation angles if the phone photo is tilted.
     * It parses subject markers (e.g., `Math:`, `Tamil:`, `Science:`, `Social:`, `English:`, `Hindi:`).
     * It extracts chapter names, question numbers, and estimated time tags.
  4. The recognized tasks are automatically converted into the standard JSON format and saved permanently in `tharun_diary_format.json`.
  5. The timetable immediately rebalances to allocate dedicated efficiency slabs for all detected subjects.

---

### ### 3.1.2 **📄 Upload Word Document (`.docx`) & PDF Ingestion**
* **Purpose**: Accepts digital homework sheets, weekly school circulars, or PDF teacher handouts sent by Senthil Public School.
* **Workflow**:
  1. Click **`📄 Upload Word / PDF`**.
  2. Select a `.docx`, `.doc`, or `.pdf` file from your computer.
  3. The parser extracts table rows, bullet points, and subject headers.
  4. A preview window displays the extracted items, allowing the user to verify subject tags and durations before committing.
  5. Click **`Commit to Timetable`** to merge the entries into today's active schedule.

---

### ### 3.1.3 **📝 Manual Quick-Add Diary Task Interface**

#### #### 3.1.3.1 Subject Dropdown, Task Description Field, Estimated Minutes, Task Type Toggle
* **Purpose**: Enables rapid manual typing of homework items when no camera or digital file is available.
* **Workflow**:
  1. Locate the **Manual Quick-Add Form** at the top of Tab 1.
  2. **Field 1: Subject Dropdown**: Click to select from the 7 standard CBSE subjects:
     * *Mathematics*, *Physical Science*, *Biological Science*, *Social Science*, *English*, *Hindi*, *Tamil*.
  3. **Field 2: Task Description**: Type the exact homework instruction (e.g., *“Ex 9.2 Questions 1 to 5 in Classwork notebook”*).
  4. **Field 3: Estimated Minutes**: Enter the estimated time required in minutes (e.g., `25`).
  5. **Field 4: Task Type Toggle**: Choose between:
     * **Written**: Triggers high-focus desk sprint with step-by-step solving.
     * **Reading**: Slotted for concept review, vocabulary memorization, or theory.
  6. Click **`➕ Add Task`**. The task is instantly saved to disk and appears in the daily schedule.

---

## ## 3.2 Permanent Homework Retention & Status Tracking

A core principle of ScholasticPulse is **Permanent Task Retention**. Completed homework items never vanish from the schedule into thin air; they remain permanently visible, marked with glowing green badges to provide a satisfying record of daily achievement.

---

### ### 3.2.1 Daily Homework Cards List & Date Switcher (Oct 06–19 Historical Log)
* **Purpose**: Allows Tharun and parents to review homework records across any date in the academic term.
* **Workflow**:
  1. On Tab 1, look at the **`Selected Date`** dropdown.
  2. Click the date selector to view any date in the historical database (e.g., `06/10/2026`, `07/10/2026`, up to the current date).
  3. The task list below instantly refreshes to display all assignments logged on that date, along with their completion status and estimated vs actual time spent.

---

### ### 3.2.2 The **✅ Done** Completion Badge (Permanent On-Screen Retention)
* **Purpose**: Reinforces student pride and dopamine reinforcement by keeping completed tasks visible throughout the evening.
* **Workflow**:
  1. When Tharun completes a homework task, he clicks the round checkbox or the **`✅ Done`** button on that task card.
  2. The task does **not** disappear. Instead:
     * The card background transitions to dark forest slate.
     * A vibrant green **`✅ Done`** badge appears on the card.
     * The task description text receives a clean strike-through line.
     * The time allocation is marked as successfully cleared in the daily audit.
  3. If accidentally clicked, clicking the badge again toggles the task back to pending state.

---

### ### 3.2.3 **🎒 School Bag Reminders & Lab Manual Audit** (Automatic 9:50 PM Trigger)
* **Purpose**: Eliminates next-morning school bag packing panic by extracting school item reminders from the diary and surfacing them in a dedicated 9:50 PM wind-down slot.
* **Workflow**:
  1. During diary ingestion, the parser automatically detects equipment phrases such as:
     * *"Bring Science practical record book without fail"*
     * *"Submit Geometry box and 30cm ruler tomorrow"*
     * *"Bring Tamil Classwork note for correction"*
  2. Instead of treating these as study homework, the app flags them as **Bag Audit Items**.
  3. At **9:50 PM**, the application surfaces the **School Bag & Materials Audit** card on the screen.
  4. Tharun inspects each highlighted item, physically packs it into his school bag, and checks off the reminder before the 10:00 PM bedtime curfew.
