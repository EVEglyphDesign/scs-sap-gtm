# -*- coding: utf-8 -*-
"""Steel Cloud Solutions house-style DOCX renderer.

Same authoring API as the EVEglyphDesign canon PDF renderer, so the contract
content modules (msa.py, sow.py, supplier.py) are used unchanged. Visual system
is the Steel Cloud Solutions template: red #e33e2b, navy #1e3a5f, charcoal
#2b2b2b, cream #fdfaf4, condensed display type over Arial body.
"""
import hashlib, re
from datetime import datetime, timezone
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------------------------------------------------------------- brand tokens
RED = "e33e2b"
NAVY = "1e3a5f"
DARK = "2b2b2b"
CHARCOAL = "3a3a3a"
LINE = "d8d8d8"
MUTE = "6b6b6b"
CREAM = "fdfaf4"
OFF = "f5f3ee"
WHITE = "ffffff"

DISPLAY = "Arial Narrow"   # stands in for Barlow Condensed on any machine
BODY = "Arial"

KEY_ID = "EgD-KEY-2026-07"
inch = 72.0  # content modules express widths as `n * inch` (points)

S = {k: k for k in ("title", "subtitle", "h1", "h2", "body", "bullet", "note",
                    "cell", "cellh", "sig", "kicker")}


# ------------------------------------------------------------------ flow types
class Flow:
    pass


class P(Flow):
    def __init__(self, t, s="body"):
        self.t, self.s = t, s


class B(Flow):
    def __init__(self, t):
        self.t = t


class H1(Flow):
    def __init__(self, t):
        self.t = t


class H2(Flow):
    def __init__(self, t):
        self.t = t


class NOTE(Flow):
    def __init__(self, t):
        self.t = "Drafting note — " + t


class TBL(Flow):
    def __init__(self, rows, widths, header=True):
        self.rows, self.widths, self.header = rows, widths, header


class PANEL(Flow):
    def __init__(self, flows, accent=True):
        self.flows, self.accent = flows, accent


class SIGBLOCK(Flow):
    def __init__(self, left_name, left_lines, right_name, right_lines):
        self.left = (left_name, left_lines)
        self.right = (right_name, right_lines)


class Spacer(Flow):
    def __init__(self, w=1, h=8):
        self.h = h


class PageBreak(Flow):
    pass


class KeepTogether(Flow):
    def __init__(self, flows):
        self.flows = flows if isinstance(flows, (list, tuple)) else [flows]


class RULE(Flow):
    def __init__(self, color=RED, width=2.2):
        self.color, self.width = color, width


# ------------------------------------------------------------------- xml utils
def _shade(el, hexcolor):
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hexcolor)
    el.append(sh)


def _borders(pPr_or_tcPr, spec):
    """spec: {'left': (size_eighths, hex), ...} ; size in 1/8 pt."""
    tag = "w:pBdr" if pPr_or_tcPr.tag.endswith("pPr") else "w:tcBorders"
    bd = OxmlElement(tag)
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement("w:" + side)
        if side in spec:
            sz, col = spec[side]
            e.set(qn("w:val"), "single")
            e.set(qn("w:sz"), str(sz))
            e.set(qn("w:space"), "0")
            e.set(qn("w:color"), col)
        else:
            e.set(qn("w:val"), "nil")
        bd.append(e)
    pPr_or_tcPr.append(bd)


def _spacing(par, before=0, after=6, line=None):
    pf = par.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line:
        pf.line_spacing = line


def _runs(par, text, font=BODY, size=9.5, color=DARK, italic=False, bold=False,
          caps=False, spacing=None):
    """Render the limited inline markup used by the contract sources (<b>)."""
    text = text.replace("&nbsp;", "\u00a0")
    for chunk in re.split(r"(<b>.*?</b>)", text, flags=re.S):
        if not chunk:
            continue
        strong = chunk.startswith("<b>")
        body = re.sub(r"</?b>", "", chunk)
        r = par.add_run(body.upper() if caps else body)
        r.font.name = font
        r.font.size = Pt(size)
        r.font.color.rgb = RGBColor.from_string(color.upper())
        r.italic = italic
        r.bold = bold or strong
        rpr = r._element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts")
            rpr.append(rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), font)
        if spacing:
            sp = OxmlElement("w:spacing")
            sp.set(qn("w:val"), str(int(spacing * 20)))
            rpr.append(sp)
    return par


def _field(par, instr):
    r = par.add_run()
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
    r._element.append(f1); r._element.append(it); r._element.append(f2)
    return r


# -------------------------------------------------------------- flow renderers
def _emit(container, flow, doc):
    if isinstance(flow, KeepTogether):
        items = flow.flows
        for i, sub in enumerate(items):
            _emit(container, sub, doc)
        return
    if isinstance(flow, PageBreak):
        p = container.add_paragraph()
        p.add_run().add_break(WD_BREAK.PAGE)
        return
    if isinstance(flow, Spacer):
        p = container.add_paragraph()
        _spacing(p, 0, 0)
        p.paragraph_format.line_spacing = Pt(max(flow.h, 2))
        return
    if isinstance(flow, RULE):
        p = container.add_paragraph()
        _spacing(p, 2, 8)
        _borders(p._p.get_or_add_pPr(),
                 {"bottom": (int(flow.width * 8), flow.color)})
        return
    if isinstance(flow, H1):
        p = container.add_paragraph()
        _spacing(p, 14, 5)
        _runs(p, flow.t, font=DISPLAY, size=14, color=NAVY, bold=True, spacing=0.2)
        _borders(p._p.get_or_add_pPr(), {"bottom": (8, LINE)})
        p.paragraph_format.keep_with_next = True
        return
    if isinstance(flow, H2):
        p = container.add_paragraph()
        _spacing(p, 10, 3)
        _runs(p, flow.t, font=DISPLAY, size=10.5, color=RED, bold=True, caps=True,
              spacing=0.6)
        p.paragraph_format.keep_with_next = True
        return
    if isinstance(flow, NOTE):
        p = container.add_paragraph()
        _spacing(p, 4, 8)
        pPr = p._p.get_or_add_pPr()
        _shade(pPr, OFF)
        _borders(pPr, {"left": (18, RED)})
        p.paragraph_format.left_indent = Pt(16)
        p.paragraph_format.right_indent = Pt(8)
        _runs(p, flow.t, size=8.8, color=MUTE, italic=True)
        return
    if isinstance(flow, P):
        p = container.add_paragraph()
        st = flow.s
        if st == "title":
            _spacing(p, 0, 4)
            _runs(p, flow.t, font=DISPLAY, size=27, color=DARK, bold=True, spacing=0.2)
        elif st == "subtitle":
            _spacing(p, 0, 12)
            _runs(p, flow.t, size=11, color=MUTE)
        elif st == "kicker":
            _spacing(p, 0, 4)
            _runs(p, flow.t, font=DISPLAY, size=9, color=RED, bold=True, caps=True,
                  spacing=1.0)
        elif st == "note":
            _spacing(p, 0, 6)
            _runs(p, flow.t, size=8.6, color=MUTE, italic=True)
        elif st == "sig":
            _spacing(p, 0, 10)
            _runs(p, flow.t, size=9.5, color=DARK)
        else:
            _spacing(p, 0, 7)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            _runs(p, flow.t, size=9.5, color=DARK)
            p.paragraph_format.line_spacing = 1.15
        return
    if isinstance(flow, B):
        p = container.add_paragraph()
        _spacing(p, 0, 5)
        p.paragraph_format.left_indent = Pt(18)
        p.paragraph_format.first_line_indent = Pt(-11)
        _runs(p, "\u2014\u2002" + flow.t, size=9.5, color=DARK)
        p.paragraph_format.line_spacing = 1.12
        return
    if isinstance(flow, TBL):
        _table(container, flow, doc)
        return
    if isinstance(flow, PANEL):
        t = container.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        cell = t.cell(0, 0)
        cell.width = Inches(6.7)
        tcPr = cell._tc.get_or_add_tcPr()
        _shade(tcPr, CREAM)
        _borders(tcPr, {"left": (24, RED if flow.accent else LINE),
                        "top": (4, LINE), "bottom": (4, LINE), "right": (4, LINE)})
        cell.paragraphs[0]._p.getparent().remove(cell.paragraphs[0]._p)
        for sub in flow.flows:
            _emit(cell, sub, doc)
        for p in cell.paragraphs:
            p.paragraph_format.space_after = Pt(2)
        _emit(container, Spacer(1, 8), doc)
        return
    if isinstance(flow, SIGBLOCK):
        t = container.add_table(rows=1, cols=2)
        t.autofit = False
        for idx, (name, lines) in enumerate((flow.left, flow.right)):
            cell = t.cell(0, idx)
            cell.width = Inches(3.35)
            _borders(cell._tc.get_or_add_tcPr(), {})
            cell.paragraphs[0]._p.getparent().remove(cell.paragraphs[0]._p)
            _emit(cell, P(name, "kicker"), doc)
            for l in lines:
                _emit(cell, P(l + "\u00a0\u00a0\u00a0" + "_" * 28, "sig"), doc)
        _emit(container, Spacer(1, 8), doc)
        return
    raise TypeError(f"unhandled flow {flow!r}")


def _table(container, flow, doc):
    rows, widths, header = flow.rows, flow.widths, flow.header
    ncols = len(rows[0])
    t = container.add_table(rows=0, cols=ncols)
    t.autofit = False
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, r in enumerate(rows):
        cells = t.add_row().cells
        head = header and i == 0
        for j, val in enumerate(r):
            c = cells[j]
            c.width = Emu(int(widths[j] / 72.0 * 914400))
            tcPr = c._tc.get_or_add_tcPr()
            if head:
                _shade(tcPr, NAVY)
            elif i % 2 == 0:
                _shade(tcPr, OFF)
            else:
                _shade(tcPr, WHITE)
            _borders(tcPr, {"bottom": (4, LINE)})
            p = c.paragraphs[0]
            _spacing(p, 3, 3)
            _runs(p, str(val), size=8.6,
                  color=WHITE if head else DARK, bold=head)
            if head:
                p.paragraph_format.keep_with_next = True
    # repeat header row on page breaks
    if header and len(t.rows):
        trPr = t.rows[0]._tr.get_or_add_trPr()
        h = OxmlElement("w:tblHeader")
        h.set(qn("w:val"), "true")
        trPr.append(h)
    _emit(container, Spacer(1, 8), doc)
    return t


# ------------------------------------------------------------------ page frame
def _frame(doc, code, short_title, sha):
    sec = doc.sections[0]
    sec.left_margin = Inches(0.9)
    sec.right_margin = Inches(0.9)
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.8)
    sec.header_distance = Inches(0.4)
    sec.footer_distance = Inches(0.35)

    hp = sec.header.paragraphs[0]
    hp.paragraph_format.tab_stops.add_tab_stop(Inches(1.9),
                                               WD_ALIGN_PARAGRAPH.LEFT)
    _runs(hp, "Steel Cloud Solutions", font=DISPLAY, size=9, color=NAVY,
          bold=True, caps=True, spacing=1.0)
    _runs(hp, "\t" + code + " \u00b7 " + short_title, size=7.5, color=MUTE)
    _borders(hp._p.get_or_add_pPr(), {"bottom": (18, RED)})
    _spacing(hp, 0, 6)

    fp = sec.footer.paragraphs[0]
    fp.paragraph_format.tab_stops.add_tab_stop(Inches(6.7),
                                               WD_ALIGN_PARAGRAPH.RIGHT)
    _borders(fp._p.get_or_add_pPr(), {"top": (4, LINE)})
    _spacing(fp, 4, 0)
    _runs(fp, f"\u00a9 2026 Steel Cloud Solutions, LLC \u00b7 controlled draft \u00b7 "
              f"{KEY_ID} \u00b7 SHA-256 {sha[:16]}\u2026",
          size=6.8, color=MUTE)
    _runs(fp, "\tPage ", size=6.8, color=MUTE)
    _field(fp, "PAGE")
    _runs(fp, " of ", size=6.8, color=MUTE)
    _field(fp, "NUMPAGES")
    for r in fp.runs:
        r.font.size = Pt(6.8)
        r.font.name = BODY
        r.font.color.rgb = RGBColor.from_string(MUTE.upper())


def cover(code, title, subtitle, meta_rows, stamp):
    return [P("Steel Cloud Solutions \u00b7 " + code, "kicker"),
            P(title, "title"),
            RULE(RED, 2.4),
            P(subtitle, "subtitle"),
            TBL(meta_rows, [1.75 * inch, 4.95 * inch], header=False),
            Spacer(1, 10),
            P(stamp, "note")]


def build(path, code, short_title, flows_fn, source_text):
    sha = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = BODY
    st.font.size = Pt(9.5)
    st.element.rPr.rFonts.set(qn("w:ascii"), BODY)
    st.element.rPr.rFonts.set(qn("w:hAnsi"), BODY)
    doc.core_properties.title = short_title
    doc.core_properties.author = "EVEglyphDesign"
    doc.core_properties.comments = f"{code} · SHA-256 {sha}"
    _frame(doc, code, short_title, sha)
    for p in list(doc.paragraphs):
        p._p.getparent().remove(p._p)
    for flow in flows_fn(sha, ts):
        _emit(doc, flow, doc)
    doc.save(path)
    return sha, ts, None
