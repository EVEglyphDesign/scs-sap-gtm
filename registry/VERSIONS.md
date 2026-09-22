# Version arc — scs-sap-gtm

Monotonic. It only grows. Every row states its inverse (EgD-BOOT-005).

| Version | ID | Change | Inverse |
|---|---|---|---|
| 1.0 | L0 | Public engagement-model surface for Jeff Eden and Jason Porterfield (`docs/index.html`) | `git revert` the initial surface commit |
| 1.1 | L1.1 | `EgD-EVE-DMZ-001` — DMZ-bound positioning note: `build/dmz/`, `docs/dmz/`, controlled PDF | `git rm -r build/dmz docs/dmz` and drop the README companion section |
| 1.2 | L1.2 | `EgD-EVE-DI-001` — decision-intelligence briefing note: `build/di/`, `docs/di/`, controlled PDF, SCS-house-style DOCX, EgD tag and hash register | `git rm -r build/di docs/di registry/VERSIONS.md` and drop the README section |
| 1.2.1 | L1.2.1 | `EgD-EVE-DI-001` rev 2 — "three lifecycle movements" corrected to "four lifecycle capabilities Gartner names"; all three surfaces and the hash register rebuilt | `git revert 318f05f` |
| 1.3 | L2.0 | `docs/index.html` rewritten to lead with the arm's-length advisory model and the two service shapes; presales-conversion framing dropped. Old copy captured in git history for restore | `git checkout <previous commit>:docs/index.html -- docs/index.html` |
| 1.3.1 | L2.1 | `docs/jason/index.html` added — Datasphere adoption lane briefing for Jason: micro / mid-cap / strategic sizing, the two services, senior-advisor bench with Lillian-type profile reference | `git rm docs/jason/index.html` |
| 1.3.2 | L2.2 | `docs/jason/BRIEFING.md` added — plain Markdown briefing suitable for sending or pasting; carries the same substance as the web page | `git rm docs/jason/BRIEFING.md` |
| 1.4 | L3.0 | Three service model corrected: Service A = Datasphere technical support and product demonstration (non-productive-system enablement, test-pointed-at-production preview); Service B = Business-case build for the SAP decision (decision support, working backwards from the decision, explicitly no audit / no entitlement pull); Service C = Executive decision-intelligence assessment. Prior two-service copy that read as audit-shaped removed from `docs/index.html`, `docs/jason/index.html`, `docs/jason/BRIEFING.md`, `README.md` | `git checkout <previous commit>:docs/index.html docs/jason/index.html docs/jason/BRIEFING.md README.md -- .` |
| 1.4.1 | L3.1 | Service C advisor sourcing rewritten: "executive-search capability and industry network" replaced everywhere with a peer network of senior SAP subject-matter experts who have worked together for decades and trust each other, from whom SCS finds the person most appropriate to lead the assessment. Operator ruled the recruiting-agency framing out on record. Updated in `docs/index.html`, `docs/jason/index.html`, `docs/jason/BRIEFING.md`, `README.md` | `git checkout <previous commit>:docs/index.html docs/jason/index.html docs/jason/BRIEFING.md README.md -- .` |

## Build order for `EgD-EVE-DI-001`

`content.py` is the single copy source for all three surfaces. Build in this order so the
hash register matches what is published:

```
cd build/di && python build.py && python build_docx.py
```

`build.py` writes the controlled PDF and `docs/di/index.html`; `build_docx.py` hashes those
committed files into the Word document's reference register.

© 2026 EVEglyphDesign. *Pour le bien-être du peuple.*
