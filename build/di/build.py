#!/usr/bin/env python3
"""Build the EgD-EVE-DI-001 briefing note: canon PDF + public HTML surface."""
import hashlib, datetime, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import content as C
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

HERE = pathlib.Path(__file__).parent
FONTS = HERE.parent / "fonts"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

SRC_HASH = hashlib.sha256((HERE / "content.py").read_bytes()).hexdigest()
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

PALETTE = """
:root{--cream:#fdfaf4;--cream-2:#f7f2e7;--ink:#1a1a1a;--line:#e7e1d3;--mute:#6b665c;--orange:#e87722;}
"""

FONT_FACES = f"""
@font-face{{font-family:'Fraunces';src:url('{FONTS}/Fraunces.ttf');font-weight:400 700;font-style:normal;}}
@font-face{{font-family:'Fraunces';src:url('{FONTS}/Fraunces-Italic.ttf');font-weight:400 700;font-style:italic;}}
@font-face{{font-family:'InterV';src:url('{FONTS}/Inter.ttf');font-weight:400 700;font-style:normal;}}
@font-face{{font-family:'InterV';src:url('{FONTS}/Inter-Italic.ttf');font-weight:400 700;font-style:italic;}}
"""

SHARED = """
body{font-family:'InterV',sans-serif;color:var(--ink);background:var(--cream);
  font-size:10.2pt;line-height:1.5;}
h1{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:24pt;line-height:1.12;
  color:var(--orange);margin:0 0 6pt;letter-spacing:-.01em;}
h2{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:15pt;margin:20pt 0 6pt;
  page-break-after:avoid;}
h3{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:11.5pt;margin:0 0 5pt;
  page-break-after:avoid;}
p{margin:0 0 8pt;}
a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--orange);}
.lead{font-size:11.2pt;line-height:1.5;}
.accent{color:var(--orange);font-weight:600;}
.pull{font-family:'Fraunces',Georgia,serif;font-weight:500;font-size:13pt;line-height:1.3;
  border-left:3px solid var(--orange);padding:4pt 0 4pt 12pt;margin:14pt 0;
  page-break-inside:avoid;}
.card{background:var(--cream-2);border:1px solid var(--line);border-radius:10pt;
  padding:12pt 14pt;margin:12pt 0;page-break-inside:avoid;}
.card p:last-child{margin-bottom:0;}
.num{font-family:'Fraunces',Georgia,serif;font-weight:600;color:var(--orange);
  font-size:10pt;display:inline-block;min-width:22pt;}
ul{margin:4pt 0 10pt;padding-left:14pt;}
li{margin:4pt 0;}
table{width:100%;border-collapse:collapse;margin:10pt 0 14pt;font-size:9.4pt;
  page-break-inside:avoid;}
th{background:var(--cream-2);text-align:left;font-weight:600;font-size:9.2pt;
  border-bottom:1px solid var(--line);padding:6pt 8pt;}
td{border-bottom:1px solid var(--line);padding:6pt 8pt;vertical-align:top;}
.kicker{font-size:8.4pt;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);
  margin:0 0 8pt;}
.sub{font-family:'Fraunces',Georgia,serif;font-style:italic;font-weight:400;
  color:var(--mute);font-size:12pt;margin:0 0 8pt;}
.deck{color:var(--mute);font-size:9.6pt;margin:0 0 4pt;}
.srcs{font-size:8.3pt;line-height:1.42;}
.srcs li{margin:1.5pt 0;}
.evidence{font-size:8.3pt;line-height:1.42;color:var(--mute);
  border-top:1px solid var(--line);padding-top:7pt;margin-top:10pt;}
.closing{font-size:8.3pt;line-height:1.42;color:var(--mute);margin-top:7pt;}
.closing em{font-family:'Fraunces',Georgia,serif;font-style:italic;}
"""


def page_css(total):
    extent = f"Verified extent: {total} pages" if total else "Verified extent: pending"
    return f"""
@page {{
  size: A4; margin: 20mm 18mm 22mm 18mm; background: var(--cream);
  @top-right {{ content: "EVEglyphDesign  |  {C.DOC_ID}"; font-family:'InterV',sans-serif;
    font-size:7.6pt; color:var(--mute); }}
  @bottom-center {{ content: "\\00a9 2026 EVEglyphDesign \\00b7 SHA-256 {SRC_HASH} \\00b7 EgD-KEY-2026-07 \\00b7 {STAMP}\\A Page " counter(page) " of " counter(pages) " \\00b7 Pour le bien-\u00eatre du peuple \\00b7 {extent}";
    white-space: pre-wrap; font-family:'InterV',sans-serif; font-size:6.6pt;
    color:var(--mute); line-height:1.5; }}
}}
"""


def doc_html():
    srcs = "\n".join(
        f'<li><a href="{u}">{n}</a> &mdash; {u}</li>' for n, u in C.SOURCES
    )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{C.TITLE} \u00b7 {C.DOC_ID}</title></head><body>
<p class="kicker">EVEglyphDesign \u00b7 {C.DOC_ID} \u00b7 Briefing note</p>
<h1>{C.TITLE}</h1>
<p class="sub">{C.SUBTITLE}</p>
<p class="deck">{C.DECK}</p>
<p class="deck">{C.PREPARED}</p>
{C.BODY}
<h2>Sources and provenance</h2>
<ul class="srcs">{srcs}</ul>
<p class="evidence">{C.EVIDENCE_NOTE}</p>
<p class="closing">\u00a9 2026 EVEglyphDesign. All rights reserved. Controlled copy.<br>
<em>Pour le bien-\u00eatre du peuple.</em></p>
</body></html>"""


def build_pdf():
    fc = FontConfiguration()
    html = HTML(string=doc_html(), base_url=str(HERE))
    def render(total):
        css = CSS(string=PALETTE + FONT_FACES + SHARED + page_css(total), font_config=fc)
        return html.render(stylesheets=[css], font_config=fc)
    first = render(None)
    total = len(first.pages)
    second = render(total)
    if len(second.pages) != total:  # settle if stamping shifted flow
        total = len(second.pages)
        second = render(total)
    path = OUT / "EVEglyphDesign_EVE_Decision_Intelligence_Layer.pdf"
    second.write_pdf(str(path))
    print(f"PDF: {path} pages={total} sha256(src)={SRC_HASH[:16]}\u2026 stamp={STAMP}")
    return path, total




# ---------------------------------------------------------------- public surface

DOCS = HERE.parent.parent / "docs" / "di"
REF_PAGE = HERE.parent.parent / "docs" / "dmz" / "index.html"
PDF_NAME = "EVEglyphDesign_EVE_Decision_Intelligence_Layer.pdf"


def _ref_styles():
    """Reuse the committed DMZ page stylesheet verbatim — same reference set."""
    html = REF_PAGE.read_text(encoding="utf-8")
    start = html.index("<style>")
    end = html.index("</head>")
    return html[start:end].rstrip()


def build_page():
    DOCS.mkdir(parents=True, exist_ok=True)
    srcs = "\n".join(
        f'<li><a href="{u}">{n}</a></li>' for n, u in C.SOURCES
    )
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>{C.TITLE} \u00b7 {C.DOC_ID}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
{_ref_styles()}
</head>
<body>
<main>
  <header>
    <div class="kicker">EVEglyphDesign \u00b7 {C.DOC_ID} \u00b7 Briefing note</div>
    <h1>{C.TITLE}</h1>
    <p class="sub">{C.SUBTITLE}</p>
  </header>
  <p class="deck">{C.DECK}</p>
  <p class="deck">{C.PREPARED}</p>
  <p><a class="dl" href="./{PDF_NAME}">Read the controlled PDF</a></p>
{C.BODY}
  <h2>Sources and provenance</h2>
  <ul class="srcs">{srcs}</ul>
  <p class="deck">{C.EVIDENCE_NOTE}</p>

  <hr class="rule">

  <div class="stamp">
    {C.DOC_ID} \u00b7 {C.TITLE}<br>
    Companion notes: <a href="../">the engagement model</a> \u00b7
    <a href="../dmz/">EVE is DMZ-bound by definition</a><br>
    Prepared by <a href="https://github.com/EVEglyphDesign/scs-sap-gtm">EVEglyphDesign \u00b7 scs-sap-gtm</a> \u00b7
    <a href="https://eveglyphdesign.github.io/eve-glyph-boot-contract/">Operating canon</a><br>
    <em>Pour le bien-\u00eatre du peuple.</em>
  </div>
</main>
</body>
</html>
"""
    out = DOCS / "index.html"
    out.write_text(page, encoding="utf-8")
    print(f"PAGE: {out} bytes={len(page)}")
    return out


if __name__ == "__main__":
    pdf, total = build_pdf()
    import shutil
    page = build_page()
    shutil.copy2(pdf, DOCS / PDF_NAME)
    print(f"PUBLISHED: {DOCS / PDF_NAME} pages={total}")
