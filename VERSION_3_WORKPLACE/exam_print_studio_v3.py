"""
EXAM PRINT STUDIO (SESSION 5)
-----------------------------
High-precision document generation engine:
1. Official CBSE Vector Question Paper PDF (ReportLab + ARIALUNI.TTF).
2. Physical Blank Answer Sheet Booklet PDF (Standardized layout for student hand-writing).
3. Responsive Modern HTML Print Studio (CSS Grid, Print @media queries).
"""

import os
import sys
import html
from typing import Dict, Any, List, Optional
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib import colors

from exam_ground_truth_v3 import EXAM_SYSTEM_DIR
from exam_typography_engine_v3 import register_reportlab_indic_fonts, TextSanitizer, get_html_typography_css
from exam_math_fraction_engine_v3 import MathFractionEngine


class ExamPrintStudio:
    """
    Renders classroom-ready examination documents:
    Vector Question Paper PDF, Blank Answer Booklet PDF, and HTML Print Views.
    """

    @classmethod
    def render_question_paper_pdf(cls, paper: Dict[str, Any], output_pdf_path: str) -> str:
        """
        Compiles an official CBSE vector question paper PDF with Indic Unicode typography.
        """
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
        reg_font, bold_font = register_reportlab_indic_fonts()

        doc = SimpleDocTemplate(
            output_pdf_path,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=32,
            bottomMargin=32
        )

        styles = getSampleStyleSheet()

        # Styles
        school_style = ParagraphStyle(
            'SchoolHeader',
            fontName=bold_font,
            fontSize=13,
            leading=16,
            alignment=1, # Center
            textColor=colors.HexColor('#0f172a')
        )
        exam_title_style = ParagraphStyle(
            'ExamTitle',
            fontName=bold_font,
            fontSize=10,
            leading=13,
            alignment=1,
            textColor=colors.HexColor('#334155')
        )
        sub_info_style = ParagraphStyle(
            'SubInfo',
            fontName=reg_font,
            fontSize=8.5,
            leading=11,
            alignment=1,
            textColor=colors.HexColor('#475569')
        )
        instruction_style = ParagraphStyle(
            'Instructions',
            fontName=reg_font,
            fontSize=8,
            leading=11,
            textColor=colors.HexColor('#334155')
        )
        sec_header_style = ParagraphStyle(
            'SecHeader',
            fontName=bold_font,
            fontSize=9.5,
            leading=13,
            alignment=1,
            textColor=colors.HexColor('#ffffff')
        )
        q_num_style = ParagraphStyle(
            'QNum',
            fontName=bold_font,
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#0f172a')
        )
        q_text_style = ParagraphStyle(
            'QText',
            fontName=reg_font,
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#1e293b')
        )
        q_marks_style = ParagraphStyle(
            'QMarks',
            fontName=bold_font,
            fontSize=8.5,
            leading=12,
            alignment=2, # Right
            textColor=colors.HexColor('#0f172a')
        )

        elements = []
        meta = paper.get("metadata", {})
        subject = meta.get("subject", "Mathematics")
        time_mins = meta.get("time_allowed_mins", 20)
        max_marks = meta.get("max_marks", 15)
        exam_id = meta.get("exam_id", "EXAM-2026-V3")
        raw_title = meta.get("exam_title", "CBSE Examination")
        exam_title = TextSanitizer.sanitize_for_reportlab(raw_title)

        # 1. School Header Banner
        elements.append(Paragraph("THARUN REVISION BANNER", school_style))
        elements.append(Paragraph("CLASS 8 CBSE • DAILY RETENTION & HOST EXAMINATION ENGINE", sub_info_style))
        elements.append(Spacer(1, 3))
        elements.append(Paragraph(f"<b>{exam_title.upper()}</b>", exam_title_style))
        elements.append(Spacer(1, 4))

        # Metadata Details Bar Table
        meta_data = [
            [
                Paragraph(f"<b>Student:</b> Tharun", q_text_style),
                Paragraph(f"<b>Class:</b> Class 8 CBSE", q_text_style),
                Paragraph(f"<b>Subject:</b> {subject}", q_text_style),
                Paragraph(f"<b>Time:</b> {time_mins} Mins | <b>Max Marks:</b> {max_marks}", q_marks_style)
            ]
        ]
        t_meta = Table(meta_data, colWidths=[120, 100, 150, 152])
        t_meta.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(t_meta)
        elements.append(Spacer(1, 6))

        # Instructions Box
        instr_p = [
            [Paragraph("<b>General Instructions:</b> (1) All questions are compulsory. (2) Show neat step-by-step working and box final values. (3) Marks are indicated against each question.", instruction_style)]
        ]
        t_instr = Table(instr_p, colWidths=[522])
        t_instr.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fafaf9')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(t_instr)
        elements.append(Spacer(1, 8))

        # 2. Iterate Sections & Questions
        for sec in paper.get("sections", []):
            sec_name = sec.get("section_name", "SECTION")
            s_marks = sec.get("allocated_marks", "")
            s_label = f"{sec_name} ({s_marks} Marks)" if s_marks else sec_name

            # Section Header Bar
            t_sec = Table([[Paragraph(f"<b>{s_label}</b>", sec_header_style)]], colWidths=[522])
            t_sec.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1e293b')),
                ('PADDING', (0,0), (-1,-1), 3),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ]))
            elements.append(t_sec)
            elements.append(Spacer(1, 5))

            # Questions Table
            for q in sec.get("questions", []):
                q_num = q.get("question_number", "Q.")
                raw_txt = q.get("question_text", "")
                q_txt = MathFractionEngine.prettify_math_text(raw_txt) if subject == "Mathematics" else raw_txt
                q_m = q.get("marks", 1)
                raw_options = q.get("options", [])
                options = [MathFractionEngine.prettify_math_text(opt) if subject == "Mathematics" else opt for opt in raw_options]

                q_body = [Paragraph(f"{q_txt}", q_text_style)]
                if options:
                    opt_cells = []
                    # 2 options per row
                    for i in range(0, len(options), 2):
                        row = []
                        row.append(Paragraph(f"{options[i]}", q_text_style))
                        if i + 1 < len(options):
                            row.append(Paragraph(f"{options[i+1]}", q_text_style))
                        else:
                            row.append(Paragraph("", q_text_style))
                        opt_cells.append(row)
                    t_opts = Table(opt_cells, colWidths=[220, 220])
                    t_opts.setStyle(TableStyle([('PADDING', (0,0), (-1,-1), 2)]))
                    q_body.append(t_opts)

                q_row = [
                    [
                        Paragraph(f"<b>{q_num}</b>", q_num_style),
                        q_body,
                        Paragraph(f"<b>[{q_m}]</b>", q_marks_style)
                    ]
                ]
                t_q = Table(q_row, colWidths=[36, 446, 40])
                t_q.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('PADDING', (0,0), (-1,-1), 3),
                    ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#f1f5f9'))
                ]))
                elements.append(t_q)

            elements.append(Spacer(1, 6))

        # Footer divider
        elements.append(Spacer(1, 10))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1')))
        elements.append(Paragraph(f"Exam ID: {exam_id} • Senthil Public School Examination Division", sub_info_style))

        doc.build(elements)
        return output_pdf_path

    @classmethod
    def render_blank_answer_sheet_pdf(cls, paper: Dict[str, Any], output_pdf_path: str) -> str:
        """
        Compiles an official CBSE physical blank answer booklet with student top-sheet,
        pre-numbered answer slabs, and a teacher's evaluation column.
        """
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
        reg_font, bold_font = register_reportlab_indic_fonts()

        doc = SimpleDocTemplate(
            output_pdf_path,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=32,
            bottomMargin=32
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('Title', fontName=bold_font, fontSize=11, leading=14, alignment=1)
        sub_style = ParagraphStyle('Sub', fontName=reg_font, fontSize=8, leading=10, alignment=1)
        cell_style = ParagraphStyle('Cell', fontName=reg_font, fontSize=8.5, leading=11)
        b_cell_style = ParagraphStyle('BCell', fontName=bold_font, fontSize=8.5, leading=11)

        elements = []
        meta = paper.get("metadata", {})
        subject = meta.get("subject", "Mathematics")
        exam_id = meta.get("exam_id", "EXAM-2026-V3")
        max_marks = meta.get("max_marks", 15)
        raw_title = meta.get("exam_title", "CBSE Examination")
        exam_title = TextSanitizer.sanitize_for_reportlab(raw_title)

        # 1. Answer Booklet Cover Top-Bar
        elements.append(Paragraph("THARUN REVISION BANNER • CBSE OFFICIAL ANSWER BOOKLET", title_style))
        elements.append(Paragraph(f"{exam_title.upper()} • BLANK RESPONSE COPY", sub_style))
        elements.append(Spacer(1, 6))

        top_bar = [
            [
                Paragraph("<b>Student Name:</b> Tharun", cell_style),
                Paragraph("<b>Class / Sec:</b> Class 8 CBSE", cell_style),
                Paragraph(f"<b>Subject:</b> {subject}", cell_style)
            ],
            [
                Paragraph(f"<b>Exam ID:</b> {exam_id}", cell_style),
                Paragraph(f"<b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}", cell_style),
                Paragraph(f"<b>Max Marks:</b> {max_marks} | <b>Marks Scored:</b> ______", b_cell_style)
            ]
        ]
        t_top = Table(top_bar, colWidths=[174, 174, 174])
        t_top.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#0f172a')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('PADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        elements.append(t_top)
        elements.append(Spacer(1, 10))

        # Instructions line
        elements.append(Paragraph("<i>Write your answers strictly inside the allocated question slabs below. Show rough calculations in the margin.</i>", sub_style))
        elements.append(Spacer(1, 8))

        # 2. Pre-Numbered Answer Slabs
        for sec in paper.get("sections", []):
            sec_name = sec.get("section_name", "SECTION")
            elements.append(Paragraph(f"<b>--- {sec_name} ---</b>", ParagraphStyle('Sec', fontName=bold_font, fontSize=9, leading=12, alignment=1, textColor=colors.HexColor('#334155'))))
            elements.append(Spacer(1, 4))

            for q in sec.get("questions", []):
                q_num = q.get("question_number", "Q.")
                raw_txt = q.get("question_text", "")
                q_txt = MathFractionEngine.prettify_math_text(raw_txt) if subject == "Mathematics" else raw_txt
                q_m = q.get("marks", 1)
                
                # Height scales with marks (1M = 50pt, 2M = 85pt, 3M = 125pt, 5M = 190pt)
                slab_height = 50 if q_m == 1 else (85 if q_m == 2 else (125 if q_m == 3 else 190))

                if subject == "Mathematics" and q_m >= 2:
                    # Specialized 75% Step-Solving + 25% Rough Work Column
                    step_content = [
                        Paragraph(f"<b>{q_num} [{q_m}M]</b>: {q_txt}", b_cell_style),
                        Paragraph("<i>Step-by-Step Formula & Working Steps:</i>", ParagraphStyle('Wk', fontName=reg_font, fontSize=7.5, textColor=colors.HexColor('#94a3b8'))),
                        Spacer(1, slab_height - 45),
                        Paragraph("┌────────────────────────────┐<br/>│ Final Answer Box:          │<br/>└────────────────────────────┘", ParagraphStyle('Bx', fontName=reg_font, fontSize=6.5, leading=8, textColor=colors.HexColor('#64748b')))
                    ]
                    rough_content = [
                        Paragraph("<b>ROUGH COLUMN</b>", ParagraphStyle('Rh', fontName=bold_font, fontSize=6.5, leading=8, alignment=1, textColor=colors.HexColor('#94a3b8'))),
                        Paragraph("<i>Scratch / Multiplications</i>", ParagraphStyle('Rs', fontName=reg_font, fontSize=6, leading=7, alignment=1, textColor=colors.HexColor('#cbd5e1')))
                    ]
                    slab_row = [[step_content, rough_content]]
                    t_slab = Table(slab_row, colWidths=[390, 132], rowHeights=[slab_height])
                    t_slab.setStyle(TableStyle([
                        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
                        ('LINEBEFORE', (1,0), (1,-1), 1, colors.HexColor('#cbd5e1')),
                        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#ffffff')),
                        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#fafaf9')),
                        ('VALIGN', (0,0), (-1,-1), 'TOP'),
                        ('PADDING', (0,0), (-1,-1), 4),
                    ]))
                else:
                    # Standard Slab
                    slab_row = [
                        [
                            Paragraph(f"<b>{q_num}</b><br/>[{q_m}M]", b_cell_style),
                            Paragraph(f"<b>{q_txt}</b><br/><i>Student Response:</i>", ParagraphStyle('Wk', fontName=reg_font, fontSize=7.5, textColor=colors.HexColor('#94a3b8'))),
                            Paragraph("<b>Marks:</b><br/>____ / " + str(q_m), ParagraphStyle('Mk', fontName=bold_font, fontSize=7.5, leading=10, alignment=1))
                        ]
                    ]
                    t_slab = Table(slab_row, colWidths=[40, 422, 60], rowHeights=[slab_height])
                    t_slab.setStyle(TableStyle([
                        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
                        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
                        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f1f5f9')),
                        ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#f8fafc')),
                        ('VALIGN', (0,0), (-1,-1), 'TOP'),
                        ('PADDING', (0,0), (-1,-1), 4),
                    ]))

                elements.append(t_slab)
                elements.append(Spacer(1, 6))

        # Final signature row
        elements.append(Spacer(1, 10))
        sig_data = [
            [Paragraph("<b>Student Signature:</b> ____________________", cell_style),
             Paragraph("<b>Teacher / Parent Evaluator:</b> ____________________", cell_style)]
        ]
        t_sig = Table(sig_data, colWidths=[261, 261])
        t_sig.setStyle(TableStyle([('PADDING', (0,0), (-1,-1), 4)]))
        elements.append(t_sig)

        doc.build(elements)
        return output_pdf_path

    @classmethod
    def render_question_paper_html(cls, paper: Dict[str, Any]) -> str:
        """
        Renders a clean, responsive HTML view supporting instant 1-click printing in browser.
        """
        meta = paper.get("metadata", {})
        subject = meta.get("subject", "Mathematics")
        time_mins = meta.get("time_allowed_mins", 20)
        max_marks = meta.get("max_marks", 15)
        exam_id = meta.get("exam_id", "EXAM-2026-V3")
        exam_title = meta.get("exam_title", "CBSE Examination")
        lang = meta.get("language", "en")

        typography_css = get_html_typography_css()

        sections_html = ""
        for sec in paper.get("sections", []):
            sec_name = html.escape(sec.get("section_name", "SECTION"))
            s_marks = sec.get("allocated_marks", "")
            s_label = f"{sec_name} ({s_marks} Marks)" if s_marks else sec_name

            q_rows = ""
            for q in sec.get("questions", []):
                q_num = html.escape(str(q.get("question_number", "Q.")))
                q_txt = html.escape(str(q.get("question_text", "")))
                q_m = q.get("marks", 1)
                options = q.get("options", [])

                opts_html = ""
                if options:
                    opts_items = "".join(f"<div class='opt-item'>{html.escape(opt)}</div>" for opt in options)
                    opts_html = f"<div class='opts-grid'>{opts_items}</div>"

                q_rows += f"""
                <div class="q-card">
                    <div class="q-meta">
                        <span class="q-num">{q_num}</span>
                        <span class="q-mark">[{q_m}]</span>
                    </div>
                    <div class="q-text">{q_txt}</div>
                    {opts_html}
                </div>
                """

            sections_html += f"""
            <div class="section-container">
                <div class="section-badge">{s_label}</div>
                {q_rows}
            </div>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(exam_title)} - {html.escape(subject)}</title>
    <style>
        {typography_css}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: #f1f5f9;
            padding: 24px;
            display: flex;
            justify-content: center;
        }}
        .print-paper {{
            background: #ffffff;
            width: 100%;
            max-width: 820px;
            padding: 36px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border-radius: 8px;
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #0f172a;
            padding-bottom: 12px;
            margin-bottom: 14px;
        }}
        .school-name {{
            font-size: 19px;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: 0.5px;
        }}
        .school-sub {{
            font-size: 11px;
            color: #64748b;
            margin-top: 2px;
        }}
        .exam-title {{
            font-size: 14px;
            font-weight: 700;
            color: #1e3a8a;
            margin-top: 6px;
            text-transform: uppercase;
        }}
        .meta-strip {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            padding: 8px 12px;
            font-size: 12px;
            border-radius: 4px;
            margin-bottom: 14px;
        }}
        .meta-strip div {{ color: #334155; }}
        .meta-strip strong {{ color: #0f172a; }}
        .instructions-box {{
            background: #fafaf9;
            border-left: 3px solid #f59e0b;
            padding: 8px 12px;
            font-size: 11px;
            color: #475569;
            margin-bottom: 18px;
            line-height: 1.4;
        }}
        .section-container {{
            margin-bottom: 20px;
        }}
        .section-badge {{
            background: #1e293b;
            color: #ffffff;
            padding: 6px 12px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            border-radius: 4px;
            text-align: center;
            margin-bottom: 10px;
        }}
        .q-card {{
            padding: 10px 0;
            border-bottom: 1px solid #f1f5f9;
        }}
        .q-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 4px;
        }}
        .q-num {{
            font-weight: 700;
            font-size: 13px;
            color: #0f172a;
        }}
        .q-mark {{
            font-weight: 700;
            font-size: 12px;
            color: #1e3a8a;
        }}
        .q-text {{
            font-size: 13px;
            line-height: 1.6;
            color: #1e293b;
            margin-bottom: 6px;
        }}
        .opts-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px 16px;
            margin-top: 6px;
            padding-left: 12px;
        }}
        .opt-item {{
            font-size: 12px;
            color: #334155;
            background: #f8fafc;
            padding: 4px 8px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }}
        .footer {{
            margin-top: 24px;
            padding-top: 10px;
            border-top: 1px solid #cbd5e1;
            text-align: center;
            font-size: 10px;
            color: #94a3b8;
        }}
        .action-bar {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            display: flex;
            gap: 10px;
            background: rgba(15, 23, 42, 0.85);
            padding: 10px 16px;
            border-radius: 30px;
            backdrop-filter: blur(8px);
        }}
        .btn {{
            background: #f97316;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: 700;
            border-radius: 20px;
            cursor: pointer;
            text-decoration: none;
        }}
        .btn:hover {{ background: #ea580c; }}
        @media print {{
            body {{ background: #ffffff; padding: 0; }}
            .print-paper {{ box-shadow: none; max-width: 100%; padding: 0; }}
            .action-bar {{ display: none !important; }}
        }}
    </style>
</head>
<body class="lang-{lang}">
    <div class="print-paper">
        <div class="header">
            <div class="school-name">THARUN REVISION BANNER</div>
            <div class="school-sub">CLASS 8 CBSE • DAILY RETENTION & HOST EXAMINATION ENGINE</div>
            <div class="exam-title">{html.escape(exam_title)}</div>
        </div>

        <div class="meta-strip">
            <div><strong>Student:</strong> Tharun</div>
            <div><strong>Class:</strong> Class 8 CBSE</div>
            <div><strong>Subject:</strong> {html.escape(subject)}</div>
            <div style="text-align: right;"><strong>Time:</strong> {time_mins}m | <strong>Marks:</strong> {max_marks}</div>
        </div>

        <div class="instructions-box">
            <strong>General Instructions:</strong> (1) All questions are compulsory. (2) Show neat step-by-step working and box final values. (3) Marks are indicated against each question.
        </div>

        {sections_html}

        <div class="footer">
            Exam ID: {html.escape(exam_id)} • Senthil Public School Examination Division
        </div>
    </div>

    <div class="action-bar">
        <button class="btn" onclick="window.print()">🖨️ Print Question Paper</button>
    </div>
</body>
</html>
"""
        return html_content


    # Backward compatibility alias
    render_blank_answer_booklet_pdf = render_blank_answer_sheet_pdf


# Architectural naming alias
ExamPrintStudioV3 = ExamPrintStudio


# ==============================================================================
# VERIFICATION RUNNER (SESSION 5 GATE)
# ==============================================================================
def run_session_5_verification():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 75)
    print("   SESSION 5: PRINT STUDIO (PDF, BLANK BOOKLET & HTML) VERIFICATION")
    print("=" * 75)

    from exam_phase_assembler_v3 import ExamSpecAssembler
    from exam_ground_truth_v3 import DiaryGroundTruth
    from exam_question_architect_v3 import GeminiQuestionArchitect

    # 1. Generate live paper data model for Mathematics
    print("\n[STEP 1] Generating Target Question Paper Data Model (Mathematics):")
    spec = ExamSpecAssembler.assemble_individual_paper_spec(
        subject="Mathematics",
        mode="balanced_daily",
        exam_type="daily_recall",
        exam_date="2026-10-12",
        topics=DiaryGroundTruth.get_portions_for_subject("Mathematics")[:1]
    )
    paper = GeminiQuestionArchitect.generate_question_paper(spec, custom_time_mins=15)
    print(f" -> Paper Title: {paper['metadata']['exam_title']}")
    print(f" -> Time & Marks: {paper['metadata']['time_allowed_mins']} Mins | {paper['metadata']['max_marks']} Marks")

    # 2. Render Official Vector Question Paper PDF
    print("\n[STEP 2] Compiling Vector Question Paper PDF:")
    qp_pdf = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", "TEST_PRINT_QUESTION_PAPER.pdf")
    res_qp = ExamPrintStudio.render_question_paper_pdf(paper, qp_pdf)
    print(f" -> ✅ Vector PDF Generated Successfully: {res_qp}")
    print(f" -> File Size: {os.path.getsize(res_qp):,} bytes")

    # 3. Render Physical Blank Answer Sheet Booklet PDF
    print("\n[STEP 3] Compiling Physical Blank Answer Sheet Booklet PDF:")
    ans_pdf = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", "TEST_PRINT_BLANK_ANSWER_SHEET.pdf")
    res_ans = ExamPrintStudio.render_blank_answer_sheet_pdf(paper, ans_pdf)
    print(f" -> ✅ Blank Booklet PDF Generated Successfully: {res_ans}")
    print(f" -> File Size: {os.path.getsize(res_ans):,} bytes")

    # 4. Render Responsive HTML Print View
    print("\n[STEP 4] Compiling Responsive HTML Print Studio View:")
    html_content = ExamPrintStudio.render_question_paper_html(paper)
    html_path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", "TEST_PRINT_PREVIEW.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f" -> ✅ HTML Print Studio Generated Successfully: {html_path}")
    print(f" -> File Size: {os.path.getsize(html_path):,} bytes")

    print("\n" + "=" * 75)
    print("   ✅ SESSION 5 VERIFICATION PASSED: All 3 Print Documents Ready!")
    print("=" * 75)


if __name__ == "__main__":
    run_session_5_verification()
