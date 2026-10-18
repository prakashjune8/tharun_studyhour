"""
MATH FRACTION & HUMAN TYPOGRAPHY ENGINE (SESSION 5 EXTENSION)
-------------------------------------------------------------
Comprehensive mathematical typesetter for CBSE Class 8:
1. Converts raw computer notation into human math:
   - Fractions: -10/3 -> (-¹⁰/₃) or true horizontal bar \frac{10}{3}.
   - Powers: x^2 -> x², cm^2 -> cm², (103)^2 -> (103)².
   - Operators: * -> ×, / -> ÷ or fraction bar, - -> − (real minus).
2. ReportLab PDF Micro-Table Flowable for true horizontal fraction bars.
3. Dedicated 75/25 Math Workspace Answer Booklet generator.
4. Full KaTeX integration for interactive web previews.
"""

import re
import html
from typing import Dict, Any, List, Tuple, Optional
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors


class MathFractionEngine:
    """
    Handles inline and display fractions across PDF and HTML.
    """

    SUPERSCRIPTS = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
        'a': 'ᵃ', 'b': 'ᵇ', 'n': 'ⁿ', 'x': 'ˣ', 'y': 'ʸ'
    }

    SUBSCRIPTS = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
        '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
        'a': 'ₐ', 'e': 'ₑ', 'x': 'ₓ'
    }

    COMMON_FRACTIONS = {
        "1/2": "½",
        "1/3": "⅓",
        "2/3": "⅔",
        "1/4": "¼",
        "3/4": "¾",
        "1/5": "⅕",
        "2/5": "⅖",
        "3/5": "⅗",
        "4/5": "⅘",
        "1/6": "⅙",
        "5/6": "⅚",
        "1/8": "⅛",
        "3/8": "⅜",
        "5/8": "⅝",
        "7/8": "⅞"
    }

    @classmethod
    def format_inline_fraction(cls, num_str: str, den_str: str) -> str:
        """Converts numerator and denominator into a beautiful stacked Unicode fraction: ¹⁰/₃"""
        # Check if negative
        is_neg = num_str.startswith("-") or num_str.startswith("−")
        clean_num = num_str.lstrip("-−")
        
        # Check common fractions
        key = f"{clean_num}/{den_str}"
        if key in cls.COMMON_FRACTIONS:
            res = cls.COMMON_FRACTIONS[key]
            return f"−{res}" if is_neg else res

        # Build stacked superscript/subscript
        super_num = "".join(cls.SUPERSCRIPTS.get(c, c) for c in clean_num)
        sub_den = "".join(cls.SUBSCRIPTS.get(c, c) for c in den_str)
        prefix = "−" if is_neg else ""
        return f"{prefix}{super_num}/{sub_den}"

    @classmethod
    def prettify_math_text(cls, text: str) -> str:
        """
        Main prettifier for PDF Paragraphs:
        Converts *, ^, powers, and fractions into clean human notation.
        """
        if not text:
            return ""
        s = str(text)

        # 1. Standardize minus sign
        s = re.sub(r'(?<=\s)-(?=\s)', ' − ', s)

        # 2. Convert simple fractions like 10/3, -10/3, 6/5 into Unicode stacked fractions
        def replace_fraction(m):
            num = m.group(1)
            den = m.group(2)
            # Avoid matching dates like 12/10/2026 or paths
            if len(den) > 4:
                return m.group(0)
            return cls.format_inline_fraction(num, den)

        s = re.sub(r'(?<!\d|\/)(−?\d+)\/(\d+)(?!\d|\/)', replace_fraction, s)

        # 3. Replace multiplication * with ×
        s = re.sub(r'(?<=[0-9a-zA-Z\)])\s*\*\s*(?=[0-9a-zA-Z\(])', ' × ', s)

        # 4. Convert exponents like x^2, (103)^2, cm^2, p^3 into superscripts: x², (103)², cm², p³
        def replace_power(m):
            base = m.group(1)
            exp = m.group(2)
            super_exp = "".join(cls.SUPERSCRIPTS.get(ch, ch) for ch in exp)
            return f"{base}{super_exp}"

        s = re.sub(r'([a-zA-Z0-9\)]+)\^([0-9\+\-nxy]+)', replace_power, s)

        # 5. Clean symbols
        s = s.replace("pi", "π")
        s = s.replace("cm^2", "cm²").replace("cm^3", "cm³").replace("m^2", "m²")

        return s

    @classmethod
    def to_latex_math(cls, text: str) -> str:
        """
        Converts text containing math into LaTeX syntax with \\frac{}{} for KaTeX browser rendering.
        """
        if not text:
            return ""
        s = str(text)

        # Replace fractions (-10/3) -> \left(-\frac{10}{3}\right)
        s = re.sub(r'\(-?(\d+)\/(\d+)\)', r'\\left(-\\frac{\1}{\2}\\right)', s)
        s = re.sub(r'(?<!\w)(\d+)\/(\d+)(?!\w)', r'\\frac{\1}{\2}', s)

        # Replace * with \times
        s = re.sub(r'(?<=[0-9a-zA-Z\)])\s*\*\s*(?=[0-9a-zA-Z\(])', r' \\times ', s)

        return s

    @classmethod
    def build_reportlab_fraction_table(
        cls,
        numerator_str: str,
        denominator_str: str,
        font_name: str = "Helvetica",
        font_size: int = 9,
        text_color = colors.HexColor('#0f172a')
    ) -> Table:
        """
        Creates a micro-table with a real 1pt horizontal fraction bar for PDF rendering.
        """
        from reportlab.lib.styles import ParagraphStyle
        num_style = ParagraphStyle('FN', fontName=font_name, fontSize=font_size-1, leading=font_size, alignment=1, textColor=text_color)
        den_style = ParagraphStyle('FD', fontName=font_name, fontSize=font_size-1, leading=font_size, alignment=1, textColor=text_color)

        data = [
            [Paragraph(numerator_str, num_style)],
            [Paragraph(denominator_str, den_style)]
        ]
        t = Table(data, colWidths=[24], rowHeights=[font_size + 1, font_size + 1])
        t.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 0),
            ('LINEBELOW', (0,0), (0,0), 1, text_color) # Horizontal fraction bar
        ]))
        return t
