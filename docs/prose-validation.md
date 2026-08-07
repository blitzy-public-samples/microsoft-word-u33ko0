# Prose Validation Record

Twenty-nine pieces of generated text carry a verdict below: 25 read CLEAN and 4 read NEEDS WORK.
Rule 3 requires a verdict and a principle scorecard for every piece of generated text. The register
in the last section names 3 hard violations and 22 soft ones, each with the passage quoted and a
replacement written out. Nothing here changes a source file. A rewrite is a proposal for
documentation prose, and every proposal keeps the factual claim, the `path:Lnn` locator and the
consequence of the sentence it replaces.

Conflict C5 in [decision-log.md](decision-log.md) at `:L111` records the gap this file fills. Rule 3
demands a verdict and a scorecard per piece of generated text, and no other enumerated deliverable
can hold them. Decision row 4 at `decision-log.md:L83` records the choice and the risk it carries.

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
scored, and a soft finding against it still appears in the register.

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

A soft finding on V1 or V5 carries less consequence than one on V2, V3, V6 or V7. The Technical class
reduces the first pair and raises the second four. The scorecards flag that difference wherever a V1
or V5 cell is not a Pass.

### Severity levels and verdict thresholds

Rule 3 defines exactly three severity levels:

- **Pass**, no meaningful violation.
- **Soft violation**, could be tighter, but not bad.
- **Hard violation**, clearly breaks the principle; the reader suffers.

Rule 3 defines exactly three verdicts, quoted as thresholds:

- **CLEAN**, zero hard violations, at most 2 soft.
- **NEEDS WORK**, 1-3 hard violations or 4+ soft.
- **ROUGH DRAFT**, 4+ hard violations.

The target for all 28 new files and for the inline documentation pass was CLEAN. Twenty-five
deliverables reached it and four did not.

Those thresholds leave one combination unclassified. Three soft violations with no hard violation
exceeds the CLEAN cap of two soft, and reaches neither the hard-violation floor nor the four-soft
floor for NEEDS WORK. One deliverable lands there,
[deployment-guide.md](deployment-guide.md). The verdict recorded for that combination is NEEDS
WORK, because the deliverable fails the CLEAN test of at most two soft violations.

### Reproducible severity bands

Severity is a judgement, and a judgement a reviewer cannot re-run is worth little. Three principles
carry countable detection heuristics in Rule 3, so each one gets a stated band. A reviewer who
measures the same corpus against these bands reaches the same cells.

| Principle | Pass | Soft violation | Hard violation |
| --- | --- | --- | --- |
| V3, Keep it simple | Longest prose sentence at most 35 words, and under 5 percent of prose sentences over 30 words | Longest prose sentence 36 to 45 words, or 5 percent or more over 30 words | Any prose sentence over 45 words |
| V2, Do not ramble | Longest paragraph at most 8 sentences | Longest paragraph 9 to 15 sentences | Any paragraph over 15 sentences |
| V7, Pity the reader | No claim that contradicts the committed tree | A stale aside that leaves a working link in place | A navigational instruction telling the reader a link is dead when the link resolves |

Rule 3 sets the underlying numbers, not this file. V3 lists "Sentences over 30 words" among its
detection heuristics, V2 lists "Paragraphs over 5 sentences", and V7 lists a reader left to do the
writer's work. The bands above turn each heuristic into a threshold at which the severity changes.

Word counts below count only the words the writer wrote. An inline code span is exempt under Rule 3's
Special Handling, so a locator or an identifier inside backticks adds nothing to a count, however long
it runs. Link text counts and a link destination does not. A paragraph is a run of prose lines between
blank lines, and a list item counts as its own paragraph.

### One finding, one principle

Each finding is charged to exactly one principle, the most precise one available. Where a second
principle shares the same detection heuristic, the scorecard marks that second principle Pass and
names where the finding sits. The 73-word sentence at `troubleshooting.md:L8-L13` is charged to V3,
Keep it simple, so A2, Short Words, Simple Structures reads Pass with a cross-reference rather than
charging one sentence twice. Without the convention, a single long sentence would produce two hard
violations and push a CLEAN document to NEEDS WORK on one defect.

### What is exempt from validation

Rule 3's Special Handling section exempts three kinds of text, and all three exemptions were applied:

- **Code blocks and inline code.** The 89 fenced blocks across the 27 committed deliverables were
  read for language tagging and never scored as prose. An inline code span counts as one word.
- **Mermaid diagram blocks.** The corpus carries 25 of them, and none was scored.
- **Quotations attributed to others.** The longest sentence anywhere in the inline documentation
  pass runs 54 words and sits at `infrastructure/terraform/main.tf:L94`. Those words belong to the
  repository's original authors, not to this engagement: the sentence is the body of a
  `HUMAN ASSISTANCE NEEDED` marker, preserved verbatim. The sentence is therefore exempt, and the
  longest sentence the engagement itself wrote runs 44 words.

Rule 3 also treats deliberate rule-breaking for effect as a choice rather than a violation. One
instance qualifies and is labelled here. The 19 module READMEs repeat six fixed terms, router,
handler, service, adapter, slice and marker, far beyond what blog rule B4 permits. The repetition is
deliberate and [decision-log.md](decision-log.md) records it at `:L94`. No other deliberate
rule-break was found, and no other passage was excused as one.

### What is out of scope

Rule 3 scopes validation to generated text, so two bodies of prose in this repository carry no
verdict and appear in no row below.

- **The root README.** [../README.md](../README.md) predates this engagement and received no edit,
  so no sentence in it was generated here. Conflict C1 at `decision-log.md:L107` records why the
  file stayed untouched. The omission is deliberate, and the file is not a deliverable.
- **The three specification documents under `../documentation/`.** All three predate this
  engagement and were read as reference only. No sentence in them was generated here, so none is
  validated. Where a locator below points into one of the three, the citation names a heading plus a
  line number, following the convention at `README.md:L91-L94`.

### The four adopted blog rules

Rule 3's blog rules apply to blog content, and none of these deliverables is blog content. Four of
the five apply here anyway as house conventions, and B4 does not.
[decision-log.md](decision-log.md) records the scoping at `:L94`, entry 15.

| Rule | Convention | Result across the 27 committed deliverables |
| --- | --- | --- |
| B1 | No em dashes | Clean. Zero em dash or en dash characters in any file |
| B2 | No bare "It" or "This" as a sentence subject | 6 findings, listed in the register as B2-1 through B2-6 |
| B3 | Active voice | 368 of 4,412 prose sentences read passive, 8 percent, and nearly all sit inside B3's own exception where no actor exists or the object is the focus |
| B5 | Cite sources | Clean. Every factual claim sampled carried a `path:Lnn` locator or a heading-plus-line citation |

Blog-rule results do not enter the hard and soft counts in the verdict table. Rule 3 computes a
verdict from the principles, so the four conventions are reported on their own line, and any
sentence that also breaks a principle is charged there.

### The anti-neutrality test

Rule 3 rejects neutral tone as a dishonest tone, and calls out a sentence that says a change "may
impact workflows" when the change will break the reader's setup. Every deliverable in this corpus
carries a defect register, so the position bites hard: softening a real consequence counts as a hard
violation on V6, Say what you mean.

The test has a worked form. A sentence reading "the backend may require import fixes" fails, because
the hedge hides a total failure behind a maintenance note. A sentence reading "the backend cannot
import, and only 3 of the 15 modules under `backend/app/` load" passes, because a reader learns the
size of the problem from the sentence itself.

Every failure sentence in the corpus was tested this way. The scan covered all 27 committed
deliverables. The softener patterns were "may impact", "may require", "might require", "may need",
"could require", "may affect", "might affect" and "may not work", and the scan returned zero hits.

Spot reading confirmed the counts travel with the failures. `troubleshooting.md:L3-L6` opens with
four flat failure statements and the line evidence for each.
`../infrastructure/docker/README.md:L7-L8` states that none of the three container artifacts works as
committed. V6 reads Pass on every deliverable for that reason.

### The anti-comprehensiveness position

Rule 3 holds that thoroughness which destroys readability is a failure of courage, and that a
document nobody reads has communicated nothing. The position produced the 150-to-400-line band for
the module READMEs, and all 19 sit inside it. The shortest is
[frontend/src/utils/README.md](../frontend/src/utils/README.md) at 196 lines and the longest is
[backend/app/api/README.md](../backend/app/api/README.md) at 396 lines. The Notes column of the
verdict table records each measurement.

Completeness is measured by the traceability matrix in [decision-log.md](decision-log.md), which
runs 257 rows and reports every row COVERED. Word count measures nothing. Conflict C4 at
`decision-log.md:L110` records how coverage and verbosity were separated.

The position also shaped how the four longest `docs/` files were scored. No line band governs a
repository-level document, so length alone earned no finding. Each was tested for the behaviour the
principle actually names, a reader who cannot find what they came for. Every one of the four carries
a symptom-first or section-first index near its top, so V10, The Indifference Detector, reads Pass on
all four. [troubleshooting.md](troubleshooting.md) runs 1,542 lines and opens with a
four-sentence failure summary followed by a symptom index, which is the structure the principle asks
for.

### Checks run

Nine checks produced the numbers in this record. A reviewer can re-run every one.

| Check | What it measured | Result |
| --- | --- | --- |
| Physical line count | Every deliverable, counting the file's last line even without a trailing newline | 19 module READMEs from 196 to 396 lines; 8 `docs/` files from 158 to 1,542 |
| Sentence length | Prose words per sentence, inline code counted as one word | 4,412 prose sentences; 49 over 30 words, 1.1 percent |
| Paragraph length | Sentences per paragraph, list items counted separately | 90 paragraphs over 5 sentences; longest 24 |
| Em dash and en dash | Whole file, fenced blocks included | Zero |
| Sentence-initial "It" and "This" | Bare pronoun as grammatical subject | 6 |
| Buzzword scan | leverage, utilize, facilitate, synergy, holistic, paradigm and 24 more | Zero |
| Softener scan | The anti-neutrality patterns listed above | Zero |
| Dignity scan | stakeholder, resource, headcount, bandwidth and similar | Zero |
| Fence integrity | Fence parity and language tag per fenced block | 89 fences, all balanced, all tagged |

Two further checks ran against the inline documentation pass. Marker preservation compared the
committed tree against base commit `06be74c` and found 27 `HUMAN ASSISTANCE NEEDED` comment lines
and 15 `TODO` comment lines on both sides, so the pass obscured none of them. Block extraction found
190 documentation blocks, 73 Python docstrings, 95 JSDoc blocks and 22 Terraform comment runs,
carrying 2,240 prose sentences between them.

One check produced an advisory result rather than a finding. Raw source line width varies from 121
characters at the narrowest file to 763 characters at
`../frontend/src/services/README.md:L7`. Markdown reflows on render, so width changes nothing a
reader sees. The measurement is recorded and charged to no principle.

## Per-deliverable verdict table

Every deliverable below was read before it was scored, and the register in the last section carries
one entry for every violation counted here. Hard and soft counts are counts of principles, not counts
of instances, because Rule 3 judges severity per principle. The two counts and the register match
exactly: 3 hard and 22 soft, 25 entries in total.

### The 19 module READMEs

The Notes column records the measured physical line count against the 150-to-400-line band.

| Deliverable | Hard | Soft | Verdict | Notes |
| --- | --- | --- | --- | --- |
| [../backend/app/README.md](../backend/app/README.md) | 0 | 0 | CLEAN | 382 lines, inside the band. Longest sentence 29 words, longest paragraph 7 sentences. Three B2 convention findings, B2-1 to B2-3, which carry no principle charge |
| [../backend/app/api/README.md](../backend/app/api/README.md) | 0 | 1 | CLEAN | 396 lines, inside the band and the longest of the 19. S1, V3 soft, longest sentence 36 words |
| [../backend/app/core/README.md](../backend/app/core/README.md) | 1 | 0 | NEEDS WORK | 333 lines, inside the band. H3, V2 hard, one 24-sentence paragraph and a second at 18. One B2 convention finding, B2-4 |
| [../backend/app/db/README.md](../backend/app/db/README.md) | 0 | 1 | CLEAN | 254 lines, inside the band. S8, V2 soft, one 11-sentence paragraph. No sentence over 30 words |
| [../backend/app/schema/README.md](../backend/app/schema/README.md) | 0 | 1 | CLEAN | 198 lines, inside the band. S13, V7 soft, one stale forward reference |
| [../backend/app/services/README.md](../backend/app/services/README.md) | 0 | 1 | CLEAN | 394 lines, inside the band. S14, V7 soft, one stale forward reference |
| [../backend/app/tasks/README.md](../backend/app/tasks/README.md) | 0 | 2 | CLEAN | 361 lines, inside the band. S2, V3 soft at 38 words. S15, V7 soft |
| [../backend/tests/README.md](../backend/tests/README.md) | 0 | 2 | CLEAN | 249 lines, inside the band. S3, V3 soft at 42 words and 5.6 percent. S9, V2 soft at 9 sentences |
| [../frontend/src/README.md](../frontend/src/README.md) | 0 | 0 | CLEAN | 261 lines, inside the band. Longest sentence 25 words, the lowest peak in the corpus |
| [../frontend/src/components/README.md](../frontend/src/components/README.md) | 0 | 0 | CLEAN | 391 lines, inside the band. Longest sentence 27 words, longest paragraph 8 sentences |
| [../frontend/src/pages/README.md](../frontend/src/pages/README.md) | 0 | 0 | CLEAN | 351 lines, inside the band. Longest sentence 30 words, exactly at the V3 Pass boundary |
| [../frontend/src/schema/README.md](../frontend/src/schema/README.md) | 0 | 0 | CLEAN | 197 lines, inside the band. No sentence over 30 words, no paragraph over 8 sentences |
| [../frontend/src/services/README.md](../frontend/src/services/README.md) | 0 | 0 | CLEAN | 213 lines, inside the band. Carries the widest raw source line in the corpus, 763 characters, advisory only |
| [../frontend/src/store/README.md](../frontend/src/store/README.md) | 0 | 0 | CLEAN | 252 lines, inside the band. Longest sentence 27 words |
| [../frontend/src/utils/README.md](../frontend/src/utils/README.md) | 0 | 0 | CLEAN | 196 lines, the shortest of the 19 and inside the band. Longest sentence 26 words |
| [../infrastructure/terraform/README.md](../infrastructure/terraform/README.md) | 0 | 0 | CLEAN | 343 lines, inside the band. Longest sentence 31 words, 4 of 125 over 30, 3.2 percent, inside the Pass band. One B2 convention finding, B2-5 |
| [../infrastructure/docker/README.md](../infrastructure/docker/README.md) | 0 | 0 | CLEAN | 247 lines, inside the band. Longest sentence 28 words |
| [../.github/workflows/README.md](../.github/workflows/README.md) | 0 | 1 | CLEAN | 250 lines, inside the band. S4, V3 soft on rate, 4 of 70 over 30 words, 5.7 percent |
| [../scripts/README.md](../scripts/README.md) | 0 | 0 | CLEAN | 249 lines, inside the band. Longest sentence 32 words, 3 of 99 over 30, 3.0 percent, inside the Pass band |

### The 9 documents under `docs/`

No line band governs a repository-level document, so the Notes column records length as measurement
rather than as a test.

| Deliverable | Hard | Soft | Verdict | Notes |
| --- | --- | --- | --- | --- |
| [README.md](README.md) | 1 | 0 | NEEDS WORK | 158 lines. H1, V7 hard: the index tells a reader that two of its own eight links are dead, and both resolve |
| [architecture-overview.md](architecture-overview.md) | 0 | 1 | CLEAN | 355 lines. S16, V7 soft, three stale asides. Longest sentence 34 words, 1.8 percent over 30, inside the V3 Pass band |
| [data-model.md](data-model.md) | 0 | 1 | CLEAN | 618 lines. S17, V7 soft. No sentence over 30 words in 199, the cleanest V3 result of any long document |
| [integration-guide.md](integration-guide.md) | 0 | 2 | CLEAN | 947 lines. S5, V3 soft at 42 words. S18, V7 soft at two sites |
| [deployment-guide.md](deployment-guide.md) | 0 | 3 | NEEDS WORK | 803 lines. S6, V3 soft at 36 words. S19, V7 soft. S22, V4 soft, a duplicated list entry. Three soft with no hard exceeds the CLEAN cap of two and reaches neither NEEDS WORK floor, so the verdict follows the failed CLEAN test |
| [troubleshooting.md](troubleshooting.md) | 1 | 2 | NEEDS WORK | 1,542 lines, the longest deliverable. H2, V3 hard at 73 words. S10, V2 soft at 9 sentences. S20, V7 soft at three sites |
| [onboarding.md](onboarding.md) | 0 | 2 | CLEAN | 795 lines. S11, V2 soft at 10 sentences. S21, V7 soft. Longest sentence 35 words, exactly at the V3 Pass boundary. One B2 convention finding, B2-6, which carries no principle charge |
| [decision-log.md](decision-log.md) | 0 | 0 | CLEAN | 719 lines. Longest sentence 30 words, longest paragraph 5 sentences, zero stale references. The strongest measured result in the corpus |
| [prose-validation.md](prose-validation.md) | 0 | 0 | CLEAN | 1,042 lines. Scored against the same target. Longest sentence 30 words, longest paragraph 5 sentences, zero em dashes, zero bare pronoun subjects |

### The inline documentation pass

The pass is one piece of generated text spanning 44 files, so it takes one row. No line band applies.

| Deliverable | Hard | Soft | Verdict | Notes |
| --- | --- | --- | --- | --- |
| The inline documentation pass: 15 Python modules under `../backend/app/`, 26 TypeScript and TSX modules under `../frontend/src/`, 3 Terraform files under `../infrastructure/terraform/` | 0 | 2 | CLEAN | 190 documentation blocks, 2,240 prose sentences. S7, V3 soft at 44 words. S12, V2 soft at 10 sentences. All 27 markers and 15 TODO comments preserved byte-identical against base commit `06be74c` |

### Verdict totals

| Verdict | Count | Deliverables |
| --- | --- | --- |
| CLEAN | 25 | 16 module READMEs, 6 `docs/` documents, this file, and the inline documentation pass |
| NEEDS WORK | 4 | [../backend/app/core/README.md](../backend/app/core/README.md), [README.md](README.md), [deployment-guide.md](deployment-guide.md), [troubleshooting.md](troubleshooting.md) |
| ROUGH DRAFT | 0 | None. No deliverable reached 4 hard violations |

Three of the four NEEDS WORK verdicts turn on a single hard violation each, and every one of the
three has a rewrite in the register that costs one edit. The fourth,
[deployment-guide.md](deployment-guide.md), carries no hard violation at all and fails only the
two-soft cap.

## Principle scorecards

Four principles carry a violation across this corpus: V2, V3, V4 and V7. The other eighteen read
Pass on every deliverable. Each row below names the worst passage found for that principle, including
the rows that pass, so a reviewer can check the judgement rather than take it.

### Vonnegut's eight principles

| # | Principle | Result | Where it is not Pass | Worst passage found |
| --- | --- | --- | --- | --- |
| V1 | Find a subject you care about | Pass, all 29. Reduced weight under the Technical class | Nowhere | Zero author-distancing hedges in 4,412 prose sentences. The closest candidate refuses the hedge and names its reason: "None of the four can be assessed here, because no version is pinned." `onboarding.md:L197` |
| V2 | Do not ramble | **1 hard, 5 soft** | Hard in [../backend/app/core/README.md](../backend/app/core/README.md). Soft in [../backend/app/db/README.md](../backend/app/db/README.md), [../backend/tests/README.md](../backend/tests/README.md), [troubleshooting.md](troubleshooting.md), [onboarding.md](onboarding.md), and the inline pass | One 24-sentence paragraph opening "`SIGNED_URL_EXPIRATION` has no declared type, no default and no bound." `../backend/app/core/README.md:L128`. Full entry at H3 |
| V3 | Keep it simple | **1 hard, 7 soft** | Hard in [troubleshooting.md](troubleshooting.md). Soft in [../backend/app/api/README.md](../backend/app/api/README.md), [../backend/app/tasks/README.md](../backend/app/tasks/README.md), [../backend/tests/README.md](../backend/tests/README.md), [../.github/workflows/README.md](../.github/workflows/README.md), [integration-guide.md](integration-guide.md), [deployment-guide.md](deployment-guide.md), and the inline pass | A 73-word sentence carrying six colon-separated clauses, `troubleshooting.md:L8-L13`. Full entry at H2 |
| V4 | Have the guts to cut | **1 soft**. Normal weight | Soft in [deployment-guide.md](deployment-guide.md) | `decision-log.md` listed twice in one seven-item list, the second entry repeating "every judgement this engagement made, with its reasoning" word for word. `deployment-guide.md:L773-L777`. Full entry at S22 |
| V5 | Sound like yourself | Pass, all 29. Reduced weight under the Technical class | Nowhere | Zero hits against a 30-word buzzword list across 4,412 sentences. The closest candidate is heading style, not prose: the 19 module READMEs title themselves five different ways, and `../frontend/src/pages/README.md:L1` wraps its path in backticks where five siblings do not. Headings are not prose, and no reader is misled, so the observation is recorded rather than charged |
| V6 | Say what you mean | Pass, all 29 | Nowhere | Zero softener hits, so the anti-neutrality test passes everywhere. Nominalization density peaks at three abstract nouns in a nine-word sentence, `../backend/app/core/README.md:L5`, and the sentence still names a concrete thing. The model pass reads "The backend cannot import, and only 3 of the 15 modules under `backend/app/` load." `troubleshooting.md:L3-L4` |
| V7 | Pity the reader | **1 hard, 8 soft** | Hard in [README.md](README.md). Soft in [../backend/app/schema/README.md](../backend/app/schema/README.md), [../backend/app/services/README.md](../backend/app/services/README.md), [../backend/app/tasks/README.md](../backend/app/tasks/README.md), [architecture-overview.md](architecture-overview.md), [data-model.md](data-model.md), [integration-guide.md](integration-guide.md), [deployment-guide.md](deployment-guide.md), [troubleshooting.md](troubleshooting.md), [onboarding.md](onboarding.md) | "so those two links do not resolve today", `README.md:L34`, said of two links that resolve. Full entry at H1 |
| V8 | Start close to the end | Pass, all 29. Normal weight | Nowhere | Four module READMEs open with a citation-convention note before the Purpose heading, the longest being three lines at `../backend/app/db/README.md:L3-L5`. Each one still leads with substance in its subtitle, and no thesis waits past the second paragraph anywhere in the corpus |

### The extended enterprise principles

| # | Principle | Result | Worst passage found |
| --- | --- | --- | --- |
| V9 | The Dignity Test | Pass, all 29 | Zero hits. The scan covered "stakeholder", "resource", "headcount", "bandwidth" and similar machinery language and returned nothing. Where the corpus names a person it names a developer doing a task: "A developer building an environment by reading import statements installs the visible packages, retries, and hits the next missing piece." `troubleshooting.md:L420-L421` |
| V10 | The Indifference Detector | Pass, all 29 | [troubleshooting.md](troubleshooting.md) at 1,542 lines is the strongest candidate in the corpus. The file survives the test because it hands the reader a route in: a four-sentence failure summary at `:L3-L6`, then a symptom-first index whose own instruction reads "Read the index to find your problem." `troubleshooting.md:L31`. All 19 module READMEs sit inside the 150-to-400-line band |
| V11 | The Indianapolis Test | Pass, all 29 | The 73-word sentence at `troubleshooting.md:L8-L13` is the one passage in the corpus nobody would say out loud. The finding is charged to V3 under the one-finding-one-principle convention, so V11 records it here and counts it there |
| V12 | Humor as Trust Signal | Pass, all 29 | Fifteen of the 19 module READMEs use no second-person address at all, which is the closest thing to bloodlessness in the corpus. The register stays plain rather than guarded: it names failures flatly instead of hedging, and warmth surfaces where a reader needs it, as at `troubleshooting.md:L34`, "differs from the eight classes above it in one way worth knowing before you reach it". Rule 3's own comparison table treats personality as useful rather than essential under the Asimov persona |

### Asimov's ten principles

| # | Principle | Result | Worst passage found |
| --- | --- | --- | --- |
| A1 | Plate Glass Clarity | Pass, all 29 | "the seven protected handlers registration order makes unreachable", inside `troubleshooting.md:L10`. The phrase drops its relative pronoun and needs a second read. The finding is charged to V3, which owns the sentence it sits in |
| A2 | Short Words, Simple Structures | Pass, all 29 | A2 shares the over-30-word heuristic with V3, so every long-sentence finding is charged there. On its own ground A2 passes cleanly: the corpus expands each acronym at first use, including "Continuous Integration (CI)" at `../.github/workflows/README.md:L6` and "create, read, update and delete (CRUD)" at `../backend/app/schema/README.md:L9` |
| A3 | Logical Sequence | Pass, all 29 | Twenty-four of the 73 Python docstrings place a prose paragraph after a Google section header, where Google style puts extended description before the sections. Each one carries an explicit label, "Internal notes.", first at `../backend/app/api/auth.py:L192`, so the reader knows a new movement has started. All 19 module READMEs carry the nine required headings in the required order |
| A4 | Ideas Carry the Weight | Pass, all 29 | No passage in the corpus builds mood or ornaments an idea. Every paragraph sampled advances a claim and cites it |
| A5 | Conversational Informality | Pass, all 29 | Passive constructions account for 368 of 4,412 prose sentences, 8 percent, and nearly all sit inside blog rule B3's stated exception where no actor exists or the object is the focus. The densest example is "No apply happens, and no resource is created, until every output either points at a declared resource or is removed." `deployment-guide.md:L147`, where Terraform is the unnamed actor and the resource is the focus |
| A6 | No Ornamental Language | Pass, all 29 | A scan for extended metaphor, simile and decorative figurative language across all 27 committed deliverables returned two hits, both mild. The stronger is "Each one looks like a local", `onboarding.md:L626`, which introduces a concrete point about four traps rather than decorating one |
| A7 | Functional Dialogue | Pass by non-applicability, all 29 | Not applicable rather than unexamined: A7 scores dialogue, and technical documentation contains no dialogue. No deliverable in this corpus carries a spoken exchange, a quoted speaker or a character, so the principle has no surface to score. The row stays in place so its absence reads as a finding rather than an oversight |
| A8 | Anticipate Reader Questions | Pass, all 29 | Blog rule B5 came back clean, so no claim sampled arrived without its locator. The unanswered question a reader will actually ask is why a document calls a link dead when the link opens, and every instance of that is charged to V7 |
| A9 | Efficiency Over Polish | Pass, all 29 | The inline documentation pass is the candidate: docstrings now account for 2,529 of the 3,043 lines under `../backend/app/`, 83 percent. The volume tracks a per-construct requirement against an unusually high defect density rather than restatement, and the one genuine repetition found anywhere in the corpus is charged to V4 |
| A10 | Respect the Reader's Intelligence | Pass, all 29 | No patronising passage and no unexplained jargon found. The corpus defines each term at first use and then trusts it, as with "Draft.js is the rich-text framework the editor is built on" at `../frontend/src/components/README.md:L8`, stated once and never repeated |

### Adopted blog-rule compliance

The four adopted conventions are scored separately, because Rule 3 computes a verdict from the
principles rather than from the blog rules.

| Rule | Result | Worst passage found |
| --- | --- | --- |
| B1, No em dashes | Pass, all 29 | Zero em dash and zero en dash characters, counted across whole files with fenced blocks included |
| B2, No bare "It" or "This" as a sentence subject | 6 findings | "It is not a statement that any release is safe." `../backend/app/README.md:L89`. Entries B2-1 through B2-6 |
| B3, Active voice | Pass, all 29 | 8 percent passive, nearly all inside B3's own exception. See the A5 row for the densest example |
| B5, Cite sources | Pass, all 29 | Every factual claim sampled carried a `path:Lnn` locator, or a heading name plus a line number where the target was a specification document |

### The scorecard for this file

Rule 3 applies to this record as much as to anything it scores, so
[prose-validation.md](prose-validation.md) carries its own row in the verdict table and its own
measurements here. Narrative prose: 260 sentences, longest 30 words, none over 30, longest paragraph
5 sentences. Replacement text inside the blockquotes: 74 sentences, longest 28 words, none over 30.

Across the whole file: zero em dashes, zero bare pronoun subjects outside the quoted passages, zero
buzzwords, zero softeners, 25 fenced blocks all tagged `text`, and no Mermaid diagram. Passive
constructions account for 29 of the 260 narrative sentences, 11 percent, and each one sits inside
blog rule B3's exception. All 22 principles read Pass, so the verdict is CLEAN and no entry for this
file appears in the register.

Two findings in this file's first draft were caught by the same scans and fixed before commit. The
opening paragraph gave the soft-violation total as 21 where the register holds 22. Eighteen narrative
sentences ran past 30 words, the longest at 40, and every one was split or cut. Recording the
correction costs three sentences and keeps the record honest about its own drafting.

One judgement about this file deserves stating plainly, because a reader will test it. A validation
record that scores everything CLEAN without quoting a line is indistinguishable from one that scored
nothing, and Rule 3's own indifference detector would fail it. Every Pass row above therefore quotes
the worst passage found rather than asserting the Pass, and the section below quotes every violation
in full.

## Violations found

Twenty-five entries follow, 3 hard and 22 soft, matching the counts in the verdict table exactly. Six
further entries record findings against the adopted blog conventions, which carry no principle charge
and enter no verdict.

Each entry carries Rule 3's four required parts: the exact passage, the principle by number and name,
the replacement text, and one sentence on why it is better. A passage appears in a fenced `text`
block, exactly as committed and wrapped as the source file wraps it. A replacement appears in a
blockquote, so the two never blur.

No entry was manufactured. Every rewrite keeps each factual claim, each `path:Lnn` locator and each
consequence of the passage it replaces, and no rewrite proposes a change to production code.

One presentation rule applies throughout. A replacement destined for a module README reproduces that
file's own relative path, shown as literal markup rather than as a live link. Such a path resolves
from the module directory and not from `docs/`, so a live link here would be dead.

### Hard violations

#### H1. `docs/README.md`, V7, Pity the reader

Passage as committed, [README.md](README.md) at `:L33-L34`:

```text
Two of the eight land at a later checkpoint, `decision-log.md` and `prose-validation.md`, so those
two links do not resolve today.
```

Both files are committed and both links resolve, so the index instructs a reader to skip two of its
own eight documents. [decision-log.md](decision-log.md), one of the two, is the single home of every
rationale in the set. Decision row 6 at `decision-log.md:L85` names the exact risk: a stale index
misdirects a reader worse than no index would.

Proposed replacement:

> All eight resolve. [decision-log.md](decision-log.md) carries every judgement this set made, and
> [prose-validation.md](prose-validation.md) carries the clarity verdicts.

Why the replacement is better: the index now sends a reader to the two documents the original told
them to skip, and 18 words fall to 16.

#### H2. `docs/troubleshooting.md`, V3, Keep it simple

Passage as committed, [troubleshooting.md](troubleshooting.md) at `:L8-L13`:

```text
The eight classes below carry every defect this
documentation pass verified against the committed source, and that includes the ones a headline
failure hides: the seven protected handlers registration order makes unreachable, the two credential
prerequisites a version 4 signed URL needs, the Pub/Sub topic nothing creates, the publish error that
is caught and printed rather than raised, the ownership subscript that answers 500 instead of 403, and
the retention sweep's partial-deletion states.
```

The sentence runs 73 prose words, more than twice the 30-word heuristic and the longest in the whole
corpus. Six items hang off one colon, and the first of them drops its relative pronoun, so "the seven
protected handlers registration order makes unreachable" reads as a garden path.

Proposed replacement:

> The eight classes below carry every defect this pass verified against the committed source,
> including six that a headline failure hides:
>
> - the seven protected handlers that registration order makes unreachable
> - the two credential prerequisites a version 4 signed URL needs
> - the Pub/Sub topic nothing creates
> - the publish error caught and printed rather than raised
> - the ownership subscript that answers 500 instead of 403
> - the retention sweep's partial-deletion states

Why the replacement is better: the longest sentence falls from 73 words to 21, all six defects survive
as scannable bullets, and the added "that" removes the garden path.

#### H3. `backend/app/core/README.md`, V2, Do not ramble

Passage as committed,
[../backend/app/core/README.md](../backend/app/core/README.md) at `:L128-L159`. The paragraph runs 24
sentences across 32 unbroken source lines. Its opening and its close are quoted exactly, and the
elision marker names the span it covers:

```text
**`SIGNED_URL_EXPIRATION` has no declared type, no default and no bound.** The key
sets the lifetime of a bearer credential. A signed URL needs no authentication:
whoever holds the link downloads the object until the link expires. The key is
absent from `Settings` entirely, so `config.py:L111-L119` constrains nothing about
it.

[... 18 further sentences, `:L132` through `:L155`, with no paragraph break ...]

The outcome therefore depends on the credential the
environment supplies, and this repository fixes neither the credential type nor the
signing route.
```

A reader who came for the type and the bound must read a wall to find them. The same file carries a
second 18-sentence paragraph at `:L30-L53`, so the pattern is not a single slip.

Proposed replacement, which adds three breaks with a lead-in at each and keeps every sentence in
order. The second block merges the two sentences at `:L132-L134` into one, which also resolves B2-4:

> **`SIGNED_URL_EXPIRATION` has no declared type, no default and no bound.** The key sets the
> lifetime of a bearer credential. A signed URL needs no authentication: whoever holds the link
> downloads the object until the link expires.
>
> **Nothing in the model constrains the value.** The key is absent from `Settings` entirely, so
> `config.py:L111-L119` constrains nothing about it. `Settings` declares no `int`, `timedelta` or
> `datetime` annotation for it, no `Field` with `le` or `ge`, and no validator, so nothing here caps
> the value the process environment supplies.
>
> **Two consequences follow once the key arrives.** Keep `:L134` through `:L139` verbatim, from "A
> unit mistake passes silently" to "a library limit rather than a project policy".
>
> **Three barriers sit in front of the gap, in order.** Keep `:L140` through `:L159` verbatim, from
> "No signed URL is generated today" to the two cross-references.

Why the replacement is better: four labelled paragraphs let a reader reach the type-and-bound answer
in three sentences instead of 24, and no locator changes.

### Soft violations, V3, Keep it simple

Each entry below records a file whose longest prose sentence runs 36 to 45 words, or whose rate of
sentences over 30 words reaches 5 percent.

#### S1. `backend/app/api/README.md`, V3, Keep it simple

Passage as committed, [../backend/app/api/README.md](../backend/app/api/README.md) at `:L55-L58`, 36
prose words:

```text
What a list response would actually contain
cannot be stated from this repository, because neither list handler has a service method behind
it: `documents.py:L142` calls `get_documents`, which `DocumentService` does not define, and
`templates.py` delegates to a `TemplateService` that no file declares.
```

Proposed replacement:

> Neither list handler has a service method behind it, so no list response can be described from this
> repository. `documents.py:L142` calls `get_documents`, which `DocumentService` does not define.
> `templates.py` delegates to a `TemplateService` that no file declares.

Why the replacement is better: three sentences of 19, 5 and 7 words replace one of 36, the point
now comes first, and both locators and both consequences survive.

#### S2. `backend/app/tasks/README.md`, V3, Keep it simple

Passage as committed, [../backend/app/tasks/README.md](../backend/app/tasks/README.md) at
`:L208-L211`, 38 prose words:

```text
Its loop body raises at five
successive points once the earlier layers clear: `:L271` on a record with no `user_id` key, `:L278` on the undeclared
`settings.DOCUMENT_BUCKET_NAME`, `:L280` on an object key no writer produces, `:L283` on `.delete()` against a list, and nothing at
all after `:L284`.
```

Proposed replacement:

> The loop body raises at five successive points once the earlier layers clear:
>
> - `:L271`, on a record with no `user_id` key
> - `:L278`, on the undeclared `settings.DOCUMENT_BUCKET_NAME`
> - `:L280`, on an object key no writer produces
> - `:L283`, on `.delete()` against a list
> - `:L284`, after which nothing runs at all

Why the replacement is better: the lead-in falls to 13 words, all five locators keep their exact
conditions, and a reader can count the raise points without re-reading.

#### S3. `backend/tests/README.md`, V3, Keep it simple

Passage as committed, [../backend/tests/README.md](../backend/tests/README.md) at `:L245-L247`, 42
prose words, in a file where 5 of 89 prose sentences exceed 30 words:

```text
Passing needs more: asserted routes matched to registered routes, the three 201
expectations reconciled against handlers that answer 200, the `set_password`, `get_token`, `add_collaborator`, `remove_collaborator` and `get_collaborators` methods defined,
the six argument shapes corrected, the four coroutines awaited, and the export patch targets pointed at names that exist.
```

Proposed replacement:

> Passing needs six more things:
>
> - asserted routes matched to registered routes
> - the three 201 expectations reconciled against handlers that answer 200
> - the `set_password`, `get_token`, `add_collaborator`, `remove_collaborator` and `get_collaborators` methods defined
> - the six argument shapes corrected
> - the four coroutines awaited
> - the export patch targets pointed at names that exist

Why the replacement is better: the lead-in falls to 5 words, every count and method name survives, and
the six requirements become six items a reader can work through.

#### S4. `.github/workflows/README.md`, V3, Keep it simple

Passage as committed, [../.github/workflows/README.md](../.github/workflows/README.md) at
`:L238-L240`, 34 prose words, in a file where 4 of 70 prose sentences exceed 30 words, a rate of 5.7
percent:

```text
If you must execute them to study the failure, use a disposable non-production project, confirm the active identity first
with `gcloud config list account` and `gcloud config get-value project`, and name the target explicitly with `--project=<disposable-project-id>` rather than
relying on the ambient default.
```

Proposed replacement:

> If you must run them to study the failure, use a disposable non-production project. Confirm the
> active identity first with `gcloud config list account` and `gcloud config get-value project`. Name
> the target explicitly with `--project=<disposable-project-id>` rather than relying on the ambient
> default.

Why the replacement is better: three imperatives of 14, 7 and 12 words replace one of 34, all three
commands survive, and the safety steps now read in order.

#### S5. `docs/integration-guide.md`, V3, Keep it simple

Passage as committed, [integration-guide.md](integration-guide.md) at `:L97-L99`, 42 prose words:

```text
Each edge carries a seam key, and the seam table under the diagram names the call the code
writes and what stands between that call and the external system, including the barriers that outlast
repairing the import chain and the undeclared settings.
```

Proposed replacement:

> Each edge carries a seam key. The seam table under the diagram names the call the code writes and
> what stands between that call and the external system. Some of those barriers outlast repairing the
> import chain and the undeclared settings.

Why the replacement is better: three sentences of 6, 22 and 13 words replace one of 42, and the
surviving barriers now carry their own claim.

#### S6. `docs/deployment-guide.md`, V3, Keep it simple

Passage as committed, [deployment-guide.md](deployment-guide.md) at `:L414-L416`, 36 prose words:

```text
Four stages make up the intended pipeline, and the diagram runs them top to bottom in the order an
operator would reach them: provision with Terraform, build the images, validate on a push to `main`,
then release.
```

Proposed replacement:

> Four stages make up the intended pipeline: provision with Terraform, build the images, validate on
> a push to `main`, then release. The diagram runs them top to bottom, in the order an operator
> reaches them.

Why the replacement is better: two sentences of 20 and 14 words replace one of 36, the four stages
arrive before the note about diagram order, and both facts survive.

#### S7. The inline documentation pass, V3, Keep it simple

Passage as committed, `../backend/app/api/templates.py:L232-L236`, 44 prose words and the longest
sentence the engagement itself wrote:

```text
No external write can be established
    either way: the absent service defines no persistence behavior, so nothing in
    the repository states which fields an update would change, whether the change
    is partial or a full replacement, or whether ownership is checked before the
    write.
```

Proposed replacement:

> No external write can be established either way, because the absent service defines no persistence
> behavior. Three questions have no answer here: which fields an update changes, whether the change
> is partial or a full replacement, and whether ownership is checked before the write.

Why the replacement is better: the cause arrives in 16 words and the three surviving questions follow
in 28, so a reader learns why before what.

### Soft violations, V2, Do not ramble

Each entry below records a file whose longest paragraph runs 9 to 15 sentences.

#### S8. `backend/app/db/README.md`, V2, Do not ramble

Passage as committed, [../backend/app/db/README.md](../backend/app/db/README.md) at `:L31-L42`, one
paragraph of 11 sentences. Its opening and its close are quoted exactly:

```text
The specification places two databases behind this folder, and the committed code delivers one.
`documentation/Technical Specifications.md, SYSTEM DESIGN > DATABASE DESIGN (L315)` describes a hybrid at L317 and restates it at L400.

[... 7 further sentences, `:L33` through `:L41`, with no paragraph break ...]

Repository-wide layering sits in
[../../../docs/architecture-overview.md](../../../docs/architecture-overview.md).
```

Proposed replacement, which keeps every sentence verbatim and in order and adds two breaks:

> Break after "The Cloud SQL half exists as declarations only." at `:L35`, which closes the
> specification-against-code comparison at 5 sentences.
>
> Break after "because nothing subclasses `Base` at `sql.py:L19`." at `:L38`, which closes the
> five-table inventory at 2 sentences.
>
> The remaining 4 sentences, from "One of those tables crossed the boundary." at `:L38` to the
> cross-reference at `:L42`, form the third paragraph.

Why the replacement is better: three paragraphs of 5, 2 and 4 sentences let a reader stop at the
comparison, the table inventory or the boundary crossing.

#### S9. `backend/tests/README.md`, V2, Do not ramble

Passage as committed, [../backend/tests/README.md](../backend/tests/README.md) at `:L109-L115`, one
paragraph of 9 sentences listing eight test patterns:

```text
The suite applies eight patterns, and naming them makes the defect inventory below easier to place. Both pytest fixtures are module-scoped and neither yields nor releases
anything (`test_api.py:L10`, `:L16`). One shared client serves all eight pytest tests, built at import (`:L8`), rather than one client per test.
```

The quoted opening covers the first 3 of the 9 sentences. Six more follow to `:L115` with no break.

Proposed replacement:

> The suite applies eight patterns, and naming them makes the defect inventory below easier to place.
> Keep the eight pattern sentences at `:L109` through `:L115` verbatim, one per bullet, so each
> pattern carries its own locators.

Why the replacement is better: eight patterns in eight bullets can be counted against the word
"eight" in the lead-in, which a 9-sentence paragraph makes impossible, and every locator survives.

#### S10. `docs/troubleshooting.md`, V2, Do not ramble

Passage as committed, [troubleshooting.md](troubleshooting.md) at `:L413-L422`, one paragraph of 9
sentences. Its opening and its close are quoted exactly:

```text
The backend requires seventeen distributions to run, and only ten of them appear in an `import`
line. [../backend/app/README.md](../backend/app/README.md) defines that count and the categories
behind it, and every dependency figure in this document uses them.

[... 5 further sentences, `:L415` through `:L421`, with no paragraph break ...]

The build
fails progressively rather than once. Four properties of this repository cause that pattern:
```

Proposed replacement, which keeps every sentence verbatim and in order and adds two breaks:

> Break after "and every dependency figure in this document uses them." at `:L415`, which closes the
> counting convention at 2 sentences.
>
> Break after "so thirteen of the seventeen have to be named to a package manager." at `:L420`, which
> closes the distribution arithmetic at 5 sentences.
>
> The remaining 2 sentences, from "A developer building an environment" at `:L420` to "Four
> properties of this repository cause that pattern:" at `:L422`, introduce the list that follows.

Why the replacement is better: the counting convention, the arithmetic and the developer's experience
become three paragraphs of 2, 5 and 2 sentences, and every count and locator survives.

#### S11. `docs/onboarding.md`, V2, Do not ramble

Passage as committed, [onboarding.md](onboarding.md) at `:L302-L312`, one paragraph of 10 sentences.
Its opening and its close are quoted exactly:

```text
**An unlocked install is neither reproducible nor auditable.** That is a risk rather than an
inconvenience. `npm install` resolves every declared range and every transitive range to whatever the
registry serves at that moment.

[... 5 further sentences, `:L304` through `:L309`, with no paragraph break ...]

Committing a lockfile changes what the pipeline installs, which makes it a repository change rather
than a documentation change, so this pass leaves the manifest as it found it.
[troubleshooting.md](troubleshooting.md#npm-ci-cannot-run-anywhere) carries the entry.
```

The same file carries a second 9-sentence paragraph at `:L189-L197`.

Proposed replacement, which keeps every sentence verbatim and in order and adds two breaks:

> Break after "and nothing records which resolution either build used." at `:L305`, which closes the
> reproducibility claim at 4 sentences.
>
> Break after "enters the tree unremarked." at `:L307`, which closes the audit consequence at 2
> sentences.
>
> The remaining 4 sentences, from "The generated `frontend/package-lock.json` pins your own machine
> only" at `:L307` to the cross-reference at `:L312`, form the third paragraph.

Why the replacement is better: three paragraphs of 4, 2 and 4 sentences separate the reproducibility
claim, the audit consequence and the reason this pass leaves the manifest alone.

#### S12. The inline documentation pass, V2, Do not ramble

Passage as committed, `../frontend/src/pages/Home.tsx:L4-L16`, one unbroken block of 10 sentences
inside a file-header comment:

```text
 * Header and Footer are default imports of default exports, so both match their
 * modules. Editor, Settings and Templates request a named Header export instead, and
 * Settings and Templates also request a named Footer export. Neither named export exists.
 * The `@/` prefix is absent from the tsconfig paths, so all four `@/` specifiers below fail
 * module resolution.
 * useAppSelector and selectCurrentUser do not exist. store/index.ts exports only RootState,
 * AppDispatch and a default store. store/userSlice.ts exports setUser, clearUser, setLoading,
 * setError and a default reducer, and no selector.
 * The greeting reads currentUser.name, which no user contract declares. schema/user.ts
 * models username and full_name, and Settings reads the same absent field.
 * The three quick-access links at L61, L64 and L67 target /new-document, /open-document and
 * /recent-documents. App.tsx:L52-L55 declares only /, /editor, /templates and /settings, so
 * none of the three targets matches a declared route.
```

Four separate subjects run together with no blank comment line between them: import form, path
prefix, store exports, and route targets.

Proposed replacement, which keeps every sentence verbatim and in order and adds three blank comment
lines:

> Insert a bare comment-continuation line, an asterisk with no text, at three points:
>
> - after "module resolution." at `:L8`
> - after "and no selector." at `:L11`
> - after "reads the same absent field." at `:L13`
>
> The four blocks then hold 3, 2, 3 and 2 sentences.

Why the replacement is better: four subjects become four visually separate blocks, so a reader chasing
one unresolved import stops at the block that names it.

### Soft violations, V7, Pity the reader

Nine deliverables describe a sibling document as uncommitted or unwritten when the document is
committed and the link resolves. Each entry gives the file's own passage and its own replacement. The
severity is soft rather than hard in all nine, because each statement is an aside and each leaves a
working link in place.

#### S13. `backend/app/schema/README.md`, V7, Pity the reader

Passage as committed, [../backend/app/schema/README.md](../backend/app/schema/README.md) at `:L135`:

```text
the planned, not yet committed [decision log](../../../docs/decision-log.md) will record the choice between them.
```

Proposed replacement:

> the `[decision log](../../../docs/decision-log.md)` records the choice between them.

Why the replacement is better: the sentence stops calling a committed file pending, and 13 words fall
to 6.

#### S14. `backend/app/services/README.md`, V7, Pity the reader

Passage as committed, [../backend/app/services/README.md](../backend/app/services/README.md) at
`:L321`:

```text
belong in the planned, not yet committed [decision log](../../../docs/decision-log.md).
```

Proposed replacement:

> belong in the `[decision log](../../../docs/decision-log.md)`.

Why the replacement is better: the phrase now describes where the material sits rather than where it
will sit, and 9 words fall to 3.

#### S15. `backend/app/tasks/README.md`, V7, Pity the reader

Passage as committed, [../backend/app/tasks/README.md](../backend/app/tasks/README.md) at `:L62-L63`:

```text
The planned, not yet committed
[decision log](../../../docs/decision-log.md) will record those inference choices.
```

Proposed replacement:

> The `[decision log](../../../docs/decision-log.md)` records those inference choices.

Why the replacement is better: a reader chasing the inference choices now opens the file instead of
waiting for it, and 12 words fall to 5.

#### S16. `docs/architecture-overview.md`, V7, Pity the reader

Passage as committed, [architecture-overview.md](architecture-overview.md) at `:L51-L52`, the first of
three sites in this file. The other two sit at `:L76` and `:L352`:

```text
Where this engagement made a judgement, [decision-log.md](decision-log.md) will carry the argument.
That file is planned for a later checkpoint and is not committed yet. No rationale lives in this file.
```

Proposed replacement:

> Where this engagement made a judgement, [decision-log.md](decision-log.md) carries the argument. No
> rationale lives in this file.

Why the replacement is better: one false sentence disappears rather than being corrected, 30 words
fall to 16, and the Rule 1 boundary the passage exists to state survives untouched.

#### S17. `docs/data-model.md`, V7, Pity the reader

Passage as committed, [data-model.md](data-model.md) at `:L50-L52`:

```text
Where this engagement made a judgement, the argument belongs in
[decision-log.md](decision-log.md), which this set has not committed yet. No rationale lives in this
file.
```

Proposed replacement:

> Where this engagement made a judgement, the argument sits in
> [decision-log.md](decision-log.md). No rationale lives in this file.

Why the replacement is better: `:L7-L8` already links the decision log without the disclaimer, so
dropping it removes an internal contradiction and cuts 24 words to 17.

#### S18. `docs/integration-guide.md`, V7, Pity the reader

Passage as committed, [integration-guide.md](integration-guide.md) at `:L915`, the second of two sites
in this file. The other sits at `:L52-L53`:

```text
[docs/README.md](README.md) is planned as the index for this documentation set, and is not committed yet.
```

Proposed replacement:

> [docs/README.md](README.md) indexes this documentation set.

Why the replacement is better: the Related documentation section now starts by naming a working entry
point, and 15 words fall to 5.

#### S19. `docs/deployment-guide.md`, V7, Pity the reader

Passage as committed, [deployment-guide.md](deployment-guide.md) at `:L763-L764`:

```text
[docs/README.md](README.md) will index every document in this set once that file lands. Until then,
the list below is the map.
```

Proposed replacement:

> [docs/README.md](README.md) indexes every document in this set. The list below covers the ones this
> guide draws on.

Why the replacement is better: both sentences become true, the second now states what the local list
adds rather than apologising for the first, and 20 words fall to 17.

#### S20. `docs/troubleshooting.md`, V7, Pity the reader

Passage as committed, [troubleshooting.md](troubleshooting.md) at `:L18-L19`, the first of three sites
in this file. The other two sit at `:L93` and `:L1399`:

```text
[decision-log.md](decision-log.md) will hold the record of that boundary, and is planned for a later
checkpoint rather than committed today.
```

Proposed replacement:

> [decision-log.md](decision-log.md) holds the record of that boundary.

Why the replacement is better: a reader learns where the boundary is recorded instead of when it will
be, and 19 words fall to 7.

#### S21. `docs/onboarding.md`, V7, Pity the reader

Passage as committed, [onboarding.md](onboarding.md) at `:L12-L14`:

```text
The
engagement that produced this file left the root README untouched, and
[decision-log.md](decision-log.md) will record that boundary as conflict C1. That file is planned for a
later checkpoint and is not committed yet.
```

Proposed replacement:

> The engagement that produced this file left the root README untouched, and
> [decision-log.md](decision-log.md) records that boundary as conflict C1 at `:L107`.

Why the replacement is better: a locator replaces the false sentence, so a first-day reader reaches
conflict C1 in one click, and 33 words fall to 20.

### Soft violation, V4, Have the guts to cut

#### S22. `docs/deployment-guide.md`, V4, Have the guts to cut

Passage as committed, [deployment-guide.md](deployment-guide.md) at `:L773-L777`, two entries in one
seven-item list naming the same document:

```text
- [decision-log.md](decision-log.md), pending and not yet committed: every judgement this engagement
  made, with its reasoning
- [data-model.md](data-model.md), the Pydantic and Zod contracts and every field divergence
- `docs/decision-log.md`, scheduled and not yet written. A later checkpoint will record every
  judgement this engagement made, with its reasoning
```

The phrase "every judgement this engagement made, with its reasoning" appears twice word for word,
and a reader counting the set's documents counts nine instead of eight.

Proposed replacement:

> - [decision-log.md](decision-log.md), every judgement this engagement made, with its reasoning
> - [data-model.md](data-model.md), the Pydantic and Zod contracts and every field divergence

Why the replacement is better: one entry per document restores the count of eight, the second bullet
is fully deletable without losing a fact, and 42 words fall to 19.

### Adopted-convention findings, B2

Six sentences open with a bare "It" as grammatical subject. Rule 3 rates B2 Hard for blog content,
and none of these deliverables is blog content, so the six carry no principle charge and enter no
verdict. Each is recorded with its replacement because the convention was adopted.

| # | File and locator | Passage as committed | Proposed replacement |
| --- | --- | --- | --- |
| B2-1 | [../backend/app/README.md](../backend/app/README.md) `:L89` | "It is not a statement that any release is safe." | "The word is not a statement that any release is safe." |
| B2-2 | [../backend/app/README.md](../backend/app/README.md) `:L97` | "It is recorded in `../../docs/onboarding.md`, and `../../docs/decision-log.md` records the inference choices below." | "`../../docs/onboarding.md` records that work, and `../../docs/decision-log.md` records the inference choices below." |
| B2-3 | [../backend/app/README.md](../backend/app/README.md) `:L357` | "It prints the chain that stops every other backend task:" | "The command prints the chain that stops every other backend task:" |
| B2-4 | [../backend/app/core/README.md](../backend/app/core/README.md) `:L132-L134` | "It declares no `Field` with `le` or `ge`, and no validator, so nothing here caps the value the process environment supplies." | "`Settings` declares no `Field` with `le` or `ge`, and no validator, so nothing here caps the value the process environment supplies." |
| B2-5 | [../infrastructure/terraform/README.md](../infrastructure/terraform/README.md) `:L281-L282` | "It exits non-zero and names `main.tf`, which carries trailing whitespace at `main.tf:L53` and `main.tf:L55` in the committed bytes." | "The check exits non-zero and names `main.tf`, which carries trailing whitespace at `main.tf:L53` and `main.tf:L55` in the committed bytes." |
| B2-6 | [onboarding.md](onboarding.md) `:L190` | "It is not a recommendation to accept any release." | "The gap is not a recommendation to accept any release." |

Each replacement names the noun the pronoun stood for and keeps every locator and every claim. Five of
the six add a word or two rather than cutting, because naming a referent costs more than hiding one.
Rule 3 asks for a cut only where a cut is possible.

### Near misses recorded rather than charged

Rule 3 forbids nothing about reporting a check that came back clean, and reporting one is more useful
than silence. Five measurements sat close to a threshold and earned no entry above. None was
manufactured into a violation.

| Observation | Measurement | Why no entry |
| --- | --- | --- |
| Heading style across the 19 module READMEs | Five title forms: 15 plain paths, 2 backticked paths, 1 path with a trailing slash, 3 prose titles | A heading is not prose, and no reader is misled by either form |
| Raw source line width | 121 characters at the narrowest file, 763 at `../frontend/src/services/README.md:L7` | Markdown reflows on render, so width changes nothing a reader sees. `MD013` is advisory |
| Passive voice | 368 of 4,412 prose sentences, 8 percent | Nearly all sit inside blog rule B3's own exception, where no actor exists or the object is the focus |
| Docstring volume in the inline pass | 2,529 of 3,043 lines under `../backend/app/`, 83 percent | Per-construct documentation against a high defect density, not restatement. The one genuine repetition found anywhere is charged at S22 |
| Second-person address in the module READMEs | Absent from 15 of the 19 | Register rather than defect. Rule 3's comparison table treats personality as useful rather than essential under the Asimov persona |

### Related documentation

- [README.md](README.md), the index for this documentation set
- [decision-log.md](decision-log.md), which carries conflict C5 at `:L111`, decision row 4 at `:L83`,
  the blog-rule scoping at `:L94` and the anti-comprehensiveness resolution at `:L110`
- Every deliverable scored above, linked from its row in the verdict table
