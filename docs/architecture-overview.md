# Architecture Overview

The `microsoft-word-u33ko0` repository implements a browser-based word processor across six
top-level areas, and neither of its two deployable units runs. The backend cannot import, and the
observed first failure is a missing name rather than a missing router. `backend/app/main.py:L16`
imports `app.api.auth`, and `backend/app/api/auth.py:L20` then asks `app.core.config` for a
`settings` name that module never binds, so `ImportError` ends the import there. Restoring
`settings` moves the failure down the same file rather than out of it: `backend/app/api/auth.py:L22`
imports `app.services.user_service`, a module with no file.

Only once that module exists does the import reach `backend/app/main.py:L16-L19` and the four
`*_router` names that no module defines. The frontend cannot typecheck, and `npx tsc --noEmit`
reports 76 errors.

Two diagrams carry the argument of this document. The first, under
[Intended interaction](#intended-interaction), shows the system the authors designed. The second,
under [Where interaction is currently broken](#where-interaction-is-currently-broken), shows the
system they committed. Everything else here is caption.

## How to read this map

Every factual claim below carries a locator in the form `path:Lnn`, and most locators also name the
symbol sitting at that line. Read the symbol name as the durable half of the citation. Line numbers
move whenever anyone edits a file above them, and symbol names do not.

Three conventions govern the locators, matching
[troubleshooting.md](troubleshooting.md) so the two documents agree:

- Locators point at the committed state at the current branch head, which includes the inline
  documentation added to 44 source files. A locator matches what you see when you open the file
  today, not what an earlier revision held.
- Line numbers are physical. No source file in this repository ends with a newline, so `wc -l`
  reports one line fewer than each file contains.
- A range such as `L125-L128` covers every line in the span, inclusive.

Six words carry one fixed meaning throughout.

| Term | Meaning |
| ------ | --------- |
| router | A FastAPI `APIRouter` instance |
| handler | A route function carrying a `@router` decorator |
| service | A domain service class under `backend/app/services/` |
| adapter | A persistence module under `backend/app/db/` |
| slice | A Redux Toolkit slice under `frontend/src/store/` |
| marker | A `HUMAN ASSISTANCE NEEDED` comment left by the code's authors |

The three documents under `documentation/` record intended behaviour rather than committed
behaviour. Anything drawn from them carries the label **declared intent** and a citation by heading
name plus line, because all three files use unnumbered headings only. A numbered section citation
anywhere in this documentation set refers to the generated Technical Specification, a separate
document, and the text says so when it does.

Where this engagement made a judgement, [decision-log.md](decision-log.md) carries the argument. No
rationale lives in this file.

## System purpose

The system exists to let someone write, format, save and export a document in a browser.
`../README.md:L4` frames the product as a web-based version of Microsoft Word, built on React for
the client and Python FastAPI for the server, and deployed on Google Cloud Platform. That framing is
declared intent, and the committed tree holds code surfaces and scaffolds rather than working
features. Nothing in the list below works end to end today.

| Committed code surface | State as committed |
| ---------------------- | ------------------ |
| Document create, read, update and delete | Five routes and four service methods exist. Every route raises before it reaches Firestore, because the module cannot import and three call sites pass the wrong number of arguments |
| Ownership-based authorization | Three comparisons are attempted, and each reads a field name the contract does not declare. Zero checks are enforced |
| Rich-text editing on Draft.js | The editor surface and both formatting helpers exist. The toolbar calls them with one argument where two are declared, and with lowercase constants Draft.js does not accept |
| Templates | Five routes and a card gallery exist. Both the template schema and the template service are absent files |
| Export to PDF and DOCX | Both methods upload a literal placeholder string rather than a converted document, and the task tier calls a method the class never defines |
| Real-time collaboration | Designed and unconnected. No route constructs the service, and the client speaks Socket.IO while the server signature expects a FastAPI WebSocket |

[onboarding.md](onboarding.md) covers what a new developer can run today.
[troubleshooting.md](troubleshooting.md) registers every blocking defect with its evidence.

## The six top-level areas

Six directories hold the entire repository. Sixty-one files sat inside them at commit `06be74c`,
the baseline this documentation measures.

| Area | What it holds | Files | Lines | Module documentation |
| ------ | --------------- | ------- | ------- | ---------------------- |
| `frontend/` | The React and TypeScript single-page application (SPA): 26 modules under `src/`, plus `package.json`, `tsconfig.json` and `public/index.html` | 29 | 969 under `src/` | [frontend/src](../frontend/src/README.md) and its six subfolder READMEs |
| `backend/` | The FastAPI application: 15 modules under `app/`, plus 3 test modules under `tests/` | 18 | 660 under `app/`, 215 under `tests/` | [backend/app](../backend/app/README.md) and its six subpackage READMEs, plus [backend/tests](../backend/tests/README.md) |
| `infrastructure/` | 3 Terraform files declaring a virtual private cloud (VPC) network, a subnet, a firewall rule and a storage bucket, plus 3 Docker artifacts | 6 | 238 Terraform, 105 Docker | [terraform](../infrastructure/terraform/README.md), [docker](../infrastructure/docker/README.md) |
| `documentation/` | 3 specification documents recording intended behaviour | 3 | 2,316 | Described from outside, in this file, and indexed at [docs/README.md](README.md). Never edited |
| `scripts/` | 2 shell scripts: one deploy, one local environment setup | 2 | 103 | [scripts](../scripts/README.md) |
| `.github/workflows/` | 2 workflows: continuous integration and continuous delivery | 2 | 43 | [workflows](../.github/workflows/README.md) |

The six rows account for 60 files. The root `../README.md` is the 61st, and this engagement read it
as reference without editing it.

Two directories carry no README of their own. `frontend/public/` holds one file, and
[frontend/src/README.md](../frontend/src/README.md) describes it. The `infrastructure/` parent holds
nothing but the two subfolders documented above.

Line counts above are physical line counts at commit `06be74c`, counting each file's last line even
where no trailing newline closes it, which is true of all 61. A line-count utility reports one line
fewer per file.

Counts for the files that received comments now run higher. `frontend/src/` holds 1,825 lines rather
than 969, and `backend/app/` holds 1,717 rather than 660. The three Terraform files hold 281 between
them rather than 238. Docker at 105, `scripts/` at 103 and `.github/workflows/` at 43
are unchanged, because none of those files receives an inline comment. The engagement added no
executable line, so code weight did not change anywhere.

## The four tiers

The committed code separates four tiers by directory: client, HTTP application programming interface
(API), domain service, and persistence with background work. Each tier owns one entry point.

| Tier | Directory | Holds | Entry point |
| ------ | ----------- | ------- | ------------- |
| Client | `frontend/src/` | 8 components, 4 routed pages, 3 Zod schema modules, 3 client services, 2 slices behind one store, 3 utility modules | `frontend/src/` `index.tsx:L33` calls `ReactDOM.render`, and `frontend/src/` `App.tsx:L33` declares the root component |
| HTTP API | `backend/app/api/` | 4 routers and 14 handlers, 12 of them behind the `get_current_user` dependency | `backend/app/` `main.py:L24` creates `app = FastAPI()`, and `:L84-L87` mounts all four routers |
| Domain service | `backend/app/services/` | 3 service classes | `DocumentService` at `backend/app/services/` `document_service.py` `L19`, `CollaborationService` at `backend/app/services/` `collaboration_service.py` `L20`, `ExportService` at `backend/app/services/` `export_service.py` `L18` |
| Persistence and background | `backend/app/db/`, `backend/app/tasks/` | 2 adapters and 1 Celery application carrying 3 tasks | `backend/app/db/` `firestore.py:L20` builds the Firestore client, `backend/app/db/` `sql.py:L16` builds the SQLAlchemy engine, and `backend/app/tasks/` `background_tasks.py` `L22` builds the Celery application. All three are module-level statements that never execute, because each module imports the absent `settings` first, at `firestore.py:L16`, `sql.py:L14` and `background_tasks.py` `L16` |

Two backend directories sit across the tiers rather than inside one. `backend/app/schema/` holds the
Pydantic contracts that cross the client and service boundaries, and `backend/app/core/` holds the
`Settings` model at `backend/app/core/config.py:L20` plus the token and password primitives at
`backend/app/core/security.py:L27-L86`. Every backend tier reads one or both. The client tier reads
neither, because no TypeScript module can import a Python package. The client restates the same
contracts in Zod under `frontend/src/schema/`, and [data-model.md](data-model.md) records the drift
that hand-restatement produced.

The client tier runs React 18 and Redux Toolkit, declared at `frontend/package.json:L8` and `:L7`.
Draft.js supplies the editor surface in 6 modules, and Zod supplies the client contracts in 4.
`frontend/package.json:L6-L14` declares neither package. `frontend/src/App.tsx:L41-L44` declares
four routes: `/`, `/editor`, `/templates` and `/settings`.

The specification describes a comparable tiering, and the committed directories match that
placement. Its SYSTEM ARCHITECTURE heading sits at
`../documentation/Technical Specifications.md:L125`, and a HIGH-LEVEL ARCHITECTURE DIAGRAM heading
follows at `:L140`. The diagram at `:L142-L177` places a single-page application in front of an API
gateway, then seven backend boxes, then storage. Read that diagram as declared intent.

The committed code ships three of those seven boxes as service classes. No API gateway, no
machine-learning service and no file-conversion service exists anywhere in the repository. The four
tiers exist as directories and do not connect, for the reasons the next two sections give.

## Intended interaction

The intended request path runs one way through the four tiers. A browser loads the single-page
application, and the client calls the HTTP API with a bearer token. A handler resolves the caller
through a FastAPI dependency, a service performs the domain operation, and an adapter reads or
writes Firestore. Export work leaves the request path for a Celery queue. Terraform provisions the
runtime, the workflows release into it, and the shell scripts stand up a local equivalent.

The diagram below shows ownership, the four backing services the server tiers fan out to, and the
specification boundary.

```mermaid
graph TD
    accTitle: The four tiers, the backing services they fan out to, and the specification boundary
    accDescr: A browser reaches the client tier, the client calls the HTTP API, a handler calls a service, a service calls an adapter or queues work, and the adapters and tasks reach four backing services. Terraform and Docker provision the runtime, the workflows release into it, and the shell scripts stand up a local equivalent. Every edge is intent rather than verified behaviour.
    BROWSER["Browser"]

    subgraph FE["frontend/ client tier"]
        PAGES["src/pages<br/>4 routed pages"]
        STORE["src/store<br/>2 slices,<br/>1 store"]
        CLIENT["src/services<br/>axios client"]
    end

    subgraph BE["backend/ server tiers"]
        MAIN["app/main.py<br/>composition root"]
        ROUTERS["app/api<br/>4 routers,<br/>14 handlers"]
        SERVICES["app/services<br/>3 services"]
        ADAPTERS["app/db<br/>2 adapters"]
        TASKS["app/tasks<br/>3 Celery<br/>tasks"]
    end

    FS[("Google Cloud<br/>Firestore")]
    GCS[("Cloud<br/>Storage")]
    PUBSUB["Google Cloud<br/>Pub/Sub"]
    BROKER[("Redis<br/>broker")]

    INFRA["infrastructure/<br/>Terraform,<br/>Docker"]
    PIPE[".github/<br/>workflows/<br/>CI and CD"]
    SH["scripts/<br/>deploy and<br/>local setup"]
    SPEC["documentation/<br/>declared intent,<br/>outside the<br/>runtime path"]

    BROWSER --> PAGES
    PAGES --> STORE
    PAGES --> CLIENT
    CLIENT --> BE
    MAIN --> ROUTERS
    ROUTERS --> SERVICES
    SERVICES --> ADAPTERS
    SERVICES --> TASKS
    ADAPTERS --> FS
    SERVICES --> GCS
    SERVICES --> PUBSUB
    TASKS --> BROKER
    TASKS --> FS
    TASKS --> GCS
    INFRA --> GCS
    PIPE --> INFRA
    SH --> BE
    INFRA --> FE
    INFRA --> BE

%% Solid edges only. Every edge here is intent, not verified behaviour.
```

## Where interaction is currently broken

The map above breaks in twelve places, and the first three stop the backend from importing at all.
The table below names each break, its evidence, its consequence, and the defect class
[troubleshooting.md](troubleshooting.md) files it under.

| Broken edge | Evidence | Consequence | Class |
| ------------- | ---------- | ------------- | ------- |
| Composition root to settings, the first failure | `backend/app/` `main.py:L20` imports `settings` from `app.core.config`, which defines the `Settings` class at `backend/app/core/` `config.py:L20` and `get_settings()` at `:L63`, and never creates a module-level instance | Eight modules import `settings` directly, and nine module-import failures trace back to the one absent name, because `app.main` fails both on its own import at `:L20` and earlier through `app.api.auth`. `ImportError` ends the import of every one | G2 |
| Composition root to the four routers, latent behind the row above | `backend/app/` `main.py:L16-L19` imports `auth_router`, `documents_router`, `users_router` and `templates_router`. All four modules export the bare name `router`, at `backend/app/api/` `auth.py:L26`, `backend/app/api/` `documents.py:L22`, `backend/app/api/` `users.py:L17` and `backend/app/api/` `templates.py:L22` | No router symbol resolves. A run never reports this, because executing `app.api.auth` at `main.py:L16` raises on the missing `settings` first, and then on the absent `app.services.user_service` module its `:L21` requests. These four names are the third failure, not the second | G2 |
| Composition root to the SQL adapter | `backend/app/` `main.py:L22` imports `init_db` from `app.db.sql`, which defines `engine`, `SessionLocal`, `Base` and `get_db` and defines no `init_db`. The startup handler awaits the absent name at `:L42` | `ImportError` ends the import of `app.main` at `:L22`, before the startup handler can run | G1 |
| Lifecycle handlers to the Firestore client | `backend/app/` `main.py:L45` calls `db.is_connected()`, which belongs to no release of the Google Cloud Firestore `Client`. `:L69` awaits `db.close()` on the object imported at `:L21`, and nothing pins `google-cloud-firestore`, so no committed file settles which `close` surface the resolved release provides | `:L50-L51` catches the startup `AttributeError` and prints it, so the application would start believing Firestore is reachable. At shutdown a synchronous `close()` returns `None`, and `await None` raises `TypeError`; a release exposing no `close` raises `AttributeError` instead. Whether anything inside the client shuts down first is unestablished here. `:L69` sits in no `try` block, so the cleanup `:L72` records as outstanding is skipped | G5 |
| Every backend module to the `app` package | No `__init__.py` file exists anywhere under `backend/`, so `app` and its six subpackages are implicit namespace packages. `infrastructure/docker/` `backend.Dockerfile` `L14` copies `./app` to `/app`, and `:L20` runs `uvicorn main:app` | The `app.` prefix used by every internal import cannot resolve inside the image as built. [backend/app/README.md](../backend/app/README.md) owns this statement | G1 |
| Router mounting to resource prefixes | `backend/app/` `main.py:L84-L87` mounts all four routers with no prefix argument, documents at `:L85` ahead of users at `:L86` and templates at `:L87` | Seven protected handlers become unreachable, not five. The five template routes collide with the five document routes on `/` and `/{id}`. `GET /me` at `backend/app/api/` `users.py:L19` plus `PUT /me` at `:L32` are claimed by `GET /{document_id}` at `backend/app/api/` `documents.py:L68` and `PUT /{document_id}` at `:L98`, because a single-segment path template matches the literal `me` | G7 |
| Root component to the store | `frontend/src/` `App.tsx:L20` imports `{ store }` as a named symbol, and `frontend/src/store/` `index.ts:L36` exports the store as a default only | The named import resolves to nothing, and the compiler reports it | G2 |
| Root component to the router library | `frontend/src/` `App.tsx:L12` imports `Switch` and `:L41-L44` passes the `component` prop. `frontend/` `package.json:L11` pins `react-router-dom` at `^6.11.1`, which removed both | Routing cannot compile against the declared dependency version | G8 |
| Provider and shell duplication | `frontend/src/` `index.tsx:L35` wraps the application in a react-redux `Provider`, and `frontend/src/` `App.tsx:L35` wraps the same store again. `frontend/src/` `App.tsx:L38` and `:L47` render `Header` and `Footer` around every route, and the pages render their own as well | The inner `Provider` is redundant. `Header` renders twice on all four routed pages (`Home.tsx:L32`, `Editor.tsx:L107`, `Settings.tsx:L61`, `Templates.tsx:L87`). `Footer` renders twice on three of them (`Home.tsx:L48`, `Settings.tsx:L88`, `Templates.tsx:L108`), because `Editor.tsx` renders no footer of its own | G8 |
| Every frontend module to its own import prefix | Nearly every module imports through a `@/` prefix. `frontend/` `tsconfig.json` `L10-L16` declares five path aliases, and none of them is `@/` | 44 of the 76 type errors come from this one unmapped prefix | G4 |
| Terraform root to its three modules | `infrastructure/terraform/` `main.tf:L67-L92` composes `./modules/word_backend`, `./modules/word_frontend` and `./modules/word_database`, with sources at `:L68`, `:L77` and `:L86`. No `modules/` directory exists | `terraform init` reports `Unreadable module directory` and stops | G8 |
| Delivery pipeline to its deployment descriptors | `.github/workflows/` `cd.yml:L19-L20` runs `gcloud app deploy app.yaml` and `gcloud app deploy dispatch.yaml`. Neither file is committed | The deploy step fails on its first command | G8 |

Two headline consequences follow, and both come from running the code rather than reading it.
Importing `app.main` fails through `backend/app/main.py:L16`, then
`backend/app/api/auth.py:L20`, raising
`ImportError: cannot import name 'settings' from 'app.core.config'`. Only 3 of the 15 modules under
`backend/app/` import successfully, and
[backend/app/README.md](../backend/app/README.md) owns that census. On the client,
`npx tsc --noEmit` reports 76 errors, and
[frontend/src/README.md](../frontend/src/README.md) owns the error profile.

The code's authors flagged much of the above themselves. Twenty-seven `HUMAN ASSISTANCE NEEDED`
markers and 15 `TODO` comments sit across the 44 source files, and
[troubleshooting.md](troubleshooting.md) registers every one.

The overlay below redraws the same skeleton with each unresolvable link dashed and labelled. Read
the dashed edges as the shape of the failure. Seven of them leave the composition root, and one of
those seven, the `settings` import at `backend/app/main.py:L20`, accounts for nine of the twelve
backend module import failures on its own.

```mermaid
graph LR
    accTitle: The broken-edge overlay, every unresolvable link dashed and labelled
    accDescr: The same skeleton redrawn so that each link which cannot resolve is dashed and labelled. Seven dashed edges leave the composition root. One solid edge marks the single import form that matches its target.
    INDEX["frontend/src/index.tsx<br/>renders and provides the store"]
    APP["frontend/src/App.tsx<br/>root component"]
    STORE2["frontend/src/store/index.ts<br/>default export only"]
    ALIAS["frontend/src: 44 @/ imports<br/>across 13 of 26 modules"]

    MAIN2["backend/app/main.py<br/>composition root"]
    AUTHR["backend/app/api/auth.py<br/>exports 'router'"]
    DOCR["backend/app/api/documents.py<br/>exports 'router'"]
    USERR["backend/app/api/users.py<br/>exports 'router'"]
    TMPLR["backend/app/api/templates.py<br/>exports 'router'"]
    CFG["backend/app/core/config.py<br/>defines Settings,<br/>creates no instance"]
    SQLA["backend/app/db/sql.py<br/>defines no init_db"]
    FSA["backend/app/db/firestore.py<br/>exports 'db'"]

    TSC["tsconfig.json<br/>5 aliases, none is @/"]
    RRD["react-router-dom ^6.11.1<br/>no Switch,<br/>no component prop"]
    TERRA["terraform/main.tf<br/>3 module blocks"]
    TFMOD["terraform/modules/<br/>directory absent"]
    CD["workflows/cd.yml<br/>deploy step"]
    DESC["app.yaml, dispatch.yaml<br/>not committed"]

    INDEX -->|"default import matches the default export, index.tsx:L14"| STORE2

    MAIN2 -.->|"imports auth_router, main.py:L16"| AUTHR
    MAIN2 -.->|"imports documents_router, main.py:L17"| DOCR
    MAIN2 -.->|"imports users_router, main.py:L18"| USERR
    MAIN2 -.->|"imports templates_router, main.py:L19"| TMPLR
    MAIN2 -.->|"imports settings, main.py:L20"| CFG
    MAIN2 -.->|"imports init_db, main.py:L22"| SQLA
    MAIN2 -.->|"calls is_connected at main.py:L45, close at :L69"| FSA
    APP -.->|"named import of a default-only export, App.tsx:L20"| STORE2
    APP -.->|"imports Switch at App.tsx:L12, passes component at :L41-L44"| RRD
    ALIAS -.->|"no matching path alias, tsconfig.json:L10-L16"| TSC
    TERRA -.->|"source ./modules/word_*, main.tf:L68, :L77, :L86"| TFMOD
    CD -.->|"deploys 2 absent<br/>descriptors,<br/>cd.yml:L19-L20"| DESC

%% Dashed edges cannot resolve. The solid edge marks the one import form that matches
%% its target, and contrasts with the dashed edge reaching that same target from App.tsx.
%% Each node label carries its own directory, so the frontend and backend halves stay legible
%% without a cluster box around them.
```

## System boundaries

Five boundaries carry data out of one process or trust domain and into another. The repository
commits no cross-language contract artifact, so anyone changing a shape on one side of a boundary
keeps the other side in agreement by hand.

Read the Current state column against one distinction. A file containing a call is not a request
path that can execute it. This document uses three labels and nothing softer. A **declared call**
means the source contains the call, and no request or process path reaches it as committed.
**Reachable after prerequisite** means the path is otherwise complete and one named prerequisite
must be satisfied first, and the prerequisite is named every time.

**Reachable as committed** means a request or process executes the call today with no repair. No
backend boundary below is reachable as committed, because importing `app.main` fails at
`backend/app/api/auth.py:L20`, so no handler is ever served.

| Boundary | What crosses it | Contract artifact | Current state |
| ---------- | ----------------- | ------------------- | --------------- |
| Browser to HTTP API | JSON request and response bodies, plus a JSON Web Token (JWT) presented as a bearer token. `backend/app/api/` `auth.py:L28` declares the `get_current_user` dependency that reads it | None shared. The repository commits no OpenAPI document and generates no client | The client and the server disagree on route paths and on the token field name. [troubleshooting.md](troubleshooting.md) records both, under G6 and G7 |
| HTTP API to domain service | Python calls carrying Pydantic models and identifier strings | The Pydantic contracts under `backend/app/schema/`, described in [data-model.md](data-model.md) | Seven call sites disagree with the signature they target, so the ownership comparison at `backend/app/services/` `document_service.py` `L108` never receives the argument it compares |
| Domain service to Google Cloud Firestore | Document reads and writes through the `google-cloud-firestore` client library | The collection and field names each caller passes. No schema constrains a stored Firestore document | Declared in the code path only, and no request crosses this boundary today. Nothing contacts the credential chain either. `backend/app/db/` `firestore.py:L16` asks `app.core.config` for the same absent `settings` name, so the module raises `ImportError` before `:L18` resolves Application Default Credentials (ADC) and before `:L20` builds the client. Once `settings` exists, both lines run at import time and importing the adapter alone contacts the credential chain. Importing the application stops earlier still, at `backend/app/api/` `auth.py:L20` |
| Domain service to Google Cloud Storage and Cloud Pub/Sub | Export objects and version 4 signed URLs, plus per-document change messages | Object key layouts and message payload shapes, both chosen at the call site | `backend/app/services/` `export_service.py` `L60-L70` uploads an object and signs a version 4 URL. `backend/app/services/` `collaboration_service.py` `L38` builds a publisher and `:L156` publishes, and no route ever constructs that service. [integration-guide.md](integration-guide.md) labels each integration reachable or scaffolded |
| Application to Celery and Redis | Task messages for export, retention and statistics work | The task signatures at `backend/app/tasks/` `background_tasks.py` `L25`, `:L73` and `:L116` | `backend/app/core/` `config.py:L48` declares `REDIS_URL`, and `backend/app/tasks/` `background_tasks.py` `L22` reads it. Nothing provisions Redis, and no worker or beat process is declared anywhere in the repository. [deployment-guide.md](deployment-guide.md) carries the detail |

## Architectural assumptions

Seven assumptions hold the design together, and the code states none of them. Committed files
contradict all seven.

| Assumption | Why it must hold | Where it is contradicted |
| ------------ | ------------------ | -------------------------- |
| An `app` package sits on the import path | Twelve modules import by absolute package path, for example `from app.core.config import settings` at `backend/app/` `main.py:L20` | No `__init__.py` file exists anywhere under `backend/`, so all seven namespaces are implicit. `infrastructure/docker/` `backend.Dockerfile` `L14` copies `./app` to `/app` and `:L20` runs `uvicorn main:app`, which flattens the package and leaves the `app.` prefix unresolvable. [backend/app/README.md](../backend/app/README.md) owns this fact |
| A `settings` singleton is importable from `app.core.config` | Eight modules read configuration through that name, including the CORS middleware at `backend/app/` `main.py:L77` | `backend/app/core/` `config.py:L20-L76` defines the `Settings` class and the `get_settings()` factory, and creates no module-level instance |
| Routers mount under resource prefixes | The client prefixes its calls with `/documents`, and documents and templates each declare five identical route paths | `backend/app/` `main.py:L84-L87` mounts all four routers with no prefix, so the two resources collide on `/` and `/{id}`. The two profile routes at `backend/app/api/` `users.py:L19` and `:L32` are shadowed by the single-segment document routes |
| Ownership travels on one field name | The document handlers compare a stored owner against the caller at `backend/app/api/` `documents.py:L94`, `:L126` and `:L154`, and the service repeats the comparison at `backend/app/services/` `document_service.py` `L108`, `:L148` and `:L184` | Four positions carry the field under two different names, and one of them is optional with a default. [data-model.md](data-model.md) names all four and names none canonical |
| The `@/` alias resolves to `src/` | 44 executable imports across 13 of the 26 modules under `frontend/src/` use that prefix, and `frontend/src/App.tsx` alone carries seven of them | `frontend/` `tsconfig.json` `L10-L16` declares five aliases, and none of them is `@/`. `react-scripts` 5 would not apply those mappings to bundler resolution in any case |
| Tailwind CSS compiles the utility classes in the markup | Two modules carry Tailwind class strings: `frontend/src/components/` `Header.tsx:L33-L44` across twelve `className` attributes, and `frontend/src/pages/` `Templates.tsx` `L86-L103` across seven | No `tailwind.config.js`, no `postcss.config.js` and no stylesheet is committed anywhere, so no authored rule backs those class strings, and once the build blockers are cleared no authored styling would apply |
| A Redis broker backs Celery | `backend/app/tasks/` `background_tasks.py` `L22` constructs `Celery('microsoft_word', broker=settings.REDIS_URL)` | `infrastructure/docker/` `docker-compose.yml` `L3-L39` declares three services, `frontend`, `backend` and `db`, and no Redis service. `infrastructure/terraform/` `main.tf` declares no cache resource. Searching all of `infrastructure/` for `redis` or `memorystore` returns nothing |

## Module documentation

All 19 module READMEs exist and describe the directories mapped above, 19 of 19 with none outstanding.
Each one carries the same nine H2 headings in the same order, opening with Purpose and closing with
Usage Examples, with Known Limitations second from last. Each links back to this file from its
Architecture Fit heading and across to [the troubleshooting register](troubleshooting.md) from its
Known Limitations heading.

Backend:

- [backend/app](../backend/app/README.md), the composition root
- [backend/app/api](../backend/app/api/README.md), four routers and 14 handlers
- [backend/app/core](../backend/app/core/README.md), settings and security primitives
- [backend/app/db](../backend/app/db/README.md), the Firestore and SQLAlchemy adapters
- [backend/app/schema](../backend/app/schema/README.md), the Pydantic contracts
- [backend/app/services](../backend/app/services/README.md), three domain services
- [backend/app/tasks](../backend/app/tasks/README.md), the Celery task tier
- [backend/tests](../backend/tests/README.md), the current state of the test suite

Frontend:

- [frontend/src](../frontend/src/README.md), bootstrap, providers and routing
- [frontend/src/components](../frontend/src/components/README.md), eight components
- [frontend/src/pages](../frontend/src/pages/README.md), four routed pages
- [frontend/src/schema](../frontend/src/schema/README.md), the Zod contracts
- [frontend/src/services](../frontend/src/services/README.md), three client services
- [frontend/src/store](../frontend/src/store/README.md), store composition and two slices
- [frontend/src/utils](../frontend/src/utils/README.md), formatting, validation and serialization

Infrastructure and automation:

- [infrastructure/terraform](../infrastructure/terraform/README.md), 35 blocks across three files
- [infrastructure/docker](../infrastructure/docker/README.md), two Dockerfiles and Compose
- [.github/workflows](../.github/workflows/README.md), the CI and CD pipelines
- [scripts](../scripts/README.md), the deploy and setup scripts

Eight repository-level documents sit beside this one: the index at [docs/README.md](README.md), plus
[onboarding.md](onboarding.md), [data-model.md](data-model.md),
[integration-guide.md](integration-guide.md), [deployment-guide.md](deployment-guide.md),
[troubleshooting.md](troubleshooting.md), [decision-log.md](decision-log.md) and
[prose-validation.md](prose-validation.md). The
[root README](../README.md) and `../documentation/Technical Specifications.md` stay as reference,
unedited by this engagement.
