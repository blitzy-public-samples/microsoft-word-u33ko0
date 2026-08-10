# Decision Log and Traceability Matrix

Twenty-five choices shaped the documentation layer over this repository, and a competent engineer
could reasonably have made every one of them differently. The decision table below records each
choice with its alternatives, its reasoning and its risk. The traceability matrix that follows
maps all 255 documented constructs to the artifacts that document them, which is how this layer
proves its own coverage.

## How to read this log

### Rationale lives here and nowhere else

Rule 1, Explainability, makes this file the single source of truth for why decisions were made.
No other artifact here argues for a choice. Docstrings, JSDoc blocks, the 19 module READMEs and
the eight sibling documents under `docs/` all describe behaviour instead. They state what a
construct does, what parameters it takes, what it returns, what it raises, what side effects it
causes, and which of its imports cannot resolve. When you want to know **why** a choice was made,
come here.

Two sentence shapes divide the two kinds of writing. A sentence stating what the code does, or
what this documentation set does, belongs wherever a reader needs it. A sentence defending that
against an alternative belongs in the decision table below, and every other artifact carries a
factual cross-reference instead. Four such defences sat outside this file before the current
pass, in [data-model.md](data-model.md), [troubleshooting.md](troubleshooting.md),
[onboarding.md](onboarding.md) and `prose-validation.md`. They are now rows 21 through 24.

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
| [The decision table](#the-decision-table) | Twenty-five choices, their alternatives, their reasons and their risks |
| [Deviations from a literal reading](#deviations-from-a-literal-reading-of-the-requirements) | Thirteen deviations: five rule conflicts, seven corrections, one re-anchoring |
| [The traceability matrix](#the-source-construct-to-documentation-artifact-traceability-matrix) | 255 rows, source construct to documenting artifact |
| [The reverse matrix](#the-reverse-matrix) | 28 rows, one per new artifact, running the mapping backwards |

Two vocabulary notes. **AAP** expands to Agent Action Plan, the plan that governs this
engagement. A **marker** is a `HUMAN ASSISTANCE NEEDED` comment, written by the original authors
to flag code they were not confident in.

## The decision table

Twenty-five decisions sit below. Each one is a choice a competent engineer could reasonably have made
differently, which is the test Rule 1 sets. Entries 1 through 4 and entry 20 resolve collisions
between the user-specified rules and the requirements, and the next section traces every collision by
identifier. Entries 16 through 18 govern how this documentation counts, scores and sites its own
evidence, and entry 19 governs the shape of the defect register itself. Entries 21 through 24 govern
four artifacts individually: the dependency register, the data model reference, the prose record and
the onboarding guide. Entry 25 governs how README length was allocated across the nineteen modules.

| What was decided | What alternatives existed | Why this choice was made | What risks it carries |
| --- | --- | --- | --- |
| **1. The root README stays reference material.** [../README.md](../README.md) receives no edit. A new [onboarding.md](onboarding.md) carries Rule 2's substance. | Edit the root README to correct its six false statements and add a link to `docs/`. | The requirements name that one file as reference rather than a rewrite target, and the instruction about a single named file is the more specific directive. Rule 2's goal, a developer reaching a modifiable application without asking questions, is fully reachable in a new document. | Nothing links into `docs/` from the repository's front door. A reader arriving at the root sees an inaccurate README, follows `pip install -r requirements.txt` against a file that does not exist, and never finds this documentation set. |
| **2. Docstrings describe, only this log justifies.** Inline documentation carries purpose, parameters, returns, raises, side effects and factual statements about broken state. Design rationale lives here. | Let each docstring explain why its design choice was made, next to the code it concerns. | Rule 1 names this log the single source of truth for why decisions were made. Describing what a function does is a different act from justifying a decision, and only the second is rationale. | A reader of a docstring must open a second file to learn why a construct exists in that shape. Rationale and code drift apart when one changes without the other. |
| **3. Onboarding documents the honest path.** [onboarding.md](onboarding.md) names the steps that work, the exact line where a run stops, and the remediation each blocker needs. | Repair the absent `settings` singleton and the unresolved module paths so a clean machine reaches a running application, then write the guide against a working system. | Repair is a logic change, and the minimal change clause forbids one. A guide promising a running application would be false at its first command, because `import app.main` fails at `auth.py:L20`. | A reader expecting working setup instructions gets a blocker register instead. Following the guide end to end leaves the application still not running. |
| **4. Prose verdicts go in their own file.** `prose-validation.md` holds Rule 3's verdicts and principle scorecards for all 29 pieces of generated text. | Place each verdict inside the document it judges, or record no verdicts at all. | Rule 3 requires a verdict and a scorecard for every piece of generated text, and no enumerated deliverable can hold them. Verdicts inside each README would push several past their stated size band. | A contributor editing a README will not see its verdict unless they open a second file, so a scorecard can describe prose that no longer exists. |
| **5. Inline comments stop at the two source globs plus Terraform.** [.github/workflows/README.md](../.github/workflows/README.md) and [scripts/README.md](../scripts/README.md) describe their files from outside. The three `.tf` files are the single configuration exception that receives `#` comments. | Read the phrase naming one exception loosely, and comment the two workflow files and two shell scripts as well. | The requirements name Terraform `.tf` files as the one exception to the two in-scope source globs. The narrower reading cannot over-reach the stated scope, and the wider one can. | Four files carry no inline explanation. A contributor editing `ci.yml` or `deploy.sh` sees no warning in the file itself and must open the neighbouring README to learn that both are broken. |
| **6. A `docs/` index was created although the requirements do not list one.** [README.md](README.md) indexes the eight sibling documents and all 19 module READMEs. | Leave the eight siblings and the 19 module READMEs with no entry point. | Eight sibling documents with no hub are not discoverable, and the root README sits out of scope, so no other file can index them. The requirements also state that cross-linking must be handled inside the `docs/` files. | One more file to keep current. A stale index misdirects a reader worse than no index would, because a reader trusts an index. |
| **7. All four ownership positions documented, none named canonical.** [data-model.md](data-model.md) presents the four code sites and three specification sites together and picks no winner. | Designate `owner_id` or `user_id` as correct and describe the other positions as wrong. | Naming a winner implies the code should change, and the minimal change clause forbids a rename. The four positions are a verifiable fact; which one is correct is a decision the maintainers own. | A reader wanting one answer gets four positions and must decide alone. Authorization depends on the field, and `owner_id` is optional with a default at `document.py:L28`, so a document can validate without the field the ownership check reads. |
| **8. Google style for Python docstrings.** `Args:`, `Returns:` and `Raises:` sections, with `Yields:` for the one generator at `sql.py:L21`. | NumPy style with underlined section headers, or reStructuredText field lists such as `:param x:`. | The user-supplied Python template is Google style, so the shape was already settled before authoring began. No competing convention existed in the repository to preserve, because the source tree carried no docstring at all. | A maintainer who later adopts Sphinx with reStructuredText would have to convert every docstring across 15 modules, covering 15 `class` statements and 43 functions and methods. |
| **9. JSDoc carries documentation tags only.** Blocks use `@param name - description` and `@returns`, with no braced types. | Include braced forms such as `@param {string} documentId`, matching common JavaScript practice. | The TypeScript Handbook supports only documentation tags in TypeScript files, and the signature already declares the type. A braced type duplicates the signature and can drift from it, at which point the comment lies. | A reader used to JavaScript JSDoc may read the absent braces as an omission and add them back, reintroducing the duplication. |
| **10. Every diagram is an inline Mermaid fence.** No generator, no image asset and no pre-render step. | Adopt a diagram generator, or commit pre-rendered SVG and PNG files to an asset directory. | GitHub renders Mermaid natively, and the three specification documents already rely on that across 25 existing fences. Mermaid therefore costs no dependency and no build step. | A Mermaid syntax error renders as a broken block rather than failing a build, so a malformed diagram can ship unnoticed. No pipeline checks the fences. |
| **11. No dependency and no linting configuration added.** `package.json` gained nothing, and the three Markdown validators run ephemerally on the host toolchain. | Add `markdownlint-cli2`, `markdown-link-check` and `@mermaid-js/mermaid-cli` to the manifest behind a `docs:lint` script. | The requirements forbid new linting configuration by name. Two of the three also declare a Node floor above this project's highest documented Node, which is 14 at `../README.md:L22`, `ci.yml:L17` and `frontend.Dockerfile:L2`. `markdownlint-cli2` 0.23.2 declares `engines.node >=22` and `@mermaid-js/mermaid-cli` 11.16.0 declares `^18.19 or >=20.0`. `markdown-link-check` 3.15.0 declares no `engines` field at all, so it is excluded on the linting-configuration ground alone rather than on a version ground. | No pipeline enforces Markdown quality. A later contributor can add an unclosed fence, an untagged code block or a dead link, and nothing in the repository catches it. |
| **12. The unresolved-module example was re-attributed and the change stated.** The example belongs to `templates.py:L17-L18`, not to `document_service.py`. | Reproduce the requirements' attribution to `document_service.py` as written. | `document_service.py` never imports `app.schema.template`. Repeating the attribution would send a reader to a file where the evidence does not exist, and the reader would conclude the documentation is wrong about everything else too. | A reader comparing this documentation against the original requirements finds a discrepancy. The correction is stated openly here for that reason rather than made silently. |
| **13. Nineteen module READMEs reported, not the stated twenty-one.** One README was created in every directory the requirements name. | Reproduce the stated total of 21 and invent two more directories to reach it. | The requirements' own enumeration yields 8 backend, 7 frontend and 4 infrastructure and automation directories. No named directory was dropped, so the correction adjusts an arithmetic total and not the scope. | A reader auditing against the stated 21 counts a shortfall of two and may hunt for files that were never named. |
| **14. Rule 1's traceability-matrix clause applied by analogy.** The clause is scoped to migrations and refactors. The matrix maps source construct to documentation artifact instead. | Declare the clause inapplicable, because this engagement is neither a migration nor a refactor, and produce no matrix. | The clause's purpose, proving nothing was left behind, transfers cleanly to documentation coverage. A documentation pass with no coverage proof cannot be audited, and Rule 1 requires any departure from a literal reading to be logged, which this entry does. | A 255-row table costs real effort to maintain. Every locator shifts when a source file gains or loses a line, so the matrix goes stale faster than the prose around it. |
| **15. Blog rule B4 declined; four blog rules adopted.** No em dashes, no bare "It" or "This" as a sentence subject, active voice and cited sources all apply. B4 does not. | Adopt B4 and vary the vocabulary with synonyms from the approved dictionary. | B4 flags a non-technical word appearing three or more times per 500 words. The AAP fixes six terms that must repeat across all 28 artifacts: router, handler, service, adapter, slice and marker. Synonym churn on those six would obscure meaning rather than sharpen it. | A reviewer applying B4 mechanically will flag this corpus for repetition. The repetition is deliberate, which this entry records so the flag can be dismissed with evidence. |
| **16. The two inner `Config` classes are documented inside their parent rows, so the matrix holds the AAP's thirteen classes and 255 rows.** Fifteen `class` statements exist. The `Settings` row and the `User` row each carry their inner Pydantic `Config` class, at `config.py:L50` and `user.py:L74`. | Give each inner class its own row, which would report fifteen classes and 257 rows, or leave both inner classes out of the matrix altogether. | Rule 1 requires the matrix complete with no gaps, and the AAP fixes the class count at thirteen. Both requirements hold at once when an inner class is documented in the row that owns it, because the construct is listed and the count is unchanged. A separate row would restate the AAP's frozen inventory, and no decision entry may amend the AAP. Dropping the two classes would leave documented constructs unlisted instead. | An inner class is findable only through its parent row, so a reader searching the matrix for `Config` has to know which model declares it. The [Backend classes heading](#backend-classes-13) and the [matrix totals](#matrix-totals) both state where the two live. |
| **17. Rule 3's own detection heuristics are the scoring thresholds.** A prose sentence over 30 words registers against the principle it touches, and so does a paragraph over five sentences. Every principle a finding touches is scored on its own. Rule 3 leaves one combination unclassified, three soft violations with no hard violation, and this file records it as NEEDS WORK. | Keep wider local bands that pass a 35-word sentence and an 8-sentence paragraph, and charge each finding to exactly one principle. | Rule 3 sets the numbers, and a local band that passes text the rule flags reports a cleaner corpus than the rule allows. Scoring each principle on its own is what the rule's per-principle scorecard asks for. | The stricter thresholds raise the finding count, so prose that read as acceptable under the wider bands had to be rewritten rather than annotated. Counting remains a choice. Inline code spans are exempt under Rule 3's Special Handling, link text counts while a link destination does not, and a list item counts as its own paragraph. A reviewer who folds list items into the surrounding paragraph measures different paragraph lengths. |
| **18. Every advisory and version-floor rationale sits in one dated register.** [troubleshooting.md](troubleshooting.md) carries the register, with the date it was compiled. A source comment states the contract and the observable defect. Where the contract depends on it, a comment states the contract and sends the reader to the register rather than naming releases, as `security.py:L100-L102` does for the passlib and bcrypt pairing. No source comment carries an advisory identifier, a dated claim or a password-hashing release version, and a release named in a comment states an observed behaviour rather than a recommended floor. | Keep each advisory beside the code that carries the risk, or open a separate dated security document. | Rule 1 makes this log and the documents it points at the single rationale surface. An advisory also ages faster than the code it describes, so a source comment goes stale where a dated register announces its own age. AAP section 0.11.1 closes the documentation set at nine `docs/` files, so a new file was not available. | A developer reading a security-relevant function sees no advisory reference in the file itself and must reach the register through the module README. Any version claim is only as current as the register's stated date. |
| **19. The defect register carries a ninth gap class the AAP does not define.** [troubleshooting.md](troubleshooting.md#g9-absent-security-controls) adds `G9 absent security controls` beyond the eight classes the AAP enumerates, holding entries 1 through 40 across five subsections, plus the sub-lettered `3a`, `22a`, `24a`, `33a`, `39a` and `39b`. | Fold every absent control into the existing `G1` through `G8` classes, or leave absent controls out of the register entirely. The ground for either would be that the AAP's taxonomy stops at `G8`, and that every class it names describes something present and wrong. | Each of `G1` through `G8` is defined by a present artifact that is wrong, and every one announces itself through a traceback, a type error or a failed command. An absent control produces no error at all, so it fails that defining property, and folding it into any of the eight would misfile it. Leaving it out would give a security reading of this repository no home in the documentation. The absences are also the findings a reader most needs before repairing the import chain, because every one goes live the moment that repair lands. | This class is the only part of the register with no upstream mandate. A reader auditing the documentation against the AAP's `G1` through `G8` finds a ninth class and cannot trace it to a requirement without this entry. Its entries are also the only ones no command reproduces, because each rests on a reading of the code rather than on an observed failure. A wrong entry would therefore survive a review that a traceback would have caught. The six sub-lettered entries keep earlier numbering stable at the cost of a sequence that no longer runs contiguously. |
| **20. Coverage and verbosity are measured separately, which is how conflict C4 dissolves.** Completeness is proved by the 255-row matrix below. Length is held down by the 150-to-400-line band on the module READMEs and by the short-cell rule in every table. | Read the instruction to be exhaustive as licence for long prose, or read Rule 3's brevity position as licence to leave constructs undocumented. | Rule 3 rejects thoroughness that destroys readability, and the requirements demand exhaustive coverage. The two collide only while one measure stands for both. Counting coverage in matrix rows and readability in sentence and paragraph length satisfies both standards at once, so no trade-off was made. | Neither number alone proves quality. A 255-row matrix of dull cells would pass the coverage measure and fail the reader, which is why `prose-validation.md` carries the second half of the proof. A reader who equates completeness with volume also reads the short cells as thin. |
| **21. The dependency register is split into a risk table and a complete inventory, and every one of the 47 distributions was queried individually.** [troubleshooting.md](troubleshooting.md#the-dated-dependency-and-advisory-register) carries thirteen PyPI risk rows first, then all 47 distributions, then four npm risk rows. Each inventory row states one of three queried verdicts, so no row reports an unexamined distribution. | One table of 47 rows carrying every advisory history, or a risk table alone with no inventory behind it. Sampling the inventory and marking the remainder as not individually queried, which is what an earlier pass of this register did. | Forty-seven advisory histories in one table bury the rows that change what a reader does. A risk table alone cannot show that nothing was omitted. Sampling fails differently: a row admitting it was never queried gives neither a clearance nor an action, so the reader redoes the work the register claimed. Querying every row is what lets absence from the risk table mean "queried, nothing found". The npm rows sit in their own table because the risk table's last two columns ask which release installs on Python 3.9, and no npm row can answer that. | A reader who stops at the risk table sees thirteen distributions and may assume the other 34 went unexamined. Three tables drift apart when a distribution is added to one and not the others. The queried verdicts are also only as current as the register's compiled date. The npm inventory covers the 26 packages this repository names rather than the 1,532 an install resolves, so an advisory inside a transitive `react-scripts` dependency is out of scope. |
| **22. [data-model.md](data-model.md) explains the drift mechanism before it enumerates the divergences.** The [Why drift arose](data-model.md#why-drift-arose) section precedes the per-entity comparisons. | Lead with the field-by-field divergence tables and explain the cause at the end, or leave the mechanism out and list the divergences alone. | The mechanism is the more useful fact. No shared schema artifact and no generated client exist, so a reader who knows that predicts the next divergence instead of memorising the current list. AAP section 0.3.3 states the same ordering. | A reader looking up one field reads a page of mechanism first. The ordering also puts the least concrete material at the top, which is exactly what a section link invites a reader to skip. |
| **23. Every generated-text piece carries its own scorecard, and every charged violation carries its own record.** `prose-validation.md` scores all 29 pieces against each principle family. Every charged violation gets one entry carrying quote, principle, replacement and reason, and every Pass cites the closest passage found rather than asserting itself. | One corpus-wide scorecard with representative entries for the worst case in each class, which is the shape that file carried before the current pass. | Rule 3's output format asks for a verdict and a scorecard per piece of generated text, and a corpus-wide row cannot show that a named file was examined. A sampled register cannot be re-derived either, because a reader cannot tell an unlisted violation from an absent one. | The per-piece tables and the full register cost more lines than a summary, and every figure in them goes stale the moment any deliverable is edited. Citing a passage under each Pass also invites a reader to mistake the citation for a defect. |
| **24. [onboarding.md](onboarding.md) pins a version only where a resolver's default breaks something.** The `passlib` and `bcrypt` pair carries exact pins at `onboarding.md:L522`. Three distributions carry a floor or a range that the code's own use establishes, and the remaining twelve are named with no version. The pyenv release tag is exact, while `nvm install 14` and `pyenv install 3.9` each resolve to the latest matching release. Every pin lives in prose because no manifest may be created. | Pin all seventeen distributions and both runtimes exactly, which is what a committed manifest would do. Or pin nothing at all and let each reader's resolver choose throughout. | An unpinned command is not a reproducible clean-machine path wherever a default resolution fails. One such pair, passlib 1.7.4 with bcrypt 5.0.0, raises on every call. Pinning the rest would assert versions no code fact establishes, so each name carries the weakest constraint its evidence supports. | Pins in prose age without warning, and no tool in this repository checks them. The twelve unpinned names resolve differently on a later date, so a reader can reach a set this guide never saw. A reader may also read a pin as a project requirement rather than as a diagnostic aid, so each pinned command has to say which it is. |
| **25. README length was allocated by evidence weight inside the 150-to-400-line band, not by the four finer sub-bands the AAP suggests.** All 19 files hold inside the band. Thirteen exceed their suggested sub-band by 2 to 50 lines, and six sit inside it. | Trim the thirteen back into their sub-bands, which cuts roughly 231 lines of cited material. Or widen the sub-bands here, which would amend an AAP that no decision entry may amend. | The AAP states one testable band, 150 to 400, and states the sub-bands as an allocation scaled to module weight. All 19 hold inside the testable band. The allocation was drawn before the defect inventory was measured, and the measured evidence redistributed the weight. [infrastructure/terraform/README.md](../infrastructure/terraform/README.md) shows why: the file carries 35 HCL blocks, 11 dead variables, 14 outputs against undeclared AWS resources and the live `terraform validate` and `fmt` results. Cutting 50 lines from it would delete cited evidence, and the AAP requires a citation for every factual claim. | A reader auditing against the sub-bands finds thirteen files over. The deltas run terraform +50, `backend/app` +44, `src` +20, `backend/tests` and `scripts` +17 each, and `pages` and `tasks` +16 each. The rest run `schema` +13, `db` and `docker` +12 each, `store` +10, and `schema` and `workflows` +2 each. Two files now sit exactly on the 400-line ceiling, `README.md` and `README.md`, so a paragraph added to either has to replace text rather than extend the file. |

## Deviations from a literal reading of the requirements

Rule 1 treats an unexplained deviation as a defect. Thirteen deviations are recorded below: five
collisions between the user-specified rules and the requirements, and seven interpretive
corrections where verification contradicted a stated fact. The thirteenth re-anchors every line
number in this file. Each collision points at the decision-table row that resolves it.

Two further departures are not numbered here, because neither is a collision between two
instructions nor a stated fact that verification contradicted. The defect register carries a ninth
gap class where the requirements enumerate eight. Decision row 19 records what was added, which
alternatives were weighed and what the addition costs a reader.

Fifteen `class` statements exist where the requirements fix the class count at thirteen, and the two
beyond the thirteen are inner Pydantic `Config` classes. Each is documented inside the row for the
model that declares it, so the requirements' thirteen classes and 255 rows both stand and no
documented construct goes unlisted. Decision row 16 records that choice, because it is a question of
representation rather than a contradicted fact.

### The five rule conflicts

| ID | The collision | How it was resolved | Decision row |
| --- | --- | --- | --- |
| C1 | Rule 2 requires updating existing onboarding documentation. The requirements place the root [../README.md](../README.md) out of scope and call it reference material. | The exclusion governs one named file, so the root README stays untouched. A new [onboarding.md](onboarding.md) carries Rule 2's substance. | 1 |
| C2 | Rule 1 forbids rationale in code comments. The requirements ask docstrings to explain why a construct exists where the name does not make that obvious. | Docstrings state the construct's role and its factual defects. Design justification stays in this log. | 2 |
| C3 | Rule 2 requires a path from a clean machine to a running application. The application does not run: `import app.main` fails at `auth.py:L20`. | [onboarding.md](onboarding.md) documents the working steps, the exact stopping point with evidence, and the remediation each blocker needs. | 3 |
| C4 | Rule 3 rejects thoroughness that destroys readability. The engagement instruction is to be exhaustive. | Coverage and verbosity were separated. Completeness is measured by the matrix below, not by word count, and every table cell stays inside two short sentences. | 20 |
| C5 | Rule 3 requires a verdict and a scorecard for every piece of generated text. No enumerated deliverable can hold them. | `prose-validation.md` became that destination. | 4 |

C4 carried no decision row until the current pass, on the ground that a conflict which dissolves
involves no trade-off. Rule 1 tests for a choice a competent engineer could have made differently,
and separating the two measures is such a choice. Row 20 now records it with its alternatives and
its risk, so every conflict in the table above points at a row.

### The seven interpretive corrections

Verification against the repository contradicted seven stated facts. Every delivered figure below is
the verified one, so each row discloses a correction rather than an error in this documentation.

| ID | What the requirements state | What verification found | Where it is recorded |
| --- | --- | --- | --- |
| A1 | Numbered section references such as a layer diagram at section 5 and intended behaviour at section 5.2.6, against a specification exceeding 12,000 lines. | The in-repository [Technical Specifications](<../documentation/Technical Specifications.md>) runs 781 physical lines and carries 5 unnumbered H1 headings, 17 unnumbered H2 headings and 18 unnumbered H3 headings, so no section anchor exists inside it. | Numbered citations resolve to the generated Technical Specification, a separate document. In-repository citations quote a heading name plus a line number, per the convention in [README.md](README.md). |
| A2 | `document_service.py` imports `app.schema.template` as the worked example of a dependency on an absent module. | `document_service.py` carries no such import. The real site is `templates.py:L17-L18`, which imports from `app.schema.template` and `app.services.template_service`, and neither module exists. | Decision row 12, and [backend/app/api/README.md](../backend/app/api/README.md). |
| A3 | Twenty-one new README files. | The enumeration yields 19: eight backend directories, seven frontend directories, four infrastructure and automation directories. | Decision row 13, and [README.md](README.md). |
| A4 | The ownership drift is two-way, `owner_id` against `user_id`, with two specification sites. | The drift spans four code positions and **three** specification sites. The third sits at `Technical Specifications.md:L383`. | [data-model.md](data-model.md), and decision row 7. |
| A5 | The reachability label `REACHABLE`, applied to Firestore and to Cloud Storage for exports. | No integration earns that label. Every module holding a Firestore call fails to import, and no handler calls either export method, so four narrower labels replace it: `WIRED, BLOCKED AT IMPORT`, `NOT REACHABLE`, `SCAFFOLDED ONLY` and `ABSENT`. | [integration-guide.md](integration-guide.md) states at `integration-guide.md:L57` that no integration earns the strongest label, and defines all four at `:L68-L73`. [README.md](README.md) fixes the same four across the set at `README.md:L122-L126`. |
| A6 | Nine modules import a `settings` singleton from `app.core.config`. | Eight import that name. Nine modules import from `config.py`, and the ninth is `security.py:L22`, which imports the `get_settings` factory instead and resolves. Nine module-import failures also trace to the absent singleton, which is a third measurement again. | [integration-guide.md](integration-guide.md) separates all three counts at `integration-guide.md:L715-L726`. [backend/app/core/README.md](../backend/app/core/README.md) carries both importer rows at `README.md:L67-L68`. |
| A7 | Five statements in the root README contradict the committed tree. | Six do. The sixth is the `git clone` command at `../README.md:L29`, which names a placeholder organisation and cannot succeed as written. | [troubleshooting.md](troubleshooting.md) lists all six at `troubleshooting.md:L1706-L1713`. [README.md](README.md) states the same total at `README.md:L182-L184`. |

#### The third specification site, in detail

Correction A4 matters enough to spell out, because the AAP cites only two specification sites and
a reader auditing the count would find a third unaccounted for. All three sites use `owner_id`,
and they sit under two different headings.

| Site | Heading it sits under | What it describes |
| --- | --- | --- |
| `Technical Specifications.md:L333` | Google Cloud Firestore (NoSQL), at `:L319` | The `owner_id` field of the Documents collection |
| `Technical Specifications.md:L375` | Google Cloud SQL (Relational), at `:L356` | The `owner_id` column of the DOCUMENTS entity |
| `Technical Specifications.md:L383` | Google Cloud SQL (Relational), at `:L356` | The `owner_id` column of the TEMPLATES entity |

The third site extends the same naming to templates, so the specification is internally
consistent on `owner_id` across both entities. The committed code is not. `backend/app/schema/document.py:L28`
declares `owner_id: Optional[str] = None`, `backend/app/schema/document.py:L85` declares
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
| `DocumentService.get_document` | `document_service.py:L26` | `document_service.py:L78` | 1 line, both |
| First `HUMAN ASSISTANCE NEEDED` marker | `main.py:L15-L16` | `main.py:L38-L39` | 2 lines, both |
| `DocumentSchema` | `document.ts:L3-L11` | `document.ts:L23-L31` | 9 lines, both |

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

The matrix runs to 255 rows, so a single table would be unreadable and would fail Rule 3's
indifference test. Rows are grouped into seventeen subsections by area. Four conventions keep
every row inside the page width, and no convention drops a locator.

- **Documenting README** carries a short key. The first key table below resolves every key to
  the README that owns the row.
- **`docs/` Coverage** carries a short key. The second key table resolves every key to a
  document under `docs/`.
- **Location** gives a file name and a line locator, such as `documents.py:L69`. The directory
  comes from the Documenting README key on the same row. Where Source Construct already names
  the file, or names the class whose module file carries the same name, Location gives the bare
  line locator, such as `L78`.
- A token too wide for its column splits across two adjacent code spans, as
  `document_service.py` `L78` or `GOOGLE_APPLICATION_` `CREDENTIALS`. The split serves
  rendering only. Read the two parts as one token.

The AAP fixes the count at 255 rows across thirteen backend classes, and the matrix matches it.
Verification found fifteen `class` statements, and the two beyond the thirteen are inner Pydantic
`Config` classes. Each is documented inside the row for the model that declares it, so construct
rows total 108 and no documented construct is left unlisted. Decision row 16 owns that choice.

Five groups of files receive no inline documentation, because the requirements exclude them:
three test modules, three container artifacts, two workflow files, two shell scripts and two
frontend manifests. Every row in those groups carries
`None by design (AAP R7)` in the Inline Documentation column and still reaches COVERED, because a
module README documents each one from outside. Decision row 5 records the boundary.

#### Documenting README key

Backend directories use their bare name. Frontend directories carry the `src/` prefix, which
keeps `schema` and `services` unambiguous across the two languages.

| Key in the matrix | README |
| --- | --- |
| `app` | [backend/app/README.md](../backend/app/README.md) |
| `api` | [backend/app/api/README.md](../backend/app/api/README.md) |
| `core` | [backend/app/core/README.md](../backend/app/core/README.md) |
| `db` | [backend/app/db/README.md](../backend/app/db/README.md) |
| `schema` | [backend/app/schema/README.md](../backend/app/schema/README.md) |
| `services` | [backend/app/services/README.md](../backend/app/services/README.md) |
| `tasks` | [backend/app/tasks/README.md](../backend/app/tasks/README.md) |
| `tests` | [backend/tests/README.md](../backend/tests/README.md) |
| `src` | [frontend/src/README.md](../frontend/src/README.md) |
| `src/components` | [frontend/src/components/README.md](../frontend/src/components/README.md) |
| `src/pages` | [frontend/src/pages/README.md](../frontend/src/pages/README.md) |
| `src/schema` | [frontend/src/schema/README.md](../frontend/src/schema/README.md) |
| `src/services` | [frontend/src/services/README.md](../frontend/src/services/README.md) |
| `src/store` | [frontend/src/store/README.md](../frontend/src/store/README.md) |
| `src/utils` | [frontend/src/utils/README.md](../frontend/src/utils/README.md) |
| `terraform` | [infrastructure/terraform/README.md](../infrastructure/terraform/README.md) |
| `docker` | [infrastructure/docker/README.md](../infrastructure/docker/README.md) |
| `.github/workflows` | [.github/workflows/README.md](../.github/workflows/README.md) |
| `scripts` | [scripts/README.md](../scripts/README.md) |

#### `docs/` coverage key

| Key in the matrix | Document |
| --- | --- |
| `architecture` | [architecture-overview.md](architecture-overview.md) |
| `data-model` | [data-model.md](data-model.md) |
| `integration` | [integration-guide.md](integration-guide.md) |
| `deployment` | [deployment-guide.md](deployment-guide.md) |
| `troubleshooting` | [troubleshooting.md](troubleshooting.md) |
| `onboarding` | [onboarding.md](onboarding.md) |

### The three worked rows

The AAP supplies three rows to fix the matrix's shape. All three are reproduced below in that
exact shape, with locators re-anchored to the current branch head per deviation D6. Each of the
three also appears in its own subsection further down, so these are a worked example rather than
three extra rows.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `DocumentService` `.get_document` | `L78` | `services` | Google-style docstring per the user template | `data-model` | COVERED |
| `HUMAN ASSISTANCE NEEDED` | `main.py:L38-L39` | `app`, Known Limitations | Preserved verbatim; referenced by the module docstring | `troubleshooting` | COVERED |
| `DocumentSchema` (no inferred type) | `document.ts:L23-L31` | `src/schema` | File header stating the root-cause chain | `data-model`, `troubleshooting` | COVERED |

### Backend modules (15)

One row per Python module under `backend/app/`. Each carries a module docstring placed above its imports.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `main.py` | `L1-L13` | `app` | Module docstring naming all six unresolved imports | `architecture`, `troubleshooting` | COVERED |
| `api/auth.py` | `L1-L18` | `api` | Module docstring; records the duplicated `get_current_user` | `integration`, `troubleshooting` | COVERED |
| `api/documents.py` | `L1-L20` | `api` | Module docstring; records five call-site defects | `data-model`, `troubleshooting` | COVERED |
| `api/templates.py` | `L1-L14` | `api` | Module docstring; names both absent modules at `:L17-L18` | `data-model`, `troubleshooting` | COVERED |
| `api/users.py` | `L1-L15` | `api` | Module docstring; records both handlers as synchronous | `data-model`, `troubleshooting` | COVERED |
| `core/config.py` | `L1-L18` | `core` | Module docstring; states that no `settings` instance exists | `deployment`, `troubleshooting` | COVERED |
| `core/security.py` | `L1-L22` | `core` | Module docstring; three undefined names, and `jwt.JWTError` confirmed sound | `integration`, `troubleshooting` | COVERED |
| `db/firestore.py` | `L1-L18` | `db` | Module docstring; import-time client construction | `integration`, `data-model` | COVERED |
| `db/sql.py` | `L1-L14` | `db` | Module docstring; the declared but unused relational path | `data-model`, `deployment` | COVERED |
| `schema/document.py` | `L1-L14` | `schema` | Module docstring; the `owner_id` and `user_id` split inside one file | `data-model`, `troubleshooting` | COVERED |
| `schema/user.py` | `L1-L15` | `schema` | Module docstring; the absent password field and the Pydantic 1.x pin | `data-model`, `troubleshooting` | COVERED |
| `services/collaboration_service.py` | `L1-L18` | `services` | Module docstring; two absent imports and the per-process registry | `integration`, `troubleshooting` | COVERED |
| `services/document_service.py` | `L1-L12` | `services` | Module docstring; async methods wrapping a synchronous SDK | `data-model`, `integration` | COVERED |
| `services/export_service.py` | `L1-L16` | `services` | Module docstring; the placeholder export payloads | `integration`, `troubleshooting` | COVERED |
| `tasks/background_tasks.py` | `L1-L20` | `tasks` | Module docstring; the absent `datetime` import and the invalid decorator | `deployment`, `integration` | COVERED |

### Backend classes (13)

Thirteen model and service classes, the count the AAP fixes. Fifteen `class` statements exist, and the two beyond the thirteen are inner Pydantic `Config` classes. Each is documented in the row for the model that declares it, `Settings` and `User`, which decision row 16 explains. Both received their own class docstring in the source, so no class is left undocumented.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `Settings` | `config.py:L20` | `core` | Class docstring listing all nine fields as `Attributes:`. Its inner `Config` at `:L50` carries a class docstring recording that it points Pydantic at an uncommitted `.env` | `deployment`, `onboarding` | COVERED |
| `DocumentBase` | `document.py:L16` | `schema` | Class docstring; `owner_id` optional with a default | `data-model`, `troubleshooting` | COVERED |
| `DocumentCreate` | `document.py:L30` | `schema` | Class docstring; inherits `DocumentBase` | `data-model`, `integration` | COVERED |
| `DocumentUpdate` | `document.py:L40` | `schema` | Class docstring; does not inherit `DocumentBase` | `data-model`, `troubleshooting` | COVERED |
| `Document` | `document.py:L52` | `schema` | Class docstring; required timestamps no service writes | `data-model`, `troubleshooting` | COVERED |
| `DocumentVersion` | `document.py:L67` | `schema` | Class docstring; names its actor `user_id` | `data-model`, `troubleshooting` | COVERED |
| `UserBase` | `user.py:L17` | `schema` | Class docstring; `username` and `full_name`, no `name` | `data-model`, `troubleshooting` | COVERED |
| `UserCreate` | `user.py:L30` | `schema` | Class docstring; carries the plaintext password field | `data-model`, `integration` | COVERED |
| `UserUpdate` | `user.py:L40` | `schema` | Class docstring; every field optional | `data-model`, `troubleshooting` | COVERED |
| `User` | `user.py:L56` | `schema` | Class docstring; flags no code path reads. Its inner `Config` at `:L74` carries a class docstring recording that `orm_mode` pins Pydantic to 1.x | `data-model`, `troubleshooting`, `onboarding` | COVERED |
| `CollaborationService` | `L20` | `services` | Class docstring; never instantiated by any route | `integration`, `troubleshooting` | COVERED |
| `DocumentService` | `L19` | `services` | Class docstring listing all four public methods | `data-model`, `integration` | COVERED |
| `ExportService` | `L18` | `services` | Class docstring; no `convert_document` despite a task calling it | `integration`, `troubleshooting` | COVERED |

### Backend functions and methods (43)

Every function and method under `backend/app/`, including the nested Pub/Sub `callback`. Docstrings follow Google style with `Args:`, `Returns:` and `Raises:` sections.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `get_current_user` | `auth.py:L28` | `api` | Docstring; duplicate of the `core` version, and returns 404 where `core` returns 401 | `integration`, `troubleshooting` | COVERED |
| `login_for_access_token` | `auth.py:L67` | `api` | Docstring with `Args:`, `Returns:` and `Raises:`; one of the two public handlers | `integration`, `onboarding` | COVERED |
| `register_user` | `auth.py:L104` | `api` | Docstring; hashes a password the `User` contract cannot store | `data-model`, `troubleshooting` | COVERED |
| `create_document` | `documents.py:L25` | `api` | Docstring; passes a `User` object where `user_id: str` is declared | `data-model`, `troubleshooting` | COVERED |
| `get_documents` | `documents.py:L50` | `api` | Docstring; calls a service method that does not exist | `data-model`, `troubleshooting` | COVERED |
| `get_document` | `documents.py:L69` | `api` | Docstring; calls the service with one argument against a two-argument signature | `data-model`, `troubleshooting` | COVERED |
| `update_document` | `documents.py:L99` | `api` | Docstring; reads `user_id` off a schema declaring `owner_id` | `data-model`, `troubleshooting` | COVERED |
| `delete_document` | `documents.py:L132` | `api` | Docstring; same arity and field defects as the read handler | `data-model`, `troubleshooting` | COVERED |
| `create_template` | `templates.py:L25` | `api` | Docstring; depends on the absent `TemplateService` | `data-model`, `troubleshooting` | COVERED |
| `get_templates` | `templates.py:L43` | `api` | Docstring; path collides with the documents list handler | `data-model`, `troubleshooting` | COVERED |
| `get_template` | `templates.py:L60` | `api` | Docstring; shadowed by the documents router, so never reached | `data-model`, `troubleshooting` | COVERED |
| `update_template` | `templates.py:L87` | `api` | Docstring; shadowed, and depends on the absent template schema | `data-model`, `troubleshooting` | COVERED |
| `delete_template` | `templates.py:L113` | `api` | Docstring; shadowed by the documents delete handler | `data-model`, `troubleshooting` | COVERED |
| `get_current_user_info` | `users.py:L20` | `api` | Docstring; declared `def`, as is the other handler in this module, while all twelve handlers in the other three routers are `async def` | `data-model`, `troubleshooting` | COVERED |
| `update_user` | `users.py:L33` | `api` | Docstring; the module's second synchronous `def` handler, and it awaits nothing and persists nothing | `data-model`, `troubleshooting` | COVERED |
| `get_settings` | `config.py:L63` | `core` | Docstring with `Returns:` and `Raises:`; carries no caching decorator | `deployment`, `onboarding` | COVERED |
| `create_access_token` | `security.py:L27` | `core` | Docstring plus a usage example, as a named primary entry point | `integration`, `onboarding` | COVERED |
| `verify_password` | `security.py:L59` | `core` | Docstring with `Args:` and `Returns:`; bcrypt comparison | `integration`, `troubleshooting` | COVERED |
| `get_password_hash` | `security.py:L86` | `core` | Docstring; the bcrypt context duplicated from the auth router | `integration`, `troubleshooting` | COVERED |
| `get_current_user` | `security.py:L110` | `core` | Docstring plus a usage example; three undefined names recorded | `integration`, `onboarding` | COVERED |
| `get_document` | `firestore.py:L22` | `db` | Docstring plus a usage example; annotated `-> dict` while returning `None` | `data-model`, `integration` | COVERED |
| `create_document` | `firestore.py:L45` | `db` | Docstring plus a usage example; synchronous, and consumed by no service | `data-model`, `integration` | COVERED |
| `update_document` | `firestore.py:L64` | `db` | Docstring; synchronous, and consumed by no service | `data-model`, `integration` | COVERED |
| `delete_document` | `firestore.py:L81` | `db` | Docstring; synchronous, and consumed by no service | `data-model`, `integration` | COVERED |
| `get_db` | `sql.py:L21` | `db` | Docstring using `Yields:`, the repository's only generator | `data-model`, `deployment` | COVERED |
| `startup_event` | `main.py:L27` | `app` | Docstring; awaits an absent `init_db` and swallows every exception | `deployment`, `troubleshooting` | COVERED |
| `shutdown_event` | `main.py:L55` | `app` | Docstring; closes nothing that the module opened | `deployment`, `troubleshooting` | COVERED |
| `CollaborationService` `.__init__` | `L32` | `services` | Constructor docstring; builds the Pub/Sub clients at construction | `integration`, `troubleshooting` | COVERED |
| `CollaborationService` `.connect` | `L44` | `services` | Docstring; registers a socket and returns before subscribing | `integration`, `troubleshooting` | COVERED |
| `callback` | `collaboration_` `service.py` `L80` | `services` | Docstring; the nested Pub/Sub message handler | `integration`, `troubleshooting` | COVERED |
| `CollaborationService` `.disconnect` | `L107` | `services` | Docstring; removes the socket from a per-process dictionary | `integration`, `troubleshooting` | COVERED |
| `CollaborationService` `.broadcast_change` | `L137` | `services` | Docstring; blocking `future.result()` inside an async method | `integration`, `troubleshooting` | COVERED |
| `DocumentService` `.__init__` | `L33` | `services` | Constructor docstring; binds the shared Firestore client | `data-model`, `integration` | COVERED |
| `DocumentService` `.create_document` | `L42` | `services` | Docstring; writes the ownership key as `user_id` | `data-model`, `integration` | COVERED |
| `DocumentService` `.get_document` | `L78` | `services` | Google-style docstring per the user template | `data-model`, `troubleshooting` | COVERED |
| `DocumentService` `.update_document` | `L116` | `services` | Docstring; read-modify-read path costing three Firestore operations | `data-model`, `integration` | COVERED |
| `DocumentService` `.delete_document` | `L159` | `services` | Docstring; ownership comparison explained as non-obvious logic | `data-model`, `integration` | COVERED |
| `ExportService` `.__init__` | `L29` | `services` | Constructor docstring; builds the Cloud Storage client | `integration`, `deployment` | COVERED |
| `ExportService` `.export_to_pdf` | `L40` | `services` | Docstring; uploads a literal placeholder payload | `integration`, `troubleshooting` | COVERED |
| `ExportService` `.export_to_docx` | `L74` | `services` | Docstring; second placeholder payload and a second key layout | `integration`, `troubleshooting` | COVERED |
| `process_document_export` | `background_` `tasks.py` `L25` | `tasks` | Task docstring; no producer enqueues it | `integration`, `deployment` | COVERED |
| `cleanup_expired_documents` | `background_` `tasks.py` `L73` | `tasks` | Task docstring; invalid periodic decorator, and `.delete()` on a result list | `deployment`, `troubleshooting` | COVERED |
| `update_document_statistics` | `background_` `tasks.py` `L116` | `tasks` | Task docstring; reads `document.pages`, which no schema declares | `data-model`, `troubleshooting` | COVERED |

### Frontend modules (26)

One row per TypeScript and TSX module under `frontend/src/`. Each carries a block comment header beginning at line 1, above the imports.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `index.tsx` | `L1` | `src` | File header; `ReactDOM.render` is the React 17 legacy path | `architecture`, `troubleshooting` | COVERED |
| `App.tsx` | `L1` | `src` | File header; the v5-only `Switch` and a second `Provider` | `architecture`, `troubleshooting` | COVERED |
| `components/DocumentCanvas.tsx` | `L1` | `src/components` | File header; the two inverse type errors documented together | `architecture`, `troubleshooting` | COVERED |
| `components/Footer.tsx` | `L1` | `src/components` | File header; five hard-coded status values | `architecture`, `troubleshooting` | COVERED |
| `components/Header.tsx` | `L1` | `src/components` | File header; reads `avatar` and `name`, neither modelled | `data-model`, `troubleshooting` | COVERED |
| `components/ImageEditor.tsx` | `L1` | `src/components` | File header; the absent `imageUtils` module | `architecture`, `troubleshooting` | COVERED |
| `components/Sidebar.tsx` | `L1` | `src/components` | File header; three absent panel modules rendered unconditionally | `architecture`, `troubleshooting` | COVERED |
| `components/TableEditor.tsx` | `L1` | `src/components` | File header; the absent `tableUtils` module | `architecture`, `troubleshooting` | COVERED |
| `components/TextEditor.tsx` | `L1` | `src/components` | File header; presented as the argument-count reference only | `architecture`, `troubleshooting` | COVERED |
| `components/Toolbar.tsx` | `L1` | `src/components` | File header; one-argument helper calls and lowercase constants | `architecture`, `troubleshooting` | COVERED |
| `pages/Editor.tsx` | `L1` | `src/pages` | File header; the five-second debounce and four named imports of defaults | `integration`, `troubleshooting` | COVERED |
| `pages/Home.tsx` | `L1` | `src/pages` | File header; the correct default imports, noted as the contrast case | `architecture`, `troubleshooting` | COVERED |
| `pages/Settings.tsx` | `L1` | `src/pages` | File header; three non-existent imported symbols | `data-model`, `troubleshooting` | COVERED |
| `pages/Templates.tsx` | `L1` | `src/pages` | File header; a local interface incompatible with the Zod schema | `data-model`, `troubleshooting` | COVERED |
| `schema/document.ts` | `L1-L12` | `src/schema` | File header stating the root-cause chain for five downstream errors | `data-model`, `troubleshooting` | COVERED |
| `schema/template.ts` | `L1` | `src/schema` | File header; diverges from the local interface in `Templates.tsx` | `data-model`, `troubleshooting` | COVERED |
| `schema/user.ts` | `L1` | `src/schema` | File header; the absent `updated_at` the server declares | `data-model`, `troubleshooting` | COVERED |
| `services/api.ts` | `L1` | `src/services` | File header; the environment variable mismatch and three absent types | `integration`, `troubleshooting` | COVERED |
| `services/auth.ts` | `L1` | `src/services` | File header; three endpoint paths no server route matches | `integration`, `troubleshooting` | COVERED |
| `services/collaboration.ts` | `L1` | `src/services` | File header; `io()` called with no URL, and no inbound event handled | `integration`, `troubleshooting` | COVERED |
| `store/documentSlice.ts` | `L1` | `src/store` | File header; the five-entry cap on recent documents | `architecture`, `troubleshooting` | COVERED |
| `store/index.ts` | `L1` | `src/store` | File header; two named reducer imports the slices never provide | `architecture`, `troubleshooting` | COVERED |
| `store/userSlice.ts` | `L1` | `src/store` | File header; the absent `updateUser` action four modules import | `architecture`, `troubleshooting` | COVERED |
| `utils/documentUtils.ts` | `L1` | `src/utils` | File header; `DocumentSchema.isValid` recorded as two faults at once | `data-model`, `troubleshooting` | COVERED |
| `utils/formatting.ts` | `L1` | `src/utils` | File header; the unused `SelectionState` import | `architecture`, `troubleshooting` | COVERED |
| `utils/validation.ts` | `L1` | `src/utils` | File header; the one defect-free module, with discarded messages | `data-model`, `troubleshooting` | COVERED |

### React components (13)

Thirteen `React.FC` components. Each carries a JSDoc block directly above its declaration, using documentation tags only.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `App` | `App.tsx:L33` | `src` | Component JSDoc; renders the shell a second time | `architecture`, `troubleshooting` | COVERED |
| `DocumentCanvas` | `DocumentCanvas.tsx` `L34` | `src/components` | Component JSDoc; propless signature against a caller passing two props | `architecture`, `troubleshooting` | COVERED |
| `Footer` | `Footer.tsx:L21` | `src/components` | Component JSDoc; two zoom buttons with no handlers | `architecture`, `troubleshooting` | COVERED |
| `Header` | `Header.tsx:L29` | `src/components` | Component JSDoc; absent logo asset and two undeclared routes | `architecture`, `troubleshooting` | COVERED |
| `ImageEditor` | `ImageEditor.tsx:L28` | `src/components` | Component JSDoc; no block renderer, so an atomic image never renders | `architecture`, `troubleshooting` | COVERED |
| `Sidebar` | `Sidebar.tsx:L22` | `src/components` | Component JSDoc; names the three absent panels | `architecture`, `troubleshooting` | COVERED |
| `TableEditor` | `TableEditor.tsx:L27` | `src/components` | Component JSDoc; renders an empty element | `architecture`, `troubleshooting` | COVERED |
| `TextEditor` | `TextEditor.tsx:L23` | `src/components` | Component JSDoc; the argument-count contract and the inline mismatch | `architecture`, `troubleshooting` | COVERED |
| `Toolbar` | `Toolbar.tsx:L34` | `src/components` | Component JSDoc; holds no editor state at all | `architecture`, `troubleshooting` | COVERED |
| `Editor` | `Editor.tsx:L28` | `src/pages` | Page JSDoc; the auto-save effect follows the user template | `integration`, `troubleshooting` | COVERED |
| `Home` | `Home.tsx:L27` | `src/pages` | Page JSDoc; three undeclared route links | `architecture`, `troubleshooting` | COVERED |
| `Settings` | `Settings.tsx:L33` | `src/pages` | Page JSDoc; once-only state initialization leaves the form empty | `data-model`, `troubleshooting` | COVERED |
| `Templates` | `Templates.tsx:L42` | `src/pages` | Page JSDoc; write-only state and a terminal card click | `data-model`, `troubleshooting` | COVERED |

### Exported TypeScript symbols (39)

Thirty-nine `export` statements. Thirteen are the component default exports listed above, kept as separate rows because the export form matters: four modules named-import a default-only export. The remaining 26 are schemas, types, reducers, functions and the two destructured action exports, which carry six and four action creators respectively and name every one.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `export default App` | `App.tsx:L54` | `src` | JSDoc on the component above; imported correctly by `index.tsx` | `architecture` | COVERED |
| `export default DocumentCanvas` | `DocumentCanvas.tsx` `L74` | `src/components` | JSDoc on the component above; default-imported by `Editor.tsx` | `architecture` | COVERED |
| `export default Footer` | `Footer.tsx:L41` | `src/components` | JSDoc on the component above; named-imported by three pages | `architecture`, `troubleshooting` | COVERED |
| `export default Header` | `Header.tsx:L65` | `src/components` | JSDoc on the component above; named-imported by three pages | `architecture`, `troubleshooting` | COVERED |
| `export default ImageEditor` | `ImageEditor.tsx:L66` | `src/components` | JSDoc on the component above; no module imports it | `architecture`, `troubleshooting` | COVERED |
| `export default Sidebar` | `Sidebar.tsx:L32` | `src/components` | JSDoc on the component above; named-imported by `Editor.tsx` | `architecture`, `troubleshooting` | COVERED |
| `export default TableEditor` | `TableEditor.tsx:L74` | `src/components` | JSDoc on the component above; no module imports it | `architecture`, `troubleshooting` | COVERED |
| `export default TextEditor` | `TextEditor.tsx:L78` | `src/components` | JSDoc on the component above; no page references it | `architecture`, `troubleshooting` | COVERED |
| `export default Toolbar` | `Toolbar.tsx:L91` | `src/components` | JSDoc on the component above; named-imported by `Editor.tsx` | `architecture`, `troubleshooting` | COVERED |
| `export default Editor` | `Editor.tsx:L119` | `src/pages` | JSDoc on the component above; routed at `/editor` | `architecture` | COVERED |
| `export default Home` | `Home.tsx:L53` | `src/pages` | JSDoc on the component above; routed at `/` | `architecture` | COVERED |
| `export default Settings` | `Settings.tsx:L93` | `src/pages` | JSDoc on the component above; routed at `/settings` | `architecture` | COVERED |
| `export default Templates` | `Templates.tsx:L113` | `src/pages` | JSDoc on the component above; routed at `/templates` | `architecture` | COVERED |
| `DocumentSchema` | `document.ts:L23-L31` | `src/schema` | JSDoc; seven required fields, and `owner_id` contradicting the server | `data-model`, `troubleshooting` | COVERED |
| `DocumentVersionSchema` | `document.ts:L39` | `src/schema` | JSDoc; names its actor `user_id`, matching the server | `data-model`, `troubleshooting` | COVERED |
| `TemplateSchema` | `template.ts:L21` | `src/schema` | JSDoc; no server counterpart exists | `data-model`, `troubleshooting` | COVERED |
| `type Template` | `template.ts:L31` | `src/schema` | JSDoc; the inferred type `document.ts` omits | `data-model`, `troubleshooting` | COVERED |
| `UserSchema` | `user.ts:L19` | `src/schema` | JSDoc; omits the `updated_at` the Pydantic contract declares | `data-model`, `troubleshooting` | COVERED |
| `type User` | `user.ts:L30` | `src/schema` | JSDoc; the inferred type `document.ts` omits | `data-model`, `troubleshooting` | COVERED |
| `getDocuments` | `api.ts:L69` | `src/services` | JSDoc with `@returns`; prefixes `/documents` against a router mounted at root | `integration`, `troubleshooting` | COVERED |
| `createDocument` | `api.ts:L82` | `src/services` | JSDoc with `@param` and `@returns`; same prefix mismatch | `integration`, `troubleshooting` | COVERED |
| `updateDocument` | `api.ts:L95` | `src/services` | JSDoc with `@param` and `@returns`; same prefix mismatch | `integration`, `troubleshooting` | COVERED |
| `login` | `auth.ts:L35` | `src/services` | JSDoc; posts to `/auth/login`, which no server route matches | `integration`, `troubleshooting` | COVERED |
| `logout` | `auth.ts:L53` | `src/services` | JSDoc; posts to `/auth/logout`, which no server route matches | `integration`, `troubleshooting` | COVERED |
| `getCurrentUser` | `auth.ts:L70` | `src/services` | JSDoc; unchecked cast to `User` | `data-model`, `troubleshooting` | COVERED |
| `export default CollaborationService` | `collaboration.ts` `L109` | `src/services` | JSDoc on the class and all three methods; never instantiated | `integration`, `troubleshooting` | COVERED |
| Six document actions: `setCurrentDocument`, `addRecentDocument`, `setLoading`, `setError`, `clearCurrentDocument`, `clearRecentDocuments` | `documentSlice.ts` `L117-L124` | `src/store` | JSDoc per action with a usage example, as named primary entry points | `architecture`, `data-model` | COVERED |
| `export default documentSlice.reducer` | `documentSlice.ts` `L127` | `src/store` | JSDoc; the store imports a named `documentReducer` instead | `architecture`, `troubleshooting` | COVERED |
| `type RootState` | `index.ts:L32` | `src/store` | JSDoc; derived from the store, so it lacks an `auth` key | `architecture`, `troubleshooting` | COVERED |
| `type AppDispatch` | `index.ts:L34` | `src/store` | JSDoc; no typed dispatch hook exports it | `architecture`, `troubleshooting` | COVERED |
| `export default store` | `index.ts:L36` | `src/store` | JSDoc; `App.tsx:L20` named-imports this default-only export | `architecture`, `troubleshooting` | COVERED |
| Four user actions: `setUser`, `clearUser`, `setLoading`, `setError` | `userSlice.ts:L97` | `src/store` | JSDoc per action with a usage example, as named primary entry points | `architecture`, `data-model` | COVERED |
| `export default userSlice.reducer` | `userSlice.ts:L100` | `src/store` | JSDoc; the store imports a named `userReducer` instead | `architecture`, `troubleshooting` | COVERED |
| `serializeDocument` | `documentUtils.ts` `L29` | `src/utils` | JSDoc with `@param` and `@returns`; validates against the wrong schema | `data-model`, `troubleshooting` | COVERED |
| `deserializeDocument` | `documentUtils.ts` `L49` | `src/utils` | JSDoc with `@param` and `@returns`; same category error | `data-model`, `troubleshooting` | COVERED |
| `applyInlineStyle` | `formatting.ts:L24` | `src/utils` | JSDoc making the two-argument contract explicit | `architecture`, `troubleshooting` | COVERED |
| `applyBlockStyle` | `formatting.ts:L45` | `src/utils` | JSDoc making the two-argument contract explicit | `architecture`, `troubleshooting` | COVERED |
| `validateEmail` | `validation.ts:L21` | `src/utils` | JSDoc; returns only `.success`, discarding its own message | `data-model`, `troubleshooting` | COVERED |
| `validatePassword` | `validation.ts:L36` | `src/utils` | JSDoc; the password policy spelled out | `data-model`, `troubleshooting` | COVERED |

### Terraform files (3)

The three HashiCorp Configuration Language (HCL) files are the single configuration-file exception that receives inline comments. Decision row 5 records the boundary.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `main.tf` | `L1-L99` | `terraform` | Short `#` comments on non-obvious blocks; three absent module sources | `deployment`, `troubleshooting` | COVERED |
| `variables.tf` | `L1-L95` | `terraform` | Short `#` comments marking each variable consumed or dead | `deployment`, `onboarding` | COVERED |
| `outputs.tf` | `L1-L87` | `terraform` | Short `#` comments naming the AWS-outputs oddity and the two password leaks | `deployment`, `troubleshooting` | COVERED |

### Test modules (3)

The only README describing a directory whose files receive no inline documentation. [backend/tests/README.md](../backend/tests/README.md) states that exclusion explicitly so a later pass does not add docstrings here.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `tests/test_api.py` | `L1-L77` | `tests` | None by design (AAP R7) | `troubleshooting`, `onboarding` | COVERED |
| `tests/test_db.py` | `L1-L58` | `tests` | None by design (AAP R7) | `troubleshooting`, `onboarding` | COVERED |
| `tests/test_services.py` | `L1-L80` | `tests` | None by design (AAP R7) | `troubleshooting`, `onboarding` | COVERED |

### Container artifacts (3)

Two Dockerfiles and one Compose file, documented from outside by [infrastructure/docker/README.md](../infrastructure/docker/README.md).

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `backend.Dockerfile` | `L1-L27` | `docker` | None by design (AAP R7) | `deployment`, `troubleshooting` | COVERED |
| `frontend.Dockerfile` | `L1-L32` | `docker` | None by design (AAP R7) | `deployment`, `troubleshooting` | COVERED |
| `docker-compose.yml` | `L1-L46` | `docker` | None by design (AAP R7) | `deployment`, `onboarding` | COVERED |

### Workflow files (2)

Continuous integration and continuous deployment definitions, documented from outside by [.github/workflows/README.md](../.github/workflows/README.md).

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `ci.yml` | `L1-L23` | `.github/workflows` | None by design (AAP R7) | `deployment`, `troubleshooting` | COVERED |
| `cd.yml` | `L1-L20` | `.github/workflows` | None by design (AAP R7) | `deployment`, `troubleshooting` | COVERED |

### Shell scripts (2)

Both scripts are documented from outside by [scripts/README.md](../scripts/README.md), which marks the exact failing command in each.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `deploy.sh` | `L1-L47` | `scripts` | None by design (AAP R7) | `deployment`, `troubleshooting` | COVERED |
| `setup_dev_environment.sh` | `L1-L56` | `scripts` | None by design (AAP R7) | `onboarding`, `troubleshooting` | COVERED |

### Frontend manifests (2)

Configuration files with no logic. [frontend/src/README.md](../frontend/src/README.md) documents both, including the five path aliases that omit the prefix nearly every module uses.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `package.json` | `L1-L57` | `src` | None by design (AAP R7) | `onboarding`, `troubleshooting` | COVERED |
| `tsconfig.json` | `L1-L30` | `src` | None by design (AAP R7) | `onboarding`, `troubleshooting` | COVERED |

### `HUMAN ASSISTANCE NEEDED` markers (33)

The repository-wide total. All 33 survive verbatim and in place, and each is cited in a Known Limitations section and again in the complete register in [troubleshooting.md](troubleshooting.md).

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `HUMAN ASSISTANCE NEEDED`, flagging the startup block that awaits an absent `init_db` | `main.py:L38-L39` | `app` | Preserved verbatim; referenced by the surrounding documentation | `deployment`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging an assumed `UserService` class that does not exist | `users.py:L54-L56` | `api` | Preserved verbatim; referenced by the surrounding documentation | `troubleshooting`, `architecture` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the token dependency's undefined `User` and `UserService` names | `security.py` `L106-L109` | `core` | Preserved verbatim; referenced by the surrounding documentation | `troubleshooting`, `integration` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging `connect`, at a stated confidence of 0.6 | `collaboration_` `service.py` `L42-L43` | `services` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging `broadcast_change`, at a stated confidence of 0.7 | `collaboration_` `service.py` `L135-L136` | `services` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging `update_document` as needing error handling and validation | `document_` `service.py` `L114-L115` | `services` | Preserved verbatim; referenced by the surrounding documentation | `data-model`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging both export methods as low confidence | `export_service.py` `L38-L39` | `services` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the export task as unready for production | `background_` `tasks.py` `L49-L50` | `tasks` | Preserved verbatim; referenced by the surrounding documentation | `deployment`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the retention sweep as unready and unoptimized | `background_` `tasks.py` `L91-L92` | `tasks` | Preserved verbatim; referenced by the surrounding documentation | `deployment`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the whole component, below a confidence of 0.8 | `DocumentCanvas.tsx` `L20-L21` | `src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the atomic-block insert helper | `ImageEditor.tsx` `L29-L30` | `src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the unwritten image-editing interface | `ImageEditor.tsx` `L58-L59` | `src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the table insert helper, at a stated confidence of 0.6 | `TableEditor.tsx` `L28-L29` | `src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the key-command handler | `TextEditor.tsx` `L26-L27` | `src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the whole toolbar as needing error handling | `Toolbar.tsx:L19-L21` | `src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the editor page as unready for production | `Editor.tsx:L20-L21` | `src/pages` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the settings page as needing refinement | `Settings.tsx` `L18-L20` | `src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging absent error handling, paired with the TODO on the next line | `Templates.tsx` `L64-L65` | `src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging absent navigation, paired with the TODO on the next line | `Templates.tsx` `L81-L82` | `src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the empty listener body, with an example listener commented out | `collaboration.ts` `L50-L53` | `src/services` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging `joinDocument` | `collaboration.ts` `L56-L57` | `src/services` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging `sendChanges` | `collaboration.ts` `L83-L84` | `src/services` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging absent thunks for asynchronous document operations | `documentSlice.ts` `L129-L132` | `src/store` | Preserved verbatim; referenced by the surrounding documentation | `architecture`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging absent error types and the absent `updateUser` action | `userSlice.ts` `L102-L105` | `src/store` | Preserved verbatim; referenced by the surrounding documentation | `architecture`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging both serialization helpers and the schema validation call | `documentUtils.ts` `L17-L19` | `src/utils` | Preserved verbatim; referenced by the surrounding documentation | `data-model`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the subnet range and the firewall rule set | `main.tf:L94-L97` | `terraform` | Preserved verbatim; referenced by the surrounding documentation | `deployment`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging outputs that may not match any declared resource | `outputs.tf:L58-L60` | `terraform` | Preserved verbatim; referenced by the surrounding documentation | `deployment`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the unconfigured test database connection | `test_api.py:L13` | `tests` | Preserved verbatim; file receives no inline documentation (AAP R7) | `troubleshooting`, `onboarding` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging absent endpoint and edge-case coverage | `test_api.py:L77` | `tests` | Preserved verbatim; file receives no inline documentation (AAP R7) | `troubleshooting`, `onboarding` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging absent update, delete and error-handling tests | `test_db.py:L56-L58` | `tests` | Preserved verbatim; file receives no inline documentation (AAP R7) | `troubleshooting`, `onboarding` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the Python version and the absent requirements file | `backend.Dockerfile` `L22-L26` | `docker` | Preserved verbatim; file receives no inline documentation (AAP R7) | `deployment`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the unwritten post-deployment checks | `deploy.sh:L37-L38` | `scripts` | Preserved verbatim; file receives no inline documentation (AAP R7) | `deployment`, `troubleshooting` | COVERED |
| `HUMAN ASSISTANCE NEEDED`, flagging the environment file, paired with the TODO on the next line | `setup_dev_` `environment.sh` `L41` | `scripts` | Preserved verbatim; file receives no inline documentation (AAP R7) | `onboarding`, `troubleshooting` | COVERED |

### `TODO` markers (16)

The repository-wide total. All 16 survive verbatim. Two sit directly beneath a marker, in `Templates.tsx` and `setup_dev_environment.sh`, and the documentation records both as pairs.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `TODO`: implement database migration logic | `main.py:L49` | `app` | Preserved verbatim; referenced by the surrounding documentation | `deployment`, `troubleshooting` | COVERED |
| `TODO`: add additional shutdown cleanup | `main.py:L72` | `app` | Preserved verbatim; referenced by the surrounding documentation | `deployment`, `troubleshooting` | COVERED |
| `TODO`: implement PDF conversion logic | `export_service.py` `L57` | `services` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `TODO`: replace the placeholder PDF content | `export_service.py` `L62` | `services` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `TODO`: implement DOCX conversion logic | `export_service.py` `L89` | `services` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `TODO`: replace the placeholder DOCX content | `export_service.py` `L94` | `services` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `TODO`: implement the insert action | `Toolbar.tsx:L67` | `src/components` | Preserved verbatim; referenced by the surrounding documentation | `architecture`, `troubleshooting` | COVERED |
| `TODO`: add proper error handling on document load | `Editor.tsx:L54` | `src/pages` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `TODO`: add error handling and user notification on auto-save | `Editor.tsx:L87` | `src/pages` | Preserved verbatim; referenced by the surrounding documentation | `integration`, `troubleshooting` | COVERED |
| `TODO`: add a success message on save | `Settings.tsx:L52` | `src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model`, `troubleshooting` | COVERED |
| `TODO`: add error handling and user feedback | `Settings.tsx:L55` | `src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model`, `troubleshooting` | COVERED |
| `TODO`: implement error handling and user feedback | `Templates.tsx:L65` | `src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model`, `troubleshooting` | COVERED |
| `TODO`: implement navigation after a template is chosen | `Templates.tsx:L82` | `src/pages` | Preserved verbatim; referenced by the surrounding documentation | `data-model`, `troubleshooting` | COVERED |
| `TODO`: implement proper schema validation on serialize | `documentUtils.ts` `L33` | `src/utils` | Preserved verbatim; referenced by the surrounding documentation | `data-model`, `troubleshooting` | COVERED |
| `TODO`: implement proper schema validation on deserialize | `documentUtils.ts` `L58` | `src/utils` | Preserved verbatim; referenced by the surrounding documentation | `data-model`, `troubleshooting` | COVERED |
| `TODO`: populate the environment file for production | `setup_dev_` `environment.sh` `L42` | `scripts` | Preserved verbatim; file receives no inline documentation (AAP R7) | `onboarding`, `troubleshooting` | COVERED |

### HTTP operations (14)

Fourteen operations across four routers. Twelve sit behind the token dependency and two are public. Every path in the templates router duplicates a path in the documents router, and `backend/app/main.py:L84-L87` mounts both without a prefix, so Starlette matches the documents router first.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `POST /token` | `auth.py:L66` | `api` | Handler docstring at `:L67`; one of the two public operations | `integration`, `onboarding` | COVERED |
| `POST /register` | `auth.py:L103` | `api` | Handler docstring at `:L104`; the second public operation | `integration`, `onboarding` | COVERED |
| `POST /` (documents) | `documents.py:L24` | `api` | Handler docstring at `:L25`; protected, and collides with the template create | `data-model`, `troubleshooting` | COVERED |
| `GET /` (documents) | `documents.py:L49` | `api` | Handler docstring at `:L50`; protected, and calls an absent service method | `data-model`, `troubleshooting` | COVERED |
| `GET /{document_id}` | `documents.py:L68` | `api` | Handler docstring at `:L69`; protected, and shadows the template read | `data-model`, `troubleshooting` | COVERED |
| `PUT /{document_id}` | `documents.py:L98` | `api` | Handler docstring at `:L99`; protected, and shadows the template update | `data-model`, `troubleshooting` | COVERED |
| `DELETE /{document_id}` | `documents.py:L131` | `api` | Handler docstring at `:L132`; protected, and shadows the template delete | `data-model`, `troubleshooting` | COVERED |
| `POST /` (templates) | `templates.py:L24` | `api` | Handler docstring at `:L25`; protected, and never reached | `data-model`, `troubleshooting` | COVERED |
| `GET /` (templates) | `templates.py:L42` | `api` | Handler docstring at `:L43`; protected, and never reached | `data-model`, `troubleshooting` | COVERED |
| `GET /{template_id}` | `templates.py:L59` | `api` | Handler docstring at `:L60`; protected, and never reached | `data-model`, `troubleshooting` | COVERED |
| `PUT /{template_id}` | `templates.py:L86` | `api` | Handler docstring at `:L87`; protected, and never reached | `data-model`, `troubleshooting` | COVERED |
| `DELETE /{template_id}` | `templates.py:L112` | `api` | Handler docstring at `:L113`; protected, and never reached | `data-model`, `troubleshooting` | COVERED |
| `GET /me` | `users.py:L19` | `api` | Handler docstring at `:L20`; protected, and synchronous | `data-model`, `troubleshooting` | COVERED |
| `PUT /me` | `users.py:L32` | `api` | Handler docstring at `:L33`; protected, synchronous, and persists nothing | `data-model`, `troubleshooting` | COVERED |

### Settings fields (15)

Nine fields are declared on the `Settings` model, and six more are read by other modules and declared nowhere. Every row is marked DECLARED or READ BUT NEVER DECLARED.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `PROJECT_NAME`, DECLARED | `config.py:L40` | `core` | Documented in the `Settings` class docstring as an `Attributes:` entry | `deployment`, `onboarding` | COVERED |
| `API_V1_STR`, DECLARED and never read | `config.py:L41` | `core` | Documented as declared with no reader anywhere in the tree | `deployment`, `onboarding` | COVERED |
| `SECRET_KEY`, DECLARED | `config.py:L42` | `core` | Documented; read at `security.py:L56` and in the auth router | `integration`, `onboarding` | COVERED |
| `ACCESS_TOKEN_` `EXPIRE_MINUTES`, DECLARED | `config.py:L43` | `core` | Documented; read at `security.py:L54` | `integration`, `onboarding` | COVERED |
| `ALGORITHM`, DECLARED | `config.py:L44` | `core` | Documented; carries no validator, so any string satisfies it | `integration`, `onboarding` | COVERED |
| `GOOGLE_CLOUD_PROJECT`, DECLARED | `config.py:L45` | `core` | Documented; read at `firestore.py:L20` | `integration`, `deployment` | COVERED |
| `GOOGLE_APPLICATION_` `CREDENTIALS`, DECLARED | `config.py:L46` | `core` | Documented; the credential model relies on it | `integration`, `deployment` | COVERED |
| `DATABASE_URL`, DECLARED | `config.py:L47` | `core` | Documented; read at `sql.py:L16` at import time | `deployment`, `onboarding` | COVERED |
| `REDIS_URL`, DECLARED | `config.py:L48` | `core` | Documented; read at `background_tasks.py` `L22` | `deployment`, `integration` | COVERED |
| `ALLOWED_ORIGINS`, READ BUT NEVER DECLARED | `main.py:L77` | `app` | Documented in the module docstring as absent from the `Settings` model | `deployment`, `troubleshooting` | COVERED |
| `PROJECT_ID`, READ BUT NEVER DECLARED | `collaboration_` `service.py` `L69` | `services` | Documented; also read at `:L128` and `:L153` | `integration`, `troubleshooting` | COVERED |
| `STORAGE_BUCKET_NAME`, READ BUT NEVER DECLARED | `export_service.py` `L60` | `services` | Documented; also read at `:L92` | `integration`, `troubleshooting` | COVERED |
| `SIGNED_URL_EXPIRATION`, READ BUT NEVER DECLARED | `export_service.py` `L68` | `services` | Documented; also read at `:L100` | `integration`, `troubleshooting` | COVERED |
| `EXPORT_BUCKET_NAME`, READ BUT NEVER DECLARED | `background_` `tasks.py` `L62` | `tasks` | Documented in the task docstring as absent from the model | `deployment`, `troubleshooting` | COVERED |
| `DOCUMENT_BUCKET_NAME`, READ BUT NEVER DECLARED | `background_` `tasks.py` `L107` | `tasks` | Documented in the task docstring as absent from the model | `deployment`, `troubleshooting` | COVERED |

### Terraform variables (13)

Thirteen declared variables. Only `project_id` and `region` reach a resource, leaving eleven dead. No variable carries a validation block.

| Source Construct | Location | Documenting README | Inline Documentation | `docs/` Coverage | Status |
| --- | --- | --- | --- | --- | --- |
| `project_id`, CONSUMED | `variables.tf:L7` | `terraform` | `#` comment marking it consumed; read at `main.tf:L10` | `deployment`, `onboarding` | COVERED |
| `region`, CONSUMED | `variables.tf:L14` | `terraform` | `#` comment marking it consumed; read at `main.tf:L11` | `deployment`, `onboarding` | COVERED |
| `zone`, DEAD | `variables.tf:L21` | `terraform` | `#` comment marking it declared and unreferenced | `deployment`, `troubleshooting` | COVERED |
| `compute_instance_type`, DEAD | `variables.tf:L29` | `terraform` | `#` comment marking it declared and unreferenced | `deployment`, `troubleshooting` | COVERED |
| `storage_class`, DEAD | `variables.tf:L37` | `terraform` | `#` comment; the bucket resource sets no storage class | `deployment`, `troubleshooting` | COVERED |
| `database_tier`, DEAD | `variables.tf:L44` | `terraform` | `#` comment marking it declared and unreferenced | `deployment`, `troubleshooting` | COVERED |
| `environment`, DEAD | `variables.tf:L53` | `terraform` | `#` comment; no validation block, so any string passes | `deployment`, `troubleshooting` | COVERED |
| `dev_instance_count`, DEAD | `variables.tf:L61` | `terraform` | `#` comment marking it declared and unreferenced | `deployment`, `troubleshooting` | COVERED |
| `staging_instance_count`, DEAD | `variables.tf:L67` | `terraform` | `#` comment marking it declared and unreferenced | `deployment`, `troubleshooting` | COVERED |
| `prod_instance_count`, DEAD | `variables.tf:L73` | `terraform` | `#` comment marking it declared and unreferenced | `deployment`, `troubleshooting` | COVERED |
| `dev_storage_size`, DEAD | `variables.tf:L79` | `terraform` | `#` comment marking it declared and unreferenced | `deployment`, `troubleshooting` | COVERED |
| `staging_storage_size`, DEAD | `variables.tf:L85` | `terraform` | `#` comment marking it declared and unreferenced | `deployment`, `troubleshooting` | COVERED |
| `prod_storage_size`, DEAD | `variables.tf:L91` | `terraform` | `#` comment marking it declared and unreferenced | `deployment`, `troubleshooting` | COVERED |

### Matrix totals

| Group | Composition | Rows |
| --- | --- | --- |
| File rows | 15 backend modules, 26 frontend modules, 3 Terraform files, 3 test modules, 3 container artifacts, 2 workflows, 2 shell scripts, 2 manifests | 56 |
| Construct rows | 13 Python classes, 43 Python functions and methods, 13 React components, 39 export statements | 108 |
| Marker rows | 33 `HUMAN ASSISTANCE NEEDED`, 16 `TODO` | 49 |
| Contract rows | 14 HTTP operations, 15 settings fields, 13 Terraform variables | 42 |
| **Total** | All four groups combined | **255** |

The two inner `Config` classes add no row, because the `Settings` row and the `User` row each carry
one. Decision row 16 records that choice.

Every one of the 255 Status cells reads COVERED. Nineteen rows describe files the requirements
exclude from inline documentation. Twelve of those are file rows carrying an explicit
`None by design (AAP R7)` cell, and seven are marker rows recording a marker preserved in a file
that was never edited. All nineteen reach COVERED through their README.

One counting note, so a mechanical check agrees with this total. The three worked rows under
[The three worked rows](#the-three-worked-rows) each carry a COVERED cell and sit outside the 255,
because they demonstrate the row shape rather than document a construct. A checker that scans the
whole section for COVERED therefore finds 258.

## The reverse matrix

Running the mapping backwards exposes two failure modes a single-direction matrix hides: an
artifact that documents nothing, and a construct documented nowhere.

One row per new artifact, 28 in total. The Constructs covered column counts the matrix rows
naming that artifact, so the figures are derived from the matrix above rather than asserted
separately. The nineteen README counts sum to 255, which proves no row lacks an owner. The six
`docs/` counts overlap by design, because most constructs appear in two repository-level
documents.

### The 19 module READMEs

| Artifact | What it documents | Constructs covered | Gaps |
| --- | --- | --- | --- |
| [backend/app/README.md](../backend/app/README.md) | The composition root: the application object, both lifecycle handlers, the four router mounts and the undeclared CORS origin setting | 7 matrix rows | None |
| [backend/app/api/README.md](../backend/app/api/README.md) | Four routers, all 14 handlers and all 14 HTTP operations, plus the documents-over-templates path collision | 34 matrix rows | None |
| [backend/app/core/README.md](../backend/app/core/README.md) | The `Settings` model with all nine declared fields, its inner `Config` class, and the four security primitives | 18 matrix rows | None |
| [backend/app/db/README.md](../backend/app/db/README.md) | The Firestore adapter's four helpers and the declared but unused relational path, including the one generator | 7 matrix rows | None |
| [backend/app/schema/README.md](../backend/app/schema/README.md) | All nine Pydantic model classes, the one inner `Config` class on `User`, and the ownership split inside one file | 11 matrix rows | None |
| [backend/app/services/README.md](../backend/app/services/README.md) | Three service classes and their thirteen function definitions, twelve methods plus the nested Pub/Sub callback at `collaboration_service.py:L80` | 30 matrix rows | None |
| [backend/app/tasks/README.md](../backend/app/tasks/README.md) | The Celery application, three tasks, the invalid periodic decorator and two undeclared bucket settings | 8 matrix rows | None |
| [backend/tests/README.md](../backend/tests/README.md) | Three test modules and their three markers, from outside | 6 matrix rows | None. Inline comments excluded by AAP R7, so coverage is README-only |
| [frontend/src/README.md](../frontend/src/README.md) | The bootstrap path, the routed shell and both frontend manifests | 6 matrix rows | None. Inline comments excluded by AAP R7, so coverage is README-only |
| [frontend/src/components/README.md](../frontend/src/components/README.md) | Eight component modules, eight components, their export forms, and six markers with one `TODO` | 31 matrix rows | None |
| [frontend/src/pages/README.md](../frontend/src/pages/README.md) | Four page modules, four page components, the five-second debounce, and four markers with six `TODO` comments | 22 matrix rows | None |
| [frontend/src/schema/README.md](../frontend/src/schema/README.md) | Three Zod modules and six exported schema values and types, including the absent inferred type | 9 matrix rows | None |
| [frontend/src/services/README.md](../frontend/src/services/README.md) | Three client modules, seven exported functions, the collaboration class and three markers | 13 matrix rows | None |
| [frontend/src/store/README.md](../frontend/src/store/README.md) | Three store modules, ten action creators, two reducers, two types and the store default export | 12 matrix rows | None |
| [frontend/src/utils/README.md](../frontend/src/utils/README.md) | Three utility modules and six exported functions, plus the one defect-free module | 12 matrix rows | None |
| [infrastructure/terraform/README.md](../infrastructure/terraform/README.md) | Three HCL files, thirteen variables marked consumed or dead, and two markers | 18 matrix rows | None |
| [infrastructure/docker/README.md](../infrastructure/docker/README.md) | Two Dockerfiles, one Compose topology and one marker, all from outside | 4 matrix rows | None. Inline comments excluded by AAP R7, so coverage is README-only |
| [.github/workflows/README.md](../.github/workflows/README.md) | Both pipeline definitions, from outside, with the exact failing step marked | 2 matrix rows | None. Inline comments excluded by AAP R7, so coverage is README-only |
| [scripts/README.md](../scripts/README.md) | Both shell scripts, from outside, plus two markers and one TODO | 5 matrix rows | None. Inline comments excluded by AAP R7, so coverage is README-only |

The nineteen counts above sum to 255, matching the matrix total exactly.

### The 9 documents under `docs/`

| Artifact | What it documents | Constructs covered | Gaps |
| --- | --- | --- | --- |
| [README.md](README.md) | The index: every sibling document and all 19 module READMEs, plus the five shared conventions | None, by design | None. An index carries navigation, not construct documentation |
| [architecture-overview.md](architecture-overview.md) | The six top-level areas, the four tiers, the five boundaries and the broken edges between them | 57 matrix rows | None |
| [data-model.md](data-model.md) | Dual persistence, four entity families, the Pydantic and Zod contracts and the four-way ownership drift | 88 matrix rows | None |
| [integration-guide.md](integration-guide.md) | Firestore, Cloud Storage signed URLs, Pub/Sub and the absent Redis broker, each labelled by reachability | 71 matrix rows | None |
| [deployment-guide.md](deployment-guide.md) | Terraform, containers, both pipelines, the deploy script and every reason a deploy fails | 51 matrix rows | None |
| [troubleshooting.md](troubleshooting.md) | The full defect register across nine gap classes, the root README inaccuracies, and all 49 markers | 209 matrix rows | None |
| [onboarding.md](onboarding.md) | Clean-machine setup, domain context, the common pitfalls, how to extend, and the ordered next tasks | 29 matrix rows | None |
| decision-log.md (this file) | Twenty-five decisions, thirteen deviations and the bidirectional matrix | All 255 matrix rows | None |
| prose-validation.md | Rule 3 verdicts and principle scorecards for all 29 pieces of generated text | None, by design | None. Validates prose quality, not construct coverage |

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
