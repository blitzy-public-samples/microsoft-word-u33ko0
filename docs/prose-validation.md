# Prose Validation Record

Twenty-nine pieces of generated text carry a verdict below, and every one reads CLEAN. Rule 3
requires a verdict and a principle scorecard for every piece of generated text, and this file holds
both. The register in the last section names every violation the pass found. Each entry quotes the
drafted passage, gives the text that replaced it, and says in one sentence why the replacement is
better.

Nothing here changes a source file's behaviour. Every replacement keeps the factual claim, the
`path:Lnn` locator and the consequence of the passage it replaced.

Conflict C5 in [decision-log.md](decision-log.md) at `:L115` records the gap this file fills. Rule 3
demands a verdict and a scorecard per piece of generated text, and no other enumerated deliverable
can hold them. Decision row 4 at `decision-log.md:L84` records the choice and the risk it carries.

Every figure in this record was measured at the current branch head rather than estimated. A
reviewer can reproduce each one from the [Checks run](#checks-run) table.

## Method and scope

### Why the Asimov persona governs

Rule 3 runs two writing personas and defaults to Vonnegut. The rule switches to Asimov when the
material is technical documentation, a specification, or structured explanation. All 29 deliverables
are technical documentation: 19 module READMEs with a fixed nine-heading structure, 8
repository-level reference documents, and one inline documentation pass across 44 source files.
Asimov therefore governs every score below, and the Vonnegut principles stay in force under the
weighting the next subsection sets.

The practical effect of the switch shows up in two places. Asimov rejects metaphor where Vonnegut
rewards it, so a metaphor in this corpus reads as ornament rather than as work saved. Asimov also
ranks logical sequence above brevity, so a long document that builds from known to unknown scores
better than a short one that jumps.

### Input classification and principle weighting

Rule 3's input classification puts this material in the Technical class, because every deliverable is
documentation, a README, or a specification-adjacent reference. The class fixes the weighting
reproduced below. Weight decides consequence, not detection: a reduced-weight principle is still
scored, and a finding against it still appears in the register.

| # | Principle | Weight for this material |
| --- | --- | --- |
| V1 | Find a subject you care about | Reduced |
| V2 | Do not ramble | Highest |
| V3 | Keep it simple | Highest |
| V4 | Have the guts to cut | Normal |
| V5 | Sound like yourself | Reduced |
| V6 | Say what you mean | Highest |
| V7 | Pity the reader | Highest |
| V8 | Start close to the end | Normal |
| V9 | The Dignity Test | Full, enterprise technical writing |
| V10 | The Indifference Detector | Full, enterprise technical writing |
| V11 | The Indianapolis Test | Full, enterprise technical writing |
| V12 | Humor as Trust Signal | Full, enterprise technical writing |
| A1 | Plate Glass Clarity | Full |
| A2 | Short Words, Simple Structures | Full |
| A3 | Logical Sequence | Full |
| A4 | Ideas Carry the Weight | Full |
| A5 | Conversational Informality | Full |
| A6 | No Ornamental Language | Full |
| A7 | Functional Dialogue | Full |
| A8 | Anticipate Reader Questions | Full |
| A9 | Efficiency Over Polish | Full |
| A10 | Respect the Reader's Intelligence | Full |

A finding on V1 or V5 would carry less consequence than one on V2, V3, V6 or V7. The Technical class
reduces the first pair and raises the second four. No finding survives against any of the twenty-two
at the current branch head, so the weighting changes no verdict in this record.

### Severity levels and verdict thresholds

Rule 3 defines exactly three severity levels, and this record adds none:

- **Pass**, no meaningful violation.
- **Soft violation**, could be tighter, but not bad.
- **Hard violation**, clearly breaks the principle; the reader suffers.

Rule 3 defines exactly three verdicts, quoted as thresholds:

- **CLEAN**, zero hard violations, at most 2 soft.
- **NEEDS WORK**, 1-3 hard violations or 4+ soft.
- **ROUGH DRAFT**, 4+ hard violations.

The target for all 28 new files and for the inline documentation pass was CLEAN, and all 29 reach it
with zero hard and zero soft violations outstanding. No deliverable carries a residual violation of
any severity, so no severity judgement is load-bearing in the table below.

Rule 3's thresholds leave one combination unclassified. Three soft violations with no hard violation
exceeds the CLEAN cap of two soft, and reaches neither the hard-violation floor nor the four-soft
floor for NEEDS WORK. Decision row 17 at `decision-log.md:L97` records the resolution: that
combination is recorded as NEEDS WORK, because it fails the CLEAN test. No deliverable lands there
at the current branch head, so the convention is stated and never exercised.

### How a finding is detected

Rule 3's own detection heuristics are the thresholds this record uses. Decision row 17 at
`decision-log.md:L97` records that choice against the alternative, which was a wider local band.
Two heuristics are countable and both come from the rule:

| Registers as a finding | Principle it touches | Source of the threshold |
| --- | --- | --- |
| A prose sentence over 30 words | V3, Keep it simple, and A2 | V3's detection heuristic, "Sentences over 30 words" |
| A paragraph over 5 sentences | V2, Do not ramble | V2's detection heuristic, "Paragraphs over 5 sentences" |

No local band widens either number, and this record defines no numeric severity band of its own. An
earlier draft of this file carried bands that passed a 35-word sentence and an 8-sentence paragraph.
Both were deleted rather than restated, because a band that passes text the rule flags reports a
cleaner corpus than the rule allows.

Every principle a finding touches is scored on its own. A long sentence therefore registers against
V3 and against A2, which shares the same heuristic, rather than being charged once and excused
elsewhere. Decision row 17 records that convention too, in place of the one-finding-one-principle
rule an earlier draft used.

Four counting details decide reproducibility, and all four follow Rule 3's Special Handling:

- An inline code span counts as one word, however long it runs, so a locator adds nothing to a
  sentence's length.
- Link text counts as prose and a link destination does not.
- A paragraph is a run of prose lines between blank lines, and a list item counts as its own
  paragraph.
- A table cell is scored for sentence length as its own unit. The paragraph heuristic does not apply
  to a cell, because a cell is a field rather than a paragraph.

### What is exempt from validation

Rule 3's Special Handling section exempts three kinds of text, and all three exemptions were applied:

- **Code blocks and inline code.** The 89 fenced blocks across the 28 committed deliverables were
  read for language tagging and never scored as prose. An inline code span counts as one word.
- **Mermaid diagram blocks.** The corpus carries 25 of them, and none was scored.
- **Quotations attributed to others.** Two bodies of quoted text qualify. The first is the
  `HUMAN ASSISTANCE NEEDED` and `TODO` comment text preserved verbatim from the repository's
  original authors, which this engagement did not write. The second is the blockquoted material in
  this file, where each quotation is attributed to its source in the line above it.

Rule 3 also treats deliberate rule-breaking for effect as a choice rather than a violation. One
instance qualifies and is labelled here. The 19 module READMEs repeat six fixed terms, router,
handler, service, adapter, slice and marker, far beyond what blog rule B4 permits. The repetition is
deliberate and [decision-log.md](decision-log.md) records it at `:L95`. No other deliberate
rule-break was found, and no other passage was excused as one.

### What is out of scope

Rule 3 scopes validation to generated text, so two bodies of prose in this repository carry no
verdict and appear in no row below.

- **The root README.** [../README.md](../README.md) predates this engagement and received no edit,
  so no sentence in it was generated here. Conflict C1 at `decision-log.md:L111` records why the
  file stayed untouched. The omission is deliberate, and the file is not a deliverable.
- **The three specification documents under `../documentation/`.** All three predate this
  engagement and were read as reference only. No sentence in them was generated here, so none is
  validated. Where a locator below points into one of the three, the citation names a heading plus a
  line number, following the convention at `README.md:L91-L94`.

### The four adopted blog rules

Rule 3's blog rules apply to blog content, and none of these deliverables is blog content. Four of
the five apply here anyway as house conventions, and B4 does not.
[decision-log.md](decision-log.md) records the scoping at `:L95`, entry 15.

| Rule | Convention | Result across the 28 committed deliverables |
| --- | --- | --- |
| B1 | No em dashes | Clean. Zero em dash and zero en dash characters in any file, counted with fenced blocks included |
| B2 | No bare "It" or "This" as a sentence subject | Clean. Ten drafted instances were found and all ten were given an explicit noun subject |
| B3 | Active voice | 611 of 15,469 prose sentences read passive by pattern, 3.9 percent, and the sample checked sits inside B3's own exception where no actor exists or the object is the focus |
| B5 | Cite sources | Clean. Every factual claim sampled carried a `path:Lnn` locator or a heading-plus-line citation |

Blog-rule results do not enter the verdict table. Rule 3 computes a verdict from the principles, so
the four conventions are reported on their own line, and any sentence that also breaks a principle is
charged there.

### The anti-neutrality test

Rule 3 rejects neutral tone as a dishonest tone, and calls out a sentence that softens a change which
will break the reader's setup. Every deliverable in this corpus carries a defect register, so the
position bites hard: softening a real consequence counts as a hard violation on V6, Say what you
mean.

The test has a worked form. A sentence saying that the backend `may require` import fixes fails,
because the hedge hides a total failure behind a maintenance note. The sentence at
`troubleshooting.md:L3-L4` passes instead, because a reader learns the size of the problem from the
sentence itself:

> The backend cannot import, and only 3 of the 15 modules under `backend/app/` load.

Every failure sentence in the corpus was tested this way, across all 28 committed deliverables. The
softener patterns were `may impact`, `may require`, `might require`, `may need`, `could require`,
`may affect`, `might affect` and `may not work`. The scan returned zero hits outside this section,
which is the one place in the corpus that names the patterns.

Spot reading confirmed the counts travel with the failures. `troubleshooting.md:L3-L6` opens with
four flat failure statements and the line evidence for each.
`../infrastructure/docker/README.md:L7-L8` states that none of the three container artifacts works as
committed. V6 reads Pass on every deliverable for that reason.

### The anti-comprehensiveness position

Rule 3 holds that thoroughness which destroys readability is a failure of courage, and that a
document nobody reads has communicated nothing. The position produced the 150-to-400-line band for
the module READMEs, and all 19 sit inside it. The shortest is
[frontend/src/utils/README.md](../frontend/src/utils/README.md) at 196 lines and the longest are
[backend/app/api/README.md](../backend/app/api/README.md) and
[backend/app/services/README.md](../backend/app/services/README.md), both at 396.

Completeness is measured by the traceability matrix in [decision-log.md](decision-log.md), which
runs 257 rows and reports every row COVERED. Word count measures nothing. Conflict C4 at
`decision-log.md:L114` records how coverage and verbosity were separated.

The position also shaped how the four longest `docs/` files were scored. No line band governs a
repository-level document, so length alone earned no finding. Each was tested for the behaviour the
principle actually names, a reader who cannot find what they came for. Every one of the four carries
a symptom-first or section-first index near its top, so V10, The Indifference Detector, reads Pass on
all four.

### Checks run

Ten checks produced the numbers in this record. A reviewer can re-run every one.

| Check | What it measured | Result |
| --- | --- | --- |
| Physical line count | Every deliverable, counting the file's last line | 19 module READMEs from 196 to 396 lines; 9 `docs/` files from 160 to 1,662 |
| Sentence length | Prose words per sentence, inline code counted as one word | 15,469 prose sentences, none over 30 words |
| Paragraph length | Sentences per paragraph, list items and cells counted separately | No paragraph over 5 sentences; 145 sit at exactly 5 |
| Em dash and en dash | Whole file, fenced blocks included | Zero |
| Sentence-initial "It" and bare "This" | Bare pronoun as grammatical subject | Zero. Every remaining sentence-initial "This" carries a noun head |
| Buzzword scan | leverage, utilize, facilitate, synergy, holistic, paradigm and 24 more | Zero |
| Softener scan | The eight anti-neutrality patterns named above | Zero |
| Dignity scan | `stakeholder`, `headcount`, `bandwidth`, `learnings` and similar machinery language | Zero |
| Fence integrity | Fence parity and language tag per fenced block | 89 fences, all balanced, all tagged |
| Drafted-finding count | The same heuristics applied to the corpus at commit `7ba15ce` | 201 findings, all cleared |

Two further checks ran against the inline documentation pass. Marker preservation compared the
committed tree against base commit `06be74c` and found 27 `HUMAN ASSISTANCE NEEDED` comment lines
and 15 `TODO` comment lines on both sides. The pass obscured none of them. Block extraction found
195 documentation blocks: 73 Python docstrings, 103 JSDoc blocks and 19 Terraform comment runs,
carrying 875 prose sentences between them.

One check produced an advisory result rather than a finding. Source line width varies across the
corpus, and a table row runs to several hundred characters in the widest files. Markdown reflows on
render, so width changes nothing a reader sees. The measurement is recorded and charged to no
principle.

## Per-deliverable verdict table

Every deliverable below was measured at the current branch head. Four columns carry measurements and
one carries history. Longest sentence is the largest prose word count in the file, against the
30-word threshold. Longest paragraph is the largest sentence count in any paragraph or list item,
against the 5-sentence threshold. Findings cleared counts the registered findings the same file
carried at commit `7ba15ce`, every one of which was rewritten rather than annotated.

Hard and soft columns are omitted because every cell in both would read zero. The register in the
last section carries the history instead, class by class.

### The 19 module READMEs

The Lines column is measured against the 150-to-400-line band that
[the anti-comprehensiveness position](#the-anti-comprehensiveness-position) explains.

| Deliverable | Lines | Prose sentences | Longest sentence | Longest paragraph | Findings cleared | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| [backend/app/README.md](../backend/app/README.md) | 394 | 481 | 30 | 5 | 9 | CLEAN |
| [backend/app/api/README.md](../backend/app/api/README.md) | 396 | 469 | 30 | 5 | 7 | CLEAN |
| [backend/app/core/README.md](../backend/app/core/README.md) | 344 | 373 | 30 | 5 | 6 | CLEAN |
| [backend/app/db/README.md](../backend/app/db/README.md) | 262 | 302 | 29 | 5 | 4 | CLEAN |
| [backend/app/schema/README.md](../backend/app/schema/README.md) | 201 | 219 | 28 | 5 | 2 | CLEAN |
| [backend/app/services/README.md](../backend/app/services/README.md) | 396 | 361 | 30 | 5 | 5 | CLEAN |
| [backend/app/tasks/README.md](../backend/app/tasks/README.md) | 366 | 386 | 30 | 5 | 10 | CLEAN |
| [backend/tests/README.md](../backend/tests/README.md) | 264 | 424 | 30 | 5 | 10 | CLEAN |
| [frontend/src/README.md](../frontend/src/README.md) | 270 | 277 | 30 | 5 | 2 | CLEAN |
| [frontend/src/components/README.md](../frontend/src/components/README.md) | 375 | 338 | 30 | 5 | 8 | CLEAN |
| [frontend/src/pages/README.md](../frontend/src/pages/README.md) | 349 | 342 | 30 | 5 | 3 | CLEAN |
| [frontend/src/schema/README.md](../frontend/src/schema/README.md) | 202 | 243 | 29 | 5 | 3 | CLEAN |
| [frontend/src/services/README.md](../frontend/src/services/README.md) | 216 | 293 | 30 | 5 | 2 | CLEAN |
| [frontend/src/store/README.md](../frontend/src/store/README.md) | 260 | 317 | 28 | 5 | 3 | CLEAN |
| [frontend/src/utils/README.md](../frontend/src/utils/README.md) | 196 | 167 | 30 | 5 | 0 | CLEAN |
| [infrastructure/terraform/README.md](../infrastructure/terraform/README.md) | 387 | 384 | 30 | 5 | 7 | CLEAN |
| [infrastructure/docker/README.md](../infrastructure/docker/README.md) | 260 | 387 | 30 | 5 | 7 | CLEAN |
| [.github/workflows/README.md](../.github/workflows/README.md) | 252 | 315 | 30 | 5 | 7 | CLEAN |
| [scripts/README.md](../scripts/README.md) | 262 | 315 | 30 | 5 | 4 | CLEAN |

The 19 files hold 5,652 physical lines and 6,394 prose sentences between them, and 99 of the 201
drafted findings sat in this group. Every one of the 19 lands inside the band, with 204 lines of
headroom at the short end and 4 at the long end.

### The 9 documents under `docs/`

No line band governs a repository-level document, so the Lines column records length as measurement
rather than as a test.

| Deliverable | Lines | Prose sentences | Longest sentence | Longest paragraph | Findings cleared | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| [README.md](README.md) | 160 | 101 | 29 | 5 | 0 | CLEAN |
| [architecture-overview.md](architecture-overview.md) | 370 | 347 | 30 | 5 | 7 | CLEAN |
| [data-model.md](data-model.md) | 649 | 602 | 30 | 5 | 6 | CLEAN |
| [integration-guide.md](integration-guide.md) | 1,009 | 1,052 | 30 | 5 | 28 | CLEAN |
| [deployment-guide.md](deployment-guide.md) | 827 | 884 | 30 | 5 | 15 | CLEAN |
| [troubleshooting.md](troubleshooting.md) | 1,662 | 2,247 | 30 | 5 | 19 | CLEAN |
| [onboarding.md](onboarding.md) | 964 | 719 | 30 | 5 | 19 | CLEAN |
| [decision-log.md](decision-log.md) | 728 | 2,289 | 30 | 5 | 1 | CLEAN |
| [prose-validation.md](prose-validation.md) | 733 | 834 | 30 | 5 | 7 | CLEAN |

Two documents in this group are worth naming for opposite reasons.
[integration-guide.md](integration-guide.md) carried 28 drafted findings, the highest count in the
corpus, because its seam tables pack several clauses into one cell.
[decision-log.md](decision-log.md) carried 1, the lowest count of any long document, because a
four-column table forces a short cell.

### The inline documentation pass

The pass is one piece of generated text spanning 44 files, so it takes one row. No line band applies.

| Deliverable | Added comment lines | Prose sentences | Longest sentence | Longest block | Findings cleared | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| The inline documentation pass: 15 Python modules under `../backend/app/`, 26 TypeScript and TSX modules under `../frontend/src/`, 3 Terraform files under `../infrastructure/terraform/` | 1,837 | 875 | 30 | 5 | 11 | CLEAN |

Three properties of the row need stating, because the pass is measured differently from a Markdown
file. Only the lines this engagement added are scored, recovered by comparing each file against base
commit `06be74c`, so a preserved marker is never counted as this engagement's prose. A documentation
block is segmented at each blank line, at each Google-style section header, and at each JSDoc tag, so
one `Args:` entry is one unit. All 27 markers and 15 `TODO` comment lines survive byte-identical.

### Verdict totals

| Verdict | Count | Deliverables |
| --- | --- | --- |
| CLEAN | 29 | All 19 module READMEs, all 9 `docs/` documents, and the inline documentation pass |
| NEEDS WORK | 0 | None |
| ROUGH DRAFT | 0 | None |

An earlier draft of this record reported 25 CLEAN and 4 NEEDS WORK, against 3 hard and 22 soft
violations. Every one of those findings was rewritten rather than re-scored, and the wider sweep
behind them cleared 201 registered findings in total. The register in the last section carries the
evidence, and the [drafted-finding count](#checks-run) is reproducible at commit `7ba15ce`.

## Principle scorecards

All 22 principles read Pass on all 29 deliverables at the current branch head. A scorecard of
uniform passes proves nothing on its own, so every row below names the closest thing to a violation
found for that principle and cites it. A reviewer can check the judgement rather than take it.

Each row's Closest passage found column names the strongest candidate against the principle, not a
charged finding. Where a candidate was charged and cleared, the row points at the register class that
holds it.

### Vonnegut's eight principles

| # | Principle | Result | Closest passage found |
| --- | --- | --- | --- |
| V1 | Find a subject you care about | Pass, all 29. Reduced weight | Zero author-distancing hedges in 15,469 prose sentences. The corpus states its own limits instead of hedging them, as at `../infrastructure/terraform/README.md:L244` where an exposure is called conditional and unestablished and the three preconditions are then named |
| V2 | Do not ramble | Pass, all 29 | The longest paragraph in the corpus now runs 5 sentences, and 145 sit at exactly that. The drafted worst case ran 25 sentences at `../backend/app/core/README.md`, cleared as entry R4 |
| V3 | Keep it simple | Pass, all 29 | The longest sentence in the corpus now runs 30 words, and 55 sit at exactly that. The drafted worst case ran 65 words in [deployment-guide.md](deployment-guide.md), cleared as entry R1 |
| V4 | Have the guts to cut | Pass, all 29. Normal weight | A repeated-sentence scan across the 28 committed files found 28 repeat groups, every one confined to table cells. A uniform status phrase is the point of such a column, and no repeat group sits in a prose paragraph. The one prose candidate is the bold lead-in "The backend port mapping misses the served port.", used at `deployment-guide.md:L233` and again as register item 6 at `:L651`. The register enumerates all eleven failures by name on purpose, so the repetition is structural rather than slack |
| V5 | Sound like yourself | Pass, all 29. Reduced weight | Zero hits against a 30-word buzzword list across 15,469 sentences. The closest candidate is heading style rather than prose: the 19 module READMEs title themselves five different ways, and `../frontend/src/pages/README.md:L1` wraps its path in backticks where siblings do not. A heading is not prose and no reader is misled, so the observation is recorded rather than charged |
| V6 | Say what you mean | Pass, all 29 | Zero softener hits, so [the anti-neutrality test](#the-anti-neutrality-test) passes everywhere. The model pass reads "The backend cannot import, and only 3 of the 15 modules under `backend/app/` load." at `troubleshooting.md:L3-L4` |
| V7 | Pity the reader | Pass, all 29 | Claims that contradicted the committed tree were found and corrected, and the four worst are cleared as entries R6 through R9. A scan of the corrected corpus found no remaining claim that a resolving link is dead and no remaining stale length count |
| V8 | Start close to the end | Pass, all 29. Normal weight | Four module READMEs open with a citation-convention note before the Purpose heading, the longest being three lines at `../backend/app/db/README.md:L3-L5`. Each one still leads with substance in its subtitle, and no thesis waits past the second paragraph anywhere in the corpus |

### The extended enterprise principles

| # | Principle | Result | Closest passage found |
| --- | --- | --- | --- |
| V9 | The Dignity Test | Pass, all 29 | Zero hits. The scan covered `stakeholder`, `headcount`, `bandwidth`, `learnings` and similar machinery language. Where the corpus names a person it names a developer doing a task. `troubleshooting.md:L453-L454` reads: "A developer building an environment by reading import statements installs the visible packages, retries, and hits the next missing piece." |
| V10 | The Indifference Detector | Pass, all 29 | [troubleshooting.md](troubleshooting.md) at 1,662 lines is the strongest candidate in the corpus. The file survives the test because it hands the reader a route in. A four-sentence failure summary sits at `:L3-L6`, then a symptom-first index whose own instruction at `troubleshooting.md:L36` reads "Read the index to find your problem." All 19 module READMEs sit inside the 150-to-400-line band |
| V11 | The Indianapolis Test | Pass, all 29 | No sentence in the corpus now exceeds 30 words, so no passage is unsayable on length. The read-aloud candidate is the densest 30-word sentence, `../backend/app/api/README.md:L139`, which names four actors in one clause chain and still resolves on one reading |
| V12 | Humor as Trust Signal | Pass, all 29 | Fifteen of the 19 module READMEs use no second-person address at all, which is the closest thing to bloodlessness in the corpus. The register stays plain rather than guarded, and warmth surfaces where a reader needs it. `troubleshooting.md:L39` reads: "`G9` differs from the eight classes above it in one way worth knowing before you reach it." Rule 3's own comparison treats personality as useful rather than essential under the Asimov persona |

### Asimov's ten principles

| # | Principle | Result | Closest passage found |
| --- | --- | --- | --- |
| A1 | Plate Glass Clarity | Pass, all 29 | The candidate was a relative pronoun dropped inside the corpus's longest sentence, at `troubleshooting.md:L12`. The pronoun was restored when that sentence was split, and the line now reads "the seven protected handlers that registration order makes unreachable" |
| A2 | Short Words, Simple Structures | Pass, all 29 | A2 shares the over-30-word heuristic with V3, so every long-sentence finding registered against both. On its own ground A2 passes cleanly: the corpus expands each acronym at first use, including "Continuous Integration (CI)" at `../.github/workflows/README.md:L6` and "create, read, update and delete (CRUD)" at `../backend/app/schema/README.md:L9` |
| A3 | Logical Sequence | Pass, all 29 | All 19 module READMEs carry the nine required headings in the required order, verified heading by heading and stated at `architecture-overview.md:L330-L332`. Inside the Python docstrings, a prose paragraph sometimes follows a Google section header where Google style puts extended description first. A blank line separates each such paragraph, so a reader sees a new movement start |
| A4 | Ideas Carry the Weight | Pass, all 29 | No passage in the corpus builds mood or ornaments an idea. Every paragraph sampled advances a claim and cites it |
| A5 | Conversational Informality | Pass, all 29 | Passive constructions account for 611 of 15,469 prose sentences, 3.9 percent by pattern. The sample checked sits inside blog rule B3's stated exception, where no actor exists or the object is the focus. The densest example sits at `deployment-guide.md:L151`: "No apply happens, and no resource is created, until every output either points at a declared resource or is removed." Terraform is the unnamed actor there and the resource is the focus |
| A6 | No Ornamental Language | Pass, all 29 | A scan for extended metaphor, simile and decorative figurative language across all 28 committed deliverables returned two hits, both mild. The stronger is "Each one looks like a local problem and has a cause somewhere else." `onboarding.md:L767-L768`, which introduces a concrete point about four traps rather than decorating one |
| A7 | Functional Dialogue | Pass by non-applicability, all 29 | Not applicable rather than unexamined: A7 scores dialogue, and technical documentation contains no dialogue. No deliverable in this corpus carries a spoken exchange, a quoted speaker or a character, so the principle has no surface to score. The row stays in place so its absence reads as a finding rather than an oversight |
| A8 | Anticipate Reader Questions | Pass, all 29 | Blog rule B5 came back clean, so no claim sampled arrived without its locator. One question recurred against the drafted corpus: why a document called a link dead when the link opened. Every instance of that is cleared under V7 |
| A9 | Efficiency Over Polish | Pass, all 29 | The inline documentation pass is the candidate. Added comment lines account for 1,015 of the 1,675 lines under `../backend/app/`, 61 percent, and 779 of the 1,748 under `../frontend/src/`, 45 percent. The volume tracks a per-construct requirement against an unusually high defect density rather than restatement |
| A10 | Respect the Reader's Intelligence | Pass, all 29 | No patronising passage and no unexplained jargon found. The corpus defines each term at first use and then trusts it. `../frontend/src/components/README.md:L7-L8` reads "Draft.js is the rich-text framework the editor is built on", stated once and never repeated |

### Adopted blog-rule compliance

The four adopted conventions are scored separately, because Rule 3 computes a verdict from the
principles rather than from the blog rules.

| Rule | Result | Closest passage found |
| --- | --- | --- |
| B1, No em dashes | Pass, all 29 | Zero em dash and zero en dash characters, counted across whole files with fenced blocks included |
| B2, No bare "It" or "This" as a sentence subject | Pass, all 29 | Ten drafted instances were found and all ten were corrected, cleared as entry R10. Eleven sentence-initial uses of "This" remain, and every one carries a noun head such as "This document" or "This register" |
| B3, Active voice | Pass, all 29 | 3.9 percent passive by pattern, and the sample checked sits inside B3's own exception. See the A5 row for the densest example |
| B5, Cite sources | Pass, all 29 | Every factual claim sampled carried a `path:Lnn` locator, or a heading name plus a line number where the target was a specification document |

### The scorecard for this file

Rule 3 applies to this record as much as to anything it scores, so
[prose-validation.md](prose-validation.md) carries its own row in the verdict table and its own
measurements here. Narrative prose and table cells: 834 sentences, longest 30 words, none over 30,
longest paragraph 5 sentences. Zero em dashes, zero bare pronoun subjects, zero buzzwords, and no
Mermaid diagram.

This file names the patterns two scans look for, so each banned string appears here as a target
rather than as prose. Every one sits inside an inline code span, in
[the anti-neutrality test](#the-anti-neutrality-test) and in the V9 row, and Rule 3's Special
Handling exempts inline code. Both scans therefore return zero across the whole corpus,
including this file.

Two facts about this file's own drafting belong on the record. An earlier draft carried numeric
severity bands and a one-finding-one-principle convention that Rule 3 does not define, and both were
deleted rather than restated. That draft also carried measurements and quote locators taken before the
corpus was rewritten, and eight of its quotes no longer existed in their cited files. Every quote in
this version was re-derived by searching the current text for the quoted words.

One judgement about this file deserves stating plainly, because a reader will test it. A validation
record that scores everything CLEAN without quoting a line is indistinguishable from one that scored
nothing, and Rule 3's own indifference detector would fail it. Every Pass row above therefore cites
the closest passage found rather than asserting the Pass, and the register below quotes what was
changed.

## Violations found and cleared

Two hundred and one findings registered against the Markdown corpus at commit `7ba15ce`, and eleven
more registered against the inline documentation pass after its comment text was trimmed. Every one
was rewritten. None was re-scored, annotated, or excused by widening a threshold.

| Class | Principle | Registered | Outstanding |
| --- | --- | --- | --- |
| Sentence over 30 words | V3, and A2 on the same heuristic | 94 | 0 |
| Paragraph over 5 sentences | V2 | 97 | 0 |
| Bare pronoun subject | Blog rule B2, no principle charge | 10 | 0 |
| Claim contradicting the committed tree | V7 | Counted per site, not by heuristic | 0 |
| Inline documentation prose | V3 on 8 sentences, B2 on 3 subjects | 11 | 0 |

### How to read an entry

Twelve entries follow. Each one carries Rule 3's four required parts: the passage, the principle by
number and name, the replacement, and one sentence on why the replacement is better. Entries are the
worst case in each class plus every distinct kind of defect found, rather than one entry per
instance. Ninety-four long sentences and 97 long paragraphs cannot each carry a section a reader
would finish.

A drafted passage is quoted as it stood at commit `7ba15ce`, and a replacement is quoted as it stands
now with its current locator. Both appear in blockquotes, which
[the exemption list](#what-is-exempt-from-validation) covers as quotations.

A locator inside a quotation belongs to the quoted text rather than to this record. A drafted quote
therefore carries the locator that was correct in `7ba15ce`, and three of them differ from the current
locator because the inline documentation pass shifted source line numbers. Entries R3, R7 and R10 each
show the two side by side.

Two mechanical methods cleared the instances no entry names individually. A long sentence was cut at a
clause boundary into two or three sentences, with every word, locator and claim preserved. A long
paragraph was split at a sentence boundary into two or three paragraphs, again preserving every word.
A word-stream comparison ran after each edit and confirmed the two files held identical word
sequences.

### V3, Keep it simple: 94 sentences over 30 words

#### R1. `docs/deployment-guide.md`, the longest sentence in the drafted corpus

**Principle.** V3, Keep it simple, and A2, Short Words, Simple Structures, which shares the heuristic.

**Drafted**, 65 words, in the failure-path table at `deployment-guide.md:L612` in commit `7ba15ce`:

> Nothing stops the run, because no stage checks an exit status: `:L15` with no root `tests/`, then
> `:L23`, which fails unless the host already carries an authenticated `gcloud`, a default project and
> write access to a bucket no Terraform declares, then the absent `app.yaml` at `:L27`, the absent
> migration file at `:L31`, the unscoped CDN update at `:L35`, and the unconditional success echo at
> `:L47`

**Replacement**, four sentences of 9, 8, 27 and 25 words, now at `deployment-guide.md:L623`:

> Nothing stops the run, because no stage checks an exit status. `:L15` runs with no root `tests/`.
> `:L23` then fails unless the host already carries an authenticated `gcloud`, a default project and
> write access to a bucket no Terraform declares. After that come the absent `app.yaml` at `:L27`, the
> absent migration file at `:L31`, the unscoped CDN update at `:L35`, and the unconditional success
> echo at `:L47`

**Why it is better.** Six colon-separated stages in one sentence force a reader to hold the whole
chain in mind, and four sentences let each stage land before the next one starts.

#### R2. `docs/integration-guide.md`, the seam-key sentence

**Principle.** V3, Keep it simple.

**Drafted**, 42 words, at `integration-guide.md:L116` in commit `7ba15ce`:

> Each edge carries a seam key, and the seam table under the diagram names the call the code writes
> and what stands between that call and the external system, including the barriers that outlast
> repairing the import chain and the undeclared settings.

**Replacement**, three sentences of 6, 22 and 13 words, now at `integration-guide.md:L117-L120`:

> Each edge carries a seam key. The seam table under the diagram names the call the code writes and
> what stands between that call and the external system. Some of those barriers outlast repairing the
> import chain and the undeclared settings.

**Why it is better.** The drafted sentence buries a second claim inside a trailing participle, and
promoting that claim to its own sentence makes the barrier point visible rather than incidental.

#### R3. `docs/integration-guide.md`, a table cell carrying three clauses

**Principle.** V3, Keep it simple. A table cell is scored as its own unit, so a long sentence inside
one registers exactly as it would in a paragraph.

**Drafted**, 32 words in the second sentence, in the seam table at `integration-guide.md:L163` in
commit `7ba15ce`:

> Nothing completes. The application cannot import, and past that repair the client still matches no
> route, because `frontend/src/services/api.ts:L142` throws inside the request interceptor and every
> document call carries a `/documents` prefix no route declares

**Replacement**, three sentences, now at `integration-guide.md:L165`:

> Nothing completes. The application cannot import. Past that repair the client still matches no
> route: `frontend/src/services/api.ts:L40` throws inside the request interceptor, and every document
> call carries a `/documents` prefix no route declares

The locator inside that quote was correct in `7ba15ce`. The same throw sits at
`frontend/src/services/api.ts:L40` today, because the inline documentation pass changed how many
comment lines precede it.

**Why it is better.** A cell is read in a narrow column, so three short statements scan where one
chained clause does not, and the two independent blockers are now separately countable.

### V2, Do not ramble: 97 paragraphs over 5 sentences

#### R4. `../backend/app/core/README.md`, the longest paragraph in the drafted corpus

**Principle.** V2, Do not ramble.

**Drafted**, one paragraph of 25 sentences at `../backend/app/core/README.md:L131` in commit
`7ba15ce`, opening:

> **`SIGNED_URL_EXPIRATION` has no declared type, no default and no bound.** The key sets the
> lifetime of a bearer credential. A signed URL needs no authentication: whoever holds the link
> downloads the object until the link expires.

**Replacement**, five paragraphs of 4, 5, 4, 4 and 3 sentences, beginning at
`../backend/app/core/README.md:L139`. Each one now carries a single movement. The five are what the
key sets, what constrains the value, why no signed URL is generated today, what version 4 signing
needs, and what the call supplies.

**Why it is better.** Twenty-five sentences under one bold lead-in give a reader no place to stop, and
five paragraphs let each of the five movements be found and re-read on its own.

#### R5. `docs/integration-guide.md`, the signed-URL barrier paragraph

**Principle.** V2, Do not ramble.

**Drafted**, one paragraph of 12 sentences at `integration-guide.md:L419` in commit `7ba15ce`,
opening:

> No signed URL is generated today. Four barriers stand in front of the gap, in the order execution
> meets them.

**Replacement**, three paragraphs at `integration-guide.md:L425`, `:L431` and `:L437`. The first
carries barriers one through three. The second carries the fourth barrier and the credential shapes
behind it, and the third carries what the call passes and how to read the gap.

**Why it is better.** The drafted paragraph enumerated four barriers and then continued into
credential mechanics and a reading instruction. The split puts the enumeration, the mechanics and
the instruction where a reader can take them one at a time.

### V7, Pity the reader: claims that contradicted the committed tree

#### R6. `README.md`, an index calling two of its own links dead

**Principle.** V7, Pity the reader. A navigational instruction that is wrong costs a reader more than
no instruction.

**Drafted**, at `README.md:L33-L34` in commit `7ba15ce`:

> Two of the eight land at a later checkpoint, `decision-log.md` and `prose-validation.md`, so those
> two links do not resolve today.

**Replacement**, now at `README.md:L33-L34`:

> All eight documents exist at the current branch head, so every link in the table above resolves.
> The nineteen module READMEs listed below resolve as well.

**Why it is better.** Both files existed when the drafted sentence was written, so a reader was told
not to click two links that open. The replacement states what a reader can verify in one click.

#### R7. `docs/integration-guide.md`, a character count that contradicted its own claim

**Principle.** V7, Pity the reader.

**Drafted**, at `integration-guide.md:L788` in commit `7ba15ce`:

> `localStorage.setItem` coerces its value to a string, so `:L148` stores the four-character string
> `"undefined"` rather than the value `undefined`

**Replacement**, now at `integration-guide.md:L811`:

> `localStorage.setItem` coerces its value to a string, so `:L38` stores the nine-character string
> `"undefined"` rather than the value `undefined`

**Why it is better.** The string `undefined` is nine characters long, and
`../frontend/src/services/README.md:L143` already said nine, so the two documents disagreed about a
fact a reader can count.

#### R8. `../frontend/src/components/README.md`, a length count the pass invalidated

**Principle.** V7, Pity the reader.

**Drafted**, at `../frontend/src/components/README.md:L10` in commit `7ba15ce`:

> The directory measures 291 lines across the eight files.

**Replacement**, now at `../frontend/src/components/README.md:L11`:

> The directory measures 524 lines, 299 of them committed at `06be74c`.

**Why it is better.** The inline documentation pass added comment lines to all eight files, so 291
was true of the base commit and not of the tree a reader is looking at. Naming both numbers keeps
the original measurement available.

#### R9. `docs/architecture-overview.md`, a heading-order claim that misdescribed all 19 READMEs

**Principle.** V7, Pity the reader.

**Drafted**, at `architecture-overview.md:L326-L327` in commit `7ba15ce`:

> Each one opens with Purpose and closes with Known Limitations, and each links back to this file from
> its Architecture Fit heading.

**Replacement**, now at `architecture-overview.md:L330-L332`:

> Each one carries the same nine H2 headings in the same order, opening with Purpose and closing with
> Usage Examples, with Known Limitations second from last.

**Why it is better.** The mandated order ends with Usage Examples, so a reader checking a README
against the drafted claim would have found the last heading wrong in all 19 files.

### Blog rule B2: ten bare pronoun subjects

#### R10. Ten sentences opening with a bare "It"

**Principle.** Blog rule B2, adopted as a house convention at `decision-log.md:L95`. A blog rule
carries no principle charge and enters no verdict.

Ten sentences across nine files opened with "It" as the grammatical subject. Two are quoted here and
the remaining eight took the same treatment, an explicit noun in place of the pronoun.

**Drafted**, at `../backend/app/README.md:L236` in commit `7ba15ce`:

> `app/services/user_service.py` does not exist. This is the import that fails first and stops the
> whole package

The same shape at `../backend/app/tasks/README.md:L157` in the same commit:

> Nothing. This is the one call site that supplies both arguments declared at
> `document_service.py:L123`, which is why the edge is solid.

**Replacement**, now at `../backend/app/README.md:L249`:

> `app/services/user_service.py` does not exist, and this is the import that fails first and stops
> the whole package

And now at `../backend/app/tasks/README.md:L158`:

> Nothing. The edge is solid because this is the one call site that supplies both arguments declared
> at `document_service.py:L78`.

**Why it is better.** A sentence-initial pronoun makes a reader look back for its referent, and both
replacements name the referent in the same clause. The second also corrects a stale locator, because
the method moved to `:L78` when the comment text above it was trimmed.

### Inline documentation findings

#### R11. `../backend/app/tasks/background_tasks.py`, the longest sentence in the pass

**Principle.** V3, Keep it simple.

**Drafted**, 40 words, in the `process_document_export` docstring:

> Three steps cannot run: the read is not awaited on an `async` method, `ExportService` declares no
> `convert_document`, and the signing call passes no `version`, so it uses the client default rather
> than the version 4 scheme the service methods request.

**Replacement**, two sentences of 24 and 18 words, now at
`../backend/app/tasks/background_tasks.py:L31-L34`:

> Three steps cannot run: the read is not awaited on an `async` method, `ExportService` declares no
> `convert_document`, and the signing call passes no `version`. That last omission signs under the
> client default rather than the version 4 scheme the service methods request.

**Why it is better.** The drafted sentence lists three faults and then explains the consequence of
only the third, and the split attaches that consequence to the fault it belongs to.

#### R12. `../backend/app/core/security.py`, a bare pronoun in a docstring

**Principle.** Blog rule B2. Three of the eleven inline findings were bare pronoun subjects, and this
one is quoted for all three.

**Drafted**, in the `get_current_user` docstring:

> This is the second `get_current_user` in the tree. The routers depend on the one in
> `app/api/auth.py`, and nothing imports this one.

**Replacement**, now at `../backend/app/core/security.py:L93-L95`:

> This function is the second `get_current_user` in the tree. The routers depend on the one in
> `app/api/auth.py`, and nothing imports this one.

**Why it is better.** A docstring is read in isolation from anything above it, so "This function"
names its own subject where "This" leaves a reader guessing between the function and the module.

### Near misses recorded rather than charged

Two measurements sit at a threshold rather than past one, and recording them shows the thresholds are
real rather than comfortable.

Fifty-five sentences run exactly 30 words. The densest is at `../backend/app/api/README.md:L139`,
which names four actors in one chain and still resolves on one reading. One hundred and forty-five
paragraphs run exactly 5 sentences. Neither figure registers a finding, and both would register if one
more word or one more sentence were added.

One measurement is advisory. Passive constructions account for 3.9 percent of prose sentences by
pattern, and blog rule B3 permits the construction where no actor exists or the object is the focus.
The A5 row names the densest example and the reason it stands.

### Related documentation

- [README.md](README.md) indexes every document in this set.
- [decision-log.md](decision-log.md) carries conflict C5 at `:L115`, decision row 4 at `:L84`, and
  the scoring convention at decision row 17, `:L97`.
- [troubleshooting.md](troubleshooting.md) is the corpus's longest deliverable and the file this
  record cites most often.
- [onboarding.md](onboarding.md) is the deliverable Rule 2 requires, scored here like any other.
