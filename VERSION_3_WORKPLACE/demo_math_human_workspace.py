"""
MATH HUMAN TYPOGRAPHY & DEDICATED WORKSPACE ENGINE (DUMMY PROTOTYPE)
--------------------------------------------------------------------
Demonstrates:
1. Natural human math formatting:
   - Fractions with horizontal bars: -10/3 -> (-10/3) formatted cleanly.
   - Superscripts: x^2 -> x², cm^2 -> cm², (103)^2 -> (103)².
   - Multiplication: * -> ×.
2. Math-specific 75/25 split workspace:
   - 75% Main step-solving zone with formula & final boxed value guidelines.
   - 25% Dedicated vertical rough-work column with dotted divider.
3. High-definition vector PDF and interactive KaTeX HTML preview.
"""

import os
import sys
import re
import html
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding="utf-8")

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors

from exam_ground_truth_v3 import EXAM_SYSTEM_DIR
from exam_typography_engine_v3 import register_reportlab_indic_fonts


class MathTypographyFormatter:
    """Converts computer-style math (*, ^, /) into beautiful human textbook math."""

    SUPERSCRIPT_MAP = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
        'n': 'ⁿ', 'x': 'ˣ', 'y': 'ʸ'
    }

    @classmethod
    def to_unicode_human_math(cls, text: str) -> str:
        """Transforms raw strings into human math for PDF rendering."""
        if not text:
            return ""
        s = str(text)

        # 1. Replace * with proper multiplication symbol ×
        # But avoid replacing ** (powers) before power handling
        s = re.sub(r'(?<=\w)\s*\*\s*(?=\w|\()', ' × ', s)
        s = re.sub(r'(?<=\))\s*\*\s*(?=\()', ' × ', s)

        # 2. Convert powers like x^2, (103)^2, cm^2, p^3 into real Unicode superscripts: x², (103)², cm², p³
        def replace_pow(m):
            base = m.group(1)
            exp = m.group(2)
            super_exp = "".join(cls.SUPERSCRIPT_MAP.get(ch, ch) for ch in exp)
            return f"{base}{super_exp}"

        s = re.sub(r'(\b[a-zA-Z0-9\)]+)\^([0-9\+\-nxy]+)', replace_pow, s)

        # 3. Clean up common fraction representations like (-10/3) -> (-¹⁰/₃) or formatted inline
        s = s.replace("pi", "π")
        s = s.replace("cm^2", "cm²").replace("cm^3", "cm³").replace("m^2", "m²")
        s = s.replace(" - ", " − ") # Real minus sign

        return s

    @classmethod
    def to_latex_katex(cls, text: str) -> str:
        """Converts math questions into LaTeX format for crisp browser KaTeX rendering."""
        s = str(text)
        s = s.replace(" * ", r" \times ")
        # Convert fractions (-10/3 * p * q^3) into \left(-\frac{10}{3}pq^3\right)
        s = re.sub(r'\(-?10/3\s*\*\s*p\s*\*\s*q\^3\)', r'\\left(-\\frac{10}{3}pq^3\\right)', s)
        s = re.sub(r'\(6/5\s*\*\s*p\^3\s*\*\s*q\)', r'\\left(\\frac{6}{5}p^3q\\right)', s)
        s = re.sub(r'\(103\)\^2', r'(103)^2', s)
        s = re.sub(r'\(2x \+ 5\)\(4x − 3\)', r'(2x + 5)(4x - 3)', s)
        s = re.sub(r'\(2a − 7\)\^2', r'(2a - 7)^2', s)
        return s


def generate_dummy_math_10min_prototype():
    """Builds a real 10-Minute Express Math Question Paper & Dedicated Workspace."""
    os.makedirs(os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS"), exist_ok=True)
    reg_font, bold_font = register_reportlab_indic_fonts()

    # Model 10-Minute Math Questions (Natural Human Math Format)
    questions = [
        {
            "q_num": "Q.1",
            "type": "MCQ",
            "marks": 1,
            "raw_text": "Find the product of the monomials: (-10/3 * p * q^3) * (6/5 * p^3 * q).",
            "human_text": "Find the product of the monomials: (−¹⁰/₃ pq³) × (⁶/₅ p³q).",
            "katex_text": r"Find the product of the monomials: \(\left(-\frac{10}{3}pq^3\right) \times \left(\frac{6}{5}p^3q\right)\)",
            "options": ["(a) −4p⁴q⁴", "(b) 4p⁴q⁴", "(c) −4p³q³", "(d) −2p⁴q⁴"],
            "ans": "(a) −4p⁴q⁴"
        },
        {
            "q_num": "Q.2",
            "type": "MCQ",
            "marks": 1,
            "raw_text": "Evaluate using identity (x + a)(x + b) or (a + b)^2: (103)^2 = (100 + 3)^2.",
            "human_text": "Evaluate using identity (a + b)²: (103)² = (100 + 3)².",
            "katex_text": r"Evaluate using standard identity \((a + b)^2\): \((103)^2 = (100 + 3)^2\)",
            "options": ["(a) 10,609", "(b) 10,906", "(c) 10,009", "(d) 10,309"],
            "ans": "(a) 10,609"
        },
        {
            "q_num": "Q.3",
            "type": "VSA",
            "marks": 2,
            "raw_text": "Multiply the binomials using distributive law: (2x + 5)(4x - 3). Show step-by-step expansion.",
            "human_text": "Multiply the binomials using distributive law: (2x + 5)(4x − 3). Show neat step-by-step expansion.",
            "katex_text": r"Multiply the binomials using distributive law: \((2x + 5)(4x - 3)\). Show step-by-step expansion.",
            "options": [],
            "ans": "8x² + 14x − 15"
        },
        {
            "q_num": "Q.4",
            "type": "SA",
            "marks": 4,
            "raw_text": "Expand using suitable algebraic identity: (2a - 7)^2. Hence evaluate the expression when a = 5.",
            "human_text": "Expand using suitable algebraic identity: (2a − 7)². Hence, evaluate the final expression when a = 5.",
            "katex_text": r"Expand using suitable algebraic identity: \((2a - 7)^2\). Hence, evaluate the expression when \(a = 5\).",
            "options": [],
            "ans": "4a² − 28a + 49; Value = 9"
        }
    ]

    # =========================================================================
    # 1. COMPILE QUESTION PAPER PDF WITH HUMAN MATH
    # =========================================================================
    qp_pdf_path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", "DEMO_HUMAN_MATH_QUESTION_PAPER.pdf")
    doc_qp = SimpleDocTemplate(qp_pdf_path, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=32, bottomMargin=32)
    styles = getSampleStyleSheet()

    header_style = ParagraphStyle('H1', fontName=bold_font, fontSize=13, leading=16, alignment=1)
    sub_style = ParagraphStyle('Sub', fontName=reg_font, fontSize=8.5, leading=11, alignment=1, textColor=colors.HexColor('#475569'))
    q_text_style = ParagraphStyle('QT', fontName=reg_font, fontSize=9.5, leading=14, textColor=colors.HexColor('#0f172a'))
    b_style = ParagraphStyle('B', fontName=bold_font, fontSize=9.5, leading=14)
    marks_style = ParagraphStyle('M', fontName=bold_font, fontSize=9, leading=13, alignment=2, textColor=colors.HexColor('#1e3a8a'))

    elements_qp = []
    elements_qp.append(Paragraph("THARUN REVISION BANNER", header_style))
    elements_qp.append(Paragraph("CLASS 8 CBSE • DAILY RETENTION & HOST EXAMINATION ENGINE", sub_style))
    elements_qp.append(Spacer(1, 4))
    elements_qp.append(Paragraph("<b>DAILY RECALL: MATHEMATICS [⚡ 10M EXPRESS SPRINT]</b>", ParagraphStyle('T', fontName=bold_font, fontSize=11, leading=14, alignment=1, textColor=colors.HexColor('#1e3a8a'))))
    elements_qp.append(Spacer(1, 4))

    meta_table = Table([[
        Paragraph("<b>Student:</b> Tharun", q_text_style),
        Paragraph("<b>Class:</b> Class 8 CBSE", q_text_style),
        Paragraph("<b>Subject:</b> Mathematics (Algebra)", q_text_style),
        Paragraph("<b>Time: 10 Mins | Marks: 8M</b>", marks_style)
    ]], colWidths=[120, 100, 170, 132])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    elements_qp.append(meta_table)
    elements_qp.append(Spacer(1, 8))

    # Questions with human math
    for q in questions:
        q_rows = []
        body = [Paragraph(f"{q['human_text']}", q_text_style)]
        if q["options"]:
            opt_table = Table([
                [Paragraph(q["options"][0], q_text_style), Paragraph(q["options"][1], q_text_style)],
                [Paragraph(q["options"][2], q_text_style), Paragraph(q["options"][3], q_text_style)]
            ], colWidths=[220, 220])
            opt_table.setStyle(TableStyle([('PADDING', (0,0), (-1,-1), 2)]))
            body.append(opt_table)

        row = [
            Paragraph(f"<b>{q['q_num']}</b>", b_style),
            body,
            Paragraph(f"<b>[{q['marks']}M]</b>", marks_style)
        ]
        t = Table([row], colWidths=[36, 446, 40])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 4),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0'))
        ]))
        elements_qp.append(t)
        elements_qp.append(Spacer(1, 4))

    doc_qp.build(elements_qp)

    # =========================================================================
    # 2. COMPILE DEDICATED 75/25 MATH WORKSPACE ANSWER BOOKLET PDF
    # =========================================================================
    ans_pdf_path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", "DEMO_DEDICATED_MATH_WORKSPACE_BOOKLET.pdf")
    doc_ans = SimpleDocTemplate(ans_pdf_path, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=32, bottomMargin=32)

    elements_ans = []
    elements_ans.append(Paragraph("THARUN REVISION BANNER • MATHEMATICS DEDICATED WORKSPACE", header_style))
    elements_ans.append(Paragraph("OFFICIAL CBSE STEP-SOLVING & ROUGH WORK BOOKLET [10 MIN SPRINT]", sub_style))
    elements_ans.append(Spacer(1, 6))

    top_box = Table([
        [
            Paragraph("<b>Student:</b> Tharun", q_text_style),
            Paragraph("<b>Class:</b> 8 CBSE", q_text_style),
            Paragraph("<b>Subject:</b> Mathematics", q_text_style),
            Paragraph("<b>Date:</b> Today", q_text_style),
            Paragraph("<b>Max: 8M | Scored: ____</b>", marks_style)
        ]
    ], colWidths=[110, 80, 130, 82, 120])
    top_box.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#0f172a')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('PADDING', (0,0), (-1,-1), 4)
    ]))
    elements_ans.append(top_box)
    elements_ans.append(Spacer(1, 8))

    elements_ans.append(Paragraph(
        "<i>Rules: Write your neat steps in the 75% Step-Zone. Do all scratch calculations, LCM & tables in the 25% Rough Column on the right.</i>",
        sub_style
    ))
    elements_ans.append(Spacer(1, 6))

    # Dedicated Math Double-Zone Slabs
    for q in questions:
        q_m = q["marks"]
        slab_h = 55 if q_m == 1 else (105 if q_m == 2 else 170)

        # Question Prompt Header Bar
        q_bar = Table([[
            Paragraph(f"<b>{q['q_num']} [{q_m} Mark{'s' if q_m > 1 else ''}]</b>: {q['human_text']}", ParagraphStyle('QB', fontName=bold_font, fontSize=8.5, leading=12, textColor=colors.HexColor('#1e293b'))),
            Paragraph(f"Score: ___ / {q_m}M", ParagraphStyle('SM', fontName=bold_font, fontSize=8, leading=11, alignment=2, textColor=colors.HexColor('#1e3a8a')))
        ]], colWidths=[422, 100])
        q_bar.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#e2e8f0')),
            ('PADDING', (0,0), (-1,-1), 3),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1'))
        ]))
        elements_ans.append(q_bar)

        # The 75% / 25% Split Workspace
        # Left (75% = 390pt): Main Step-Solving Zone
        # Right (25% = 132pt): Dedicated Rough Column
        step_zone_content = [
            Paragraph("<i>Step-by-Step Working & Formula Application:</i>", ParagraphStyle('G', fontName=reg_font, fontSize=7.5, textColor=colors.HexColor('#94a3b8'))),
            Spacer(1, slab_h - 35),
            Paragraph("┌──────────────────────────────────┐<br/>│ Final Answer Box:                │<br/>└──────────────────────────────────┘", ParagraphStyle('Box', fontName=reg_font, fontSize=7, leading=9, textColor=colors.HexColor('#64748b')))
        ] if q_m >= 2 else [
            Paragraph("<i>Selected Option / Quick Answer:</i>", ParagraphStyle('G', fontName=reg_font, fontSize=7.5, textColor=colors.HexColor('#94a3b8')))
        ]

        rough_content = [
            Paragraph("<b>ROUGH COLUMN</b>", ParagraphStyle('R_hdr', fontName=bold_font, fontSize=7, leading=9, alignment=1, textColor=colors.HexColor('#94a3b8'))),
            Paragraph("<i>(Scratch, LCM, Multiplications)</i>", ParagraphStyle('R_sub', fontName=reg_font, fontSize=6.5, leading=8, alignment=1, textColor=colors.HexColor('#cbd5e1')))
        ]

        workspace_table = Table([[step_zone_content, rough_content]], colWidths=[390, 132], rowHeights=[slab_h])
        workspace_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
            ('LINEBEFORE', (1,0), (1,-1), 1, colors.HexColor('#cbd5e1')),
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#ffffff')),
            ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#fafaf9')), # Subtle shade for rough column
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        elements_ans.append(workspace_table)
        elements_ans.append(Spacer(1, 8))

    doc_ans.build(elements_ans)

    # =========================================================================
    # 3. COMPILE INTERACTIVE KATEX HTML PREVIEW (TRUE HUMAN MATH)
    # =========================================================================
    html_path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", "DEMO_KATEX_MATH_PREVIEW.html")
    
    q_html_cards = ""
    for q in questions:
        opts_div = ""
        if q["options"]:
            opts_div = "<div class='opts-grid'>" + "".join(f"<div class='opt'>{html.escape(o)}</div>" for o in q["options"]) + "</div>"
        
        q_html_cards += f"""
        <div class="q-block">
            <div class="q-header">
                <span class="q-num">{q['q_num']}</span>
                <span class="q-marks">[{q['marks']} Mark{'s' if q['marks']>1 else ''}]</span>
            </div>
            <div class="q-katex-text">{q['katex_text']}</div>
            {opts_div}
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Tharun Revision - Human Math Typography</title>
    <!-- KaTeX CDN for real textbook math rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
            onload="renderMathInElement(document.body);"></script>
    <style>
        body {{
            background: #0f172a;
            color: #f8fafc;
            font-family: 'Segoe UI', system-ui, sans-serif;
            padding: 30px;
            display: flex;
            justify-content: center;
        }}
        .container {{
            max-width: 850px;
            width: 100%;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }}
        .banner {{
            text-align: center;
            border-bottom: 2px solid #f97316;
            padding-bottom: 12px;
            margin-bottom: 20px;
        }}
        .banner h1 {{
            font-size: 20px;
            color: #f97316;
            letter-spacing: 1px;
            margin: 0;
        }}
        .banner h2 {{
            font-size: 14px;
            color: #38bdf8;
            margin-top: 4px;
            font-weight: 600;
        }}
        .meta-strip {{
            display: flex;
            justify-content: space-between;
            background: #0f172a;
            border: 1px solid #334155;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 13px;
            margin-bottom: 24px;
        }}
        .q-block {{
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
        }}
        .q-header {{
            display: flex;
            justify-content: space-between;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .q-num {{ color: #fbbf24; font-size: 14px; }}
        .q-marks {{ color: #34d399; font-size: 13px; }}
        .q-katex-text {{
            font-size: 15px;
            line-height: 1.8;
            color: #f1f5f9;
        }}
        .opts-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-top: 12px;
        }}
        .opt {{
            background: #1e293b;
            border: 1px solid #475569;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 13px;
            color: #cbd5e1;
        }}
        .workspace-demo {{
            background: #ffffff;
            color: #0f172a;
            border-radius: 8px;
            padding: 16px;
            margin-top: 24px;
        }}
        .workspace-demo h3 {{
            font-size: 13px;
            color: #0f172a;
            margin-bottom: 8px;
        }}
        .split-grid {{
            display: grid;
            grid-template-columns: 3fr 1fr;
            border: 1px solid #94a3b8;
            height: 120px;
            border-radius: 4px;
        }}
        .main-zone {{
            padding: 8px;
            border-right: 1px dashed #94a3b8;
            font-size: 11px;
            color: #64748b;
        }}
        .rough-zone {{
            background: #f8fafc;
            padding: 8px;
            font-size: 11px;
            color: #94a3b8;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="banner">
            <h1>THARUN REVISION BANNER</h1>
            <h2>CLASS 8 CBSE • DAILY RETENTION & HOST EXAMINATION ENGINE</h2>
        </div>

        <div class="meta-strip">
            <span><strong>Student:</strong> Tharun</span>
            <span><strong>Subject:</strong> Mathematics (Algebraic Identities)</span>
            <span><strong>Pace:</strong> ⚡ 10m Express</span>
            <span style="color: #34d399;"><strong>Max Marks:</strong> 8M</span>
        </div>

        {q_html_cards}

        <div class="workspace-demo">
            <h3>📝 PREVIEW OF THARUN'S DEDICATED 75/25 MATH WORKSPACE:</h3>
            <div class="split-grid">
                <div class="main-zone">
                    <strong>75% MAIN STEP-SOLVING ZONE:</strong><br/>
                    • Formula substitution: \((a + b)(a - b) = a^2 - b^2\)<br/>
                    • Vertical equality alignment (= under =)<br/>
                    • Boxed Final Answer: \([ \text{{Result}} = 8x^2 + 14x - 15 ]\)
                </div>
                <div class="rough-zone">
                    <strong>25% ROUGH COLUMN:</strong><br/>
                    Scratch calculations,<br/>
                    LCM, long division &<br/>
                    side multiplications
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("=" * 75)
    print("   ✅ DUMMY MATH PROTOTYPE GENERATED SUCCESSFULLY!")
    print("=" * 75)
    print(f" -> 1. Vector Question Paper PDF:  {qp_pdf_path}")
    print(f" -> 2. Dedicated 75/25 Math PDF:    {ans_pdf_path}")
    print(f" -> 3. Interactive KaTeX HTML:      {html_path}")
    print("=" * 75)


if __name__ == "__main__":
    generate_dummy_math_10min_prototype()
