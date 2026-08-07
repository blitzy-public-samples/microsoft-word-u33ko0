# backend/app/db

Two modules hold the whole persistence layer. `firestore.py` builds a Google Cloud Firestore client plus four helper functions, and `sql.py` builds a
SQLAlchemy engine, a session factory and a declarative base. Both act at import time. Every `Lnn` locator below numbers the file at the current
branch head, which includes the comment blocks this pass added.

## Purpose

`backend/app/db` holds the two low-level persistence entry points, and no abstraction unifies them. `firestore.py:L40` constructs one Firestore
client, and the four helpers at `firestore.py:L42`, `L70`, `L92` and `L110` cover create, read, update and delete work against a collection the
caller names. `sql.py:L16` opens a SQLAlchemy engine, `sql.py:L17` binds a session factory, and `sql.py:L19` declares a base class for models. Three
modules import the Firestore client name and then call it directly. The four helpers and the entire SQLAlchemy path are dead: no module imports a
helper, no class subclasses `Base`, and `get_db` at `sql.py:L21` has no consumer.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `db` | Firestore `Client` instance | `firestore.py:L40` | The single client the backend uses. Built at import time from `settings.GOOGLE_CLOUD_PROJECT`. Imported by `main.py:L21`, `services/document_service.py:L59` and `tasks/background_tasks.py:L93`. |
| `get_document` | Function, synchronous | `firestore.py:L42` | Reads one document from a named collection. Returns the stored fields at L67 and `None` at L68. No module imports it. |
| `create_document` | Function, synchronous | `firestore.py:L70` | Adds a document to a collection at L89 and returns the generated identifier at L90. No module imports it. |
| `update_document` | Function, synchronous | `firestore.py:L92` | Merges the supplied fields into an existing document at L108. Returns `None`. No module imports it. |
| `delete_document` | Function, synchronous | `firestore.py:L110` | Deletes one document at L125. Returns `None`. No module imports it. |
| `engine` | SQLAlchemy `Engine` | `sql.py:L16` | Built at import time from `settings.DATABASE_URL`. Bound to `SessionLocal` at L17 and referenced nowhere else. |
| `SessionLocal` | Session factory | `sql.py:L17` | Configured with `autocommit=False` and `autoflush=False`, so a caller must commit explicitly. Called only at `sql.py:L35`. |
| `Base` | Declarative base class | `sql.py:L19` | The parent class for Object-Relational Mapping (ORM) models. No class in the repository subclasses it. |
| `get_db` | Generator function | `sql.py:L21` | Yields one session at L37 and closes it in a `finally` block at L38-L39. No caller requests it. |

## Architecture Fit

The specification places two databases behind this folder, and the committed code delivers one.
`documentation/Technical Specifications.md, SYSTEM DESIGN > DATABASE DESIGN (L315)` describes a hybrid at L317 and restates it at L400. Google Cloud
Firestore, a non-relational store, holds flexible documents, and Google Cloud SQL, a relational store, holds structured data. The committed code
matches the Firestore half, and `services/document_service.py` and `tasks/background_tasks.py` read and write through the client at
`firestore.py:L42`. The Cloud SQL half exists as declarations only.
`documentation/Technical Specifications.md, SYSTEM DESIGN > DATABASE DESIGN > Google Cloud SQL (Relational) (L356)` diagrams five tables at
L359-L397: USERS, DOCUMENTS carrying `owner_id` at L375, TEMPLATES, DOCUMENT_PERMISSIONS at L387-L391, and TEMPLATE_PERMISSIONS. Zero of the five
have an implementing class, because nothing subclasses `Base` at `sql.py:L19`. One of those tables crossed the boundary. The specification models
DOCUMENT_PERMISSIONS as a relational table at `documentation/Technical Specifications.md:L387-L391`, while `tasks/background_tasks.py:L283` reaches
`document_permissions` as a Firestore collection. The specification also lists four Firestore collections at L330-L354, named Documents, Versions,
Comments and Users, and the code touches `documents`, `document_permissions` and `document_metadata` instead. Repository-wide layering sits in
[../../../docs/architecture-overview.md](../../../docs/architecture-overview.md).

## Dependencies

Four import statements touching this folder do not resolve. What each external service can reach sits in
[../../../docs/integration-guide.md](../../../docs/integration-guide.md), contract shapes sit in
[../../../docs/data-model.md](../../../docs/data-model.md), and the package-wide floor set for all thirteen required distributions sits in
[../README.md](../README.md).

### Internal

| Imported name | Import site | Resolves | Evidence |
| --- | --- | --- | --- |
| `settings` from `app.core.config` | `firestore.py:L36` | No | `core/config.py` declares the `Settings` class at L51 and a `get_settings` factory at L126, and creates no module-level instance. |
| `settings` from `app.core.config` | `sql.py:L14` | No | The same absent name. Importing either module raises `ImportError: cannot import name 'settings' from 'app.core.config'`. |
| `db` from `app.db.firestore` | `main.py:L21`, `services/document_service.py:L59`, `tasks/background_tasks.py:L93` | Yes | `firestore.py:L40` defines the name. Each consumer then calls the client directly rather than through a helper. |
| `init_db` from `app.db.sql` | `main.py:L22` | No | `sql.py` declares `engine`, `SessionLocal`, `Base` and `get_db`, and declares no `init_db`. `main.py:L60` awaits the absent name. |
| `get_db` from `app.database` | `backend/tests/test_api.py:L5` | No | The import names `app.database`, not `app.db.sql`, and no file exists at `backend/app/database.py`. The test module never calls the name. |

### External

| Distribution | Floor | Establishing code fact |
| --- | --- | --- |
| `google-cloud-firestore` | Unestablished | `from google.cloud.firestore import Client` at `firestore.py:L34`, constructed at `firestore.py:L40`. |
| `google-auth` | Unestablished | `from google.auth import default` at `firestore.py:L35`, called at `firestore.py:L39`. |
| `sqlalchemy` | 1.4 or newer | `declarative_base` is imported from `sqlalchemy.orm` at `sql.py:L13` and called at `sql.py:L19`. Version 1.3 exposed that name from `sqlalchemy.ext.declarative` instead. |

No dependency manifest and no lock file is committed anywhere in the repository. Each row above therefore records what the code requires, not a
supported version. "Unestablished" means nothing here pins the distribution, and it is not a statement that any release is acceptable. Only the
SQLAlchemy row carries a floor, and it comes from an import path rather than a pin. A reviewed manifest and lock, with a tested compatibility and
security matrix, is required future work and is recorded in [../../../docs/onboarding.md](../../../docs/onboarding.md). Inference choices sit in
[../../../docs/decision-log.md](../../../docs/decision-log.md).

## Configuration

Each module reads exactly one setting, and both settings are declared. [../core/README.md](../core/README.md) classifies all fifteen settings the
backend reads.

| Setting | Status | Declared at | Read at |
| --- | --- | --- | --- |
| `GOOGLE_CLOUD_PROJECT` | DECLARED | `core/config.py:L116`, typed `Optional[str]` | `firestore.py:L40`, at import time |
| `DATABASE_URL` | DECLARED | `core/config.py:L118`, typed `str` | `sql.py:L16`, at import time |

`Optional[str]` carries an implicit `None` under Pydantic 1.x, so a `Settings` instance can leave `GOOGLE_CLOUD_PROJECT` unset and `firestore.py:L40`
can then build the client with `project=None`. The inner `Config` class at `core/config.py:L121` sets `env_file` to `.env` at `core/config.py:L123`,
and the repository commits no `.env` file.

## Data Flows

Consumers bypass the helpers in this folder and hold the client instead. `services/document_service.py:L70` assigns the imported client to `self.db`,
and the Celery tasks in [../tasks/README.md](../tasks/README.md) call the same client on three collections. Nothing flows through `sql.py`.

**No edge below carries data today, and every edge below is dashed; no relationship in this module resolves.** Some of those edges are call sites that
resolve in source, and they still reach no client, because `firestore.py:L40` never constructs one once the settings import at `firestore.py:L36`
raises. The rest name a target that does not exist at all. Everything downstream of that conditional construction is unreachable as well. Every edge
carries a key, and the table under the diagram names the reason for each one.

```mermaid
graph LR
    accTitle: The live Firestore path and the dead SQLAlchemy path
    accDescr: Every edge is dashed because no relationship in this module resolves. Consumers on the left hold the Firestore client directly, the client itself is never constructed, and the SQLAlchemy declarations reach no caller. Every edge carries a key resolved in the table below the diagram.
    DSVC["document_service.py:L59<br/>self.db at L70"]
    TASKS["background_tasks.py:L93"]
    MAIN["main.py:L21<br/>imports db"]
    HELPERS["firestore.py:L42, L70,<br/>L92, L110<br/>the four helpers"]
    SQLBOOT["sql.py:L16 engine<br/>sql.py:L17 SessionLocal"]
    BASE["sql.py:L19 Base"]
    TEST["test_api.py:L5<br/>get_db from app.database"]

    CLIENT["firestore.py:L40<br/>db = Client(...)<br/>never built,<br/>L36 raises first"]
    GETDB["sql.py:L21 get_db<br/>yields at L37"]
    INITDB["init_db<br/>never defined<br/>in sql.py"]
    DEAD["no caller<br/>anywhere"]

    DOCS[("documents")]
    PERMS[("document_permissions")]
    META[("document_metadata")]

    DSVC -.->|"D1"| CLIENT
    TASKS -.->|"D2"| CLIENT
    MAIN -.->|"D3"| CLIENT
    MAIN -.->|"D4"| INITDB
    MAIN -.->|"D5"| CLIENT
    MAIN -.->|"D6"| CLIENT
    CLIENT -.->|"D7"| DOCS
    TASKS -.->|"D8"| PERMS
    TASKS -.->|"D9"| META
    SQLBOOT -.->|"D10"| GETDB
    HELPERS -.->|"D11"| DEAD
    GETDB -.->|"D12"| DEAD
    BASE -.->|"D13"| DEAD
    TEST -.->|"D14"| GETDB

%% Every edge is dashed: no request-to-database path executes as committed.
```

| Key | Edge | What the code does | Why it does not resolve |
| --- | --- | --- | --- |
| D1 | `document_service.py` to the client | `:L59` imports `db` and `:L70` assigns it to `self.db`, then `:L114`, `:L168`, `:L234` and `:L273` open a collection on it | The call sites resolve in source. The client they reach is never constructed |
| D2 | `background_tasks.py` to the client | `:L93` imports `db`, and `:L267`, `:L274` and `:L317` open the `documents` collection on it | Same. The call sites resolve and the client is absent |
| D3 | `main.py` import of the client | `main.py:L21` runs `from app.db.firestore import db` | `firestore.py:L36` imports `settings` from `app.core.config`, which never defines it, so the import raises before `db` is bound |
| D4 | `main.py` to `init_db` | `main.py:L22` imports `init_db` and `:L60` awaits it | `sql.py` defines no `init_db`, so the import fails |
| D5 | `main.py` readiness probe | `main.py:L63` calls `db.is_connected()` | `AttributeError`. The Firestore `Client` exposes no `is_connected` |
| D6 | `main.py` shutdown | `main.py:L110` runs `await db.close()` | `TypeError`. `Client` has no awaitable `close` |
| D7 | client to the `documents` collection | nothing | No client is constructed, so no traffic reaches the collection |
| D8 | `background_tasks.py` to `document_permissions` | `:L283` queries the collection and calls `.delete()` on the result | Unreachable, and `.get()` returns a list, which has no `.delete()` |
| D9 | `background_tasks.py` to `document_metadata` | `:L284` deletes one metadata document | Unreachable. The task raises earlier |
| D10 | engine to `get_db` | `sql.py:L35` calls `SessionLocal()` inside `get_db` | `sql.py:L16` builds the engine from `settings.DATABASE_URL` at import time, and that import raises first |
| D11 | the four helpers to no caller | `firestore.py:L42`, `:L70`, `:L92` and `:L110` define `get_document`, `create_document`, `update_document` and `delete_document` | No module in the repository imports any of the four |
| D12 | `get_db` to no caller | `sql.py:L21` declares the dependency and yields at `:L37` | No handler takes it as a dependency |
| D13 | `Base` to no caller | `sql.py:L19` calls `declarative_base()` | Nothing subclasses it, so the repository declares zero ORM models |
| D14 | the test suite to `get_db` | `backend/tests/test_api.py:L5` runs `from app.database import get_db` | `app.database` does not exist. The real module is `app.db.sql`, and the test never calls the fixture either |

## Design Patterns

Four patterns appear across the two modules, and one expected pattern does not. `firestore.py:L42` builds a module-level singleton, so one client
exists per process and every importer shares it. The four helpers wrap that client thinly and synchronously, each resolving a document reference at
`firestore.py:L66`, `L91`, `L109` or `L126` and then making one client call. `sql.py:L21` follows the per-request session generator pattern, closing
the session in a `finally` block at L38-L39 so the connection returns to the pool on every path including an exception. `sql.py:L19` declares an
Object-Relational Mapping base class for models that nobody wrote. No repository abstraction sits over the two persistence paths.
`services/document_service.py:L72` holds the raw Firestore client and calls `self.db.collection('documents')` inline, and a service needing the
relational path would import `sql.py` itself. Service-tier detail sits in [../services/README.md](../services/README.md).

## Known Limitations

Zero `HUMAN ASSISTANCE NEEDED` markers and zero `TODO` markers sit in this folder, and the single `#` comment at `firestore.py:L40` labels the client
construction. Every defect below comes from reading the two modules and their callers. Repository-wide defects sit in
[../../../docs/troubleshooting.md](../../../docs/troubleshooting.md). Provisioning splits three ways, and the three must not be conflated.

- **Managed provisioning: none.** `infrastructure/terraform/main.tf` declares one provider, four resources and three module blocks, and none of them
  is a Firestore database or a Cloud SQL instance. The three module sources at `main.tf:L67`, `:L76` and `:L85` point at `./modules/word_backend`,
  `./modules/word_frontend` and `./modules/word_database`. No `modules/` directory is committed, so the one block named for a database resolves to
  nothing. Nothing in the repository provisions the Firestore database that `firestore.py:L40` connects to, and nothing provisions a managed instance
  for the `DATABASE_URL` that `sql.py:L16` consumes.
- **Local provisioning: one PostgreSQL service.** `infrastructure/docker/docker-compose.yml:L30-L39` declares a `db` service on `postgres:13`, with
  database `wordapp`, user `postgres` and password `password` at `:L33-L35`, and a named `postgres_data` volume at `:L37`. That service starts on its
  own and accepts connections, so the relational path has a running server available in local development even though no managed equivalent exists.
- **Application use of that server: none.** The local PostgreSQL service is provisioned and unused. One module does import `sql.py`: `main.py:L20`
  asks it for `init_db`, a name this module never defines, so that import raises `ImportError` rather than reaching the engine. Every name `sql.py`
  actually exports is unconsumed. `engine` at `sql.py:L17` has no reader, `Base` at `sql.py:L19` is never subclassed, `get_db` at `sql.py:L21` has no
  consumer, no ORM model is declared, and no migration tool is configured. Every request-path persistence call in the committed code goes to
  Firestore through `services/document_service.py`. A reader should therefore treat the Compose database as a configured-but-dead path rather than as
  the store behind any request.

[../../../docs/deployment-guide.md](../../../docs/deployment-guide.md) holds the infrastructure evidence, and
[../../../docs/integration-guide.md](../../../docs/integration-guide.md) records what each store can reach and what blocks it.

- **Neither module imports.** `firestore.py:L36` and `sql.py:L14` both request a `settings` singleton from `app.core.config`. That module declares
  the `Settings` class at `core/config.py:L51` and a `get_settings` factory at `core/config.py:L126`, and creates no instance, so importing either
  module raises `ImportError`.
- **Import-time credential discovery serves nothing.** `firestore.py:L39` runs Application Default Credentials (ADC) discovery and binds
  `credentials` and `project`. No line in the repository reads either name, because `firestore.py:L40` takes the project from
  `settings.GOOGLE_CLOUD_PROJECT` instead. Importing the module still demands resolvable Google credentials.
- **No module imports the four helpers.** A repository-wide search for an import of `get_document`, `create_document`, `update_document` or
  `delete_document` returns nothing. Only the `db` client leaves this folder, to `main.py:L21`, `services/document_service.py:L59` and
  `tasks/background_tasks.py:L93`.
- **`get_document` contradicts its own annotation.** `firestore.py:L42` declares `-> dict`, and `firestore.py:L68` returns `None` when the snapshot
  does not exist. A caller that trusts the annotation and subscripts the result raises `TypeError` for a missing document.
- **None of the four helpers handles failure.** No transaction, no retry policy, no timeout and no `except` clause appears anywhere in
  `firestore.py:L42-L125`. A transport error or a permission error reaches the caller unchanged.
- **`create_document` binds a tuple to the name `doc_ref`.** `firestore.py:L89` assigns the result of `add(data)`, and Firestore returns that call as
  a `(timestamp, reference)` tuple. `firestore.py:L90` indexes position one to reach `.id`.
- **`get_db` returns a generator rather than a `Session`.** `sql.py:L21` annotates `-> Session`, and `sql.py:L37` yields, so a direct call produces a
  generator object. FastAPI resolves generator dependencies, and no dependency declaration names this one.
- **The SQLAlchemy path is dead.** `Base` at `sql.py:L19` has no subclass, so the repository holds zero Object-Relational Mapping models, and
  `get_db` at `sql.py:L21` has no consumer. `backend/tests/test_api.py:L5` imports a same-named symbol from the absent module `app.database` and
  never calls it. No migration tooling pairs with `Base` either, because neither `alembic.ini` nor a migration directory is tracked anywhere.
- **`sql.py` opens the engine at import time.** `sql.py:L16` calls `create_engine`, so a missing or malformed `DATABASE_URL` fails on import rather
  than at first query.
- **`main.py` expects three things from this folder, and one of them does not exist.** `main.py:L22` imports `init_db` and `main.py:L60` awaits it,
  and `sql.py` defines no such name. The other two depend on an unpinned client surface rather than on this folder: `main.py:L63` calls
  `db.is_connected()` and `main.py:L110` awaits `db.close()`, both on the client built at `firestore.py:L40`. No dependency manifest pins
  `google-cloud-firestore`, so whether either method exists, and whether `close()` returns something `await` accepts, is decided by whichever version
  resolves. `main.py:L110` sits in no `try` block, so anything raised there propagates and leaves cleanup undone.

## Usage Examples

`get_document` and `create_document` are the primary helpers, and both examples below match the signatures declared at `firestore.py:L42` and
`firestore.py:L70`. `update_document` and `delete_document` take the same two-line shape, so neither receives an example. Reading one document:

```python
from app.db.firestore import get_document

fields = get_document("documents", "abc123")

# firestore.py:L68 returns None for a missing document despite the -> dict
# annotation at :L44, so subscripting None raises TypeError. Guard the read.
title = fields["title"] if fields is not None else None
```

The call above cannot run. `firestore.py:L36` imports the absent `settings` singleton, so the import statement raises `ImportError` before any later
line executes.

Creating one document:

```python
from app.db.firestore import create_document

document_id = create_document(
    "documents",
    {"title": "Quarterly report", "content": "", "user_id": "user-42"},
)
```

The same `ImportError` blocks this call, and no code path in the repository invokes the helper. Field names for a document body sit in
[../../../docs/data-model.md](../../../docs/data-model.md) and [../schema/README.md](../schema/README.md). Reproduce either failure from `backend/`:

```bash
python -c "import app.db.firestore"   # app.db.sql fails the same way, at sql.py:L14
# ImportError: cannot import name 'settings' from 'app.core.config'
```

Setup and remediation steps sit in [../../../docs/onboarding.md](../../../docs/onboarding.md).
