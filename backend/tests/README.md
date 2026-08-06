# backend/tests

## Purpose

`backend/tests` holds the backend test suite: three modules, 21 tests, and no passing run. Eight tests run under pytest in
`test_api.py`, which exercises the Hypertext Transfer Protocol (HTTP) surface through a FastAPI test client. The other 13 run
under the standard-library `unittest` framework in `test_db.py` and `test_services.py`, which exercise persistence helpers
and domain services. All three modules target an application programming interface (API) the committed application does not
expose, so each fails at import before its first assertion runs.

The three modules carry no docstrings and no inline comments, and that state is deliberate. Documentation for this directory
lives in this file, and future passes must leave `test_api.py`, `test_db.py` and `test_services.py` byte-for-byte unchanged.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `test_api.py` | Test module, 77 lines | `backend/tests/test_api.py` | pytest tests over the HTTP surface, using `fastapi.testclient.TestClient` |
| `test_db.py` | Test module, 58 lines | `backend/tests/test_db.py` | `unittest` tests over two persistence helper classes the repository never defines |
| `test_services.py` | Test module, 80 lines | `backend/tests/test_services.py` | `unittest` tests over the three domain services |
| `client` | Module-level test client | `test_api.py:L8` | `TestClient(app)` built at import time and shared by all eight pytest tests |
| `db` | pytest fixture, module scope | `test_api.py:L10-L14` | Declares a test database session. The body is two comment lines plus `pass` at `L14`, so the fixture yields `None` |
| `test_user` | pytest fixture, module scope | `test_api.py:L16-L22` | Builds a `User`, calls `set_password` at `L19`, then `db.add` at `L20` and `db.commit` at `L21` |
| `test_login`, `test_login_invalid_credentials` | pytest tests | `test_api.py:L25`, `:L30` | Post credentials to `/auth/login`, asserting 200 with an `access_token`, then 401 |
| `test_create_document`, `test_get_document` | pytest tests | `test_api.py:L35`, `:L40` | Create through `POST /documents/` asserting 201, then read through `GET /documents/{id}` |
| `test_create_user`, `test_get_user`, `test_create_template`, `test_get_template` | pytest tests | `test_api.py:L51`, `:L56`, `:L62`, `:L67` | Create through `POST /users/` and `POST /templates/` asserting 201, then read each back by identifier |
| `TestDatabaseOperations` | `unittest.TestCase` | `test_db.py:L9` | `setUp` at `L11` starts two patches, `tearDown` at `L17` releases them at `L18`. Four tests at `L20`, `L30`, `L39` and `L47` add and read a Firestore document, then add and read a relational record |
| `TestDocumentService` | `unittest.TestCase` | `test_services.py:L9`, `setUp` at `:L10` | Four tests at `:L13`, `:L20`, `:L26` and `:L32` create, read, update and delete a document |
| `TestCollaborationService` | `unittest.TestCase` | `test_services.py:L37`, `setUp` at `:L38` | Three tests at `:L41`, `:L47` and `:L53` add, remove and list collaborators |
| `TestExportService` | `unittest.TestCase` | `test_services.py:L59`, `setUp` at `:L60` | Two tests at `:L64` and `:L72` patch a generator function, then assert the returned bytes |
| `__main__` guard | Entry point | `test_services.py:L79-L80` | Calls `unittest.main()`, which pytest ignores during collection |

## Architecture Fit

The suite sits outside the application layers and reaches into three of them. `test_api.py` drives the router tier through
its test client, `test_services.py` drives the service tier directly, and `test_db.py` drives a persistence tier the
committed tree does not contain. No test touches the configuration tier or the Celery task tier. For the layer map these
tiers belong to, see [the architecture overview](../../docs/architecture-overview.md).

The suite tracks the specification's route shape rather than the code's, and that one fact explains most of its route
failures. `documentation/Technical Specifications.md` declares four prefixed endpoint groups under
`SYSTEM DESIGN > API DESIGN` at L406-L432: `/auth`, `/documents`, `/users` and `/templates`. `test_api.py` asserts that same
prefixed grouping at L26, L36, L46, L52, L57, L63 and L73, and five of those seven paths match a declared endpoint character
for character. The committed routers mount with no prefix at `backend/app/main.py:L125-L128`, so the server answers on `/`,
`/{id}`, `/token`, `/register` and `/me`.

Intended behavior per `documentation/Technical Specifications.md`, `SYSTEM DESIGN > API DESIGN`: each resource group answers
under its own prefix. The committed code registers no prefix, and this pass changes neither side.

The specification also names one backend testing framework where this directory uses two. Its `TECHNOLOGY STACK > Backend`
list names Pytest alone, at L553, while `test_db.py:L9` and `test_services.py:L9` build on `unittest.TestCase`. The
specification mentions testing at three lines only, L546, L553 and L729, and carries no test-strategy section.

## Dependencies

Nine of the ten modules these imports target do not exist, so every internal row carries its resolution status. The suite
asserts against the document and user contracts, described in [the data model reference](../../docs/data-model.md), and
mocks Firestore and SQLAlchemy, covered in [the integration guide](../../docs/integration-guide.md).

### Internal

| Import | Site | Resolves? |
| --- | --- | --- |
| `app.main.app` | `test_api.py:L3` | Yes as a module. Importing it raises through the application chain, traced under Data Flows |
| `app.models` for `User`, `Document`, `Template` | `test_api.py:L4` | No. Neither `backend/app/models.py` nor `backend/app/models/` exists |
| `app.database` for `get_db` | `test_api.py:L5` | No. Neither `backend/app/database.py` nor `backend/app/database/` exists, and the name is never used |
| `backend.db.firestore_operations` for `FirestoreOperations` | `test_db.py:L6` | No. `backend/db/` does not exist, and no `FirestoreOperations` class exists anywhere |
| `backend.db.sql_operations` for `SQLOperations` | `test_db.py:L7` | No. Same absent package, and no `SQLOperations` class exists anywhere |
| `services.document_service`, `services.collaboration_service`, `services.export_service` | `test_services.py:L3-L5` | No. The real modules live under `app.services.*` |
| `models.document`, `models.user` | `test_services.py:L6-L7` | No. No `models` package exists at any import root |

### External

| Package | Imported name | Site |
| --- | --- | --- |
| `pytest` | `pytest` | `test_api.py:L1` |
| `fastapi` | `fastapi.testclient.TestClient` | `test_api.py:L2` |
| `sqlalchemy` | `sqlalchemy.orm.Session`, then `create_engine` and `sqlalchemy.orm.sessionmaker` | `test_api.py:L6`, `test_db.py:L4-L5` |
| `google-cloud-firestore` | `google.cloud.firestore` | `test_db.py:L3` |
| Standard library | `unittest`, `unittest.mock` | `test_db.py:L1-L2`, `test_services.py:L1-L2` |

No manifest declares any of these packages, because the repository contains no Python manifest. `requirements.txt`,
`pyproject.toml`, `setup.py`, `setup.cfg`, `tox.ini`, `Pipfile` and `.python-version` are all absent, so no version floor
exists to quote.

## Configuration

Nothing in this directory is configured, so the table records the verified negatives, because an absent input still governs how the suite behaves.

| Configuration input | Read by this suite | Status |
| --- | --- | --- |
| `Settings` fields from `backend/app/core/config.py:L51` | No. No module here imports `app.core.config` | DECLARED, unread by this suite |
| Environment variables | No. Neither `os.environ` nor `os.getenv` appears in any of the three modules | Neither declared nor read |
| pytest configuration | No. `pytest.ini`, `conftest.py`, `tox.ini` and every `[tool.pytest]` host are absent | READ-BUT-NEVER-DECLARED |
| Package roots through `__init__.py` | No. Zero `__init__.py` files exist under `backend/`, so `app`, `backend` and `backend.tests` are namespace paths rather than packages | READ-BUT-NEVER-DECLARED |
| Interpreter `sys.path` and working directory | Yes, implicitly. Every import in all three modules resolves against them | READ-BUT-NEVER-DECLARED |

The last row carries the whole configuration surface, and no single working directory satisfies all three import roots at
once. For prerequisites and setup steps, see [the onboarding guide](../../docs/onboarding.md), which this file does not
restate.

## Data Flows

`test_api.py:L8` builds one module-level client over the real application imported at `L3`, so importing the module runs the
whole application import chain before pytest collects a single test. That chain enters `backend/app/main.py:L16`, which
imports `auth_router` from `app.api.auth`, and stops at `backend/app/api/auth.py:L84`, which imports `settings` from
`app.core.config`. That configuration module binds only `Settings` at `L51` and `get_settings` at `L126`, so the name
`settings` does not exist and the import raises. A second import-time cost sits at `backend/app/db/firestore.py:L42`, which
constructs a Firestore client and so triggers Google Cloud credential discovery.

The two `unittest` modules never reach the application. `test_db.py` replaces `google.cloud.firestore.Client` and
`sqlalchemy.create_engine` with mocks at `L12-L13`, so its data flow stays synthetic and touches no real service.
`test_services.py` constructs real service objects in `setUp` at `L11`, `L39` and `L61`, and each constructor would open a
live Google Cloud client. Neither module gets that far, because both fail on absent imports first.

## Design Patterns

The suite applies eight patterns, and naming them makes the defect inventory below easier to place.

- **Module-scoped fixtures with no teardown.** Both declare `scope="module"` and neither yields nor releases anything
  (`test_api.py:L10`, `:L16`).
- **One shared client rather than one per test.** `test_api.py:L8` builds it at import, and all eight pytest tests reuse that
  instance.
- **`unittest.TestCase` with per-test construction.** Each `setUp` rebuilds its subject (`test_db.py:L11`,
  `test_services.py:L10`, `:L38`, `:L60`).
- **Manual patch lifecycle.** `test_db.py` starts patches in `setUp` at `L12-L13` and releases them through
  `patch.stopall()` at `L18`, while `test_services.py` uses the decorator form at `L63` and `L71`.
- **Chained attribute access to configure mocks** (`test_db.py:L15`, `:L22-L23`, `:L32-L33`, `:L49`).
- **A `__main__` guard.** `test_services.py:L79-L80` calls `unittest.main()`, which pytest ignores.
- **Synchronous tests only.** No `async` test exists here, though 12 of the 14 route handlers under `backend/app/api/` are
  declared `async def`.
- **Happy-path coverage.** `test_login_invalid_credentials` (`test_api.py:L30`) is the only negative case among the 21 tests.

Two frameworks coexist here with no shared configuration, so pytest and `unittest` collect these modules differently.

## Known Limitations

No test in this directory currently runs. `test_api.py` fails at import through the application chain, `test_db.py` on both of
its persistence imports, and `test_services.py` on all five of its own imports. The three modules also receive no docstrings
and no inline comments, by standing instruction, so this README carries every defect below rather than the source files.

**Three mutually incompatible import roots.**

| Module | Import root | Sites | Resolves? |
| --- | --- | --- | --- |
| `test_api.py` | `app.*` | `L3` `from app.main import app`, `L4` `from app.models import ...`, `L5` `from app.database import get_db` | `app.main` exists; `app.models` and `app.database` do not |
| `test_db.py` | `backend.db.*` | `L6`, `L7` | Neither module exists, and `backend` is not an importable package |
| `test_services.py` | bare `services.*` and `models.*` | `L3-L5`, `L6-L7` | The real service modules live at `app.services.*`; `models.*` exists at no root |

No single `sys.path` entry or working directory satisfies all three roots at once, so pytest cannot collect the three files
in one run however a reader invokes it. Zero `__init__.py` files exist under `backend/`, so none of the three roots is a real
package.

- **Six modules that exist nowhere in the repository**: `app.models` and `app.database` (`test_api.py:L4-L5`),
  `backend.db.firestore_operations` and `backend.db.sql_operations` (`test_db.py:L6-L7`), and `models.document` with
  `models.user` (`test_services.py:L6-L7`). No `FirestoreOperations` or `SQLOperations` class exists either. The three
  `services.*` imports differ: those modules do exist, at `app.services.*`.
- **A fixture body that is a bare `pass`.** The `db` fixture at `test_api.py:L10-L14` holds two comment lines plus `pass` at
  `L14`, so it yields `None`. `test_user` at `L17` accepts that value as `db: Session`, then calls `db.add(user)` at `L20`
  and `db.commit()` at `L21` against `None`. Four further tests take the same fixture, at `L35`, `L40`, `L62` and `L67`.
- **Methods that no contract declares.** `user.set_password("testpassword")` at `test_api.py:L19`, and
  `test_user.get_token()` at `:L36`, `:L46`, `:L57`, `:L63` and `:L73`. The real `User` is a Pydantic model at
  `backend/app/schema/user.py:L114` and declares neither method.
- **Five required fields omitted.** `User(id=1, username="testuser")` at `test_services.py:L14` supplies two of the seven
  required fields, and the five omissions raise the validation error. `backend/app/schema/user.py` requires `id` (`L169`),
  `created_at` (`L170`), `updated_at` (`L171`), `is_active` (`L172`) and `is_superuser` (`L173`), plus inherited `email`
  (`L80`) and `username` (`L81`). The integer `id` is a separate mismatch against the declared `str` hint, which Pydantic
  1.x coerces rather than rejects.
- **A field that no contract declares.** `document.owner` at `test_services.py:L18`. The `Document` contract declares
  `owner_id` at `backend/app/schema/document.py:L68` and no `owner`, while `DocumentService` writes `user_id` at
  `backend/app/services/document_service.py:L118`. The assertions on `document.title` (`L17`), `document.id` (`L24`) and
  `document.content` (`L30`) do resolve.
- **Routes asserted that were never registered.** `test_api.py` calls `/auth/login` (`L26`, `L31`), `/documents/` (`L36`),
  `/documents/{id}` (`L46`), `/users/` (`L52`), `/users/{id}` (`L57`), `/templates/` (`L63`) and `/templates/{id}` (`L73`).
  The server exposes `POST /token` (`backend/app/api/auth.py:L170`) and `POST /register` (`:L245`), `GET /me`
  (`backend/app/api/users.py:L32`) and `PUT /me` (`:L53`), plus the document and template routes at `/` and `/{id}` with no
  prefix (`main.py:L125-L128`). Not one asserted path matches a registered one, and the prefixless document and template
  routes also collide with each other.
- **201 expected where handlers return 200.** `test_api.py:L37`, `:L53` and `:L64` assert 201. No handler in any of the four
  routers sets `status_code=`, so every one returns 200 on success. The create handlers are `create_document`
  (`backend/app/api/documents.py:L56`) and `create_template` (`templates.py:L82`).
- **Five names the services never define.** `test_services.py` calls `add_collaborator` (`L44`), `remove_collaborator`
  (`L50`) and `get_collaborators` (`L55`), while `CollaborationService` defines only `connect`
  (`backend/app/services/collaboration_service.py:L75`), `disconnect` (`:L168`) and `broadcast_change` (`:L213`). The
  `@patch` decorators at `L63` and `L71` target `services.export_service.generate_pdf` and `generate_docx`, while
  `ExportService` defines `export_to_pdf` (`backend/app/services/export_service.py:L87`) and `export_to_docx` (`:L168`).
- **Five wrong argument shapes**, all in `test_services.py`. `create_document(user, "Test Document")` at `L15` passes a
  `User` where `document: DocumentCreate` is declared at `backend/app/services/document_service.py:L74`, and omits
  `user_id`. `get_document(document_id)` at `L22` and `delete_document(document_id)` at `L34` each pass one argument against
  two, at `:L125` and `:L254`. `update_document(document_id, new_content)` at `L29` passes two against three at `:L185`,
  with a `str` where a `DocumentUpdate` is declared. `export_to_pdf` at `L67` and `export_to_docx` at `L75` pass the integer
  `document_id` where a `Document` is declared.
- **One return-type mismatch.** Both export methods are annotated `-> str` and return a signed uniform resource locator
  (`export_service.py:L166`, `:L240`), while the tests assert bytes (`test_services.py:L68`, `:L76`).
- **Five unused imports.** `get_db` (`test_api.py:L5`) and `Mock` (`test_services.py:L2`) are imported once and never
  referenced again. In `test_db.py`, `firestore` (`L3`), `create_engine` (`L4`) and `sessionmaker` (`L5`) are never
  referenced as names. The first two reappear only inside the patch target strings at `L12-L13`, and `patch` resolves those
  strings itself, so the imports are not what makes patching work.
- **No packaging and no test configuration.** No `__init__.py`, no `conftest.py`, no `pytest.ini`, no `tox.ini`, no
  `[tool.pytest]` section, and no Python manifest of any kind.

The authors left three markers in place, and this pass preserves all three verbatim. `test_services.py` carries no marker,
and no file in this directory carries a to-do marker either.

- `test_api.py:L13`: `# HUMAN ASSISTANCE NEEDED: Configure test database connection`, sitting inside the `db` fixture body
  described above.
- `test_api.py:L77`: `# HUMAN ASSISTANCE NEEDED: Add more comprehensive test cases for each endpoint, including edge cases and error scenarios`.
  The coverage gap that marker names shows up as the single negative case at `L30`.
- `test_db.py:L56`: `# HUMAN ASSISTANCE NEEDED`, continued at `L57-L58`, asking for update, delete and error-handling
  coverage. `test_db.py` tests only add and read, at `L20`, `L30`, `L39` and `L47`.

One documentation inaccuracy concerns this directory. The root `README.md` project-structure block at `L59-L66` claims a
root-level `tests/` directory at `L65`. No such directory exists, and the backend tests live here. That README stays out of
scope for this pass, so this file records the inaccuracy rather than correcting it. For the consolidated defect register
covering the whole repository, see [the troubleshooting guide](../../docs/troubleshooting.md).

## Usage Examples

A reader wanting to run the suite would reach for pytest from the repository root, then narrow to one module when the first
run fails:

```bash
python -m pytest backend/tests -q
python -m pytest backend/tests/test_db.py -q
```

Neither command reaches an assertion. The first fails during collection because `test_api.py:L3` imports `app.main`, whose
chain reaches `backend/app/api/auth.py:L84` and requests a `settings` name that `backend/app/core/config.py` never binds.
The second fails at `test_db.py:L6`, which imports `backend.db.firestore_operations`, because `backend/db/` does not exist.

Comparing a declared signature against its call site shows the contract the suite assumes:

```python
# Declared, at backend/app/services/document_service.py:L125
async def get_document(self, document_id: str, user_id: str) -> Document:
    ...

# Called, at backend/tests/test_services.py:L22
document = self.document_service.get_document(document_id)
```

That call omits `user_id` and never awaits the coroutine, so it would yield a coroutine object rather than a `Document` even
after the imports resolved.

Four conditions must hold before any test here runs. The three import roots must resolve, and the six absent modules must
exist. The asserted routes must match registered routes, and the asserted signatures must match the declared ones. Each is a
code change, and this pass makes none of them. For the registered routes and the real signatures, see
[the router documentation](../app/api/README.md) and [the service documentation](../app/services/README.md).
