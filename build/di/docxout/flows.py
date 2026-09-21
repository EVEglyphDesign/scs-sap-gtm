# -*- coding: utf-8 -*-
"""HTML-to-flow bridge for the Steel Cloud Solutions house-style DOCX renderer.

`content.py` is the single source of copy for all three surfaces (canon PDF,
public HTML page, SCS Word document). This module converts that HTML body into
the flow objects `docxout/render.py` already understands, and adds clickable
hyperlink runs so the canon rule "clickable links only" survives into Word.

No visual decisions are made here. Sizes, colours and spacing all come from
render.py's Steel Cloud Solutions token set.
"""
import re
from html.parser import HTMLParser

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

import render as R

_BASE_EMIT = R._emit


# --------------------------------------------------------------- rich inline runs
def _hyperlink(par, url, text, size, color=R.NAVY, bold=False, italic=False):
    part = par.part
    rid = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), rid)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rf = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), R.BODY)
    rPr.append(rf)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size * 2)))
    rPr.append(sz)
    col = OxmlElement("w:color")
    col.set(qn("w:val"), color.upper())
    rPr.append(col)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)
    if bold:
        rPr.append(OxmlElement("w:b"))
    if italic:
        rPr.append(OxmlElement("w:i"))
    run.append(rPr)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    run.append(t)
    link.append(run)
    par._p.append(link)


_ENT = {
    "&mdash;": "\u2014", "&ndash;": "\u2013", "&nbsp;": "\u00a0",
    "&ldquo;": "\u201c", "&rdquo;": "\u201d", "&lsquo;": "\u2018",
    "&rsquo;": "\u2019", "&amp;": "&", "&lt;": "<", "&gt;": ">",
}


def _ents(s):
    for k, v in _ENT.items():
        s = s.replace(k, v)
    return s


_TOKEN = re.compile(
    r'(<a\s+href="[^"]+">.*?</a>|</?strong>|</?b>|</?em>|'
    r'<span class="accent">|<span class="num">|</span>)',
    re.S,
)


def inline(par, html, size=9.5, color=R.DARK):
    """Emit runs for the limited inline vocabulary used in content.py."""
    bold = italic = 0
    accent = 0
    for chunk in _TOKEN.split(_ents(html)):
        if not chunk:
            continue
        if chunk.startswith('<a href="'):
            url = re.match(r'<a\s+href="([^"]+)"', chunk).group(1)
            text = re.sub(r"<[^>]+>", "", chunk)
            _hyperlink(par, url, text, size, bold=bool(bold), italic=bool(italic))
            continue
        if chunk in ("<strong>", "<b>"):
            bold += 1
            continue
        if chunk in ("</strong>", "</b>"):
            bold = max(0, bold - 1)
            continue
        if chunk == "<em>":
            italic += 1
            continue
        if chunk == "</em>":
            italic = max(0, italic - 1)
            continue
        if chunk in ('<span class="accent">', '<span class="num">'):
            accent += 1
            continue
        if chunk == "</span>":
            accent = max(0, accent - 1)
            continue
        text = re.sub(r"<[^>]+>", "", chunk)
        if not text:
            continue
        r = par.add_run(text)
        r.font.name = R.BODY
        r.font.size = Pt(size)
        r.bold = bool(bold) or bool(accent)
        r.italic = bool(italic)
        r.font.color.rgb = __import__("docx").shared.RGBColor.from_string(
            (R.RED if accent else color).upper()
        )
        rpr = r._element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts")
            rpr.append(rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), R.BODY)


# ------------------------------------------------------------------- flow types
class RICH(R.Flow):
    """A paragraph of content.py HTML rendered in an SCS body style."""

    def __init__(self, html, style="body"):
        self.html, self.style = html, style


class PULL(R.Flow):
    def __init__(self, html):
        self.html = html


class BULLET(R.Flow):
    def __init__(self, html):
        self.html = html


def emit(container, flow, doc):
    if isinstance(flow, RICH):
        p = container.add_paragraph()
        if flow.style == "lead":
            R._spacing(p, 0, 8)
            p.paragraph_format.line_spacing = 1.18
            inline(p, flow.html, size=10.5)
        elif flow.style == "note":
            R._spacing(p, 0, 6)
            inline(p, flow.html, size=8.4, color=R.MUTE)
        else:
            R._spacing(p, 0, 7)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.15
            inline(p, flow.html)
        return
    if isinstance(flow, PULL):
        p = container.add_paragraph()
        R._spacing(p, 8, 10)
        pPr = p._p.get_or_add_pPr()
        R._shade(pPr, R.CREAM)
        R._borders(pPr, {"left": (24, R.RED)})
        p.paragraph_format.left_indent = Pt(16)
        p.paragraph_format.right_indent = Pt(10)
        inline(p, flow.html, size=11, color=R.NAVY)
        for r in p.runs:
            r.bold = True
        return
    if isinstance(flow, BULLET):
        p = container.add_paragraph()
        R._spacing(p, 0, 5)
        p.paragraph_format.left_indent = Pt(18)
        p.paragraph_format.first_line_indent = Pt(-11)
        p.paragraph_format.line_spacing = 1.12
        r = p.add_run("\u2014\u2002")
        r.font.name = R.BODY
        r.font.size = Pt(9.5)
        inline(p, flow.html)
        return
    _BASE_EMIT(container, flow, doc)


# ------------------------------------------------------------------- HTML parse
class _Body(HTMLParser):
    """Walk content.BODY into an ordered flow list."""

    BLOCK = {"h2", "h3", "p", "li", "td", "th"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.flows = []
        self.buf = []
        self.tag = None
        self.cls = ""
        self.card = None
        self.table = None
        self.row = None
        self.rowspans = {}

    # -- helpers
    def _text(self):
        return re.sub(r"\s+", " ", "".join(self.buf)).strip()

    def _out(self, flow):
        (self.card if self.card is not None else self.flows).append(flow)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div" and "card" in a.get("class", ""):
            self.card = []
            return
        if tag == "table":
            self.table = []
            return
        if tag == "tr":
            self.row = []
            return
        if tag in self.BLOCK:
            self.tag, self.cls, self.buf = tag, a.get("class", ""), []
            if tag in ("td", "th"):
                self.span = int(a.get("rowspan", 1))
            return
        if self.tag:
            self.buf.append(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if self.tag:
            self.buf.append(self.get_starttag_text())

    def handle_data(self, data):
        if self.tag:
            self.buf.append(data)

    def handle_entityref(self, name):
        if self.tag:
            self.buf.append("&%s;" % name)

    def handle_charref(self, name):
        if self.tag:
            self.buf.append("&#%s;" % name)

    def handle_endtag(self, tag):
        if tag == "div" and self.card is not None:
            self.flows.append(R.PANEL(self.card))
            self.card = None
            return
        if tag == "table":
            self.flows.append(("TABLE", self.table))
            self.table = None
            return
        if tag == "tr":
            self.table.append(self.row)
            self.row = None
            return
        if tag in ("td", "th"):
            self.row.append((self._text(), getattr(self, "span", 1)))
            self.tag = None
            return
        if tag != self.tag:
            if self.tag:
                self.buf.append("</%s>" % tag)
            return
        txt = self._text()
        if txt:
            if tag == "h2":
                self._out(R.H1(re.sub(r"<[^>]+>", "", _ents(txt))))
            elif tag == "h3":
                self._out(R.H2(re.sub(r"<[^>]+>", "", _ents(txt))))
            elif tag == "li":
                self._out(BULLET(txt))
            elif "pull" in self.cls:
                self._out(PULL(txt))
            elif "lead" in self.cls:
                self._out(RICH(txt, "lead"))
            elif "deck" in self.cls:
                self._out(RICH(txt, "note"))
            else:
                self._out(RICH(txt))
        self.tag = None


def expand(rows):
    """Flatten (text, rowspan) cells, repeating spanned values down the column."""
    out = []
    carry = {}
    for r in rows:
        line, i = [], 0
        for col in range(len(rows[0]) if rows else 0):
            if col in carry and carry[col][1] > 0:
                line.append(carry[col][0])
                carry[col] = (carry[col][0], carry[col][1] - 1)
                continue
            if i < len(r):
                txt, span = r[i]
                i += 1
                if span > 1:
                    carry[col] = (txt, span - 1)
                line.append(txt)
        while i < len(r):
            line.append(r[i][0])
            i += 1
        out.append(line)
    return out


def parse(body_html, widths):
    p = _Body()
    p.feed(body_html)
    flows = []
    for f in p.flows:
        if isinstance(f, tuple) and f[0] == "TABLE":
            rows = expand(f[1])
            rows = [[re.sub(r"<[^>]+>", "", _ents(c)) for c in r] for r in rows]
            flows.append(R.TBL(rows, widths[: len(rows[0])]))
        else:
            flows.append(f)
    return flows
