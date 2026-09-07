
DOC_ID = "EgD-EVE-DMZ-001"
TITLE = "EVE is DMZ-bound by definition"
SUBTITLE = "Why the additive posture is a structural fact, not a promise"
DECK = ("Positioning note for the Steel Cloud Solutions \u2013 SAP North America lane. "
        "Tested against the Hana Europe / EAT HAPPY consolidation brief EgD-HAN-PNL-001.")

BODY = r"""
<h2>The proposition, stated precisely</h2>

<p class="lead">EVE is a <span class="accent">DMZ-bound</span> solution. It operates in the
zone between the client's managed systems of record and the outside parties who are asked
to do work against them. It holds authorized copies, decisions and evidence &mdash; never
the record itself. Everything that follows from that boundary is additive by construction:
it exists to satisfy compliance and to accelerate work that already sits outside the
data-management organization's span of control.</p>

<p class="pull">Nothing EVE does can subtract, because EVE never holds the original.</p>

<h2>Why &ldquo;DMZ-bound&rdquo; is a definition, not a claim</h2>

<p>A DMZ is a perimeter network placed between an organization's internal network and an
external network, exposing only what is intended to be reachable and holding the internal
estate behind a second boundary
(<a href="https://csrc.nist.gov/glossary/term/demilitarized_zone">NIST CSRC glossary</a>;
<a href="https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-41r1.pdf">NIST SP 800-41 Rev. 1</a>).
Applied to a consulting and decision-intelligence engagement, three structural facts make
the term literal rather than metaphorical.</p>

<div class="card">
  <h3>The three structural facts</h3>
  <p><span class="num">01</span> <strong>EVE never receives write authority to a system of
  record.</strong> The canon states that systems of record remain authoritative, that
  AI-assisted changes enter as proposals, and that a named person approves a specific
  version
  (<a href="https://github.com/EVEglyphDesign/enterprise-program-alignment/blob/main/DECISIONS.md">enterprise-program-alignment/DECISIONS.md</a>).
  A component with no write path to the ledger cannot be a ledger.</p>

  <p><span class="num">02</span> <strong>What crosses in is an authorized extract, not the
  estate.</strong> The Datasphere model is explicitly a customer-owned, read-only
  analytical copy with a semantic spine
  (<a href="https://github.com/EVEglyphDesign/eve-datasphere-sovereign/blob/main/README.md">eve-datasphere-sovereign/README.md</a>).
  The client's data organization decides what crosses and keeps the source.</p>

  <p style="margin-bottom:0"><span class="num">03</span> <strong>The repository, not the
  session, is the record of what happened in the zone.</strong> Decisions, evidence,
  versions and approvals land as committed files the client owns
  (<a href="https://github.com/EVEglyphDesign/sovereign-starter/blob/main/SOVEREIGN-STARTER.md">sovereign-starter/SOVEREIGN-STARTER.md</a>).
  A DMZ with no log is an exposure; a DMZ whose entire content is an append-only log is a
  control.</p>
</div>

<h2>What lives in the zone, and what never does</h2>

<table>
  <thead>
    <tr><th>Inside the DMZ (EVE)</th><th>Behind the boundary (client-managed, untouched)</th></tr>
  </thead>
  <tbody>
    <tr><td>Authorized extracts and signed trial balances</td><td>ERP ledgers, postings, the general ledger of record</td></tr>
    <tr><td>Mapping rules, crosswalks, semantic models</td><td>Operational chart of accounts and master data</td></tr>
    <tr><td>Decision records, rationale, named approvals</td><td>Statutory books, filings, the audited financial statements</td></tr>
    <tr><td>Evidence links, validation results, defect register</td><td>Local tax and VAT compliance systems</td></tr>
    <tr><td>Proposed changes awaiting human authorization</td><td>Production configuration, transports, roles and access grants</td></tr>
    <tr><td>Consultant working artifacts, versioned</td><td>Identity, network, backup, retention and DR operations</td></tr>
  </tbody>
</table>

<h2>Consequence one &mdash; additive by construction</h2>

<p>Most vendors assert that they are additive. The assertion is only worth what the
architecture makes unavoidable. Because EVE holds no original and has no write path, the
worst-case failure of an EVE engagement is a discarded copy and a set of documents the
client already owns. There is no rollback of a migration, no reprocessing of a ledger, no
orphaned integration inside the estate. That is what makes it signable by a client data
organization that has been burned before.</p>

<ul>
  <li><strong>No displacement.</strong> The incumbent SI, the platform vendor, and the
  internal data team each keep their scope entirely. EVE consumes their outputs; it does
  not arbitrate them.</li>
  <li><strong>No exit cost.</strong> The client keeps the repository whether the
  engagement continues, pauses, or ends. Removal of EVE removes nothing the client needs.</li>
  <li><strong>No procurement fight.</strong> A read-only zone under the client's own
  identity and hosting is a control decision, not a platform decision, and it does not
  compete for the platform budget.</li>
</ul>

<h2>Consequence two &mdash; compliance is the payload, not a feature</h2>

<p>The reason to stand up the zone at all is that the work happening outside the managed
estate is exactly the work that is hardest to evidence. Auditors examining end-user
computing look at provenance, logic, access, change control, versioning and
reproducibility
(<a href="https://www.icaew.com/technical/audit-and-assurance/faculty-resources/audit-and-beyond/2024/articles/the-auditors-review-of-management-spreadsheets">ICAEW, &ldquo;The auditor&rsquo;s review of management spreadsheets&rdquo;</a>).
Those six things are the DMZ's entire content. A signed mapping, an automated validation,
a locked package and a named approver are minimum controls for a workbook-era bridge, and
they are what EVE supplies without anyone touching the source ledgers.</p>

<p>The same logic covers the delivery bench. The traditional offshore risk is context
drift &mdash; the delivery team quietly substituting its own reasoning for the client's.
Inside the zone, every artifact is versioned as it is produced and reviewable in the same
working session, so review stops being a weekly cadence and becomes a property of the
surface.</p>

<h2>Consequence three &mdash; it accelerates only what is already outside</h2>

<p>The acceleration claim is bounded by the same boundary, and that is why it survives
scrutiny. EVE speeds up assessment, mapping design, policy documentation, decision capture,
close-package preparation and artifact production &mdash; work that today happens in
inboxes, decks and unversioned workbooks, outside the data organization's control
framework and outside its tooling. It does not speed up anything the data organization
already runs well, and it does not ask for a change window to do its job.</p>

<div class="card">
  <h3>The line the client's data lead actually hears</h3>
  <p style="margin-bottom:0">&ldquo;We are not asking for access to your systems, a change
  to your landscape, or a seat in your change-advisory board. We are asking you to
  authorize an extract into a zone you own, and in exchange the work your business is
  already doing outside your control framework becomes evidenced, versioned and reversible
  &mdash; and finishes faster.&rdquo;</p>
</div>

<h2>What this settles in the Hana brief</h2>

<p>The consolidation brief EgD-HAN-PNL-001 delivered an honest verdict: EVE is the lightest
governance wrapper but not the lightest complete consolidation solution, and it must not be
represented as a consolidation engine. Under the DMZ framing that verdict stops being a
limitation and becomes the specification.</p>

<ul>
  <li><strong>&ldquo;Scope mismatch&rdquo; resolves.</strong> Consolidation requires
  accounting rules, ownership logic, journals and eliminations. Those are engine functions
  behind the boundary. Custody, provenance and decision continuity are zone functions. The
  brief's recommended Option 2 &mdash; a thin, controlled trial-balance mapping and evidence
  layer &mdash; is a DMZ pattern described in accounting language.</li>
  <li><strong>&ldquo;Implementation weight hides in sovereign&rdquo; resolves.</strong>
  Weight enters when a project reaches behind the boundary to replicate transactional
  detail. The DMZ rule is the test that keeps the first close light: if it requires a write
  path or a landscape change, it is out of scope for the bridge.</li>
  <li><strong>&ldquo;No automatic statutory acceptability&rdquo; stands and must
  stand.</strong> A zone that evidences preparation does not certify the result. The
  reporting parent still owes IFRS 10 consolidation and IFRS 3 acquisition accounting, and
  the auditor still decides what to rely on.</li>
</ul>

<h2>Where the framing must not be over-claimed</h2>

<p>The positioning is strong precisely because it is narrow. Four honest limits keep it
defensible in front of a CISO, a data protection officer, or an audit partner.</p>

<ul>
  <li><strong>A DMZ is a boundary, not an assurance certificate.</strong> The zone still
  needs its own access model, segregation of duties, retention rules and logging. Being
  outside the estate is not the same as being controlled.</li>
  <li><strong>Copies carry obligations.</strong> Personal data crossing into the zone is
  still processing under GDPR, and transfers outside the EEA still require an adequacy
  basis or safeguards
  (<a href="https://www.edpb.europa.eu/sme/be-compliant/international-data-transfers_en">EDPB international transfers</a>).
  Classification, minimization of identifiers and a documented transfer assessment are part
  of standing the zone up, not an afterthought.</li>
  <li><strong>Read-only is an architecture, not a slogan.</strong> It has to be provable in
  the connection design and the access grants, or the claim collapses on first review.</li>
  <li><strong>Additive is not free of supportability risk.</strong> The client must own the
  runbooks, tests, access and deployment for the zone, or a custom layer becomes a new
  key-person dependency.</li>
</ul>

<h2>What it does for the GTM lane</h2>

<p>For the Steel Cloud Solutions position with SAP North America presales, the DMZ frame is
the mechanism underneath the arm's-length posture already published on the
<a href="https://eveglyphdesign.github.io/scs-sap-gtm/">SCS SAP GTM surface</a>. It converts
three of that page's assertions into structural facts.</p>

<ul>
  <li><strong>&ldquo;Not a reseller, not an SI, not a displacement&rdquo;</strong> becomes
  architecturally true rather than contractually promised: a party with no write authority
  cannot take over anyone's scope.</li>
  <li><strong>&ldquo;Own the ground floor, rent whatever you want above it&rdquo;</strong>
  gains its floor plan. The custody layer is the DMZ; the vendor stack stays where it is;
  the estate stays where it is.</li>
  <li><strong>Protection of the account team's standing</strong> becomes demonstrable. The
  semantic model stays on ground the customer owns and SAP can reach, and no one has to
  explain to a security review why a third party holds write access to the ledger.</li>
</ul>

<p class="pull">The additive posture is not restraint. It is the shape of the thing.</p>
"""

SOURCES = [
    ("NIST CSRC \u2014 demilitarized zone (DMZ)", "https://csrc.nist.gov/glossary/term/demilitarized_zone"),
    ("NIST SP 800-41 Rev. 1 \u2014 Guidelines on Firewalls and Firewall Policy", "https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-41r1.pdf"),
    ("ICAEW \u2014 The auditor\u2019s review of management spreadsheets", "https://www.icaew.com/technical/audit-and-assurance/faculty-resources/audit-and-beyond/2024/articles/the-auditors-review-of-management-spreadsheets"),
    ("EDPB \u2014 international data transfers", "https://www.edpb.europa.eu/sme/be-compliant/international-data-transfers_en"),
    ("IFRS 10 \u2014 Consolidated Financial Statements", "https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2026/issued/ifrs10.html"),
    ("IFRS 3 \u2014 Business Combinations", "https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2026/issued/ifrs3.html"),
    ("Enterprise Program Alignment \u2014 decision canon", "https://github.com/EVEglyphDesign/enterprise-program-alignment/blob/main/DECISIONS.md"),
    ("EVE Datasphere Sovereign \u2014 README", "https://github.com/EVEglyphDesign/eve-datasphere-sovereign/blob/main/README.md"),
    ("Sovereign Starter \u2014 boot, canon, defect loop", "https://github.com/EVEglyphDesign/sovereign-starter/blob/main/SOVEREIGN-STARTER.md"),
    ("Steel Cloud Solutions \u2014 SAP North America additive layer", "https://eveglyphdesign.github.io/scs-sap-gtm/"),
    ("EVEglyphDesign Executive Boot Contract", "https://eveglyphdesign.github.io/eve-glyph-boot-contract/"),
]

EVIDENCE_NOTE = (
    "Evidence classification. External definitions and requirements are linked inline. "
    "EVE statements are grounded in the committed repository files linked above. The DMZ "
    "characterization, its consequences, and the reconciliation with EgD-HAN-PNL-001 are "
    "advisory judgments of positioning, not verified facts about any client estate."
)
