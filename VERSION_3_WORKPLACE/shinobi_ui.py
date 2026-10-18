# Shinobi Dark-Glass UI Design System and High-DPI Graphics Engine
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import math

# =============================================================================
# 🎨 SHINOBI HIGH-DPI GRAPHICS ENGINE (4X SSAA + GAUSSIAN GLOW + 3D SCROLLS)
# =============================================================================
class ShinobiGraphicsEngine:
    """
    Dedicated High-DPI / SSAA Rendering Engine for ScholasticPulse Desktop:
    - 4x Supersampled (SSAA) rounded glass cards with subtle vertical gradients.
    - Soft Gaussian radial auras and silky anti-aliased timer progress rings.
    - True 3D shaded cylindrical mahogany/crimson parchment scrolls matching Web UI.
    - Anti-aliased rounded pill selector cards and stacked action tiles.
    """
    _cache = {}

    @classmethod
    def clear_cache(cls):
        """Clears all cached SSAA cards, 3D parchment scrolls, circular emblems, and rank plaques."""
        cls._cache.clear()

    @classmethod
    def _hex_to_rgb(cls, hex_color):
        if not hex_color or not isinstance(hex_color, str) or not hex_color.startswith('#'):
            return (15, 23, 42)
        h = hex_color.lstrip('#')
        if len(h) == 3:
            h = ''.join([c * 2 for c in h])
        try:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        except Exception:
            return (15, 23, 42)

    @classmethod
    def create_rounded_glass_card(cls, width, height, radius=14, bg_top='#111827', bg_bot='#0b1120',
                                  border_color='#d97706', border_width=1, glow_color=None, glow_radius=0):
        key = ('card', width, height, radius, bg_top, bg_bot, border_color, border_width, glow_color, glow_radius)
        if key in cls._cache:
            return cls._cache[key]
        
        if Image is None or ImageDraw is None:
            return None

        scale = 3
        sw, sh = max(1, width * scale), max(1, height * scale)
        srad = radius * scale

        # Gradient fill
        top_rgb = cls._hex_to_rgb(bg_top)
        bot_rgb = cls._hex_to_rgb(bg_bot)
        grad = Image.new('RGBA', (sw, sh))
        gdraw = ImageDraw.Draw(grad)
        for y in range(sh):
            ratio = y / max(1, sh - 1)
            r = int(top_rgb[0] + (bot_rgb[0] - top_rgb[0]) * ratio)
            g = int(top_rgb[1] + (bot_rgb[1] - top_rgb[1]) * ratio)
            b = int(top_rgb[2] + (bot_rgb[2] - top_rgb[2]) * ratio)
            gdraw.line([(0, y), (sw, y)], fill=(r, g, b, 255))

        mask = Image.new('L', (sw, sh), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle([0, 0, sw - 1, sh - 1], radius=srad, fill=255)

        base_card = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
        base_card.paste(grad, (0, 0), mask)

        # Border
        if border_color and border_width > 0:
            b_rgb = cls._hex_to_rgb(border_color)
            sbw = border_width * scale
            bdraw = ImageDraw.Draw(base_card)
            bdraw.rounded_rectangle([sbw // 2, sbw // 2, sw - 1 - sbw // 2, sh - 1 - sbw // 2],
                                   radius=srad, outline=(*b_rgb, 255), width=sbw)

        res = base_card.resize((width, height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(res)
        cls._cache[key] = photo
        return photo

    @classmethod
    def create_konoha_crest_emblem(cls, size=52, border_color="#f59e0b", stroke_color="#fb923c"):
        """
        Creates an anti-aliased 4x SSAA Konoha Leaf Village crest medallion matching the Web UI (#deckCrest).
        Features:
        - Theme-aware glowing chakra outer ring
        - Deep radial gradient medallion core
        - Precision Konoha leaf beak and golden spiral curve
        """
        key = ('konoha_crest', size, border_color, stroke_color)
        if key in cls._cache:
            return cls._cache[key]
        if Image is None or ImageDraw is None:
            return None
        scale = 4
        s = max(4, size * scale)
        img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        center = s / 2.0
        radius = (s - 12 * scale) / 2.0

        b_rgb = cls._hex_to_rgb(border_color)
        s_rgb = cls._hex_to_rgb(stroke_color) if stroke_color else b_rgb

        # Outer chakra glow ring
        for gw in range(int(5 * scale), 0, -2):
            alpha = int(35 * (1.0 - gw / (5.0 * scale)))
            draw.ellipse(
                [center - radius - gw, center - radius - gw, center + radius + gw, center + radius + gw],
                outline=(*b_rgb, alpha),
                width=2
            )

        # Dark radial medallion core
        for r in range(int(radius), 0, -1):
            ratio = r / radius
            cr = int(31 * (1.0 - ratio * 0.7) + 11 * (ratio * 0.7))
            cg = int(20 * (1.0 - ratio * 0.7) + 16 * (ratio * 0.7))
            cb = int(9 * (1.0 - ratio * 0.7) + 30 * (ratio * 0.7))
            draw.ellipse([center - r, center - r, center + r, center + r], fill=(cr, cg, cb, 255))

        # Circular outer border
        border_w = max(2, int(2.5 * scale))
        draw.ellipse([center - radius, center - radius, center + radius, center + radius], outline=(*b_rgb, 255), width=border_w)

        # Konoha Leaf triangle beak
        import math
        svg_scale = (s * 0.58) / 48.0
        ox = center - 24 * svg_scale
        oy = center - 24 * svg_scale
        def pt(x, y): return (ox + x * svg_scale, oy + y * svg_scale)

        tri = [pt(11.5, 36), pt(7.5, 41.5), pt(15, 38.5)]
        draw.polygon(tri, fill=(*s_rgb, 255))

        # Spiral curve points
        spiral_pts = []
        for deg in range(0, 540, 2):
            rad = math.radians(deg)
            r_val = 1.8 + deg * 0.024
            x = 24 + r_val * math.cos(rad - math.pi * 0.5)
            y = 24 + r_val * math.sin(rad - math.pi * 0.5)
            spiral_pts.append(pt(x, y))
        stroke_w = max(2, int(2.6 * scale))
        draw.line(spiral_pts, fill=(*s_rgb, 255), width=stroke_w, joint='curve')

        # Outer tail arc
        tail_pts = []
        for deg in range(120, 210, 2):
            rad = math.radians(deg)
            r_val = 13.5
            x = 24 + r_val * math.cos(rad)
            y = 24 + r_val * math.sin(rad)
            tail_pts.append(pt(x, y))
        draw.line(tail_pts, fill=(*s_rgb, 255), width=stroke_w, joint='curve')

        res = img.resize((size, size), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(res)
        cls._cache[key] = photo
        return photo

    @classmethod
    def create_circular_emblem(cls, size=52, bg="#111827", border_color="#f97316", border_width=2.5):
        return cls.create_konoha_crest_emblem(size=size, border_color=border_color, stroke_color=border_color)

    @classmethod
    def create_hexagonal_rank_plaque(cls, width=144, height=28, text="RANK: HOKAGE"):
        key = ('hex_rank', width, height, text)
        if key in cls._cache:
            return cls._cache[key]
        if Image is None or ImageDraw is None:
            return None
        scale = 4
        sw, sh = max(1, width * scale), max(1, height * scale)
        img = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Chamfered pointed ribbon polygon: polygon(8% 0, 92% 0, 100% 50%, 92% 100%, 8% 100%, 0 50%)
        inset_x = int(sw * 0.08)
        poly = [
            (inset_x, 0),
            (sw - inset_x, 0),
            (sw - 1, sh // 2),
            (sw - inset_x, sh - 1),
            (inset_x, sh - 1),
            (0, sh // 2)
        ]
        
        mask = Image.new('L', (sw, sh), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.polygon(poly, fill=255)
        
        # Metallic gold vertical gradient: #fde68a (top) -> #d99a2b (mid) -> #8a5a12 (bottom)
        grad = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(grad)
        top_c = (253, 230, 138)
        mid_c = (217, 154, 43)
        bot_c = (138, 90, 18)
        for y in range(sh):
            rel_y = y / max(1, sh - 1)
            if rel_y < 0.5:
                fac = rel_y / 0.5
                r = int(top_c[0] + (mid_c[0] - top_c[0]) * fac)
                g = int(top_c[1] + (mid_c[1] - top_c[1]) * fac)
                b = int(top_c[2] + (mid_c[2] - top_c[2]) * fac)
            else:
                fac = (rel_y - 0.5) / 0.5
                r = int(mid_c[0] + (bot_c[0] - mid_c[0]) * fac)
                g = int(mid_c[1] + (bot_c[1] - mid_c[1]) * fac)
                b = int(mid_c[2] + (bot_c[2] - mid_c[2]) * fac)
            gdraw.line([(0, y), (sw, y)], fill=(r, g, b, 255))
            
        img.paste(grad, (0, 0), mask)
        draw.polygon(poly, outline=(254, 240, 138, 255), width=max(1, int(1.5 * scale)))
        
        # Render text in crisp dark ink (#1b1205)
        try:
            from PIL import ImageFont
            font = None
            for font_name in ["segoeuib.ttf", "arialbd.ttf", "tahoma.ttf"]:
                try:
                    font = ImageFont.truetype(font_name, int(9 * scale))
                    break
                except Exception:
                    pass
            if not font:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            tx = (sw - tw) // 2
            ty = (sh - th) // 2 - int(1 * scale)
            draw.text((tx, ty), text, fill=(27, 18, 5, 255), font=font)
        except Exception:
            pass
            
        res = img.resize((width, height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(res)
        cls._cache[key] = photo
        return photo

    @classmethod
    def create_3d_parchment_scroll(cls, width, height, roller_width=18, is_mini_badge=False, is_rollover=False, is_dark_slate=False):
        key = ('scroll', width, height, roller_width, is_mini_badge, is_rollover, is_dark_slate)
        if key in cls._cache:
            return cls._cache[key]

        if Image is None or ImageDraw is None:
            return None

        scale = 3
        sw, sh = max(1, width * scale), max(1, height * scale)
        srw = max(4, roller_width * scale)

        img = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Center parchment:
        # Standard: #d6be96 top shadow -> #fdf3dc center highlight -> #e6cfa7 bottom edge
        # Amber Rollover: #fef3c7 center, #fde68a bottom
        # Dark Slate Inactive: #1e293b top -> #161f30 center -> #0f172a bottom
        cx1 = srw - (2 * scale)
        cx2 = sw - srw + (2 * scale)
        for y in range(sh):
            rel_y = y / max(1, sh - 1)
            if is_dark_slate:
                if rel_y < 0.4:
                    fac = rel_y / 0.4
                    r = int(30 + (22 - 30) * fac)
                    g = int(41 + (28 - 41) * fac)
                    b = int(59 + (46 - 59) * fac)
                else:
                    fac = (rel_y - 0.4) / 0.6
                    r = int(22 + (15 - 22) * fac)
                    g = int(28 + (23 - 28) * fac)
                    b = int(46 + (42 - 46) * fac)
            elif is_rollover:
                if rel_y < 0.35:
                    fac = rel_y / 0.35
                    r = int(254 + (255 - 254) * fac)
                    g = int(240 + (250 - 240) * fac)
                    b = int(195 + (215 - 195) * fac)
                else:
                    fac = (rel_y - 0.35) / 0.65
                    r = int(255 + (253 - 255) * fac)
                    g = int(250 + (230 - 250) * fac)
                    b = int(215 + (138 - 215) * fac)
            else:
                if rel_y < 0.35:
                    fac = rel_y / 0.35
                    r = int(214 + (253 - 214) * fac)
                    g = int(190 + (243 - 190) * fac)
                    b = int(150 + (220 - 150) * fac)
                else:
                    fac = (rel_y - 0.35) / 0.65
                    r = int(253 + (230 - 253) * fac)
                    g = int(243 + (207 - 243) * fac)
                    b = int(220 + (167 - 220) * fac)
            draw.line([(cx1, y), (cx2, y)], fill=(r, g, b, 255))

        top_border_col = (51, 65, 85, 255) if is_dark_slate else ((217, 119, 6, 255) if is_rollover else (180, 83, 9, 255))
        draw.line([(cx1, 0), (cx2, 0)], fill=top_border_col, width=max(1, scale))
        draw.line([(cx1, sh - 1), (cx2, sh - 1)], fill=top_border_col, width=max(1, scale))

        # Cylindrical mahogany-crimson rollers:
        def _draw_roller(rx1, rx2):
            rw = rx2 - rx1
            for x in range(rw):
                rel_x = x / max(1, rw - 1)
                if is_dark_slate:
                    # Dark mahogany for inactive scroll rollers: #4a0d13 -> #7f1d1d -> #3b0709
                    if rel_x < 0.45:
                        fac = rel_x / 0.45
                        cr = int(74 + (127 - 74) * fac)
                        cg = int(13 + (29 - 13) * fac)
                        cb = int(19 + (29 - 19) * fac)
                    else:
                        fac = (rel_x - 0.45) / 0.55
                        cr = int(127 + (59 - 127) * fac)
                        cg = int(29 + (7 - 29) * fac)
                        cb = int(29 + (9 - 29) * fac)
                else:
                    if rel_x < 0.45:
                        fac = rel_x / 0.45
                        cr = int(69 + (220 - 69) * fac)
                        cg = int(10 + (38 - 10) * fac)
                        cb = int(10 + (38 - 10) * fac)
                    else:
                        fac = (rel_x - 0.45) / 0.55
                        cr = int(220 + (127 - 220) * fac)
                        cg = int(38 + (29 - 38) * fac)
                        cb = int(38 + (29 - 38) * fac)
                draw.line([(rx1 + x, 0), (rx1 + x, sh - 1)], fill=(cr, cg, cb, 255))
            cap_h = max(3, 4 * scale // 2)
            cap_col = (148, 163, 184, 255) if is_dark_slate else (234, 179, 8, 255)
            draw.rectangle([rx1, 0, rx2, cap_h], fill=cap_col)
            draw.rectangle([rx1, sh - 1 - cap_h, rx2, sh - 1], fill=cap_col)
            outline_col = (71, 85, 105, 255) if is_dark_slate else (153, 27, 27, 255)
            draw.rectangle([rx1, 0, rx2, sh - 1], outline=outline_col, width=max(1, scale // 2))

        _draw_roller(0, srw - 1)
        _draw_roller(sw - srw, sw - 1)

        res = img.resize((width, height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(res)
        cls._cache[key] = photo
        return photo

    @classmethod
    def create_rounded_pill_button(cls, parent, text, width, height, bg_top="#1e293b", bg_bot="#0f172a",
                                   border_color="#475569", fg_color="#f8fafc", font=("Segoe UI", 8, "bold"),
                                   command=None, radius=10, **kwargs):
        """Creates a supersampled anti-aliased rounded glass pill button."""
        return ShinobiPillButton(parent, text=text, width=width, height=height, bg_top=bg_top, bg_bot=bg_bot,
                                 border_color=border_color, fg_color=fg_color, font=font, command=command,
                                 radius=radius, **kwargs)


class ShinobiPillButton(tk.Canvas):
    """
    3x Supersampled Anti-Aliased Rounded Pill Button:
    - Renders smooth rounded glass pills using ShinobiGraphicsEngine.
    - Duck-typed drop-in replacement for tk.Button:
      supports .config(text=..., bg=..., fg=..., state=..., command=...),
      .cget(), and standard pack/grid/place geometry managers.
    """
    def __init__(self, parent, text="", width=100, height=32, bg_top="#1e293b", bg_bot="#0f172a",
                 border_color="#475569", fg_color="#f8fafc", font=("Segoe UI", 8, "bold"),
                 command=None, radius=10, active_bg="#f59e0b", active_fg="#0f172a", **kwargs):
        self._btn_width = int(width)
        self._btn_height = int(height)
        self._radius = radius
        self._text = text
        self._bg_top = bg_top
        self._bg_bot = bg_bot
        self._border_color = border_color
        self._fg_color = fg_color
        self._active_bg = active_bg
        self._active_fg = active_fg
        self._font = font
        self._command = command
        self._state = "normal"
        self._is_hovered = False

        bg_parent = kwargs.pop("bg", None) or kwargs.pop("background", None)
        if not bg_parent:
            try:
                bg_parent = parent.cget("bg")
            except Exception:
                bg_parent = "#0b1120"

        # Pop any tk.Button specific kwargs
        for k in ["padx", "pady", "relief", "bd", "highlightthickness", "activebackground", "activeforeground"]:
            kwargs.pop(k, None)

        super().__init__(parent, width=self._btn_width, height=self._btn_height, bg=bg_parent, bd=0, highlightthickness=0, cursor="hand2", **kwargs)

        self._render_button()

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Configure>", self._on_configure)

    def _render_button(self):
        w = max(10, self.winfo_width() if self.winfo_width() > 10 else self._btn_width)
        h = max(10, self.winfo_height() if self.winfo_height() > 10 else self._btn_height)

        bg_t = self._bg_top
        bg_b = self._bg_bot
        b_col = self._border_color
        fg = self._fg_color

        if self._state == "disabled":
            fg = "#64748b"
            b_col = "#334155"
        elif self._is_hovered:
            b_col = "#f59e0b"

        photo = ShinobiGraphicsEngine.create_rounded_glass_card(
            w, h, radius=self._radius, bg_top=bg_t, bg_bot=bg_b, border_color=b_col, border_width=1
        )
        self.delete("all")
        if photo:
            self._cached_photo = photo
            self.create_image(0, 0, image=photo, anchor="nw")
        else:
            self.create_rectangle(0, 0, w, h, fill=bg_t, outline=b_col)

        self.create_text(w // 2, h // 2, text=self._text, font=self._font, fill=fg)

    def _on_click(self, event=None):
        if self._state != "disabled" and self._command:
            self._command()

    def _on_enter(self, event=None):
        if self._state != "disabled":
            self._is_hovered = True
            self._render_button()

    def _on_leave(self, event=None):
        self._is_hovered = False
        self._render_button()

    def _on_configure(self, event=None):
        self._render_button()

    def config(self, **kwargs):
        self.configure(**kwargs)

    def configure(self, **kwargs):
        redraw = False
        if "text" in kwargs:
            self._text = kwargs.pop("text")
            redraw = True
        if "command" in kwargs:
            self._command = kwargs.pop("command")
        if "state" in kwargs:
            self._state = kwargs.pop("state")
            if self._state == "disabled":
                super().configure(cursor="")
            else:
                super().configure(cursor="hand2")
            redraw = True
        if "bg" in kwargs or "background" in kwargs:
            bg_val = kwargs.pop("bg", None) or kwargs.pop("background", None)
            self._bg_top = bg_val
            self._bg_bot = bg_val
            redraw = True
        if "bg_top" in kwargs:
            self._bg_top = kwargs.pop("bg_top")
            redraw = True
        if "bg_bot" in kwargs:
            self._bg_bot = kwargs.pop("bg_bot")
            redraw = True
        if "fg" in kwargs or "foreground" in kwargs or "fg_color" in kwargs:
            self._fg_color = kwargs.pop("fg", None) or kwargs.pop("foreground", None) or kwargs.pop("fg_color", None)
            redraw = True
        if "highlightbackground" in kwargs:
            self._border_color = kwargs.pop("highlightbackground")
            redraw = True
        if "border_color" in kwargs:
            self._border_color = kwargs.pop("border_color")
            redraw = True
        if "font" in kwargs:
            self._font = kwargs.pop("font")
            redraw = True
        for k in ["padx", "pady", "relief", "bd", "highlightthickness", "activebackground", "activeforeground"]:
            if k in kwargs:
                kwargs.pop(k)

        if kwargs:
            super().configure(**kwargs)
        if redraw and self.winfo_exists():
            self._render_button()

    def cget(self, key):
        if key == "text":
            return self._text
        if key in ("bg", "background"):
            return self._bg_top
        if key in ("fg", "foreground"):
            return self._fg_color
        if key == "state":
            return self._state
        return super().cget(key)

    def __getitem__(self, item):
        return self.cget(item)

    def __setitem__(self, item, value):
        self.configure(**{item: value})


NARUTO_METADATA = {
    "naruto_sage": {
        "display_name": "🍥 Naruto: Sage Mode & Kurama",
        "character": "Naruto Uzumaki",
        "title": "Seventh Hokage • Master Sage",
        "quote": "I never go back on my word! That's my nindo, my ninja way! Dattebayo!",
        "stylish_letter": "",
        "icon": "🍥",
        "jutsu": "🔥 Sage Art: Massive Rasengan & Kurama Link",
        "rank": "Hokage"
    },
    "sasuke_chidori": {
        "display_name": "⚡ Sasuke: Chidori & Sharingan",
        "character": "Sasuke Uchiha",
        "title": "Shadow Hokage • Uchiha Prodigy",
        "quote": "Concentrate chakra like the Chidori: 100% piercing focus on a single target!",
        "stylish_letter": "",
        "icon": "⚡",
        "jutsu": "⚡ Chidori Lightning Blade & Susanoo Flame",
        "rank": "Shadow Shinobi"
    },
    "kakashi_hatake": {
        "display_name": "🌀 Kakashi: Copy Ninja & Anbu",
        "character": "Kakashi Hatake",
        "title": "Sixth Hokage • Team 7 Captain",
        "quote": "Those who break rules are scum, but those who abandon their routine are worse than scum!",
        "stylish_letter": "",
        "icon": "🌀",
        "jutsu": "⚡ Raikiri & Thousand Years of Training",
        "rank": "Sixth Hokage"
    },
    "minato_flash": {
        "display_name": "⚡ Minato: The Yellow Flash",
        "character": "Minato Namikaze",
        "title": "Fourth Hokage • The Yellow Flash",
        "quote": "Speed and unwavering precision! Clear your homework in a flash with zero delay!",
        "stylish_letter": "",
        "icon": "⚡",
        "jutsu": "🌪️ Flying Thunder God & Spiral Sphere",
        "rank": "Fourth Hokage"
    },
    "itachi_uchiha": {
        "display_name": "🌙 Itachi: Akatsuki & Tsukuyomi",
        "character": "Itachi Uchiha",
        "title": "Uchiha Genius • Leaf Guardian",
        "quote": "Self-mastery is acknowledging your limits and expanding them calmly every single day.",
        "stylish_letter": "",
        "icon": "🌙",
        "jutsu": "👁️ Tsukuyomi & Crow Mirage Illusion",
        "rank": "S-Rank Master"
    },
    "leaf_village": {
        "display_name": "🍃 Konoha: Will of Fire",
        "character": "Hidden Leaf Shinobi",
        "title": "Konohagakure • Will of Fire",
        "quote": "Where tree leaves dance, one shall find flame. The fire's shadow illuminates the village!",
        "stylish_letter": "",
        "icon": "🍃",
        "jutsu": "🍃 Leaf Hurricane & Will of Fire",
        "rank": "Leaf Champion"
    },
    "dark": {
        "display_name": "🌙 Classic Dark Slate",
        "character": "Classic Dark",
        "title": "Standard Slate Interface",
        "quote": "Quiet focus and clear concentration.",
        "stylish_letter": "",
        "icon": "🌙",
        "jutsu": "Focused Mind",
        "rank": "Scholar"
    },
    "light": {
        "display_name": "☀️ Classic Light Day",
        "character": "Classic Light",
        "title": "Daylight Paper Interface",
        "quote": "Clear vision and bright morning energy.",
        "stylish_letter": "",
        "icon": "☀️",
        "jutsu": "Daylight Study",
        "rank": "Scholar"
    }
}


class ShinobiPillSelector(tk.Frame):
    """
    Custom Rounded Dark-Glass Selector Card with Native Dark Popup Menu:
    Replaces clunky Win32 ttk.Combobox with high-polish dark card (radius=12, bg=#131c2e, border=#334155).
    Fully compatible with ttk.Combobox methods: ['values'], .current(), .set(), .get(), .configure().
    """
    def __init__(self, parent, title="", values=None, initial_value="", on_select_callback=None, textvariable=None, width=120, height=None, title_color=None, **kwargs):
        self.title = title or ""
        self.title_color = title_color
        self.values = list(values) if values else []
        self.current_value = str(initial_value) if initial_value else ""
        self.on_select_callback = on_select_callback
        self.textvariable = textvariable

        if "state" in kwargs:
            kwargs.pop("state")
        if "width" in kwargs:
            width = kwargs.pop("width")
        if "height" in kwargs:
            height = kwargs.pop("height")

        bg_col = "#161f30"
        super().__init__(parent, bg=bg_col, bd=1, relief=tk.SOLID, highlightbackground="#2e3b52", highlightthickness=1, cursor="hand2", **kwargs)

        px_w = int(width * 8 + 30) if (width and width <= 35) else int(width if width else 120)
        px_h = int(height) if height else (32 if not self.title else 40)
        self._pill_width = px_w
        self._pill_height = px_h

        super().configure(width=px_w, height=px_h)
        self.pack_propagate(False)

        if self.title:
            self.lbl_title = tk.Label(self, text=self.title, font=("Segoe UI", 7, "bold"), fg=self.title_color or "#fb923c", bg=bg_col, anchor="w")
            self.lbl_title.pack(anchor="w", padx=6, pady=(2, 0))
        else:
            self.lbl_title = None

        val_row = tk.Frame(self, bg=bg_col)
        val_row.pack(fill=tk.BOTH, expand=True, padx=6, pady=(1 if self.title else 2, 2))
        self.val_row = val_row

        disp_txt = self.current_value if self.current_value else (self.values[0] if self.values else "")
        self.current_value = disp_txt
        formatted_txt = self._format_display_text(disp_txt)
        self.lbl_val = tk.Label(val_row, text=formatted_txt, font=("Segoe UI", 8, "bold"), fg="#f8fafc", bg=bg_col, anchor="w")
        self.lbl_val.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.lbl_chev = tk.Label(val_row, text="▾", font=("Segoe UI", 8, "bold"), fg="#fb923c", bg=bg_col)
        self.lbl_chev.pack(side=tk.RIGHT)

        widgets = [self, self.val_row, self.lbl_val, self.lbl_chev]
        if self.lbl_title:
            widgets.append(self.lbl_title)
        for w in widgets:
            w.bind("<Button-1>", self._popup_menu)
            w.bind("<Enter>", lambda e: self.configure(highlightbackground="#f59e0b"))
            w.bind("<Leave>", lambda e: self.configure(highlightbackground="#334155"))

        if self.textvariable:
            def _on_var_write(*args):
                val = self.textvariable.get()
                if val != self.current_value:
                    self.set(val)
            self.textvariable.trace_add("write", _on_var_write)
            if self.textvariable.get():
                self.set(self.textvariable.get())

    _active_popup = None

    @classmethod
    def close_active_popup(cls):
        if cls._active_popup and cls._active_popup.winfo_exists():
            try:
                cls._active_popup.unbind_all("<MouseWheel>")
            except Exception:
                pass
            try:
                cls._active_popup.destroy()
            except Exception:
                pass
        cls._active_popup = None

    @staticmethod
    def _parse_dropdown_item_info(val):
        txt = str(val).strip()
        DROPDOWN_ITEM_METADATA = {
            "🌿 Balanced Daily": ("🌿", "Balanced Daily Routine", "CBSE Senthil Diary Balanced Routine (Levels 1–3)"),
            "🔥 Exam Sprint": ("🔥", "Exam Eve Sprint", "3-Stage Cognitive Mastery & Kit Audit"),
            "Level 1: 🔰 Genin": ("🔰", "Level 1: Genin", "15m Focus Slabs • Sitting Endurance Building"),
            "Level 2: ⚡ Chunin": ("⚡", "Level 2: Chunin", "30m Standard Slabs • Balanced Daily Study Habit"),
            "Level 3: 🔥 Jonin": ("🔥", "Level 3: Jonin", "45m Deep Work • Peak Cognitive Mastery"),
            "7:00 PM": ("🕒", "7:00 PM Focus", "Standard Evening Focus Routine (Default)"),
            "5:00 PM": ("🕒", "5:00 PM Focus", "Early Evening Focus Session"),
            "10:00 AM": ("☀️", "10:00 AM Focus", "Holiday & Weekend Morning Session"),
            "2:00 PM": ("🌤️", "2:00 PM Focus", "Weekend Afternoon Study Block"),
            "⚡ Start Now": ("⚡", "Start Right Now", "Align Schedule Start with Live System Clock"),
            "✏️ Custom Time...": ("✏️", "Custom Start Time", "Set Any Custom Hour & Minute for Routine"),
            "Custom Time": ("✏️", "Custom Start Time", "Set Any Custom Hour & Minute for Routine"),
            "Tamil": ("📖", "Tamil (09.09)", "Grammar, Prose & Thirukkural Memorization"),
            "Mathematics": ("📐", "Mathematics (11.09)", "Ch 1-8 Concepts, Formulas & Hand Solving"),
            "Physical Science": ("🔬", "Physical Science (16.09)", "Physics Laws, Equations & Numerical Practice"),
            "Social Science": ("🌍", "Social Science (18.09)", "History, Geography Maps & Civics Concepts"),
            "Hindi": ("📝", "Hindi (22.09)", "Grammar, Comprehension & Essay Writing"),
            "Biological Science": ("🧬", "Biological Science (24.09)", "Labeled Anatomy Diagrams & Recall"),
            "English": ("📚", "English (26.09)", "Literature, Formal Writing & Vocabulary"),
        }
        if txt in DROPDOWN_ITEM_METADATA:
            return DROPDOWN_ITEM_METADATA[txt]

        for k, meta in NARUTO_METADATA.items():
            if meta.get("display_name") == txt:
                icon_map = {
                    "naruto_sage": "🍥", "sasuke_chidori": "⚡", "kakashi_hatake": "👁️",
                    "minato_flash": "🟡", "itachi_uchiha": "🔴", "leaf_village": "🍃",
                    "dark": "🌑", "light": "📜"
                }
                icon = icon_map.get(k, "🍥")
                title = meta.get("display_name", txt)
                sub = meta.get("jutsu", "")
                return icon, title, sub

        if txt.startswith("Day ") and ":" in txt:
            parts = txt.split(":", 1)
            day_tag = parts[0].strip()
            day_title = parts[1].strip()
            return "🎯", day_tag, day_title

        if "Pre-Exam Planner" in txt:
            return "📅", txt, "Dynamic Multi-Day Horizon & Exam Portions"

        if (txt.endswith("PM") or txt.endswith("AM")) and (":" in txt or any(c.isdigit() for c in txt)):
            return "🕒", f"{txt} Focus", "Custom Scheduled Study Routine"

        if "(" in txt and ")" in txt:
            idx = txt.index("(")
            dt = txt[:idx].strip()
            subs = txt[idx+1:txt.rindex(")")].strip()
            return "📅", dt, f"Subjects: {subs}"

        emojis = ['🌿', '🔥', '📅', '⚡', '🍥', '👁️', '🟡', '🔴', '🍃', '🌑', '📜', '🔰', '🕒', '☀️', '🌤️', '📐', '🔬', '🌍', '📝', '🧬', '📚', '📖', '🎨', '🎯', '✏️']
        for em in emojis:
            if txt.startswith(em):
                rem = txt[len(em):].strip()
                return em, rem, ""

        return "✦", txt, ""

    def _rebuild_menu(self):
        pass

    def _popup_menu(self, event=None):
        if ShinobiPillSelector._active_popup:
            prev = ShinobiPillSelector._active_popup
            ShinobiPillSelector.close_active_popup()
            if getattr(prev, "_owner_pill", None) == self:
                return

        if not self.values:
            return

        popup = tk.Toplevel(self)
        popup._owner_pill = self
        ShinobiPillSelector._active_popup = popup

        popup.overrideredirect(True)
        try:
            popup.attributes("-topmost", True)
        except Exception:
            pass

        popup.configure(bg="#0c1322", bd=1, relief=tk.SOLID, highlightthickness=1, highlightbackground="#d97706")

        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 2
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        popup_w = max(self.winfo_width(), 310)

        # Check subtitle presence to accurately gauge required height
        parsed_items = [self._parse_dropdown_item_info(v) for v in self.values]
        has_sub = any(bool(s) for _, _, s in parsed_items)
        card_est_h = 52 if has_sub else 38
        total_items_h = len(self.values) * card_est_h + 16

        max_allowed_h = min(380, screen_h - 100)
        use_scroll = total_items_h > max_allowed_h

        if use_scroll:
            popup_h = max_allowed_h
            canvas = tk.Canvas(popup, bg="#0c1322", highlightthickness=0)
            scrollbar = tk.Scrollbar(popup, orient=tk.VERTICAL, command=canvas.yview, width=6, bg="#0f172a", troughcolor="#0c1322", bd=0, relief=tk.FLAT)
            canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            inner = tk.Frame(canvas, bg="#0c1322", padx=2, pady=2)
            inner_id = canvas.create_window((0, 0), window=inner, anchor="nw", width=popup_w - 10)

            def _on_cfg(e):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(inner_id, width=canvas.winfo_width())
            inner.bind("<Configure>", _on_cfg)
            canvas.bind("<Configure>", lambda e: canvas.itemconfig(inner_id, width=e.width))

            def _on_wheel(e):
                try:
                    canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
                except Exception:
                    pass
            popup.bind_all("<MouseWheel>", _on_wheel)
            container = inner
            for val in self.values:
                self._create_dropdown_item_card(container, val, popup)
            popup.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        else:
            container = tk.Frame(popup, bg="#0c1322", padx=4, pady=4)
            container.pack(fill=tk.BOTH, expand=True)
            for val in self.values:
                self._create_dropdown_item_card(container, val, popup)
            popup.update_idletasks()
            popup_h = popup.winfo_reqheight() + 4

        if x + popup_w > screen_w - 10:
            x = max(10, screen_w - popup_w - 10)
        if y + popup_h > screen_h - 40:
            y = max(10, self.winfo_rooty() - popup_h - 2)

        popup.geometry(f"{popup_w}x{popup_h}+{x}+{y}")

        def _check_click_outside(e):
            if not popup.winfo_exists():
                return
            try:
                px = popup.winfo_rootx()
                py = popup.winfo_rooty()
                pw = popup.winfo_width()
                ph = popup.winfo_height()
                if not (px <= e.x_root <= px + pw and py <= e.y_root <= py + ph):
                    ShinobiPillSelector.close_active_popup()
            except Exception:
                ShinobiPillSelector.close_active_popup()

        popup.bind("<FocusOut>", lambda e: ShinobiPillSelector.close_active_popup())
        popup.bind("<Escape>", lambda e: ShinobiPillSelector.close_active_popup())
        try:
            self.winfo_toplevel().bind("<Button-1>", _check_click_outside, add="+")
        except Exception:
            pass
        popup.focus_set()

    def _create_dropdown_item_card(self, container, val, popup):
        is_selected = (str(val).strip() == str(self.current_value).strip())
        icon, title, sub = self._parse_dropdown_item_info(val)

        item_bg = "#162032" if is_selected else "#0f172a"
        border_col = "#f59e0b" if is_selected else "#1e293b"

        card = tk.Frame(
            container,
            bg=item_bg,
            bd=1,
            relief=tk.SOLID,
            highlightthickness=1,
            highlightbackground=border_col,
            cursor="hand2"
        )
        card.pack(fill=tk.X, padx=4, pady=2)

        badge_frame = tk.Frame(card, bg="#1e293b", width=28, height=28)
        badge_frame.pack_propagate(False)
        badge_frame.pack(side=tk.LEFT, padx=(6, 8), pady=4)
        lbl_icon = tk.Label(badge_frame, text=icon, font=("Segoe UI Emoji", 11), fg="#f59e0b", bg="#1e293b")
        lbl_icon.pack(expand=True)

        txt_box = tk.Frame(card, bg=item_bg)
        txt_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=3)

        title_col = "#fbbf24" if is_selected else "#f8fafc"
        lbl_t = tk.Label(txt_box, text=title, font=("Segoe UI", 8, "bold"), fg=title_col, bg=item_bg, anchor="w")
        lbl_t.pack(anchor="w")

        lbl_s = None
        if sub:
            lbl_s = tk.Label(txt_box, text=sub, font=("Segoe UI", 7), fg="#94a3b8", bg=item_bg, anchor="w")
            lbl_s.pack(anchor="w")

        check_txt = "✓" if is_selected else ""
        lbl_chk = tk.Label(card, text=check_txt, font=("Segoe UI", 9, "bold"), fg="#f59e0b", bg=item_bg, width=3)
        lbl_chk.pack(side=tk.RIGHT, padx=(0, 6))

        all_widgets = [card, badge_frame, lbl_icon, txt_box, lbl_t, lbl_chk]
        if lbl_s:
            all_widgets.append(lbl_s)

        def _on_enter(e):
            card.configure(bg="#1e293b", highlightbackground="#f59e0b")
            txt_box.configure(bg="#1e293b")
            lbl_t.configure(bg="#1e293b", fg="#fbbf24")
            if lbl_s: lbl_s.configure(bg="#1e293b")
            lbl_chk.configure(bg="#1e293b")

        def _on_leave(e):
            if is_selected:
                card.configure(bg="#162032", highlightbackground="#f59e0b")
                txt_box.configure(bg="#162032")
                lbl_t.configure(bg="#162032", fg="#fbbf24")
                if lbl_s: lbl_s.configure(bg="#162032")
                lbl_chk.configure(bg="#162032")
            else:
                card.configure(bg="#0f172a", highlightbackground="#1e293b")
                txt_box.configure(bg="#0f172a")
                lbl_t.configure(bg="#0f172a", fg="#f8fafc")
                if lbl_s: lbl_s.configure(bg="#0f172a")
                lbl_chk.configure(bg="#0f172a")

        def _on_click(e):
            ShinobiPillSelector.close_active_popup()
            self._select_val(val)

        for w in all_widgets:
            w.bind("<Enter>", _on_enter)
            w.bind("<Leave>", _on_leave)
            w.bind("<Button-1>", _on_click)

    def _select_val(self, val):
        self.set(val)
        if self.on_select_callback:
            self.on_select_callback(val)

    def _format_display_text(self, val):
        txt = str(val) if val is not None else ""
        max_chars = max(22, int(getattr(self, "_pill_width", 120) / 7.2))
        if len(txt) > max_chars:
            txt = txt[:max_chars - 1] + "…"
        return txt

    def set(self, val):
        self.current_value = str(val)
        if self.textvariable and self.textvariable.get() != self.current_value:
            self.textvariable.set(self.current_value)
        self.lbl_val.configure(text=self._format_display_text(self.current_value))

    def get(self):
        return self.current_value

    def configure_values(self, values):
        self.values = list(values)
        self._rebuild_menu()

    def current(self, newindex=None):
        if newindex is None:
            try:
                return self.values.index(self.current_value)
            except ValueError:
                return -1
        else:
            if 0 <= newindex < len(self.values):
                self.set(self.values[newindex])
                if self.on_select_callback:
                    self.on_select_callback(self.values[newindex])

    def __getitem__(self, item):
        if item == "values":
            return self.values
        return super().cget(item)

    def __setitem__(self, item, value):
        if item == "values":
            self.configure_values(value)
        else:
            self.configure(**{item: value})

    def configure(self, **kwargs):
        if "values" in kwargs:
            self.configure_values(kwargs.pop("values"))
        if "state" in kwargs:
            kwargs.pop("state")
        if "width" in kwargs:
            w = kwargs.pop("width")
            if w is not None:
                px_w = int(w * 8 + 30) if w <= 35 else int(w)
                self._pill_width = px_w
                super().configure(width=px_w)
                if hasattr(self, "lbl_val"):
                    self.lbl_val.configure(text=self._format_display_text(self.current_value))
        if "height" in kwargs:
            h = kwargs.pop("height")
            if h is not None:
                self._pill_height = int(h)
                super().configure(height=self._pill_height)
        if kwargs:
            super().configure(**kwargs)

    def config(self, **kwargs):
        self.configure(**kwargs)

    def bind(self, sequence=None, func=None, add=None):
        if sequence == "<<ComboboxSelected>>":
            orig_cb = self.on_select_callback
            def _combo_sel_wrapper(v):
                if orig_cb:
                    orig_cb(v)
                if func:
                    func(None)
            self.on_select_callback = _combo_sel_wrapper
        else:
            super().bind(sequence, func, add)



class ShinobiTabBar(tk.Frame):
    """
    3D Glowing Scroll & Rounded Dark-Glass Tab Navigation Bar:
    - Active Tab: True 3D cylindrical parchment scroll (create_3d_parchment_scroll) with dark ink text (#1f1206) and golden bottom indicator glow.
    - Inactive Tabs: Rounded dark-glass pills (radius=10, bg=#131c2e, border=#334155, fg=#94a3b8, hover=#f59e0b).
    """
    def __init__(self, parent, notebook, on_tab_changed=None, **kwargs):
        super().__init__(parent, bg="#0b1120", height=42, **kwargs)
        self.notebook = notebook
        self.on_tab_changed = on_tab_changed
        self.pack_propagate(False)

        self.tab_defs = []
        self.tab_widgets = {}
        self.active_tab_id = None
        self.active_indicator_color = "#f59e0b" 

    def set_tabs(self, tabs_info):
        """
        tabs_info: list of (tab_id, tab_frame, icon, title)
        """
        self.tab_defs = tabs_info
        for w in self.winfo_children():
            w.destroy()
        self.tab_widgets.clear()

        for tab_id, tab_frame, icon, title in tabs_info:
            tab_card = tk.Canvas(self, height=36, bg="#0b1120", bd=0, highlightthickness=0, cursor="hand2")
            tab_card.pack(side=tk.LEFT, padx=(0, 10))
            self.tab_widgets[tab_id] = {
                "canvas": tab_card,
                "frame": tab_frame,
                "icon": icon,
                "title": title,
                "hover": False
            }

            def _bind_tab(t_id=tab_id, c=tab_card):
                c.bind("<Button-1>", lambda e: self.select_tab(t_id))
                c.bind("<Enter>", lambda e: self._on_hover(t_id, True))
                c.bind("<Leave>", lambda e: self._on_hover(t_id, False))
                c.bind("<Configure>", lambda e: self._draw_tab(t_id))

            _bind_tab(tab_id, tab_card)

        self._refresh_all_tabs()

    def select_tab(self, tab_id):
        self.active_tab_id = tab_id
        if tab_id in self.tab_widgets:
            target_frame = self.tab_widgets[tab_id]["frame"]
            try:
                self.notebook.select(target_frame)
            except Exception:
                pass
        self._refresh_all_tabs()
        if self.on_tab_changed:
            self.on_tab_changed(tab_id)

    def _on_hover(self, tab_id, is_hover):
        if tab_id in self.tab_widgets:
            self.tab_widgets[tab_id]["hover"] = is_hover
            self._draw_tab(tab_id)

    def _draw_tab(self, tab_id):
        info = self.tab_widgets.get(tab_id)
        if not info:
            return
        c = info["canvas"]
        title_text = f"{info['icon']}  {info['title']}"
        is_active = (self.active_tab_id == tab_id)
        
        tw = len(title_text) * 8 + 48
        w = max(tw, c.winfo_width() if c.winfo_width() > 10 else tw)
        h = 36
        c.configure(width=w, height=h)
        c.delete("all")

        if is_active:
            # 3D Shaded Cylindrical Parchment Scroll (Active: Cream Parchment + Golden Bottom Indicator)
            photo = ShinobiGraphicsEngine.create_3d_parchment_scroll(w, h, roller_width=16, is_dark_slate=False)
            if photo:
                c._active_photo = photo
                c.create_image(0, 0, image=photo, anchor="nw")
            else:
                c.create_rectangle(0, 0, w, h, fill="#fdf3dc", outline="#d97706")
            
            c.create_text(w // 2, h // 2, text=title_text, font=("Segoe UI", 9, "bold"), fill="#1f1206")
            # Glowing 3px underline bar matching active theme primary/accent
            ind_col = getattr(self, "active_indicator_color", "#f59e0b")
            c.create_line(16, h - 2, w - 16, h - 2, fill=ind_col, width=3)
        else:
            # 3D Dark-Slate Scroll with Dark Crimson Cylindrical Rollers
            photo = ShinobiGraphicsEngine.create_3d_parchment_scroll(w, h, roller_width=16, is_dark_slate=True)
            if photo:
                c._inactive_photo = photo
                c.create_image(0, 0, image=photo, anchor="nw")
            else:
                c.create_rectangle(0, 0, w, h, fill="#161f30", outline="#334155")

            fg_col = "#ffffff" if info.get("hover") else "#cbd5e1"
            c.create_text(w // 2, h // 2, text=title_text, font=("Segoe UI", 8, "bold"), fill=fg_col)

    def _refresh_all_tabs(self):
        for tab_id in self.tab_widgets:
            self._draw_tab(tab_id)


