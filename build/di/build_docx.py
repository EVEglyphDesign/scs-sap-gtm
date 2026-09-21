#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build EgD-EVE-DI-001 as a Steel Cloud Solutions house-style Word document.

Copy comes from `content.py` unchanged — the same source that builds the canon
PDF and the public HTML page. The visual system is the committed SCS renderer
(`docxout/render.py`, taken verbatim from scs-billing). This build adds the EgD
tag and hash register so the document is referenceable across the repositories.
"""
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "docxout"))

import content as C          # noqa: E402
import render as R           # noqa: E402
import flows as F            # noqa: E402

REPO = HERE.parent.parent
OUT = REPO / "docs" / "di"
DOCX_NAME = "SteelCloudSolutions_EVE_Decision_Intelligence_Layer.docx"
PDF_NAME = "EVEglyphDesign_EVE_Decision_Intelligence_Layer.pdf"
inch = R.inch


def sha(path):
    p = pathlib.Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def short(h):
    return (h[:32] + "\u2026") if h else "not built"


# ------------------------------------------------------------ hash + tag register
ARTIFACTS = [
    ("EgD-EVE-DI-001", "This briefing note \u2014 copy source",
     HERE / "content.py",
     "build/di/content.py"),
    ("EgD-EVE-DI-001", "This briefing note \u2014 controlled PDF",
     OUT / PDF_NAME,
     "docs/di/" + PDF_NAME),
    ("EgD-EVE-DI-001", "This briefing note \u2014 public HTML surface",
     OUT / "index.html",
     "docs/di/index.html"),
    ("EgD-EVE-DMZ-001", "DMZ-bound positioning \u2014 copy source",
     REPO / "build" / "dmz" / "content.py",
     "build/dmz/content.py"),
    ("EgD-EVE-DMZ-001", "DMZ-bound positioning \u2014 controlled PDF",
     REPO / "docs" / "dmz" / "EVEglyphDesign_EVE_DMZ_Bound_Positioning.pdf",
     "docs/dmz/EVEglyphDesign_EVE_DMZ_Bound_Positioning.pdf"),
    ("SCS house style", "Word renderer, reused verbatim from scs-billing",
     HERE / "docxout" / "render.py",
     "build/di/docxout/render.py"),
]

TAGS = [
    ("EgD-EVE-DI-001", "This note \u2014 EVE as an additive decision-intelligence layer",
     "scs-sap-gtm"),
    ("EgD-EVE-DMZ-001", "EVE is DMZ-bound by definition \u2014 the additive boundary",
     "scs-sap-gtm"),
    ("EgD-BOOT-001", "Executive Boot Contract \u2014 retrieval ladder, spend classes, output canon",
     "eve-glyph-boot-contract"),
    ("EgD-BOOT-002", "Burn Ledger measurement gate \u2014 credits per artifact, daily control",
     "eve-glyph-boot-contract"),
    ("EgD-BOOT-003", "Durability and non-destruction \u2014 the repository is the record",
     "eve-glyph-boot-contract"),
    ("EgD-BOOT-004", "Everything lands in the repository \u2014 no session-only state",
     "eve-glyph-boot-contract"),
    ("EgD-BOOT-005", "Versioned and reversible \u2014 every change states its inverse",
     "eve-glyph-boot-contract"),
    ("EgD-BOOT-006", "The rule of three \u2014 architecture explicable in words",
     "eve-glyph-boot-contract"),
    ("EgD-BOOT-007", "The burn switch \u2014 ECONOMY and BURN model-routing lanes",
     "eve-glyph-boot-contract"),
    ("EgD-GEO-003", "Sovereign-starter geometry \u2014 reference drawing wins over prose",
     "eve-glyph-boot-contract"),
    ("EgD-KEY-2026-07", "Controlled-copy key ID stamped on every canon artifact",
     "eve-glyph-boot-contract"),
    ("EgD-SCT-001", "Sovereign Capital Twin \u2014 custody at L0, CONTRACTUS register at L1",
     "eve-datasphere-sovereign"),
    ("EgD-SCT-INS-001", "Latencia \u2014 2,000 synthetic commitments, published refusals",
     "eve-datasphere-sovereign"),
    ("EgD-HAN-PNL-001", "Hana Europe / EAT HAPPY consolidation brief \u2014 DMZ test case",
     "eat-happy-hana"),
]

DEFECTS = [
    ("L", "Link or format \u2014 a bare, non-clickable URL"),
    ("R", "Retrieval waste \u2014 a held fact re-derived from scratch"),
    ("S", "Unconfirmed spend \u2014 an expensive action taken without approval"),
    ("I", "Interrupt \u2014 permission requested for a free action"),
    ("C", "Canon breach \u2014 palette, typography, naming or format"),
    ("D", "Durability \u2014 state that exists only inside a session"),
    ("V", "Unversioned or irreversible \u2014 a change with no stated inverse"),
    ("T", "Drift or shape breach \u2014 a return that varied its written shape"),
]


def register_flows(doc_sha, stamp):
    rows = [["Tag", "Artifact", "Repository path", "SHA-256 (first 32)"]]
    for tag, label, path, rel in ARTIFACTS:
        rows.append([tag, label, rel, short(sha(path))])
    tagrows = [["Tag", "What it governs", "Home repository"]] + [list(t) for t in TAGS]
    defrows = [["Class", "Defect"]] + [list(d) for d in DEFECTS]
    return [
        R.PageBreak(),
        R.H1("Reference register \u2014 EgD tags and content hashes"),
        F.RICH("Every artifact below is addressable by tag across the EVEglyphDesign "
               "repositories. Hashes are SHA-256 over the committed file at build time, so a "
               "reviewer can confirm that the copy in front of them is the copy that was "
               "published.", "body"),
        R.TBL(rows, [1.15 * inch, 2.0 * inch, 1.85 * inch, 1.7 * inch]),
        R.H2("Tag index"),
        R.TBL(tagrows, [1.15 * inch, 3.75 * inch, 1.8 * inch]),
        R.H2("Defect classes \u2014 EgD-BOOT-001 \u00a75"),
        R.TBL(defrows, [0.6 * inch, 6.1 * inch]),
        R.H2("This document"),
        F.RICH(f"Document tag <b>{C.DOC_ID}</b> \u00b7 key ID <b>{R.KEY_ID}</b> \u00b7 "
               f"copy-source SHA-256 <b>{doc_sha}</b> \u00b7 built {stamp}. "
               "Governed by "
               '<a href="https://eveglyphdesign.github.io/eve-glyph-boot-contract/">'
               "EgD-BOOT-001</a>. Source and build: "
               '<a href="https://github.com/EVEglyphDesign/scs-sap-gtm/tree/main/build/di">'
               "scs-sap-gtm/build/di</a>.", "note"),
    ]


# ----------------------------------------------------------------------- document
def flows_fn(doc_sha, stamp):
    meta = [
        ["Document", f"{C.DOC_ID} \u00b7 controlled draft"],
        ["Prepared for", "Jeff Eden \u2014 Steel Cloud Solutions"],
        ["Prepared by", "Dany Theriault \u00b7 EVEglyphDesign"],
        ["Subject", "Conformance of EVE to the eight-capability decision-intelligence test"],
        ["Key ID", R.KEY_ID],
        ["SHA-256 (copy source)", doc_sha],
        ["Built", stamp],
    ]
    out = R.cover(C.DOC_ID, "EVE as an additive decision-intelligence layer",
                  C.SUBTITLE, meta, C.DECK)
    out += [R.Spacer(1, 6)]
    out += F.parse(C.BODY, [1.35 * inch, 1.85 * inch, 3.5 * inch])
    out += [R.H1("Sources and provenance")]
    for name, url in C.SOURCES:
        out.append(F.BULLET(f'<a href="{url}">{name}</a>'))
    out += [F.RICH(C.EVIDENCE_NOTE, "note")]
    out += register_flows(doc_sha, stamp)
    return out


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    src = (HERE / "content.py").read_text(encoding="utf-8")
    path = OUT / DOCX_NAME
    # render.build uses flows_fn(sha, ts) and emits via render._emit; swap in the
    # rich dispatcher so RICH/PULL/BULLET flows resolve.
    R._emit = F.emit
    s, ts, _ = R.build(str(path), C.DOC_ID, C.TITLE, flows_fn, src)
    print(f"DOCX: {path} sha256(src)={s[:16]}\u2026 stamp={ts}")
    return path


if __name__ == "__main__":
    build()
