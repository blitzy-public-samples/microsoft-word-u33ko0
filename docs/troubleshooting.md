# Troubleshooting and Defect Register

The `microsoft-word-u33ko0` repository does not run. The backend cannot import, and only 3 of the
15 modules under `backend/app/` load. The frontend cannot typecheck, and `tsc --noEmit` reports 76
errors. Neither container builds, the Terraform cannot initialise, and both `npm ci` invocations
fail. Every one of those failures appears below with the file and line that causes it.

Coverage is wider than that opening list. The eight classes below carry every defect this
documentation pass verified against the committed source, and that includes the ones a headline
failure hides: the seven protected handlers registration order makes unreachable, the two credential
prerequisites a version 4 signed URL needs, the Pub/Sub topic nothing creates, the publish error that
is caught and printed rather than raised, the ownership subscript that answers 500 instead of 403, and
the retention sweep's partial-deletion states. A defect is listed here only when a committed line
demonstrates it, so the register grows if someone verifies one this pass did not reach.

This document records defects. Repairing them fell outside the documentation engagement that
produced this file, so that engagement fixed none of them. Read no entry here as fixed.
[decision-log.md](decision-log.md) will hold the record of that boundary, and is planned for a later
checkpoint rather than committed today.

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
- A range such as `backend/app/core/config.py:L111-L119` covers every line in the span,
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
  to [onboarding.md](onboarding.md), which closes with a prioritised task list.
- **No design rationale.** Where this engagement made a judgement, for example declining to name
  any single ownership field canonical, the entry states the judgement and links to
  [decision-log.md](decision-log.md), which is planned for a later checkpoint and not committed yet.
  Arguments belong there rather than here.
- **No specification claims presented as behaviour.** The three documents under `documentation/`
  describe intended behaviour rather than committed behaviour. Anything drawn from them carries the
  label **declared intent** and a citation by heading name plus line, because all three files use
  unnumbered headings only. `documentation/Technical Specifications.md` holds five level-one
  headings: `L3` INTRODUCTION, `L125` SYSTEM ARCHITECTURE, `L300` SYSTEM DESIGN, `L523` TECHNOLOGY
  STACK and `L620` SECURITY CONSIDERATIONS. No numbered section anchor exists inside it. A numbered
  section citation anywhere in this documentation set refers to the generated Technical
  Specification, a separate document, and the text says so when it does.

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
| The interface renders with no styling at all | Viewing the running frontend | [G8](#tailwind-never-compiles) | No `tailwind.config.js`, no `postcss.config.js` and no committed stylesheet |
| `uvicorn main:app --reload` cannot find the application | Starting the backend from `backend/` per the README | [README](#documentation-inaccuracies-in-the-root-readme) | The application object sits at `backend/app/main.py:L24` (`app = FastAPI()`), one directory deeper |
| `ImportError: cannot import name 'settings' from 'app.core.config'` | Importing `app.main` from `backend/` | [G2](#the-absent-settings-singleton) | `backend/app/main.py:L16` reaches `backend/app/api/auth.py:L81`, which requests a name `backend/app/core/config.py` never defines |
| `ModuleNotFoundError: No module named 'app.schema.template'` | Importing `app.api.templates` | [G1](#g1-absent-modules-referenced-by-committed-code) | `backend/app/api/templates.py:L70` |
| `ModuleNotFoundError: No module named 'app.services.user_service'` | Importing `app.api.users` or `app.api.auth` | [G1](#g1-absent-modules-referenced-by-committed-code) | `backend/app/api/users.py:L24` and `backend/app/api/auth.py:L83` |
| `NameError: name 'Optional' is not defined` | Importing `app.core.security` | [G3](#g3-undefined-names-that-raise-at-execution) | `backend/app/core/security.py:L48` uses `Optional` with no import behind it |
| Template endpoints return document responses | Calling any `/{id}` route | [G7](#document-routes-shadow-the-template-and-profile-routes) | `backend/app/main.py:L125-L128` mounts every router with no prefix |
| `GET /me` returns a document read, or 404 for a document called `me` | Fetching the signed-in profile | [G7](#document-routes-shadow-the-template-and-profile-routes) | `backend/app/api/documents.py:L145` claims every single-segment path ahead of `backend/app/api/users.py:L29` |
| `POST /documents` answers 405 while `PUT /documents/{id}` answers 404 | Calling the document API from the client | [G7](#the-client-calls-six-routes-and-no-server-route-matches-any-of-them) | `frontend/src/services/api.ts:L246` and `:L288` prefix a segment no route declares |
| Login answers 422 rather than 401 once the path is corrected | Signing in | [G7](#the-client-calls-six-routes-and-no-server-route-matches-any-of-them) | `frontend/src/services/auth.ts:L146` sends JSON `email`, and `backend/app/api/auth.py:L168` reads a form `username` |
| `npm ci` fails with `EUSAGE` in continuous integration | Running the CI workflow | [G8](#npm-ci-cannot-run-anywhere) | `.github/workflows/ci.yml:L19` runs at the repository root, where no manifest and no lockfile exist |
| `docker compose build` cannot find a Dockerfile | Building the containers | [G8](#compose-points-at-dockerfiles-that-are-not-there) | `infrastructure/docker/docker-compose.yml:L6-L7` and `:L19-L20` |
| `terraform init` reports `Unreadable module directory` | Initialising the infrastructure | [G8](#three-terraform-module-sources-do-not-exist) | `infrastructure/terraform/main.tf:L67`, `:L76`, `:L85`. No `modules/` directory exists |
| Celery workers have no broker to attach to | Running background jobs | [G8](#no-redis-service-backs-the-celery-broker) | `backend/app/tasks/background_tasks.py:L98` reads `settings.REDIS_URL`, and no service provides Redis |
| The deploy step uploads descriptors that do not exist | Running the CD workflow | [G8](#the-cd-workflow-deploys-two-absent-descriptors) | `.github/workflows/cd.yml:L19-L20` deploys `app.yaml` and `dispatch.yaml` |
| An export uploads and then fails to produce a link | Exporting a document once the earlier blockers clear | [G8](#signed-url-generation-needs-credentials-nothing-supplies) | `backend/app/services/export_service.py:L160-L164` signs version 4 with credentials that carry no private key and no `signBlob` grant |
| A collaboration subscribe or publish answers `NotFound` | Opening a second editor on one document | [G7](#nothing-creates-the-pubsub-topic-the-server-addresses) | `backend/app/services/collaboration_service.py:L124` and `:L248` address a topic no code and no infrastructure creates |
| A change publishes silently and never arrives | Editing with collaboration wired up | [G7](#a-failed-publish-is-caught-and-logged-rather-than-raised) | `backend/app/services/collaboration_service.py:L250` catches every publish failure and `:L252` prints it |

## G1 absent modules referenced by committed code

Committed code imports ten application modules that no file provides, and the test suite adds six
more. Each import below resolves to nothing, so the importing module cannot load.

### Application modules

| Absent module | Requested at | Symbols requested | Effect |
| --------------- | -------------- | ------------------- | -------- |
| `app.services.user_service` | `backend/app/api/auth.py:L83`, `backend/app/api/users.py:L24` | `UserService` | Both routers fail to import. `backend/app/core/security.py:L186` also constructs `UserService()` with no import at all, covered in [G3](#g3-undefined-names-that-raise-at-execution) |
| `app.schema.template` | `backend/app/api/templates.py:L70` | `Template`, `TemplateCreate`, `TemplateUpdate` | The template router fails to import. No Pydantic contract for a template exists anywhere in the backend |
| `app.services.template_service` | `backend/app/api/templates.py:L71` | `TemplateService` | The template router has no service tier behind its five handlers |
| `@/components/StylePanel` | `frontend/src/components/Sidebar.tsx:L8` | `StylePanel` | Rendered unconditionally at `Sidebar.tsx:L23` |
| `@/components/CommentPanel` | `frontend/src/components/Sidebar.tsx:L9` | `CommentPanel` | Rendered unconditionally at `Sidebar.tsx:L24` |
| `@/components/RevisionPanel` | `frontend/src/components/Sidebar.tsx:L10` | `RevisionPanel` | Rendered unconditionally at `Sidebar.tsx:L25` |
| `@/utils/tableUtils` | `frontend/src/components/TableEditor.tsx:L26` | `insertTable`, `deleteTable`, `modifyTable` | `handleInsertTable` at `TableEditor.tsx:L67` calls `insertTable`, and no module defines it |
| `@/utils/imageUtils` | `frontend/src/components/ImageEditor.tsx:L30` | `resizeImage`, `cropImage` | Neither import is used in the component body |
| `init_db` from `app.db.sql` | `backend/app/main.py:L22` | `init_db` | `backend/app/db/sql.py` defines `engine`, `SessionLocal`, `Base` and `get_db`, and defines no `init_db`. The startup handler awaits the missing name at `main.py:L60` |
| The `app` package itself | Every `from app.*` import across 12 modules | the `app`, `app.api`, `app.core`, `app.db`, `app.schema`, `app.services` and `app.tasks` namespaces | No `__init__.py` file exists anywhere under `backend/`, so all seven are implicit namespace packages. They resolve only while `backend/` sits on the import path, and `infrastructure/docker/backend.Dockerfile:L14` copies `./app` to `/app`, which flattens the package and leaves the `app.` prefix unresolvable inside the image |

The five frontend rows above carry a second, independent failure. Each specifier uses the `@/`
prefix, which the compiler cannot resolve either, as [G4](#the-unmapped-import-prefix) records.
Creating the five missing files would not clear those five errors on its own.

`backend/app/api/templates.py:L70-L71` is the clearest example of the pattern in the whole
repository: one module, two imports, neither target present. The engagement that produced this
register corrected an earlier attribution of this example to
`backend/app/services/document_service.py`, which carries no such import.
[decision-log.md](decision-log.md) will record that correction, and is planned rather than committed.

Full treatment sits in [../backend/app/api/README.md](../backend/app/api/README.md),
[../frontend/src/components/README.md](../frontend/src/components/README.md) and
[../backend/app/db/README.md](../backend/app/db/README.md).

### Modules referenced only by the test suite

The three modules under `backend/tests/` import five further roots that do not exist, using three
mutually incompatible import conventions. No test in this repository can collect.

| Absent root | Requested at | Import convention |
| ------------- | -------------- | ------------------- |
| `app.models` | `backend/tests/test_api.py:L4` | `app.*`, matching the application source |
| `app.database` | `backend/tests/test_api.py:L5` | `app.*` |
| `backend.db.firestore_operations` | `backend/tests/test_db.py:L6` | `backend.*`, a root the application never uses |
| `backend.db.sql_operations` | `backend/tests/test_db.py:L7` | `backend.*` |
| bare `services.*` and `models.*` | `backend/tests/test_services.py:L3-L7` | no package root at all |

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

`backend/app/core/config.py` defines a `Settings` class at `L51` and a `get_settings()` factory at
`L126`, and it never creates a module-level `settings` instance. The file contains no `settings =`
assignment at any line. Eight modules import that name:

| Importing module | Line |
| ------------------ | ------ |
| `backend/app/main.py` | `L20` |
| `backend/app/api/auth.py` | `L81` |
| `backend/app/db/firestore.py` | `L36` |
| `backend/app/db/sql.py` | `L14` |
| `backend/app/services/collaboration_service.py` | `L39` |
| `backend/app/services/document_service.py` | `L60` |
| `backend/app/services/export_service.py` | `L61` |
| `backend/app/tasks/background_tasks.py` | `L92` |

Each import raises `ImportError: cannot import name 'settings' from 'app.core.config'`.
`backend/app/core/security.py:L43` imports `get_settings` instead, which exists, so that module's
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

`app.main` surfaces its failure at `backend/app/api/auth.py:L81`, reached through
`backend/app/main.py:L16`. Two modules fail indirectly through the Firestore adapter:
`app.api.documents` and `app.services.document_service` both surface at
`backend/app/db/firestore.py:L36`. See [../backend/app/README.md](../backend/app/README.md), which
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

All four names are then passed to `include_router` at `backend/app/main.py:L125-L128`.

### Absent methods on classes that exist

| Symbol | Called at | Defined on |
| -------- | ----------- | ------------ |
| `DocumentService.get_documents` | `backend/app/api/documents.py:L142` | nothing. `DocumentService` defines `create_document` at `backend/app/services/document_service.py:L72`, `get_document` at `:L123`, `update_document` at `:L183` and `delete_document` at `:L252` |
| `ExportService.convert_document` | `backend/app/tasks/background_tasks.py:L138` | nothing. `ExportService` defines `export_to_pdf` (`L87`) and `export_to_docx` (`L168`) |

### Absent frontend exports

`frontend/src/schema/document.ts` omits **three requested names**, not one. Consumers ask for
`Document`, `DocumentCreate` and `DocumentUpdate` across five positions, and the module declares none
of the three. Its two exports are both Zod schema values, `DocumentSchema` at `L65` and
`DocumentVersionSchema` at `L86`, and it exports **no inferred type**. Both sibling schema modules do
export one: `frontend/src/schema/user.ts:L56` and `frontend/src/schema/template.ts:L40` each end with
a `z.infer` declaration. The three omissions together produce five of the six `TS2305` errors in the
whole frontend, because the compiler reports one error per requested name per import statement.

| Requested name | Requested at | Positions | What closing it needs |
|----------------|--------------|-----------|------------------------|
| `Document` | `frontend/src/services/api.ts:L80`, `frontend/src/services/collaboration.ts:L15`, `frontend/src/store/documentSlice.ts:L22` | 3 | One line. `DocumentSchema` already exists at `frontend/src/schema/document.ts:L65`, so a `z.infer` export beside it closes all three positions at once |
| `DocumentCreate` | `frontend/src/services/api.ts:L80` | 1 | A schema first. No Zod object in the module models a creation payload, so nothing exists to infer from. `backend/app/schema/document.py:L68` declares the server-side equivalent |
| `DocumentUpdate` | `frontend/src/services/api.ts:L80` | 1 | A schema first. `backend/app/schema/document.py:L82` declares the server-side equivalent and inherits nothing, so neither side holds a field list to mirror |

| Requested symbol | Requested at |
| ------------------ | -------------- |
| `Document`, `DocumentCreate`, `DocumentUpdate` | `frontend/src/services/api.ts:L80` |
| `Document` | `frontend/src/services/collaboration.ts:L15` |
| `Document` | `frontend/src/store/documentSlice.ts:L22` |

`frontend/src/store/index.ts` omits two hooks that seven modules import, and registers neither of
two named exports its consumers expect:

| Absent symbol | Expected from | Requested at |
| --------------- | --------------- | -------------- |
| `useAppSelector`, `useAppDispatch` | `frontend/src/store/index.ts` | seven modules across the four pages and three components |
| `documentReducer` | `frontend/src/store/documentSlice.ts` | `frontend/src/store/index.ts:L21`. The slice exports its reducer as the module default at `frontend/src/store/documentSlice.ts:L169` |
| `userReducer` | `frontend/src/store/userSlice.ts` | `frontend/src/store/index.ts:L22`. The slice exports its reducer as the module default at `frontend/src/store/userSlice.ts:L147` |
| `updateDocument`, `selectCurrentDocument` | `frontend/src/store/documentSlice.ts` | `frontend/src/components/DocumentCanvas.tsx:L23`, `frontend/src/components/Toolbar.tsx:L24`. The slice exports exactly six actions at `frontend/src/store/documentSlice.ts:L154-L161`, and `updateDocument` is not among them |
| `updateUser`, `selectCurrentUser` | `frontend/src/store/userSlice.ts` | `frontend/src/pages/Settings.tsx:L33`, plus `selectCurrentUser` at `frontend/src/components/Header.tsx:L23`, `frontend/src/pages/Home.tsx:L23` and `frontend/src/pages/Templates.tsx:L37`. The slice exports `setUser`, `clearUser`, `setLoading` and `setError` at `frontend/src/store/userSlice.ts:L139` |
| `getDocument`, `updateUserSettings` | `frontend/src/services/api.ts` | `frontend/src/pages/Editor.tsx:L25` and `frontend/src/pages/Settings.tsx:L31`. The module exports only `getDocuments` (`frontend/src/services/api.ts:L217`), `createDocument` (`:L245`) and `updateDocument` (`:L287`) |
| `getTemplates` | `frontend/src/services/api.ts` | `frontend/src/pages/Templates.tsx`. No template request function exists in the client |
| `Switch` | `react-router-dom` | `frontend/src/App.tsx:L15`. Version 6 removed `Switch`, and `frontend/package.json:L11` pins `^6.11.1` |

`createApiClient` at `frontend/src/services/api.ts:L133` carries no `export` keyword, so the
factory is module-private and only the local `api` instance at `L162` consumes it.

See [../frontend/src/schema/README.md](../frontend/src/schema/README.md),
[../frontend/src/store/README.md](../frontend/src/store/README.md) and
[../frontend/src/services/README.md](../frontend/src/services/README.md).

## G3 undefined names that raise at execution

Seven references across six distinct names have no import behind them. Reading the import block at
the top of each file will not reveal any of them, which is what makes this class expensive to
diagnose. The name looks ordinary at the point of use, and the failure arrives later.

| Name | Referenced at | Raises when |
| ------ | --------------- | ------------- |
| `Optional` | `backend/app/core/security.py:L48`, in the `create_access_token` signature | the module body executes, so at import |
| `User` | `backend/app/core/security.py:L117`, as the `get_current_user` return annotation | the module body executes, so at import |
| `UserService` | `backend/app/core/security.py:L186`, inside `get_current_user` | `get_current_user` first runs |
| `asyncio` | `backend/app/services/collaboration_service.py:L163`, inside the Pub/Sub `callback` | a published message first arrives |
| `json` | `backend/app/services/collaboration_service.py:L248`, inside `broadcast_change` | `broadcast_change` first runs |
| `datetime` | `backend/app/tasks/background_tasks.py:L267`, inside `cleanup_expired_documents` | the retention sweep first runs |
| `datetime` | `backend/app/tasks/background_tasks.py:L321`, inside `update_document_statistics` | the statistics task first runs |

`backend/app/tasks/background_tasks.py:L96` imports `timedelta` alone, so `timedelta` resolves at
both `L146` and `L151` while `datetime` resolves nowhere.

### Two of the seven raise at import, not at execution

Python evaluates a function's annotations when the `def` statement runs, so an undefined name in a
signature fails as the module loads rather than when the function is called. `Optional` at
`backend/app/core/security.py:L48` therefore raises
`NameError: name 'Optional' is not defined` during import of `app.core.security`, and the module
cannot import at all. `User` at `L117` would raise the same way, and `L48` raises first, so
execution never reaches it.

The remaining five references sit inside function bodies and raise only when that function runs.
The register states the mechanism because the two cases need different diagnosis: a signature
failure appears in an import traceback, and a body failure appears only under exercise.

### Two findings in this file that are not defects

Diagnosing `backend/app/core/security.py` goes wrong in two predictable ways, so this register
records both explicitly.

- **`backend/app/core/security.py:L43` imports `get_settings`, not `settings`.** That name exists,
  at `backend/app/core/config.py:L126`. The configuration import in this one module resolves
  correctly, unlike the eight listed in
  [G2](#the-absent-settings-singleton). The real defects in this file are the three undefined names
  above.
- **`except jwt.JWTError` at `backend/app/core/security.py:L183` resolves correctly and is not a
  defect.** `L41` imports `jwt` from `jose`, and the installed `python-jose` distribution exposes
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
| `draft-js` | 6 | `frontend/src/utils/documentUtils.ts:L21`, `frontend/src/utils/formatting.ts:L13`, `frontend/src/components/DocumentCanvas.tsx:L21` |
| `zod` | 4 | the three modules under `frontend/src/schema/`, for example `frontend/src/schema/document.ts:L43`, plus `frontend/src/utils/validation.ts:L13` |
| `axios` | 2 | `frontend/src/services/api.ts:L78`, `frontend/src/services/auth.ts:L68` |
| `socket.io-client` | 1 | `frontend/src/services/collaboration.ts:L13` |

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
| `pydantic` | `pydantic`, 1.x only | `backend/app/core/config.py:L48` imports `BaseSettings` from the main package, and `backend/app/schema/user.py:L177` sets `orm_mode`. Pydantic 2 moved `BaseSettings` to `pydantic-settings` and renamed `orm_mode` |
| `sqlalchemy` | `SQLAlchemy`, 1.4 or newer | `backend/app/db/sql.py:L13` imports `declarative_base` from `sqlalchemy.orm`, where 1.4 moved it |
| `jose` | `python-jose` | `backend/app/api/auth.py` and `backend/app/core/security.py:L39`. The import name and the distribution name differ |
| `passlib` | `passlib` | `CryptContext` in the same two modules |
| `celery` | `celery` | `backend/app/tasks/background_tasks.py:L98` |
| `google` | `google-cloud-firestore`, `google-cloud-pubsub`, `google-cloud-storage` and `google-auth` | one namespace splits across four distributions: `google.cloud.firestore`, `google.cloud.pubsub_v1`, `google.cloud.storage` and `google.auth` |

### The progressive Python dependency-resolution failure

The backend requires seventeen distributions to run, and only ten of them appear in an `import`
line. [../backend/app/README.md](../backend/app/README.md) defines that count and the categories
behind it, and every dependency figure in this document uses them. `uvicorn` is named by a run
command instead, at `infrastructure/docker/backend.Dockerfile:L20` and `../README.md:L55`. The
remaining six divide two ways. Four arrive transitively and need no naming: `starlette` with
`fastapi`, and `ecdsa`, `rsa` and `pyasn1` with `python-jose`. Two do not arrive at all: `bcrypt`
and `python-multipart` are runtime backends that nothing declares, so thirteen of the seventeen
have to be named to a package manager. A developer building an environment by reading import
statements installs the visible packages, retries, and hits the next missing piece. The build
fails progressively rather than once. Four properties of this repository cause that pattern:

- **One import name does not match its distribution name.** `import jose` needs `python-jose`.
  Guessing `pip install jose` installs an unrelated package, and the real one pulls `ecdsa`, `rsa` and
  `pyasn1` along with it, so a key-format error can name a package no committed line mentions.
- **One namespace maps to four distributions.** `from google.cloud... import` gives no hint that
  Firestore, Pub/Sub, Cloud Storage and authentication ship separately.
- **Two runtime needs are declared by nothing.** `passlib` performs bcrypt hashing at
  `backend/app/api/auth.py:L86` and does not depend on `bcrypt`, so password hashing fails until a
  developer adds `bcrypt` by hand. FastAPI parses the form body at `backend/app/api/auth.py:L168`
  through `python-multipart` and does not require it, so a login post fails the same way.
- **Two version ceilings are invisible without reading the code.** Installing the current
  `pydantic` breaks `backend/app/core/config.py:L48` immediately, because the 1.x constraint lives
  in an import statement rather than in a manifest.

Three more distributions sit outside the seventeen, because a configuration value rather than a
committed line makes each one necessary: `psycopg2-binary` once the Cloud SQL path is exercised,
`redis` once a Celery worker attaches, and `cryptography` once `settings.ALGORITHM` names an RSA or
ECDSA algorithm. [onboarding.md](onboarding.md#setting-up-the-backend) states the condition for each.

[onboarding.md](onboarding.md) records the working package set for a first-time environment build.

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
| `backend/app/api/documents.py:L108` | `create_document(document, current_user)` | `create_document(self, document: DocumentCreate, user_id: str)` at `backend/app/services/document_service.py:L72` | Passes a `User` object where the signature declares `user_id: str` |
| `backend/app/api/documents.py:L183` | `get_document(document_id)` | `get_document(self, document_id: str, user_id: str)` at `backend/app/services/document_service.py:L123` | One argument against two parameters, so the ownership check cannot run |
| `backend/app/api/documents.py:L231` | `get_document(document_id)` | the same two-parameter signature | One argument against two |
| `backend/app/api/documents.py:L278` | `get_document(document_id)` | the same two-parameter signature | One argument against two |
| `backend/app/api/documents.py:L234` | `update_document(document_id, document)` | `update_document(self, document_id: str, document: DocumentUpdate, user_id: str)` at `backend/app/services/document_service.py:L183` | Two arguments against three parameters |
| `backend/app/api/documents.py:L281` | `delete_document(document_id)` | `delete_document(self, document_id: str, user_id: str)` at `backend/app/services/document_service.py:L252` | One argument against two |
| `backend/app/tasks/background_tasks.py:L310` | `get_document(document_id)` | the same two-parameter signature | One argument against two |
| `frontend/src/components/Toolbar.tsx:L62` | `applyInlineStyle(style)` | `applyInlineStyle(editorState: EditorState, inlineStyle: string)` at `frontend/src/utils/formatting.ts:L31` | One argument against two, and the missing argument is the editor state the helper transforms |
| `frontend/src/components/Toolbar.tsx:L67` | `applyBlockStyle(style)` | `applyBlockStyle(editorState: EditorState, blockType: string)` at `frontend/src/utils/formatting.ts:L61` | One argument against two |
| `frontend/src/pages/Editor.tsx:L238` | `<DocumentCanvas content={...} onContentChange={...} />` | `const DocumentCanvas: React.FC = () => {` at `frontend/src/components/DocumentCanvas.tsx:L108` | Two props passed to a component declaring none |

One call site in the same repository gets the argument count right, which is worth knowing when
reading the rows above. `backend/app/tasks/background_tasks.py:L135` calls
`get_document(document_id, user_id)` with both arguments, while `L310` in the same file passes one.
`frontend/src/components/TextEditor.tsx:L109` and `:L116` pass both arguments to the formatting
helpers, while `Toolbar.tsx` passes one to each. Comparing the two shows the contract faster than
reading either alone.

`TextEditor.tsx` is correct on the argument count and on the block types, and not on the inline style
names. `:L111-L115` forwards `header-one`, `header-two`, `blockquote`, `unordered-list-item` and
`ordered-list-item` into `applyBlockStyle`, and Draft.js spells every one of those exactly that way.
`:L106-L108` forwards the lowercase `bold`, `italic` and `underline` into `applyInlineStyle` at `:L109`,
and Draft.js spells those `BOLD`, `ITALIC` and `UNDERLINE`. An inline toggle through this component
would therefore apply a style name the renderer carries no rule for. Read the module as the correct
reference for the helper signatures and the block types, not for the inline style constants.

### Type inversions in the editor canvas

`frontend/src/components/DocumentCanvas.tsx` carries two errors that are exact inverses, so
correcting one in isolation risks reinforcing the other.

| Line | Call | Receives | Expects |
| ------ | ------ | ---------- | --------- |
| `L117` | `EditorState.createWithContent(contentState)` | an `EditorState`, returned by `deserializeDocument` at `frontend/src/utils/documentUtils.ts:L63` and assigned at `DocumentCanvas.tsx:L116` | a `ContentState` |
| `L163` | `serializeDocument(newEditorState.getCurrentContent())` | a `ContentState`, returned by `getCurrentContent()` | an `EditorState`, per `frontend/src/utils/documentUtils.ts:L39` |

`DocumentCanvas.tsx:L21` imports `ContentState` and never uses it.

### Other contract violations

| Site | Violation |
| ------ | ----------- |
| `backend/app/tasks/background_tasks.py:L283` | Calls `.delete()` on the result of `.get()`, which returns a list of documents rather than a reference. Lists carry no `delete` method |
| `backend/app/api/users.py:L77` | Calls `user_service.update_user(...)` from the synchronous handler declared at `L51`, so the call cannot be awaited. A coroutine object is always truthy, so if the absent `UserService` declares the method `async`, the guard at `L78` can never observe a failure. `app.services.user_service` does not exist, so no contract settles which it is |
| `backend/app/api/users.py:L30`, `:L51` | Both handlers use plain `def` while all 12 other handlers use `async def` |
| `backend/app/tasks/background_tasks.py:L151` | Stacks `@celery_app.periodic_task(run_every=timedelta(days=1))` beneath `@celery_app.task` at `L150`. Celery 5 exposes no `periodic_task` decorator, so the module raises `AttributeError` once the earlier import failures clear |
| `backend/app/db/firestore.py:L42-L68` | `get_document` is annotated `-> dict` and returns `None` at `L68` when the document is absent |
| `frontend/src/utils/documentUtils.ts:L44`, `:L73` | Calls `DocumentSchema.isValid(...)`. Zod exposes `parse` and `safeParse` and no `isValid`, and the argument is Draft.js content while `DocumentSchema` models document metadata, so the check targets the wrong contract twice over |

### The ownership check subscripts a key it does not verify

All three guarded `DocumentService` methods compare ownership by subscripting the raw Firestore
dictionary. `backend/app/services/document_service.py:L175`, `:L241` and `:L280` each evaluate
`doc.to_dict()['user_id'] != user_id`, and none of the three tests for the key first.

`create_document` is the only writer of that key, at `:L118`, so a document this service created
carries it. A record written any other way does not, and the `Document` contract itself declares
`owner_id` rather than `user_id` at `backend/app/schema/document.py:L66`. A stored record without a
`user_id` key therefore raises `KeyError` on the subscript.

`KeyError` is not an `HTTPException`, and no handler in `backend/app/api/documents.py` wraps the
service call in a `try`, so FastAPI's default exception handling answers **500 Internal Server Error**.
A caller who is genuinely not the owner receives 403, and a caller hitting a record with a missing key
receives 500 for what is the same authorization decision.

### The retention sweep fails partway and leaves records behind

`cleanup_expired_documents` at `backend/app/tasks/background_tasks.py:L152` deletes across two systems
and three collections with no transaction, no compensating action and no `try` anywhere in the loop.
The table below walks the loop body in execution order. Rows 1 and 2 sit above the first delete, and
every row from 4 onward runs after the Firestore document is already gone.

| Step | Statement | Locator | What happens |
|------|-----------|---------|--------------|
| 1 | `db.collection('documents').where('expiration_date', ...).get()` | `:L267` | `datetime.now()` raises `NameError`, because `:L96` imports `timedelta` alone. Nothing else in the task runs |
| 2 | The same query, once `datetime` is imported | `:L267` | No committed line writes `expiration_date` and `backend/app/schema/document.py` never declares it, so no record the application created can match. Which records return depends on what the collection already holds |
| 3 | `user_id = doc.get('user_id')` | `background_tasks.py:L271` | Raises for a matched record that carries no `user_id`. `doc.id` at `:L270` always exists, so this is the only read that can fail before the first delete |
| 4 | `db.collection('documents').document(doc_id).delete()` | `background_tasks.py:L274` | **The first destructive step, and it succeeds.** Everything below can now fail with the document already gone |
| 5 | `storage_client.bucket(settings.DOCUMENT_BUCKET_NAME)` | `background_tasks.py:L278` | `Settings` declares no `DOCUMENT_BUCKET_NAME`, so this raises `AttributeError` |
| 6 | `blob.delete()` on the key `{user_id}/{doc_id}` | `background_tasks.py:L279`, `:L280` | No writer uses that layout. Three writers produce export objects, and each uses a different key: `backend/app/services/export_service.py:L155` writes `exports/{document.id}.pdf`, `:L229` writes `exports/{document.id}.docx`, and `background_tasks.py:L142` writes `exports/{user_id}/{document_id}.{export_format}`. The retention key matches none of the three, and it addresses `DOCUMENT_BUCKET_NAME` while the three writers address `STORAGE_BUCKET_NAME` and `EXPORT_BUCKET_NAME`, so the delete raises `NotFound` |
| 7 | `db.collection('document_permissions').where(...).get().delete()` | `background_tasks.py:L283` | `.get()` returns a list of snapshots, and a list carries no `delete` method, so this raises `AttributeError` |
| 8 | `db.collection('document_metadata').document(doc_id).delete()` | `background_tasks.py:L284` | The last statement. Reached only if every step above succeeded |

Four partial states follow, one per failure point after the first delete:

| Stops at | Document record | Stored file | Permissions | Metadata |
|----------|-----------------|-------------|-------------|----------|
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
| `update_document` at `backend/app/services/document_service.py:L183` | `:L235` | `:L237`, 404 at `:L238` | `:L241`, 403 at `:L242` | `:L246` |
| `delete_document` at `backend/app/services/document_service.py:L252` | `:L274` | `:L276`, 404 at `:L277` | `:L280`, 403 at `:L281` | `:L284` |

Two outcomes follow. A concurrent owner change between the read and the write is overwritten silently,
because `update()` at `:L246` sends only the caller's fields and asserts nothing about the document it
found. A concurrent delete makes that same `update()` fail on a document the check at `:L237` reported
as present. Firestore supports both a transaction and a precondition, and neither method uses either.

`delete_document` compounds the problem by reporting success unconditionally. `:L287` returns the
literal `True` whatever `doc_ref.delete()` at `:L284` did, so the value means the method reached its
last line rather than that a document was removed. A Firestore delete of an already-absent document
succeeds silently, so the return value cannot distinguish a deletion from a no-op.

## G6 field and shape drift

No artifact keeps the two languages in agreement. The repository commits no OpenAPI document,
generates no client, and shares no schema package across the Python and TypeScript trees.
Developers therefore maintain the Pydantic models under `backend/app/schema/` and the Zod schemas
under `frontend/src/schema/` by hand, and the divergences below follow from that.

### The ownership field, four positions

Authorization in this repository compares an ownership field, and four positions disagree about its
name. **No position is canonical.** Selecting one would change an interface, which the documentation
engagement excluded, so this register lists all four and prefers none. The full treatment sits in
[data-model.md](data-model.md), and [decision-log.md](decision-log.md) will record the choice once
that planned file is committed.

| Position | Locator | Field |
| ---------- | --------- | ------- |
| The Pydantic document contract | `backend/app/schema/document.py:L66`, on `DocumentBase` and inherited by `Document` | `owner_id: Optional[str] = None` |
| The Pydantic version contract | `backend/app/schema/document.py:L135`, on `DocumentVersion` | `user_id: str` |
| The document service | `backend/app/services/document_service.py:L116` writes it, and `:L175`, `:L241` and `:L280` compare it | `user_id` |
| The in-repository specification, declared intent | `documentation/Technical Specifications.md:L333`, `:L375`, `:L383`, under the SYSTEM DESIGN heading at `L300` | `owner_id` |

Two details make the drift worse than a naming disagreement.

The first: `owner_id` at `backend/app/schema/document.py:L66` is optional and defaults to `None`, so
a `Document` validates successfully without the field that authorization depends on. The contract
never requires the value the ownership check reads.

The second: the document router reads `.user_id` off objects typed as `Document` at
`backend/app/api/documents.py:L184`, `:L232` and `:L279`. The router follows the service convention
rather than the contract its own type annotation names. The client repeats the same split, with
`owner_id` at `frontend/src/schema/document.ts:L69` and `user_id` at `:L91`.

### Field and shape divergences

| Divergence | Client or consumer | Server or contract |
| ------------ | -------------------- | -------------------- |
| Access token field | `frontend/src/services/auth.ts:L147` reads `response.data.accessToken` and stores it at `:L148` | The token handler at `backend/app/api/auth.py:L167-L168` follows the OAuth2 convention and returns `access_token` |
| Base URL variable | `frontend/src/services/api.ts:L82` reads `process.env.REACT_APP_API_BASE_URL` | `infrastructure/docker/docker-compose.yml:L11` injects `REACT_APP_API_URL`. The names never meet, so the client resolves an undefined base URL |
| User display name | `frontend/src/components/Header.tsx:L77-L78`, `frontend/src/pages/Home.tsx:L59` and `frontend/src/pages/Settings.tsx:L82` read `currentUser.name` | `backend/app/schema/user.py:L81-L82` models `username` and `full_name`. No contract declares `name` |
| User avatar | `frontend/src/components/Header.tsx:L77` reads `currentUser.avatar` | No contract in either language declares `avatar` |
| Page count | `backend/app/tasks/background_tasks.py:L314` reads `len(document.pages)` | `backend/app/schema/document.py` declares no `pages` field on any of its five models |
| User update timestamp | `frontend/src/schema/user.ts` omits `updated_at` | `backend/app/schema/user.py:L171` declares `updated_at: datetime` as required |
| Template shape | `frontend/src/pages/Templates.tsx` declares a local `Template` interface incompatible with the Zod schema at `frontend/src/schema/template.ts:L40` | The backend declares no template contract at all, per [G1](#g1-absent-modules-referenced-by-committed-code) |
| Timestamp type | `frontend/src/schema/document.ts:L70-L71` and `:L90` use `z.date()`, which rejects a string | Every timestamp crossing the boundary arrives as a JavaScript Object Notation (JSON) string, so validation fails on well-formed server data |
| Collaborator list | `frontend/src/schema/document.ts:L72` declares `collaborators: z.array(z.string())` | No Pydantic model declares a collaborator field, and no handler returns one |
| Password storage | `backend/app/api/auth.py:L323` computes a bcrypt hash during registration | The `User` contract at `backend/app/schema/user.py:L114` declares no password field, so the response model has nowhere to carry the hash. `UserCreate` declares `password` at `:L94` |

Required fields that no code path writes compound the drift. `backend/app/schema/document.py:L111`
and `:L112` declare `created_at` and `updated_at` as required on `Document`, and no service method
sets either. `backend/app/schema/user.py:L172-L173` declare `is_active` and `is_superuser`, and no
code path reads either.

`backend/app/schema/document.py:L82` declares `DocumentUpdate` without inheriting `DocumentBase`,
so the update contract shares no field definitions with the model it updates. Both schema modules
import `List` and never use it, at `backend/app/schema/document.py:L52` and
`backend/app/schema/user.py:L68`.

See [data-model.md](data-model.md),
[../backend/app/schema/README.md](../backend/app/schema/README.md) and
[../frontend/src/schema/README.md](../frontend/src/schema/README.md).

## G7 endpoint and transport mismatch

The client calls routes the server does not expose, and the collaboration path has a different
protocol at each end.

### The client calls six routes, and no server route matches any of them

| Client call | Locator | Server route | Locator |
| ------------- | --------- | -------------- | --------- |
| `POST /auth/login` | `frontend/src/services/auth.ts:L146` | `POST /token` | `backend/app/api/auth.py:L167` |
| `POST /auth/logout` | `frontend/src/services/auth.ts:L194` | none. No handler implements logout | |
| `GET /auth/me` | `frontend/src/services/auth.ts:L239` | `GET /me` | `backend/app/api/users.py:L29` |
| `GET /documents` | `frontend/src/services/api.ts:L218` | `GET /` | `backend/app/api/documents.py:L111` |
| `POST /documents` | `frontend/src/services/api.ts:L246` | `POST /` | `backend/app/api/documents.py:L53` |
| `PUT /documents/{id}` | `frontend/src/services/api.ts:L288` | `PUT /{document_id}` | `backend/app/api/documents.py:L188` |

The login call carries two further mismatches that survive a path correction. First, encoding:
`frontend/src/services/auth.ts:L146` passes a plain object to `axios.post`, and Axios serializes a
plain object as JSON under `Content-Type: application/json`, while
`form_data: OAuth2PasswordRequestForm = Depends()` at `backend/app/api/auth.py:L168` reads an
`application/x-www-form-urlencoded` body. FastAPI answers **422** before the handler body runs. Second,
field name: the client sends `email` and `password`, and `OAuth2PasswordRequestForm` supplies
`username` and `password`, which `backend/app/api/auth.py:L230` reads as `form_data.username`. No
submitted field carries the identifier the handler reads.

The document prefix mismatch has a single cause. `backend/app/main.py:L125-L128` calls
`include_router` four times and passes no `prefix` argument to any of them, so every route mounts at
the application root. The client prefixes `/documents`, and the server serves `/`. The registration
also ignores `API_V1_STR`, which `backend/app/core/config.py:L112` declares and no module reads.

The three prefixed document calls fail in three different ways, which matters when reading a response
rather than a route table. The outcomes below assume the import chain and the client's own blockers
are repaired, so dispatch actually happens.

| Client call | Locator | Dispatch outcome |
|-------------|---------|------------------|
| `GET /documents` | `frontend/src/services/api.ts:L218` | `/documents` is one path segment, so it matches `GET /{document_id}` at `backend/app/api/documents.py:L145` and `document_id` binds to the literal string `documents`. No body follows. That handler raises first: `:L183` passes one argument to the two-parameter `get_document` signature at `backend/app/services/document_service.py:L123`, so a `TypeError` propagates and the response is a 500. The declared `Document[]` never meets a document object |
| `POST /documents` | `frontend/src/services/api.ts:L246` | The single-segment shape matches `GET`, `PUT` and `DELETE` at `backend/app/api/documents.py:L145`, `:L188` and `:L237`, and no router declares `POST /{document_id}`. Starlette answers **405 Method Not Allowed**, not 404 |
| `PUT /documents/{id}` | `frontend/src/services/api.ts:L288` | Two path segments, and no two-segment route exists in any of the four routers. The response is **404** |

A 500 from a raising handler, a 405 and a 404 are three distinct symptoms from one root cause, so a
developer who repairs only the call that returns 404 leaves the other two in place.

`frontend/src/services/auth.ts:L68` imports the bare `axios` global and uses it at `L146`, `:L194`
and `:L239`, bypassing the configured instance created at `frontend/src/services/api.ts:L162`.
Requests from the authentication module therefore carry neither the base URL nor the bearer
interceptor.

### Document routes shadow the template and profile routes

The overlap has two forms, and the second is easy to miss because the paths do not look alike.

The document and template routers declare five route shapes each, and the shapes are identical. A
path parameter's name does not participate in matching, so `/{document_id}` and `/{template_id}`
compile to the same single-segment pattern.

| Method and shape | Document handler | Template handler |
| ------------------ | ------------------ | ------------------ |
| `POST /` | `backend/app/api/documents.py:L53` | `backend/app/api/templates.py:L77` |
| `GET /` | `backend/app/api/documents.py:L111` | `backend/app/api/templates.py:L118` |
| `GET /{id}` | `backend/app/api/documents.py:L145` | `backend/app/api/templates.py:L151` |
| `PUT /{id}` | `backend/app/api/documents.py:L188` | `backend/app/api/templates.py:L195` |
| `DELETE /{id}` | `backend/app/api/documents.py:L237` | `backend/app/api/templates.py:L254` |

The profile router declares two literal single-segment paths, and a literal path is still a single
segment. Both fall inside the pattern the document router already claimed.

| Method and path | Profile handler | Shadowing document handler |
|-----------------|-----------------|----------------------------|
| `GET /me` | `backend/app/api/users.py:L29` | `GET /{document_id}` at `backend/app/api/documents.py:L145` |
| `PUT /me` | `backend/app/api/users.py:L50` | `PUT /{document_id}` at `backend/app/api/documents.py:L188` |

`backend/app/main.py:L126` registers the document router first, then `:L127` the profile router and
`:L128` the template router. Starlette matches routes in registration order and returns the first
route whose pattern matches, so the document handler wins every collision. **Seven of the twelve
protected handlers are unreachable**: all five template handlers and both profile handlers. A request
to `GET /me` reaches the single-document read with `document_id` bound to the literal string `me`.

### The collaboration path has no route and two protocols

| End | Protocol | Locator |
| ----- | ---------- | --------- |
| Client | Socket.IO, with `io()` called at `frontend/src/services/collaboration.ts:L77` and no URL argument | `L13` imports `io` from `socket.io-client` |
| Server | A FastAPI `WebSocket`, per the `connect(self, websocket: WebSocket, ...)` signature | `backend/app/services/collaboration_service.py:L36` and `:L75` |

The client emits three events, and each has a server method that was clearly meant to receive it.
None of the three pairs can meet.

| Client event | Emitted payload | Nearest server counterpart | Why the pair cannot meet |
| -------------- | ----------------- | ---------------------------- | -------------------------- |
| `join_document` | the bare `documentId` string, at `frontend/src/services/collaboration.ts:L126` | `CollaborationService.connect` at `backend/app/services/collaboration_service.py:L75` | `connect` declares a `WebSocket`, a `document_id` and a `user_id`. The emit carries one string, no socket object and no user identity |
| `leave_document` | the bare `currentDocumentId` string, at `:L154` | `CollaborationService.disconnect` at `backend/app/services/collaboration_service.py:L173` | `disconnect` declares `document_id` and `user_id`. The emit carries the identifier alone, and `:L155` clears it immediately with nothing confirming delivery |
| `document_changes` | the envelope `{ documentId, changes }`, at `:L201-L204` | `CollaborationService.broadcast_change` at `backend/app/services/collaboration_service.py:L218` | `broadcast_change` declares `document_id` and a `change` dictionary and publishes `json.dumps(change)` at `:L248`. The client nests the change inside an envelope, so the shapes differ even with a route in place |

Socket.IO is a protocol layered over WebSocket rather than a WebSocket client, so the two ends could
not complete a handshake even with a route between them. No route exists: no module constructs
`CollaborationService`, and no `@app.websocket` declaration appears anywhere in the backend.
`frontend/src/services/collaboration.ts:L212` exports the client class, and no module imports it.

`setupEventListeners` at `frontend/src/services/collaboration.ts:L88-L93` has a body consisting
only of a marker and comments, so the client registers no inbound handler and would ignore every
message it received.

### Nothing creates the Pub/Sub topic the server addresses

Two of the four Pub/Sub calls name a topic and need it to exist. `create_subscription` at
`backend/app/services/collaboration_service.py:L124` passes `topic=topic_name`, and `publish` at
`:L248` addresses the same path. Neither creates a topic, no `create_topic` call exists anywhere in
the repository, and the module records the gap in its own docstring at `:L8-L12`.

No committed infrastructure supplies one either. Searching all of `infrastructure/` for `pubsub`,
`topic` and `subscription` returns nothing, and `infrastructure/terraform/main.tf` declares one
provider plus four Google Cloud resources with no messaging resource among them. The topic path is
derived per document at `backend/app/services/collaboration_service.py:L120`, so a deployment needs one
topic per document identifier, created outside this repository before any editor connects.

| Call | Locator | Needs a topic | Result without a pre-created topic |
|------|---------|---------------|-------------------------------------|
| `create_subscription` | `collaboration_service.py:L124` | Yes | `NotFound`, caught at `:L125`, printed at `:L127`, and `:L128` returns |
| `subscribe` | `collaboration_service.py:L165` | No | Never reached, because `:L128` returned first |
| `delete_subscription` | `collaboration_service.py:L211` | No | `NotFound` for a subscription never created, caught at `:L212`, printed at `:L214` |
| `publish` | `collaboration_service.py:L248` | Yes | `NotFound`, caught at `:L250`, printed at `:L252`, and the method returns normally |

### A failed publish is caught and logged rather than raised

`broadcast_change` at `backend/app/services/collaboration_service.py:L218` reads
`settings.PROJECT_ID` at `:L245`, which sits **above** the `try` at `:L247`. `Settings` declares no
`PROJECT_ID`, so the `AttributeError` propagates to the caller on the first call. That read is the
method's first statement, so nothing is published and no partial state remains.

Everything after it is guarded. `:L248` calls `json.dumps(change)` against a module that imports no
`json`, `:L250` catches every exception the body raises, and `:L252` prints it. Once `PROJECT_ID`
exists, a publish failure therefore surfaces as a printed line and a normal `None` return, and a caller
cannot tell a delivered change from a dropped one.

Three more faults in the same path deserve their own statement:

- **The callback carries three faults on one line.** `:L163` calls
  `asyncio.run(websocket.send_json(message.data))`. `asyncio` is never imported, so the first delivered
  message raises `NameError`. Supplying the import exposes the next fault: `message.data` is `bytes`,
  `WebSocket.send_json` serializes with `json.dumps`, and `json.dumps` rejects `bytes`. Nothing decodes
  the payload, while `:L248` encoded it as UTF-8 before publishing, so the round trip is unbalanced. The
  third fault is event-loop ownership, because `asyncio.run` builds a new loop and closes it while the
  socket belongs to the server's already-running loop, and `asyncio.run` refuses outright when a loop is
  already running on the calling thread. The Pub/Sub client invokes the callback on its own thread, so
  none of the three reaches `connect`.
- **Acknowledgement precedes delivery.** `:L162` calls `message.ack()` before `:L163` sends. A send that
  fails after the acknowledgement loses the message, because Pub/Sub has already been told it was
  handled and will not redeliver.
- **Two partial states can persist.** `connect` mutates the registry at `:L115-L117` before it touches
  Pub/Sub, so a caught subscription failure leaves a socket in `active_connections` with no subscription
  behind it, and no later call removes it. `disconnect` removes the registry entry at `:L203-L206`
  before deleting the subscription, so a caught failure at `:L212` leaves a subscription with no
  registry entry. Neither method compensates or reports the state.
- **Both futures block, and one method has no future at all.** `future.result()` at `:L168` and `:L249`
  pass no timeout, so each blocks its calling thread, and `connect` is `async def`, so `:L168` holds the
  event loop. `disconnect` calls `delete_subscription` at `:L211`, which returns nothing to wait on.

### Route registration and protection

Fourteen handlers exist across the four routers, and twelve sit behind the `get_current_user`
dependency. The two public handlers are `POST /token` at `backend/app/api/auth.py:L167` and
`POST /register` at `:L242`. The full route table lives in
[../backend/app/api/README.md](../backend/app/api/README.md).

Two `get_current_user` implementations exist and disagree on status codes. The routers all import
the one at `backend/app/api/auth.py:L89`, for example at
`backend/app/api/documents.py:L48`, which raises **404** at `backend/app/api/auth.py:L164` when the
user is absent. The unused implementation at `backend/app/core/security.py:L117` raises **401** for
the same condition at `:L189`. A missing user is an authentication failure rather than a missing
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
| `TS2305` | 6 | Module has no exported member | 5 from the missing `Document` family, 1 from `Switch` at `frontend/src/App.tsx:L15` |
| `TS7006` | 5 | Parameter implicitly has an `any` type | `frontend/src/services/api.ts:L141`, `:L148`, `:L152`, `:L153`; `frontend/src/pages/Editor.tsx:L85` |
| `TS2322` | 4 | Type not assignable | `frontend/src/App.tsx:L52-L55`, the four `Route` elements passing the version 5 `component` prop |
| `TS2614` | 2 | No exported member, import form mismatch | `frontend/src/store/index.ts:L21`, `:L22` |
| `TS2552` | 1 | Cannot find name | `frontend/src/services/api.ts:L142`, the undefined `store` |
| `TS2339` | 1 | Property does not exist on type | `frontend/src/services/api.ts:L142`, `.auth` on `{ document: unknown; user: unknown; }` |

`frontend/src/services/api.ts:L142` carries two of the seven codes on one line. The compiler reports
the state shape as `{ document: unknown; user: unknown; }`, which is direct evidence that the store
registers only the two reducer keys at `frontend/src/store/index.ts:L43-L44` and no `auth` key.

### `npm ci` cannot run anywhere

The repository commits no lockfile. No `package-lock.json`, `yarn.lock` or `pnpm-lock.yaml` exists,
and the repository root holds no `package.json` either. Both invocations fail with
`npm error code EUSAGE`.

| Invocation | Locator | Working directory | Result |
| ------------ | --------- | ------------------- | -------- |
| Continuous integration | `.github/workflows/ci.yml:L19` | the repository root, because the step sets no `working-directory` | Fails. No manifest and no lockfile |
| Container build | `infrastructure/docker/frontend.Dockerfile:L11` | `/app`, after `L8` copies `package*.json` | Fails. The glob at `L8` matches only `package.json` |

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
   constant at `frontend/src/services/api.ts:L82`, which reads `REACT_APP_API_BASE_URL`. Compose sets
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

`Settings` declares nine fields at `backend/app/core/config.py:L111-L119`. Seven carry no default and
are required, and the two `Optional` Google Cloud fields at `:L116-L117` default to `None`. Compose
supplies exactly one of the nine. Six further settings are read from `settings` in application code and
declared on no model, so neither a `.env` file nor a Compose entry can reach them through Pydantic. The
matrix covers all 15.

| Setting | Declared at | Required | Compose supplies | Consequence |
| --- | --- | --- | --- | --- |
| `PROJECT_NAME` | `config.py:L111` | Yes | No | `Settings()` raises `ValidationError` |
| `API_V1_STR` | `config.py:L112` | Yes | No | `ValidationError`. Read by no module |
| `SECRET_KEY` | `config.py:L113` | Yes | No | `ValidationError`. Signs and verifies every token |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `config.py:L114` | Yes | No | `ValidationError`. Sets token lifetime |
| `ALGORITHM` | `config.py:L115` | Yes | No | `ValidationError`. Names the JWT algorithm |
| `GOOGLE_CLOUD_PROJECT` | `config.py:L116` | No, `Optional` | No | Resolves to `None`, and `backend/app/db/firestore.py:L40` passes it as the Firestore project |
| `GOOGLE_APPLICATION_CREDENTIALS` | `config.py:L117` | No, `Optional` | No | Resolves to `None`. No credential file is mounted into any container |
| `DATABASE_URL` | `config.py:L118` | Yes | Yes, at `docker-compose.yml:L24` | Satisfied. Read at `backend/app/db/sql.py:L16` |
| `REDIS_URL` | `config.py:L119` | Yes | No | `ValidationError`. Compose declares no Redis service to point it at |
| `ALLOWED_ORIGINS` | Nowhere | n/a | No | `AttributeError` at `backend/app/main.py:L118` when the CORS middleware reads it |
| `PROJECT_ID` | Nowhere | n/a | No | `AttributeError` at `backend/app/services/collaboration_service.py:L120` |
| `STORAGE_BUCKET_NAME` | Nowhere | n/a | No | `AttributeError` at `backend/app/services/export_service.py:L154` |
| `SIGNED_URL_EXPIRATION` | Nowhere | n/a | No | `AttributeError` at `backend/app/services/export_service.py:L162` |
| `EXPORT_BUCKET_NAME` | Nowhere | n/a | No | `AttributeError` at `backend/app/tasks/background_tasks.py:L141` |
| `DOCUMENT_BUCKET_NAME` | Nowhere | n/a | No | `AttributeError` at `backend/app/tasks/background_tasks.py:L278` |

Six required fields are absent, and six more are unsatisfiable by any environment mechanism at all. A
backend container that got past the absent `requirements.txt` would still fail during import, because
`backend/app/core/config.py` never constructs the module-level `settings` instance that eight modules
request. [../infrastructure/docker/README.md](../infrastructure/docker/README.md) and
[deployment-guide.md](deployment-guide.md) carry the same matrix with the same counts.

### No Redis service backs the Celery broker

`backend/app/tasks/background_tasks.py:L98` constructs a Celery application whose broker reads
`settings.REDIS_URL`, and `backend/app/core/config.py:L119` declares `REDIS_URL` as a required
setting. Nothing provides Redis. `infrastructure/docker/docker-compose.yml` declares three services,
`frontend`, `backend` and `db`, and no cache or broker. `infrastructure/terraform/main.tf` declares
no Memorystore instance.

No process runs the tasks either. No worker command appears in any Dockerfile, Compose service,
workflow or script, and no beat scheduler exists for the daily sweep declared at
`backend/app/tasks/background_tasks.py:L151`. No producer enqueues the three tasks, because nothing
calls `.delay()` or `.apply_async()` anywhere in the repository.

### Signed URL generation needs credentials nothing supplies

`ExportService` writes an object and signs a link for it, and neither step completes. Three
prerequisites are missing, and they fail in this order inside `export_to_pdf`.

| Order | Statement | Locator | What it needs |
|-------|-----------|---------|---------------|
| 1 | `self.storage_client.bucket(settings.STORAGE_BUCKET_NAME)` | `backend/app/services/export_service.py:L154` | A declared `STORAGE_BUCKET_NAME`. `Settings` declares nine fields at `backend/app/core/config.py:L111-L119` and this is not one, so attribute access raises `AttributeError` before any network call |
| 2 | `blob.upload_from_string(...)` | `backend/app/services/export_service.py:L157` | Credentials that authenticate and can write to the bucket. `backend/app/db/firestore.py:L39` holds the repository's only Application Default Credentials resolution, and no committed file supplies `GOOGLE_APPLICATION_CREDENTIALS` |
| 3 | `blob.generate_signed_url(version="v4", ...)` | `backend/app/services/export_service.py:L160-L164` | Sign-capable credentials, plus an expiry inside the version 4 limit |

Step 3 is the prerequisite most easily missed, because authentication alone does not satisfy it. A
version 4 signature is computed locally, so the credentials must be able to sign bytes. Two shapes do
that. The first is a service-account private key, referenced through `GOOGLE_APPLICATION_CREDENTIALS`,
which `backend/app/core/config.py:L117` declares as `Optional[str]` with no explicit default,
which Pydantic 1.x treats as optional with a `None` default, so the
contract never requires it, and no committed `.env` supplies it, with
`Config.env_file` at `:L123` naming the uncommitted file. The second is an IAM `signBlob` grant, which
credentials with no private key must use by delegating to the IAM Credentials application programming
interface (API). That path needs `iam.serviceAccounts.signBlob` on the signing service account, granted
through the Service Account Token Creator role, and the caller must name the signer explicitly. Neither
the code nor `infrastructure/terraform/main.tf` grants that permission or names a signer.

Credentials from `gcloud auth application-default login` carry neither a private key nor a signer
identity, so `generate_signed_url` raises for a local developer even when the upload succeeds.

The expiry adds two more constraints. `generate_signed_url` accepts an `int` of seconds, a
`datetime.timedelta` or an absolute `datetime`, and `backend/app/services/export_service.py:L162`
passes `settings.SIGNED_URL_EXPIRATION` with no conversion, so the call receives whatever type that
field eventually holds. A version 4 signature also caps the lifetime at seven days, and a longer expiry
raises `ValueError` rather than shortening the link. `Settings` declares no `SIGNED_URL_EXPIRATION`, so
no committed value can be checked against either constraint. Neither export method holds a `try`, so
both errors reach the caller, and step 2 has already written the placeholder object by the time step 3
fails. The task path signs differently again: `backend/app/tasks/background_tasks.py:L146` passes no
`version` argument at all, so it would sign under version 2.

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
| `L26` | `pip install -r requirements.txt` | No such file, per [G4](#the-backend-has-no-dependency-manifest) |
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
environment template at `L40` and both migrations at `L47-L48` do not.

**The credentials guard authenticates nothing.** `scripts/deploy.sh:L4-L7` tests only that
`GOOGLE_APPLICATION_CREDENTIALS` holds a non-empty value, then proceeds. That variable configures
Application Default Credentials, which is the mechanism the Google client libraries use inside the
application. Every cloud command the script runs is a `gcloud` or `gsutil` invocation, and those read
the CLI's own active account from its configuration rather than that variable. Setting the variable to
any non-empty string satisfies the guard, and `gsutil cp` at `:L23` is the first command to expose the
gap by failing on authentication. Authenticating the CLI takes
`gcloud auth activate-service-account --key-file` or `gcloud auth login`, and no committed file runs
either.

**The archive carries more than the application.** `scripts/deploy.sh:L19` runs
`zip -r app.zip . -x "*.git*" -x "node_modules/*" -x "venv/*"` from the repository root, and the two
directory patterns are anchored at that root. Neither matches `frontend/node_modules/`, which the
install step creates, and neither matches `backend/venv/`, which
`scripts/setup_dev_environment.sh:L14` creates. Nothing excludes a `.env` file, and nothing excludes a
service-account JSON key. `:L23` then uploads the result to a hard-coded public-name bucket. A
developer who followed the setup script and placed credentials in the tree ships both the credentials
and two dependency trees. The exclusion patterns need `**/node_modules/*`, `**/venv/*`, `.env` and the
key file's own name, and adding them is a repository change that this documentation pass does not make.

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
`infrastructure/terraform/outputs.tf:L20` and `read_replica_connection_string` at `:L26`.
Both set `sensitive = true`, at `:L21` and `:L27`, which masks the value in command-line output.
Terraform still writes the resolved password to state in plaintext, so the setting reduces exposure
without removing it. Two facts make that worse here. The configuration declares no backend block, so
state lands on the local filesystem unencrypted. No `.gitignore` exists at any path in this repository
either, so `terraform.tfstate` is an untracked file that `git add .` stages along with everything else.
A single unguarded commit publishes the password.

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
`md:grid-cols-2` and `lg:grid-cols-3`, both at `frontend/src/pages/Templates.tsx:L174`.

### Frontend framework version mismatches

| Usage | Locator | Declared version |
| ------- | --------- | ------------------ |
| `ReactDOM.render`, the React 17 entry point | `frontend/src/index.tsx:L34` | `react` and `react-dom` at `^18.2.0`, `frontend/package.json:L8-L9`. React 18 expects `createRoot` |
| `Switch` and the `component` prop, both removed in version 6 | `frontend/src/App.tsx:L15` and `:L52-L55` | `react-router-dom` at `^6.11.1`, `frontend/package.json:L11` |
| Two nested `Provider` elements wrapping one store | `frontend/src/index.tsx:L36` and `frontend/src/App.tsx:L46` | the inner element is redundant |
| Named import of a default-only export | `frontend/src/App.tsx:L23` imports `{ store }`; `frontend/src/index.tsx:L17` imports the default correctly | `frontend/src/store/index.ts:L65` exports only a default |

Five navigation links target routes the router never declares. `frontend/src/App.tsx:L52-L55`
declares `/`, `/editor`, `/templates` and `/settings`.

| Link | Locator |
| ------ | --------- |
| `/documents` | `frontend/src/components/Header.tsx:L69` |
| `/login` | `frontend/src/components/Header.tsx:L81` |
| `/new-document` | `frontend/src/pages/Home.tsx:L61` |
| `/open-document` | `frontend/src/pages/Home.tsx:L64` |
| `/recent-documents` | `frontend/src/pages/Home.tsx:L67` |

### Runtime versions are declared three ways and enforced nowhere

| Runtime | Declarations | Enforcement | End of life |
| --------- | -------------- | ------------- | ------------- |
| Python | 3.8 or later at `README.md:L23`; `python:3.9-slim` at `infrastructure/docker/backend.Dockerfile:L2`; unpinned `apt-get` packages at `scripts/setup_dev_environment.sh:L10` | none. No `.python-version` and no manifest | 3.9 ended support on 31 October 2025, with 3.9.25 as its final security release. 3.8 ended earlier still |
| Node.js | 14 or later at `README.md:L22`; `node-version: '14'` at `.github/workflows/ci.yml:L17`; `node:14-alpine` at `infrastructure/docker/frontend.Dockerfile:L2` | none. `frontend/package.json` declares no `engines` field and no `.nvmrc` exists | 14 ended support on 30 April 2023 |
| PostgreSQL | `postgres:13` at `infrastructure/docker/docker-compose.yml:L31`; `postgresql`, unpinned, at `scripts/setup_dev_environment.sh:L10`; Cloud SQL named with no version in `infrastructure/terraform/main.tf` | none. No version appears in any application file | 13 ended support on 13 November 2025, with 13.23 as its final release |

**All three declared runtimes are past end of life.** None receives security patches as of 6 August
2026, so a machine or an image built to these declarations runs unsupported software at every layer.
`nginx:alpine` at `infrastructure/docker/frontend.Dockerfile:L20` pins no version at all, so a rebuild
can change the serving runtime with no file changing.

One further version interaction sits behind the Python pin. The current `google-cloud-firestore`
release requires Python 3.10 or newer, and `backend/app/db/firestore.py:L34` imports from it. A 3.9
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
Nothing here does. No entry in this class was found by running anything. Each one was found by
reading the code and asking what is not there.

**Absence and current unreachability are separate facts, and this register states both.** No route
in `backend/app/` serves a request today, because `import app.main` fails at
`backend/app/api/auth.py:L81`. A missing check on an unreachable path exposes nothing while the path
stays unreachable. The moment the import failures at
[G2](#g2-absent-symbols-inside-modules-that-do-exist) are repaired, every gap below becomes live at
once. None of them is mentioned in the repair steps that would make them live. That ordering is the
reason this class exists. Where a claim about runtime behaviour would depend on a service this
repository does not provide, the entry says what cannot be established rather than guessing.

### G9.1 The backend HTTP surface

Fourteen handlers exist across four routers. Twelve declare the bearer dependency and two are public.
The controls below are absent from all of them.

| # | Absent control | Evidence | What the absence permits once routes serve traffic |
|---|----------------|----------|-----------------------------------------------------|
| 1 | Rate limiting or throttling on any route, including the two public ones | `backend/app/main.py:L116` adds one middleware, and it is CORS. No limiter, no dependency and no proxy configuration is committed anywhere. The public routes are `backend/app/api/auth.py:L167` (`POST /token`) and `:L242` (`POST /register`) | Unmetered credential guessing against `/token` and unmetered account creation against `/register` |
| 2 | A request body size limit | No handler, no middleware and no server flag bounds a body. `backend/app/schema/document.py:L65` declares `content` as a bare `str` | A single request can carry an unbounded document body into a Firestore write |
| 3 | Field length or format bounds on any model field | Neither `backend/app/schema/document.py` nor `backend/app/schema/user.py` contains a single `Field(` call, so no `max_length`, no `min_length` and no pattern applies to any field. `backend/app/schema/user.py:L80` declares `email: str` rather than an email type | Oversized and malformed values validate successfully and reach storage |
| 4 | A server-side password policy | `backend/app/schema/user.py:L94` declares `password: str` with no constraint, and `backend/app/api/auth.py:L323` hashes whatever arrives. The only policy in the repository is client-side, at `frontend/src/utils/validation.ts:L44-L50`, and a client-side check is not a control | Any password, including an empty string, is accepted at registration |
| 5 | Uniform responses that do not distinguish known accounts | Registration answers a known address with 400 `Email already registered` at `backend/app/api/auth.py:L320-L321`. Login answers a bad credential with 401 `Incorrect username or password` at `:L231-L232`, which is correctly uniform. The registration route is the enumeration oracle | An attacker learns which email addresses hold accounts by submitting registrations |
| 6 | Any check on `is_active` before a token is honoured | `backend/app/schema/user.py:L172` declares `is_active`, and no code path in the repository reads it. `backend/app/api/auth.py:L165` returns the user immediately after lookup, and `backend/app/core/security.py:L186-L189` does the same in the duplicate dependency | A deactivated account keeps full access for the life of its token |
| 7 | A `WWW-Authenticate: Bearer` header on every 401 | Two sources answer 401, and only one carries a challenge. `OAuth2PasswordBearer`, constructed at `backend/app/api/auth.py:L85` and `backend/app/core/security.py:L46`, leaves `auto_error` at its default `True`, and FastAPI's OAuth2 base raises `HTTPException(401, headers={"WWW-Authenticate": "Bearer"})` for a missing or non-bearer `Authorization` header, so that path is conformant. The six explicit raises are not, at `backend/app/api/auth.py:L157-L158`, `:L160`, `:L231-L232`, and `backend/app/core/security.py:L182`, `:L184`, `:L189`. None of the six sets a `headers` argument | A client that presents a malformed or expired token, or a valid token for an absent user, receives a 401 with no challenge, so it cannot distinguish that case from an authorization failure by header alone |
| 8 | Any constraint on the JWT secret, algorithm or lifetime | `backend/app/core/config.py:L113` declares `SECRET_KEY: str`, `:L115` declares `ALGORITHM: str` and `:L114` declares `ACCESS_TOKEN_EXPIRE_MINUTES`, none with a validator, a minimum or an allowed-value list. `backend/app/core/security.py:L79` passes the algorithm value straight to `jwt.encode` | A weak secret, an attacker-influenced algorithm choice or an indefinite lifetime all pass configuration unchallenged |
| 9 | Issuer, audience and token identifier claims, and any revocation path | `backend/app/api/auth.py:L235-L239` encodes exactly two claims, `sub` and `exp`. The decode at `:L155` reads `sub` only, and `backend/app/core/security.py:L179` does the same | A token cannot be scoped to one service or one audience, and no issued token can be withdrawn before it expires |
| 10 | A declared, reviewed CORS origin list | `backend/app/main.py:L118` reads `settings.ALLOWED_ORIGINS`, and `backend/app/core/config.py:L111-L119` never declares that field, so the value comes from outside every declared contract. `:L119` sets `allow_credentials=True` while `:L120` and `:L121` allow every method and every header | Credentialed cross-origin access is granted on the strength of an undeclared value. Whether any origin is actually permitted cannot be established from this repository, because the field has no declared source |
| 11 | Object-level authorization on any template route | `backend/app/api/templates.py:L190`, `:L249` and `:L304` delegate to a `TemplateService`, and no file exists at `backend/app/services/template_service.py`. The 404 details at `:L192`, `:L251` and `:L306` read `Template not found or user not authorized`, so the message promises a check that no committed code performs | Any authenticated caller reaches any template once a service is supplied, unless that new service adds the check the message already advertises |
| 12 | Object-level authorization on eleven of the fourteen handlers | Three handlers attempt an owner comparison, at `backend/app/api/documents.py:L184`, `:L232` and `:L279`, each raising 403 at `:L185`, `:L233` and `:L280`. Document create and list perform none, and neither do the two profile handlers or the five template handlers | Bearer authentication alone decides access on eleven handlers, so holding any valid token is sufficient |

Entry 12 carries one further qualification. The three attempted comparisons do not currently run to
completion either. Each reads `.user_id` from a value the service returns, while
`backend/app/schema/document.py:L66` declares the field as `owner_id`. The call-site defects at
[G5](#g5-call-site-contract-violations) also stop the enclosing handlers before the comparison is
reached. Three attempted checks and eleven absent ones is the accurate count, and zero enforced checks
is the current state.

### G9.2 The frontend client

The client cannot build, for the reasons at [G8](#the-verified-type-check-profile). The controls below
are absent from its source regardless.

| # | Absent control | Evidence | What the absence permits |
|---|----------------|----------|--------------------------|
| 13 | Storage of the bearer token outside script-readable persistence | `frontend/src/services/auth.ts:L148` writes the login response value to `localStorage`, which persists past the tab and is readable by any script on the origin. Nothing reads it back. `frontend/src/services/api.ts:L142` reads `auth.token` from the Redux store instead, a key `frontend/src/store/index.ts` never registers, so the request interceptor throws and no request carries an `Authorization` header. The two stores are disconnected, and the write itself stores the string `"undefined"` today, because `frontend/src/services/auth.ts:L147` reads `accessToken` from a response that returns `access_token` | Any injected or third-party script on the origin reads whatever the write persists, and it survives the session. Reconciling the field name and the store turns that value into a live bearer token in the same place |
| 14 | Redaction before an error is logged | `frontend/src/services/auth.ts:L197`, `frontend/src/pages/Editor.tsx:L112` and `:L209`, `frontend/src/pages/Templates.tsx:L145` and `frontend/src/pages/Settings.tsx:L125` each pass a whole error object to `console.error`. An Axios error carries the request configuration, which includes the `Authorization` header, the full URL and the request body | Bearer tokens and document content reach the browser console and anything that collects from it |
| 15 | A request timeout or a cancellation path | `frontend/src/services/api.ts:L134-L136` creates the Axios instance with a `baseURL` and no `timeout`, and no call site passes an `AbortSignal` | A request hangs indefinitely, and no in-flight request can be withdrawn |
| 16 | Ordering protection on the auto-save path | `frontend/src/pages/Editor.tsx:L214` schedules a save five seconds after the last edit, and nothing tracks whether an earlier save is still in flight | A slower earlier save can land after a later one and overwrite newer content |
| 17 | Any applied response validation | Three Zod schemas exist under `frontend/src/schema/`, and no module passes a server response through any of them. `frontend/src/services/auth.ts:L240` asserts `as User` instead, which is a compile-time claim that checks nothing at runtime | Server responses are trusted unvalidated, and a schema that exists gives no protection |
| 18 | An allow-list on remote image sources | `frontend/src/components/Header.tsx:L77` renders `currentUser.avatar` and `frontend/src/pages/Templates.tsx:L182` renders `template.thumbnail`, both as an unconstrained `src`. Neither carries a `referrerPolicy`, and no Content Security Policy is committed | A stored URL causes the browser to contact an arbitrary host, disclosing the viewer address and referrer to it |

One frontend absence is easy to misread. `frontend/src/utils/validation.ts` expresses its email and
password rules correctly, and it is still not a control. The module cannot resolve its `zod` import,
no other module calls either function, and a client-side check never binds a caller who does not use
the client. [../frontend/src/utils/README.md](../frontend/src/utils/README.md) records all four
conditions.

### G9.3 Collaboration, background jobs and signed links

None of these paths executes as committed. Each entry names the absent control and the reason the
path does not run, because both facts matter to whoever repairs it.

| # | Absent control | Evidence | What the absence permits once the path runs |
|---|----------------|----------|---------------------------------------------|
| 19 | Authentication on the collaboration handshake | `backend/app/services/collaboration_service.py:L75` accepts `websocket`, `document_id` and `user_id` as plain arguments, and no route constructs the service, so nothing verifies a token before a socket is registered at `:L115-L117` | A caller supplies any `user_id` and joins as that identity |
| 20 | Authorization against the document being joined | The same method never checks that `user_id` may read `document_id` before it derives a topic at `:L120` and a subscription at `:L121` | Any caller joins the collaboration stream of any document identifier |
| 21 | Validation of `document_id` before it names a broker resource | `:L120` and `:L121` interpolate the value straight into Pub/Sub resource paths, and `:L173` does the same on disconnect | An unvalidated identifier selects or creates broker resources |
| 22 | A payload schema and a size bound on broadcast changes | `:L218` declares `change: dict` with no model behind it, and `:L248` serialises whatever arrives with `json.dumps` | Arbitrary unbounded structures are published to every subscriber |
| 23 | Producer authentication and authorization on the Celery broker | `backend/app/tasks/background_tasks.py:L98` builds the Celery application from `settings.REDIS_URL` alone. No service provides Redis, so no transport security, no access control list and no credential is configured anywhere. See [G8](#no-redis-service-backs-the-celery-broker) | Anyone who reaches the broker enqueues work that workers execute. What a deployed broker would actually permit cannot be established here, because no broker is provisioned |
| 24 | Format allow-listing and idempotency on the export task | `:L101` accepts `export_format` and `:L142` interpolates it into the object key `exports/{user_id}/{document_id}.{export_format}`. No allowed-value check and no deduplication key exists | A caller influences the stored object path, and a replayed message repeats the work |
| 25 | An authorization check before a signed link is minted | `backend/app/services/export_service.py:L160-L164` and `:L234-L238` generate a v4 signed URL immediately after upload, with no check that the requester may read the document | A link is issued to whoever reached the call |
| 26 | A reviewed expiry and a protected signing credential | The two v4 calls read `settings.SIGNED_URL_EXPIRATION`, a field `backend/app/core/config.py:L111-L119` never declares. `backend/app/tasks/background_tasks.py:L146` signs with `expiration=timedelta(hours=1)` and passes no `version`, so the two paths do not even agree on a signing scheme | A signed URL is a bearer credential, and possession alone authorises the read for the whole validity window |

Entries 25 and 26 describe code that never runs. `backend/app/tasks/background_tasks.py:L138` calls
`convert_document` on the export service, and
[G2](#absent-methods-on-classes-that-exist) records that the class never defines that method, so the
task raises before it reaches any upload or any signing call. `export_to_pdf` and `export_to_docx`
have no caller in `backend/app/` at all. No signed URL is produced by this repository today.

### G9.4 Supply chain and workflow identity

| # | Absent control | Evidence | What the absence permits |
|---|----------------|----------|--------------------------|
| 27 | Immutable action references | `.github/workflows/ci.yml:L13` and `:L15` and `.github/workflows/cd.yml:L11` and `:L13` each name a mutable tag. A tag can be moved or deleted by whoever controls the action repository, so a tag is a reference and not a pin. Only a full-length commit SHA is immutable. The March 2025 compromise of `tj-actions/changed-files` moved every tag in that repository | A third party changes the code your workflow runs without any change to this repository |
| 28 | A pinned runner and pinned base images | Both workflows request `ubuntu-latest`, at `ci.yml:L11` and `cd.yml:L9`. `infrastructure/docker/backend.Dockerfile:L2`, `frontend.Dockerfile:L2` and `:L20`, and `infrastructure/docker/docker-compose.yml:L31` each name a mutable tag rather than an `image@sha256:` digest | The build environment and the image contents change underneath an unchanged repository |
| 29 | A least-privilege `permissions:` block | Neither workflow file declares `permissions:` at any level, so `GITHUB_TOKEN` receives the repository default rather than the minimum each job needs | Every step in every job holds broader repository access than its work requires |
| 30 | Short-lived federated credentials | `.github/workflows/cd.yml:L16` supplies `GCP_SA_KEY`, a long-lived user-managed service account key held as a secret. Workload Identity Federation exchanges the workflow OIDC token for a short-lived credential and stores no key, and an attribute condition on the provider restricts which workflow may complete that exchange. No federation configuration is committed | A single leaked secret grants standing access until someone notices and rotates it |
| 31 | Any credential rotation or expiry mechanism | No workflow, script or Terraform file references key rotation, expiry or an age bound on `GCP_SA_KEY` | The key stays valid indefinitely |
| 32 | A gate between integration and deployment | `.github/workflows/cd.yml:L3-L5` triggers on every push to `main` and declares no `needs:`, no `workflow_run` and no `environment` | A deploy proceeds without the CI job passing and without an approval step |

### G9.5 Secrets, state and data retention

| # | Absent control | Evidence | What the absence permits |
|---|----------------|----------|--------------------------|
| 33 | Any ignore rule protecting generated state | No `.gitignore`, `.dockerignore` or `.terraformignore` is tracked anywhere in this repository. `infrastructure/terraform/main.tf` declares no `backend` block, so state is written locally, and Terraform state records resource attributes in clear text | A local state file, which can contain secret values, is one `git add` away from the history |
| 34 | A secret allow-list or a preflight on the deploy archive | `scripts/deploy.sh:L19` runs `zip -r app.zip . -x "*.git*" -x "node_modules/*" -x "venv/*"`, a deny-list of three patterns, and `:L23` uploads the archive with `gsutil cp`. Any `.env`, key file, credential or state file outside those three patterns is included | Local secrets leave the machine inside a deployed artifact |
| 35 | Failure handling in the deploy script | `scripts/deploy.sh` sets no `set -e`, installs no `trap` and inspects `$?` nowhere. Its only guard is the credentials check at `:L4-L7`. `:L47` prints `Deployment completed successfully!` unconditionally | Every stage failure is ignored, and the run reports success after failing |
| 36 | A retention or lifecycle rule on stored objects | `infrastructure/terraform/main.tf:L56-L58` enables bucket versioning and declares no `lifecycle_rule`. A delete on a versioned bucket leaves earlier generations readable | Content deleted through the application remains retrievable from earlier object generations indefinitely |
| 37 | Two credential literals safe to commit | `infrastructure/docker/docker-compose.yml:L35` sets `POSTGRES_PASSWORD=password`, and `scripts/setup_dev_environment.sh:L32` creates a database user with the same literal. Compose maps no port for the database service, which limits reach and does not make either literal safe | A committed credential is reused in an environment that is reachable |
| 38 | A supported runtime on any of three declared versions | Python 3.9 reached end of support on 31 October 2025 and is named at `infrastructure/docker/backend.Dockerfile:L2`. Node.js 14 left support on 30 April 2023, with its final release 14.21.3 shipped on 16 February 2023, and is named at `.github/workflows/ci.yml:L17` and `infrastructure/docker/frontend.Dockerfile:L2`. PostgreSQL 13 reached end of life on 13 November 2025 and is named at `infrastructure/docker/docker-compose.yml:L31` | Three components receive no security patches, and no future vulnerability in any of them will be fixed upstream |
| 39 | Any committed transport security or security headers | `infrastructure/docker/frontend.Dockerfile:L20` serves through `nginx:alpine`, and `:L26` leaves the `COPY nginx.conf` line commented out. No `nginx.conf` is tracked, so no TLS configuration, no HSTS, no Content Security Policy and no proxy rule is committed | The served client carries no transport or header protection from anything in this repository |
| 40 | A network rule narrower than the whole subnet | `infrastructure/terraform/main.tf:L35` declares a firewall rule opening TCP ports 0 through 65535 across the subnet range | Every port on every instance in the subnet is reachable from every other address in it |

### Where these entries are owned

Each module README carries the subset that applies to its own directory, with the same locators.
Start there when you are working inside one directory rather than surveying the whole repository.

- [../backend/app/api/README.md](../backend/app/api/README.md) owns entries 1 through 12
- [../backend/app/core/README.md](../backend/app/core/README.md) owns entries 8 through 10
- [../frontend/src/services/README.md](../frontend/src/services/README.md) owns entries 13 through 15 and 17
- [../frontend/src/pages/README.md](../frontend/src/pages/README.md) owns entries 14, 16 and 18
- [../backend/app/services/README.md](../backend/app/services/README.md) owns entries 19 through 22, 25 and 26
- [../backend/app/tasks/README.md](../backend/app/tasks/README.md) owns entries 23 and 24
- [../.github/workflows/README.md](../.github/workflows/README.md) owns entries 27 through 32
- [../infrastructure/terraform/README.md](../infrastructure/terraform/README.md) owns entries 33, 36 and 40
- [../scripts/README.md](../scripts/README.md) owns entries 34 and 35
- [../infrastructure/docker/README.md](../infrastructure/docker/README.md) owns entries 28, 37, 38 and 39

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
[decision-log.md](decision-log.md), planned for a later checkpoint and not committed yet.

| Line | Claim | Reality |
| ------ | ------- | --------- |
| `README.md:L29` | `git clone https://github.com/your-organization/microsoft-word.git` | A placeholder organisation. The command cannot succeed as written |
| `README.md:L42` | `pip install -r requirements.txt`, run from `backend/` | No `requirements.txt` exists anywhere in the repository, per [G4](#the-backend-has-no-dependency-manifest) |
| `README.md:L55` | `uvicorn main:app --reload`, run from `backend/` after `cd backend` at `L54` | The application object sits at `backend/app/main.py:L24`, one directory deeper. From `backend/`, the target is `app.main:app` |
| `README.md:L59-L66` | A project structure listing a root-level `docs/` at `L64` and a root-level `tests/` at `L65` | Half true as of this documentation set. A root-level `docs/` now exists, created by this engagement, so `L64` describes the tree correctly. No root-level `tests/` exists and this engagement creates none, so `L65` stays false. The only test modules sit at `backend/tests/`. Both halves are expanded below the table |
| `README.md:L81` | Claims an MIT licence and links to a licence file | No `LICENSE` file is committed, so the README's link resolves to nothing. This register quotes that markup as code rather than reproducing it, so no broken link appears here. `frontend/package.json` declares no `license` field either |
| `README.md:L86-L87` | `John Doe` and `Jane Smith` as project maintainers, with `example.com` addresses | Placeholder contacts |

Two notes on the structure claim at `README.md:L59-L66`, because the two halves of it diverge once
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
| `backend/app/main.py:L56` | marker | Low confidence in the startup and shutdown block below it | [G2](#the-absent-settings-singleton) |
| `backend/app/main.py:L67` | TODO | Database migration logic is unimplemented, inside the startup handler that awaits the absent `init_db` | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `backend/app/main.py:L113` | TODO | Shutdown cleanup tasks are unimplemented | none |
| `backend/app/api/users.py:L73` | marker | The code assumes a `UserService` class with an `update_user` method, and asks for verification | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `backend/app/core/security.py:L113` | marker | `get_current_user` needs review for its integration with the `User` model and `UserService`, neither of which this module imports | [G3](#g3-undefined-names-that-raise-at-execution) |
| `backend/app/services/document_service.py:L181` | marker | Asks for error handling and validation on `update_document`, the method the router calls with two arguments against three parameters | [G5](#argument-count-and-type) |
| `backend/app/services/collaboration_service.py:L73` | marker | `connect` carries a stated confidence of 0.6 and is not production ready | [G7](#the-collaboration-path-has-no-route-and-two-protocols) |
| `backend/app/services/collaboration_service.py:L216` | marker | `broadcast_change` carries a stated confidence of 0.7 and is not production ready | [G3](#g3-undefined-names-that-raise-at-execution) |
| `backend/app/services/export_service.py:L85` | marker | Both export methods have a low confidence score and need implementation detail or error handling | [G2](#absent-methods-on-classes-that-exist) |
| `backend/app/services/export_service.py:L151` | TODO | PDF conversion logic is unimplemented | [G2](#absent-methods-on-classes-that-exist) |
| `backend/app/services/export_service.py:L156` | TODO | The literal `"PDF_CONTENT"` uploaded at `:L157` stands in for a real document | [G2](#absent-methods-on-classes-that-exist) |
| `backend/app/services/export_service.py:L225` | TODO | DOCX conversion logic is unimplemented | [G2](#absent-methods-on-classes-that-exist) |
| `backend/app/services/export_service.py:L230` | TODO | The literal `"DOCX_CONTENT"` uploaded at `:L231` stands in for a real document | [G2](#absent-methods-on-classes-that-exist) |
| `backend/app/tasks/background_tasks.py:L128` | marker | `process_document_export` needs review for production readiness and error handling | [G2](#absent-methods-on-classes-that-exist) |
| `backend/app/tasks/background_tasks.py:L262` | marker | `cleanup_expired_documents` needs review for readiness, error handling and optimisation | [G3](#g3-undefined-names-that-raise-at-execution), [G5](#other-contract-violations) |

### Frontend markers and TODOs

| Location | Kind | What it flags | Class |
| ---------- | ------ | --------------- | ------- |
| `frontend/src/components/DocumentCanvas.tsx:L26` | marker | Component confidence below 0.8, on the component carrying the two inverse type errors | [G5](#type-inversions-in-the-editor-canvas) |
| `frontend/src/components/ImageEditor.tsx:L54` | marker | `handleInsertImage` needs review for production readiness | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `frontend/src/components/ImageEditor.tsx:L102` | marker | The component's rendered structure is unimplemented | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `frontend/src/components/TableEditor.tsx:L52` | marker | `handleInsertTable` carries a stated confidence of 0.6 | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `frontend/src/components/TextEditor.tsx:L80` | marker | `handleKeyCommand` needs review for production readiness | none. The module calls both formatting helpers correctly |
| `frontend/src/components/Toolbar.tsx:L26` | marker | The component needs refinement and error handling | [G5](#argument-count-and-type) |
| `frontend/src/components/Toolbar.tsx:L72` | TODO | Insert functionality is unimplemented, so the button at `:L89` does nothing | none |
| `frontend/src/pages/Editor.tsx:L29` | marker | The page needs review for production readiness | [G5](#argument-count-and-type) |
| `frontend/src/pages/Editor.tsx:L113` | TODO | Document load errors reach the console only | none |
| `frontend/src/pages/Editor.tsx:L210` | TODO | Auto-save errors reach the console only, with no user notification | none |
| `frontend/src/pages/Settings.tsx:L35` | marker | The page needs refinement for production readiness | [G2](#absent-frontend-exports) |
| `frontend/src/pages/Settings.tsx:L123` | TODO | No success message follows a settings save | none |
| `frontend/src/pages/Settings.tsx:L126` | TODO | Save errors produce no user feedback | none |
| `frontend/src/pages/Templates.tsx:L146` | marker | Carries no body text of its own and sits directly above the TODO at `:L147`, on the template fetch path | [G2](#absent-frontend-exports) |
| `frontend/src/pages/Templates.tsx:L147` | TODO | Template fetch errors have no handling or user feedback | none |
| `frontend/src/pages/Templates.tsx:L165` | marker | Carries no body text of its own and sits directly above the TODO at `:L166`, on template selection | [G6](#field-and-shape-divergences) |
| `frontend/src/pages/Templates.tsx:L166` | TODO | Selecting a template navigates nowhere, so the card click is terminal | none |
| `frontend/src/services/collaboration.ts:L89` | marker | Inbound collaboration event listeners are unimplemented, inside the otherwise empty `setupEventListeners` body | [G7](#the-collaboration-path-has-no-route-and-two-protocols) |
| `frontend/src/services/collaboration.ts:L95` | marker | `joinDocument` emits an event no server route receives | [G7](#the-collaboration-path-has-no-route-and-two-protocols) |
| `frontend/src/services/collaboration.ts:L159` | marker | `sendChanges` emits a payload shape the server does not expect | [G7](#the-collaboration-path-has-no-route-and-two-protocols) |
| `frontend/src/store/documentSlice.ts:L171` | marker | The slice lacks asynchronous actions and error handling for document fetch and save | [G2](#absent-frontend-exports) |
| `frontend/src/store/userSlice.ts:L149` | marker | Names three gaps directly, including an `updateUser` action and selectors for state access, both of which four modules already import | [G2](#absent-frontend-exports) |
| `frontend/src/utils/documentUtils.ts:L24` | marker | Both functions need error handling, and states that the `DocumentSchema` validation needs to be implemented correctly | [G5](#other-contract-violations) |
| `frontend/src/utils/documentUtils.ts:L43` | TODO | `DocumentSchema` validation in `serializeDocument` is unimplemented | [G5](#other-contract-violations) |
| `frontend/src/utils/documentUtils.ts:L72` | TODO | `DocumentSchema` validation in `deserializeDocument` is unimplemented | [G5](#other-contract-violations) |

### Test suite markers

These three sit in files that receive no inline documentation. See
[../backend/tests/README.md](../backend/tests/README.md).

| Location | Kind | What it flags | Class |
| ---------- | ------ | --------------- | ------- |
| `backend/tests/test_api.py:L13` | marker | The test database connection is unconfigured. The fixture body directly below is a bare `pass` at `:L14` | [G1](#modules-referenced-only-by-the-test-suite) |
| `backend/tests/test_api.py:L77` | marker | Endpoint coverage is incomplete, with no edge cases and no error scenarios | [G1](#modules-referenced-only-by-the-test-suite) |
| `backend/tests/test_db.py:L56` | marker | Update, delete and error-handling cases are absent | [G1](#modules-referenced-only-by-the-test-suite) |

### Infrastructure, container and script markers

| Location | Kind | What it flags | Class |
| ---------- | ------ | --------------- | ------- |
| `infrastructure/terraform/main.tf:L94` | marker | Asks for review of the subnet range, of whether more firewall rules are needed, and of the bucket configuration. The firewall it points at opens every TCP port to the subnet | [G8](#other-terraform-defects) |
| `infrastructure/terraform/outputs.tf:L58` | marker | States that the outputs may not match the resources the configuration actually creates. Every output reads an AWS address, and the only provider is `google` | [G8](#terraform-outputs-describe-a-different-cloud) |
| `infrastructure/docker/backend.Dockerfile:L22` | marker | Asks for verification that `requirements.txt` sits in the right place and that the application code is in `./app`. Neither holds: no `requirements.txt` exists, and `:L14` flattens the package | [G8](#the-backend-image-cannot-build-or-start) |
| `scripts/deploy.sh:L37` | marker | Post-deployment checks are unimplemented, so `:L47` reports success unconditionally | [G8](#the-setup-script-targets-the-wrong-framework) |
| `scripts/setup_dev_environment.sh:L41` | marker | Environment configuration needs manual completion, immediately after `:L40` copies an `.env.example` that does not exist | [G8](#the-setup-script-targets-the-wrong-framework) |
| `scripts/setup_dev_environment.sh:L42` | TODO | The `.env` file needs production values, in a file the preceding line failed to create | [G8](#the-setup-script-targets-the-wrong-framework) |

## Where to go next

| Question | Document |
| ---------- | ---------- |
| What can I run today, and what should I fix first? | [onboarding.md](onboarding.md) |
| How do the six top-level areas fit together? | [architecture-overview.md](architecture-overview.md) |
| Which contract is authoritative for a given field? | [data-model.md](data-model.md) |
| Which external services does the code reach, and what blocks each one? | [integration-guide.md](integration-guide.md) |
| Why does a deploy fail? | [deployment-guide.md](deployment-guide.md) |
| Why was something documented this way? | [decision-log.md](decision-log.md), planned and not yet committed |
| Where is the index for this documentation set? | [README.md](README.md), planned and not yet committed |

The three specification documents record declared intent and never committed behaviour. Read them as
the design the code was aiming at:

- [Technical Specifications](<../documentation/Technical Specifications.md>)
- [Software Requirements Specifications](<../documentation/Software Requirements Specifications (SRS).md>)
- [Software Project Proposal](<../documentation/Software Project Proposal.md>)

One divergence between intent and code is worth naming here, because it looks like a defect and is
not one. The requirements specification calls for a 30-second auto-save at
`documentation/Software Requirements Specifications (SRS).md:L543`, under the requirement group for
file management. The editor implements a five-second debounce at
`frontend/src/pages/Editor.tsx:L214`. The code is internally consistent, and the two documents
disagree. See [../frontend/src/pages/README.md](../frontend/src/pages/README.md).
