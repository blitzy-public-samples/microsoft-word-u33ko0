# Decision Log and Traceability Matrix

Fifteen choices shaped the documentation layer over this repository, and a competent engineer
could reasonably have made every one of them differently. The decision table below records each
choice with its alternatives, its reasoning and its risk. The traceability matrix that follows
maps all 257 documented constructs to the artifacts that document them, which is how this layer
proves its own coverage.

## How to read this log

### Rationale lives here and nowhere else

Rule 1, Explainability, makes this file the single source of truth for why decisions were made.
No docstring, no JSDoc block and no README in this repository carries design rationale. Those
artifacts describe behaviour: what a construct does, what parameters it takes, what it returns,
what it raises, what side effects it causes, and which of its imports cannot resolve. When you
want to know **why** a choice was made, come here.

The boundary matters in one direction more than the other. A docstring that says a method
compares a stored `user_id` against the caller is describing behaviour, and belongs in the code.
A sentence arguing that the field should have been named `owner_id` is rationale, and belongs in
the decision table below.

### Citation format

Every factual claim carries a locator in the form `path:Lnn`. A range such as `L65-L73` covers
every line in the span, inclusive. Locators point at the committed state at the current branch
head, which includes the documentation comments this engagement added to 44 source files. The
convention comes from [README.md](README.md), and this file follows it without exception.

Line numbers are physical. No source or configuration file in this repository ends with a
newline, so `wc -l` reports one line fewer than the file contains. Every locator in the matrix
below was asserted mechanically: a checker read the cited span and confirmed the named symbol
appears inside it. No row is estimated.

A locator always carries its full repository-relative path. A code span holding a bare
filename, such as `main.py:L38`, is a short label for reading convenience. The
authoritative locator for that construct sits in the Location column beside it.

Documents under `documentation/` are cited by heading name plus line number, never by section
number, because all three use unnumbered headings only. A numbered section citation anywhere in
this file refers to the generated Technical Specification, which is a separate document, and the
text says so wherever one appears.

### What COVERED means

A matrix row reads COVERED when three conditions hold together.

1. A module README owns the construct and names it under one of its nine headings.
2. The construct carries inline documentation, or sits in a file the requirements exclude from
   inline documentation, in which case the cell says so explicitly.
3. At least one repository-level document under `docs/` places the construct in a wider context.

Rule 1 demands full coverage with no gaps, so every Status cell reads COVERED. A cell reading
anything else would mean either an artifact documents nothing or a construct is documented
nowhere. The reverse matrix in the final section exists to expose both failures.

### Section map

| Section | What you will find |
| --- | --- |
| [The decision table](#the-decision-table) | Nineteen choices, their alternatives, their reasons and their risks |
| [Deviations from a literal reading](#deviations-from-a-literal-reading-of-the-requirements) | Eleven deviations: five rule conflicts, five corrections, one re-anchoring |
| [The traceability matrix](#the-source-construct-to-documentation-artifact-traceability-matrix) | 257 rows, source construct to documenting artifact |
| [The reverse matrix](#the-reverse-matrix) | 28 rows, one per new artifact, running the mapping backwards |

Two vocabulary notes. **AAP** expands to Agent Action Plan, the plan that governs this
engagement. A **marker** is a `HUMAN ASSISTANCE NEEDED` comment, written by the original authors
to flag code they were not confident in.

## The decision table

Nineteen decisions sit below. Each one is a choice a competent engineer could reasonably have made
differently, which is the test Rule 1 sets. Entries 1 through 4 resolve collisions between the
user-specified rules and the requirements, and the next section traces every collision by
identifier. Entries 16 through 18 govern how this documentation counts, scores and sites its own
evidence, and entry 19 governs the shape of the defect register itself.

| What was decided | What alternatives existed | Why this choice was made | What risks it carries |
| --- | --- | --- | --- |
| **1. The root README stays reference material.** [../README.md](../README.md) receives no edit. A new [onboarding.md](onboarding.md) carries Rule 2's substance. | Edit the root README to correct its six false statements and add a link to `docs/`. | The requirements name that one file as reference rather than a rewrite target, and the instruction about a single named file is the more specific directive. Rule 2's goal, a developer reaching a modifiable application without asking questions, is fully reachable in a new document. | Nothing links into `docs/` from the repository's front door. A reader arriving at the root sees an inaccurate README, follows `pip install -r requirements.txt` against a file that does not exist, and never finds this documentation set. |
| **2. Docstrings describe, only this log justifies.** Inline documentation carries purpose, parameters, returns, raises, side effects and factual statements about broken state. Design rationale lives here. | Let each docstring explain why its design choice was made, next to the code it concerns. | Rule 1 names this log the single source of truth for why decisions were made. Describing what a function does is a different act from justifying a decision, and only the second is rationale. | A reader of a docstring must open a second file to learn why a construct exists in that shape. Rationale and code drift apart when one changes without the other. |
| **3. Onboarding documents the honest path.** [onboarding.md](onboarding.md) names the steps that work, the exact line where a run stops, and the remediation each blocker needs. | Repair the absent `settings` singleton and the unresolved module paths so a clean machine reaches a running application, then write the guide against a working system. | Repair is a logic change, and the minimal change clause forbids one. A guide promising a running application would be false at its first command, because `import app.main` fails at `backend/app/api/auth.py:L19`. | A reader expecting working setup instructions gets a blocker register instead. Following the guide end to end leaves the application still not running. |
| **4. Prose verdicts go in their own file.** `prose-validation.md` holds Rule 3's verdicts and principle scorecards for all 28 new artifacts. | Place each verdict inside the document it judges, or record no verdicts at all. | Rule 3 requires a verdict and a scorecard for every piece of generated text, and no enumerated deliverable can hold them. Verdicts inside each README would push several past their stated size band. | A contributor editing a README will not see its verdict unless they open a second file, so a scorecard can describe prose that no longer exists. |
| **5. Inline comments stop at the two source globs plus Terraform.** [.github/workflows/README.md](../.github/workflows/README.md) and [scripts/README.md](../scripts/README.md) describe their files from outside. The three `.tf` files are the single configuration exception that receives `#` comments. | Read the phrase naming one exception loosely, and comment the two workflow files and two shell scripts as well. | The requirements name Terraform `.tf` files as the one exception to the two in-scope source globs. The narrower reading cannot over-reach the stated scope, and the wider one can. | Four files carry no inline explanation. A contributor editing `ci.yml` or `deploy.sh` sees no warning in the file itself and must open the neighbouring README to learn that both are broken. |
| **6. A `docs/` index was created although the requirements do not list one.** [README.md](README.md) indexes the eight sibling documents and all 19 module READMEs. | Leave the eight siblings and the 19 module READMEs with no entry point. | Eight sibling documents with no hub are not discoverable, and the root README sits out of scope, so no other file can index them. The requirements also state that cross-linking must be handled inside the `docs/` files. | One more file to keep current. A stale index misdirects a reader worse than no index would, because a reader trusts an index. |
| **7. All four ownership positions documented, none named canonical.** [data-model.md](data-model.md) presents the four code sites and three specification sites together and picks no winner. | Designate `owner_id` or `user_id` as correct and describe the other positions as wrong. | Naming a winner implies the code should change, and the minimal change clause forbids a rename. The four positions are a verifiable fact; which one is correct is a decision the maintainers own. | A reader wanting one answer gets four positions and must decide alone. Authorization depends on the field, and `owner_id` is optional with a default at `backend/app/schema/document.py:L28`, so a document can validate without the field the ownership check reads. |
| **8. Google style for Python docstrings.** `Args:`, `Returns:` and `Raises:` sections, with `Yields:` for the one generator at `backend/app/db/sql.py:L21`. | NumPy style with underlined section headers, or reStructuredText field lists such as `:param x:`. | The user-supplied Python template is Google style, so the shape was already settled before authoring began. No competing convention existed in the repository to preserve, because the source tree carried no docstring at all. | A maintainer who later adopts Sphinx with reStructuredText would have to convert every docstring across 15 modules, covering 15 classes and 43 functions and methods. |
| **9. JSDoc carries documentation tags only.** Blocks use `@param name - description` and `@returns`, with no braced types. | Include braced forms such as `@param {string} documentId`, matching common JavaScript practice. | The TypeScript Handbook supports only documentation tags in TypeScript files, and the signature already declares the type. A braced type duplicates the signature and can drift from it, at which point the comment lies. | A reader used to JavaScript JSDoc may read the absent braces as an omission and add them back, reintroducing the duplication. |
| **10. Every diagram is an inline Mermaid fence.** No generator, no image asset and no pre-render step. | Adopt a diagram generator, or commit pre-rendered SVG and PNG files to an asset directory. | GitHub renders Mermaid natively, and the three specification documents already rely on that across 25 existing fences. Mermaid therefore costs no dependency and no build step. | A Mermaid syntax error renders as a broken block rather than failing a build, so a malformed diagram can ship unnoticed. No pipeline checks the fences. |
| **11. No dependency and no linting configuration added.** `frontend/package.json` gained nothing, and the three Markdown validators run ephemerally on the host toolchain. | Add `markdownlint-cli2`, `markdown-link-check` and `@mermaid-js/mermaid-cli` to the manifest behind a `docs:lint` script. | The requirements forbid new linting configuration by name. All three validators also require Node 18 or newer, while this project's highest documented Node is 14, declared at `../README.md:L22`, `.github/workflows/ci.yml:L17` and `infrastructure/docker/frontend.Dockerfile:L2`. | No pipeline enforces Markdown quality. A later contributor can add an unclosed fence, an untagged code block or a dead link, and nothing in the repository catches it. |
| **12. The unresolved-module example was re-attributed and the change stated.** The example belongs to `backend/app/api/templates.py:L17-L18`, not to `document_service.py`. | Reproduce the requirements' attribution to `document_service.py` as written. | `document_service.py` never imports `app.schema.template`. Repeating the attribution would send a reader to a file where the evidence does not exist, and the reader would conclude the documentation is wrong about everything else too. | A reader comparing this documentation against the original requirements finds a discrepancy. The correction is stated openly here for that reason rather than made silently. |
| **13. Nineteen module READMEs reported, not the stated twenty-one.** One README was created in every directory the requirements name. | Reproduce the stated total of 21 and invent two more directories to reach it. | The requirements' own enumeration yields 8 backend, 7 frontend and 4 infrastructure and automation directories. No named directory was dropped, so the correction adjusts an arithmetic total and not the scope. | A reader auditing against the stated 21 counts a shortfall of two and may hunt for files that were never named. |
| **14. Rule 1's traceability-matrix clause applied by analogy.** The clause is scoped to migrations and refactors. The matrix maps source construct to documentation artifact instead. | Declare the clause inapplicable, because this engagement is neither a migration nor a refactor, and produce no matrix. | The clause's purpose, proving nothing was left behind, transfers cleanly to documentation coverage. A documentation pass with no coverage proof cannot be audited, and Rule 1 requires any departure from a literal reading to be logged, which this entry does. | A 257-row table costs real effort to maintain. Every locator shifts when a source file gains or loses a line, so the matrix goes stale faster than the prose around it. |
| **15. Blog rule B4 declined; four blog rules adopted.** No em dashes, no bare "It" or "This" as a sentence subject, active voice and cited sources all apply. B4 does not. | Adopt B4 and vary the vocabulary with synonyms from the approved dictionary. | B4 flags a non-technical word appearing three or more times per 500 words. The AAP fixes six terms that must repeat across all 28 artifacts: router, handler, service, adapter, slice and marker. Synonym churn on those six would obscure meaning rather than sharpen it. | A reviewer applying B4 mechanically will flag this corpus for repetition. The repetition is deliberate, which this entry records so the flag can be dismissed with evidence. |
| **16. The matrix counts every class statement, so it runs 257 rows and not the 255 the AAP projects.** Fifteen `class` statements exist, and the two beyond the AAP's thirteen are the inner Pydantic `Config` classes at `backend/app/core/config.py:L50` and `backend/app/schema/user.py:L74`. | Report thirteen classes and 255 rows to match the AAP, leaving both `Config` classes out of the matrix. | Rule 1 requires the matrix complete with no gaps. Both inner classes received a class docstring under the inline-documentation requirement, so omitting them would leave documented constructs unlisted and make the no-gaps claim false. The AAP's thirteen is a projection written before the source tree was read. | A reader auditing against the AAP's 255 finds two extra rows and may read them as padding. The [Backend classes heading](#backend-classes-15) and the [matrix totals](#matrix-totals) both state the split, so the two rows can be identified and subtracted. |
| **17. Rule 3's own detection heuristics are the scoring thresholds.** A prose sentence over 30 words registers against the principle it touches, and so does a paragraph over five sentences. Every principle a finding touches is scored on its own. Rule 3 leaves one combination unclassified, three soft violations with no hard violation, and this file records it as NEEDS WORK. | Keep wider local bands that pass a 35-word sentence and an 8-sentence paragraph, and charge each finding to exactly one principle. | Rule 3 sets the numbers, and a local band that passes text the rule flags reports a cleaner corpus than the rule allows. Scoring each principle on its own is what the rule's per-principle scorecard asks for. | The stricter thresholds raise the finding count, so prose that read as acceptable under the wider bands had to be rewritten rather than annotated. Counting remains a choice. Inline code spans are exempt under Rule 3's Special Handling, link text counts while a link destination does not, and a list item counts as its own paragraph. A reviewer who folds list items into the surrounding paragraph measures different paragraph lengths. |
| **18. Every advisory and version-floor rationale sits in one dated register.** [troubleshooting.md](troubleshooting.md) carries the register, with the date it was compiled. A source comment states the contract and the observable defect. Where the contract depends on it, a comment may name the release in which a documented behaviour changed, as `backend/app/core/security.py:L82` does for bcrypt. No source comment carries an advisory identifier, a recommended floor or a dated claim. | Keep each advisory beside the code that carries the risk, or open a separate dated security document. | Rule 1 makes this log and the documents it points at the single rationale surface. An advisory also ages faster than the code it describes, so a source comment goes stale where a dated register announces its own age. AAP section 0.11.1 closes the documentation set at nine `docs/` files, so a new file was not available. | A developer reading a security-relevant function sees no advisory reference in the file itself and must reach the register through the module README. Any version claim is only as current as the register's stated date. |
| **19. The defect register carries a ninth gap class the AAP does not define.** [troubleshooting.md](troubleshooting.md#g9-absent-security-controls) adds `G9 absent security controls` beyond the eight classes the AAP enumerates, holding entries 1 through 40 across five subsections, plus the sub-lettered `22a`, `33a`, `39a` and `39b`. | Fold every absent control into the existing `G1` through `G8` classes, or leave absent controls out of the register entirely, on the ground that the AAP's taxonomy stops at `G8` and every class it names describes something present and wrong. | Each of `G1` through `G8` is defined by a present artifact that is wrong: an absent module referenced by committed code, an absent symbol, an undefined name, an undeclared dependency, a violated call-site contract, drifted field names, a mismatched endpoint, a platform defect. Every one announces itself through a traceback, a type error or a failed command. An absent control produces no error at all, so it fails the defining property of all eight and folding it in would misfile it under a class it does not belong to. Leaving it out would give a security reading of this repository no home in the documentation, and the absences are the findings a reader most needs before repairing the import chain, because every one of them goes live the moment that repair lands. | This class is the only part of the register with no upstream mandate, so a reader auditing the documentation against the AAP's `G1` through `G8` finds a ninth class and cannot trace it to a requirement without this entry. Its entries are also the only ones no command reproduces: each rests on a reading of the code rather than on an observed failure, so a reader cannot confirm one by running anything, and a wrong entry would survive review that a traceback would have caught. The four sub-lettered entries keep earlier numbering stable at the cost of a sequence that no longer runs contiguously. |

## Deviations from a literal reading of the requirements

Rule 1 treats an unexplained deviation as a defect. Eleven deviations are recorded below: five
collisions between the user-specified rules and the requirements, and five interpretive
corrections where verification contradicted a stated fact. The eleventh re-anchors every line
number in this file. Each collision points at the decision-table row that resolves it.

One further departure is not numbered here, because it is neither a collision between two
instructions nor a stated fact that verification contradicted. The defect register carries a ninth
gap class where the requirements enumerate eight, and decision row 19 records what was added, which
alternatives were weighed and what the addition costs a reader.

### The five rule conflicts

| ID | The collision | How it was resolved | Decision row |
| --- | --- | --- | --- |
| C1 | Rule 2 requires updating existing onboarding documentation. The requirements place the root [../README.md](../README.md) out of scope and call it reference material. | The exclusion governs one named file, so the root README stays untouched. A new [onboarding.md](onboarding.md) carries Rule 2's substance. | 1 |
| C2 | Rule 1 forbids rationale in code comments. The requirements ask docstrings to explain why a construct exists where the name does not make that obvious. | Docstrings state the construct's role and its factual defects. Design justification stays in this log. | 2 |
| C3 | Rule 2 requires a path from a clean machine to a running application. The application does not run: `import app.main` fails at `backend/app/api/auth.py:L19`. | [onboarding.md](onboarding.md) documents the working steps, the exact stopping point with evidence, and the remediation each blocker needs. | 3 |
| C4 | Rule 3 rejects thoroughness that destroys readability. The engagement instruction is to be exhaustive. | Coverage and verbosity were separated. Completeness is measured by the matrix below, not by word count, and every table cell stays inside two short sentences. | See note under this table |
| C5 | Rule 3 requires a verdict and a scorecard for every piece of generated text. No enumerated deliverable can hold them. | `prose-validation.md` became that destination. | 4 |

C4 needs no decision row of its own, because the conflict dissolves once coverage and verbosity
are treated as separate measures. A 257-row matrix proves coverage. Short cells preserve
readability. Both standards are met at once, so no trade-off was made and nothing was chosen
against an alternative.

### The five interpretive corrections

Verification against the repository contradicted five stated facts. Recording them here stops a
reader from treating a corrected claim as an error in this documentation.

| ID | What the requirements state | What verification found | Where it is recorded |
| --- | --- | --- | --- |
| A1 | Numbered section references such as a layer diagram at section 5 and intended behaviour at section 5.2.6, against a specification exceeding 12,000 lines. | The in-repository [Technical Specifications](<../documentation/Technical Specifications.md>) runs 781 physical lines and carries 5 unnumbered H1 headings, 17 unnumbered H2 headings and 18 unnumbered H3 headings, so no section anchor exists inside it. | Numbered citations resolve to the generated Technical Specification, a separate document. In-repository citations quote a heading name plus a line number, per the convention in [README.md](README.md). |
| A2 | `document_service.py` imports `app.schema.template` as the worked example of a dependency on an absent module. | `document_service.py` carries no such import. The real site is `backend/app/api/templates.py:L17-L18`, which imports from `app.schema.template` and `app.services.template_service`, and neither module exists. | Decision row 12, and [backend/app/api/README.md](../backend/app/api/README.md). |
| A3 | Twenty-one new README files. | The enumeration yields 19: eight backend directories, seven frontend directories, four infrastructure and automation directories. | Decision row 13, and [README.md](README.md). |
| A4 | The ownership drift is two-way, `owner_id` against `user_id`, with two specification sites. | The drift spans four code positions and **three** specification sites. The third sits at `documentation/Technical Specifications.md:L383`. | [data-model.md](data-model.md), and decision row 7. |
| A5 | Thirteen backend classes, giving 108 construct rows and a matrix of roughly 255 rows. | Fifteen `class` statements exist. Thirteen are model or service classes and two are inner Pydantic `Config` classes, at `backend/app/core/config.py:L50` and `backend/app/schema/user.py:L74`. Construct rows therefore total 110 and the matrix totals 257. | Decision row 16, the [Backend classes heading](#backend-classes-15) and the [matrix totals](#matrix-totals). |

#### The third specification site, in detail

Correction A4 matters enough to spell out, because the AAP cites only two specification sites and
a reader auditing the count would find a third unaccounted for. All three sites use `owner_id`,
and they sit under two different headings.

| Site | Heading it sits under | What it describes |
| --- | --- | --- |
| `documentation/Technical Specifications.md:L333` | Google Cloud Firestore (NoSQL), at `:L319` | The `owner_id` field of the Documents collection |
| `documentation/Technical Specifications.md:L375` | Google Cloud SQL (Relational), at `:L356` | The `owner_id` column of the DOCUMENTS entity |
| `documentation/Technical Specifications.md:L383` | Google Cloud SQL (Relational), at `:L356` | The `owner_id` column of the TEMPLATES entity |

The third site extends the same naming to templates, so the specification is internally
consistent on `owner_id` across both entities. The committed code is not. `backend/app/schema/document.py:L28`
declares `owner_id: Optional[str] = None`, `backend/app/schema/document.py:L84` declares
`user_id: str`, `backend/app/services/document_service.py:L71` writes `user_id` and compares
it at `:L108`, `:L148` and `:L184`, and `frontend/src/schema/document.ts:L27` declares
`owner_id` beside `user_id` at `:L44`. Four positions, and no code change to reconcile them.

### D6, every line number in this file was re-anchored

The one deviation with no counterpart in the AAP gets the same four-part treatment the decision
table uses. A reader checking this file against the AAP will notice the change immediately.

**What was decided.** Every locator in this file cites the current branch head, not the state the
AAP describes. The three worked rows the AAP supplies were reproduced in shape and re-anchored in
locator.

**What alternatives existed.** Reproduce the AAP locators verbatim, including
`document_service.py:L26` for `DocumentService.get_document`, `main.py:L15-L16` for the first
marker, and `document.ts:L3-L11` for `DocumentSchema`.

**Why this choice was made.** The inline-documentation pass has already landed across all 44
source files, so every file grew. `DocumentService.get_document` sat at L26 in the original
79-line module and now sits at `backend/app/services/document_service.py:L78` in a 191-line
module. Three facts settle the choice together.

1. The AAP requires every locator to be real, and a stale locator points a reader at unrelated
   text.
2. [README.md](README.md) at `:L83-L84` already fixes the corpus convention as the current
   branch head.
3. Every sibling artifact already follows that convention, and
   [backend/app/services/README.md](../backend/app/services/README.md) cites `:L78` for the same method.

**What risks it carries.** A reader comparing this file against the AAP finds every locator
changed and may suspect the wrong file. The re-anchoring is a pure offset, and the span lengths
confirm that. The marker occupied two lines before and occupies two now, and `DocumentSchema`
occupied nine lines and still occupies nine.

| Worked row | AAP locator | Locator used here | Span |
| --- | --- | --- | --- |
| `DocumentService.get_document` | `document_service.py:L26` | `backend/app/services/document_service.py:L78` | 1 line, both |
| First `HUMAN ASSISTANCE NEEDED` marker | `main.py:L15-L16` | `backend/app/main.py:L38-L39` | 2 lines, both |
| `DocumentSchema` | `document.ts:L3-L11` | `frontend/src/schema/document.ts:L23-L31` | 9 lines, both |

## The source-construct to documentation-artifact traceability matrix

Rule 1 requires this matrix complete, with no gaps. Every row below reads COVERED, and every
locator was asserted mechanically against the file it cites. The matrix answers one question per
row: for this construct, which README owns it, what inline documentation does it carry, and which
repository-level document places it in context.

Two marker counts appear in this engagement and must not be conflated. **The matrix denominators
are 33 and 16**, the repository-wide totals of `HUMAN ASSISTANCE NEEDED` comments and `TODO`
comments. A second pair, 27 and 15, counts the markers inside the 44 files that received inline
documentation, and measures a preservation obligation rather than a coverage one. The remaining
six markers and one TODO sit in files that were never edited. Three sit in `backend/tests/`,
one in `infrastructure/docker/`, and two markers plus one TODO in `scripts/`.

### How the matrix is organised

The matrix runs to 257 rows, so a single table would be unreadable and would fail Rule 3's
indifference test. Rows are grouped into seventeen subsections by area. Two key tables below
keep each row narrow: the Documenting README column carries a directory path, and the
`docs/` Coverage column carries a filename. Both resolve through the keys.

The AAP projects 255 rows across thirteen backend classes. Verification found fifteen `class`
statements, so construct rows total 110 and the matrix totals 257. Decision row 16 owns that
choice and correction A5 records the count it departs from.

Five groups of files receive no inline documentation, because the requirements exclude them:
three test modules, three container artifacts, two workflow files, two shell scripts and two
frontend manifests. Every row in those groups carries
`None by design (AAP R7)` in the Inline Documentation column and still reaches COVERED, because a
module README documents each one from outside. Decision row 5 records the boundary.

#### Documenting README key

| Path in the matrix | README |
| --- | --- |
| `backend/app` | [backend/app/README.md](../backend/app/README.md) |
| `backend/app/api` | [backend/app/api/README.md](../backend/app/api/README.md) |
| `backend/app/core` | [backend/app/core/README.md](../backend/app/core/README.md) |
| `backend/app/db` | [backend/app/db/README.md](../backend/app/db/README.md) |
| `backend/app/schema` | [backend/app/schema/README.md](../backend/app/schema/README.md) |
| `backend/app/services` | [backend/app/services/README.md](../backend/app/services/README.md) |
| `backend/app/tasks` | [backend/app/tasks/README.md](../backend/app/tasks/README.md) |
| `backend/tests` | [backend/tests/README.md](../backend/tests/README.md) |
| `frontend/src` | [frontend/src/README.md](../frontend/src/README.md) |
| `frontend/src/components` | [frontend/src/components/README.md](../frontend/src/components/README.md) |
| `frontend/src/pages` | [frontend/src/pages/README.md](../frontend/src/pages/README.md) |
| `frontend/src/schema` | [frontend/src/schema/README.md](../frontend/src/schema/README.md) |
| `frontend/src/services` | [frontend/src/services/README.md](../frontend/src/services/README.md) |
| `frontend/src/store` | [frontend/src/store/README.md](../frontend/src/store/README.md) |
| `frontend/src/utils` | [frontend/src/utils/README.md](../frontend/src/utils/README.md) |
| `infrastructure/terraform` | [infrastructure/terraform/README.md](../infrastructure/terraform/README.md) |
| `infrastructure/docker` | [infrastructure/docker/README.md](../infrastructure/docker/README.md) |
| `.github/workflows` | [.github/workflows/README.md](../.github/workflows/README.md) |
| `scripts` | [scripts/README.md](../scripts/README.md) |

#### `docs/` coverage key

| Filename in the matrix | Document |
| --- | --- |
| `architecture-overview.md` | [architecture-overview.md](architecture-overview.md) |
| `data-model.md` | [data-model.md](data-model.md) |
| `integration-guide.md` | [integration-guide.md](integration-guide.md) |
| `deployment-guide.md` | [deployment-guide.md](deployment-guide.md) |
| `troubleshooting.md` | [troubleshooting.md](troubleshooting.md) |
| `onboarding.md` | [onboarding.md](onboarding.md) |

### The three worked rows

The AAP supplies three rows to fix the matrix's shape. All three are reproduced below in that
exact shape, with locators re-anchored to the current branch head per deviation D6. Each of the
three also appears in its own subsection further down, so these are a worked example rather than
three extra rows.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `DocumentService.get_document` | `backend/app/services/document_service.py:L78` | `backend/app/services/README.md` | Google-style docstring per the user template | `docs/data-model.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `main.py:L38` | `backend/app/main.py:L38-L39` | `backend/app/README.md`, Known Limitations | Preserved verbatim; referenced by the module docstring | `docs/troubleshooting.md` | COVERED |
| `DocumentSchema` (no inferred type) | `frontend/src/schema/document.ts:L23-L31` | `frontend/src/schema/README.md` | File header stating the root-cause chain | `docs/data-model.md`, `docs/troubleshooting.md` | COVERED |

### Backend modules (15)

One row per Python module under `backend/app/`. Each carries a module docstring placed above its imports.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `main.py` | `backend/app/main.py:L1-L13` | `backend/app` | Module docstring naming all six unresolved imports | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `api/auth.py` | `backend/app/api/auth.py:L1-L17` | `backend/app/api` | Module docstring; records the duplicated `get_current_user` | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `api/documents.py` | `backend/app/api/documents.py:L1-L20` | `backend/app/api` | Module docstring; records five call-site defects | `data-model.md`, `troubleshooting.md` | COVERED |
| `api/templates.py` | `backend/app/api/templates.py:L1-L14` | `backend/app/api` | Module docstring; names both absent modules at `:L17-L18` | `data-model.md`, `troubleshooting.md` | COVERED |
| `api/users.py` | `backend/app/api/users.py:L1-L15` | `backend/app/api` | Module docstring; records both handlers as synchronous | `data-model.md`, `troubleshooting.md` | COVERED |
| `core/config.py` | `backend/app/core/config.py:L1-L18` | `backend/app/core` | Module docstring; states that no `settings` instance exists | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `core/security.py` | `backend/app/core/security.py:L1-L20` | `backend/app/core` | Module docstring; three undefined names, and `jwt.JWTError` confirmed sound | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `db/firestore.py` | `backend/app/db/firestore.py:L1-L18` | `backend/app/db` | Module docstring; import-time client construction | `integration-guide.md`, `data-model.md` | COVERED |
| `db/sql.py` | `backend/app/db/sql.py:L1-L14` | `backend/app/db` | Module docstring; the declared but unused relational path | `data-model.md`, `deployment-guide.md` | COVERED |
| `schema/document.py` | `backend/app/schema/document.py:L1-L14` | `backend/app/schema` | Module docstring; the `owner_id` and `user_id` split inside one file | `data-model.md`, `troubleshooting.md` | COVERED |
| `schema/user.py` | `backend/app/schema/user.py:L1-L15` | `backend/app/schema` | Module docstring; the absent password field and the Pydantic 1.x pin | `data-model.md`, `troubleshooting.md` | COVERED |
| `services/collaboration_service.py` | `backend/app/services/collaboration_service.py:L1-L18` | `backend/app/services` | Module docstring; two absent imports and the per-process registry | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `services/document_service.py` | `backend/app/services/document_service.py:L1-L12` | `backend/app/services` | Module docstring; async methods wrapping a synchronous SDK | `data-model.md`, `integration-guide.md` | COVERED |
| `services/export_service.py` | `backend/app/services/export_service.py:L1-L16` | `backend/app/services` | Module docstring; the placeholder export payloads | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `tasks/background_tasks.py` | `backend/app/tasks/background_tasks.py:L1-L20` | `backend/app/tasks` | Module docstring; the absent `datetime` import and the invalid decorator | `deployment-guide.md`, `integration-guide.md` | COVERED |

### Backend classes (15)

Fifteen `class` statements exist. Thirteen are model or service classes, the count the AAP reports. The other two are inner Pydantic `Config` classes, carried here so no class is left undocumented, which decision row 16 explains.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `Settings` | `backend/app/core/config.py:L20` | `backend/app/core` | Class docstring listing all nine fields as `Attributes:` | `deployment-guide.md`, `onboarding.md` | COVERED |
| `Settings.Config` | `backend/app/core/config.py:L50` | `backend/app/core` | Class docstring; points Pydantic at an uncommitted `.env` | `deployment-guide.md`, `onboarding.md` | COVERED |
| `DocumentBase` | `backend/app/schema/document.py:L16` | `backend/app/schema` | Class docstring; `owner_id` optional with a default | `data-model.md`, `troubleshooting.md` | COVERED |
| `DocumentCreate` | `backend/app/schema/document.py:L30` | `backend/app/schema` | Class docstring; inherits `DocumentBase` | `data-model.md`, `integration-guide.md` | COVERED |
| `DocumentUpdate` | `backend/app/schema/document.py:L39` | `backend/app/schema` | Class docstring; does not inherit `DocumentBase` | `data-model.md`, `troubleshooting.md` | COVERED |
| `Document` | `backend/app/schema/document.py:L51` | `backend/app/schema` | Class docstring; required timestamps no service writes | `data-model.md`, `troubleshooting.md` | COVERED |
| `DocumentVersion` | `backend/app/schema/document.py:L66` | `backend/app/schema` | Class docstring; names its actor `user_id` | `data-model.md`, `troubleshooting.md` | COVERED |
| `UserBase` | `backend/app/schema/user.py:L17` | `backend/app/schema` | Class docstring; `username` and `full_name`, no `name` | `data-model.md`, `troubleshooting.md` | COVERED |
| `UserCreate` | `backend/app/schema/user.py:L30` | `backend/app/schema` | Class docstring; carries the plaintext password field | `data-model.md`, `integration-guide.md` | COVERED |
| `UserUpdate` | `backend/app/schema/user.py:L40` | `backend/app/schema` | Class docstring; every field optional | `data-model.md`, `troubleshooting.md` | COVERED |
| `User` | `backend/app/schema/user.py:L56` | `backend/app/schema` | Class docstring; flags no code path reads | `data-model.md`, `troubleshooting.md` | COVERED |
| `User.Config` | `backend/app/schema/user.py:L74` | `backend/app/schema` | Class docstring; `orm_mode` pins Pydantic to 1.x | `data-model.md`, `onboarding.md` | COVERED |
| `CollaborationService` | `backend/app/services/collaboration_service.py:L20` | `backend/app/services` | Class docstring; never instantiated by any route | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `DocumentService` | `backend/app/services/document_service.py:L19` | `backend/app/services` | Class docstring listing all four public methods | `data-model.md`, `integration-guide.md` | COVERED |
| `ExportService` | `backend/app/services/export_service.py:L18` | `backend/app/services` | Class docstring; no `convert_document` despite a task calling it | `integration-guide.md`, `troubleshooting.md` | COVERED |

### Backend functions and methods (43)

Every function and method under `backend/app/`, including the nested Pub/Sub `callback`. Docstrings follow Google style with `Args:`, `Returns:` and `Raises:` sections.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `get_current_user` | `backend/app/api/auth.py:L27` | `backend/app/api` | Docstring; duplicate of the `core` version, and returns 404 where `core` returns 401 | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `login_for_access_token` | `backend/app/api/auth.py:L66` | `backend/app/api` | Docstring with `Args:`, `Returns:` and `Raises:`; one of the two public handlers | `integration-guide.md`, `onboarding.md` | COVERED |
| `register_user` | `backend/app/api/auth.py:L103` | `backend/app/api` | Docstring; hashes a password the `User` contract cannot store | `data-model.md`, `troubleshooting.md` | COVERED |
| `create_document` | `backend/app/api/documents.py:L25` | `backend/app/api` | Docstring; passes a `User` object where `user_id: str` is declared | `data-model.md`, `troubleshooting.md` | COVERED |
| `get_documents` | `backend/app/api/documents.py:L50` | `backend/app/api` | Docstring; calls a service method that does not exist | `data-model.md`, `troubleshooting.md` | COVERED |
| `get_document` | `backend/app/api/documents.py:L69` | `backend/app/api` | Docstring; calls the service with one argument against a two-argument signature | `data-model.md`, `troubleshooting.md` | COVERED |
| `update_document` | `backend/app/api/documents.py:L97` | `backend/app/api` | Docstring; reads `document.user_id` off a schema declaring `owner_id` | `data-model.md`, `troubleshooting.md` | COVERED |
| `delete_document` | `backend/app/api/documents.py:L127` | `backend/app/api` | Docstring; same arity and field defects as the read handler | `data-model.md`, `troubleshooting.md` | COVERED |
| `create_template` | `backend/app/api/templates.py:L25` | `backend/app/api` | Docstring; depends on the absent `TemplateService` | `data-model.md`, `troubleshooting.md` | COVERED |
| `get_templates` | `backend/app/api/templates.py:L43` | `backend/app/api` | Docstring; path collides with the documents list handler | `data-model.md`, `troubleshooting.md` | COVERED |
| `get_template` | `backend/app/api/templates.py:L60` | `backend/app/api` | Docstring; shadowed by the documents router, so never reached | `data-model.md`, `troubleshooting.md` | COVERED |
| `update_template` | `backend/app/api/templates.py:L87` | `backend/app/api` | Docstring; shadowed, and depends on the absent template schema | `data-model.md`, `troubleshooting.md` | COVERED |
| `delete_template` | `backend/app/api/templates.py:L113` | `backend/app/api` | Docstring; shadowed by the documents delete handler | `data-model.md`, `troubleshooting.md` | COVERED |
| `get_current_user_info` | `backend/app/api/users.py:L20` | `backend/app/api` | Docstring; declared `def` while every other handler is `async def` | `data-model.md`, `troubleshooting.md` | COVERED |
| `update_user` | `backend/app/api/users.py:L33` | `backend/app/api` | Docstring; awaits nothing and persists nothing | `data-model.md`, `troubleshooting.md` | COVERED |
| `get_settings` | `backend/app/core/config.py:L61` | `backend/app/core` | Docstring with `Returns:` and `Raises:`; carries no caching decorator | `deployment-guide.md`, `onboarding.md` | COVERED |
| `create_access_token` | `backend/app/core/security.py:L25` | `backend/app/core` | Docstring plus a usage example, as a named primary entry point | `integration-guide.md`, `onboarding.md` | COVERED |
| `verify_password` | `backend/app/core/security.py:L57` | `backend/app/core` | Docstring with `Args:` and `Returns:`; bcrypt comparison | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `get_password_hash` | `backend/app/core/security.py:L69` | `backend/app/core` | Docstring; the bcrypt context duplicated from the auth router | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `get_current_user` | `backend/app/core/security.py:L90` | `backend/app/core` | Docstring plus a usage example; three undefined names recorded | `integration-guide.md`, `onboarding.md` | COVERED |
| `get_document` | `backend/app/db/firestore.py:L22` | `backend/app/db` | Docstring plus a usage example; annotated `-> dict` while returning `None` | `data-model.md`, `integration-guide.md` | COVERED |
| `create_document` | `backend/app/db/firestore.py:L45` | `backend/app/db` | Docstring plus a usage example; synchronous, and consumed by no service | `data-model.md`, `integration-guide.md` | COVERED |
| `update_document` | `backend/app/db/firestore.py:L64` | `backend/app/db` | Docstring; synchronous, and consumed by no service | `data-model.md`, `integration-guide.md` | COVERED |
| `delete_document` | `backend/app/db/firestore.py:L79` | `backend/app/db` | Docstring; synchronous, and consumed by no service | `data-model.md`, `integration-guide.md` | COVERED |
| `get_db` | `backend/app/db/sql.py:L21` | `backend/app/db` | Docstring using `Yields:`, the repository's only generator | `data-model.md`, `deployment-guide.md` | COVERED |
| `startup_event` | `backend/app/main.py:L27` | `backend/app` | Docstring; awaits an absent `init_db` and swallows every exception | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `shutdown_event` | `backend/app/main.py:L55` | `backend/app` | Docstring; closes nothing that the module opened | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `CollaborationService.__init__` | `backend/app/services/collaboration_service.py:L32` | `backend/app/services` | Constructor docstring; builds the Pub/Sub clients at construction | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `CollaborationService.connect` | `backend/app/services/collaboration_service.py:L44` | `backend/app/services` | Docstring; registers a socket and returns before subscribing | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `callback` | `backend/app/services/collaboration_service.py:L80` | `backend/app/services` | Docstring; the nested Pub/Sub message handler | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `CollaborationService.disconnect` | `backend/app/services/collaboration_service.py:L103` | `backend/app/services` | Docstring; removes the socket from a per-process dictionary | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `CollaborationService.broadcast_change` | `backend/app/services/collaboration_service.py:L133` | `backend/app/services` | Docstring; blocking `future.result()` inside an async method | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `DocumentService.__init__` | `backend/app/services/document_service.py:L33` | `backend/app/services` | Constructor docstring; binds the shared Firestore client | `data-model.md`, `integration-guide.md` | COVERED |
| `DocumentService.create_document` | `backend/app/services/document_service.py:L42` | `backend/app/services` | Docstring; writes the ownership key as `user_id` | `data-model.md`, `integration-guide.md` | COVERED |
| `DocumentService.get_document` | `backend/app/services/document_service.py:L78` | `backend/app/services` | Google-style docstring per the user template | `data-model.md`, `troubleshooting.md` | COVERED |
| `DocumentService.update_document` | `backend/app/services/document_service.py:L116` | `backend/app/services` | Docstring; read-modify-read path costing three Firestore operations | `data-model.md`, `integration-guide.md` | COVERED |
| `DocumentService.delete_document` | `backend/app/services/document_service.py:L159` | `backend/app/services` | Docstring; ownership comparison explained as non-obvious logic | `data-model.md`, `integration-guide.md` | COVERED |
| `ExportService.__init__` | `backend/app/services/export_service.py:L29` | `backend/app/services` | Constructor docstring; builds the Cloud Storage client | `integration-guide.md`, `deployment-guide.md` | COVERED |
| `ExportService.export_to_pdf` | `backend/app/services/export_service.py:L40` | `backend/app/services` | Docstring; uploads a literal placeholder payload | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `ExportService.export_to_docx` | `backend/app/services/export_service.py:L74` | `backend/app/services` | Docstring; second placeholder payload and a second key layout | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `process_document_export` | `backend/app/tasks/background_tasks.py:L25` | `backend/app/tasks` | Task docstring; no producer enqueues it | `integration-guide.md`, `deployment-guide.md` | COVERED |
| `cleanup_expired_documents` | `backend/app/tasks/background_tasks.py:L73` | `backend/app/tasks` | Task docstring; invalid periodic decorator, and `.delete()` on a result list | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `update_document_statistics` | `backend/app/tasks/background_tasks.py:L116` | `backend/app/tasks` | Task docstring; reads `document.pages`, which no schema declares | `data-model.md`, `troubleshooting.md` | COVERED |

### Frontend modules (26)

One row per TypeScript and TSX module under `frontend/src/`. Each carries a block comment header beginning at line 1, above the imports.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `index.tsx` | `frontend/src/index.tsx:L1` | `frontend/src` | File header; `ReactDOM.render` is the React 17 legacy path | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `App.tsx` | `frontend/src/App.tsx:L1` | `frontend/src` | File header; the v5-only `Switch` and a second `Provider` | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `components/DocumentCanvas.tsx` | `frontend/src/components/DocumentCanvas.tsx:L1` | `frontend/src/components` | File header; the two inverse type errors documented together | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `components/Footer.tsx` | `frontend/src/components/Footer.tsx:L1` | `frontend/src/components` | File header; five hard-coded status values | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `components/Header.tsx` | `frontend/src/components/Header.tsx:L1` | `frontend/src/components` | File header; reads `avatar` and `name`, neither modelled | `data-model.md`, `troubleshooting.md` | COVERED |
| `components/ImageEditor.tsx` | `frontend/src/components/ImageEditor.tsx:L1` | `frontend/src/components` | File header; the absent `imageUtils` module | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `components/Sidebar.tsx` | `frontend/src/components/Sidebar.tsx:L1` | `frontend/src/components` | File header; three absent panel modules rendered unconditionally | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `components/TableEditor.tsx` | `frontend/src/components/TableEditor.tsx:L1` | `frontend/src/components` | File header; the absent `tableUtils` module | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `components/TextEditor.tsx` | `frontend/src/components/TextEditor.tsx:L1` | `frontend/src/components` | File header; presented as the correct-usage reference | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `components/Toolbar.tsx` | `frontend/src/components/Toolbar.tsx:L1` | `frontend/src/components` | File header; one-argument helper calls and lowercase constants | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `pages/Editor.tsx` | `frontend/src/pages/Editor.tsx:L1` | `frontend/src/pages` | File header; the five-second debounce and four named imports of defaults | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `pages/Home.tsx` | `frontend/src/pages/Home.tsx:L1` | `frontend/src/pages` | File header; the correct default imports, noted as the contrast case | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `pages/Settings.tsx` | `frontend/src/pages/Settings.tsx:L1` | `frontend/src/pages` | File header; three non-existent imported symbols | `data-model.md`, `troubleshooting.md` | COVERED |
| `pages/Templates.tsx` | `frontend/src/pages/Templates.tsx:L1` | `frontend/src/pages` | File header; a local interface incompatible with the Zod schema | `data-model.md`, `troubleshooting.md` | COVERED |
| `schema/document.ts` | `frontend/src/schema/document.ts:L1-L12` | `frontend/src/schema` | File header stating the root-cause chain for five downstream errors | `data-model.md`, `troubleshooting.md` | COVERED |
| `schema/template.ts` | `frontend/src/schema/template.ts:L1` | `frontend/src/schema` | File header; diverges from the local interface in `Templates.tsx` | `data-model.md`, `troubleshooting.md` | COVERED |
| `schema/user.ts` | `frontend/src/schema/user.ts:L1` | `frontend/src/schema` | File header; the absent `updated_at` the server declares | `data-model.md`, `troubleshooting.md` | COVERED |
| `services/api.ts` | `frontend/src/services/api.ts:L1` | `frontend/src/services` | File header; the environment variable mismatch and three absent types | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `services/auth.ts` | `frontend/src/services/auth.ts:L1` | `frontend/src/services` | File header; three endpoint paths no server route matches | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `services/collaboration.ts` | `frontend/src/services/collaboration.ts:L1` | `frontend/src/services` | File header; `io()` called with no URL, and no inbound event handled | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `store/documentSlice.ts` | `frontend/src/store/documentSlice.ts:L1` | `frontend/src/store` | File header; the five-entry cap on recent documents | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `store/index.ts` | `frontend/src/store/index.ts:L1` | `frontend/src/store` | File header; two named reducer imports the slices never provide | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `store/userSlice.ts` | `frontend/src/store/userSlice.ts:L1` | `frontend/src/store` | File header; the absent `updateUser` action four modules import | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `utils/documentUtils.ts` | `frontend/src/utils/documentUtils.ts:L1` | `frontend/src/utils` | File header; `DocumentSchema.isValid` recorded as two faults at once | `data-model.md`, `troubleshooting.md` | COVERED |
| `utils/formatting.ts` | `frontend/src/utils/formatting.ts:L1` | `frontend/src/utils` | File header; the unused `SelectionState` import | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `utils/validation.ts` | `frontend/src/utils/validation.ts:L1` | `frontend/src/utils` | File header; the one defect-free module, with discarded messages | `data-model.md`, `troubleshooting.md` | COVERED |

### React components (13)

Thirteen `React.FC` components. Each carries a JSDoc block directly above its declaration, using documentation tags only.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `App` | `frontend/src/App.tsx:L33` | `frontend/src` | Component JSDoc; renders the shell a second time | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `DocumentCanvas` | `frontend/src/components/DocumentCanvas.tsx:L34` | `frontend/src/components` | Component JSDoc; propless signature against a caller passing two props | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `Footer` | `frontend/src/components/Footer.tsx:L21` | `frontend/src/components` | Component JSDoc; two zoom buttons with no handlers | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `Header` | `frontend/src/components/Header.tsx:L30` | `frontend/src/components` | Component JSDoc; absent logo asset and two undeclared routes | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `ImageEditor` | `frontend/src/components/ImageEditor.tsx:L29` | `frontend/src/components` | Component JSDoc; no block renderer, so an atomic image never renders | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `Sidebar` | `frontend/src/components/Sidebar.tsx:L22` | `frontend/src/components` | Component JSDoc; names the three absent panels | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `TableEditor` | `frontend/src/components/TableEditor.tsx:L28` | `frontend/src/components` | Component JSDoc; renders an empty element | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `TextEditor` | `frontend/src/components/TextEditor.tsx:L23` | `frontend/src/components` | Component JSDoc; the correct formatting-helper contract | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `Toolbar` | `frontend/src/components/Toolbar.tsx:L34` | `frontend/src/components` | Component JSDoc; holds no editor state at all | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `Editor` | `frontend/src/pages/Editor.tsx:L28` | `frontend/src/pages` | Page JSDoc; the auto-save effect follows the user template | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `Home` | `frontend/src/pages/Home.tsx:L27` | `frontend/src/pages` | Page JSDoc; three undeclared route links | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `Settings` | `frontend/src/pages/Settings.tsx:L33` | `frontend/src/pages` | Page JSDoc; once-only state initialization leaves the form empty | `data-model.md`, `troubleshooting.md` | COVERED |
| `Templates` | `frontend/src/pages/Templates.tsx:L42` | `frontend/src/pages` | Page JSDoc; write-only state and a terminal card click | `data-model.md`, `troubleshooting.md` | COVERED |

### Exported TypeScript symbols (39)

Thirty-nine `export` statements. Thirteen are the component default exports listed above, kept as separate rows because the export form matters: four modules named-import a default-only export. The remaining 26 are schemas, types, reducers, functions and the two destructured action exports, which carry six and four action creators respectively and name every one.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `export default App` | `frontend/src/App.tsx:L54` | `frontend/src` | JSDoc on the component above; imported correctly by `index.tsx` | `architecture-overview.md` | COVERED |
| `export default DocumentCanvas` | `frontend/src/components/DocumentCanvas.tsx:L74` | `frontend/src/components` | JSDoc on the component above; default-imported by `Editor.tsx` | `architecture-overview.md` | COVERED |
| `export default Footer` | `frontend/src/components/Footer.tsx:L41` | `frontend/src/components` | JSDoc on the component above; named-imported by three pages | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `export default Header` | `frontend/src/components/Header.tsx:L66` | `frontend/src/components` | JSDoc on the component above; named-imported by three pages | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `export default ImageEditor` | `frontend/src/components/ImageEditor.tsx:L67` | `frontend/src/components` | JSDoc on the component above; no module imports it | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `export default Sidebar` | `frontend/src/components/Sidebar.tsx:L32` | `frontend/src/components` | JSDoc on the component above; named-imported by `Editor.tsx` | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `export default TableEditor` | `frontend/src/components/TableEditor.tsx:L75` | `frontend/src/components` | JSDoc on the component above; no module imports it | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `export default TextEditor` | `frontend/src/components/TextEditor.tsx:L78` | `frontend/src/components` | JSDoc on the component above; no page references it | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `export default Toolbar` | `frontend/src/components/Toolbar.tsx:L91` | `frontend/src/components` | JSDoc on the component above; named-imported by `Editor.tsx` | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `export default Editor` | `frontend/src/pages/Editor.tsx:L110` | `frontend/src/pages` | JSDoc on the component above; routed at `/editor` | `architecture-overview.md` | COVERED |
| `export default Home` | `frontend/src/pages/Home.tsx:L53` | `frontend/src/pages` | JSDoc on the component above; routed at `/` | `architecture-overview.md` | COVERED |
| `export default Settings` | `frontend/src/pages/Settings.tsx:L93` | `frontend/src/pages` | JSDoc on the component above; routed at `/settings` | `architecture-overview.md` | COVERED |
| `export default Templates` | `frontend/src/pages/Templates.tsx:L104` | `frontend/src/pages` | JSDoc on the component above; routed at `/templates` | `architecture-overview.md` | COVERED |
| `DocumentSchema` | `frontend/src/schema/document.ts:L23-L31` | `frontend/src/schema` | JSDoc; seven required fields, and `owner_id` contradicting the server | `data-model.md`, `troubleshooting.md` | COVERED |
| `DocumentVersionSchema` | `frontend/src/schema/document.ts:L39` | `frontend/src/schema` | JSDoc; names its actor `user_id`, matching the server | `data-model.md`, `troubleshooting.md` | COVERED |
| `TemplateSchema` | `frontend/src/schema/template.ts:L21` | `frontend/src/schema` | JSDoc; no server counterpart exists | `data-model.md`, `troubleshooting.md` | COVERED |
| `type Template` | `frontend/src/schema/template.ts:L31` | `frontend/src/schema` | JSDoc; the inferred type `document.ts` omits | `data-model.md`, `troubleshooting.md` | COVERED |
| `UserSchema` | `frontend/src/schema/user.ts:L19` | `frontend/src/schema` | JSDoc; omits the `updated_at` the Pydantic contract declares | `data-model.md`, `troubleshooting.md` | COVERED |
| `type User` | `frontend/src/schema/user.ts:L30` | `frontend/src/schema` | JSDoc; the inferred type `document.ts` omits | `data-model.md`, `troubleshooting.md` | COVERED |
| `getDocuments` | `frontend/src/services/api.ts:L69` | `frontend/src/services` | JSDoc with `@returns`; prefixes `/documents` against a router mounted at root | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `createDocument` | `frontend/src/services/api.ts:L81` | `frontend/src/services` | JSDoc with `@param` and `@returns`; same prefix mismatch | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `updateDocument` | `frontend/src/services/api.ts:L94` | `frontend/src/services` | JSDoc with `@param` and `@returns`; same prefix mismatch | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `login` | `frontend/src/services/auth.ts:L34` | `frontend/src/services` | JSDoc; posts to `/auth/login`, which no server route matches | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `logout` | `frontend/src/services/auth.ts:L52` | `frontend/src/services` | JSDoc; posts to `/auth/logout`, which no server route matches | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `getCurrentUser` | `frontend/src/services/auth.ts:L69` | `frontend/src/services` | JSDoc; unchecked cast to `User` | `data-model.md`, `troubleshooting.md` | COVERED |
| `export default CollaborationService` | `frontend/src/services/collaboration.ts:L107` | `frontend/src/services` | JSDoc on the class and all three methods; never instantiated | `integration-guide.md`, `troubleshooting.md` | COVERED |
| Six document actions: `setCurrentDocument`, `addRecentDocument`, `setLoading`, `setError`, `clearCurrentDocument`, `clearRecentDocuments` | `frontend/src/store/documentSlice.ts:L84-L91` | `frontend/src/store` | JSDoc per action with a usage example, as named primary entry points | `architecture-overview.md`, `data-model.md` | COVERED |
| `export default documentSlice.reducer` | `frontend/src/store/documentSlice.ts:L93` | `frontend/src/store` | JSDoc; the store imports a named `documentReducer` instead | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `type RootState` | `frontend/src/store/index.ts:L32` | `frontend/src/store` | JSDoc; derived from the store, so it lacks an `auth` key | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `type AppDispatch` | `frontend/src/store/index.ts:L34` | `frontend/src/store` | JSDoc; no typed dispatch hook exports it | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `export default store` | `frontend/src/store/index.ts:L36` | `frontend/src/store` | JSDoc; `App.tsx:L20` named-imports this default-only export | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| Four user actions: `setUser`, `clearUser`, `setLoading`, `setError` | `frontend/src/store/userSlice.ts:L75` | `frontend/src/store` | JSDoc per action with a usage example, as named primary entry points | `architecture-overview.md`, `data-model.md` | COVERED |
| `export default userSlice.reducer` | `frontend/src/store/userSlice.ts:L76` | `frontend/src/store` | JSDoc; the store imports a named `userReducer` instead | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `serializeDocument` | `frontend/src/utils/documentUtils.ts:L29` | `frontend/src/utils` | JSDoc with `@param` and `@returns`; validates against the wrong schema | `data-model.md`, `troubleshooting.md` | COVERED |
| `deserializeDocument` | `frontend/src/utils/documentUtils.ts:L49` | `frontend/src/utils` | JSDoc with `@param` and `@returns`; same category error | `data-model.md`, `troubleshooting.md` | COVERED |
| `applyInlineStyle` | `frontend/src/utils/formatting.ts:L24` | `frontend/src/utils` | JSDoc making the two-argument contract explicit | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `applyBlockStyle` | `frontend/src/utils/formatting.ts:L45` | `frontend/src/utils` | JSDoc making the two-argument contract explicit | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `validateEmail` | `frontend/src/utils/validation.ts:L21` | `frontend/src/utils` | JSDoc; returns only `.success`, discarding its own message | `data-model.md`, `troubleshooting.md` | COVERED |
| `validatePassword` | `frontend/src/utils/validation.ts:L36` | `frontend/src/utils` | JSDoc; the password policy spelled out | `data-model.md`, `troubleshooting.md` | COVERED |

### Terraform files (3)

The three HashiCorp Configuration Language (HCL) files are the single configuration-file exception that receives inline comments. Decision row 5 records the boundary.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `main.tf` | `infrastructure/terraform/main.tf:L1-L99` | `infrastructure/terraform` | Short `#` comments on non-obvious blocks; three absent module sources | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `variables.tf` | `infrastructure/terraform/variables.tf:L1-L95` | `infrastructure/terraform` | Short `#` comments marking each variable consumed or dead | `deployment-guide.md`, `onboarding.md` | COVERED |
| `outputs.tf` | `infrastructure/terraform/outputs.tf:L1-L87` | `infrastructure/terraform` | Short `#` comments naming the AWS-outputs oddity and the two password leaks | `deployment-guide.md`, `troubleshooting.md` | COVERED |

### Test modules (3)

The only README describing a directory whose files receive no inline documentation. [backend/tests/README.md](../backend/tests/README.md) states that exclusion explicitly so a later pass does not add docstrings here.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `tests/test_api.py` | `backend/tests/test_api.py:L1-L77` | `backend/tests` | None by design (AAP R7) | `troubleshooting.md`, `onboarding.md` | COVERED |
| `tests/test_db.py` | `backend/tests/test_db.py:L1-L58` | `backend/tests` | None by design (AAP R7) | `troubleshooting.md`, `onboarding.md` | COVERED |
| `tests/test_services.py` | `backend/tests/test_services.py:L1-L80` | `backend/tests` | None by design (AAP R7) | `troubleshooting.md`, `onboarding.md` | COVERED |

### Container artifacts (3)

Two Dockerfiles and one Compose file, documented from outside by [infrastructure/docker/README.md](../infrastructure/docker/README.md).

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `backend.Dockerfile` | `infrastructure/docker/backend.Dockerfile:L1-L27` | `infrastructure/docker` | None by design (AAP R7) | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `frontend.Dockerfile` | `infrastructure/docker/frontend.Dockerfile:L1-L32` | `infrastructure/docker` | None by design (AAP R7) | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `docker-compose.yml` | `infrastructure/docker/docker-compose.yml:L1-L46` | `infrastructure/docker` | None by design (AAP R7) | `deployment-guide.md`, `onboarding.md` | COVERED |

### Workflow files (2)

Continuous integration and continuous deployment definitions, documented from outside by [.github/workflows/README.md](../.github/workflows/README.md).

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `ci.yml` | `.github/workflows/ci.yml:L1-L23` | `.github/workflows` | None by design (AAP R7) | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `cd.yml` | `.github/workflows/cd.yml:L1-L20` | `.github/workflows` | None by design (AAP R7) | `deployment-guide.md`, `troubleshooting.md` | COVERED |

### Shell scripts (2)

Both scripts are documented from outside by [scripts/README.md](../scripts/README.md), which marks the exact failing command in each.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `deploy.sh` | `scripts/deploy.sh:L1-L47` | `scripts` | None by design (AAP R7) | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `setup_dev_environment.sh` | `scripts/setup_dev_environment.sh:L1-L56` | `scripts` | None by design (AAP R7) | `onboarding.md`, `troubleshooting.md` | COVERED |

### Frontend manifests (2)

Configuration files with no logic. [frontend/src/README.md](../frontend/src/README.md) documents both, including the five path aliases that omit the prefix nearly every module uses.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `package.json` | `frontend/package.json:L1-L57` | `frontend/src` | None by design (AAP R7) | `onboarding.md`, `troubleshooting.md` | COVERED |
| `tsconfig.json` | `frontend/tsconfig.json:L1-L30` | `frontend/src` | None by design (AAP R7) | `onboarding.md`, `troubleshooting.md` | COVERED |

### `HUMAN ASSISTANCE NEEDED` markers (33)

The repository-wide total. All 33 survive verbatim and in place, and each is cited in a Known Limitations section and again in the complete register in [troubleshooting.md](troubleshooting.md).

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `HUMAN ASSISTANCE NEEDED` at `main.py:L38`, flagging the startup block that awaits an absent `init_db` | `backend/app/main.py:L38-L39` | `backend/app` | Preserved verbatim; referenced by the surrounding documentation | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `users.py:L54`, flagging an assumed `UserService` class that does not exist | `backend/app/api/users.py:L54-L56` | `backend/app/api` | Preserved verbatim; referenced by the surrounding documentation | `troubleshooting.md`, `architecture-overview.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `security.py:L86`, flagging the token dependency's undefined `User` and `UserService` names | `backend/app/core/security.py:L86-L89` | `backend/app/core` | Preserved verbatim; referenced by the surrounding documentation | `troubleshooting.md`, `integration-guide.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `collaboration_service.py:L42`, flagging `connect`, at a stated confidence of 0.6 | `backend/app/services/collaboration_service.py:L42-L43` | `backend/app/services` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `collaboration_service.py:L131`, flagging `broadcast_change`, at a stated confidence of 0.7 | `backend/app/services/collaboration_service.py:L131-L132` | `backend/app/services` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `document_service.py:L114`, flagging `update_document` as needing error handling and validation | `backend/app/services/document_service.py:L114-L115` | `backend/app/services` | Preserved verbatim; referenced by the surrounding documentation | `data-model.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `export_service.py:L38`, flagging both export methods as low confidence | `backend/app/services/export_service.py:L38-L39` | `backend/app/services` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `background_tasks.py:L49`, flagging the export task as unready for production | `backend/app/tasks/background_tasks.py:L49-L50` | `backend/app/tasks` | Preserved verbatim; referenced by the surrounding documentation | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `background_tasks.py:L91`, flagging the retention sweep as unready and unoptimized | `backend/app/tasks/background_tasks.py:L91-L92` | `backend/app/tasks` | Preserved verbatim; referenced by the surrounding documentation | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `DocumentCanvas.tsx:L20`, flagging the whole component, below a confidence of 0.8 | `frontend/src/components/DocumentCanvas.tsx:L20-L21` | `frontend/src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `ImageEditor.tsx:L30`, flagging the atomic-block insert helper | `frontend/src/components/ImageEditor.tsx:L30-L31` | `frontend/src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `ImageEditor.tsx:L59`, flagging the unwritten image-editing interface | `frontend/src/components/ImageEditor.tsx:L59-L60` | `frontend/src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `TableEditor.tsx:L29`, flagging the table insert helper, at a stated confidence of 0.6 | `frontend/src/components/TableEditor.tsx:L29-L30` | `frontend/src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `TextEditor.tsx:L26`, flagging the key-command handler | `frontend/src/components/TextEditor.tsx:L26-L27` | `frontend/src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `Toolbar.tsx:L19`, flagging the whole toolbar as needing error handling | `frontend/src/components/Toolbar.tsx:L19-L21` | `frontend/src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `Editor.tsx:L20`, flagging the editor page as unready for production | `frontend/src/pages/Editor.tsx:L20-L21` | `frontend/src/pages` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `Settings.tsx:L18`, flagging the settings page as needing refinement | `frontend/src/pages/Settings.tsx:L18-L20` | `frontend/src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `Templates.tsx:L55`, flagging absent error handling, paired with the TODO on the next line | `frontend/src/pages/Templates.tsx:L55-L56` | `frontend/src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `Templates.tsx:L72`, flagging absent navigation, paired with the TODO on the next line | `frontend/src/pages/Templates.tsx:L72-L73` | `frontend/src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `collaboration.ts:L48`, flagging the empty listener body, with an example listener commented out | `frontend/src/services/collaboration.ts:L48-L51` | `frontend/src/services` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `collaboration.ts:L54`, flagging `joinDocument` | `frontend/src/services/collaboration.ts:L54-L55` | `frontend/src/services` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `collaboration.ts:L81`, flagging `sendChanges` | `frontend/src/services/collaboration.ts:L81-L82` | `frontend/src/services` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `documentSlice.ts:L95`, flagging absent thunks for asynchronous document operations | `frontend/src/store/documentSlice.ts:L95-L98` | `frontend/src/store` | Preserved verbatim; referenced by the surrounding documentation | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `userSlice.ts:L78`, flagging absent error types and the absent `updateUser` action | `frontend/src/store/userSlice.ts:L78-L81` | `frontend/src/store` | Preserved verbatim; referenced by the surrounding documentation | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `documentUtils.ts:L17`, flagging both serialization helpers and the schema validation call | `frontend/src/utils/documentUtils.ts:L17-L19` | `frontend/src/utils` | Preserved verbatim; referenced by the surrounding documentation | `data-model.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `main.tf:L94`, flagging the subnet range and the firewall rule set | `infrastructure/terraform/main.tf:L94-L97` | `infrastructure/terraform` | Preserved verbatim; referenced by the surrounding documentation | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `outputs.tf:L58`, flagging outputs that may not match any declared resource | `infrastructure/terraform/outputs.tf:L58-L60` | `infrastructure/terraform` | Preserved verbatim; referenced by the surrounding documentation | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `test_api.py:L13`, flagging the unconfigured test database connection | `backend/tests/test_api.py:L13` | `backend/tests` | Preserved verbatim; file receives no inline documentation (AAP R7) | `troubleshooting.md`, `onboarding.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `test_api.py:L77`, flagging absent endpoint and edge-case coverage | `backend/tests/test_api.py:L77` | `backend/tests` | Preserved verbatim; file receives no inline documentation (AAP R7) | `troubleshooting.md`, `onboarding.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `test_db.py:L56`, flagging absent update, delete and error-handling tests | `backend/tests/test_db.py:L56-L58` | `backend/tests` | Preserved verbatim; file receives no inline documentation (AAP R7) | `troubleshooting.md`, `onboarding.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `backend.Dockerfile:L22`, flagging the Python version and the absent requirements file | `infrastructure/docker/backend.Dockerfile:L22-L26` | `infrastructure/docker` | Preserved verbatim; file receives no inline documentation (AAP R7) | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `deploy.sh:L37`, flagging the unwritten post-deployment checks | `scripts/deploy.sh:L37-L38` | `scripts` | Preserved verbatim; file receives no inline documentation (AAP R7) | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `HUMAN ASSISTANCE NEEDED` at `setup_dev_environment.sh:L41`, flagging the environment file, paired with the TODO on the next line | `scripts/setup_dev_environment.sh:L41` | `scripts` | Preserved verbatim; file receives no inline documentation (AAP R7) | `onboarding.md`, `troubleshooting.md` | COVERED |

### `TODO` markers (16)

The repository-wide total. All 16 survive verbatim. Two sit directly beneath a marker, in `Templates.tsx` and `setup_dev_environment.sh`, and the documentation records both as pairs.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `TODO` at `main.py:L49`: implement database migration logic | `backend/app/main.py:L49` | `backend/app` | Preserved verbatim; referenced by the surrounding documentation | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `TODO` at `main.py:L68`: add additional shutdown cleanup | `backend/app/main.py:L68` | `backend/app` | Preserved verbatim; referenced by the surrounding documentation | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `TODO` at `export_service.py:L57`: implement PDF conversion logic | `backend/app/services/export_service.py:L57` | `backend/app/services` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `TODO` at `export_service.py:L62`: replace the placeholder PDF content | `backend/app/services/export_service.py:L62` | `backend/app/services` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `TODO` at `export_service.py:L89`: implement DOCX conversion logic | `backend/app/services/export_service.py:L89` | `backend/app/services` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `TODO` at `export_service.py:L94`: replace the placeholder DOCX content | `backend/app/services/export_service.py:L94` | `backend/app/services` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `TODO` at `Toolbar.tsx:L67`: implement the insert action | `frontend/src/components/Toolbar.tsx:L67` | `frontend/src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture-overview.md`, `troubleshooting.md` | COVERED |
| `TODO` at `Editor.tsx:L48`: add proper error handling on document load | `frontend/src/pages/Editor.tsx:L48` | `frontend/src/pages` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `TODO` at `Editor.tsx:L78`: add error handling and user notification on auto-save | `frontend/src/pages/Editor.tsx:L78` | `frontend/src/pages` | Preserved verbatim; referenced by the surrounding documentation | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `TODO` at `Settings.tsx:L52`: add a success message on save | `frontend/src/pages/Settings.tsx:L52` | `frontend/src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model.md`, `troubleshooting.md` | COVERED |
| `TODO` at `Settings.tsx:L55`: add error handling and user feedback | `frontend/src/pages/Settings.tsx:L55` | `frontend/src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model.md`, `troubleshooting.md` | COVERED |
| `TODO` at `Templates.tsx:L56`: implement error handling and user feedback | `frontend/src/pages/Templates.tsx:L56` | `frontend/src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model.md`, `troubleshooting.md` | COVERED |
| `TODO` at `Templates.tsx:L73`: implement navigation after a template is chosen | `frontend/src/pages/Templates.tsx:L73` | `frontend/src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model.md`, `troubleshooting.md` | COVERED |
| `TODO` at `documentUtils.ts:L33`: implement proper schema validation on serialize | `frontend/src/utils/documentUtils.ts:L33` | `frontend/src/utils` | Preserved verbatim; referenced by the surrounding documentation | `data-model.md`, `troubleshooting.md` | COVERED |
| `TODO` at `documentUtils.ts:L58`: implement proper schema validation on deserialize | `frontend/src/utils/documentUtils.ts:L58` | `frontend/src/utils` | Preserved verbatim; referenced by the surrounding documentation | `data-model.md`, `troubleshooting.md` | COVERED |
| `TODO` at `setup_dev_environment.sh:L42`: populate the environment file for production | `scripts/setup_dev_environment.sh:L42` | `scripts` | Preserved verbatim; file receives no inline documentation (AAP R7) | `onboarding.md`, `troubleshooting.md` | COVERED |

### HTTP operations (14)

Fourteen operations across four routers. Twelve sit behind the token dependency and two are public. Every path in the templates router duplicates a path in the documents router, and `backend/app/main.py:L80-L83` mounts both without a prefix, so Starlette matches the documents router first.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `POST /token` | `backend/app/api/auth.py:L65` | `backend/app/api` | Handler docstring at `:L66`; one of the two public operations | `integration-guide.md`, `onboarding.md` | COVERED |
| `POST /register` | `backend/app/api/auth.py:L102` | `backend/app/api` | Handler docstring at `:L103`; the second public operation | `integration-guide.md`, `onboarding.md` | COVERED |
| `POST /` (documents) | `backend/app/api/documents.py:L24` | `backend/app/api` | Handler docstring at `:L25`; protected, and collides with the template create | `data-model.md`, `troubleshooting.md` | COVERED |
| `GET /` (documents) | `backend/app/api/documents.py:L49` | `backend/app/api` | Handler docstring at `:L50`; protected, and calls an absent service method | `data-model.md`, `troubleshooting.md` | COVERED |
| `GET /{document_id}` | `backend/app/api/documents.py:L68` | `backend/app/api` | Handler docstring at `:L69`; protected, and shadows the template read | `data-model.md`, `troubleshooting.md` | COVERED |
| `PUT /{document_id}` | `backend/app/api/documents.py:L96` | `backend/app/api` | Handler docstring at `:L97`; protected, and shadows the template update | `data-model.md`, `troubleshooting.md` | COVERED |
| `DELETE /{document_id}` | `backend/app/api/documents.py:L126` | `backend/app/api` | Handler docstring at `:L127`; protected, and shadows the template delete | `data-model.md`, `troubleshooting.md` | COVERED |
| `POST /` (templates) | `backend/app/api/templates.py:L24` | `backend/app/api` | Handler docstring at `:L25`; protected, and never reached | `data-model.md`, `troubleshooting.md` | COVERED |
| `GET /` (templates) | `backend/app/api/templates.py:L42` | `backend/app/api` | Handler docstring at `:L43`; protected, and never reached | `data-model.md`, `troubleshooting.md` | COVERED |
| `GET /{template_id}` | `backend/app/api/templates.py:L59` | `backend/app/api` | Handler docstring at `:L60`; protected, and never reached | `data-model.md`, `troubleshooting.md` | COVERED |
| `PUT /{template_id}` | `backend/app/api/templates.py:L86` | `backend/app/api` | Handler docstring at `:L87`; protected, and never reached | `data-model.md`, `troubleshooting.md` | COVERED |
| `DELETE /{template_id}` | `backend/app/api/templates.py:L112` | `backend/app/api` | Handler docstring at `:L113`; protected, and never reached | `data-model.md`, `troubleshooting.md` | COVERED |
| `GET /me` | `backend/app/api/users.py:L19` | `backend/app/api` | Handler docstring at `:L20`; protected, and synchronous | `data-model.md`, `troubleshooting.md` | COVERED |
| `PUT /me` | `backend/app/api/users.py:L32` | `backend/app/api` | Handler docstring at `:L33`; protected, synchronous, and persists nothing | `data-model.md`, `troubleshooting.md` | COVERED |

### Settings fields (15)

Nine fields are declared on the `Settings` model, and six more are read by other modules and declared nowhere. Every row is marked DECLARED or READ BUT NEVER DECLARED.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `PROJECT_NAME`, DECLARED | `backend/app/core/config.py:L40` | `backend/app/core` | Documented in the `Settings` class docstring as an `Attributes:` entry | `deployment-guide.md`, `onboarding.md` | COVERED |
| `API_V1_STR`, DECLARED and never read | `backend/app/core/config.py:L41` | `backend/app/core` | Documented as declared with no reader anywhere in the tree | `deployment-guide.md`, `onboarding.md` | COVERED |
| `SECRET_KEY`, DECLARED | `backend/app/core/config.py:L42` | `backend/app/core` | Documented; read at `backend/app/core/security.py:L54` and in the auth router | `integration-guide.md`, `onboarding.md` | COVERED |
| `ACCESS_TOKEN_EXPIRE_MINUTES`, DECLARED | `backend/app/core/config.py:L43` | `backend/app/core` | Documented; read at `backend/app/core/security.py:L52` | `integration-guide.md`, `onboarding.md` | COVERED |
| `ALGORITHM`, DECLARED | `backend/app/core/config.py:L44` | `backend/app/core` | Documented; carries no validator, so any string satisfies it | `integration-guide.md`, `onboarding.md` | COVERED |
| `GOOGLE_CLOUD_PROJECT`, DECLARED | `backend/app/core/config.py:L45` | `backend/app/core` | Documented; read at `backend/app/db/firestore.py:L20` | `integration-guide.md`, `deployment-guide.md` | COVERED |
| `GOOGLE_APPLICATION_CREDENTIALS`, DECLARED | `backend/app/core/config.py:L46` | `backend/app/core` | Documented; the credential model relies on it | `integration-guide.md`, `deployment-guide.md` | COVERED |
| `DATABASE_URL`, DECLARED | `backend/app/core/config.py:L47` | `backend/app/core` | Documented; read at `backend/app/db/sql.py:L16` at import time | `deployment-guide.md`, `onboarding.md` | COVERED |
| `REDIS_URL`, DECLARED | `backend/app/core/config.py:L48` | `backend/app/core` | Documented; read at `backend/app/tasks/background_tasks.py:L22` | `deployment-guide.md`, `integration-guide.md` | COVERED |
| `ALLOWED_ORIGINS`, READ BUT NEVER DECLARED | `backend/app/main.py:L73` | `backend/app` | Documented in the module docstring as absent from the `Settings` model | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `PROJECT_ID`, READ BUT NEVER DECLARED | `backend/app/services/collaboration_service.py:L69` | `backend/app/services` | Documented; also read at `:L124` and `:L149` | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `STORAGE_BUCKET_NAME`, READ BUT NEVER DECLARED | `backend/app/services/export_service.py:L60` | `backend/app/services` | Documented; also read at `:L92` | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `SIGNED_URL_EXPIRATION`, READ BUT NEVER DECLARED | `backend/app/services/export_service.py:L68` | `backend/app/services` | Documented; also read at `:L100` | `integration-guide.md`, `troubleshooting.md` | COVERED |
| `EXPORT_BUCKET_NAME`, READ BUT NEVER DECLARED | `backend/app/tasks/background_tasks.py:L62` | `backend/app/tasks` | Documented in the task docstring as absent from the model | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `DOCUMENT_BUCKET_NAME`, READ BUT NEVER DECLARED | `backend/app/tasks/background_tasks.py:L107` | `backend/app/tasks` | Documented in the task docstring as absent from the model | `deployment-guide.md`, `troubleshooting.md` | COVERED |

### Terraform variables (13)

Thirteen declared variables. Only `project_id` and `region` reach a resource, leaving eleven dead. No variable carries a validation block.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `project_id`, CONSUMED | `infrastructure/terraform/variables.tf:L7` | `infrastructure/terraform` | `#` comment marking it consumed; read at `main.tf:L10` | `deployment-guide.md`, `onboarding.md` | COVERED |
| `region`, CONSUMED | `infrastructure/terraform/variables.tf:L14` | `infrastructure/terraform` | `#` comment marking it consumed; read at `main.tf:L11` | `deployment-guide.md`, `onboarding.md` | COVERED |
| `zone`, DEAD | `infrastructure/terraform/variables.tf:L21` | `infrastructure/terraform` | `#` comment marking it declared and unreferenced | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `compute_instance_type`, DEAD | `infrastructure/terraform/variables.tf:L29` | `infrastructure/terraform` | `#` comment marking it declared and unreferenced | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `storage_class`, DEAD | `infrastructure/terraform/variables.tf:L37` | `infrastructure/terraform` | `#` comment; the bucket resource sets no storage class | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `database_tier`, DEAD | `infrastructure/terraform/variables.tf:L44` | `infrastructure/terraform` | `#` comment marking it declared and unreferenced | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `environment`, DEAD | `infrastructure/terraform/variables.tf:L53` | `infrastructure/terraform` | `#` comment; no validation block, so any string passes | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `dev_instance_count`, DEAD | `infrastructure/terraform/variables.tf:L61` | `infrastructure/terraform` | `#` comment marking it declared and unreferenced | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `staging_instance_count`, DEAD | `infrastructure/terraform/variables.tf:L67` | `infrastructure/terraform` | `#` comment marking it declared and unreferenced | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `prod_instance_count`, DEAD | `infrastructure/terraform/variables.tf:L73` | `infrastructure/terraform` | `#` comment marking it declared and unreferenced | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `dev_storage_size`, DEAD | `infrastructure/terraform/variables.tf:L79` | `infrastructure/terraform` | `#` comment marking it declared and unreferenced | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `staging_storage_size`, DEAD | `infrastructure/terraform/variables.tf:L85` | `infrastructure/terraform` | `#` comment marking it declared and unreferenced | `deployment-guide.md`, `troubleshooting.md` | COVERED |
| `prod_storage_size`, DEAD | `infrastructure/terraform/variables.tf:L91` | `infrastructure/terraform` | `#` comment marking it declared and unreferenced | `deployment-guide.md`, `troubleshooting.md` | COVERED |

### Matrix totals

| Group | Composition | Rows |
| --- | --- | --- |
| File rows | 15 backend modules, 26 frontend modules, 3 Terraform files, 3 test modules, 3 container artifacts, 2 workflows, 2 shell scripts, 2 manifests | 56 |
| Construct rows | 15 Python classes, 43 Python functions and methods, 13 React components, 39 export statements | 110 |
| Marker rows | 33 `HUMAN ASSISTANCE NEEDED`, 16 `TODO` | 49 |
| Contract rows | 14 HTTP operations, 15 settings fields, 13 Terraform variables | 42 |
| **Total** | All four groups combined | **257** |

Every one of the 257 Status cells reads COVERED. Nineteen rows describe files the requirements
exclude from inline documentation. Twelve of those are file rows carrying an explicit
`None by design (AAP R7)` cell, and seven are marker rows recording a marker preserved in a file
that was never edited. All nineteen reach COVERED through their README.

## The reverse matrix

Running the mapping backwards exposes two failure modes a single-direction matrix hides: an
artifact that documents nothing, and a construct documented nowhere.

One row per new artifact, 28 in total. The Constructs covered column counts the matrix rows
naming that artifact, so the figures are derived from the matrix above rather than asserted
separately. The nineteen README counts sum to 257, which proves no row lacks an owner. The six
`docs/` counts overlap by design, because most constructs appear in two repository-level
documents.

### The 19 module READMEs

| Artifact | What it documents | Constructs covered | Gaps |
| --- | --- | --- | --- |
| [backend/app/README.md](../backend/app/README.md) | The composition root: the application object, both lifecycle handlers, the four router mounts and the undeclared CORS origin setting | 7 matrix rows | None |
| [backend/app/api/README.md](../backend/app/api/README.md) | Four routers, all 14 handlers and all 14 HTTP operations, plus the documents-over-templates path collision | 34 matrix rows | None |
| [backend/app/core/README.md](../backend/app/core/README.md) | The `Settings` model with all nine declared fields, both `Config` inner classes' parent, and the four security primitives | 19 matrix rows | None |
| [backend/app/db/README.md](../backend/app/db/README.md) | The Firestore adapter's four helpers and the declared but unused relational path, including the one generator | 7 matrix rows | None |
| [backend/app/schema/README.md](../backend/app/schema/README.md) | All nine Pydantic model classes plus the two inner `Config` classes, and the ownership split inside one file | 12 matrix rows | None |
| [backend/app/services/README.md](../backend/app/services/README.md) | Three service classes and their thirteen function definitions, twelve methods plus the nested Pub/Sub callback at `backend/app/services/collaboration_service.py:L80` | 30 matrix rows | None |
| [backend/app/tasks/README.md](../backend/app/tasks/README.md) | The Celery application, three tasks, the invalid periodic decorator and two undeclared bucket settings | 8 matrix rows | None |
| [backend/tests/README.md](../backend/tests/README.md) | Three test modules and their three markers, from outside | 6 matrix rows | None. Inline comments excluded by AAP R7, so coverage is README-only |
| [frontend/src/README.md](../frontend/src/README.md) | The bootstrap path, the routed shell and both frontend manifests | 6 matrix rows | None. Inline comments excluded by AAP R7, so coverage is README-only |
| [frontend/src/components/README.md](../frontend/src/components/README.md) | Eight component modules, eight components, their export forms and eleven markers | 31 matrix rows | None |
| [frontend/src/pages/README.md](../frontend/src/pages/README.md) | Four page modules, four page components, the five-second debounce and eleven markers | 22 matrix rows | None |
| [frontend/src/schema/README.md](../frontend/src/schema/README.md) | Three Zod modules and six exported schema values and types, including the absent inferred type | 9 matrix rows | None |
| [frontend/src/services/README.md](../frontend/src/services/README.md) | Three client modules, seven exported functions, the collaboration class and three markers | 13 matrix rows | None |
| [frontend/src/store/README.md](../frontend/src/store/README.md) | Three store modules, ten action creators, two reducers, two types and the store default export | 12 matrix rows | None |
| [frontend/src/utils/README.md](../frontend/src/utils/README.md) | Three utility modules and six exported functions, plus the one defect-free module | 12 matrix rows | None |
| [infrastructure/terraform/README.md](../infrastructure/terraform/README.md) | Three HCL files, thirteen variables marked consumed or dead, and two markers | 18 matrix rows | None |
| [infrastructure/docker/README.md](../infrastructure/docker/README.md) | Two Dockerfiles, one Compose topology and one marker, all from outside | 4 matrix rows | None. Inline comments excluded by AAP R7, so coverage is README-only |
| [.github/workflows/README.md](../.github/workflows/README.md) | Both pipeline definitions, from outside, with the exact failing step marked | 2 matrix rows | None. Inline comments excluded by AAP R7, so coverage is README-only |
| [scripts/README.md](../scripts/README.md) | Both shell scripts, from outside, plus two markers and one TODO | 5 matrix rows | None. Inline comments excluded by AAP R7, so coverage is README-only |

The nineteen counts above sum to 257, matching the matrix total exactly.

### The 9 documents under `docs/`

| Artifact | What it documents | Constructs covered | Gaps |
| --- | --- | --- | --- |
| [README.md](README.md) | The index: every sibling document and all 19 module READMEs, plus the five shared conventions | None, by design | None. An index carries navigation, not construct documentation |
| [architecture-overview.md](architecture-overview.md) | The six top-level areas, the four tiers, the five boundaries and the broken edges between them | 57 matrix rows | None |
| [data-model.md](data-model.md) | Dual persistence, four entity families, the Pydantic and Zod contracts and the four-way ownership drift | 89 matrix rows | None |
| [integration-guide.md](integration-guide.md) | Firestore, Cloud Storage signed URLs, Pub/Sub and the absent Redis broker, each labelled by reachability | 71 matrix rows | None |
| [deployment-guide.md](deployment-guide.md) | Terraform, containers, both pipelines, the deploy script and every reason a deploy fails | 52 matrix rows | None |
| [troubleshooting.md](troubleshooting.md) | The full defect register across nine gap classes, the root README inaccuracies, and all 49 markers | 209 matrix rows | None |
| [onboarding.md](onboarding.md) | Clean-machine setup, domain context, the common pitfalls, how to extend, and the ordered next tasks | 30 matrix rows | None |
| decision-log.md (this file) | Fifteen decisions, ten deviations and the bidirectional matrix | All 257 matrix rows | None |
| prose-validation.md | Rule 3 verdicts and principle scorecards for all 28 new artifacts | None, by design | None. Validates prose quality, not construct coverage |

Two artifacts cover no construct, and both do so deliberately. [README.md](README.md) navigates,
and `prose-validation.md` judges writing quality. Naming them here rather than leaving them out
is the point of a reverse matrix: a reader can see that the two zero counts are chosen, not
accidental.

### Related documentation

| Document | Why you would open it from here |
| --- | --- |
| [README.md](README.md) | The index, and the shared conventions this file follows |
| [onboarding.md](onboarding.md) | The destination for conflicts C1 and C3, recorded in decision rows 1 and 3 |
| [troubleshooting.md](troubleshooting.md) | The full evidence behind every defect this log names in passing |
| [data-model.md](data-model.md) | The four ownership positions decision row 7 declines to rank |
| [architecture-overview.md](architecture-overview.md) | Where each documented construct sits in the four tiers |
| [integration-guide.md](integration-guide.md) | Reachability labels for the external services named above |
| [deployment-guide.md](deployment-guide.md) | Why the infrastructure decisions in rows 10 and 11 carry no pipeline cost |
| [../README.md](../README.md) | The root README, reference only, and the subject of decision row 1 |
| [Technical Specifications](<../documentation/Technical Specifications.md>) | Declared intent, cited by heading name and line number throughout |
