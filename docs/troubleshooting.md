# Troubleshooting and Defect Register

The `microsoft-word-u33ko0` repository does not run. The backend cannot import, and only 3 of the
15 modules under `backend/app/` load. The frontend cannot typecheck, and `tsc --noEmit` reports 76
errors. Neither container builds, the Terraform cannot initialise, and both `npm ci` invocations
fail. Every one of those failures appears below with the file and line that causes it.

Coverage is wider than that opening list. The nine classes below carry every defect this
documentation pass verified against the committed source, including the ones a headline failure
hides. Eight of the nine are the classes the requirements enumerate, `G1` through `G8`, and the ninth
is `G9 absent security controls`, which decision row 19 in
[decision-log.md](decision-log.md#the-decision-table) explains. Six of those hidden defects are worth
naming up front:

- the seven protected handlers that registration order makes unreachable
- the two credential prerequisites a version 4 signed URL needs
- the Pub/Sub topic nothing creates
- the publish error that is caught and printed rather than raised
- the ownership subscript that answers 500 instead of 403
- the retention sweep's partial-deletion states

A defect is listed here only when a committed line demonstrates it, so the register grows if someone
verifies one this pass did not reach.

This document records defects. Repairing them fell outside the documentation engagement that
produced this file, so that engagement fixed none of them. Read no entry here as fixed.
[decision-log.md](decision-log.md) holds the record of that boundary.

## How to read this register

Two orderings run through this document, and they serve different readers.

The [symptom-first index](#symptom-first-index) runs in **encounter order**. Rows follow the
sequence a developer meets them while working through the setup steps in
[the root README](../README.md), starting with a clone and ending at a deploy. Each row names a
defect class and points into the section that carries the detail.

Sections `G1` through `G9` run in **taxonomy order** and stay there, because a reference section is
easier to return to when its position never moves. Read the index to find your problem. Read the
taxonomy section to understand it.

`G9` differs from the eight classes above it in one way worth knowing before you reach it. Classes
`G1` through `G8` record something present and wrong. `G9` records something absent, so no error
message announces any of it and no command surfaces it. A missing control produces no symptom until
someone exploits it, which is why the symptom-first index cannot carry these rows.

### The defect classes

| Class | Covers |
| ------- | -------- |
| [G1](#g1-absent-modules-referenced-by-committed-code) | Absent modules referenced by committed code |
| [G2](#g2-absent-symbols-inside-modules-that-do-exist) | Absent symbols inside modules that do exist |
| [G3](#g3-undefined-names-that-raise-at-execution) | Undefined names with no import behind them |
| [G4](#g4-undeclared-third-party-dependencies) | Third-party packages the code imports and no manifest declares |
| [G5](#g5-call-site-contract-violations) | Calls that disagree with the signature they target |
| [G6](#g6-field-and-shape-drift) | Field names and shapes that disagree across a boundary |
| [G7](#g7-endpoint-and-transport-mismatch) | Client routes, server routes and transports that do not meet |
| [G8](#g8-platform-and-automation-defects) | Container, pipeline, script and infrastructure defects |
| [G9](#g9-absent-security-controls) | Security controls the committed code does not implement |

### How citations work

Every factual claim carries a locator in the form `path:Lnn`, and most locators also name the
symbol at that line. Read the symbol name as the durable half of the citation. Line numbers move
whenever anyone edits a file above them, and symbol names do not.

Three conventions govern the locators:

- Locators point at the **committed state at the current branch head**, which includes the inline
  documentation added to 44 source files. A locator therefore matches what you see when you open
  the file today, not what an earlier revision held.
- Line numbers are **physical**. No source or configuration file in this repository ends with a
  newline, so `wc -l` reports one line fewer than each of those files contains. Counting tools
  that rely on trailing newlines will disagree with this register by one line. The Markdown this
  engagement added does end with a newline, so no README and no file under `docs/` carries that
  discrepancy.
- A range such as `backend/app/core/config.py:L40-L48` covers every line in the span,
  inclusive.

### Terminology

The words below carry one fixed meaning throughout this register.

| Term | Meaning |
| ------ | --------- |
| router | A FastAPI `APIRouter` instance |
| handler | A route function carrying a `@router` decorator |
| service | A domain service class under `backend/app/services/` |
| adapter | A persistence module under `backend/app/db/` |
| slice | A Redux Toolkit slice under `frontend/src/store/` |
| marker | A `HUMAN ASSISTANCE NEEDED` comment left by the code's authors |

### What this register does not do

Three limits apply, and each one has a home elsewhere.

- **No repair guidance.** Entries state what is broken and where. Ordering the repair work belongs
  to [onboarding.md](onboarding.md), whose Suggested next tasks section orders that work.
- **No design rationale.** Where this engagement made a judgement, the entry states it and links
  to [decision-log.md](decision-log.md). Declining to name any single ownership field canonical is
  one such judgement. Arguments belong in the decision log rather than here.
- **No specification claims presented as behaviour.** The three documents under `documentation/`
  describe intended behaviour rather than committed behaviour. Anything drawn from them carries the
  label **declared intent** and a citation by heading name plus line, because all three files use
  unnumbered headings only. `documentation/Technical Specifications.md` holds five level-one
  headings: `L3` INTRODUCTION, `L125` SYSTEM ARCHITECTURE, `L300` SYSTEM DESIGN, `L523` TECHNOLOGY
  STACK and `L620` SECURITY CONSIDERATIONS.

  No numbered section anchor exists inside it. A numbered section citation anywhere in this
  documentation set refers to the generated Technical Specification, a separate document, and the
  text says so when it does.

## Symptom-first index

Rows run in the order a developer meets them, following the setup and run steps in
[the root README](../README.md) and then the automation. The Class column points into the taxonomy
section that carries the detail.

| Symptom | What you were doing | Class | Evidence |
| --------- | --------------------- | ------- | ---------- |
| `git clone` targets a placeholder organisation and fails | Following step 1 of the README installation section | [README](#documentation-inaccuracies-in-the-root-readme) | `README.md:L29` names `github.com/your-organization/microsoft-word.git` |
| `npm install` succeeds. One observed run resolved 1,532 packages | Installing frontend dependencies | none | Verified in `frontend/`. The count follows the registry rather than this repository. The five packages at [G4](#g4-undeclared-third-party-dependencies) stay missing because no manifest lists them |
| `pip install -r requirements.txt` fails, no such file | Installing backend dependencies | [G4](#g4-undeclared-third-party-dependencies) | No `requirements.txt` exists anywhere. `README.md:L42` and `scripts/setup_dev_environment.sh:L26` both invoke it |
| `tsc --noEmit` reports 76 errors, so the build fails | Starting or building the frontend | [G1](#g1-absent-modules-referenced-by-committed-code), [G2](#g2-absent-symbols-inside-modules-that-do-exist), [G4](#g4-undeclared-third-party-dependencies) | Distribution in [the type-check profile](#the-verified-type-check-profile) |
| The interface renders with no styling at all | Viewing the running frontend | [G8 Tailwind](#tailwind-never-compiles) | No `tailwind.config.js`, no `postcss.config.js` and no committed stylesheet |
| `uvicorn main:app --reload` cannot find the application | Starting the backend from `backend/` per the README | [README](#documentation-inaccuracies-in-the-root-readme) | The application object sits at `backend/app/main.py:L24` (`app = FastAPI()`), one directory deeper |
| `ImportError: cannot import name 'settings' from 'app.core.config'` | Importing `app.main` from `backend/` | [G2 settings singleton](#the-absent-settings-singleton) | `backend/app/main.py:L16` reaches `backend/app/api/auth.py:L19`, which requests a name `backend/app/core/config.py` never defines |
| `ModuleNotFoundError: No module named 'app.schema.template'` | Importing `app.api.templates` | [G1](#g1-absent-modules-referenced-by-committed-code) | `backend/app/api/templates.py:L17` |
| `ModuleNotFoundError: No module named 'app.services.user_service'` | Importing `app.api.users` or `app.api.auth` | [G1](#g1-absent-modules-referenced-by-committed-code) | `backend/app/api/users.py:L14` and `backend/app/api/auth.py:L21` |
| `NameError: name 'Optional' is not defined` | Importing `app.core.security` | [G3](#g3-undefined-names-that-raise-at-execution) | `backend/app/core/security.py:L25` uses `Optional` with no import behind it |
| Template endpoints return document responses | Calling any `/{id}` route | [G7 shadowed routes](#document-routes-shadow-the-template-and-profile-routes) | `backend/app/main.py:L84-L87` mounts every router with no prefix |
| `GET /me` answers 401 without valid credentials, and with them returns a document read or a 404 for a document called `me` | Fetching the signed-in profile | [G7 shadowed routes](#document-routes-shadow-the-template-and-profile-routes) | `backend/app/api/documents.py:L68` claims every single-segment path ahead of `backend/app/api/users.py:L19`, and both routes are protected, so the token resolves before the substitution is observable |
| `POST /documents` answers 405 while `PUT /documents/{id}` answers 404 | Calling the document API from the client | [G7 client routes](#the-client-calls-six-routes-and-no-server-route-matches-any-of-them) | `frontend/src/services/api.ts:L82` and `:L95` prefix a segment no route declares. Routing settles both before any dependency runs, so neither depends on credentials |
| `GET /documents` answers 401 without valid credentials and 500 with them | Listing documents from the client | [G7 client routes](#the-client-calls-six-routes-and-no-server-route-matches-any-of-them) | `frontend/src/services/api.ts:L70` sends one segment, which the protected `GET /{document_id}` at `backend/app/api/documents.py:L68` claims |
| Login answers 422 rather than 401 once the path is corrected | Signing in | [G7 client routes](#the-client-calls-six-routes-and-no-server-route-matches-any-of-them) | `frontend/src/services/auth.ts:L36` sends JSON `email`, and `backend/app/api/auth.py:L66` reads a form `username` |
| `npm ci` fails in continuous integration, reporting `ENOENT` on npm 6 or `EUSAGE` on npm 7 and newer | Running the CI workflow | [G8 npm ci](#npm-ci-cannot-run-anywhere) | `.github/workflows/ci.yml:L19` runs at the repository root, where no manifest and no lockfile exist. `ci.yml:L17` pins Node 14, which ships npm 6 |
| `docker compose build` cannot find a Dockerfile | Building the containers | [G8 Compose contexts](#compose-points-at-dockerfiles-that-are-not-there) | `infrastructure/docker/docker-compose.yml:L6-L7` and `:L19-L20` |
| `terraform init` reports `Unreadable module directory` | Initialising the infrastructure | [G8 absent modules](#three-terraform-module-sources-do-not-exist) | `infrastructure/terraform/main.tf:L67`, `:L76`, `:L85`. No `modules/` directory exists |
| Celery workers have no broker to attach to | Running background jobs | [G8 no Redis broker](#no-redis-service-backs-the-celery-broker) | `backend/app/tasks/background_tasks.py:L22` reads `settings.REDIS_URL`, and no service provides Redis |
| The deploy step uploads descriptors that do not exist | Running the CD workflow | [G8 CD descriptors](#the-cd-workflow-deploys-two-absent-descriptors) | `.github/workflows/cd.yml:L19-L20` deploys `app.yaml` and `dispatch.yaml` |
| An export uploads and then fails to produce a link | Exporting a document once the earlier blockers clear | [G8 signed URL credentials](#signed-url-generation-needs-credentials-nothing-supplies) | `backend/app/services/export_service.py:L66-L70` signs version 4 with credentials that carry no private key and no `signBlob` grant |
| A collaboration subscribe or publish answers `NotFound` | Opening a second editor on one document | [G7 absent topic](#nothing-creates-the-pubsub-topic-the-server-addresses) | `backend/app/services/collaboration_service.py:L73` and `:L156` address a topic no code and no infrastructure creates |
| A change publishes silently and never arrives | Editing with collaboration wired up | [G7 swallowed publish](#a-failed-publish-is-caught-and-logged-rather-than-raised) | `backend/app/services/collaboration_service.py:L158` catches every publish failure and `:L160` prints it |

## G1 absent modules referenced by committed code

Committed code imports ten application modules that no file provides, and the test suite adds six
more. Each import in the two tables below resolves to nothing, so the importing module cannot load.
Three further test imports are a different case, and the third table separates them out: those files
exist, and only the import root and a later missing symbol stop them.

### Application modules

| Absent module | Requested at | Symbols requested | Effect |
| --------------- | -------------- | ------------------- | -------- |
| `app.services.user_service` | `backend/app/api/auth.py:L21`, `backend/app/api/users.py:L14` | `UserService` | Both routers fail to import. `backend/app/core/security.py:L159` also constructs `UserService()` with no import at all, covered in [G3](#g3-undefined-names-that-raise-at-execution) |
| `app.schema.template` | `backend/app/api/templates.py:L17` | `Template`, `TemplateCreate`, `TemplateUpdate` | The template router fails to import. No Pydantic contract for a template exists anywhere in the backend |
| `app.services.template_service` | `backend/app/api/templates.py:L18` | `TemplateService` | The template router has no service tier behind its five handlers |
| `@/components/StylePanel` | `frontend/src/components/Sidebar.tsx:L10` | `StylePanel` | Rendered unconditionally at `Sidebar.tsx:L25` |
| `@/components/CommentPanel` | `frontend/src/components/Sidebar.tsx:L11` | `CommentPanel` | Rendered unconditionally at `Sidebar.tsx:L26` |
| `@/components/RevisionPanel` | `frontend/src/components/Sidebar.tsx:L12` | `RevisionPanel` | Rendered unconditionally at `Sidebar.tsx:L27` |
| `@/utils/tableUtils` | `frontend/src/components/TableEditor.tsx:L12` | `insertTable`, `deleteTable`, `modifyTable` | `handleInsertTable` at `TableEditor.tsx:L42` calls `insertTable`, and no module defines it |
| `@/utils/imageUtils` | `frontend/src/components/ImageEditor.tsx:L12` | `resizeImage`, `cropImage` | Neither import is used in the component body |
| `init_db` from `app.db.sql` | `backend/app/main.py:L22` | `init_db` | `backend/app/db/sql.py` defines `engine`, `SessionLocal`, `Base` and `get_db`, and defines no `init_db`. The startup handler awaits the missing name at `main.py:L42` |
| The `app` package itself | Every `from app.*` import across 12 modules | the `app`, `app.api`, `app.core`, `app.db`, `app.schema`, `app.services` and `app.tasks` namespaces | No `__init__.py` file exists anywhere under `backend/`, so all seven are implicit namespace packages. They resolve only while `backend/` sits on the import path, and `infrastructure/docker/backend.Dockerfile:L14` copies `./app` to `/app`, which flattens the package and leaves the `app.` prefix unresolvable inside the image |

The five frontend rows above carry a second, independent failure. Each specifier uses the `@/`
prefix, which the compiler cannot resolve either, as [G4 unmapped prefix](#the-unmapped-import-prefix) records.
Creating the five missing files would not clear those five errors on its own.

`backend/app/api/templates.py:L17-L18` is the clearest example of the pattern in the whole
repository: one module, two imports, neither target present. The engagement that produced this
register corrected an earlier attribution of this example to
`backend/app/services/document_service.py`, which carries no such import.
[decision-log.md](decision-log.md) records that correction as decision row 12.

Full treatment sits in [../backend/app/api/README.md](../backend/app/api/README.md),
[../frontend/src/components/README.md](../frontend/src/components/README.md) and
[../backend/app/db/README.md](../backend/app/db/README.md).

### Modules referenced only by the test suite

The three modules under `backend/tests/` name six further module targets that no file provides, using
three mutually incompatible import conventions. No test in this repository can collect.

| Absent module | Requested at | Import convention |
| --------------- | -------------- | ------------------- |
| `app.models` | `backend/tests/test_api.py:L4` | `app.*`, matching the application source |
| `app.database` | `backend/tests/test_api.py:L5` | `app.*` |
| `backend.db.firestore_operations` | `backend/tests/test_db.py:L6` | `backend.*`, a root the application never uses |
| `backend.db.sql_operations` | `backend/tests/test_db.py:L7` | `backend.*` |
| `models.document` | `backend/tests/test_services.py:L6` | bare `models.*`, a root that exists nowhere |
| `models.user` | `backend/tests/test_services.py:L7` | bare `models.*` |

`backend` and `app` themselves resolve as implicit namespace packages whenever their parent directory
sits on the import path, so `backend.db` fails with `No module named 'backend.db'` rather than
`No module named 'backend'`. The bare `models.*` root fails with `No module named 'models'`.

### Three test imports that are path-dependent rather than absent

`backend/tests/test_services.py:L3-L5` imports three `services.*` modules, and those three files do
exist. Grouping them with the six rows above overstates the problem, so this register keeps them
apart. Two separate conditions have to hold before one of them loads.

| Import specifier | The file behind it | Discoverable when | What stops it next |
| ------------------ | -------------------- | ------------------- | -------------------- |
| `services.document_service` | `backend/app/services/document_service.py` | `backend/app/` sits on the import path, because `services/` holds no `__init__.py` and acts as an implicit namespace package | Execution needs `backend/` on the path too, for the `app.*` imports. `document_service.py:L16` imports `app.db.firestore`, and `backend/app/db/firestore.py:L16` requests the absent `settings` name. The module also requests it directly at `L17` |
| `services.collaboration_service` | `backend/app/services/collaboration_service.py` | The same condition | `collaboration_service.py:L18` requests `settings` directly |
| `services.export_service` | `backend/app/services/export_service.py` | The same condition | `export_service.py:L16` requests `settings` directly |

No single import path satisfies every root at once. `backend/app/` makes the three `services.*`
specifiers discoverable, `backend/` makes `app.*` resolvable, and the repository root makes neither.
From the repository root, `python -m pytest backend/tests` therefore stops at three different lines:
`test_api.py:L3` with `No module named 'app'`, `test_db.py:L6` with `No module named 'backend.db'`,
and `test_services.py:L3` with `No module named 'services'`.

The test modules also call methods no committed class defines, including `set_password` and
`get_token` at `backend/tests/test_api.py:L19` and `:L36`. The fixture at
`backend/tests/test_api.py:L11-L14` has a bare `pass` for a body, so any test depending on it
receives `None` rather than a session. See
[../backend/tests/README.md](../backend/tests/README.md), which also records that these three
files receive no inline documentation.

## G2 absent symbols inside modules that do exist

The modules below load, or would load, and the names other files request from them are not there.
Absent symbols cause more failures in this repository than absent modules do, and one of them
accounts for nine module import failures on its own.

### The absent `settings` singleton

`backend/app/core/config.py` defines a `Settings` class at `L20` and a `get_settings()` factory at
`L61`, and it never creates a module-level `settings` instance. The file contains no `settings =`
assignment at any line. Eight modules import that name:

| Importing module | Line |
| ------------------ | ------ |
| `backend/app/main.py` | `L20` |
| `backend/app/api/auth.py` | `L19` |
| `backend/app/db/firestore.py` | `L16` |
| `backend/app/db/sql.py` | `L14` |
| `backend/app/services/collaboration_service.py` | `L18` |
| `backend/app/services/document_service.py` | `L17` |
| `backend/app/services/export_service.py` | `L16` |
| `backend/app/tasks/background_tasks.py` | `L16` |

Each import raises `ImportError: cannot import name 'settings' from 'app.core.config'`.
`backend/app/core/security.py:L20` imports `get_settings` instead, which exists, so that module's
configuration import resolves. [G3](#g3-undefined-names-that-raise-at-execution) records why
`app.core.security` still fails.

### The verified import census

The census imported each of the 15 modules under `backend/app/` in a fresh interpreter, with
third-party packages present and Pydantic pinned to the 1.x line the code requires. The result:
**3 modules import successfully and 12 fail.**

| Outcome | Modules |
| --------- | --------- |
| Imports (3) | `app.core.config`, `app.schema.document`, `app.schema.user` |
| Fails (12) | `app.main`, `app.api.auth`, `app.api.documents`, `app.api.templates`, `app.api.users`, `app.core.security`, `app.db.firestore`, `app.db.sql`, `app.services.collaboration_service`, `app.services.document_service`, `app.services.export_service`, `app.tasks.background_tasks` |

The 12 failures resolve to three distinct causes, so repairing one name clears three quarters of
them:

| Cause | Count | Modules affected |
| ------- | ------- | ------------------ |
| The absent `settings` singleton | 9 | `app.main`, `app.api.auth`, `app.api.documents`, `app.db.firestore`, `app.db.sql`, `app.services.collaboration_service`, `app.services.document_service`, `app.services.export_service`, `app.tasks.background_tasks` |
| An absent module, per [G1](#g1-absent-modules-referenced-by-committed-code) | 2 | `app.api.templates` (`app.schema.template`), `app.api.users` (`app.services.user_service`) |
| An undefined name, per [G3](#g3-undefined-names-that-raise-at-execution) | 1 | `app.core.security` (`Optional`) |

`app.main` surfaces its failure at `backend/app/api/auth.py:L19`, reached through
`backend/app/main.py:L16`. Two modules fail indirectly through the Firestore adapter:
`app.api.documents` and `app.services.document_service` both surface at
`backend/app/db/firestore.py:L16`. See [../backend/app/README.md](../backend/app/README.md), which
owns the census figure and the package-boundary statement.

### The four router names

`backend/app/main.py:L16-L19` imports `auth_router`, `documents_router`, `users_router` and
`templates_router`. All four router modules export the bare name `router` instead.

| Requested name | Requested at | Provided name |
| ---------------- | -------------- | --------------- |
| `auth_router` | `backend/app/main.py:L16` | `router` in `backend/app/api/auth.py` |
| `documents_router` | `backend/app/main.py:L17` | `router` in `backend/app/api/documents.py` |
| `users_router` | `backend/app/main.py:L18` | `router` in `backend/app/api/users.py` |
| `templates_router` | `backend/app/main.py:L19` | `router` in `backend/app/api/templates.py` |

All four names are then passed to `include_router` at `backend/app/main.py:L84-L87`.

### Absent methods on classes that exist

| Symbol | Called at | Defined on |
| -------- | ----------- | ------------ |
| `DocumentService.get_documents` | `backend/app/api/documents.py:L65` | nothing. `DocumentService` defines `create_document` at `backend/app/services/document_service.py:L42`, `get_document` at `:L78`, `update_document` at `:L116` and `delete_document` at `:L159` |
| `ExportService.convert_document` | `backend/app/tasks/background_tasks.py:L59` | nothing. `ExportService` defines `export_to_pdf` (`L40`) and `export_to_docx` (`L74`) |

### Absent frontend exports

`frontend/src/schema/document.ts` omits **three requested names**, not one. Consumers ask for
`Document`, `DocumentCreate` and `DocumentUpdate` across five positions, and the module declares none
of the three. Its two exports are both Zod schema values, `DocumentSchema` at `L23` and
`DocumentVersionSchema` at `L39`, and it exports **no inferred type**. Both sibling schema modules do
export one: `frontend/src/schema/user.ts:L30` and `frontend/src/schema/template.ts:L31` each end with
a `z.infer` declaration. The three omissions together produce five of the six `TS2305` errors in the
whole frontend, because the compiler reports one error per requested name per import statement.

| Requested name | Requested at | Positions | What closing it needs |
| ---------------- | -------------- | ----------- | ------------------------ |
| `Document` | `frontend/src/services/api.ts:L19`, `frontend/src/services/collaboration.ts:L17`, `frontend/src/store/documentSlice.ts:L15` | 3 | One line. `DocumentSchema` already exists at `frontend/src/schema/document.ts:L23`, so a `z.infer` export beside it closes all three positions at once |
| `DocumentCreate` | `frontend/src/services/api.ts:L19` | 1 | A schema first. No Zod object in the module models a creation payload, so nothing exists to infer from. `backend/app/schema/document.py:L30` declares the server-side equivalent |
| `DocumentUpdate` | `frontend/src/services/api.ts:L19` | 1 | A schema first. `backend/app/schema/document.py:L39` declares the server-side equivalent and inherits nothing, so neither side holds a field list to mirror |

| Requested symbol | Requested at |
| ------------------ | -------------- |
| `Document`, `DocumentCreate`, `DocumentUpdate` | `frontend/src/services/api.ts:L19` |
| `Document` | `frontend/src/services/collaboration.ts:L17` |
| `Document` | `frontend/src/store/documentSlice.ts:L15` |

`frontend/src/store/index.ts` omits two hooks that seven modules import, and registers neither of
two named exports its consumers expect:

| Absent symbol | Expected from | Requested at |
| --------------- | --------------- | -------------- |
| `useAppSelector`, `useAppDispatch` | `frontend/src/store/index.ts` | seven modules across the four pages and three components |
| `documentReducer` | `frontend/src/store/documentSlice.ts` | `frontend/src/store/index.ts:L15`. The slice exports its reducer as the module default at `frontend/src/store/documentSlice.ts:L93` |
| `userReducer` | `frontend/src/store/userSlice.ts` | `frontend/src/store/index.ts:L16`. The slice exports its reducer as the module default at `frontend/src/store/userSlice.ts:L76` |
| `updateDocument`, `selectCurrentDocument` | `frontend/src/store/documentSlice.ts` | `frontend/src/components/DocumentCanvas.tsx:L17`, `frontend/src/components/Toolbar.tsx:L17`. The slice exports exactly six actions at `frontend/src/store/documentSlice.ts:L84-L91`, and `updateDocument` is not among them |
| `updateUser`, `selectCurrentUser` | `frontend/src/store/userSlice.ts` | `frontend/src/pages/Settings.tsx:L16`, plus `selectCurrentUser` at `frontend/src/components/Header.tsx:L10`, `frontend/src/pages/Home.tsx:L15` and `frontend/src/pages/Templates.tsx:L16`. The slice exports `setUser`, `clearUser`, `setLoading` and `setError` at `frontend/src/store/userSlice.ts:L75` |
| `getDocument`, `updateUserSettings` | `frontend/src/services/api.ts` | `frontend/src/pages/Editor.tsx:L16` and `frontend/src/pages/Settings.tsx:L14`. The module exports only `getDocuments` (`frontend/src/services/api.ts:L69`), `createDocument` (`:L81`) and `updateDocument` (`:L94`) |
| `getTemplates` | `frontend/src/services/api.ts` | `frontend/src/pages/Templates.tsx`. No template request function exists in the client |
| `Switch` | `react-router-dom` | `frontend/src/App.tsx:L12`. Version 6 removed `Switch`, and `frontend/package.json:L11` pins `^6.11.1` |

`createApiClient` at `frontend/src/services/api.ts:L31` carries no `export` keyword, so the
factory is module-private and only the local `api` instance at `L61` consumes it.

See [../frontend/src/schema/README.md](../frontend/src/schema/README.md),
[../frontend/src/store/README.md](../frontend/src/store/README.md) and
[../frontend/src/services/README.md](../frontend/src/services/README.md).

## G3 undefined names that raise at execution

Seven references across six distinct names have no import behind them. Reading the import block at
the top of each file will not reveal any of them, which is what makes this class expensive to
diagnose. The name looks ordinary at the point of use, and the failure arrives later.

| Name | Referenced at | Raises when |
| ------ | --------------- | ------------- |
| `Optional` | `backend/app/core/security.py:L25`, in the `create_access_token` signature | the module body executes, so at import |
| `User` | `backend/app/core/security.py:L119`, as the `get_current_user` return annotation | the module body executes, so at import |
| `UserService` | `backend/app/core/security.py:L159`, inside `get_current_user` | `get_current_user` first runs |
| `asyncio` | `backend/app/services/collaboration_service.py:L97`, inside the Pub/Sub `callback` | a published message first arrives |
| `json` | `backend/app/services/collaboration_service.py:L156`, inside `broadcast_change` | `broadcast_change` first runs |
| `datetime` | `backend/app/tasks/background_tasks.py:L96`, inside `cleanup_expired_documents` | the retention sweep first runs |
| `datetime` | `backend/app/tasks/background_tasks.py:L146`, inside `update_document_statistics` | the statistics task first runs |

`backend/app/tasks/background_tasks.py:L20` imports `timedelta` alone, so `timedelta` resolves at
both `L67` and `L72` while `datetime` resolves nowhere.

### Two of the seven raise at import, not at execution

Python evaluates a function's annotations when the `def` statement runs, so an undefined name in a
signature fails as the module loads rather than when the function is called. `Optional` at
`backend/app/core/security.py:L25` therefore raises
`NameError: name 'Optional' is not defined` during import of `app.core.security`, and the module
cannot import at all. `User` at `L90` would raise the same way, and `L25` raises first, so
execution never reaches it.

The remaining five references sit inside function bodies and raise only when that function runs.
The register states the mechanism because the two cases need different diagnosis: a signature
failure appears in an import traceback, and a body failure appears only under exercise.

### Two findings in this file that are not defects

Diagnosing `backend/app/core/security.py` goes wrong in two predictable ways, so this register
records both explicitly.

- **`backend/app/core/security.py:L20` imports `get_settings`, not `settings`.** That name exists,
  at `backend/app/core/config.py:L61`. The configuration import in this one module resolves
  correctly, unlike the eight listed in
  [G2 settings singleton](#the-absent-settings-singleton). The real defects in this file are the three undefined names
  above.
- **`except jwt.JWTError` at `backend/app/core/security.py:L156` resolves correctly and is not a
  defect.** `L16` imports `jwt` from `jose`, and the installed `python-jose` distribution exposes
  `JWTError` on that module. Recording the line as broken would send a reader after a working
  import.

See [../backend/app/core/README.md](../backend/app/core/README.md),
[../backend/app/services/README.md](../backend/app/services/README.md) and
[../backend/app/tasks/README.md](../backend/app/tasks/README.md).

## G4 undeclared third-party dependencies

The frontend needs five packages its manifest does not declare, and the backend has no manifest
at all.

### Five npm packages the manifest omits

`frontend/package.json:L6-L14` declares exactly seven runtime dependencies: `@reduxjs/toolkit`,
`react`, `react-dom`, `react-redux`, `react-router-dom`, `tailwindcss` and `typescript`. Five
packages are missing from that manifest, and four of the five are named by an import statement.

| Package | Importing modules | Sample locator |
| --------- | ------------------- | ---------------- |
| `draft-js` | 6 | `frontend/src/utils/documentUtils.ts:L14`, `frontend/src/utils/formatting.ts:L14`, `frontend/src/components/DocumentCanvas.tsx:L15` |
| `zod` | 4 | the three modules under `frontend/src/schema/`, for example `frontend/src/schema/document.ts:L13`, plus `frontend/src/utils/validation.ts:L13` |
| `axios` | 2 | `frontend/src/services/api.ts:L17`, `frontend/src/services/auth.ts:L16` |
| `socket.io-client` | 1 | `frontend/src/services/collaboration.ts:L15` |

**One is a required type package with no direct import.** `@types/draft-js` appears in zero import
statements anywhere in `frontend/src/`, and it is absent from `devDependencies` at
`frontend/package.json:L15-L30`. The six `draft-js` importers need it to typecheck, because
`draft-js` ships no bundled type declarations. No grep of the source finds it. A developer who derives
the dependency set from import statements alone therefore omits it, and meets a fresh error class
after installing the other four.

`npm install` inside `frontend/` succeeds and installs none of the five, because a package manager
installs what a manifest declares. One observed run on Node 14 resolved 1,532 packages, and with no
lockfile committed that figure is a single observation rather than a repeatable result. The four
packages an import statement names contribute 13 of the 57 `TS2307` errors: six for `draft-js`, four
for `zod`, two for `axios` and one for `socket.io-client`.

### The backend has no dependency manifest

No `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `tox.ini`, `Pipfile` or
`.python-version` exists anywhere in the repository. Two committed instructions install from a file
that was never added: `../README.md:L42` and `scripts/setup_dev_environment.sh:L26` both run
`pip install -r requirements.txt`, and
`infrastructure/docker/backend.Dockerfile:L8` copies `requirements.txt` into the image before
`L11` installs from it.

A developer must infer the dependency set from import statements. Seven third-party root modules
appear across `backend/app/`:

| Import root | Distribution supplying it | Established by |
| ------------- | --------------------------- | ---------------- |
| `fastapi` | `fastapi`, 0.89.0 or newer | Response models come from return annotations, and no handler passes `response_model=` |
| `pydantic` | `pydantic`, 1.x only | `backend/app/core/config.py:L17` imports `BaseSettings` from the main package, and `backend/app/schema/user.py:L81` sets `orm_mode`. Pydantic 2 moved `BaseSettings` to `pydantic-settings` and renamed `orm_mode` |
| `sqlalchemy` | `SQLAlchemy`, 1.4 or newer | `backend/app/db/sql.py:L13` imports `declarative_base` from `sqlalchemy.orm`, where 1.4 moved it |
| `jose` | `python-jose` | `backend/app/api/auth.py` and `backend/app/core/security.py:L16`. The import name and the distribution name differ |
| `passlib` | `passlib` | `CryptContext` in the same two modules |
| `celery` | `celery` | `backend/app/tasks/background_tasks.py:L22` |
| `google` | `google-cloud-firestore`, `google-cloud-pubsub`, `google-cloud-storage` and `google-auth` | one namespace splits across four distributions: `google.cloud.firestore`, `google.cloud.pubsub_v1`, `google.cloud.storage` and `google.auth` |

### The progressive Python dependency-resolution failure

The backend requires seventeen distributions to run, and only ten of them appear in an `import`
line. [../backend/app/README.md](../backend/app/README.md) defines that count and the categories
behind it, and every dependency figure in this document uses them. `uvicorn` is named by a run
command instead, at `infrastructure/docker/backend.Dockerfile:L20` and `../README.md:L55`. The
remaining six divide two ways.

Four arrive transitively and need no naming: `starlette` with `fastapi`, and `ecdsa`, `rsa` and
`pyasn1` with `python-jose`. Two do not arrive at all: `bcrypt` and `python-multipart` are runtime
backends that nothing declares, so thirteen of the seventeen have to be named to a package manager.
A developer building an environment by reading import statements installs the visible packages,
retries, and hits the next missing piece. The build fails progressively rather than once. Four
properties of this repository cause that pattern:

- **One import name does not match its distribution name.** `import jose` needs `python-jose`.
  Guessing `pip install jose` installs an unrelated package, and the real one pulls `ecdsa`, `rsa` and
  `pyasn1` along with it, so a key-format error can name a package no committed line mentions.
- **One namespace maps to four distributions.** `from google.cloud... import` gives no hint that
  Firestore, Pub/Sub, Cloud Storage and authentication ship separately.
- **Two runtime needs are declared by nothing, and one of them is not fixed by installing it.**
  `passlib` performs bcrypt hashing at `backend/app/api/auth.py:L24` and does not depend on
  `bcrypt`, so password hashing fails until a developer adds `bcrypt` by hand. Adding the current
  release does not clear it, because passlib 1.7.4 cannot drive bcrypt 5.0.0, and
  [the pairing subsection](#the-passlib-and-bcrypt-pairing-decides-whether-any-password-can-be-hashed)
  sets out why. FastAPI parses the form body at `backend/app/api/auth.py:L66` through
  `python-multipart` and does not require it, so a login post fails the same way.
- **Two version ceilings are invisible without reading the code.** Installing the current
  `pydantic` breaks `backend/app/core/config.py:L17` immediately, because the 1.x constraint lives
  in an import statement rather than in a manifest.

Four more distributions sit outside the seventeen, because a configuration value rather than a
committed line makes each one necessary. `psycopg2-binary` arrives once the Cloud SQL path is
exercised, and `redis` once a Celery worker attaches. `cryptography` arrives once
`settings.ALGORITHM` names an RSA or ECDSA algorithm, and `python-dotenv` once a `.env` file exists
where the backend process starts.

The last of the four hides itself twice over. Pydantic 1.x requires a separate install to read the
`Config.env_file` value at `backend/app/core/config.py:L58`. That read happens only when the
named file is found, so an absent `.env` conceals the absent distribution until the file is created.
[onboarding.md](onboarding.md#setting-up-the-backend) states the condition for each.

[onboarding.md](onboarding.md) records the working package set for a first-time environment build.

### The dated dependency and advisory register

Compiled 8 August 2026. Every advisory identifier, version floor and runtime-support fact in this
documentation set lives in this one table. Decision row 18 in
[decision-log.md](decision-log.md#the-decision-table) records why. An advisory ages faster than the
code it describes, so a source comment would go stale silently while a dated table announces its own
age. No docstring, no JSDoc block and no `#` comment in the repository names an advisory, a version
floor or a date.

Read the table as a snapshot, not as a clearance. The repository pins nothing, so no row states what
a deployment would install. Each row states what the code requires and which published advisories
reach a release the code could load. The last two columns then ask whether a fixed release installs
on the Python version the repository documents. Runtime support comes from each release's own
`Requires-Python` metadata.

Two tables follow, because this repository needs 47 distributions in total. Of those, 21 are
declared in `../frontend/package.json`, 5 are imported by the frontend and declared nowhere, and 17
are required by the backend. A configuration value rather than a committed line makes the last 4
necessary. The first table is **risk-based** and carries only the distributions where a published
advisory reaches a release this code could load. The second is the **complete inventory** of all 47.

Every one of the 47 distributions was queried against its ecosystem's published advisory database.
Absence from the risk table therefore reports a result rather than a gap. The inventory carries the
verdict for every row, and decision row 21 in
[decision-log.md](decision-log.md#the-decision-table) records why the register is split in two.

**Risk table.** Thirteen rows, all PyPI. Eleven carry a published advisory that reaches a release this
code could load. The remaining two, `bcrypt` and `passlib`, carry no advisory and appear for a
different reason. The pair decides what registration does at `../backend/app/api/auth.py:L139`, and
neither current release works with the other.

The four npm distributions that carry an advisory sit below the inventory, because these columns ask a
Python question.

| Distribution | What the code requires | Advisories reaching a loadable release | Highest release installable on Python 3.9 | Fixed release reachable on 3.9 |
| --- | --- | --- | --- | --- |
| `python-jose` | Any release exposing `jwt` and `JWTError`, imported at `../backend/app/core/security.py:L16` | [CVE-2024-33663](https://github.com/advisories/GHSA-6c5p-j8vq-pqhj) algorithm confusion with OpenSSH ECDSA and other key formats, and [CVE-2024-33664](https://github.com/advisories/GHSA-cjwg-qfpm-7377) resource exhaustion decoding a compressed JWE token. Both fixed in 3.4.0. [CVE-2016-7036](https://github.com/advisories/GHSA-w799-prg3-cx77) non-constant-time HMAC comparison, fixed in 1.3.2 | 3.5.0, whose metadata requires Python 3.9 or newer | Yes. 3.4.0 and 3.5.0 both install |
| `pydantic` | 1.x only. `../backend/app/core/config.py:L17` imports `BaseSettings` from the main package and `../backend/app/schema/user.py:L81` sets `orm_mode`, both of which Pydantic 2 moved or renamed | [CVE-2024-3772](https://github.com/advisories/GHSA-mr82-8j83-vxmv) regular-expression denial of service, fixed in 1.10.13 on the 1.x line. [CVE-2021-29510](https://github.com/advisories/GHSA-5jqp-qgf6-3pvh) infinite loop on an `infinity` date input, fixed in 1.8.2 | The 1.10 series, whose metadata requires Python 3.7 or newer | Yes. `>=1.10.13,<2` satisfies both advisories and keeps 1.x |
| `python-multipart` | Any release FastAPI can use to parse the form body at `../backend/app/api/auth.py:L66` | Nine advisories, fixed across 0.0.7, 0.0.18, 0.0.22, 0.0.26, 0.0.27, 0.0.30 for three of them, and 0.0.31 | 0.0.20. Every release from 0.0.21 onward requires Python 3.10 or newer | **No.** 0.0.20 carries the two earliest fixes and none of the seven from 0.0.22 onward |
| `celery` | Any release exposing `Celery`, imported at `../backend/app/tasks/background_tasks.py:L14` | Two advisories. [CVE-2021-23727](https://github.com/advisories/GHSA-q4xr-rc97-m4xx) command injection through a stored result, fixed in 5.2.2. [CVE-2011-4356](https://github.com/advisories/GHSA-rpc6-h455-3rx5) local privilege escalation, fixed in 2.2.8, 2.3.4 and 2.4.4 | 5.6.3, whose metadata requires Python 3.9 or newer | Yes. Every release from 5.2.2 onward carries both fixes and installs |
| `bcrypt` | A release `passlib` can actually drive as its bcrypt backend, configured at `../backend/app/core/security.py:L22`. Current 5.0.0 is not such a release, so this row states a compatibility requirement rather than a version floor | None recorded against the distribution. Two separate behaviour facts decide the contract. bcrypt reads at most 72 bytes, and 5.0.0 raises where earlier releases truncated. Passlib 1.7.4 cannot initialise a 5.0.0 backend at all, which [the pairing subsection](#the-passlib-and-bcrypt-pairing-decides-whether-any-password-can-be-hashed) sets out. The docstrings record both, at `../backend/app/core/security.py:L91-L97` and `:L106-L111` | 5.0.0, whose metadata requires Python 3.8 or newer | Not applicable |
| `starlette` | Any release `fastapi` depends on. Arrives transitively and is named by no committed line | Ten advisories, the largest set on any backend row. Five are fixed at or below 0.49.3: [CVE-2023-30798](https://github.com/advisories/GHSA-74m5-2c7w-9w3x) in 0.25.0, [CVE-2023-29159](https://github.com/advisories/GHSA-v5gw-mw7f-84px) in 0.27.0, [CVE-2024-47874](https://github.com/advisories/GHSA-f96h-pmfr-66vw) in 0.40.0, [CVE-2025-54121](https://github.com/advisories/GHSA-2c2j-9gv5-cj73) in 0.47.2 and [CVE-2025-62727](https://github.com/advisories/GHSA-7f5h-v6xp-fcq8) in 0.49.1. Five are fixed only above it: [CVE-2026-48710](https://github.com/advisories/GHSA-86qp-5c8j-p5mr) in 1.0.1, [CVE-2026-48817](https://github.com/advisories/GHSA-x746-7m8f-x49c) and [CVE-2026-48818](https://github.com/advisories/GHSA-wqp7-x3pw-xc5r) in 1.1.0, [CVE-2026-54282](https://github.com/advisories/GHSA-jp82-jpqv-5vv3) in 1.3.0 and [CVE-2026-54283](https://github.com/advisories/GHSA-82w8-qh3p-5jfq) in 1.3.1. The 1.0.1 fix stops an unvalidated `Host` header poisoning `request.url.path` past a path-based check, and the 1.3.1 fix, rated 7.5, stops `request.form()` ignoring its own body limits. That last precondition is met by committed code: `../backend/app/api/auth.py:L66` parses exactly that body type through `OAuth2PasswordRequestForm`, on a public route | 0.49.3, because 1.0.1 and every later release require Python 3.10 or newer | **No, for five of the ten.** Every fix from 1.0.1 onward is unreachable on Python 3.9 |
| `ecdsa` | Any release `python-jose` depends on. Arrives transitively and is named by no committed line | Four advisories. Three are fixed at or below 0.19.2: [CVE-2019-14853](https://github.com/advisories/GHSA-pwfw-mgfj-7g3g) and [CVE-2019-14859](https://github.com/advisories/GHSA-8qxj-f9rh-9fg2) in 0.13.3, and [CVE-2026-33936](https://github.com/advisories/GHSA-9f5j-8jwj-x28g) in 0.19.2. That third one is where `remove_octet_string()` accepts a DER length longer than the buffer, so `SigningKey.from_der()` raises `IndexError` instead of rejecting the input. No committed line calls `from_der`, so that third precondition rests on `python-jose` rather than on this repository. The fourth is [CVE-2024-23342](https://github.com/advisories/GHSA-wj6h-64fc-37mp), the Minerva timing attack on the P-256 curve, which reaches signing, key generation and key exchange, leaves signature verification unaffected, and has no planned fix | 0.19.2 | **Mixed.** All three fixed advisories are reachable at 0.19.2. Minerva has no fix anywhere. Its precondition is an elliptic-curve `ALGORITHM` value. `backend/app/core/config.py:L44` declares `ALGORITHM: str` with no committed value, no default, no validator and no allowed-value list, so the algorithm a deployment would select is unestablished rather than excluded |
| `pyasn1` | Any release `python-jose` depends on, by way of `rsa`. Arrives transitively and is named by no committed line | Five advisories, each rated 7.5 and each a denial of service in the BER, CER and DER codecs. [CVE-2026-23490](https://github.com/advisories/GHSA-63vm-454h-vhhq) memory exhaustion from a malformed RELATIVE-OID, fixed in 0.6.2. [CVE-2026-30922](https://github.com/advisories/GHSA-jr27-m4p2-rc6r) unbounded recursion, fixed in 0.6.3. Then three published together on 21 July 2026, all fixed in 0.6.4. They are [CVE-2026-59884](https://github.com/advisories/GHSA-m4p7-r5rc-7g4j) unbounded long-form tag identifiers, [CVE-2026-59885](https://github.com/advisories/GHSA-8ppf-4f7h-5ppj) quadratic OBJECT IDENTIFIER and RELATIVE-OID processing, and [CVE-2026-59886](https://github.com/advisories/GHSA-hm4w-wwcw-mr6r) uncontrolled consumption converting a decoded REAL value | 0.6.4 | **Yes.** 0.6.4 carries all five fixes and installs on Python 3.9 |
| `passlib` | Any release exposing `CryptContext`, imported at `../backend/app/core/security.py:L17` | None recorded against the distribution. The distribution's last release is 1.7.4, dated 8 October 2020, and its bcrypt backend cannot drive bcrypt 5.0.0. [The pairing subsection](#the-passlib-and-bcrypt-pairing-decides-whether-any-password-can-be-hashed) carries the mechanism and the two ways out | 1.7.4, which declares no Python floor | Not applicable |
| `rsa` | Any release `python-jose` depends on for RSA key handling. Arrives transitively and is named by no committed line | Three advisories: [CVE-2016-1494](https://github.com/advisories/GHSA-8rjr-6qq5-pj9p) signature spoofing, fixed in 3.3; [CVE-2020-13757](https://github.com/advisories/GHSA-537h-rv9q-vvph) denial of service decrypting a crafted ciphertext, fixed in 4.1; and [CVE-2020-25658](https://github.com/advisories/GHSA-xrx6-fmxq-rjj2) a Bleichenbacher timing attack, fixed in 4.7 | 4.9.1 | **Yes.** 4.9.1 carries all three fixes. The precondition for the timing attack is an RSA `ALGORITHM` value, which no committed file selects |
| `redis` | Any release a Celery worker could use against the `REDIS_URL` declared at `../backend/app/core/config.py:L47`. No committed line imports it | Two advisories, both a race condition where a cancelled command leaks its response to the next caller on the same connection. [CVE-2023-28858](https://github.com/advisories/GHSA-24wv-mv5m-xv4h) is fixed in 4.3.6, 4.4.3 and 4.5.3. [CVE-2023-28859](https://github.com/advisories/GHSA-8fww-64cx-x8p5), the follow-up for an incomplete first fix, is fixed in 4.4.4 and 4.5.4 | 7.0.1 | **Yes.** 7.0.1 carries both fixes. The precondition needs `asyncio` cancellation against a live broker, and Compose declares no Redis service while Terraform declares no Memorystore instance |
| `cryptography` | Any release `python-jose` can use once `settings.ALGORITHM` names an RSA or ECDSA algorithm. No committed line imports it | Twenty-four advisories, the longest history in this register, spanning 2018 to 2026. Every fix lands at or below 50.0.0. The three most recent were published together on 3 August 2026: [CVE-2026-69247](https://github.com/advisories/GHSA-g6cj-pr64-35w5), fixed in 50.0.0, and [CVE-2026-69248](https://github.com/advisories/GHSA-m2h6-j472-rp4c) with [CVE-2026-69249](https://github.com/advisories/GHSA-jwv3-5hgf-82ww), both fixed in 49.0.0 | Depends on the patch level. 50.0.0 declares `!=3.9.0,!=3.9.1,>=3.9`, so a 3.9.2 interpreter reaches it while a 3.9.0 or 3.9.1 interpreter is capped at 43.0.3 | **Yes on Python 3.9.2 or newer.** On 3.9.0 or 3.9.1 the 43.0.3 ceiling misses ten fixes, including all three from August 2026 |
| `python-dotenv` | Any release Pydantic 1.x can use to read the `Config.env_file` value at `../backend/app/core/config.py:L58`. Loaded only when that file exists | [CVE-2026-28684](https://github.com/advisories/GHSA-mf9w-mj56-hr94), symlink following in `set_key` that overwrites an arbitrary file through a cross-device rename fallback, fixed in 1.2.2 | 1.2.1, because 1.2.2 requires Python 3.10 or newer | **No.** The fix is unreachable on Python 3.9. The precondition is a call to `set_key`, and no committed line writes a `.env` file: this repository only ever reads one |

Three rows carry a fix that Python 3.9 cannot reach, and together they hold the register's sharpest
finding. `python-multipart` is capped at 0.0.20 while seven of its nine advisories are fixed only from
0.0.22 onward. `starlette` is capped at 0.49.3 while five of its ten are fixed only from 1.0.1
onward. `python-dotenv` is capped at 1.2.1 while its one advisory is fixed in 1.2.2. Choosing the
runtime the repository documents therefore forecloses thirteen fixes across the three.

The three declarations that document Python 3.9 are `infrastructure/docker/backend.Dockerfile:L2`,
`../README.md:L23`, which asks for 3.8 or later, and `scripts/setup_dev_environment.sh`, which pins
nothing. Moving to Python 3.10 or newer is the only route to all thirteen. That move does not collide
with the Pydantic 1.x requirement, because the 1.10 series supports Python 3.10 as well.

Two limits on this table. Whether any advisory is exploitable in this repository depends on values no
committed file supplies, and each entry below states its own preconditions. The advisory set also
grows, so a reader repairing this repository should re-query rather than trust the date above.

#### The passlib and bcrypt pairing decides whether any password can be hashed

Two rows above carry no advisory and still decide the outcome of registration and login.
`../backend/app/core/security.py:L22` and `../backend/app/api/auth.py:L24` each build a passlib
`CryptContext` with the bcrypt scheme, so every hash and every verify reaches bcrypt through passlib.
No manifest pins either distribution, which leaves the pair to whatever `pip install passlib bcrypt`
resolves on the day.

Two behaviour facts apply, and reading either one alone produces a wrong contract.

1. **bcrypt's own limit.** bcrypt reads at most 72 bytes of a password. Releases before 5.0.0
   truncate a longer password, so two passwords sharing a 72-byte prefix produce interchangeable
   hashes. Release 5.0.0, dated 25 September 2025, raises `ValueError` instead of truncating.
2. **passlib cannot drive bcrypt 5.0.0.** The last passlib release is 1.7.4, dated 8 October 2020.
   Its bcrypt backend reads `bcrypt.__about__.__version__`, which no release from 4.1.0 onward
   provides, and then probes the backend for a historical wraparound bug by hashing a 255-byte test
   secret. bcrypt 5.0.0 rejects that 255-byte probe, the `ValueError` escapes backend
   initialisation, and passlib does not cache the failed probe.

The consequence is the one a reader needs before touching either route. With passlib 1.7.4 and
bcrypt 5.0.0 installed, **every** `CryptContext.hash` and `CryptContext.verify` call raises
`ValueError`, including a five-byte password. The message reads `password cannot be longer than 72
bytes, truncate manually if necessary (e.g. my_password[:72])`. That limit is one the submitted
password never reaches, so the error misdescribes its own cause and sends a reader hunting for a long
password that does not exist.

| Pair installed | `hash("short")` | A password over 72 bytes | What a reader sees besides |
| --- | --- | --- | --- |
| passlib 1.7.4 with bcrypt 5.0.0 | Raises `ValueError` naming the 72-byte limit | Raises the same `ValueError` | A logged warning, `(trapped) error reading bcrypt version`, from the absent `__about__` attribute |
| passlib 1.7.4 with bcrypt 4.3.0 | Returns a `$2b$` hash | Truncates silently at 72 bytes | The same logged warning, which is cosmetic here |
| passlib 1.7.4 with bcrypt 4.0.1 | Returns a `$2b$` hash | Truncates silently at 72 bytes | No warning, because 4.0.1 still exposes `__about__` |

Both bcrypt rows above were observed directly on Python 3.11 against the committed
`CryptContext(schemes=['bcrypt'], deprecated='auto')` construction.

Two routes out exist, and each is a code or dependency change that this documentation pass does not
make. The narrow one pins a bcrypt release passlib can drive, which makes the diagnostic commands in
[onboarding.md](onboarding.md#setting-up-the-backend) work and leaves silent truncation in place. The
durable one replaces the wrapper, because passlib has published nothing for over five years. Two
maintained replacements exist. `libpass` 1.9.3 is a fork exposing the same `CryptContext` API, and
`pwdlib` 0.3.0 with `argon2-cffi` 25.1.0 is the path a new service would take.

Whichever route a maintainer picks, `../backend/app/schema/user.py:L38` still bounds no password
length, so entry 4 in [G9](#g9-absent-security-controls) stays open either way.

#### The complete distribution inventory

All 47 distributions, so no dependency of this repository goes unlisted. Every row was queried
individually, and the Advisory status column says one of three things.

**Risk table** means an advisory reaches a release this code could load and the table above carries
the detail. **None recorded** means the query returned nothing. **Fixes precede the floor** means
advisories exist but every one is fixed below the lowest release this code can use, so no unpinned
install can land on an affected release.

The three verdicts partition the inventory exactly. 27 of the 47 distributions have no recorded
advisory, 5 have only advisories fixed below their floor, and 15 carry an advisory that reaches a
release this code could load. `passlib` and `bcrypt` fall in the first group and still appear in the
risk table, for the pairing reason stated above it.

The Reachability column gives the highest release installable on Python 3.9 for every PyPI row, taken
from each release's own `Requires-Python` metadata. The npm rows state the declared range instead,
because no committed file pins a Node version that `npm` would enforce. One caveat bounds the npm
rows. The 21 declared and 5 undeclared packages are the ones this repository names, while `npm
install` resolves 1,532 packages in total. An advisory inside a transitive dependency of
`react-scripts` therefore sits outside this inventory.

| # | Distribution | Class | Declared range or inferred requirement | Advisory status | Reachability and the precondition that would make it matter |
| --- | --- | --- | --- | --- | --- |
| 1 | `@reduxjs/toolkit` | npm runtime, declared | `^1.9.5` | None recorded | Nothing loads it, because the client cannot build |
| 2 | `react` | npm runtime, declared | `^18.2.0` | Fixes precede the floor | React 18 is declared while `../frontend/src/index.tsx` uses the React 17 `ReactDOM.render` entry point. Both advisories are fixed at 0.14.0 and below, so `^18.2.0` is far past them |
| 3 | `react-dom` | npm runtime, declared | `^18.2.0` | Fixes precede the floor | As `react`. The one advisory is fixed at 16.4.2 and below, so `^18.2.0` is far past it |
| 4 | `react-redux` | npm runtime, declared | `^8.0.5` | None recorded | `Provider` is mounted twice, in `index.tsx` and again in `App.tsx` |
| 5 | `react-router-dom` | npm runtime, declared | `^6.11.1` | **Advisory reaches it.** See the npm row below | Highest 6.x is 6.30.4 and no 6.x release carries the patch. The precondition is an open redirect, and no redirect construct exists anywhere in `../frontend/src/` |
| 6 | `tailwindcss` | npm runtime, declared | `^3.3.2` | None recorded | No `tailwind.config.js`, no `postcss.config.js` and no stylesheet is committed, so no utility class compiles |
| 7 | `typescript` | npm runtime, declared | `^4.9.5` | None recorded | Declared as a runtime rather than a development dependency |
| 8 | `@testing-library/jest-dom` | npm dev, declared | `^5.16.5` | None recorded | No frontend test file is committed, so nothing consumes it |
| 9 | `@testing-library/react` | npm dev, declared | `^14.0.0` | None recorded | As row 8 |
| 10 | `@testing-library/user-event` | npm dev, declared | `^14.4.3` | None recorded | As row 8 |
| 11 | `@types/jest` | npm dev, declared | `^29.5.1` | None recorded | Types only, erased at compile time |
| 12 | `@types/node` | npm dev, declared | `^18.16.3` | None recorded | Types only. Declares Node 18 types against a documented Node 14 runtime |
| 13 | `@types/react` | npm dev, declared | `^18.2.0` | None recorded | Types only |
| 14 | `@types/react-dom` | npm dev, declared | `^18.2.1` | None recorded | Types only |
| 15 | `@typescript-eslint/eslint-plugin` | npm dev, declared | `^5.59.2` | None recorded | No workflow step runs a lint, so it never executes in automation |
| 16 | `@typescript-eslint/parser` | npm dev, declared | `^5.59.2` | None recorded | As row 15 |
| 17 | `eslint` | npm dev, declared | `^8.39.0` | None recorded | Configured inline in `../frontend/package.json` rather than in a config file, and never run by automation |
| 18 | `eslint-config-prettier` | npm dev, declared | `^8.8.0` | **Advisory reaches it.** See the npm table below | As row 17. The declared `^8.8.0` spans the malicious 8.10.1, and with no lockfile committed nothing pinned it out during the compromise window |
| 19 | `eslint-plugin-react` | npm dev, declared | `^7.32.2` | None recorded | As row 17 |
| 20 | `prettier` | npm dev, declared | `^2.8.8` | None recorded | No Prettier configuration file is committed, so the 100-character convention rests on the default |
| 21 | `react-scripts` | npm dev, declared | `5.0.1`, an exact pin | None recorded | Version 5 does not apply `tsconfig` `paths` to webpack resolution, which is why the `@/` prefix cannot be fixed in `tsconfig.json` alone |
| 22 | `axios` | npm, imported and declared nowhere | Any release exposing `AxiosInstance`, imported at `../frontend/src/services/api.ts:L15` and `auth.ts:L16` | **Advisory reaches it.** See the npm table below | Absent from the manifest, so `npm install` never fetches it and the import fails resolution. Nothing pins a version either, so an install by hand takes whatever is current |
| 23 | `draft-js` | npm, imported and declared nowhere | Any release exposing `EditorState`, `ContentState` and `RichUtils`. Imported by six modules | None recorded | As row 22 |
| 24 | `@types/draft-js` | npm, required by the compiler and declared nowhere. No module imports it | Types for the six Draft.js importers. TypeScript loads a package under `@types` from `node_modules` without an import statement, so this row is required rather than imported | None recorded | Absent from the manifest, so `npm install` never fetches it. Adding `draft-js` alone leaves every Draft.js import untyped, which turns row 23's resolution error into an implicit `any` |
| 25 | `zod` | npm, imported and declared nowhere | Any release exposing `z`. Imported by the three schema modules and `utils/validation.ts` | **Advisory reaches it.** See the npm table below | As row 22. An install by hand today resolves a 4.x release, which is past the one advisory |
| 26 | `socket.io-client` | npm, imported and declared nowhere | Any release exposing `io`, imported at `../frontend/src/services/collaboration.ts` | None recorded | As row 22. The server side declares a FastAPI `WebSocket` instead, so the two ends do not share a protocol |
| 27 | `fastapi` | PyPI, required | 0.89.0 or newer, because response models come from return annotations and no handler passes `response_model=` | Fixes precede the floor | 0.128.8 on Python 3.9. The one advisory is fixed in 0.65.2, below the 0.89.0 floor the response-model behaviour requires |
| 28 | `uvicorn` | PyPI, required | Any release able to serve `main:app`, named at `../infrastructure/docker/backend.Dockerfile:L20` | Fixes precede the floor | 0.39.0 on Python 3.9. Both advisories are fixed in 0.11.7, which every release able to serve `main:app` today is past |
| 29 | `starlette` | PyPI, required, transitive with `fastapi` | Whatever `fastapi` resolves | Risk table | 0.49.3 on Python 3.9. Five of the ten fixes land at 1.0.1 or above, and 1.0.1 needs Python 3.10, so those five are unreachable |
| 30 | `pydantic` | PyPI, required | 1.x only, fixed by the `BaseSettings` import at `../backend/app/core/config.py:L17` and `orm_mode` at `../backend/app/schema/user.py:L81` | Risk table | 2.13.4 installs on Python 3.9 but breaks both 1.x usages, so the ceiling is a code constraint rather than a runtime one |
| 31 | `python-jose` | PyPI, required | Any release exposing `jwt` and `JWTError` | Risk table | 3.5.0 on Python 3.9. The import name differs from the distribution name |
| 32 | `ecdsa` | PyPI, required, transitive with `python-jose` | Whatever `python-jose` resolves | Risk table | 0.19.2 on Python 3.9, which carries three of the four fixes. Minerva has none, and needs an elliptic-curve `ALGORITHM` that no committed file selects |
| 33 | `rsa` | PyPI, required, transitive with `python-jose` | Whatever `python-jose` resolves | Risk table | 4.9.1 on Python 3.9, which carries all three fixes |
| 34 | `pyasn1` | PyPI, required, transitive with `rsa` | Whatever `rsa` resolves | Risk table | 0.6.4 on Python 3.9, and all five fixes are reachable there |
| 35 | `passlib` | PyPI, required | Any release exposing `CryptContext` | None recorded | 1.7.4, dated 8 October 2020 and the last release, which declares no Python floor. Does not depend on `bcrypt`, which is why row 36 has to be installed by hand |
| 36 | `bcrypt` | PyPI, required, declared by nothing | A release `passlib` can actually drive, which excludes current 5.0.0 | None recorded | 5.0.0 on Python 3.9. Two facts combine. Release 5.0.0 raises `ValueError` above 72 bytes where earlier releases truncate, and passlib 1.7.4 cannot initialise a 5.0.0 backend at all, so every hash and verify raises. [The pairing subsection](#the-passlib-and-bcrypt-pairing-decides-whether-any-password-can-be-hashed) carries the mechanism, and entry 4 in G9.1 records what it means for registration |
| 37 | `python-multipart` | PyPI, required, declared by nothing | Any release FastAPI can use to parse the form body at `../backend/app/api/auth.py:L66` | Risk table | 0.0.20 on Python 3.9, and seven of the nine fixes land only from 0.0.22, which needs Python 3.10 |
| 38 | `google-cloud-firestore` | PyPI, required | Any release exposing `Client`, imported at `../backend/app/db/firestore.py` | None recorded | 2.27.0 on Python 3.9 |
| 39 | `google-cloud-storage` | PyPI, required | Any release exposing `Client`, used by the export path | None recorded | 3.9.0 on Python 3.9 |
| 40 | `google-cloud-pubsub` | PyPI, required | Any release exposing `PublisherClient` and `SubscriberClient` | None recorded | 2.38.0 on Python 3.9. No route constructs the collaboration service, so nothing loads it today |
| 41 | `google-auth` | PyPI, required, imported directly and also transitive | Any release exposing `default` for Application Default Credentials, imported by name at `../backend/app/db/firestore.py:L15` and pulled in again by the three Google client libraries | None recorded | 2.50.0 on Python 3.9. The direct import means this row must be installed even if a maintainer drops every Google client |
| 42 | `sqlalchemy` | PyPI, required | 1.4 or newer, because `../backend/app/db/sql.py:L13` imports `declarative_base` from `sqlalchemy.orm` | Fixes precede the floor | 2.0.51 on Python 3.9. All three advisories are fixed at 1.3.0b3 and below, under the 1.4 floor the `declarative_base` import requires. No model subclasses `Base`, so the path is declared and dead |
| 43 | `celery` | PyPI, required | Any release exposing `Celery` | Risk table | 5.6.3 on Python 3.9, which carries both fixes. No producer enqueues a task and no broker is provisioned |
| 44 | `psycopg2-binary` | PyPI, conditional | Needed once the Cloud SQL path is exercised through `DATABASE_URL` | None recorded | 2.9.12 on Python 3.9 |
| 45 | `redis` | PyPI, conditional | Needed once a Celery worker attaches to `REDIS_URL` | Risk table | 7.0.1 on Python 3.9, which carries both fixes. Compose declares no Redis service and Terraform declares no Memorystore instance |
| 46 | `cryptography` | PyPI, conditional | Needed once `settings.ALGORITHM` names an RSA or ECDSA algorithm | Risk table | 50.0.0 on Python 3.9.2 or newer, because 50.0.0 declares `!=3.9.0,!=3.9.1,>=3.9`. A 3.9.0 or 3.9.1 interpreter is capped at 43.0.3 and misses ten fixes |
| 47 | `python-dotenv` | PyPI, conditional | Needed by Pydantic 1.x to read the `Config.env_file` value at `../backend/app/core/config.py:L58` | Risk table | 1.2.1 on Python 3.9, and the fix in 1.2.2 needs Python 3.10, so it is unreachable. The read happens only when the named file is found, so an absent `.env` hides the absent distribution. No committed line calls `set_key` |

**The npm advisories.** Four of the 26 npm rows carry an advisory that reaches a release this code
could load. These columns ask a Node question rather than a Python one, which is why they sit apart
from the risk table above. `react` and `react-dom` are absent from this table on purpose: both carry
only advisories fixed at 0.14.0 and 16.4.2 respectively, and the declared `^18.2.0` is far past them.

| Distribution | What pins it | Advisories reaching a loadable release | Does an install reach a patched release |
| --- | --- | --- | --- |
| `react-router-dom` | `^6.11.1`, declared at `../frontend/package.json` | [CVE-2026-53668](https://github.com/advisories/GHSA-jjmj-jmhj-qwj2), an open redirect leading to cross-site scripting, covering 6.30.2 through 6.30.4 with **no patched 6.x release**. The fix ships in `react-router` 7.13.0 | **No.** The declared range resolves inside the affected span, so no install under it reaches a patch. The precondition is an open redirect, and this repository has none: no `Navigate`, `useNavigate`, `Redirect`, `history.push` or `window.location` construct appears under `../frontend/src/`, where `App.tsx` declares four static routes. Closing the row means a major-version move to `react-router` 7, which is a code change rather than a version bump |
| `eslint-config-prettier` | `^8.8.0`, declared at `../frontend/package.json` | [CVE-2025-54313](https://github.com/advisories/GHSA-f29h-pxvx-f335), embedded malicious code published on 19 July 2025 after a maintainer credential compromise, fixed in 8.10.2, 9.1.2 and 10.1.8 | **Yes today, and that is a timing accident rather than a control.** The malicious 8.10.1 sits inside `^8.8.0`, and no lockfile is committed, so an install run during the compromise window had nothing pinning it out. The range now resolves to 8.10.2 or later. [`npm ci` cannot run anywhere](#npm-ci-cannot-run-anywhere) records the absent lockfile that both `../.github/workflows/ci.yml` and `../infrastructure/docker/frontend.Dockerfile` depend on |
| `axios` | Nothing. Imported at `../frontend/src/services/api.ts:L15` and `auth.ts:L16`, declared in no manifest | Forty-three advisories, the largest set in this register. The fix ladder runs from 0.18.1 to 0.33.0 and 1.18.0, and includes [CVE-2026-40175](https://github.com/advisories/GHSA-fvcv-3m26-pcqx) cloud-metadata exfiltration through a header-injection chain and [CVE-2025-62718](https://github.com/advisories/GHSA-3p68-rc4w-qgx5) a `NO_PROXY` normalisation bypass, both fixed in 1.15.0 | **Yes, by accident of timing again.** No committed range pins the distribution, so an install by hand takes the current release, which is past every fix. The same absence of a pin is the exposure. axios 1.14.1 and 0.30.4 were published as malware on 31 March 2026 before removal, and nothing here would have held an install below them |
| `zod` | Nothing. Imported by the three modules under `../frontend/src/schema/` and by `utils/validation.ts`, declared in no manifest | [CVE-2023-4316](https://github.com/advisories/GHSA-m95q-7qp3-xv42), a denial of service, fixed in 3.22.3 | **Yes.** An install by hand resolves a 4.x release, well past the fix |

### The unmapped import prefix

Forty-four executable imports across 13 of the 26 modules under `frontend/src/` use a `@/` prefix, and
no configuration maps it. The other 13 modules import through relative paths, and every module under
`frontend/src/schema/`, `services/`, `store/` and `utils/` falls in that second group.
`frontend/tsconfig.json:L10-L16` declares five path aliases, and none of them is `@/`:

```text
"paths": {
  "@components/*": ["components/*"],
  "@utils/*": ["utils/*"],
  "@styles/*": ["styles/*"],
  "@hooks/*": ["hooks/*"],
  "@services/*": ["services/*"]
}
```

Adding `@/*` to that block would still not produce a working build. `react-scripts` 5.0.1, pinned
at `frontend/package.json:L29`, does not translate `tsconfig` path mappings into webpack module
resolution, so the bundler would continue to fail on specifiers the compiler had accepted.

The prefix accounts for 44 of the 57 `TS2307` errors. See
[../frontend/src/README.md](../frontend/src/README.md), which owns the type-check profile, and
[../frontend/src/utils/README.md](../frontend/src/utils/README.md) for the two utility modules the
absent specifiers target.

## G5 call-site contract violations

Calls in this class reach a symbol that exists and disagree with its signature. The compiler
catches none of them on the Python side, because the modules fail earlier at import.

### Argument count and type

| Call site | Call | Target signature | Disagreement |
| ----------- | ------ | ------------------ | -------------- |
| `backend/app/api/documents.py:L46` | `create_document(document, current_user)` | `create_document(self, document: DocumentCreate, user_id: str)` at `backend/app/services/document_service.py:L42` | Passes a `User` object where the signature declares `user_id: str` |
| `backend/app/api/documents.py:L91` | `get_document(document_id)` | `get_document(self, document_id: str, user_id: str)` at `backend/app/services/document_service.py:L78` | One argument against two parameters, so the ownership check cannot run |
| `backend/app/api/documents.py:L120` | `get_document(document_id)` | the same two-parameter signature | One argument against two |
| `backend/app/api/documents.py:L146` | `get_document(document_id)` | the same two-parameter signature | One argument against two |
| `backend/app/api/documents.py:L123` | `update_document(document_id, document)` | `update_document(self, document_id: str, document: DocumentUpdate, user_id: str)` at `backend/app/services/document_service.py:L116` | Two arguments against three parameters |
| `backend/app/api/documents.py:L149` | `delete_document(document_id)` | `delete_document(self, document_id: str, user_id: str)` at `backend/app/services/document_service.py:L159` | One argument against two |
| `backend/app/tasks/background_tasks.py:L135` | `get_document(document_id)` | the same two-parameter signature | One argument against two |
| `frontend/src/components/Toolbar.tsx:L45` | `applyInlineStyle(style)` | `applyInlineStyle(editorState: EditorState, inlineStyle: string)` at `frontend/src/utils/formatting.ts:L24` | One argument against two, and the missing argument is the editor state the helper transforms |
| `frontend/src/components/Toolbar.tsx:L56` | `applyBlockStyle(style)` | `applyBlockStyle(editorState: EditorState, blockType: string)` at `frontend/src/utils/formatting.ts:L45` | One argument against two |
| `frontend/src/pages/Editor.tsx:L111` | `<DocumentCanvas content={...} onContentChange={...} />` | `const DocumentCanvas: React.FC = () => {` at `frontend/src/components/DocumentCanvas.tsx:L34` | Two props passed to a component declaring none |

One call site in the same repository gets the argument count right, which is worth knowing when
reading the rows above. `backend/app/tasks/background_tasks.py:L56` calls
`get_document(document_id, user_id)` with both arguments, while `L135` in the same file passes one.
`frontend/src/components/TextEditor.tsx:L48` and `:L55` pass both arguments to the formatting
helpers, while `Toolbar.tsx` passes one to each. Comparing the two shows the contract faster than
reading either alone.

`TextEditor.tsx` is correct on the argument count and on the block types, and not on the inline style
names. `:L50-L54` forwards `header-one`, `header-two`, `blockquote`, `unordered-list-item` and
`ordered-list-item` into `applyBlockStyle`, and Draft.js spells every one of those exactly that way.
`:L45-L47` forwards the lowercase `bold`, `italic` and `underline` into `applyInlineStyle` at `:L48`,
and Draft.js spells those `BOLD`, `ITALIC` and `UNDERLINE`. An inline toggle through this component
would therefore apply a style name the renderer carries no rule for. Read the module as the correct
reference for the helper signatures and the block types, not for the inline style constants.

### Type inversions in the editor canvas

`frontend/src/components/DocumentCanvas.tsx` carries two errors that are exact inverses, so
correcting one in isolation risks reinforcing the other.

| Line | Call | Receives | Expects |
| ------ | ------ | ---------- | --------- |
| `L43` | `EditorState.createWithContent(contentState)` | an `EditorState`, returned by `deserializeDocument` at `frontend/src/utils/documentUtils.ts:L49` and assigned at `DocumentCanvas.tsx:L42` | a `ContentState` |
| `L59` | `serializeDocument(newEditorState.getCurrentContent())` | a `ContentState`, returned by `getCurrentContent()` | an `EditorState`, per `frontend/src/utils/documentUtils.ts:L29` |

`DocumentCanvas.tsx:L15` imports `ContentState` and never uses it.

### Other contract violations

| Site | Violation |
| ------ | ----------- |
| `backend/app/tasks/background_tasks.py:L112` | Calls `.delete()` on the result of `.get()`, which returns a list of documents rather than a reference. Lists carry no `delete` method |
| `backend/app/api/users.py:L58` | Calls `user_service.update_user(...)` from the synchronous handler declared at `L33`, so the call cannot be awaited. A coroutine object is always truthy, so if the absent `UserService` declares the method `async`, the guard at `L59` can never observe a failure. `app.services.user_service` does not exist, so no contract settles which it is |
| `backend/app/api/users.py:L20`, `:L33` | Both handlers use plain `def` while all 12 other handlers use `async def` |
| `backend/app/tasks/background_tasks.py:L72` | Stacks `@celery_app.periodic_task(run_every=timedelta(days=1))` beneath `@celery_app.task` at `L71`. Celery 5 exposes no `periodic_task` decorator, so the module raises `AttributeError` once the earlier import failures clear |
| `backend/app/db/firestore.py:L22-L43` | `get_document` is annotated `-> dict` and returns `None` at `L43` when the document is absent |
| `frontend/src/utils/documentUtils.ts:L34`, `:L59` | Calls `DocumentSchema.isValid(...)`. Zod exposes `parse` and `safeParse` and no `isValid`, and the argument is Draft.js content while `DocumentSchema` models document metadata, so the check targets the wrong contract twice over |

### The ownership check subscripts a key it does not verify

All three guarded `DocumentService` methods compare ownership by subscripting the raw Firestore
dictionary. `backend/app/services/document_service.py:L108`, `:L148` and `:L184` each evaluate
`doc.to_dict()['user_id'] != user_id`, and none of the three tests for the key first.

`create_document` is the only writer of that key, at `:L73`, so a document this service created
carries it. A record written any other way does not, and the `Document` contract itself declares
`owner_id` rather than `user_id` at `backend/app/schema/document.py:L28`. A stored record without a
`user_id` key therefore raises `KeyError` on the subscript.

`KeyError` is not an `HTTPException`, and no handler in `backend/app/api/documents.py` wraps the
service call in a `try`, so FastAPI's default exception handling answers **500 Internal Server Error**.
A caller who is genuinely not the owner receives 403, and a caller hitting a record with a missing key
receives 500 for what is the same authorization decision.

### The retention sweep fails partway and leaves records behind

`cleanup_expired_documents` at `backend/app/tasks/background_tasks.py:L73` deletes across two systems
and three collections with no transaction, no compensating action and no `try` anywhere in the loop.
The table below walks the loop body in execution order. Rows 1 and 2 sit above the first delete, and
every row from 4 onward runs after the Firestore document is already gone.

| Step | Statement | Locator | What happens |
| ------ | ----------- | --------- | -------------- |
| 1 | `db.collection('documents').where('expiration_date', ...).get()` | `:L96` | `datetime.now()` raises `NameError`, because `:L20` imports `timedelta` alone. Nothing else in the task runs |
| 2 | The same query, once `datetime` is imported | `:L96` | No committed line writes `expiration_date` and `backend/app/schema/document.py` never declares it, so no record the application created can match. Which records return depends on what the collection already holds |
| 3 | `user_id = doc.get('user_id')` | `background_tasks.py:L100` | Raises for a matched record that carries no `user_id`. `doc.id` at `:L99` always exists, so this is the only read that can fail before the first delete |
| 4 | `db.collection('documents').document(doc_id).delete()` | `background_tasks.py:L103` | **The first destructive step, and it succeeds.** Everything below can now fail with the document already gone |
| 5 | `storage_client.bucket(settings.DOCUMENT_BUCKET_NAME)` | `background_tasks.py:L107` | `Settings` declares no `DOCUMENT_BUCKET_NAME`, so this raises `AttributeError` |
| 6 | `blob.delete()` on the key `{user_id}/{doc_id}` | `background_tasks.py:L108`, `:L109` | No writer uses that layout. Two writers produce export objects, and their layouts disagree: `backend/app/services/export_service.py:L61` writes `exports/{document.id}.pdf` and `:L93` writes `exports/{document.id}.docx`, while `background_tasks.py:L63` writes `exports/{user_id}/{document_id}.{export_format}`. The retention key matches neither, and it addresses `DOCUMENT_BUCKET_NAME` while those two writers address `STORAGE_BUCKET_NAME` and `EXPORT_BUCKET_NAME`, so no committed writer creates the key this delete addresses. Whether the call raises `NotFound` depends on whether a matching object already exists in that bucket |
| 7 | `db.collection('document_permissions').where(...).get().delete()` | `background_tasks.py:L112` | `.get()` returns a list of snapshots, and a list carries no `delete` method, so this raises `AttributeError` |
| 8 | `db.collection('document_metadata').document(doc_id).delete()` | `background_tasks.py:L113` | The last statement. Reached only if every step above succeeded |

Four partial states follow, one per failure point after the first delete:

| Stops at | Document record | Stored file | Permissions | Metadata |
| ---------- | ----------------- | ------------- | ------------- | ---------- |
| Step 5 | Deleted | Present | Present | Present |
| Step 6 | Deleted | Present, delete failed on the wrong key | Present | Present |
| Step 7 | Deleted | Deleted | Present | Present |
| Step 8 succeeds | Deleted | Deleted | Deleted | Deleted |

The loop holds no `try`, so the first raise propagates out of the task and abandons every remaining
expired document in the same run. Nothing records which documents were processed, so a retry starts
from the query again and cannot tell a half-deleted document from an untouched one.
[../backend/app/tasks/README.md](../backend/app/tasks/README.md) carries the module detail.

### The mutating methods check, then write, with nothing between

`update_document` and `delete_document` both read a snapshot, decide on it, and then write, with no
transaction and no precondition on the write. The window between the read and the write is a
time-of-check to time-of-use race.

| Method | Read | Existence check | Ownership check | Write |
|--------|------|-----------------|-----------------|-------|
| `update_document` at `backend/app/services/document_service.py:L116` | `:L142` | `:L144`, 404 at `:L145` | `:L148`, 403 at `:L149` | `:L153` |
| `delete_document` at `backend/app/services/document_service.py:L159` | `:L178` | `:L180`, 404 at `:L181` | `:L184`, 403 at `:L185` | `:L188` |

Two outcomes follow. A concurrent owner change between the read and the write is overwritten silently,
because `update()` at `:L153` sends only the caller's fields and asserts nothing about the document it
found. A concurrent delete makes that same `update()` fail on a document the check at `:L144` reported
as present. Firestore supports both a transaction and a precondition, and neither method uses either.

`delete_document` compounds the problem by reporting success unconditionally. `:L191` returns the
literal `True` whatever `doc_ref.delete()` at `:L188` did, so the value means the method reached its
last line rather than that a document was removed. A Firestore delete of an already-absent document
succeeds silently, so the return value cannot distinguish a deletion from a no-op.

## G6 field and shape drift

No artifact keeps the two languages in agreement. The repository commits no OpenAPI document,
generates no client, and shares no schema package across the Python and TypeScript trees.
Developers therefore maintain the Pydantic models under `backend/app/schema/` and the Zod schemas
under `frontend/src/schema/` by hand, and the divergences below follow from that.

### The ownership field, four positions

Authorization in this repository compares an ownership field, and four positions disagree about its
name under two spellings, `owner_id` and `user_id`. **No position is canonical.** Selecting one would
change an interface, which the documentation engagement excluded, so this register lists all four
and prefers none. The full treatment sits in [data-model.md](data-model.md), and
[decision-log.md](decision-log.md) records the choice as decision row 7.

| Position | Locator | Field |
| ---------- | --------- | ------- |
| The Pydantic document contract | `backend/app/schema/document.py:L28`, on `DocumentBase` and inherited by `Document` | `owner_id: Optional[str] = None` |
| The Pydantic version contract | `backend/app/schema/document.py:L84`, on `DocumentVersion` | `user_id: str` |
| The document service | `backend/app/services/document_service.py:L71` writes it, and `:L108`, `:L148` and `:L184` compare it | `user_id` |
| The in-repository specification, declared intent | `documentation/Technical Specifications.md:L333`, `:L375`, `:L383`, under the SYSTEM DESIGN heading at `L300` | `owner_id` |

Two details make the drift worse than a naming disagreement.

The first: `owner_id` at `backend/app/schema/document.py:L28` is optional and defaults to `None`, so
a `Document` validates successfully without the field that authorization depends on. The contract
never requires the value the ownership check reads.

The second: the document router reads `.user_id` off objects typed as `Document` at
`backend/app/api/documents.py:L92`, `:L121` and `:L147`. The router follows the service convention
rather than the contract its own type annotation names. The client repeats the same split, with
`owner_id` at `frontend/src/schema/document.ts:L27` and `user_id` at `:L44`.

### Field and shape divergences

| Divergence | Client or consumer | Server or contract |
| ------------ | -------------------- | -------------------- |
| Access token field | `frontend/src/services/auth.ts:L37` reads `response.data.accessToken` and stores it at `:L38` | The token handler at `backend/app/api/auth.py:L65-L66` follows the OAuth2 convention and returns `access_token` |
| Base URL variable | `frontend/src/services/api.ts:L21` reads `process.env.REACT_APP_API_BASE_URL` | `infrastructure/docker/docker-compose.yml:L11` injects `REACT_APP_API_URL`. The names never meet, so the client resolves an undefined base URL |
| User display name | `frontend/src/components/Header.tsx:L52-L53`, `frontend/src/pages/Home.tsx:L35` and `frontend/src/pages/Settings.tsx:L36` read `currentUser.name` | `backend/app/schema/user.py:L27-L28` models `username` and `full_name`. No contract declares `name` |
| User avatar | `frontend/src/components/Header.tsx:L52` reads `currentUser.avatar` | No contract in either language declares `avatar` |
| Page count | `backend/app/tasks/background_tasks.py:L139` reads `len(document.pages)` | `backend/app/schema/document.py` declares no `pages` field on any of its five models |
| User update timestamp | `frontend/src/schema/user.ts` omits `updated_at` | `backend/app/schema/user.py:L70` declares `updated_at: datetime` as required |
| Template shape | `frontend/src/pages/Templates.tsx` declares a local `Template` interface incompatible with the Zod schema at `frontend/src/schema/template.ts:L31` | The backend declares no template contract at all, per [G1](#g1-absent-modules-referenced-by-committed-code) |
| Timestamp type | `frontend/src/schema/document.ts:L28-L29` and `:L43` use `z.date()`, which rejects a string | Every timestamp crossing the boundary arrives as a JavaScript Object Notation (JSON) string, so validation fails on well-formed server data |
| Collaborator list | `frontend/src/schema/document.ts:L30` declares `collaborators: z.array(z.string())` | No Pydantic model declares a collaborator field, and no handler returns one |
| Password storage | `backend/app/api/auth.py:L139` computes a bcrypt hash during registration | The `User` contract at `backend/app/schema/user.py:L56` declares no password field, so the response model has nowhere to carry the hash. `UserCreate` declares `password` at `:L38` |

Required fields that no code path writes compound the drift. `backend/app/schema/document.py:L63`
and `:L64` declare `created_at` and `updated_at` as required on `Document`, and no service method
sets either. `backend/app/schema/user.py:L71-L72` declare `is_active` and `is_superuser`, and no
code path reads either.

`backend/app/schema/document.py:L39` declares `DocumentUpdate` without inheriting `DocumentBase`,
so the update contract shares no field definitions with the model it updates. Both schema modules
import `List` and never use it, at `backend/app/schema/document.py:L13` and
`backend/app/schema/user.py:L14`.

See [data-model.md](data-model.md),
[../backend/app/schema/README.md](../backend/app/schema/README.md) and
[../frontend/src/schema/README.md](../frontend/src/schema/README.md).

## G7 endpoint and transport mismatch

The client calls routes the server does not expose, and the collaboration path has a different
protocol at each end.

### The client calls six routes, and no server route matches any of them

| Client call | Locator | Server route | Locator |
| ------------- | --------- | -------------- | --------- |
| `POST /auth/login` | `frontend/src/services/auth.ts:L36` | `POST /token` | `backend/app/api/auth.py:L65` |
| `POST /auth/logout` | `frontend/src/services/auth.ts:L54` | none. No handler implements logout | n/a |
| `GET /auth/me` | `frontend/src/services/auth.ts:L71` | `GET /me` | `backend/app/api/users.py:L19` |
| `GET /documents` | `frontend/src/services/api.ts:L70` | `GET /` | `backend/app/api/documents.py:L49` |
| `POST /documents` | `frontend/src/services/api.ts:L82` | `POST /` | `backend/app/api/documents.py:L24` |
| `PUT /documents/{id}` | `frontend/src/services/api.ts:L95` | `PUT /{document_id}` | `backend/app/api/documents.py:L96` |

The login call carries two further mismatches that survive a path correction. First, encoding:
`frontend/src/services/auth.ts:L36` passes a plain object to `axios.post`, and Axios serializes a
plain object as JSON under `Content-Type: application/json`, while
`form_data: OAuth2PasswordRequestForm = Depends()` at `backend/app/api/auth.py:L66` reads an
`application/x-www-form-urlencoded` body. FastAPI answers **422** before the handler body runs. Second,
field name: the client sends `email` and `password`, and `OAuth2PasswordRequestForm` supplies
`username` and `password`, which `backend/app/api/auth.py:L90` reads as `form_data.username`. No
submitted field carries the identifier the handler reads.

The document prefix mismatch has a single cause. `backend/app/main.py:L84-L87` calls
`include_router` four times and passes no `prefix` argument to any of them, so every route mounts at
the application root. The client prefixes `/documents`, and the server serves `/`. The registration
also ignores `API_V1_STR`, which `backend/app/core/config.py:L41` declares and no module reads.

The three prefixed document calls fail in three different ways, which matters when reading a response
rather than a route table. The outcomes below assume the import chain and the client's own blockers
are repaired, so dispatch actually happens.

| Client call | Locator | Dispatch outcome |
|-------------|---------|------------------|
| `GET /documents` | `frontend/src/services/api.ts:L70` | `/documents` is one path segment, so it matches `GET /{document_id}` at `backend/app/api/documents.py:L68`, `document_id` binds to the literal string `documents`, and no body follows. The matched route is protected at `backend/app/api/documents.py:L69`, so the dependency resolves before the body runs, and without a valid token the response is **401** and the handler never executes. For an authenticated caller whose user record resolves, `:L91` passes one argument to the two-parameter `get_document` signature at `backend/app/services/document_service.py:L78`, so a `TypeError` propagates and the response is a **500**. The declared `Document[]` never meets a document object on either path |
| `POST /documents` | `frontend/src/services/api.ts:L82` | The single-segment shape matches `GET`, `PUT` and `DELETE` at `backend/app/api/documents.py:L68`, `:L96` and `:L126`, and no router declares `POST /{document_id}`. Starlette answers **405 Method Not Allowed**, not 404. Routing settles that before any dependency runs, so the outcome does not depend on credentials |
| `PUT /documents/{id}` | `frontend/src/services/api.ts:L95` | Two path segments, and no two-segment route exists in any of the four routers. The response is **404**, again settled by routing before any dependency runs, so it too is independent of credentials |

Four distinct symptoms come from one root cause, and only the first depends on who is calling. `GET`
answers 401 or 500 according to the credentials presented, while the 405 and the 404 are fixed by
routing alone. A developer who repairs only the call that returns 404 leaves the other three in place.

`frontend/src/services/auth.ts:L16` imports the bare `axios` global and uses it at `L36`, `:L54`
and `:L71`, bypassing the configured instance created at `frontend/src/services/api.ts:L61`.
Requests from the authentication module therefore carry neither the base URL nor the bearer
interceptor.

### Document routes shadow the template and profile routes

The overlap has two forms, and the second is easy to miss because the paths do not look alike.

The document and template routers declare five route shapes each, and the shapes are identical. A
path parameter's name does not participate in matching, so `/{document_id}` and `/{template_id}`
compile to the same single-segment pattern.

| Method and shape | Document handler | Template handler |
| ------------------ | ------------------ | ------------------ |
| `POST /` | `backend/app/api/documents.py:L24` | `backend/app/api/templates.py:L24` |
| `GET /` | `backend/app/api/documents.py:L49` | `backend/app/api/templates.py:L42` |
| `GET /{id}` | `backend/app/api/documents.py:L68` | `backend/app/api/templates.py:L59` |
| `PUT /{id}` | `backend/app/api/documents.py:L96` | `backend/app/api/templates.py:L86` |
| `DELETE /{id}` | `backend/app/api/documents.py:L126` | `backend/app/api/templates.py:L112` |

The profile router declares two literal single-segment paths, and a literal path is still a single
segment. Both fall inside the pattern the document router already claimed.

| Method and path | Profile handler | Shadowing document handler |
|-----------------|-----------------|----------------------------|
| `GET /me` | `backend/app/api/users.py:L19` | `GET /{document_id}` at `backend/app/api/documents.py:L68` |
| `PUT /me` | `backend/app/api/users.py:L32` | `PUT /{document_id}` at `backend/app/api/documents.py:L96` |

`backend/app/main.py:L85` registers the document router first, then `:L86` the profile router and
`:L87` the template router. Starlette matches routes in registration order and returns the first
route whose pattern matches, so the document handler wins every collision. **Seven of the twelve
protected handlers are unreachable**: all five template handlers and both profile handlers.

A request to `GET /me` reaches the single-document read with `document_id` bound to the literal string
`me`.
Both routes are protected, so that substitution is only observable to a caller who presents valid
credentials. Without them the shared dependency answers 401, and the shadowing stays invisible.

### The collaboration path has no route and two protocols

| End | Protocol | Locator |
| ----- | ---------- | --------- |
| Client | Socket.IO, with `io()` called at `frontend/src/services/collaboration.ts:L37` and no URL argument | `L15` imports `io` from `socket.io-client` |
| Server | A FastAPI `WebSocket`, per the `connect(self, websocket: WebSocket, ...)` signature | `backend/app/services/collaboration_service.py:L15` and `:L44` |

The client emits three events, and each has a server method that was clearly meant to receive it.
None of the three pairs can meet.

| Client event | Emitted payload | Nearest server counterpart | Why the pair cannot meet |
| -------------- | ----------------- | ---------------------------- | -------------------------- |
| `join_document` | the bare `documentId` string, at `frontend/src/services/collaboration.ts:L63` | `CollaborationService.connect` at `backend/app/services/collaboration_service.py:L44` | `connect` declares a `WebSocket`, a `document_id` and a `user_id`. The emit carries one string, no socket object and no user identity |
| `leave_document` | the bare `currentDocumentId` string, at `:L76` | `CollaborationService.disconnect` at `backend/app/services/collaboration_service.py:L107` | `disconnect` declares `document_id` and `user_id`. The emit carries the identifier alone, and `:L159` clears it immediately with nothing confirming delivery |
| `document_changes` | the envelope `{ documentId, changes }`, at `:L96-L99` | `CollaborationService.broadcast_change` at `backend/app/services/collaboration_service.py:L137` | `broadcast_change` declares `document_id` and a `change` dictionary and publishes `json.dumps(change)` at `:L156`. The client nests the change inside an envelope, so the shapes differ even with a route in place |

Socket.IO is a protocol layered over WebSocket rather than a WebSocket client, so the two ends could
not complete a handshake even with a route between them. No route exists: no module constructs
`CollaborationService`, and no `@app.websocket` declaration appears anywhere in the backend.
`frontend/src/services/collaboration.ts:L107` exports the client class, and no module imports it.

`setupEventListeners` at `frontend/src/services/collaboration.ts:L47-L52` has a body consisting
only of a marker and comments, so the client registers no inbound handler and would ignore every
message it received.

### Nothing creates the Pub/Sub topic the server addresses

Two of the four Pub/Sub calls name a topic and need it to exist. `create_subscription` at
`backend/app/services/collaboration_service.py:L73` passes `topic=topic_name`, and `publish` at
`:L156` addresses the same path. Neither creates a topic, no `create_topic` call exists anywhere in
the repository, and the module records the gap in its own docstring at `:L8-L12`.

No committed infrastructure supplies one either. Searching all of `infrastructure/` for `pubsub`,
`topic` and `subscription` returns nothing, and `infrastructure/terraform/main.tf` declares one
provider plus four Google Cloud resources with no messaging resource among them. The topic path is
derived per document at `backend/app/services/collaboration_service.py:L69`, so a deployment needs one
topic per document identifier, created outside this repository before any editor connects.

| Call | Locator | Needs a topic | Result without a pre-created topic |
| ------ | --------- | --------------- | ------------------------------------- |
| `create_subscription` | `collaboration_service.py:L73` | Yes | `NotFound`, caught at `:L74`, printed at `:L76`, and `:L77` returns |
| `subscribe` | `collaboration_service.py:L99` | No | Never reached, because `:L77` returned first |
| `delete_subscription` | `collaboration_service.py:L130` | No | `NotFound` for a subscription never created, caught at `:L131`, printed at `:L133` |
| `publish` | `collaboration_service.py:L156` | Yes | `NotFound`, caught at `:L158`, printed at `:L160`, and the method returns normally |

### A failed publish is caught and logged rather than raised

`broadcast_change` at `backend/app/services/collaboration_service.py:L137` reads
`settings.PROJECT_ID` at `:L153`, which sits **above** the `try` at `:L155`. `Settings` declares no
`PROJECT_ID`, so the `AttributeError` propagates to the caller on the first call. That read is the
method's first statement, so nothing is published and no partial state remains.

Everything after it is guarded. `:L152` calls `json.dumps(change)` against a module that imports no
`json`, `:L154` catches every exception the body raises, and `:L156` prints it. Once `PROJECT_ID`
exists, a publish failure therefore surfaces as a printed line and a normal `None` return, and a caller
cannot tell a delivered change from a dropped one.

Three more faults in the same path deserve their own statement:

- **The callback carries three faults on one line.** `:L93` calls
  `asyncio.run(websocket.send_json(message.data))`. `asyncio` is never imported, so the first
  delivered message raises `NameError`. Supplying the import exposes the next fault: `message.data`
  is `bytes`, `WebSocket.send_json` serializes with `json.dumps`, and `json.dumps` rejects `bytes`.
  Nothing decodes the payload, while `:L152` encoded it as UTF-8 before publishing, so the round
  trip is unbalanced.

  The third fault is event-loop ownership. `asyncio.run` builds a new loop and closes it, while the
  socket belongs to the server's already-running loop. `asyncio.run` also refuses outright when a
  loop is already running on the calling thread. The Pub/Sub client invokes the callback on its own
  thread, so none of the three reaches `connect`.
- **Acknowledgement precedes delivery.** `:L92` calls `message.ack()` before `:L93` sends. A send that
  fails after the acknowledgement loses the message, because Pub/Sub has already been told it was
  handled and will not redeliver.
- **Two partial states can persist.** `connect` mutates the registry at `:L64-L66` before it touches
  Pub/Sub. A caught subscription failure therefore leaves a socket in `active_connections` with no
  subscription behind it, and no later call removes it. `disconnect` removes the registry entry at `:L118-L121`
  before deleting the subscription, so a caught failure at `:L127` leaves a subscription with no
  registry entry. Neither method compensates or reports the state.
- **Both futures block, and one method has no future at all.** `future.result()` at `:L98` and `:L153`
  pass no timeout, so each blocks its calling thread, and `connect` is `async def`, so `:L98` holds the
  event loop. `disconnect` calls `delete_subscription` at `:L126`, which returns nothing to wait on.

### Route registration and protection

Fourteen handlers exist across the four routers, and twelve sit behind the `get_current_user`
dependency. The two public handlers are `POST /token` at `backend/app/api/auth.py:L65` and
`POST /register` at `:L102`. The full route table lives in
[../backend/app/api/README.md](../backend/app/api/README.md).

Two `get_current_user` implementations exist and disagree on status codes. The routers all import
the one at `backend/app/api/auth.py:L27`, for example at
`backend/app/api/documents.py:L19`, which raises **404** at `backend/app/api/auth.py:L62` when the
user is absent. The unused implementation at `backend/app/core/security.py:L119` raises **401** for
the same condition at `:L162`. A missing user is an authentication failure rather than a missing
resource, and the reachable handler reports the latter.

See [../backend/app/api/README.md](../backend/app/api/README.md),
[../frontend/src/services/README.md](../frontend/src/services/README.md) and
[integration-guide.md](integration-guide.md).

## G8 platform and automation defects

Neither container builds, neither pipeline completes, neither script runs to the end, and the
Terraform cannot initialise. Entries group by artifact.

### The verified type-check profile

Running `npx tsc --noEmit` inside `frontend/` produces **76 errors**:

| Code | Count | Meaning | Concentrated in |
| ------ | ------- | --------- | ----------------- |
| `TS2307` | 57 | Cannot find module | 44 from the unmapped `@/` prefix, 13 from the five undeclared packages |
| `TS2305` | 6 | Module has no exported member | 5 from the missing `Document` family, 1 from `Switch` at `frontend/src/App.tsx:L12` |
| `TS7006` | 5 | Parameter implicitly has an `any` type | `frontend/src/services/api.ts:L39`, `:L46`, `:L50`, `:L51`; `frontend/src/pages/Editor.tsx:L30` |
| `TS2322` | 4 | Type not assignable | `frontend/src/App.tsx:L41-L44`, the four `Route` elements passing the version 5 `component` prop |
| `TS2614` | 2 | No exported member, import form mismatch | `frontend/src/store/index.ts:L15`, `:L16` |
| `TS2552` | 1 | Cannot find name | `frontend/src/services/api.ts:L40`, the undefined `store` |
| `TS2339` | 1 | Property does not exist on type | `frontend/src/services/api.ts:L40`, `.auth` on `{ document: unknown; user: unknown; }` |

`frontend/src/services/api.ts:L40` carries two of the seven codes on one line. The compiler reports
the state shape as `{ document: unknown; user: unknown; }`, which is direct evidence that the store
registers only the two reducer keys at `frontend/src/store/index.ts:L26-L27` and no `auth` key.

### `npm ci` cannot run anywhere

The repository commits no lockfile. No `package-lock.json`, `yarn.lock` or `pnpm-lock.yaml` exists,
and the repository root holds no `package.json` either. Both invocations fail, and the diagnostic
depends on the npm major.

On npm 7 or newer the code reads `npm error code EUSAGE`. The npm 6 that ships with the Node 14 this
repository pins reports different codes (`.github/workflows/ci.yml:L17` and
`infrastructure/docker/frontend.Dockerfile:L2`). The root invocation reports `npm ERR! code ENOENT`
for the absent `package.json`, and the container build reports `npm ERR! cipm can only install
packages with an existing package-lock.json`.

| Invocation | Locator | Working directory | Result |
| ------------ | --------- | ------------------- | -------- |
| Continuous integration | `.github/workflows/ci.yml:L19` | the repository root, because the step sets no `working-directory` | Fails. No manifest and no lockfile. npm 6 reports `ENOENT`, npm 7 or newer reports `EUSAGE` |
| Container build | `infrastructure/docker/frontend.Dockerfile:L11` | `/app`, after `L8` copies `package*.json` | Fails. The glob at `L8` matches only `package.json`. npm 6 reports the `cipm` message, npm 7 or newer reports `EUSAGE` |

`npm install` inside `frontend/` succeeds, so a developer working by hand gets further than either
automated path. One observed run on Node 14 resolved 1,532 packages, and no lockfile fixes that
number for a later run.

### The backend image cannot build or start

| Line | Instruction | Defect |
| ------ | ------------- | -------- |
| `infrastructure/docker/backend.Dockerfile:L8` | `COPY requirements.txt .` | The file does not exist, so the build fails here. `L11` would install from it |
| `infrastructure/docker/backend.Dockerfile:L14` | `COPY ./app /app` | Copies the package contents to the working directory root, so the modules land beside each other with no enclosing `app` package. Every `from app.core...` import in the source cannot resolve inside the image |
| `infrastructure/docker/backend.Dockerfile:L20` | `CMD ["uvicorn", "main:app", ...]` | Matches the flattened layout at `L14` and contradicts the source layout, where the application object sits at `backend/app/main.py:L24`. The command is consistent with the broken copy and inconsistent with the repository |
| `infrastructure/docker/backend.Dockerfile:L17` | `EXPOSE 8000` | Disagrees with the Compose port mapping below |

### Compose points at Dockerfiles that are not there

Both services in `infrastructure/docker/docker-compose.yml` name `dockerfile: Dockerfile` relative
to a context that contains no such file. The real Dockerfiles sit in `infrastructure/docker/` under
different names. Locators below are relative to that Compose file.

| Service | Declared context and file | Locator | Actual file |
| --------- | -------------------------- | --------- | ------------- |
| `frontend` | `../../frontend` plus `Dockerfile` | `docker-compose.yml:L6-L7` | `infrastructure/docker/frontend.Dockerfile` |
| `backend` | `../../backend` plus `Dockerfile` | `docker-compose.yml:L19-L20` | `infrastructure/docker/backend.Dockerfile` |

The backend port mapping compounds the problem.
`infrastructure/docker/docker-compose.yml:L21-L22` publishes `"5000:5000"` while the image serves
8000, per `infrastructure/docker/backend.Dockerfile:L17` and `:L20`. Compose then points the
frontend at `http://backend:5000` at `docker-compose.yml:L11`, so all three values would have to
change together.

One more Compose defect belongs here rather than in a section of its own.
`infrastructure/docker/docker-compose.yml:L12-L13` and `:L25-L26` declare `depends_on`, which orders
container start and waits for no readiness signal. No service declares a `healthcheck`, so the
backend starts as soon as the database container starts rather than when PostgreSQL accepts
connections. `docker compose exec db pg_isready -U postgres` is the check the file omits.

`infrastructure/docker/docker-compose.yml` and `scripts/setup_dev_environment.sh` also provision
different databases:

| Setting | Compose | Setup script |
| --------- | --------- | -------------- |
| Database name | `wordapp`, at `docker-compose.yml:L33` | `msword_clone`, at `scripts/setup_dev_environment.sh:L31` |
| User | `postgres`, at `docker-compose.yml:L34` | `msword_user`, at `scripts/setup_dev_environment.sh:L32` |

### The frontend never receives a working API base URL

`infrastructure/docker/docker-compose.yml:L11` sets `REACT_APP_API_URL=http://backend:5000`, and four
barriers stand between that value and a request reaching the backend. Each barrier is sufficient on its
own, so fixing any one leaves the other three.

1. **The key name does not match.** The frontend's only `process.env` read is the `API_BASE_URL`
   constant at `frontend/src/services/api.ts:L21`, which reads `REACT_APP_API_BASE_URL`. Compose sets
   `REACT_APP_API_URL`.
2. **Substitution happens at build time, not run time.** `frontend/package.json:L29` pins
   `react-scripts` at `5.0.1`, and Create React App substitutes every `process.env.REACT_APP_*`
   reference into the bundle during `npm run build`, at
   `infrastructure/docker/frontend.Dockerfile:L17`. The runtime stage starts `nginx:alpine` at `:L20`
   and serves already-compiled files, so a Compose `environment` entry arrives after substitution has
   happened.
3. **The browser cannot resolve the host.** `backend` is a Compose service name, and Docker resolves it
   only for containers joined to `word-app-network` at `docker-compose.yml:L44-L46`. The bundle runs in
   the user's browser on the host, where `backend` is not a resolvable name.
4. **The port is wrong even from inside the network.** The value names 5000, Compose publishes
   `5000:5000` at `:L21-L22`, and Uvicorn listens on 8000 per
   `infrastructure/docker/backend.Dockerfile:L20`.

Supplying a working base URL therefore needs a build argument consumed before `npm run build`. That
argument must use the key the code reads, name a host the browser can resolve, and carry the port the
server listens on. [../infrastructure/docker/README.md](../infrastructure/docker/README.md) and
[deployment-guide.md](deployment-guide.md) carry the same four barriers.

### Compose supplies one of the seven required backend settings

`Settings` declares nine fields at `backend/app/core/config.py:L40-L48`. Seven carry no default and
are required, and the two `Optional` Google Cloud fields at `:L45-L46` default to `None`. Compose
supplies exactly one of the nine. Six further settings are read from `settings` in application code and
declared on no model, so neither a `.env` file nor a Compose entry can reach them through Pydantic. The
matrix covers all 15.

| Setting | Declared at | Required | Compose supplies | Consequence |
| --- | --- | --- | --- | --- |
| `PROJECT_NAME` | `config.py:L40` | Yes | No | `Settings()` raises `ValidationError` |
| `API_V1_STR` | `config.py:L41` | Yes | No | `ValidationError`. Read by no module |
| `SECRET_KEY` | `config.py:L42` | Yes | No | `ValidationError`. Signs and verifies every token |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `config.py:L43` | Yes | No | `ValidationError`. Sets token lifetime |
| `ALGORITHM` | `config.py:L44` | Yes | No | `ValidationError`. Names the JWT algorithm |
| `GOOGLE_CLOUD_PROJECT` | `config.py:L45` | No, `Optional` | No | Resolves to `None`, and `backend/app/db/firestore.py:L20` passes it as the Firestore project |
| `GOOGLE_APPLICATION_CREDENTIALS` | `config.py:L46` | No, `Optional` | No | Resolves to `None`. No credential file is mounted into any container |
| `DATABASE_URL` | `config.py:L47` | Yes | Yes, at `docker-compose.yml:L24` | Satisfied. Read at `backend/app/db/sql.py:L16` |
| `REDIS_URL` | `config.py:L48` | Yes | No | `ValidationError`. Compose declares no Redis service to point it at |
| `ALLOWED_ORIGINS` | Nowhere | n/a | No | `AttributeError` at `backend/app/main.py:L77` when the CORS middleware reads it |
| `PROJECT_ID` | Nowhere | n/a | No | `AttributeError` at `backend/app/services/collaboration_service.py:L69` |
| `STORAGE_BUCKET_NAME` | Nowhere | n/a | No | `AttributeError` at `backend/app/services/export_service.py:L60` |
| `SIGNED_URL_EXPIRATION` | Nowhere | n/a | No | `AttributeError` at `backend/app/services/export_service.py:L68` |
| `EXPORT_BUCKET_NAME` | Nowhere | n/a | No | `AttributeError` at `backend/app/tasks/background_tasks.py:L62` |
| `DOCUMENT_BUCKET_NAME` | Nowhere | n/a | No | `AttributeError` at `backend/app/tasks/background_tasks.py:L107` |

Six required fields are absent, and six more are unsatisfiable by any environment mechanism at all. A
backend container that got past the absent `requirements.txt` would still fail during import, because
`backend/app/core/config.py` never constructs the module-level `settings` instance that eight modules
request. [../infrastructure/docker/README.md](../infrastructure/docker/README.md) and
[deployment-guide.md](deployment-guide.md) carry the same matrix with the same counts.

### No Redis service backs the Celery broker

`backend/app/tasks/background_tasks.py:L22` constructs a Celery application whose broker reads
`settings.REDIS_URL`, and `backend/app/core/config.py:L48` declares `REDIS_URL` as a required
setting. Nothing provides Redis. `infrastructure/docker/docker-compose.yml` declares three services,
`frontend`, `backend` and `db`, and no cache or broker. `infrastructure/terraform/main.tf` declares
no Memorystore instance.

No process runs the tasks either. No worker command appears in any Dockerfile, Compose service,
workflow or script, and no beat scheduler exists for the daily sweep declared at
`backend/app/tasks/background_tasks.py:L72`. No producer enqueues the three tasks, because nothing
calls `.delay()` or `.apply_async()` anywhere in the repository.

### Signed URL generation needs credentials nothing supplies

`ExportService` writes an object and signs a link for it, and neither step completes. Three
prerequisites are missing, and they fail in this order inside `export_to_pdf`.

| Order | Statement | Locator | What it needs |
| ------- | ----------- | --------- | --------------- |
| 1 | `self.storage_client.bucket(settings.STORAGE_BUCKET_NAME)` | `backend/app/services/export_service.py:L60` | A declared `STORAGE_BUCKET_NAME`. `Settings` declares nine fields at `backend/app/core/config.py:L40-L48` and this is not one, so attribute access raises `AttributeError` before any network call |
| 2 | `blob.upload_from_string(...)` | `backend/app/services/export_service.py:L63` | Credentials that authenticate and can write to the bucket. `backend/app/services/export_service.py:L36` builds `Client()` with no arguments, so the Cloud Storage client runs its own Application Default Credentials lookup. That lookup is independent of the Firestore lookup at `backend/app/db/firestore.py:L19`, the repository's only explicit `default()` call. ADC consults several sources, among them `GOOGLE_APPLICATION_CREDENTIALS`, a `gcloud` user credential in the well-known configuration file, and the instance metadata server. No committed file supplies any of them |
| 3 | `blob.generate_signed_url(version="v4", ...)` | `backend/app/services/export_service.py:L66-L70` | Sign-capable credentials, plus an expiry inside the version 4 limit |

Step 3 is the prerequisite most easily missed, because authentication alone does not satisfy it. A
version 4 signature is computed locally, so the credentials must be able to sign bytes. Two shapes
do that. The first is a service-account private key, referenced through
`GOOGLE_APPLICATION_CREDENTIALS`, which `backend/app/core/config.py:L46` declares as `Optional[str]`
so the field defaults to `None`. No committed `.env` supplies a value, and `Config.env_file` at
`:L58` names the uncommitted file that Pydantic would read.

The second is an IAM `signBlob` grant, which credentials with no private key must use by delegating
to the IAM Credentials application programming interface (API). That path needs
`iam.serviceAccounts.signBlob` on the signing service account, granted through the Service Account
Token Creator role, and the caller must name the signer explicitly. Neither the code nor
`infrastructure/terraform/main.tf` grants that permission or names a signer.

Credentials from `gcloud auth application-default login` carry neither a private key nor a signer
identity, so `generate_signed_url` raises for a local developer even when the upload succeeds.

The expiry adds two more constraints. `generate_signed_url` accepts an `int` of seconds, a
`datetime.timedelta` or an absolute `datetime`, and `backend/app/services/export_service.py:L68`
passes `settings.SIGNED_URL_EXPIRATION` with no conversion, so the call receives whatever type that
field eventually holds. A version 4 signature also caps the lifetime at seven days, and a longer
expiry raises `ValueError` rather than shortening the link. `Settings` declares no
`SIGNED_URL_EXPIRATION`, so no committed value can be checked against either constraint.

Neither export method holds a `try`, so both errors reach the caller, and step 2 has already written
the placeholder object by the time step 3 fails. The task path signs differently again:
`backend/app/tasks/background_tasks.py:L67` passes no `version` argument at all, so it would sign
under version 2.

### The CD workflow deploys two absent descriptors

`.github/workflows/cd.yml:L19-L20` runs `gcloud app deploy app.yaml` and
`gcloud app deploy dispatch.yaml`. Neither file exists. `scripts/deploy.sh:L27` deploys the same
absent `app.yaml`.

**Only one of the two failures is visible.** GitHub Actions runs a `run:` block through `bash -e` by
default, and the block opens at `.github/workflows/cd.yml:L18`. Fail-fast means `:L19` aborts the whole
step the moment `gcloud app deploy app.yaml` reports a missing descriptor, so `:L20` never executes and
its own absent `dispatch.yaml` stays latent. A reader who supplies `app.yaml` alone sees the step
advance one line and fail again. Both descriptors have to arrive together, and
[deployment-guide.md](deployment-guide.md#why-a-deploy-fails-as-committed) counts them as one first hit
and one latent blocker for that reason.

**The credentials the step runs with make the failure order matter.**
`.github/workflows/cd.yml:L16` passes `GCP_SA_KEY` into the job, so every action and every command in
it holds a service-account credential. A step that aborts mid-sequence leaves whatever it already
changed in place, and this step has no rollback.

The workflow carries three further defects:

- **No gate before deploy.** A push to `main` deploys without waiting for continuous integration,
  which would fail anyway. A `needs:` key cannot supply the gate, because `needs:` orders jobs
  inside one workflow and cannot reference another workflow. Gating delivery on integration needs
  either one combined workflow or a `workflow_run` trigger on `cd.yml`, and neither file contains
  `needs:` or `workflow_run`.
- **No rollback.** No step captures the previous version or reverts on failure.
- **Deprecated action versions.** `actions/checkout@v2` at `.github/workflows/ci.yml:L13` and
  `.github/workflows/cd.yml:L11`, `actions/setup-node@v2` at `ci.yml:L15`, and
  `google-github-actions/setup-gcloud@v0.2.0` at `cd.yml:L13`. All three run on a deprecated Node
  runtime.
- **Every action reference is a mutable tag.** A tag such as `@v2` points wherever its owner moves it.
  The code that executes in a job holding `GCP_SA_KEY` can therefore change with no change to any
  committed file. Only a full-length commit SHA is immutable, and all four references above name a tag.

### The continuous integration workflow validates almost nothing

The continuous integration workflow exercises only the frontend. `.github/workflows/ci.yml` declares no
Python job, no dedicated linting step and no dedicated type-check step, so the pipeline reports none of
the 12 import failures at all.

The 76 type errors are a different case, and the distinction matters because the workflow does contain a
step that would surface them. `.github/workflows/ci.yml:L23` runs `npm run build`, which
`frontend/package.json:L33` resolves to `react-scripts build`. Create React App treats a TypeScript
error as a build failure rather than a warning unless `TSC_COMPILE_ON_ERROR=true` is set in the
environment, and nothing in the repository sets it. Fixing the install step at `:L19` therefore moves
the CI failure from installation to the build, and the build failure names type errors rather than a
missing lockfile. A `lint` script exists at `frontend/package.json:L36` and no workflow step invokes it.

Neither of those steps runs today, because `:L19` fails first. See
[`npm ci` cannot run anywhere](#npm-ci-cannot-run-anywhere).

### The setup script targets the wrong framework

`scripts/setup_dev_environment.sh` runs Django management commands against a FastAPI project.
No `manage.py` exists anywhere in the repository.

| Line | Command | Defect |
| ------ | --------- | -------- |
| `L26` | `pip install -r requirements.txt` | No such file, per [G4 no backend manifest](#the-backend-has-no-dependency-manifest) |
| `L40` | `cp .env.example .env` | No `.env.example` is committed, so the copy fails and every required setting stays unset |
| `L47` | `python manage.py makemigrations` | A Django command, and no `manage.py` exists. Nothing in this repository provides a migration mechanism of any kind, and this register names no replacement |
| `L48` | `python manage.py migrate` | A Django command |
| `L55` | `python manage.py runserver` | A Django command, printed as the instruction for starting the backend |
| `L10` | `apt-get install -y nodejs npm python3 ...` | Pins no version, so the installed runtimes depend on the distribution rather than on the project's declared floors |

`scripts/deploy.sh` has no `set -e`, so every step runs regardless of whether the previous one
failed, and the script prints `Deployment completed successfully!` at `L47` unconditionally. The
message is not conditional on failure either, so a run in which every cloud command failed still
reports success. `L23` hard-codes the bucket `gs://my-word-app-bucket/`. `L15` runs
`python -m pytest tests/` against a root-level `tests/` directory that does not exist, and `L11` runs
`npm run build` from the repository root, where no manifest exists.

`scripts/setup_dev_environment.sh` shares the pattern. That script has no `set -e` either, so the three
defective steps above do not stop it, and `L52` prints `Development environment setup complete!`
unconditionally. The result is a partial run reported as a success. The `apt-get` installs, the virtual
environment at `L14` and `npm install` at `L20` do complete. The dependency install at `L26`, the
environment template at `L31` and both migrations at `L47-L48` do not.

**The credentials guard authenticates nothing.** `scripts/deploy.sh:L4-L7` tests only that
`GOOGLE_APPLICATION_CREDENTIALS` holds a non-empty value, then proceeds. That variable configures
Application Default Credentials, which is the mechanism the Google client libraries use inside the
application. Every cloud command the script runs is a `gcloud` or `gsutil` invocation, and those
read the CLI's own active account from its configuration rather than that variable.

Setting the variable to any non-empty string satisfies the guard, and `gsutil cp` at `:L23` is the
first command to expose the gap by failing on authentication. Authenticating the CLI takes `gcloud
auth activate-service-account --key-file` or `gcloud auth login`, and no committed file runs either.

**The archive carries more than the application.** `scripts/deploy.sh:L19` runs `zip -r app.zip . -x
"*.git*" -x "node_modules/*" -x "venv/*"` from the repository root, and the two directory patterns
are anchored at that root. Neither matches `frontend/node_modules/`, which the install step creates,
nor `backend/venv/`, which `scripts/setup_dev_environment.sh:L14` creates, and nothing excludes a
`.env` file or a service-account JSON key. `:L23` then uploads the
result to a hard-coded public-name bucket.

A developer who followed the setup script and placed credentials in the tree ships both the
credentials and two dependency trees. The exclusion patterns need `**/node_modules/*`, `**/venv/*`,
`.env` and the key file's own name, and adding them is a repository change that this documentation
pass does not make.

Three operational details compound the archive step. `:L19` writes `app.zip` into the working
directory, so a second run updates the existing archive rather than replacing it, and stale paths from
an earlier run survive. Every step assumes the repository root as the working directory, and the script
sets none, so invoking it from `scripts/` changes what `npm run build`, `pytest` and `zip` see. `:L31`
and `:L35` mutate remote state on every run: `gcloud sql connect` replays
`db_migrations.sql`, a file the repository does not commit, and `gcloud compute backend-services update`
re-applies the CDN flag. `:L35` also names no `--global` or `--region` scope and no `--quiet`, so the
command either prompts or fails depending on the CLI's configured defaults.

### Three Terraform module sources do not exist

`infrastructure/terraform/main.tf` declares three module blocks whose `source` paths point into a
directory that was never added. No `infrastructure/terraform/modules/` directory exists.

| Module | Declared at | Source |
| -------- | ------------- | -------- |
| `word_backend` | `main.tf:L67` | `./modules/word_backend` |
| `word_frontend` | `main.tf:L76` | `./modules/word_frontend` |
| `word_database` | `main.tf:L85` | `./modules/word_database` |

`terraform init` reports an unreadable module directory for each of the three absent sources. The exact
wording, the ordering and the number of errors shown depend on the Terraform release, and no committed
file pins a version. Treat any transcript of that output as illustrative rather than exact.
Terraform's own locator reads `main.tf:67`, which is where the `word_backend` block opens.
[../infrastructure/terraform/README.md](../infrastructure/terraform/README.md) carries the same
qualification.

### Terraform outputs describe a different cloud

`infrastructure/terraform/outputs.tf` declares 14 outputs, and every value reads an Amazon Web
Services (AWS) resource address. The 14 outputs name **12 distinct resource addresses across 9
resource types**, and the file references no `google_` resource at all. The only provider configured
anywhere is `google`, at `infrastructure/terraform/main.tf:L9`, so no output can resolve and none of
the addressed resources can be created.

| Resource type | Addresses referenced |
| --------------- | --------------------- |
| `aws_api_gateway_deployment` | `.main` |
| `aws_api_gateway_stage` | `.main` |
| `aws_db_instance` | `.main`, `.read_replica` |
| `aws_s3_bucket` | `.main`, `.backup` |
| `aws_instance` | `.main` |
| `aws_lambda_function` | `.main` |
| `aws_cloudfront_distribution` | `.main` |
| `aws_vpc` | `.main` |
| `aws_subnet` | `.public`, `.private` |

No output exports the four resources the configuration does declare:
`google_compute_network.word_network` at `infrastructure/terraform/main.tf:L19`,
`google_compute_subnetwork.word_subnet` at `:L25`, `google_compute_firewall.allow_internal` at
`:L35` and `google_storage_bucket.word_documents` at `:L50`.

Two outputs interpolate a database password into their value: `database_connection_string` at
`infrastructure/terraform/outputs.tf:L20` and `read_replica_connection_string` at `:L26`. Both set
`sensitive = true`, at `:L21` and `:L27`, which masks the value in command-line output. Terraform
still writes the resolved password to state in plaintext, so the setting reduces exposure without
removing it.

Two facts make that worse here. The configuration declares no backend block, so state lands on the
local filesystem unencrypted. No `.gitignore` exists at any path in this repository either, so
`terraform.tfstate` is an untracked file that `git add .` stages along with everything else. A
single unguarded commit publishes the password.

### Other Terraform defects

| Defect | Locator |
| -------- | --------- |
| A firewall rule opens every Transmission Control Protocol (TCP) port, `0-65535`, to the whole subnet `10.0.0.0/24` | `infrastructure/terraform/main.tf:L41` and `:L44`, inside the rule declared at `:L35` |
| No `required_providers` and no `required_version` block, so provider and Terraform versions float | `infrastructure/terraform/main.tf` contains neither |
| No backend block, so state is written to the local filesystem and shared with nobody | `infrastructure/terraform/main.tf` contains none |
| Local state is written in plaintext and nothing prevents committing it | No `.gitignore` exists at any path in the repository, verified by both a filesystem scan and `git ls-files`. `terraform.tfstate` therefore appears as an untracked file that `git add .` will stage |
| 11 of the 13 declared variables are never referenced. Only `project_id` and `region` reach a resource | `infrastructure/terraform/variables.tf` declares variables at `L7`, `L14`, `L21`, `L29`, `L37`, `L44`, `L53`, `L61`, `L67`, `L73`, `L79`, `L85` and `L91` |
| `storage_class` is declared and the bucket sets no storage class | declared at `variables.tf:L37`; the bucket at `main.tf:L50` omits the argument |
| No variable declares a `validation` block, so `environment` accepts any string | `infrastructure/terraform/variables.tf` contains zero validation blocks |

### Tailwind never compiles

`frontend/package.json:L12` declares Tailwind CSS, and nothing configures it. No
`tailwind.config.js` exists, no `postcss.config.js` exists, and the repository commits no `.css`
file anywhere. No authored rule therefore backs any Tailwind utility class in the markup, and once the
build blockers above are cleared no authored styling would apply.

Two styling conventions coexist, and no authored rule backs either one. Tailwind utility classes appear
in exactly two modules, `frontend/src/components/Header.tsx` across twelve `className` attributes and
the body of `frontend/src/pages/Templates.tsx` across seven. Bespoke semantic class names with no
backing stylesheet appear in eight modules: `Footer.tsx`, `Sidebar.tsx`, `Toolbar.tsx`,
`DocumentCanvas.tsx`, `Home.tsx`, `Editor.tsx`, `Settings.tsx` and the wrapper of `Templates.tsx`. That
last file therefore uses both conventions at once. The only responsive breakpoint strings anywhere are
`md:grid-cols-2` and `lg:grid-cols-3`, both at `frontend/src/pages/Templates.tsx:L92`.

### Frontend framework version mismatches

| Usage | Locator | Declared version |
| ------- | --------- | ------------------ |
| `ReactDOM.render`, the React 17 entry point | `frontend/src/index.tsx:L33` | `react` and `react-dom` at `^18.2.0`, `frontend/package.json:L8-L9`. React 18 expects `createRoot` |
| `Switch` and the `component` prop, both removed in version 6 | `frontend/src/App.tsx:L12` and `:L41-L44` | `react-router-dom` at `^6.11.1`, `frontend/package.json:L11` |
| Two nested `Provider` elements wrapping one store | `frontend/src/index.tsx:L35` and `frontend/src/App.tsx:L35` | the inner element is redundant |
| Named import of a default-only export | `frontend/src/App.tsx:L20` imports `{ store }`; `frontend/src/index.tsx:L14` imports the default correctly | `frontend/src/store/index.ts:L36` exports only a default |

Five navigation links target routes the router never declares. `frontend/src/App.tsx:L41-L44`
declares `/`, `/editor`, `/templates` and `/settings`.

| Link | Locator |
| ------ | --------- |
| `/documents` | `frontend/src/components/Header.tsx:L44` |
| `/login` | `frontend/src/components/Header.tsx:L56` |
| `/new-document` | `frontend/src/pages/Home.tsx:L37` |
| `/open-document` | `frontend/src/pages/Home.tsx:L40` |
| `/recent-documents` | `frontend/src/pages/Home.tsx:L43` |

### Runtime versions are declared three ways and enforced nowhere

Each End of life cell below cites the upstream project that publishes the date. This table is the source
every other runtime claim in this documentation set refers back to.

| Runtime | Declarations | Enforcement | End of life |
| --------- | -------------- | ------------- | ------------- |
| Python | 3.8 or later at `README.md:L23`; `python:3.9-slim` at `infrastructure/docker/backend.Dockerfile:L2`; unpinned `apt-get` packages at `scripts/setup_dev_environment.sh:L10` | none. No `.python-version` and no manifest | 3.9 ended support on 31 October 2025, with 3.9.25 as its final security release. 3.8 ended earlier still. Source: the [Python release cycle](https://devguide.python.org/versions/) |
| Node.js | 14 or later at `README.md:L22`; `node-version: '14'` at `.github/workflows/ci.yml:L17`; `node:14-alpine` at `infrastructure/docker/frontend.Dockerfile:L2` | none. `frontend/package.json` declares no `engines` field and no `.nvmrc` exists | 14 ended support on 30 April 2023. Source: [Node.js previous releases](https://nodejs.org/en/about/previous-releases) |
| PostgreSQL | `postgres:13` at `infrastructure/docker/docker-compose.yml:L31`; `postgresql`, unpinned, at `scripts/setup_dev_environment.sh:L10`; Cloud SQL named with no version in `infrastructure/terraform/main.tf` | none. No version appears in any application file | 13 ended support on 13 November 2025, with 13.23 as its final release. Sources: the [PostgreSQL versioning policy](https://www.postgresql.org/support/versioning/) and the [release announcement](https://www.postgresql.org/about/news/postgresql-181-177-1611-1515-1420-and-1323-released-3171/) that records 13 as end-of-life |

**All three declared runtimes are past end of life.** None receives security patches as of 6 August
2026, so a machine or an image built to these declarations runs unsupported software at every layer.
`nginx:alpine` at `infrastructure/docker/frontend.Dockerfile:L20` pins no version at all, so a rebuild
can change the serving runtime with no file changing.

One further version interaction sits behind the Python pin. The current `google-cloud-firestore`
release requires Python 3.10 or newer, and `backend/app/db/firestore.py:L14` imports from it. A 3.9
interpreter resolves the install to an older release rather than failing, so an environment built to
the declared floor pins an unmaintained client without reporting anything.
[onboarding.md](onboarding.md#prerequisites) carries that interaction.

See [deployment-guide.md](deployment-guide.md),
[../infrastructure/terraform/README.md](../infrastructure/terraform/README.md),
[../infrastructure/docker/README.md](../infrastructure/docker/README.md),
[../.github/workflows/README.md](../.github/workflows/README.md),
[../scripts/README.md](../scripts/README.md) and
[../frontend/src/pages/README.md](../frontend/src/pages/README.md).

## G9 absent security controls

Every entry below records a control the committed code does not implement. Read the two
qualifications first, because they govern how every row in this class should be read.

**An absent control produces no error.** The eight classes above this one record something present
and wrong. Most of them announce themselves through a traceback, a type error or a failed command.
Nothing here does.

No entry in this class was found by running anything. Each one was found by reading the code and
asking what is not there.

**Absence and current unreachability are separate facts, and this register states both.** No route
in `backend/app/` serves a request today, because `import app.main` fails at
`backend/app/api/auth.py:L19`. A missing check on an unreachable path exposes nothing while the path
stays unreachable. The moment the import failures at
[G2](#g2-absent-symbols-inside-modules-that-do-exist) are repaired, every gap below becomes live at
once. None of them is mentioned in the repair steps that would make them live.

That ordering is the reason this class exists. Where a claim about runtime behaviour would depend on
a service this repository does not provide, the entry says what cannot be established rather than
guessing.

### G9.1 The backend HTTP surface

Fourteen handlers exist across four routers. Twelve declare the bearer dependency and two are public.
Each control below is absent from one or more of those paths rather than from every one of them.
Several rows qualify their own scope, naming a path that is already conformant or a check that is
attempted, so read each row's scope from the row itself. Entry 7 records one 401 path that does carry
a challenge, and entry 12 records three handlers that attempt an owner comparison.

| # | Absent control | Evidence | What the absence permits once routes serve traffic |
|---|----------------|----------|-----------------------------------------------------|
| 1 | Rate limiting or throttling on any route, including the two public ones | `backend/app/main.py:L75` adds one middleware, and it is CORS. No limiter, no dependency and no proxy configuration is committed anywhere. The public routes are `backend/app/api/auth.py:L65` (`POST /token`) and `:L102` (`POST /register`) | Unmetered credential guessing against `/token` and unmetered account creation against `/register` |
| 2 | A request body size limit | No handler, no middleware and no server flag bounds a body. `backend/app/schema/document.py:L27` declares `content` as a bare `str` | A single request can carry an unbounded document body into a Firestore write |
| 3 | Field length or format bounds on any model field | Neither `backend/app/schema/document.py` nor `backend/app/schema/user.py` contains a single `Field(` call, so no `max_length`, no `min_length` and no pattern applies to any field. `backend/app/schema/user.py:L26` declares `email: str` rather than an email type | Oversized and malformed values validate successfully and reach storage |
| 4 | A server-side password policy | `backend/app/schema/user.py:L38` declares `password: str` with no constraint, and `backend/app/api/auth.py:L139` hashes whatever arrives through a passlib `CryptContext`. The only policy in the repository is client-side, at `frontend/src/utils/validation.ts:L36-L42`, and a client-side check is not a control | No length or complexity rule applies at the schema, so an empty password validates and reaches the hash. Acceptance and hashing are separate steps, and the hash step's behaviour is decided by the resolved passlib and bcrypt pair, which no committed manifest pins. With passlib 1.7.4 and bcrypt 5.0.0 every call raises `ValueError` whatever the length, which surfaces as an unhandled 500 on the public register route. With a bcrypt release passlib can drive, a password over 72 bytes is truncated, so two longer passwords sharing that prefix authenticate interchangeably. [The pairing subsection](#the-passlib-and-bcrypt-pairing-decides-whether-any-password-can-be-hashed) carries the evidence |
| 5 | Uniform responses that do not distinguish known accounts | Registration answers a known address with 400 `Email already registered` at `backend/app/api/auth.py:L136-L137`. Login answers a bad credential with 401 `Incorrect username or password` at `:L91-L92`, which is correctly uniform. The registration route is the enumeration oracle | An attacker learns which email addresses hold accounts by submitting registrations |
| 6 | Any check on `is_active` before a token is honoured | `backend/app/schema/user.py:L71` declares `is_active`, and no code path in the repository reads it. `backend/app/api/auth.py:L63` returns the user immediately after lookup, and `backend/app/core/security.py:L159-L162` does the same in the duplicate dependency | A deactivated account keeps full access for the life of its token |
| 7 | A `WWW-Authenticate: Bearer` header on every 401 | Two sources answer 401, and only one carries a challenge. `OAuth2PasswordBearer`, constructed at `backend/app/api/auth.py:L23` and `backend/app/core/security.py:L23`, leaves `auto_error` at its default `True`, and FastAPI's OAuth2 base raises `HTTPException(401, headers={"WWW-Authenticate": "Bearer"})` for a missing or non-bearer `Authorization` header, so that path is conformant. The six explicit raises are not, at `backend/app/api/auth.py:L55-L56`, `:L58`, `:L91-L92`, and `backend/app/core/security.py:L155`, `:L157`, `:L162`. None of the six sets a `headers` argument | A client that presents a malformed or expired token, or a valid token for an absent user, receives a 401 with no challenge. The client cannot distinguish that case from an authorization failure by header alone |
| 8 | Any constraint on the JWT secret, algorithm or lifetime | `backend/app/core/config.py:L42` declares `SECRET_KEY: str`, `:L44` declares `ALGORITHM: str` and `:L43` declares `ACCESS_TOKEN_EXPIRE_MINUTES`, none with a validator, a minimum or an allowed-value list. `backend/app/core/security.py:L54` passes the algorithm value straight to `jwt.encode`, and the two verifying calls pass it to `jwt.decode`, at `backend/app/core/security.py:L152` and `backend/app/api/auth.py:L53` | A weak secret or an indefinite lifetime passes configuration unchallenged. Algorithm choice is set by configuration rather than by an allow-list. Both decode calls restrict verification to the single value `ALGORITHM` names, so an attacker-supplied algorithm is not accepted by these call sites as written |
| 9 | Issuer, audience and token identifier claims, and any revocation path | `backend/app/api/auth.py:L95-L99` encodes exactly two claims, `sub` and `exp`. The decode at `:L53` reads `sub` only, and `backend/app/core/security.py:L152` does the same | A token cannot be scoped to one service or one audience, and no issued token can be withdrawn before it expires |
| 10 | A declared, reviewed CORS origin list | `backend/app/main.py:L77` reads `settings.ALLOWED_ORIGINS`, and `backend/app/core/config.py:L40-L48` never declares that field, so the value comes from outside every declared contract. `:L74` sets `allow_credentials=True` while `:L75` and `:L50` allow every method and every header | Credentialed cross-origin access is configured against an origin source no committed file declares or supplies. Which origins a deployment would permit is therefore unreviewable here, and so is whether the list is safe |
| 11 | Object-level authorization on any template route | `backend/app/api/templates.py:L81`, `:L107` and `:L131` delegate to a `TemplateService`, and no file exists at `backend/app/services/template_service.py`. The 404 detail at `:L83` reads `Template not found`, while `:L109` and `:L133` read `Template not found or user not authorized`, so two of the three messages promise a check that no committed code performs | Unestablished. No router line performs a check, and the delegate that would is absent, so what a template request authorizes cannot be read from this repository. Two of the three messages advertise a check, which is enough to make a reader assume one runs |
| 12 | Enforced object-level authorization on any of the twelve protected handlers | Of the fourteen handlers, twelve require a bearer token and two are public, at `backend/app/api/auth.py:L65` and `:L102`, and the twelve split four ways. Three attempt an owner comparison, at `backend/app/api/documents.py:L92`, `:L121` and `:L147`, each raising 403 at `:L93`, `:L122` and `:L148`, and none of the three reaches its comparison. Two are self-scoped by the token, at `backend/app/api/users.py:L20` and `:L33`, and one is the create path at `backend/app/api/documents.py:L46`, which fails before it persists. Six leave object scope unestablished, and the paragraph below takes each group in turn | Bearer authentication alone decides access on the document list handler and the five template handlers, and none of the six can be shown to scope its result to the caller. No object check is enforced anywhere today |

The twelve protected handlers do not all mean the same thing, and entry 12 counts only the ones where
the absence matters. Four groups divide them.

- **Self-scoped by the token, two handlers.** `backend/app/api/users.py:L20` returns
  `current_user` itself and `:L33` updates `current_user.id`, so each handler addresses the token's
  own subject and no path parameter can name another account. No owner check is missing from these
  two, because no other user's object is addressable.
- **Blocked before persistence, one handler.** `backend/app/api/documents.py:L46` passes
  `current_user`, a `User` object, where `backend/app/services/document_service.py:L42` declares
  `user_id: str`. The Firestore client cannot encode a Pydantic model into a stored value, so the
  write at `backend/app/services/document_service.py:L73` raises before it is sent. No document is
  stored, so the create path establishes no owner at all rather than establishing the caller as the
  owner.
- **Unestablished, six handlers.** `backend/app/api/documents.py:L65` calls
  `DocumentService.get_documents`, which the class does not define, so what the list handler would
  return cannot be read from this repository. The five template handlers delegate to an absent
  `TemplateService`, as entry 11 records. Whether any of the six scopes its result to the caller
  depends on code a repair supplies.
- **Attempted and blocked, three handlers.** The three document comparisons do not run to
  completion. Each reads `.user_id` from a value the service returns, while
  `backend/app/schema/document.py:L28` declares the field as `owner_id`. The call-site defects at
  [G5](#g5-call-site-contract-violations) stop the enclosing handlers before the comparison is
  reached.

The accurate accounting is fourteen handlers, twelve protected and two public. The twelve split into
three attempted object checks, two self-scoped handlers, one create path blocked before persistence,
and six whose scope is unestablished. Zero object checks are enforced today.

### G9.2 The frontend client

The client cannot build, for the reasons at [G8 type-check profile](#the-verified-type-check-profile). The controls below
are absent from its source regardless.

| # | Absent control | Evidence | What the absence permits |
|---|----------------|----------|--------------------------|
| 13 | Storage of the bearer token outside script-readable persistence | `frontend/src/services/auth.ts:L38` writes the login response value to `localStorage`, which persists past the tab and is readable by any script on the origin. Nothing reads it back. `frontend/src/services/api.ts:L40` reads `auth.token` from the Redux store instead, a key `frontend/src/store/index.ts` never registers, so the request interceptor throws and no request carries an `Authorization` header. The two stores are disconnected, and the write itself stores the string `"undefined"` today, because `frontend/src/services/auth.ts:L37` reads `accessToken` from a response that returns `access_token` | Any injected or third-party script on the origin reads whatever the write persists, and it survives the session. Reconciling the field name and the store turns that value into a live bearer token in the same place |
| 14 | Redaction before an error is logged | `frontend/src/services/auth.ts:L57`, `frontend/src/pages/Editor.tsx:L53` and `:L86`, `frontend/src/pages/Templates.tsx:L65` and `frontend/src/pages/Settings.tsx:L54` each pass a whole error object to `console.error`. An Axios error carries the request configuration, which includes the `Authorization` header, the full URL and the request body | Nothing leaks today, because the client cannot build and no request carries a token. Once the blockers clear, any failed request whose configuration holds a bearer token or a document body puts both in the browser console and in anything that collects from it |
| 15 | A request timeout or a cancellation path | `frontend/src/services/api.ts:L32-L34` creates the Axios instance with a `baseURL` and no `timeout`, and no call site passes an `AbortSignal` | A request hangs indefinitely, and no in-flight request can be withdrawn |
| 16 | Ordering protection on the auto-save path | `frontend/src/pages/Editor.tsx:L91` schedules a save five seconds after the last edit, and nothing tracks whether an earlier save is still in flight | A slower earlier save can land after a later one and overwrite newer content |
| 17 | Any applied response validation | Four Zod object schemas exist across the three modules under `frontend/src/schema/`, and no module passes a server response through any of them. `frontend/src/services/auth.ts:L72` asserts `as User` instead, which is a compile-time claim that checks nothing at runtime | Server responses are trusted unvalidated, and a schema that exists gives no protection |
| 18 | An allow-list on remote image sources | `frontend/src/components/Header.tsx:L52` renders `currentUser.avatar` and `frontend/src/pages/Templates.tsx:L100` renders `template.thumbnail`, both as an unconstrained `src`. Neither carries a `referrerPolicy`, and no Content Security Policy is committed | A stored URL causes the browser to contact an arbitrary host, disclosing the viewer address and referrer to it |

One frontend absence is easy to misread. `frontend/src/utils/validation.ts` expresses its email and
password rules correctly, and it is still not a control. The module cannot resolve its `zod` import,
no other module calls either function, and a client-side check never binds a caller who does not use
the client. [../frontend/src/utils/README.md](../frontend/src/utils/README.md) records all four
conditions.

### G9.3 Collaboration, background jobs and signed links

None of these paths executes as committed. Each entry names the absent control and the reason the
path does not run, because both facts matter to whoever repairs it.

The last column is conditional throughout, and the condition is not a detail. No route constructs the
collaboration service and no producer enqueues a task, so every entry below describes what a caller
would face rather than what a caller faces. Each cell states the guarantee the method itself does not
make. Whether a repair leaves that gap open depends on the route or the producer it adds, because a
caller could establish the identity and the authorization the method never checks.

| # | Absent control | Evidence | What the method does not guarantee, and what a caller would therefore have to supply |
| --- | ---------------- | ---------- | --------------------------------------------- |
| 19 | Authentication on the collaboration handshake | `backend/app/services/collaboration_service.py:L44` accepts `websocket`, `document_id` and `user_id` as plain arguments, and no route constructs the service, so nothing verifies a token before a socket is registered at `:L64-L66` | The method establishes no identity. The method registers whatever `user_id` string it receives, so the caller has to prove that identity before calling. A route that forwarded a client-supplied value would let a client join as any identity |
| 20 | Authorization against the document being joined | The same method never checks that `user_id` may read `document_id` before it derives a topic at `:L69` and a subscription at `:L70` | The method performs no ownership or membership check. A caller has to authorize the pair itself, and a route that did not would join any caller to any document identifier |
| 21 | Validation of `document_id` before it names a broker resource | `:L69` and `:L70` interpolate the value straight into Pub/Sub resource paths, and `:L103` does the same on disconnect | The method validates no format and consults no allow-list, so an unvalidated identifier reaches a resource path. A caller has to constrain the value before the interpolation happens |
| 22 | A payload schema and a size bound on broadcast changes | `:L133` declares `change: dict` with no model behind it, and `:L152` serialises whatever arrives with `json.dumps` | Arbitrary unbounded structures are published to every subscriber |
| 22a | Per-connection identity in the socket registry, so two sessions for one user can coexist | `:L66` keys `active_connections` by `user_id` rather than by connection, so a second socket for the same document and user replaces the first without closing it. Both sockets resolve to one subscription name at `:L70`, so the second `create_subscription` at `:L73` answers `AlreadyExists`, which `:L76` prints before `:L77` returns. On disconnect, `:L124` rebuilds that same shared name and `:L126` deletes it | A second session evicts the first from the registry and receives no feed itself, and either session closing deletes the subscription the other still depends on. Holding both would need a unique connection identifier per socket and subscription ownership that is reference counted or idempotent |
| 23 | Producer authentication and authorization on the Celery broker | `backend/app/tasks/background_tasks.py:L22` builds the Celery application from `settings.REDIS_URL` alone. No committed file gives that setting a value and no service provides Redis. The transport security, the access control list and the credentials a deployment would use are therefore all unestablished here. The URL could encode a password or select `rediss://`, and nothing tracked says whether it does. See [G8 no Redis broker](#no-redis-service-backs-the-celery-broker) | Anyone who reaches the broker enqueues work that workers execute, and no committed control stands in the way |
| 24 | Format allow-listing and idempotency on the export task | `:L25` accepts `export_format` and `:L63` interpolates it into the object key `exports/{user_id}/{document_id}.{export_format}`. No allowed-value check and no deduplication key exists | A caller influences the stored object path, and a replayed message repeats the work |
| 25 | An authorization check before a signed link is minted | `backend/app/services/export_service.py:L66-L70` and `:L98-L102` generate a v4 signed URL immediately after upload, with no check that the requester may read the document | A link is issued to whoever reached the call |
| 26 | A reviewed expiry and a protected signing credential | The two v4 calls read `settings.SIGNED_URL_EXPIRATION`, a field `backend/app/core/config.py:L40-L48` never declares. `backend/app/tasks/background_tasks.py:L67` signs with `expiration=timedelta(hours=1)` and passes no `version`, so the two paths do not even agree on a signing scheme | A signed URL is a bearer credential, and possession alone authorises the read for the whole validity window |

Entries 25 and 26 describe code that never runs. `backend/app/tasks/background_tasks.py:L59` calls
`convert_document` on the export service, and
[G2 absent methods](#absent-methods-on-classes-that-exist) records that the class never defines that method. The
task therefore raises before it reaches any upload or any signing call. `export_to_pdf` and `export_to_docx`
have no caller in `backend/app/` at all. No signed URL is produced by this repository today.

### G9.4 Supply chain and workflow identity

| # | Absent control | Evidence | What the absence permits |
| --- | ---------------- | ---------- | -------------------------- |
| 27 | Immutable action references | `.github/workflows/ci.yml:L13` and `:L15` and `.github/workflows/cd.yml:L11` and `:L13` each name a mutable tag. A tag can be moved or deleted by whoever controls the action repository, so a tag is a reference and not a pin. Only a full-length commit SHA is immutable, which is [GitHub's own position](https://docs.github.com/en/actions/reference/security/secure-use). In the March 2025 compromise of `tj-actions/changed-files`, tags v1 through v45.0.7 were repointed at a single malicious commit on 14 and 15 March 2025. The fix shipped in v46.0.1 ([CVE-2025-30066](https://github.com/advisories/GHSA-mrrh-fwg8-r2c3), [CISA alert](https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction)) | A third party changes the code your workflow runs without any change to this repository |
| 28 | A pinned runner and pinned base images | Both workflows request `ubuntu-latest`, at `ci.yml:L11` and `cd.yml:L9`. `infrastructure/docker/backend.Dockerfile:L2`, `frontend.Dockerfile:L2` and `:L20`, and `infrastructure/docker/docker-compose.yml:L31` each name a mutable tag rather than an `image@sha256:` digest | The build environment and the image contents change underneath an unchanged repository |
| 29 | A least-privilege `permissions:` block | Neither workflow file declares `permissions:` at any level, so `GITHUB_TOKEN` receives whatever default the repository or organisation sets. Neither default is committed, so the scope each job actually receives is unknown from this tree | Least privilege is neither explicit nor auditable. Add a `permissions:` block to each job so the scope is stated in the file rather than inherited from a setting no reviewer can see here |
| 30 | Short-lived federated credentials | `.github/workflows/cd.yml:L16` supplies `GCP_SA_KEY`, a long-lived user-managed service account key held as a secret. Workload Identity Federation exchanges the workflow OIDC token for a short-lived credential and stores no key, and an attribute condition on the provider restricts which workflow may complete that exchange. No federation configuration is committed | A single leaked secret grants standing access until someone notices and rotates it |
| 31 | Any credential rotation or expiry mechanism | No workflow, script or Terraform file references key rotation, expiry or an age bound on `GCP_SA_KEY`. The key's role, age and expiry are not determinable from this repository. A user-managed service account key does not expire on its own, and only an organization policy or an external process outside these files could bound it | Nothing in the repository limits how long the key remains usable, and no committed file records whether anything outside it does |
| 32 | A gate between integration and deployment | `.github/workflows/cd.yml:L3-L5` triggers on every push to `main` and declares no `needs:`, no `workflow_run` and no `environment` | A deploy proceeds without the CI job passing and without an approval step |

### G9.5 Secrets, state and data retention

| # | Absent control | Evidence | What the absence permits |
| --- | ---------------- | ---------- | -------------------------- |
| 33 | Any ignore rule protecting generated state | No `.gitignore`, `.dockerignore` or `.terraformignore` is tracked anywhere in this repository. `infrastructure/terraform/main.tf` declares no `backend` block, so state is written locally, and Terraform state records resource attributes in clear text | A local state file, which can contain secret values, is one `git add` away from the history |
| 33a | A `.dockerignore` bounding either build context | No `.dockerignore` is tracked anywhere, so a `docker build` sends the whole named directory to the daemon as its [build context](https://docs.docker.com/build/concepts/context/). `infrastructure/docker/frontend.Dockerfile:L14` then runs `COPY . .`, copying that entire context into the build stage on top of the `node_modules` its own `npm ci` at `:L11` installed | A local `frontend/node_modules`, a local `.env` and any key file in the tree are uploaded to the daemon and written into a build layer. The final stage copies only `/app/build` at `:L23`, so the shipped image is clean while the build cache is not. A host `node_modules` also silently replaces the one the image installed |
| 34 | A secret allow-list or a preflight on the deploy archive | `scripts/deploy.sh:L19` runs `zip -r app.zip . -x "*.git*" -x "node_modules/*" -x "venv/*"`, a deny-list of three patterns, and `:L23` uploads the archive with `gsutil cp`. Any `.env`, key file, credential or state file outside those three patterns is included | Local secrets leave the machine inside a deployed artifact |
| 35 | Failure handling in the deploy script | `scripts/deploy.sh` sets no `set -e`, installs no `trap` and inspects `$?` nowhere. Its only guard is the credentials check at `:L4-L7`. `:L47` prints `Deployment completed successfully!` unconditionally | Every stage failure is ignored, and the run reports success after failing |
| 36 | A retention or lifecycle rule on stored objects | `infrastructure/terraform/main.tf:L56-L58` enables bucket versioning and declares no `lifecycle_rule`. A delete or an overwrite on a versioned bucket archives the current generation instead of removing the bytes. No committed source file reads this bucket, because `main.tf:L51` names it `word-documents-${var.project_id}` and that name appears in no other tracked file | Prospective. Once user content is stored here and an object-delete path is connected, deleted content stays retrievable from archived generations until a lifecycle rule or a generation-level delete removes it. `DocumentService.delete_document` reaches no bucket today (`backend/app/services/document_service.py:L187-L188`) |
| 37 | Two credential literals safe to commit | `infrastructure/docker/docker-compose.yml:L35` sets `POSTGRES_PASSWORD=password`, and `scripts/setup_dev_environment.sh:L32` creates a database user with the same literal. Compose maps no port for the database service, which limits reach and does not make either literal safe | A committed credential is reused in an environment that is reachable |
| 38 | A supported runtime on any of three declared versions | Python 3.9 reached end of support on 31 October 2025 and is named at `infrastructure/docker/backend.Dockerfile:L2`. Node.js 14 left support on 30 April 2023, with its final release 14.21.3 shipped on 16 February 2023, and is named at `.github/workflows/ci.yml:L17` and `infrastructure/docker/frontend.Dockerfile:L2`. PostgreSQL 13 reached end of life on 13 November 2025 and is named at `infrastructure/docker/docker-compose.yml:L31` | Three components receive no security patches, and no future vulnerability in any of them will be fixed upstream |
| 39 | Any committed transport security or security headers | `infrastructure/docker/frontend.Dockerfile:L20` serves through `nginx:alpine`, and `:L26` leaves the `COPY nginx.conf` line commented out. No `nginx.conf` is tracked, so no TLS configuration, no HSTS, no Content Security Policy and no proxy rule is committed | The served client carries no transport or header protection from anything in this repository |
| 39a | A non-root runtime user in either image | No `USER` instruction appears in `infrastructure/docker/backend.Dockerfile` or in either stage of `infrastructure/docker/frontend.Dockerfile`. `python:3.9-slim` (`backend.Dockerfile:L2`), `node:14-alpine` (`frontend.Dockerfile:L2`) and `nginx:alpine` (`:L20`) all default to root, so Uvicorn at `backend.Dockerfile:L20` and the Nginx master at `frontend.Dockerfile:L32` both start as uid 0. The `nginx:alpine` default configuration carries `user nginx;`, and `:L26` leaves the `COPY nginx.conf` override commented out, so the master drops its worker processes to the unprivileged `nginx` user | The backend process and the Nginx master run as root, so an exploited one begins with root inside the container, and with host root wherever the runtime is not user-namespaced. Nginx workers are the one exception, since the image default drops them to an unprivileged user. Closing it needs a `USER` with a non-root uid in each final stage |
| 39b | Any containment or resource bound on a Compose service | `infrastructure/docker/docker-compose.yml` declares no `user:`, `read_only:`, `cap_drop:`, `security_opt:`, `pids_limit:`, `mem_limit:` or `cpus:`, and no `deploy.resources.limits` block | Each of the three services keeps the default Linux capability set, a writable root filesystem, and unbounded CPU, memory and process count. One runaway container can then exhaust the host, and a compromised one can raise its own privileges. Closing it needs capabilities dropped to only what each service uses, `no-new-privileges`, a read-only root filesystem with explicit writable `tmpfs` paths, and per-service CPU and memory limits |
| 40 | A network rule narrower than the whole subnet | `infrastructure/terraform/main.tf:L35` declares a firewall rule opening TCP ports 0 through 65535 across the subnet range | Every port on every instance in the subnet is reachable from every other address in it |

### Where these entries are owned

Each module README carries the subset that applies to its own directory, with the same file and line locators.
Start there when you are working inside one directory rather than surveying the whole repository.

All 44 entries are owned, and the four sub-lettered ones sit with the entry they extend. An entry whose evidence spans two
directories is owned by both, which is why entries 14 and 18 appear twice below. Four of the eleven READMEs carry an
`Absent security controls` heading that cites these entry numbers directly: `backend/app/services`, `frontend/src/pages`,
`frontend/src/components` and `frontend/src/services`. The other seven fold the same material into their own Known
Limitations numbering, so match them on the locator rather than on the entry number.

- [../backend/app/api/README.md](../backend/app/api/README.md) owns entries 1 through 12
- [../backend/app/core/README.md](../backend/app/core/README.md) owns entries 8 through 10
- [../frontend/src/services/README.md](../frontend/src/services/README.md) owns entries 13 through 15 and 17
- [../frontend/src/pages/README.md](../frontend/src/pages/README.md) owns entries 14, 16 and 18
- [../frontend/src/components/README.md](../frontend/src/components/README.md) owns entry 18, for the `Header.tsx:L52` call site
- [../backend/app/services/README.md](../backend/app/services/README.md) owns entries 19 through 22, 22a, 25 and 26
- [../backend/app/tasks/README.md](../backend/app/tasks/README.md) owns entries 23 and 24
- [../.github/workflows/README.md](../.github/workflows/README.md) owns entries 27 through 32
- [../infrastructure/terraform/README.md](../infrastructure/terraform/README.md) owns entries 33, 36 and 40
- [../scripts/README.md](../scripts/README.md) owns entries 34 and 35
- [../infrastructure/docker/README.md](../infrastructure/docker/README.md) owns entries 28, 33a, 37, 38, 39, 39a and 39b

[integration-guide.md](integration-guide.md#collaboration-trust-boundary) carries the collaboration
and signed-link trust boundaries in full.
[deployment-guide.md](deployment-guide.md#operations-risk-register) carries the operations risk
register covering entries 27 through 32 and 38.

## Documentation inaccuracies in the root README

[The root README](../README.md) carries six statements the committed tree contradicts, one of them only
in part. Three sit under the README's own `### Installation` and `### Running the application` headings,
at `L29`, `L42` and `L55`, so a developer following the file in order hits all three before reaching
any code.

The engagement that produced this register placed the root README out of scope, so this register
records the six entries rather than correcting them in place. The scope entry belongs in
[decision-log.md](decision-log.md), which records it as decision row 1.

| Line | Claim | Reality |
| ------ | ------- | --------- |
| `README.md:L29` | `git clone https://github.com/your-organization/microsoft-word.git` | A placeholder organisation. The command cannot succeed as written |
| `README.md:L42` | `pip install -r requirements.txt`, run from `backend/` | No `requirements.txt` exists anywhere in the repository, per [G4 no backend manifest](#the-backend-has-no-dependency-manifest) |
| `README.md:L55` | `uvicorn main:app --reload`, run from `backend/` after `cd backend` at `L54` | The application object sits at `backend/app/main.py:L24`, one directory deeper. From `backend/`, the target is `app.main:app` |
| `README.md:L59-L66` | A project structure listing a root-level `docs/` at `L64` and a root-level `tests/` at `L65` | Half true as of this documentation set. A root-level `docs/` now exists, created by this engagement, so `L64` describes the tree correctly. No root-level `tests/` exists and this engagement creates none, so `L65` stays false. The only test modules sit at `backend/tests/`. Both halves are expanded below the table |
| `README.md:L81` | Claims an MIT licence and links to a licence file | No `LICENSE` file is committed, so the README's link resolves to nothing. This register quotes that markup as code rather than reproducing it, so no broken link appears here. `frontend/package.json` declares no `license` field either |
| `README.md:L86-L87` | `John Doe` and `Jane Smith` as project maintainers, with `example.com` addresses | Placeholder contacts |

Two notes on the structure claim at `../README.md:L59-L66`, because the two halves of it diverge once
this documentation set lands.

The `docs/` claim at `L64` becomes accidentally true. A root-level `docs/` directory now exists,
created by this engagement, so the line describes the tree correctly by coincidence rather than by
correction. Nobody edited the README to make it so.

The `tests/` claim at `L65` stays false. No root-level `tests/` directory exists, and this
engagement creates none. `scripts/deploy.sh:L15` runs `python -m pytest tests/` against that absent
path.

Prerequisites at `README.md:L22-L23` are accurate as written. Read them beside the
[runtime version table](#runtime-versions-are-declared-three-ways-and-enforced-nowhere), which records
that neither of those two floors is enforced anywhere and that both have passed end of life.

## The complete marker and TODO register

The code's authors left 33 `HUMAN ASSISTANCE NEEDED` markers and 16 `TODO` comments. Read them as a
backlog written by the people who wrote the code, because each one names a gap its author already
knew about.

### Distribution

| Area | Markers | TODOs |
| ------ | --------- | ------- |
| `backend/app/` | 9 | 6 |
| `frontend/src/` | 16 | 9 |
| `infrastructure/terraform/` | 2 | 0 |
| `backend/tests/` | 3 | 0 |
| `infrastructure/docker/` | 1 | 0 |
| `scripts/` | 2 | 1 |
| **Total** | **33** | **16** |

A second pair of figures, 27 and 15, counts the subset inside the 44 inline-documented files and
measures a preservation obligation, not the coverage denominators used here.

### Backend application markers and TODOs

| Location | Kind | What it flags | Class |
| ---------- | ------ | --------------- | ------- |
| `backend/app/main.py:L38` | marker | Low confidence in the startup and shutdown block below it | [G2 settings singleton](#the-absent-settings-singleton) |
| `backend/app/main.py:L49` | TODO | Database migration logic is unimplemented, inside the startup handler that awaits the absent `init_db` | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `backend/app/main.py:L72` | TODO | Shutdown cleanup tasks are unimplemented | none |
| `backend/app/api/users.py:L54` | marker | The code assumes a `UserService` class with an `update_user` method, and asks for verification | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `backend/app/core/security.py:L115` | marker | `get_current_user` needs review for its integration with the `User` model and `UserService`, neither of which this module imports | [G3](#g3-undefined-names-that-raise-at-execution) |
| `backend/app/services/document_service.py:L114` | marker | Asks for error handling and validation on `update_document`, the method the router calls with two arguments against three parameters | [G5 argument count](#argument-count-and-type) |
| `backend/app/services/collaboration_service.py:L42` | marker | `connect` carries a stated confidence of 0.6 and is not production ready | [G7 collaboration path](#the-collaboration-path-has-no-route-and-two-protocols) |
| `backend/app/services/collaboration_service.py:L135` | marker | `broadcast_change` carries a stated confidence of 0.7 and is not production ready | [G3](#g3-undefined-names-that-raise-at-execution) |
| `backend/app/services/export_service.py:L38` | marker | Both export methods have a low confidence score and need implementation detail or error handling | [G2 absent methods](#absent-methods-on-classes-that-exist) |
| `backend/app/services/export_service.py:L57` | TODO | PDF conversion logic is unimplemented | [G2 absent methods](#absent-methods-on-classes-that-exist) |
| `backend/app/services/export_service.py:L62` | TODO | The literal `"PDF_CONTENT"` uploaded at `:L63` stands in for a real document | [G2 absent methods](#absent-methods-on-classes-that-exist) |
| `backend/app/services/export_service.py:L89` | TODO | DOCX conversion logic is unimplemented | [G2 absent methods](#absent-methods-on-classes-that-exist) |
| `backend/app/services/export_service.py:L94` | TODO | The literal `"DOCX_CONTENT"` uploaded at `:L95` stands in for a real document | [G2 absent methods](#absent-methods-on-classes-that-exist) |
| `backend/app/tasks/background_tasks.py:L49` | marker | `process_document_export` needs review for production readiness and error handling | [G2 absent methods](#absent-methods-on-classes-that-exist) |
| `backend/app/tasks/background_tasks.py:L91` | marker | `cleanup_expired_documents` needs review for readiness, error handling and optimisation | [G3](#g3-undefined-names-that-raise-at-execution), [G5 other violations](#other-contract-violations) |

### Frontend markers and TODOs

| Location | Kind | What it flags | Class |
| ---------- | ------ | --------------- | ------- |
| `frontend/src/components/DocumentCanvas.tsx:L20` | marker | Component confidence below 0.8, on the component carrying the two inverse type errors | [G5 canvas type inversion](#type-inversions-in-the-editor-canvas) |
| `frontend/src/components/ImageEditor.tsx:L30` | marker | `handleInsertImage` needs review for production readiness | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `frontend/src/components/ImageEditor.tsx:L59` | marker | The component's rendered structure is unimplemented | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `frontend/src/components/TableEditor.tsx:L29` | marker | `handleInsertTable` carries a stated confidence of 0.6 | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `frontend/src/components/TextEditor.tsx:L26` | marker | `handleKeyCommand` needs review for production readiness | none. The module calls both formatting helpers correctly |
| `frontend/src/components/Toolbar.tsx:L19` | marker | The component needs refinement and error handling | [G5 argument count](#argument-count-and-type) |
| `frontend/src/components/Toolbar.tsx:L67` | TODO | Insert functionality is unimplemented, so the button at `:L84` does nothing | none |
| `frontend/src/pages/Editor.tsx:L20` | marker | The page needs review for production readiness | [G5 argument count](#argument-count-and-type) |
| `frontend/src/pages/Editor.tsx:L54` | TODO | Document load errors reach the console only | none |
| `frontend/src/pages/Editor.tsx:L87` | TODO | Auto-save errors reach the console only, with no user notification | none |
| `frontend/src/pages/Settings.tsx:L18` | marker | The page needs refinement for production readiness | [G2 absent frontend exports](#absent-frontend-exports) |
| `frontend/src/pages/Settings.tsx:L52` | TODO | No success message follows a settings save | none |
| `frontend/src/pages/Settings.tsx:L55` | TODO | Save errors produce no user feedback | none |
| `frontend/src/pages/Templates.tsx:L66` | marker | Carries no body text of its own and sits directly above the TODO at `:L67`, on the template fetch path | [G2 absent frontend exports](#absent-frontend-exports) |
| `frontend/src/pages/Templates.tsx:L67` | TODO | Template fetch errors have no handling or user feedback | none |
| `frontend/src/pages/Templates.tsx:L83` | marker | Carries no body text of its own and sits directly above the TODO at `:L84`, on template selection | [G6 divergence table](#field-and-shape-divergences) |
| `frontend/src/pages/Templates.tsx:L84` | TODO | Selecting a template navigates nowhere, so the card click is terminal | none |
| `frontend/src/services/collaboration.ts:L48` | marker | Inbound collaboration event listeners are unimplemented, inside the otherwise empty `setupEventListeners` body | [G7 collaboration path](#the-collaboration-path-has-no-route-and-two-protocols) |
| `frontend/src/services/collaboration.ts:L54` | marker | `joinDocument` emits an event no server route receives | [G7 collaboration path](#the-collaboration-path-has-no-route-and-two-protocols) |
| `frontend/src/services/collaboration.ts:L81` | marker | `sendChanges` emits a payload shape the server does not expect | [G7 collaboration path](#the-collaboration-path-has-no-route-and-two-protocols) |
| `frontend/src/store/documentSlice.ts:L95` | marker | The slice lacks asynchronous actions and error handling for document fetch and save | [G2 absent frontend exports](#absent-frontend-exports) |
| `frontend/src/store/userSlice.ts:L78` | marker | Names three gaps directly, including an `updateUser` action and selectors for state access, both of which four modules already import | [G2 absent frontend exports](#absent-frontend-exports) |
| `frontend/src/utils/documentUtils.ts:L17` | marker | Both functions need error handling, and states that the `DocumentSchema` validation needs to be implemented correctly | [G5 other violations](#other-contract-violations) |
| `frontend/src/utils/documentUtils.ts:L33` | TODO | `DocumentSchema` validation in `serializeDocument` is unimplemented | [G5 other violations](#other-contract-violations) |
| `frontend/src/utils/documentUtils.ts:L58` | TODO | `DocumentSchema` validation in `deserializeDocument` is unimplemented | [G5 other violations](#other-contract-violations) |

### Test suite markers

These three sit in files that receive no inline documentation. See
[../backend/tests/README.md](../backend/tests/README.md).

| Location | Kind | What it flags | Class |
| ---------- | ------ | --------------- | ------- |
| `backend/tests/test_api.py:L13` | marker | The test database connection is unconfigured. The fixture body directly below is a bare `pass` at `:L14` | [G1 test-suite modules](#modules-referenced-only-by-the-test-suite) |
| `backend/tests/test_api.py:L77` | marker | Endpoint coverage is incomplete, with no edge cases and no error scenarios | [G1 test-suite modules](#modules-referenced-only-by-the-test-suite) |
| `backend/tests/test_db.py:L56` | marker | Update, delete and error-handling cases are absent | [G1 test-suite modules](#modules-referenced-only-by-the-test-suite) |

### Infrastructure, container and script markers

| Location | Kind | What it flags | Class |
| ---------- | ------ | --------------- | ------- |
| `infrastructure/terraform/main.tf:L94` | marker | Asks for review of the subnet range, of whether more firewall rules are needed, and of the bucket configuration. The firewall it points at opens every TCP port to the subnet | [G8 other Terraform defects](#other-terraform-defects) |
| `infrastructure/terraform/outputs.tf:L58` | marker | States that the outputs may not match the resources the configuration actually creates. Every output reads an AWS address, and the only provider is `google` | [G8 Terraform outputs](#terraform-outputs-describe-a-different-cloud) |
| `infrastructure/docker/backend.Dockerfile:L22` | marker | Asks for verification that `requirements.txt` sits in the right place and that the application code is in `./app`. Neither holds: no `requirements.txt` exists, and `:L14` flattens the package | [G8 backend image](#the-backend-image-cannot-build-or-start) |
| `scripts/deploy.sh:L37` | marker | Post-deployment checks are unimplemented, so `:L47` reports success unconditionally | [G8 setup script](#the-setup-script-targets-the-wrong-framework) |
| `scripts/setup_dev_environment.sh:L41` | marker | Environment configuration needs manual completion, immediately after `:L40` copies an `.env.example` that does not exist | [G8 setup script](#the-setup-script-targets-the-wrong-framework) |
| `scripts/setup_dev_environment.sh:L42` | TODO | The `.env` file needs production values, in a file the preceding line failed to create | [G8 setup script](#the-setup-script-targets-the-wrong-framework) |

## Where to go next

| Question | Document |
| ---------- | ---------- |
| What can I run today, and what should I fix first? | [onboarding.md](onboarding.md) |
| How do the six top-level areas fit together? | [architecture-overview.md](architecture-overview.md) |
| Which contract is authoritative for a given field? | [data-model.md](data-model.md) |
| Which external services does the code reach, and what blocks each one? | [integration-guide.md](integration-guide.md) |
| Why does a deploy fail? | [deployment-guide.md](deployment-guide.md) |
| Why was something documented this way? | [decision-log.md](decision-log.md) |
| Where is the index for this documentation set? | [README.md](README.md) |
| Does the writing meet the clarity standard? | [prose-validation.md](prose-validation.md) |

The three specification documents record declared intent and never committed behaviour. Read them as
the design the code was aiming at:

- [Technical Specifications](<../documentation/Technical Specifications.md>)
- [Software Requirements Specifications](<../documentation/Software Requirements Specifications (SRS).md>)
- [Software Project Proposal](<../documentation/Software Project Proposal.md>)

One divergence between intent and code is worth naming here, because it looks like a defect and is
not one. The requirements specification calls for a 30-second auto-save at
`documentation/Software Requirements Specifications (SRS).md:L543`, under the requirement group for
file management. The editor implements a five-second debounce at
`frontend/src/pages/Editor.tsx:L91`. The code is internally consistent, and the two documents
disagree. See [../frontend/src/pages/README.md](../frontend/src/pages/README.md).
