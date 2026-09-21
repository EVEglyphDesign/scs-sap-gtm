# Version arc — scs-sap-gtm

Monotonic. It only grows. Every row states its inverse (EgD-BOOT-005).

| Version | ID | Change | Inverse |
|---|---|---|---|
| 1.0 | L0 | Public engagement-model surface for Jeff Eden and Jason Porterfield (`docs/index.html`) | `git revert` the initial surface commit |
| 1.1 | L1.1 | `EgD-EVE-DMZ-001` — DMZ-bound positioning note: `build/dmz/`, `docs/dmz/`, controlled PDF | `git rm -r build/dmz docs/dmz` and drop the README companion section |
| 1.2 | L1.2 | `EgD-EVE-DI-001` — decision-intelligence briefing note: `build/di/`, `docs/di/`, controlled PDF, SCS-house-style DOCX, EgD tag and hash register | `git rm -r build/di docs/di registry/VERSIONS.md` and drop the README section |
| 1.2.1 | L1.2.1 | `EgD-EVE-DI-001` rev 2 — "three lifecycle movements" corrected to "four lifecycle capabilities Gartner names"; all three surfaces and the hash register rebuilt | `git revert 318f05f` |

## Build order for `EgD-EVE-DI-001`

`content.py` is the single copy source for all three surfaces. Build in this order so the
hash register matches what is published:

```
cd build/di && python build.py && python build_docx.py
```

`build.py` writes the controlled PDF and `docs/di/index.html`; `build_docx.py` hashes those
committed files into the Word document's reference register.

© 2026 EVEglyphDesign. *Pour le bien-être du peuple.*
