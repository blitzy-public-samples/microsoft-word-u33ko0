# Troubleshooting and Defect Register

The `microsoft-word-u33ko0` repository does not run. The backend cannot import, and only 3 of the
15 modules under `backend/app/` load. The frontend cannot typecheck, and `tsc --noEmit` reports 76
errors. Neither container builds, the Terraform cannot initialise, and both `npm ci` invocations
fail. Every one of those failures appears below with the file and line that causes it.

This document records defects. Repairing them fell outside the documentation engagement that
produced this file, so that engagement fixed none of them. Read no entry here as fixed. See
[decision-log.md](decision-log.md) for the record of that boundary.

## How to read this register

Two orderings run through this document, and they serve different readers.

The [symptom-first index](#symptom-first-index) runs in **encounter order**. Rows follow the
sequence a developer meets them while working through the setup steps in
[the root README](../README.md), starting with a clone and ending at a deploy. Each row names a
defect class and points into the section that carries the detail.

Sections `G1` through `G8` run in **taxonomy order** and stay there, because a reference section is
easier to return to when its position never moves. Read the index to find your problem. Read the
taxonomy section to understand it.

### The defect classes

| Class | Covers |
|-------|--------|
| [G1](#g1-absent-modules-referenced-by-committed-code) | Absent modules referenced by committed code |
| [G2](#g2-absent-symbols-inside-modules-that-do-exist) | Absent symbols inside modules that do exist |
| [G3](#g3-undefined-names-that-raise-at-execution) | Undefined names with no import behind them |
| [G4](#g4-undeclared-third-party-dependencies) | Third-party packages the code imports and no manifest declares |
| [G5](#g5-call-site-contract-violations) | Calls that disagree with the signature they target |
| [G6](#g6-field-and-shape-drift) | Field names and shapes that disagree across a boundary |
| [G7](#g7-endpoint-and-transport-mismatch) | Client routes, server routes and transports that do not meet |
| [G8](#g8-platform-and-automation-defects) | Container, pipeline, script and infrastructure defects |

### How citations work

Every factual claim carries a locator in the form `path:Lnn`, and most locators also name the
symbol at that line. Read the symbol name as the durable half of the citation. Line numbers move
whenever anyone edits a file above them, and symbol names do not.

Three conventions govern the locators:

- Locators point at the **committed state at the current branch head**, which includes the inline
  documentation added to 44 source files. A locator therefore matches what you see when you open
  the file today, not what an earlier revision held.
- Line numbers are **physical**. No tracked file in this repository ends with a newline, so
  `wc -l` reports one line fewer than each file contains. Counting tools that rely on trailing
  newlines will disagree with this register by one line.
- A range such as `L111-L119` covers every line in the span, inclusive.

### Terminology

The words below carry one fixed meaning throughout this register.

| Term | Meaning |
|------|---------|
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
  [decision-log.md](decision-log.md). Arguments live there.
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
|---------|---------------------|-------|----------|
| `git clone` targets a placeholder organisation and fails | Following step 1 of the README installation section | [README](#documentation-inaccuracies-in-the-root-readme) | `README.md:L29` names `github.com/your-organization/microsoft-word.git` |
| `npm install` succeeds and resolves 1,532 packages | Installing frontend dependencies | none | Verified in `frontend/`. The five packages at [G4](#g4-undeclared-third-party-dependencies) stay missing because no manifest lists them |
| `pip install -r requirements.txt` fails, no such file | Installing backend dependencies | [G4](#g4-undeclared-third-party-dependencies) | No `requirements.txt` exists anywhere. `README.md:L42` and `scripts/setup_dev_environment.sh:L26` both invoke it |
| `tsc --noEmit` reports 76 errors, so the build fails | Starting or building the frontend | [G1](#g1-absent-modules-referenced-by-committed-code), [G2](#g2-absent-symbols-inside-modules-that-do-exist), [G4](#g4-undeclared-third-party-dependencies) | Distribution in [the type-check profile](#the-verified-type-check-profile) |
| The interface renders with no styling at all | Viewing the running frontend | [G8](#tailwind-never-compiles) | No `tailwind.config.js`, no `postcss.config.js` and no committed stylesheet |
| `uvicorn main:app --reload` cannot find the application | Starting the backend from `backend/` per the README | [README](#documentation-inaccuracies-in-the-root-readme) | The application object sits at `backend/app/main.py:L24` (`app = FastAPI()`), one directory deeper |
| `ImportError: cannot import name 'settings' from 'app.core.config'` | Importing `app.main` from `backend/` | [G2](#the-absent-settings-singleton) | `backend/app/main.py:L16` reaches `backend/app/api/auth.py:L84`, which requests a name `backend/app/core/config.py` never defines |
| `ModuleNotFoundError: No module named 'app.schema.template'` | Importing `app.api.templates` | [G1](#g1-absent-modules-referenced-by-committed-code) | `backend/app/api/templates.py:L75` |
| `ModuleNotFoundError: No module named 'app.services.user_service'` | Importing `app.api.users` or `app.api.auth` | [G1](#g1-absent-modules-referenced-by-committed-code) | `backend/app/api/users.py:L27` and `backend/app/api/auth.py:L86` |
| `NameError: name 'Optional' is not defined` | Importing `app.core.security` | [G3](#g3-undefined-names-that-raise-at-execution) | `backend/app/core/security.py:L50` uses `Optional` with no import behind it |
| Template endpoints return document responses | Calling any `/{id}` route | [G7](#documents-and-templates-collide-on-identical-paths) | `backend/app/main.py:L125-L128` mounts every router with no prefix |
| `npm ci` fails with `EUSAGE` in continuous integration | Running the CI workflow | [G8](#npm-ci-cannot-run-anywhere) | `.github/workflows/ci.yml:L19` runs at the repository root, where no manifest and no lockfile exist |
| `docker compose build` cannot find a Dockerfile | Building the containers | [G8](#compose-points-at-dockerfiles-that-are-not-there) | `infrastructure/docker/docker-compose.yml:L6-L7` and `:L19-L20` |
| `terraform init` reports `Unreadable module directory` | Initialising the infrastructure | [G8](#three-terraform-module-sources-do-not-exist) | `infrastructure/terraform/main.tf:L67`, `:L76`, `:L85`. No `modules/` directory exists |
| Celery workers have no broker to attach to | Running background jobs | [G8](#no-redis-service-backs-the-celery-broker) | `backend/app/tasks/background_tasks.py:L98` reads `settings.REDIS_URL`, and no service provides Redis |
| The deploy step uploads descriptors that do not exist | Running the CD workflow | [G8](#the-cd-workflow-deploys-two-absent-descriptors) | `.github/workflows/cd.yml:L19-L20` deploys `app.yaml` and `dispatch.yaml` |

## G1 absent modules referenced by committed code

Committed code imports ten application modules that no file provides, and the test suite imports
five more. Each import below resolves to nothing, so the importing module cannot load.

### Application modules

| Absent module | Requested at | Symbols requested | Effect |
|---------------|--------------|-------------------|--------|
| `app.services.user_service` | `backend/app/api/auth.py:L86`, `backend/app/api/users.py:L27` | `UserService` | Both routers fail to import. `backend/app/core/security.py:L188` also constructs `UserService()` with no import at all, covered in [G3](#g3-undefined-names-that-raise-at-execution) |
| `app.schema.template` | `backend/app/api/templates.py:L75` | `Template`, `TemplateCreate`, `TemplateUpdate` | The template router fails to import. No Pydantic contract for a template exists anywhere in the backend |
| `app.services.template_service` | `backend/app/api/templates.py:L76` | `TemplateService` | The template router has no service tier behind its five handlers |
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

`backend/app/api/templates.py:L75-L76` is the clearest example of the pattern in the whole
repository: one module, two imports, neither target present. The engagement that produced this
register corrected an earlier attribution of this example to
`backend/app/services/document_service.py`, which carries no such import. See
[decision-log.md](decision-log.md).

Full treatment sits in [../backend/app/api/README.md](../backend/app/api/README.md),
[../frontend/src/components/README.md](../frontend/src/components/README.md) and
[../backend/app/db/README.md](../backend/app/db/README.md).

### Modules referenced only by the test suite

The three modules under `backend/tests/` import five further roots that do not exist, using three
mutually incompatible import conventions. No test in this repository can collect.

| Absent root | Requested at | Import convention |
|-------------|--------------|-------------------|
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
|------------------|------|
| `backend/app/main.py` | `L20` |
| `backend/app/api/auth.py` | `L84` |
| `backend/app/db/firestore.py` | `L38` |
| `backend/app/db/sql.py` | `L14` |
| `backend/app/services/collaboration_service.py` | `L39` |
| `backend/app/services/document_service.py` | `L62` |
| `backend/app/services/export_service.py` | `L61` |
| `backend/app/tasks/background_tasks.py` | `L92` |

Each import raises `ImportError: cannot import name 'settings' from 'app.core.config'`.
`backend/app/core/security.py:L45` imports `get_settings` instead, which exists, so that module's
configuration import resolves. [G3](#g3-undefined-names-that-raise-at-execution) records why
`app.core.security` still fails.

### The verified import census

The census imported each of the 15 modules under `backend/app/` in a fresh interpreter, with
third-party packages present and Pydantic pinned to the 1.x line the code requires. The result:
**3 modules import successfully and 12 fail.**

| Outcome | Modules |
|---------|---------|
| Imports (3) | `app.core.config`, `app.schema.document`, `app.schema.user` |
| Fails (12) | `app.main`, `app.api.auth`, `app.api.documents`, `app.api.templates`, `app.api.users`, `app.core.security`, `app.db.firestore`, `app.db.sql`, `app.services.collaboration_service`, `app.services.document_service`, `app.services.export_service`, `app.tasks.background_tasks` |

The 12 failures resolve to three distinct causes, so repairing one name clears three quarters of
them:

| Cause | Count | Modules affected |
|-------|-------|------------------|
| The absent `settings` singleton | 9 | `app.main`, `app.api.auth`, `app.api.documents`, `app.db.firestore`, `app.db.sql`, `app.services.collaboration_service`, `app.services.document_service`, `app.services.export_service`, `app.tasks.background_tasks` |
| An absent module, per [G1](#g1-absent-modules-referenced-by-committed-code) | 2 | `app.api.templates` (`app.schema.template`), `app.api.users` (`app.services.user_service`) |
| An undefined name, per [G3](#g3-undefined-names-that-raise-at-execution) | 1 | `app.core.security` (`Optional`) |

`app.main` surfaces its failure at `backend/app/api/auth.py:L84`, reached through
`backend/app/main.py:L16`. Two modules fail indirectly through the Firestore adapter:
`app.api.documents` and `app.services.document_service` both surface at
`backend/app/db/firestore.py:L38`. See [../backend/app/README.md](../backend/app/README.md), which
owns the census figure and the package-boundary statement.

### The four router names

`backend/app/main.py:L16-L19` imports `auth_router`, `documents_router`, `users_router` and
`templates_router`. All four router modules export the bare name `router` instead.

| Requested name | Requested at | Provided name |
|----------------|--------------|---------------|
| `auth_router` | `backend/app/main.py:L16` | `router` in `backend/app/api/auth.py` |
| `documents_router` | `backend/app/main.py:L17` | `router` in `backend/app/api/documents.py` |
| `users_router` | `backend/app/main.py:L18` | `router` in `backend/app/api/users.py` |
| `templates_router` | `backend/app/main.py:L19` | `router` in `backend/app/api/templates.py` |

All four names are then passed to `include_router` at `backend/app/main.py:L125-L128`.

### Absent methods on classes that exist

| Symbol | Called at | Defined on |
|--------|-----------|------------|
| `DocumentService.get_documents` | `backend/app/api/documents.py:L145` | nothing. `DocumentService` defines `create_document` (`L74`), `get_document` (`L125`), `update_document` (`L185`) and `delete_document` (`L254`) |
| `ExportService.convert_document` | `backend/app/tasks/background_tasks.py:L138` | nothing. `ExportService` defines `export_to_pdf` (`L87`) and `export_to_docx` (`L168`) |

### Absent frontend exports

One omission in `frontend/src/schema/document.ts` causes five separate compiler errors, which makes
it the cheapest entry in this register to act on. The module exports two Zod schemas,
`DocumentSchema` at `L65` and `DocumentVersionSchema` at `L86`, and it exports **no inferred type**.
Both sibling schema modules do export one:
`frontend/src/schema/user.ts:L56` and `frontend/src/schema/template.ts:L41` each end with a
`z.infer` type export. The single omission produces five of the six `TS2305` errors in the whole
frontend:

| Requested symbol | Requested at |
|------------------|--------------|
| `Document`, `DocumentCreate`, `DocumentUpdate` | `frontend/src/services/api.ts:L80` |
| `Document` | `frontend/src/services/collaboration.ts:L15` |
| `Document` | `frontend/src/store/documentSlice.ts:L22` |

`frontend/src/store/index.ts` omits two hooks that seven modules import, and registers neither of
two named exports its consumers expect:

| Absent symbol | Expected from | Requested at |
|---------------|---------------|--------------|
| `useAppSelector`, `useAppDispatch` | `frontend/src/store/index.ts` | seven modules across the four pages and three components |
| `documentReducer` | `frontend/src/store/documentSlice.ts` | `frontend/src/store/index.ts:L21`. The slice exports its reducer as the module default at `L169` |
| `userReducer` | `frontend/src/store/userSlice.ts` | `frontend/src/store/index.ts:L22`. The slice exports its reducer as the module default at `L147` |
| `updateDocument`, `selectCurrentDocument` | `frontend/src/store/documentSlice.ts` | `frontend/src/components/DocumentCanvas.tsx:L23`, `frontend/src/components/Toolbar.tsx:L24`. The slice exports exactly six actions at `L154-L161`, and `updateDocument` is not among them |
| `updateUser`, `selectCurrentUser` | `frontend/src/store/userSlice.ts` | `frontend/src/pages/Settings.tsx:L33`, plus `selectCurrentUser` at `frontend/src/components/Header.tsx:L23`, `frontend/src/pages/Home.tsx:L23` and `frontend/src/pages/Templates.tsx:L37`. The slice exports `setUser`, `clearUser`, `setLoading` and `setError` at `L139` |
| `getDocument`, `updateUserSettings` | `frontend/src/services/api.ts` | `frontend/src/pages/Editor.tsx:L25` and `frontend/src/pages/Settings.tsx:L31`. The module exports only `getDocuments` (`L217`), `createDocument` (`L245`) and `updateDocument` (`L287`) |
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
|------|---------------|-------------|
| `Optional` | `backend/app/core/security.py:L50`, in the `create_access_token` signature | the module body executes, so at import |
| `User` | `backend/app/core/security.py:L119`, as the `get_current_user` return annotation | the module body executes, so at import |
| `UserService` | `backend/app/core/security.py:L188`, inside `get_current_user` | `get_current_user` first runs |
| `asyncio` | `backend/app/services/collaboration_service.py:L163`, inside the Pub/Sub `callback` | a published message first arrives |
| `json` | `backend/app/services/collaboration_service.py:L248`, inside `broadcast_change` | `broadcast_change` first runs |
| `datetime` | `backend/app/tasks/background_tasks.py:L267`, inside `cleanup_expired_documents` | the retention sweep first runs |
| `datetime` | `backend/app/tasks/background_tasks.py:L321`, inside `update_document_statistics` | the statistics task first runs |

`backend/app/tasks/background_tasks.py:L96` imports `timedelta` alone, so `timedelta` resolves at
both `L146` and `L151` while `datetime` resolves nowhere.

### Two of the seven raise at import, not at execution

Python evaluates a function's annotations when the `def` statement runs, so an undefined name in a
signature fails as the module loads rather than when the function is called. `Optional` at
`backend/app/core/security.py:L50` therefore raises
`NameError: name 'Optional' is not defined` during import of `app.core.security`, and the module
cannot import at all. `User` at `L119` would raise the same way, and `L50` raises first, so
execution never reaches it.

The remaining five references sit inside function bodies and raise only when that function runs.
The register states the mechanism because the two cases need different diagnosis: a signature
failure appears in an import traceback, and a body failure appears only under exercise.

### Two findings in this file that are not defects

Diagnosing `backend/app/core/security.py` goes wrong in two predictable ways, so this register
records both explicitly.

- **`backend/app/core/security.py:L45` imports `get_settings`, not `settings`.** That name exists,
  at `backend/app/core/config.py:L126`. The configuration import in this one module resolves
  correctly, unlike the eight listed in
  [G2](#the-absent-settings-singleton). The real defects in this file are the three undefined names
  above.
- **`except jwt.JWTError` at `backend/app/core/security.py:L185` resolves correctly and is not a
  defect.** `L41` imports `jwt` from `jose`, and the installed `python-jose` distribution exposes
  `JWTError` on that module. Recording the line as broken would send a reader after a working
  import.

See [../backend/app/core/README.md](../backend/app/core/README.md),
[../backend/app/services/README.md](../backend/app/services/README.md) and
[../backend/app/tasks/README.md](../backend/app/tasks/README.md).

## G4 undeclared third-party dependencies

The frontend imports five packages its manifest does not declare, and the backend has no manifest
at all.

### Five npm packages the code imports and the manifest omits

`frontend/package.json:L6-L14` declares exactly seven runtime dependencies: `@reduxjs/toolkit`,
`react`, `react-dom`, `react-redux`, `react-router-dom`, `tailwindcss` and `typescript`. The five
below appear in import statements and in no dependency list.

| Package | Importing modules | Sample locator |
|---------|-------------------|----------------|
| `draft-js` | 6 | `frontend/src/utils/documentUtils.ts:L21`, `frontend/src/utils/formatting.ts:L13`, `frontend/src/components/DocumentCanvas.tsx:L21` |
| `zod` | 3 | all three modules under `frontend/src/schema/` |
| `axios` | 2 | `frontend/src/services/api.ts:L78`, `frontend/src/services/auth.ts:L68` |
| `socket.io-client` | 1 | `frontend/src/services/collaboration.ts:L13` |
| `@types/draft-js` | 0 direct imports | required to typecheck the six `draft-js` importers, and absent from `devDependencies` at `frontend/package.json:L15-L30` |

`npm install` inside `frontend/` succeeds and resolves 1,532 packages, and it installs none of the
five, because a package manager installs what a manifest declares. The five contribute 13 of the
57 `TS2307` errors.

### The backend has no dependency manifest

No `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `tox.ini`, `Pipfile` or
`.python-version` exists anywhere in the repository. Two committed instructions install from a file
that was never added: `README.md:L42` and `scripts/setup_dev_environment.sh:L26` both run
`pip install -r requirements.txt`, and
`infrastructure/docker/backend.Dockerfile:L8` copies `requirements.txt` into the image before
`L11` installs from it.

A developer must infer the dependency set from import statements. Seven third-party root modules
appear across `backend/app/`:

| Import root | Distribution supplying it | Established by |
|-------------|---------------------------|----------------|
| `fastapi` | `fastapi`, 0.89.0 or newer | Response models come from return annotations, and no handler passes `response_model=` |
| `pydantic` | `pydantic`, 1.x only | `backend/app/core/config.py:L48` imports `BaseSettings` from the main package, and `backend/app/schema/user.py:L177` sets `orm_mode`. Pydantic 2 moved `BaseSettings` to `pydantic-settings` and renamed `orm_mode` |
| `sqlalchemy` | `SQLAlchemy`, 1.4 or newer | `backend/app/db/sql.py:L13` imports `declarative_base` from `sqlalchemy.orm`, where 1.4 moved it |
| `jose` | `python-jose` | `backend/app/api/auth.py` and `backend/app/core/security.py:L41`. The import name and the distribution name differ |
| `passlib` | `passlib` | `CryptContext` in the same two modules |
| `celery` | `celery` | `backend/app/tasks/background_tasks.py:L98` |
| `google` | `google-cloud-firestore`, `google-cloud-pubsub`, `google-cloud-storage` and `google-auth` | one namespace splits across four distributions: `google.cloud.firestore`, `google.cloud.pubsub_v1`, `google.cloud.storage` and `google.auth` |

### The progressive Python dependency-resolution failure

The backend requires seventeen distributions to run, and six of them are transitive-only, meaning
no import statement names them. A developer building an environment by reading import statements
installs the visible packages, retries, and hits the next missing piece. The build fails
progressively rather than once. Four properties of this repository cause that pattern:

- **One import name does not match its distribution name.** `import jose` needs `python-jose`.
  Guessing `pip install jose` installs an unrelated package.
- **One namespace maps to four distributions.** `from google.cloud... import` gives no hint that
  Firestore, Pub/Sub, Cloud Storage and authentication ship separately.
- **Two runtime needs appear in no import statement.** `passlib` performs bcrypt hashing at
  `backend/app/api/auth.py` and does not depend on `bcrypt`, so password hashing fails until a
  developer adds `bcrypt` by hand. `uvicorn` appears in no import statement, and
  `infrastructure/docker/backend.Dockerfile:L20` requires it.
- **Two version ceilings are invisible without reading the code.** Installing the current
  `pydantic` breaks `backend/app/core/config.py:L48` immediately, because the 1.x constraint lives
  in an import statement rather than in a manifest.

[onboarding.md](onboarding.md) records the working package set for a first-time environment build.

### The unmapped import prefix

Essentially every frontend module imports through a `@/` prefix, and no configuration maps it.
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
|-----------|------|------------------|--------------|
| `backend/app/api/documents.py:L111` | `create_document(document, current_user)` | `create_document(self, document: DocumentCreate, user_id: str)` at `backend/app/services/document_service.py:L74` | Passes a `User` object where the signature declares `user_id: str` |
| `backend/app/api/documents.py:L186` | `get_document(document_id)` | `get_document(self, document_id: str, user_id: str)` at `backend/app/services/document_service.py:L125` | One argument against two parameters, so the ownership check cannot run |
| `backend/app/api/documents.py:L234` | `get_document(document_id)` | the same two-parameter signature | One argument against two |
| `backend/app/api/documents.py:L281` | `get_document(document_id)` | the same two-parameter signature | One argument against two |
| `backend/app/api/documents.py:L237` | `update_document(document_id, document)` | `update_document(self, document_id: str, document: DocumentUpdate, user_id: str)` at `backend/app/services/document_service.py:L185` | Two arguments against three parameters |
| `backend/app/api/documents.py:L284` | `delete_document(document_id)` | `delete_document(self, document_id: str, user_id: str)` at `backend/app/services/document_service.py:L254` | One argument against two |
| `backend/app/tasks/background_tasks.py:L310` | `get_document(document_id)` | the same two-parameter signature | One argument against two |
| `frontend/src/components/Toolbar.tsx:L62` | `applyInlineStyle(style)` | `applyInlineStyle(editorState: EditorState, inlineStyle: string)` at `frontend/src/utils/formatting.ts:L31` | One argument against two, and the missing argument is the editor state the helper transforms |
| `frontend/src/components/Toolbar.tsx:L67` | `applyBlockStyle(style)` | `applyBlockStyle(editorState: EditorState, blockType: string)` at `frontend/src/utils/formatting.ts:L61` | One argument against two |
| `frontend/src/pages/Editor.tsx:L238` | `<DocumentCanvas content={...} onContentChange={...} />` | `const DocumentCanvas: React.FC = () => {` at `frontend/src/components/DocumentCanvas.tsx:L108` | Two props passed to a component declaring none |

One call site in the same repository gets the contract right, which is worth knowing when reading
the rows above. `backend/app/tasks/background_tasks.py:L135` calls
`get_document(document_id, user_id)` with both arguments, while `L310` in the same file passes one.
`frontend/src/components/TextEditor.tsx:L109` and `:L116` call both formatting helpers with both
arguments, while `Toolbar.tsx` passes one to each. Comparing the working call with the broken one
shows the contract faster than reading either alone.

### Type inversions in the editor canvas

`frontend/src/components/DocumentCanvas.tsx` carries two errors that are exact inverses, so
correcting one in isolation risks reinforcing the other.

| Line | Call | Receives | Expects |
|------|------|----------|---------|
| `L117` | `EditorState.createWithContent(contentState)` | an `EditorState`, returned by `deserializeDocument` at `frontend/src/utils/documentUtils.ts:L63` and assigned at `DocumentCanvas.tsx:L116` | a `ContentState` |
| `L163` | `serializeDocument(newEditorState.getCurrentContent())` | a `ContentState`, returned by `getCurrentContent()` | an `EditorState`, per `frontend/src/utils/documentUtils.ts:L39` |

`DocumentCanvas.tsx:L21` imports `ContentState` and never uses it.

### Other contract violations

| Site | Violation |
|------|-----------|
| `backend/app/tasks/background_tasks.py:L283` | Calls `.delete()` on the result of `.get()`, which returns a list of documents rather than a reference. Lists carry no `delete` method |
| `backend/app/api/users.py:L80` | Calls `user_service.update_user(...)` from the synchronous handler declared at `L54`, so the call cannot be awaited. A coroutine object is always truthy, so if the absent `UserService` declares the method `async`, the guard at `L81` can never observe a failure. `app.services.user_service` does not exist, so no contract settles which it is |
| `backend/app/api/users.py:L33`, `:L54` | Both handlers use plain `def` while all 12 other handlers use `async def` |
| `backend/app/tasks/background_tasks.py:L151` | Stacks `@celery_app.periodic_task(run_every=timedelta(days=1))` beneath `@celery_app.task` at `L150`. Celery 5 exposes no `periodic_task` decorator, so the module raises `AttributeError` once the earlier import failures clear |
| `backend/app/db/firestore.py:L44-L70` | `get_document` is annotated `-> dict` and returns `None` at `L70` when the document is absent |
| `frontend/src/utils/documentUtils.ts:L44`, `:L73` | Calls `DocumentSchema.isValid(...)`. Zod exposes `parse` and `safeParse` and no `isValid`, and the argument is Draft.js content while `DocumentSchema` models document metadata, so the check targets the wrong contract twice over |

## G6 field and shape drift

No artifact keeps the two languages in agreement. The repository commits no OpenAPI document,
generates no client, and shares no schema package across the Python and TypeScript trees.
Developers therefore maintain the Pydantic models under `backend/app/schema/` and the Zod schemas
under `frontend/src/schema/` by hand, and the divergences below follow from that.

### The ownership field, four positions

Authorization in this repository compares an ownership field, and four positions disagree about its
name. **No position is canonical.** Selecting one would change an interface, which the documentation
engagement excluded, so this register lists all four and prefers none. See
[decision-log.md](decision-log.md) and the full treatment in [data-model.md](data-model.md).

| Position | Locator | Field |
|----------|---------|-------|
| The Pydantic document contract | `backend/app/schema/document.py:L68`, on `DocumentBase` and inherited by `Document` | `owner_id: Optional[str] = None` |
| The Pydantic version contract | `backend/app/schema/document.py:L137`, on `DocumentVersion` | `user_id: str` |
| The document service | `backend/app/services/document_service.py:L118` writes it, and `:L177`, `:L243` and `:L282` compare it | `user_id` |
| The in-repository specification, declared intent | `documentation/Technical Specifications.md:L333`, `:L375`, `:L383`, under the SYSTEM DESIGN heading at `L300` | `owner_id` |

Two details make the drift worse than a naming disagreement.

The first: `owner_id` at `backend/app/schema/document.py:L68` is optional and defaults to `None`, so
a `Document` validates successfully without the field that authorization depends on. The contract
never requires the value the ownership check reads.

The second: the document router reads `.user_id` off objects typed as `Document` at
`backend/app/api/documents.py:L187`, `:L235` and `:L282`. The router follows the service convention
rather than the contract its own type annotation names. The client repeats the same split, with
`owner_id` at `frontend/src/schema/document.ts:L69` and `user_id` at `:L91`.

### Field and shape divergences

| Divergence | Client or consumer | Server or contract |
|------------|--------------------|--------------------|
| Access token field | `frontend/src/services/auth.ts:L147` reads `response.data.accessToken` and stores it at `:L148` | The token handler at `backend/app/api/auth.py:L170-L171` follows the OAuth2 convention and returns `access_token` |
| Base URL variable | `frontend/src/services/api.ts:L82` reads `process.env.REACT_APP_API_BASE_URL` | `infrastructure/docker/docker-compose.yml:L11` injects `REACT_APP_API_URL`. The names never meet, so the client resolves an undefined base URL |
| User display name | `frontend/src/components/Header.tsx:L77-L78`, `frontend/src/pages/Home.tsx:L59` and `frontend/src/pages/Settings.tsx:L82` read `currentUser.name` | `backend/app/schema/user.py:L81-L82` models `username` and `full_name`. No contract declares `name` |
| User avatar | `frontend/src/components/Header.tsx:L77` reads `currentUser.avatar` | No contract in either language declares `avatar` |
| Page count | `backend/app/tasks/background_tasks.py:L314` reads `len(document.pages)` | `backend/app/schema/document.py` declares no `pages` field on any of its five models |
| User update timestamp | `frontend/src/schema/user.ts` omits `updated_at` | `backend/app/schema/user.py:L171` declares `updated_at: datetime` as required |
| Template shape | `frontend/src/pages/Templates.tsx` declares a local `Template` interface incompatible with the Zod schema at `frontend/src/schema/template.ts:L41` | The backend declares no template contract at all, per [G1](#g1-absent-modules-referenced-by-committed-code) |
| Timestamp type | `frontend/src/schema/document.ts:L70-L71` and `:L90` use `z.date()`, which rejects a string | Every timestamp crossing the boundary arrives as a JavaScript Object Notation (JSON) string, so validation fails on well-formed server data |
| Collaborator list | `frontend/src/schema/document.ts:L72` declares `collaborators: z.array(z.string())` | No Pydantic model declares a collaborator field, and no handler returns one |
| Password storage | `backend/app/api/auth.py:L246` computes a bcrypt hash during registration | The `User` contract at `backend/app/schema/user.py:L114` declares no password field, so the response model has nowhere to carry the hash. `UserCreate` declares `password` at `:L94` |

Required fields that no code path writes compound the drift. `backend/app/schema/document.py:L113`
and `:L114` declare `created_at` and `updated_at` as required on `Document`, and no service method
sets either. `backend/app/schema/user.py:L172-L173` declare `is_active` and `is_superuser`, and no
code path reads either.

`backend/app/schema/document.py:L84` declares `DocumentUpdate` without inheriting `DocumentBase`,
so the update contract shares no field definitions with the model it updates. Both schema modules
import `List` and never use it, at `backend/app/schema/document.py:L54` and
`backend/app/schema/user.py:L68`.

See [data-model.md](data-model.md),
[../backend/app/schema/README.md](../backend/app/schema/README.md) and
[../frontend/src/schema/README.md](../frontend/src/schema/README.md).

## G7 endpoint and transport mismatch

The client calls routes the server does not expose, and the collaboration path has a different
protocol at each end.

### The client calls three routes that do not exist

| Client call | Locator | Server route | Locator |
|-------------|---------|--------------|---------|
| `POST /auth/login` | `frontend/src/services/auth.ts:L146` | `POST /token` | `backend/app/api/auth.py:L170` |
| `POST /auth/logout` | `frontend/src/services/auth.ts:L194` | none. No handler implements logout | |
| `GET /auth/me` | `frontend/src/services/auth.ts:L239` | `GET /me` | `backend/app/api/users.py:L32` |
| `GET /documents` | `frontend/src/services/api.ts:L218` | `GET /` | `backend/app/api/documents.py:L114` |
| `POST /documents` | `frontend/src/services/api.ts:L246` | `POST /` | `backend/app/api/documents.py:L56` |
| `PUT /documents/{id}` | `frontend/src/services/api.ts:L288` | `PUT /{document_id}` | `backend/app/api/documents.py:L191` |

The document prefix mismatch has a single cause. `backend/app/main.py:L125-L128` calls
`include_router` four times and passes no `prefix` argument to any of them, so every route mounts at
the application root. The client prefixes `/documents`, and the server serves `/`. The registration
also ignores `API_V1_STR`, which `backend/app/core/config.py:L112` declares and no module reads.

`frontend/src/services/auth.ts:L68` imports the bare `axios` global and uses it at `L146`, `:L194`
and `:L239`, bypassing the configured instance created at `frontend/src/services/api.ts:L162`.
Requests from the authentication module therefore carry neither the base URL nor the bearer
interceptor.

### Documents and templates collide on identical paths

The two routers declare five route shapes each, and the shapes are identical. A path parameter's
name does not participate in matching, so `/{document_id}` and `/{template_id}` compile to the same
single-segment pattern.

| Method and shape | Document handler | Template handler |
|------------------|------------------|------------------|
| `POST /` | `backend/app/api/documents.py:L56` | `backend/app/api/templates.py:L82` |
| `GET /` | `backend/app/api/documents.py:L114` | `backend/app/api/templates.py:L123` |
| `GET /{id}` | `backend/app/api/documents.py:L148` | `backend/app/api/templates.py:L156` |
| `PUT /{id}` | `backend/app/api/documents.py:L191` | `backend/app/api/templates.py:L200` |
| `DELETE /{id}` | `backend/app/api/documents.py:L240` | `backend/app/api/templates.py:L259` |

`backend/app/main.py:L126` registers the document router before `:L128` registers the template
router. FastAPI matches routes in registration order, so the document handler wins every collision
and **all five template handlers are unreachable**.

### The collaboration path has no route and two protocols

| End | Protocol | Locator |
|-----|----------|---------|
| Client | Socket.IO, with `io()` called at `frontend/src/services/collaboration.ts:L77` and no URL argument | `L13` imports `io` from `socket.io-client` |
| Server | A FastAPI `WebSocket`, per the `connect(self, websocket: WebSocket, ...)` signature | `backend/app/services/collaboration_service.py:L36` and `:L75` |

Socket.IO is a protocol layered over WebSocket rather than a WebSocket client, so the two ends could
not complete a handshake even with a route between them. No route exists: no module constructs
`CollaborationService`, and no `@app.websocket` declaration appears anywhere in the backend.
`frontend/src/services/collaboration.ts:L212` exports the client class, and no module imports it.

`setupEventListeners` at `frontend/src/services/collaboration.ts:L88-L93` has a body consisting
only of a marker and comments, so the client registers no inbound handler and would ignore every
message it received.

### Route registration and protection

Fourteen handlers exist across the four routers, and twelve sit behind the `get_current_user`
dependency. The two public handlers are `POST /token` at `backend/app/api/auth.py:L170` and
`POST /register` at `:L245`. The full route table lives in
[../backend/app/api/README.md](../backend/app/api/README.md).

Two `get_current_user` implementations exist and disagree on status codes. The routers all import
the one at `backend/app/api/auth.py:L92`, for example at
`backend/app/api/documents.py:L51`, which raises **404** at `backend/app/api/auth.py:L167` when the
user is absent. The unused implementation at `backend/app/core/security.py:L119` raises **401** for
the same condition at `:L191`. A missing user is an authentication failure rather than a missing
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
|------|-------|---------|-----------------|
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
|------------|---------|-------------------|--------|
| Continuous integration | `.github/workflows/ci.yml:L19` | the repository root, because the step sets no `working-directory` | Fails. No manifest and no lockfile |
| Container build | `infrastructure/docker/frontend.Dockerfile:L11` | `/app`, after `L8` copies `package*.json` | Fails. The glob at `L8` matches only `package.json` |

`npm install` inside `frontend/` succeeds and resolves 1,532 packages, so a developer working by
hand gets further than either automated path.

### The backend image cannot build or start

| Line | Instruction | Defect |
|------|-------------|--------|
| `infrastructure/docker/backend.Dockerfile:L8` | `COPY requirements.txt .` | The file does not exist, so the build fails here. `L11` would install from it |
| `infrastructure/docker/backend.Dockerfile:L14` | `COPY ./app /app` | Copies the package contents to the working directory root, so the modules land beside each other with no enclosing `app` package. Every `from app.core...` import in the source cannot resolve inside the image |
| `infrastructure/docker/backend.Dockerfile:L20` | `CMD ["uvicorn", "main:app", ...]` | Matches the flattened layout at `L14` and contradicts the source layout, where the application object sits at `backend/app/main.py:L24`. The command is consistent with the broken copy and inconsistent with the repository |
| `infrastructure/docker/backend.Dockerfile:L17` | `EXPOSE 8000` | Disagrees with the Compose port mapping below |

### Compose points at Dockerfiles that are not there

Both services in `infrastructure/docker/docker-compose.yml` name `dockerfile: Dockerfile` relative
to a context that contains no such file. The real Dockerfiles sit in `infrastructure/docker/` under
different names. Locators below are relative to that Compose file.

| Service | Declared context and file | Locator | Actual file |
|---------|--------------------------|---------|-------------|
| `frontend` | `../../frontend` plus `Dockerfile` | `docker-compose.yml:L6-L7` | `infrastructure/docker/frontend.Dockerfile` |
| `backend` | `../../backend` plus `Dockerfile` | `docker-compose.yml:L19-L20` | `infrastructure/docker/backend.Dockerfile` |

The backend port mapping compounds the problem.
`infrastructure/docker/docker-compose.yml:L21-L22` publishes `"5000:5000"` while the image serves
8000, per `infrastructure/docker/backend.Dockerfile:L17` and `:L20`. Compose then points the
frontend at `http://backend:5000` at `docker-compose.yml:L11`, so all three values would have to
change together.

`infrastructure/docker/docker-compose.yml` and `scripts/setup_dev_environment.sh` also provision
different databases:

| Setting | Compose | Setup script |
|---------|---------|--------------|
| Database name | `wordapp`, at `docker-compose.yml:L33` | `msword_clone`, at `scripts/setup_dev_environment.sh:L31` |
| User | `postgres`, at `docker-compose.yml:L34` | `msword_user`, at `scripts/setup_dev_environment.sh:L32` |

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

### The CD workflow deploys two absent descriptors

`.github/workflows/cd.yml:L19-L20` runs `gcloud app deploy app.yaml` and
`gcloud app deploy dispatch.yaml`. Neither file exists. `scripts/deploy.sh:L27` deploys the same
absent `app.yaml`.

The workflow carries three further defects:

- **No gate before deploy.** The job declares no `needs:` dependency, so a push to `main` deploys
  without waiting for continuous integration, which would fail anyway.
- **No rollback.** No step captures the previous version or reverts on failure.
- **Deprecated action versions.** `actions/checkout@v2` at `.github/workflows/ci.yml:L13` and
  `.github/workflows/cd.yml:L11`, `actions/setup-node@v2` at `ci.yml:L15`, and
  `google-github-actions/setup-gcloud@v0.2.0` at `cd.yml:L13`. All three run on a deprecated Node
  runtime.

The continuous integration workflow tests only the frontend. `ci.yml` declares no Python job, no
linting step and no type-check step. The pipeline would therefore report none of the 76 type errors
and none of the 12 import failures.

### The setup script targets the wrong framework

`scripts/setup_dev_environment.sh` runs Django management commands against a FastAPI project.
No `manage.py` exists anywhere in the repository.

| Line | Command | Defect |
|------|---------|--------|
| `L26` | `pip install -r requirements.txt` | No such file, per [G4](#the-backend-has-no-dependency-manifest) |
| `L40` | `cp .env.example .env` | No `.env.example` is committed, so the copy fails and every required setting stays unset |
| `L47` | `python manage.py makemigrations` | A Django command. FastAPI projects use Alembic, and no Alembic configuration exists |
| `L48` | `python manage.py migrate` | A Django command |
| `L55` | `python manage.py runserver` | A Django command, printed as the instruction for starting the backend |
| `L10` | `apt-get install -y nodejs npm python3 ...` | Pins no version, so the installed runtimes depend on the distribution rather than on the project's declared floors |

`scripts/deploy.sh` has no `set -e`, so every step runs regardless of whether the previous one
failed, and the script prints `Deployment completed successfully!` at `L47` unconditionally. `L23`
hard-codes the bucket `gs://my-word-app-bucket/`. `L15` runs `python -m pytest tests/` against a
root-level `tests/` directory that does not exist, and `L11` runs `npm run build` from the
repository root, where no manifest exists.

### Three Terraform module sources do not exist

`infrastructure/terraform/main.tf` declares three module blocks whose `source` paths point into a
directory that was never added. No `infrastructure/terraform/modules/` directory exists.

| Module | Declared at | Source |
|--------|-------------|--------|
| `word_backend` | `main.tf:L67` | `./modules/word_backend` |
| `word_frontend` | `main.tf:L76` | `./modules/word_frontend` |
| `word_database` | `main.tf:L85` | `./modules/word_database` |

`terraform init` stops with `Error: Unreadable module directory` and names `main.tf:67` in its
output.

### Terraform outputs describe a different cloud

`infrastructure/terraform/outputs.tf` declares 14 outputs, and every value reads an Amazon Web
Services (AWS) resource address. The 14 outputs name **12 distinct resource addresses across 9
resource types**, and the file references no `google_` resource at all. The only provider configured
anywhere is `google`, at `infrastructure/terraform/main.tf:L9`, so no output can resolve and none of
the addressed resources can be created.

| Resource type | Addresses referenced |
|---------------|---------------------|
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
without removing it.

### Other Terraform defects

| Defect | Locator |
|--------|---------|
| A firewall rule opens every Transmission Control Protocol (TCP) port, `0-65535`, to the whole subnet `10.0.0.0/24` | `infrastructure/terraform/main.tf:L41` and `:L44`, inside the rule declared at `:L35` |
| No `required_providers` and no `required_version` block, so provider and Terraform versions float | `infrastructure/terraform/main.tf` contains neither |
| No backend block, so state is written to the local filesystem and shared with nobody | `infrastructure/terraform/main.tf` contains none |
| 11 of the 13 declared variables are never referenced. Only `project_id` and `region` reach a resource | `infrastructure/terraform/variables.tf` declares variables at `L7`, `L14`, `L21`, `L29`, `L37`, `L44`, `L53`, `L61`, `L67`, `L73`, `L79`, `L85` and `L91` |
| `storage_class` is declared and the bucket sets no storage class | declared at `variables.tf:L37`; the bucket at `main.tf:L50` omits the argument |
| No variable declares a `validation` block, so `environment` accepts any string | `infrastructure/terraform/variables.tf` contains zero validation blocks |

### Tailwind never compiles

`frontend/package.json:L12` declares Tailwind CSS, and nothing configures it. No
`tailwind.config.js` exists, no `postcss.config.js` exists, and the repository commits no `.css`
file anywhere. Every Tailwind utility class in the components therefore resolves to no rule, and the
interface renders unstyled.

Two styling conventions coexist, and neither produces output. Tailwind utility classes appear in
`frontend/src/components/Header.tsx` and in the body of `frontend/src/pages/Templates.tsx`. Bespoke
semantic class names with no backing stylesheet appear in eight modules: `Footer.tsx`,
`Sidebar.tsx`, `Toolbar.tsx`, `DocumentCanvas.tsx`, `Home.tsx`, `Editor.tsx`, `Settings.tsx` and the
wrapper of `Templates.tsx`. That last file therefore uses both conventions at once.

### Frontend framework version mismatches

| Usage | Locator | Declared version |
|-------|---------|------------------|
| `ReactDOM.render`, the React 17 entry point | `frontend/src/index.tsx:L34` | `react` and `react-dom` at `^18.2.0`, `frontend/package.json:L8-L9`. React 18 expects `createRoot` |
| `Switch` and the `component` prop, both removed in version 6 | `frontend/src/App.tsx:L15` and `:L52-L55` | `react-router-dom` at `^6.11.1`, `frontend/package.json:L11` |
| Two nested `Provider` elements wrapping one store | `frontend/src/index.tsx:L36` and `frontend/src/App.tsx:L46` | the inner element is redundant |
| Named import of a default-only export | `frontend/src/App.tsx:L23` imports `{ store }`; `frontend/src/index.tsx:L17` imports the default correctly | `frontend/src/store/index.ts:L65` exports only a default |

Five navigation links target routes the router never declares. `frontend/src/App.tsx:L52-L55`
declares `/`, `/editor`, `/templates` and `/settings`.

| Link | Locator |
|------|---------|
| `/documents` | `frontend/src/components/Header.tsx:L69` |
| `/login` | `frontend/src/components/Header.tsx:L81` |
| `/new-document` | `frontend/src/pages/Home.tsx:L61` |
| `/open-document` | `frontend/src/pages/Home.tsx:L64` |
| `/recent-documents` | `frontend/src/pages/Home.tsx:L67` |

### Runtime versions are declared three ways and enforced nowhere

| Runtime | Declarations | Enforcement |
|---------|--------------|-------------|
| Python | 3.8 or later at `README.md:L23`; `python:3.9-slim` at `infrastructure/docker/backend.Dockerfile:L2`; unpinned `apt-get` packages at `scripts/setup_dev_environment.sh:L10` | none. No `.python-version` and no manifest |
| Node.js | 14 or later at `README.md:L22`; `node-version: '14'` at `.github/workflows/ci.yml:L17`; `node:14-alpine` at `infrastructure/docker/frontend.Dockerfile:L2` | none. `frontend/package.json` declares no `engines` field and no `.nvmrc` exists |

Both declared runtimes have passed end of life.

See [deployment-guide.md](deployment-guide.md),
[../infrastructure/terraform/README.md](../infrastructure/terraform/README.md),
[../infrastructure/docker/README.md](../infrastructure/docker/README.md),
[../.github/workflows/README.md](../.github/workflows/README.md),
[../scripts/README.md](../scripts/README.md) and
[../frontend/src/pages/README.md](../frontend/src/pages/README.md).

## Documentation inaccuracies in the root README

[The root README](../README.md) carries six statements that the committed tree contradicts. Four of
them appear in the setup instructions, so a developer following the file in order hits them before
reaching any code.

The engagement that produced this register placed the root README out of scope, so this register
records the six entries rather than correcting them in place. See
[decision-log.md](decision-log.md) for the scope entry.

| Line | Claim | Reality |
|------|-------|---------|
| `README.md:L29` | `git clone https://github.com/your-organization/microsoft-word.git` | A placeholder organisation. The command cannot succeed as written |
| `README.md:L42` | `pip install -r requirements.txt`, run from `backend/` | No `requirements.txt` exists anywhere in the repository, per [G4](#the-backend-has-no-dependency-manifest) |
| `README.md:L55` | `uvicorn main:app --reload`, run from `backend/` after `cd backend` at `L54` | The application object sits at `backend/app/main.py:L24`, one directory deeper. From `backend/`, the target is `app.main:app` |
| `README.md:L59-L66` | A project structure listing a root-level `docs/` at `L64` and a root-level `tests/` at `L65` | Neither directory exists at the repository root. The only test modules sit at `backend/tests/` |
| `README.md:L81` | Claims an MIT licence and links to a `LICENSE` file with the markup `[LICENSE](LICENSE)` | No `LICENSE` file is committed, so the link resolves to nothing. `frontend/package.json` declares no `license` field either |
| `README.md:L86-L87` | `John Doe` and `Jane Smith` as project maintainers, with `example.com` addresses | Placeholder contacts |

Two notes on the structure claim at `README.md:L59-L66`, because the two halves of it diverge once
this documentation set lands.

The `docs/` claim at `L64` becomes accidentally true. A root-level `docs/` directory now exists,
created by this engagement, so the line describes the tree correctly by coincidence rather than by
correction. Nobody edited the README to make it so.

The `tests/` claim at `L65` stays false. No root-level `tests/` directory exists, and this
engagement creates none. `scripts/deploy.sh:L15` runs `python -m pytest tests/` against that absent
path.

Prerequisites at `README.md:L22-L23` are accurate as written and worth reading beside the
[runtime version table](#runtime-versions-are-declared-three-ways-and-enforced-nowhere), which
records that neither floor is enforced anywhere.

## The complete marker and TODO register

The code's authors left 33 `HUMAN ASSISTANCE NEEDED` markers and 16 `TODO` comments. Read them as a
backlog written by the people who wrote the code, because each one names a gap its author already
knew about.

### Distribution

| Area | Markers | TODOs |
|------|---------|-------|
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
|----------|------|---------------|-------|
| `backend/app/main.py:L56` | marker | Low confidence in the startup and shutdown block below it | [G2](#the-absent-settings-singleton) |
| `backend/app/main.py:L67` | TODO | Database migration logic is unimplemented, inside the startup handler that awaits the absent `init_db` | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `backend/app/main.py:L113` | TODO | Shutdown cleanup tasks are unimplemented | none |
| `backend/app/api/users.py:L76` | marker | The code assumes a `UserService` class with an `update_user` method, and asks for verification | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `backend/app/core/security.py:L115` | marker | `get_current_user` needs review for its integration with the `User` model and `UserService`, neither of which this module imports | [G3](#g3-undefined-names-that-raise-at-execution) |
| `backend/app/services/document_service.py:L183` | marker | Asks for error handling and validation on `update_document`, the method the router calls with two arguments against three parameters | [G5](#argument-count-and-type) |
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
|----------|------|---------------|-------|
| `frontend/src/components/DocumentCanvas.tsx:L26` | marker | Component confidence below 0.8, on the component carrying the two inverse type errors | [G5](#type-inversions-in-the-editor-canvas) |
| `frontend/src/components/ImageEditor.tsx:L54` | marker | `handleInsertImage` needs review for production readiness | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `frontend/src/components/ImageEditor.tsx:L102` | marker | The component's rendered structure is unimplemented | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `frontend/src/components/TableEditor.tsx:L52` | marker | `handleInsertTable` carries a stated confidence of 0.6 | [G1](#g1-absent-modules-referenced-by-committed-code) |
| `frontend/src/components/TextEditor.tsx:L80` | marker | `handleKeyCommand` needs review for production readiness | none. This module calls both formatting helpers correctly |
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
|----------|------|---------------|-------|
| `backend/tests/test_api.py:L13` | marker | The test database connection is unconfigured. The fixture body directly below is a bare `pass` at `:L14` | [G1](#modules-referenced-only-by-the-test-suite) |
| `backend/tests/test_api.py:L77` | marker | Endpoint coverage is incomplete, with no edge cases and no error scenarios | [G1](#modules-referenced-only-by-the-test-suite) |
| `backend/tests/test_db.py:L56` | marker | Update, delete and error-handling cases are absent | [G1](#modules-referenced-only-by-the-test-suite) |

### Infrastructure, container and script markers

| Location | Kind | What it flags | Class |
|----------|------|---------------|-------|
| `infrastructure/terraform/main.tf:L94` | marker | Asks for review of the subnet range, of whether more firewall rules are needed, and of the bucket configuration. The firewall it points at opens every TCP port to the subnet | [G8](#other-terraform-defects) |
| `infrastructure/terraform/outputs.tf:L58` | marker | States that the outputs may not match the resources the configuration actually creates. Every output reads an AWS address, and the only provider is `google` | [G8](#terraform-outputs-describe-a-different-cloud) |
| `infrastructure/docker/backend.Dockerfile:L22` | marker | Asks for verification that `requirements.txt` sits in the right place and that the application code is in `./app`. Neither holds: no `requirements.txt` exists, and `:L14` flattens the package | [G8](#the-backend-image-cannot-build-or-start) |
| `scripts/deploy.sh:L37` | marker | Post-deployment checks are unimplemented, so `:L47` reports success unconditionally | [G8](#the-setup-script-targets-the-wrong-framework) |
| `scripts/setup_dev_environment.sh:L41` | marker | Environment configuration needs manual completion, immediately after `:L40` copies an `.env.example` that does not exist | [G8](#the-setup-script-targets-the-wrong-framework) |
| `scripts/setup_dev_environment.sh:L42` | TODO | The `.env` file needs production values, in a file the preceding line failed to create | [G8](#the-setup-script-targets-the-wrong-framework) |

## Where to go next

| Question | Document |
|----------|----------|
| What can I run today, and what should I fix first? | [onboarding.md](onboarding.md) |
| How do the six top-level areas fit together? | [architecture-overview.md](architecture-overview.md) |
| Which contract is authoritative for a given field? | [data-model.md](data-model.md) |
| Which external services are reachable? | [integration-guide.md](integration-guide.md) |
| Why does a deploy fail? | [deployment-guide.md](deployment-guide.md) |
| Why was something documented this way? | [decision-log.md](decision-log.md) |
| Where is the index for this documentation set? | [README.md](README.md) |

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
