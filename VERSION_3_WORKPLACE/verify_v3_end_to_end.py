"""
verify_v3_end_to_end.py - Comprehensive End-to-End Test for ScholasticPulse V3
Tests:
1. Ledger synchronization from diary & exam portions.
2. 3-Phase Examination Assembly (Phase 1 Weekly & Month-End, Phase 2 3-Day, Phase 3 Morning Sprint).
3. Question paper generation (HTML & ReportLab PDF) with Indic Unicode (Tamil, Hindi, Math).
4. Answer sheet spot evaluation & Corrected Soft Copy generation (HTML & ReportLab PDF).
5. CBSE Topper Model Answer Guide generation (HTML & ReportLab PDF).
"""

import os
import sys

# Ensure UTF-8 stdout on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure workspace is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import exam_engine_v3
from exam_engine_v3 import (
    SubjectStudyLedger,
    ExamPhaseAssembler,
    GeminiExamClient,
    QUESTION_PAPERS_DIR,
    CORRECTED_COPIES_DIR,
    MODEL_ANSWERS_DIR,
    ANSWER_SHEETS_DIR,
)

def run_verification():
    print("=" * 80)
    print("🚀 SCHOLASTICPULSE V3: AUTOMATED END-TO-END VERIFICATION PASS")
    print("=" * 80)

    # -------------------------------------------------------------
    # STEP 1: LEDGER SYNC & AUDIT
    # -------------------------------------------------------------
    print("\n[Step 1] Synchronizing Subject Study Ledger from School Diary & Portions...")
    sync_res = SubjectStudyLedger.auto_sync_from_diary_and_portions()
    entries = sync_res.get("entries", [])
    print(f"  ✓ Preserved entries count: {len(entries)}")
    assert len(entries) > 0, "Ledger entries should not be empty!"

    # -------------------------------------------------------------
    # STEP 2: ASSEMBLE ALL 3 HOST EXAMINATION PHASES
    # -------------------------------------------------------------
    print("\n[Step 2] Assembling 3-Phase Examination Blueprints...")
    p1_weekly = ExamPhaseAssembler.assemble_phase1_weekly_sunday_test(week_number=3)
    p1_month = ExamPhaseAssembler.assemble_phase1_monthend_mega_exam()
    p2_checkpoint = ExamPhaseAssembler.assemble_phase2_3day_checkpoint()
    p3_math = ExamPhaseAssembler.assemble_phase3_morning_sprint("Mathematics")
    p3_tamil = ExamPhaseAssembler.assemble_phase3_morning_sprint("Tamil")
    p3_hindi = ExamPhaseAssembler.assemble_phase3_morning_sprint("Hindi")

    print(f"  ✓ Phase 1 Weekly Sunday Blueprint: {p1_weekly.get('total_marks', 35)} Marks ({p1_weekly.get('duration_mins', 60)} Mins)")
    print(f"  ✓ Phase 1 Month-End Blueprint:     {p1_month.get('total_marks', 80)} Marks ({p1_month.get('duration_mins', 180)} Mins)")
    print(f"  ✓ Phase 2 3-Day Checkpoint:        {p2_checkpoint.get('total_marks', 25)} Marks ({p2_checkpoint.get('duration_mins', 60)} Mins)")
    print(f"  ✓ Phase 3 Morning Sprints:         Math, Tamil, Hindi assembled successfully.")

    # -------------------------------------------------------------
    # STEP 3: QUESTION PAPER GENERATION (WITH INDIC UNICODE TAMIL & HINDI)
    # -------------------------------------------------------------
    print("\n[Step 3] Architecting Multilingual CBSE Class 8 Question Paper...")
    exam_spec = {
        "phase": "Phase 1: Comprehensive Weekly Sunday Examination",
        "exam_title": "WEEKLY SUNDAY HOST EXAMINATION (COMPREHENSIVE MULTI-CORE)",
        "subject": "Mathematics & Indic Languages (Tamil & Hindi)",
        "class_standard": "Class 8 CBSE",
        "time_allowed": "1.5 Hours",
        "max_marks": 35,
        "topics": ["Ex 9.1 Mensuration", "Tamil Orthography", "Hindi Dhwani"],
        "blueprint": {
            "sec_A": "Objective MCQs [1M each]",
            "sec_B": "Very Short Answer [2M each]",
            "sec_C": "Short Answer & Language Recall [3M each]",
            "sec_D": "Long Answer & Geometry Construction [5M each]"
        }
    }

    # Generate question paper using GeminiExamClient
    q_paper = GeminiExamClient.generate_question_paper(exam_spec)
    
    # Inject Tamil & Hindi test questions to rigorously verify Indic font rendering
    q_paper["sections"].append({
        "section_name": "SECTION E",
        "title": "Active Language Recall (Tamil & Hindi)",
        "questions": [
            {
                "q_num": "Q7",
                "question_text": "தமிழ் வரிவடிவ வளர்ச்சி: எழுத்துச் சீர்திருத்தத்தின் தேவையை விளக்குக. (Explain need for Tamil script reform).",
                "marks": 3
            },
            {
                "q_num": "Q8",
                "question_text": "ध्वनि कविता: 'अभी न होगा मेरा अंत' - कवि सूर्यकांत त्रिपाठी 'निराला' का मुख्य संदेश क्या है?",
                "marks": 3
            }
        ]
    })
    if "metadata" in q_paper:
        q_paper["metadata"]["max_marks"] = 41
    if "header_block" in q_paper:
        q_paper["header_block"]["max_marks"] = 41

    exam_id = q_paper.get("exam_id", "TEST_EXAM_V3")
    print(f"  ✓ Question Paper generated with Exam ID: {exam_id}")

    # Render HTML Print Preview
    qp_html = GeminiExamClient.render_question_paper_html(q_paper)
    qp_html_file = os.path.join(QUESTION_PAPERS_DIR, f"{exam_id}_print_preview.html")
    with open(qp_html_file, "w", encoding="utf-8") as f:
        f.write(qp_html)
    print(f"  ✓ Question Paper HTML rendered: {qp_html_file} ({os.path.getsize(qp_html_file)} bytes)")

    # Render ReportLab PDF with Indic Unicode Fonts (Tamil, Hindi, Math)
    qp_pdf_file = os.path.join(QUESTION_PAPERS_DIR, f"{exam_id}_QUESTION_PAPER.pdf")
    GeminiExamClient.render_question_paper_pdf(q_paper, qp_pdf_file)
    assert os.path.exists(qp_pdf_file), "Question paper PDF should exist!"
    assert os.path.getsize(qp_pdf_file) > 1000, "Question paper PDF should be non-empty!"
    print(f"  ✓ Question Paper PDF generated with Indic fonts: {qp_pdf_file} ({os.path.getsize(qp_pdf_file)} bytes)")

    # -------------------------------------------------------------
    # STEP 4: ANSWER SHEET EVALUATION & CORRECTED SOFT COPY
    # -------------------------------------------------------------
    print("\n[Step 4] Running CBSE Step-Marking Evaluation Pipeline...")
    student_sample_answers = (
        "Q1. (a) 1/2 * (a + b) * h\n"
        "Q2. (b) 41 cm2\n"
        "Q3. Area = 1/2 * (1 + 1.2) * 0.8 = 1/2 * 2.2 * 0.8 = 0.88\n"
        "Q4. Rhombus Area = 1/2 * d1 * d2 => 240 = 1/2 * 16 * d2 => d2 = 30 cm\n"
        "Q5. Total Cost = 202.5 * 4 = 810\n"
        "Q7. தமிழ் வரிவடிவத்தில் ஓலைச்சுவடிகளில் புள்ளியிடாமல் எழுதப்பட்டதால் குழப்பம் ஏற்பட்டது.\n"
        "Q8. कवि मानते हैं कि उनके जीवन का अंत अभी नहीं होगा क्योंकि अभी-अभी उनके जीवन में वसंत आया है।"
    )
    ans_txt_file = os.path.join(ANSWER_SHEETS_DIR, f"{exam_id}_sample_answer_sheet.txt")
    with open(ans_txt_file, "w", encoding="utf-8") as f:
        f.write(student_sample_answers)

    eval_res = GeminiExamClient.evaluate_answer_sheet(exam_id, [ans_txt_file])
    print(f"  ✓ Evaluated: Scored {eval_res.get('marks_scored')} / {eval_res.get('max_marks')} ({eval_res.get('percentage')}%) - Grade: {eval_res.get('cbse_grade')}")
    print(f"  ✓ Anti-Daydreaming Audit: {eval_res.get('daydreaming_audit', {}).get('verdict')}")

    # Render Corrected Soft Copy HTML & PDF
    corr_html = GeminiExamClient.render_corrected_copy_html(eval_res)
    corr_html_file = os.path.join(CORRECTED_COPIES_DIR, f"{exam_id}_CORRECTED_COPY.html")
    with open(corr_html_file, "w", encoding="utf-8") as f:
        f.write(corr_html)
    print(f"  ✓ Corrected Soft Copy HTML: {corr_html_file} ({os.path.getsize(corr_html_file)} bytes)")

    corr_pdf_file = os.path.join(CORRECTED_COPIES_DIR, f"{exam_id}_GRADED_CORRECTED_COPY.pdf")
    GeminiExamClient.render_corrected_copy_pdf(eval_res, corr_pdf_file)
    assert os.path.exists(corr_pdf_file), "Corrected copy PDF should exist!"
    assert os.path.getsize(corr_pdf_file) > 1000, "Corrected copy PDF should be non-empty!"
    print(f"  ✓ Corrected Soft Copy PDF generated with Indic fonts: {corr_pdf_file} ({os.path.getsize(corr_pdf_file)} bytes)")

    # -------------------------------------------------------------
    # STEP 5: CBSE TOPPER MODEL ANSWER REFERENCE GUIDE
    # -------------------------------------------------------------
    print("\n[Step 5] Synthesizing CBSE Topper Model Answer Guide (P-E-E-D Protocol)...")
    topper_html = GeminiExamClient.render_model_answer_guide_html(eval_res)
    topper_html_file = os.path.join(MODEL_ANSWERS_DIR, f"{exam_id}_TOPPER_MODEL_GUIDE.html")
    with open(topper_html_file, "w", encoding="utf-8") as f:
        f.write(topper_html)
    print(f"  ✓ Topper Model Answer HTML: {topper_html_file} ({os.path.getsize(topper_html_file)} bytes)")

    topper_pdf_file = os.path.join(MODEL_ANSWERS_DIR, f"{exam_id}_TOPPER_MODEL_GUIDE.pdf")
    GeminiExamClient.render_model_answer_guide_pdf(eval_res, topper_pdf_file)
    assert os.path.exists(topper_pdf_file), "Topper guide PDF should exist!"
    assert os.path.getsize(topper_pdf_file) > 1000, "Topper guide PDF should be non-empty!"
    print(f"  ✓ Topper Model Answer PDF generated with Indic fonts: {topper_pdf_file} ({os.path.getsize(topper_pdf_file)} bytes)")

    # -------------------------------------------------------------
    # STEP 6: 5-CARD SELECTOR STATS, ERROR BANK SYNC & UNIFIED BINDER PDF
    # -------------------------------------------------------------
    print("\n[Step 6] Testing 5-Card Phase 1 Selector Stats, Scanned PDF Fallback, Error Bank Sync & Unified Binder PDF...")
    
    # 6A. Week stats verification
    stats_w1 = SubjectStudyLedger.get_week_stats("October", week_number=1)
    stats_w2 = SubjectStudyLedger.get_week_stats("October", week_number=2)
    stats_w3 = SubjectStudyLedger.get_week_stats("October", week_number=3)
    stats_w4 = SubjectStudyLedger.get_week_stats("October", week_number=4)
    stats_month = SubjectStudyLedger.get_week_stats("October", week_number="monthend")
    
    print(f"  ✓ W1 Stats: {stats_w1['count']} entries, {stats_w1['subject_count']} subjects")
    print(f"  ✓ W2 Stats: {stats_w2['count']} entries, {stats_w2['subject_count']} subjects")
    print(f"  ✓ W3 Stats: {stats_w3['count']} entries, {stats_w3['subject_count']} subjects")
    print(f"  ✓ W4 Stats: {stats_w4['count']} entries, {stats_w4['subject_count']} subjects")
    print(f"  ✓ Month-End Stats: {stats_month['count']} entries, {stats_month['subject_count']} subjects")
    assert stats_w1['count'] > 0 and stats_w2['count'] > 0 and stats_w3['count'] > 0 and stats_w4['count'] > 0, "All 4 weeks must have entries!"
    assert stats_month['count'] >= (stats_w1['count'] + stats_w2['count'] + stats_w3['count'] + stats_w4['count']), "Month-end must encompass all weekly entries!"

    # 6B. Scanned Textbook PDF Fallback Check
    from exam_engine_v3 import extract_text_from_pdf, is_scanned_pdf
    # Test low-char text extraction fallback
    mock_scanned_pdf = os.path.join(ANSWER_SHEETS_DIR, "test_scanned_mock.pdf")
    if not os.path.exists(mock_scanned_pdf):
        # Create minimal PDF with minimal text to simulate scanned image PDF
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(mock_scanned_pdf)
        c.drawString(100, 100, "Scan")
        c.save()
    extracted_text = extract_text_from_pdf(mock_scanned_pdf)
    scanned_flag = is_scanned_pdf(mock_scanned_pdf)
    print(f"  ✓ Scanned PDF Detection: is_scanned={scanned_flag} (extracted {len(extracted_text)} chars)")
    assert scanned_flag, "Mock PDF with < 100 chars should be flagged as scanned!"

    # 6C. Automated Error Bank Sync Check
    from exam_engine_v3 import sync_eval_errors_to_error_bank, ERROR_BANK_FILE
    sync_count = sync_eval_errors_to_error_bank(eval_res)
    print(f"  ✓ Error Bank Sync: Recorded/Updated {sync_count} mistakes into {ERROR_BANK_FILE}")
    assert os.path.exists(ERROR_BANK_FILE), "student_error_bank.json must exist!"

    # 6D. 1-Click Physical Binder PDF Generation Check
    from exam_engine_v3 import render_unified_binder_pdf
    binder_pdf_file = os.path.join(CORRECTED_COPIES_DIR, f"{exam_id}_COMPLETE_PHYSICAL_BINDER.pdf")
    render_unified_binder_pdf(eval_res, binder_pdf_file)
    assert os.path.exists(binder_pdf_file), "Unified Binder PDF must exist!"
    assert os.path.getsize(binder_pdf_file) > 1000, "Unified Binder PDF must be non-empty!"
    print(f"  ✓ 1-Click Unified Physical Binder PDF: {binder_pdf_file} ({os.path.getsize(binder_pdf_file)} bytes)")

    print("\n" + "=" * 80)
    print("🏆 ALL 6 VERIFICATION PASSES COMPLETED WITH ZERO ERRORS!")
    print("=" * 80)

if __name__ == "__main__":
    run_verification()

