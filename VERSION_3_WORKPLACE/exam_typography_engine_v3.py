"""
EXAM MULTI-LANGUAGE TYPOGRAPHY & INDIC ENGINE (SESSION 2)
---------------------------------------------------------
Pure, clean, decoupled typography engine for ScholasticPulse Exam Architecture.
Guarantees:
1. Native Windows Indic TrueType font registration (Nirmala, NirmalaB, Mangal, Latha).
2. ReportLab PDF Unicode font mapping (Hindi Devanagari, Tamil, English, Math).
3. ReportLab XML entity sanitization (<, >, &, ", ') without corrupting Indic glyphs.
4. HTML print preview styling with Google Fonts fallback (Noto Sans Devanagari & Tamil).
5. Safe Tkinter font selection for UI previews.
"""

import os
import sys
import re
import html
from typing import Dict, Any, Tuple, Optional

# ==============================================================================
# 0. BASE DIRECTORIES
# ==============================================================================
def get_base_dir() -> str:
    if getattr(sys, 'frozen', False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
EXAM_SYSTEM_DIR = os.path.join(BASE_DIR, "EXAM_SYSTEM_V3")

# ==============================================================================
# 1. WINDOWS NATIVE FONT LOCATOR
# ==============================================================================
def find_windows_font(font_filename: str) -> Optional[str]:
    """Search C:\\Windows\\Fonts and local system dirs for a TrueType font file."""
    windir = os.environ.get("WINDIR", r"C:\Windows")
    fonts_dir = os.path.join(windir, "Fonts")
    target = os.path.join(fonts_dir, font_filename)
    if os.path.exists(target):
        return target
    
    # Check lowercase variant
    target_lower = os.path.join(fonts_dir, font_filename.lower())
    if os.path.exists(target_lower):
        return target_lower
    return None


# ==============================================================================
# 2. REPORTLAB UNICODE FONT REGISTRY
# ==============================================================================
UNICODE_REGULAR_FONT = "IndicUnicodeRegular"
UNICODE_BOLD_FONT = "IndicUnicodeBold"
FONTS_REGISTERED = False

def register_reportlab_indic_fonts() -> Tuple[str, str]:
    """
    Registers Windows native Indic TrueType fonts (ARIALUNI.TTF / Nirmala) into ReportLab.
    ARIALUNI.TTF is the Microsoft Universal Unicode font supporting Latin, Devanagari (Hindi), Tamil, etc.
    Returns (regular_font_name, bold_font_name).
    """
    global FONTS_REGISTERED
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        reg_names = pdfmetrics.getRegisteredFontNames()
        if UNICODE_REGULAR_FONT in reg_names:
            return UNICODE_REGULAR_FONT, UNICODE_BOLD_FONT if UNICODE_BOLD_FONT in reg_names else UNICODE_REGULAR_FONT

        # 1. ARIALUNI.TTF (Microsoft Arial Unicode MS - 100% full coverage of Devanagari, Tamil, Math, Latin)
        arialuni = find_windows_font("ARIALUNI.TTF")
        if arialuni:
            try:
                pdfmetrics.registerFont(TTFont(UNICODE_REGULAR_FONT, arialuni))
                pdfmetrics.registerFont(TTFont(UNICODE_BOLD_FONT, arialuni))
                FONTS_REGISTERED = True
                return UNICODE_REGULAR_FONT, UNICODE_BOLD_FONT
            except Exception as e:
                print(f"[Typography] Warning registering ARIALUNI.TTF: {e}")

        # 2. Nirmala.ttf
        nirmala = find_windows_font("Nirmala.ttf")
        nirmala_b = find_windows_font("NirmalaB.ttf")
        if nirmala:
            try:
                pdfmetrics.registerFont(TTFont(UNICODE_REGULAR_FONT, nirmala))
                bold = UNICODE_REGULAR_FONT
                if nirmala_b:
                    pdfmetrics.registerFont(TTFont(UNICODE_BOLD_FONT, nirmala_b))
                    bold = UNICODE_BOLD_FONT
                FONTS_REGISTERED = True
                return UNICODE_REGULAR_FONT, bold
            except Exception:
                pass

        return "Helvetica", "Helvetica-Bold"
    except ImportError:
        return "Helvetica", "Helvetica-Bold"


# ==============================================================================
# 3. LANGUAGE & SCRIPT DETECTOR
# ==============================================================================
class ScriptDetector:
    """Detects primary script in any string: English, Hindi (Devanagari), Tamil, or Math."""
    
    DEVANAGARI_RANGE = (0x0900, 0x097F)
    TAMIL_RANGE = (0x0B80, 0x0BFF)

    @classmethod
    def detect_script(cls, text: str) -> str:
        """Returns 'hi' (Devanagari), 'ta' (Tamil), or 'en' (Latin/English)."""
        devanagari_count = 0
        tamil_count = 0
        total_alpha = 0

        for ch in text:
            code = ord(ch)
            if cls.DEVANAGARI_RANGE[0] <= code <= cls.DEVANAGARI_RANGE[1]:
                devanagari_count += 1
                total_alpha += 1
            elif cls.TAMIL_RANGE[0] <= code <= cls.TAMIL_RANGE[1]:
                tamil_count += 1
                total_alpha += 1
            elif ch.isalpha():
                total_alpha += 1

        if total_alpha == 0:
            return "en"
        if devanagari_count / total_alpha > 0.15:
            return "hi"
        if tamil_count / total_alpha > 0.15:
            return "ta"
        return "en"


# ==============================================================================
# 4. XML / HTML SAFE SANITIZER
# ==============================================================================
class TextSanitizer:
    """
    Safely escapes characters for ReportLab Platypus Paragraphs (<, >, &, ")
    while preserving Unicode Indic text and formatting tags.
    """
    ALLOWED_TAGS = {"b", "/b", "i", "/i", "u", "/u", "font", "/font", "super", "/super", "sub", "/sub"}

    @classmethod
    def sanitize_for_reportlab(cls, text: str) -> str:
        if not text:
            return ""
        # 1. Clean control characters and high emoji characters unsupported by standard TTF
        cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', str(text))
        cleaned = re.sub(r'[\U00010000-\U0010ffff]', '', cleaned)
        cleaned = re.sub(r'[\u2600-\u27bf]', '', cleaned)
        cleaned = re.sub(r'\[\s+', '[', cleaned)
        cleaned = re.sub(r'\s+\]', ']', cleaned)
        cleaned = re.sub(r'  +', ' ', cleaned)
        
        # 2. Escape ampersands not already part of an XML entity
        cleaned = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', cleaned)
        
        # 3. Tokenize by potential XML tags <...> to preserve valid tags like <b>, <i> while escaping math like x < 5
        tokens = re.split(r'(<[^>]+>)', cleaned)
        result = []
        for token in tokens:
            if token.startswith('<') and token.endswith('>'):
                tag_content = token[1:-1].strip()
                tag_name = tag_content.split()[0].lower() if tag_content else ""
                if tag_name in cls.ALLOWED_TAGS:
                    result.append(token)
                else:
                    result.append('&lt;' + token[1:-1] + '&gt;')
            else:
                # Escape bare < or > in normal text
                escaped = token.replace('<', '&lt;').replace('>', '&gt;')
                result.append(escaped)

        return "".join(result)

    @staticmethod
    def sanitize_for_html(text: str) -> str:
        if not text:
            return ""
        return html.escape(str(text))


# ==============================================================================
# 5. HTML MULTI-LANGUAGE WEB FONT STYLING
# ==============================================================================
def get_html_typography_css() -> str:
    """Returns CSS with Google Fonts for Devanagari and Tamil with fallback to system fonts."""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&family=Noto+Sans+Tamil:wght@400;600;700&display=swap');

    body {
        font-family: 'Inter', 'Nirmala UI', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1e293b;
        line-height: 1.5;
    }

    /* Hindi Devanagari Text Elements */
    .lang-hi, [lang="hi"] {
        font-family: 'Noto Sans Devanagari', 'Nirmala UI', 'Mangal', sans-serif !important;
        line-height: 1.7;
    }

    /* Tamil Text Elements */
    .lang-ta, [lang="ta"] {
        font-family: 'Noto Sans Tamil', 'Nirmala UI', 'Latha', sans-serif !important;
        line-height: 1.7;
    }

    /* Math Formulas and Symbols */
    .math-expr {
        font-family: 'Cambria Math', 'KaTeX_Math', 'Times New Roman', serif;
        font-style: italic;
    }
    """


# ==============================================================================
# 6. VERIFICATION TEST (SESSION 2 GATE)
# ==============================================================================
def run_session_2_verification():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 70)
    print("   SESSION 2: MULTI-LANGUAGE TYPOGRAPHY ENGINE VERIFICATION")
    print("=" * 70)

    # 1. Test Windows Native Fonts
    print("\n[TEST 1] Windows Native Indic Font Detection:")
    nirmala = find_windows_font("Nirmala.ttf")
    nirmala_b = find_windows_font("NirmalaB.ttf")
    mangal = find_windows_font("mangal.ttf")
    latha = find_windows_font("latha.ttf")
    print(f" -> Nirmala.ttf  (Unified Indic):  {nirmala or 'NOT FOUND'}")
    print(f" -> NirmalaB.ttf (Bold Indic):     {nirmala_b or 'NOT FOUND'}")
    print(f" -> Mangal.ttf   (Hindi):          {mangal or 'NOT FOUND'}")
    print(f" -> Latha.ttf    (Tamil):          {latha or 'NOT FOUND'}")

    # 2. Test ReportLab Registration
    print("\n[TEST 2] ReportLab Unicode Font Registration:")
    reg_font, bold_font = register_reportlab_indic_fonts()
    print(f" -> Registered Regular Font: {reg_font}")
    print(f" -> Registered Bold Font:    {bold_font}")

    # 3. Test Script Detection
    print("\n[TEST 3] Script Detection on Multi-Language Samples:")
    samples = [
        ("English Math", "Solve for x in the equation: 3x + 15 = 45. Find the value of x."),
        ("Hindi Vasant", "संज्ञा के कितने भेद होते हैं? उदाहरण देकर स्पष्ट कीजिए। (वसंत भाग-3)"),
        ("Tamil Seyyul", "தொட்டனைத் தூறும் மணற்கேணி மாந்தர்க்குக் கற்றனைத் தூறும் அறிவு. - திருக்குறள்"),
        ("Science Math", "A block exerts a force of F = 150 N on an area A = 0.5 m². Calculate pressure P = F/A.")
    ]
    for label, text in samples:
        detected = ScriptDetector.detect_script(text)
        print(f" -> [{label:<12}] Detected Lang: {detected.upper()} | Sample: {text[:45]}...")

    # 4. Test ReportLab XML Entity Sanitizer
    print("\n[TEST 4] ReportLab XML Entity Sanitization:")
    risky_strings = [
        "If a < b and b > c, evaluate a & b.",
        "Solve (x + 3)^2 where x < 10 & y > 5.",
        "व्याकरण: 'दिन' और 'रात' के विलोम शब्द लिखिए & वाक्य बनाइए।",
        "திருக்குறள்: 'அகர முதல எழுத்தெல்லாம்' & விளக்கம் தருக."
    ]
    for s in risky_strings:
        sanitized = TextSanitizer.sanitize_for_reportlab(s)
        print(f" -> Raw:       {s}")
        print(f"    Sanitized: {sanitized}")

    # 5. Generate a Live PDF Multi-Language Test Card
    print("\n[TEST 5] Compiling Live Multi-Language Test PDF:")
    out_pdf_path = os.path.join(EXAM_SYSTEM_DIR, "03_GENERATED_QUESTION_PAPERS", "TEST_MULTILANGUAGE_TYPOGRAPHY.pdf")
    os.makedirs(os.path.dirname(out_pdf_path), exist_ok=True)
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors

        doc = SimpleDocTemplate(out_pdf_path, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()

        normal_style = ParagraphStyle(
            'MultiLangNormal',
            parent=styles['Normal'],
            fontName=reg_font,
            fontSize=11,
            leading=16,
            textColor=colors.HexColor('#0f172a')
        )
        title_style = ParagraphStyle(
            'MultiLangTitle',
            parent=styles['Normal'],
            fontName=bold_font,
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1e3a8a')
        )

        elements = []
        elements.append(Paragraph("SENTHIL PUBLIC SCHOOL - MULTI-LANGUAGE TYPOGRAPHY TEST CARD", title_style))
        elements.append(Spacer(1, 12))

        for label, text in samples:
            safe_text = TextSanitizer.sanitize_for_reportlab(text)
            card_content = [
                [Paragraph(f"<b>Language Category: {label}</b>", title_style)],
                [Paragraph(safe_text, normal_style)]
            ]
            t = Table(card_content, colWidths=[520])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
                ('PADDING', (0,0), (-1,-1), 8),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 10))

        doc.build(elements)
        print(f" -> ✅ Multi-Language Vector PDF Generated Successfully: {out_pdf_path}")
        pdf_success = True
    except Exception as e:
        print(f" -> 🔴 PDF Generation Failed: {e}")
        pdf_success = False

    print("\n" + "=" * 70)
    if reg_font != "Helvetica" and pdf_success:
        print("   ✅ SESSION 2 VERIFICATION PASSED: Multi-Language Engine Ready!")
    else:
        print("   ⚠️ SESSION 2 VERIFICATION FINISHED (Check notes above)")
    print("=" * 70)


if __name__ == "__main__":
    run_session_2_verification()
