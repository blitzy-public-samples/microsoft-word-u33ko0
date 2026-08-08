# backend/tests

## Purpose

`backend/tests` holds the backend test suite: three modules, 21 tests, and no passing run. Eight tests run under pytest in `test_api.py`, the only module that
exercises the Hypertext Transfer Protocol (HTTP) surface, which it reaches through a FastAPI test client. The other 13 run under the standard-library `unittest`
framework.

Four of them, in `test_db.py`, drive Python persistence wrapper classes. The remaining nine, in `test_services.py`, call Python service methods directly. Neither
module issues an HTTP request. All three target interfaces that do not match the committed code, so each fails at import before its first assertion runs.

This pass adds no docstrings and no inline documentation to the three modules. The three existing `HUMAN ASSISTANCE NEEDED` comments remain verbatim, alongside the nine other
comment lines in `test_api.py` and `test_db.py`. Documentation for this directory lives in this file, and future passes must leave all three modules byte-for-byte unchanged.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `test_api.py` | Test module, 77 lines | `backend/tests/test_api.py` | pytest tests over the HTTP surface, using `fastapi.testclient.TestClient` |
| `test_db.py` | Test module, 58 lines | `backend/tests/test_db.py` | `unittest` tests over two persistence helper classes the repository never defines |
| `test_services.py` | Test module, 80 lines | `backend/tests/test_services.py` | `unittest` tests over the three domain services |
| `client` | Module-level test client | `test_api.py:L8` | `TestClient(app)` built at import time and shared by all eight pytest tests |
| `db` | pytest fixture, module scope | `test_api.py:L10-L14` | Declares a test database session. The body is two comment lines plus `pass` at `L14`, so the fixture yields `None` |
| `test_user` | pytest fixture, module scope | `test_api.py:L16-L22` | Builds a `User`, calls `set_password` at `L19`, then `db.add` at `L20` and `db.commit` at `L21` |
| The eight pytest tests | pytest tests | `test_api.py:L25`, `:L30`, `:L35`, `:L40`, `:L51`, `:L56`, `:L62`, `:L67` | Post credentials to `/auth/login` asserting 200 with an `access_token` then 401, and create through `POST /documents/`, `POST /users/` and `POST /templates/` asserting 201, reading each back by identifier. The request contract table under Known Limitations carries every path, body and assertion |
| `TestDatabaseOperations` | `unittest.TestCase` | `test_db.py:L9` | `setUp` at `L11` starts two patches, `tearDown` at `L17` releases them at `L18`. Four tests at `L20`, `L30`, `L39` and `L47` add and read a Firestore document, then add and read a relational record |
| `TestDocumentService`, `TestCollaborationService`, `TestExportService` | Three `unittest.TestCase` classes | `test_services.py:L9`, `:L37`, `:L59`, with `setUp` at `:L10`, `:L38` and `:L60` | Four document tests at `:L13`, `:L20`, `:L26` and `:L32` create, read, update and delete. Three collaboration tests at `:L41`, `:L47` and `:L53` add, remove and list collaborators. Two export tests at `:L64` and `:L72` patch `services.export_service.generate_pdf` and `generate_docx`, two module-level names the real module never defines, then assert the bytes the mock was told to return |
| `__main__` guard | Entry point | `test_services.py:L79-L80` | Calls `unittest.main()`, which pytest ignores during collection |

## Architecture Fit

The suite sits outside the application layers and reaches into three of them. `test_api.py` drives the router tier through its test client, `test_services.py` drives the
service tier directly, and `test_db.py` drives a persistence tier the committed tree does not contain. No test touches the configuration tier or the Celery task tier. For the
layer map these tiers belong to, see [the architecture overview](../../docs/architecture-overview.md).

The suite tracks the specification's route shape rather than the code's, and that one fact explains most of its route failures. `documentation/Technical
Specifications.md` declares four prefixed endpoint groups under `SYSTEM DESIGN > API DESIGN` at L406-L432, and `test_api.py` asserts that same prefixed grouping at
L26, L36, L46, L52, L57, L63 and L73. Three of those seven paths correspond to a declared endpoint. `/auth/login` composes the `/auth` group node at `:L408` with
`POST /login` at `:L413`, and `/documents/{id}` and `/templates/{id}` appear verbatim at `:L419` and `:L430`.

The other four do not. `/documents/` and `/templates/` carry a trailing slash that `:L418` and `:L429` do not declare. The specification declares neither `POST
/users` nor `GET /users/{id}`, listing only `GET /users/me` at `:L424`, `PUT /users/me` at `:L425` and `GET /users/{id}/documents` at `:L426`. Intended behavior per
that section: each resource group answers under its own prefix. The committed routers mount with no prefix at `backend/app/main.py:L84-L87`, so the server answers on
`/`, `/{id}`, `/token`, `/register` and `/me`, and this pass changes neither side.

The specification also names one backend testing framework where this directory uses two. Its `TECHNOLOGY STACK > Backend` list names Pytest alone, at
`documentation/Technical Specifications.md:L553`, while `test_db.py:L9` and `test_services.py:L9` build on `unittest.TestCase`. That specification mentions testing at three
lines only, `documentation/Technical Specifications.md:L546`, `:L553` and `:L729`, and carries no test-strategy section.

## Dependencies

The three modules name ten internal import targets, and each falls into one of three states.

Six name a module that no file provides. Three name a module that does exist under a different root, so whether the name resolves depends on `sys.path`. One,
`app.main`, resolves and then raises during its own import. The suite checks the document and user contracts described in [the data model
reference](../../docs/data-model.md). The integration guide covers its [Firestore and SQLAlchemy mocks](../../docs/integration-guide.md).

### Internal

| Import | Site | State |
| --- | --- | --- |
| `app.main.app` | `test_api.py:L3` | Present, path-dependent, and fails during import. `find_spec('app.main')` resolves to `backend/app/main.py` once `backend/` sits on `sys.path`, and importing it then raises through the application chain traced under Data Flows |
| `services.document_service`, `services.collaboration_service`, `services.export_service` | `test_services.py:L3-L5` | Present and path-dependent, and locatable is not the same as importable. All three files exist, and `find_spec` resolves each once `backend/app/` sits on `sys.path`, because `services/` holds no `__init__.py` and so acts as a namespace package. Executing any of them additionally needs `backend/` on the path, because each opens with `app.*` imports, and each then stops at the absent `settings` name traced under Data Flows |
| `app.models` for `User`, `Document`, `Template`, and `app.database` for `get_db` | `test_api.py:L4-L5` | Physically absent. None of `backend/app/models.py`, `backend/app/models/`, `backend/app/database.py` or `backend/app/database/` exists, and the `get_db` name is never used |
| `backend.db.firestore_operations` for `FirestoreOperations`, and `backend.db.sql_operations` for `SQLOperations` | `test_db.py:L6-L7` | Physically absent. `backend/` resolves from the repository root as a namespace package and `backend/db/` does not exist, so both fail with `No module named 'backend.db'`. Neither class exists anywhere |
| `models.document`, `models.user` | `test_services.py:L6-L7` | Physically absent. No `models` package or module exists at any import root, including `backend/app/` |

### External

| Package | Imported name | Site |
| --- | --- | --- |
| `pytest`, `fastapi` | `pytest`, `fastapi.testclient.TestClient` | `test_api.py:L1-L2` |
| `sqlalchemy` | `sqlalchemy.orm.Session`, then `create_engine` and `sqlalchemy.orm.sessionmaker` | `test_api.py:L6`, `test_db.py:L4-L5` |
| `google-cloud-firestore` | `google.cloud.firestore` | `test_db.py:L3` |
| Standard library | `unittest`, `unittest.mock` | `test_db.py:L1-L2`, `test_services.py:L1-L2` |

No manifest declares any of these packages, because the repository contains no Python manifest. `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `tox.ini`,
`Pipfile` and `.python-version` are all absent, so no floor to quote.

## Configuration

Nothing in this directory is configured, so the table records the verified negatives, because an absent input still governs how the suite behaves.

| Configuration input | Read by this suite | Status |
| --- | --- | --- |
| `Settings` fields from `backend/app/core/config.py:L20` | No. No module here imports `app.core.config` | DECLARED, unread by this suite |
| Environment variables | No. Neither `os.environ` nor `os.getenv` appears in any of the three modules | Neither declared nor read |
| pytest configuration | No. `pytest.ini`, `conftest.py`, `tox.ini` and every `[tool.pytest]` host are absent | READ-BUT-NEVER-DECLARED |
| Package roots through `__init__.py` | No. Zero `__init__.py` files exist under `backend/`. So `app`, `backend`, `services` and `backend.tests` resolve as implicit namespace packages when their parent directory sits on the path, and never as regular packages | READ-BUT-NEVER-DECLARED |
| Interpreter `sys.path` and working directory | Yes, implicitly. Every import in all three modules resolves against them | READ-BUT-NEVER-DECLARED |

The last two rows carry the whole configuration surface. Namespace-package resolution is what makes the three `services.*` imports reachable at all, and no single working
directory satisfies all three import roots at once. For prerequisites and setup steps, see [the onboarding guide](../../docs/onboarding.md), which this file does not restate.

## Data Flows

Where the path stops depends on where the reader stands. From the repository root, `python -m pytest backend/tests` puts the repository root on `sys.path` and nothing else,
so `test_api.py:L3` raises `ModuleNotFoundError: No module named 'app'` during collection, before any application code runs.

Add `backend/` to the path and the next failure appears. `test_api.py:L8` builds one module-level client over the real application imported at `L3`, so importing the module
runs the whole application import chain before pytest collects a single test. That chain enters `backend/app/main.py:L16`, which imports `auth_router` from `app.api.auth`,
and stops at `backend/app/api/auth.py:L20`, which imports `settings` from `app.core.config`. That configuration module binds only `Settings` at `L21` and `get_settings` at
`L62`, so the name does not exist and the import raises `ImportError`. A second import-time cost sits at `backend/app/db/firestore.py:L20`, which constructs a Firestore
client and so triggers Google Cloud credential discovery.

The two `unittest` modules never reach the application, because both fail on absent imports first. `test_db.py` replaces `google.cloud.firestore.Client` and
`sqlalchemy.create_engine` with mocks at `L12-L13`, so its data flow stays synthetic.

`test_services.py` constructs real service objects in `setUp` at `L11`, `L39` and `L61`, and the three constructors differ. `DocumentService.__init__` binds the
module-level Firestore client at `backend/app/services/document_service.py:L33-L40` and opens nothing new. `CollaborationService.__init__` opens a Pub/Sub publisher
and subscriber at `collaboration_service.py:L38-L39`. `ExportService.__init__` opens a Cloud Storage client at `export_service.py:L36`.

## Design Patterns

The suite applies eight patterns, and naming them makes the defect inventory below easier to place. Both pytest fixtures are module-scoped and neither yields nor
releases anything (`test_api.py:L10`, `:L16`). One shared client serves all eight pytest tests, built at import (`:L8`), rather than one client per test. The
`unittest` modules construct their subject per test in `setUp` (`test_db.py:L11`, `test_services.py:L10`, `:L38`, `:L60`).

Patch lifecycle is manual in `test_db.py`, which starts patches at `L12-L13` and releases them with `patch.stopall()` at `L18`, while `test_services.py` uses the
decorator form at `L63` and `L71`. Mock returns are configured through chained attribute access (`test_db.py:L15`, `:L22-L23`, `:L32-L33`, `:L49`). A `__main__`
guard at `test_services.py:L79-L80` calls `unittest.main()`, which pytest ignores. Every test is synchronous, though 12 of the 14 route handlers under
`backend/app/api/` are declared `async def`. Coverage is almost entirely happy-path, and `test_login_invalid_credentials` at `test_api.py:L30` is the only negative
case among the 21 tests.

## Known Limitations

No test in this directory currently runs. From the repository root, collection stops at `test_api.py:L3`, because `app` is not on `sys.path`, and the Resolves column below
states what each module does once a path is configured. Adding no comment to the three modules is a standing instruction, so this README carries every defect below.

**Three mutually incompatible import roots.** Each root needs a different directory on `sys.path`, and the Resolves column states what happens once that directory is there.

| Module | Import root | Needs on `sys.path` | Resolves? |
| --- | --- | --- | --- |
| `test_api.py` | `app.*` | `backend/` | `app.main` resolves and then raises `ImportError`; `app.models` and `app.database` do not exist |
| `test_db.py` | `backend.db.*` | repository root | `backend` resolves as a namespace package, and `backend/db/` does not exist, so both imports raise `No module named 'backend.db'` |
| `test_services.py` | bare `services.*` and `models.*` | `backend/app/` for discovery, plus `backend/` for execution | All three `services.*` specifiers are located, and importing one then needs `app.*` reachable and still stops at the absent `settings` name; `models.document` and `models.user` exist at no root |

No single `sys.path` entry or working directory satisfies all three roots at once, so pytest cannot collect the three files in one run however a reader invokes it. Zero
`__init__.py` files exist under `backend/`, so every root that does resolve resolves as an implicit namespace package.

| Defect | Evidence |
| --- | --- |
| Six imports name a module that no file provides | `app.models` and `app.database` (`test_api.py:L4-L5`), `backend.db.firestore_operations` and `backend.db.sql_operations` (`test_db.py:L6-L7`), and `models.document` with `models.user` (`test_services.py:L6-L7`). No `FirestoreOperations` or `SQLOperations` class exists either. The three `services.*` imports are a separate case: those files exist at `backend/app/services/`, so the wrong root blocks discovery and the absent `settings` name then blocks execution |
| A fixture body that is a bare `pass` | The `db` fixture at `test_api.py:L10-L14` holds two comment lines plus `pass` at `L14`, so it yields `None`. `test_user` at `L17` accepts that value as `db: Session`, then calls `db.add(user)` at `L20` and `db.commit()` at `L21` against `None`. Four further tests take the same fixture, at `L35`, `L40`, `L62` and `L67` |
| Methods that no contract declares | `user.set_password("testpassword")` at `test_api.py:L19`, and `test_user.get_token()` at `:L36`, `:L46`, `:L57`, `:L63` and `:L73`. The real `User` is a Pydantic model at `backend/app/schema/user.py:L56` and declares neither method |
| Five required fields omitted | `User(id=1, username="testuser")` at `test_services.py:L14` supplies two of the seven required fields, and the five omissions raise the validation error. `backend/app/schema/user.py` requires `id` (`L68`), `created_at` (`L69`), `updated_at` (`L70`), `is_active` (`L71`) and `is_superuser` (`L72`), plus inherited `email` (`L26`) and `username` (`L27`). The integer `id` also mismatches the declared `str` hint, which Pydantic 1.x coerces |
| A field that no contract declares | `document.owner` at `test_services.py:L18`. The `Document` contract declares `owner_id` at `backend/app/schema/document.py:L28` and no `owner`, while `DocumentService` writes `user_id` at `backend/app/services/document_service.py:L71`. The assertions on `document.title` (`L17`), `document.id` (`L24`) and `document.content` (`L30`) do resolve |

**The request contract, call by call.** `test_api.py` issues eight requests, and none reaches a server today, because the module fails at import. Column four names the closest
committed endpoint, and column five names the first mismatch a reader would hit after correcting the ones before it.

| Site | Request | Body and headers | Asserted | Closest committed endpoint | First mismatch |
| --- | --- | --- | --- | --- | --- |
| `L26` | `POST /auth/login` | JavaScript Object Notation (JSON) `username` and `password`, no header | 200 with `access_token` | `POST /token`, `backend/app/api/auth.py:L66` | Path. No registered route carries two segments. Correct the path and the encoding still fails: `auth.py:L67` binds `OAuth2PasswordRequestForm`, which reads form fields, so request validation answers 422 before the 200 branch |
| `L32` | `POST /auth/login` | JSON with a wrong password, no header | 401 | `POST /token`, `auth.py:L66` | The same path miss, then the same 422 before the 401 branch at `auth.py:L93` |
| `L37` | `POST /documents/` | JSON `title` and `content`, bearer header from `get_token()` | 201 with `title` | `POST /`, `documents.py:L24` | Path. `main.py:L84-L87` mounts every router with no prefix, so the create route is `/`. The decorator sets no `status_code`, so a success answers 200 rather than 201 |
| `L46` | `GET /documents/{id}` | Bearer header only | 200 with `title` | `GET /{document_id}`, `documents.py:L68` | Path. The `documents` segment is not mounted, and `/{document_id}` collides with the template router's `/{template_id}` at `templates.py:L59` |
| `L52` | `POST /users/` | JSON `username`, `email` and `password`, no header | 201 with `username` | None. `users.py` registers `GET /me` at `L19` and `PUT /me` at `L32` only | No user-creation route exists on that router. Registration lives at `POST /register`, `auth.py:L103`, which answers 200 and takes `UserCreate` |
| `L58` | `GET /users/{id}` | Bearer header only | 200 with `username` | `GET /me`, `users.py:L19` | Contract shape. The server identifies the user from the token dependency, not from a path parameter, so no per-identifier user route exists |
| `L63` | `POST /templates/` | JSON `name` and `content`, bearer header | 201 with `name` | `POST /`, `templates.py:L24` | Path, as at `L36`, plus the same 200-versus-201 gap. The template router also fails to import, at `templates.py:L17-L18` |
| `L20` | `GET /templates/{id}` | Bearer header only | 200 with `name` | `GET /{template_id}`, `templates.py:L59` | Path, plus the collision with `documents.py:L68` over the identical mounted pattern |

Two consequences generalise across the table: not one asserted path matches a registered path. The three 201 assertions at `L37`, `:L24` and `:L64` face a 200 even after
every path is corrected, because no handler in the four routers sets `status_code=`.

**Six call sites carry the wrong shape**, all in `test_services.py`.

| Call site | Declared signature | What is wrong |
| --- | --- | --- |
| `create_document(user, "Test Document")`, `L15` | `create_document(self, document: DocumentCreate, user_id: str)`, `document_service.py:L42` | Both parameters bind, so nothing is omitted. The `User` binds to `document` and the string `"Test Document"` binds to `user_id`, so both arguments carry the wrong type |
| `get_document(document_id)`, `L22` | `get_document(self, document_id: str, user_id: str)`, `:L78` | One argument against two, and the integer `1` against a `str` hint |
| `update_document(document_id, new_content)`, `L29` | `update_document(self, document_id: str, document: DocumentUpdate, user_id: str)`, `:L116` | Two arguments against three, with a `str` where `DocumentUpdate` is declared |
| `delete_document(document_id)`, `L34` | `delete_document(self, document_id: str, user_id: str)`, `:L159` | One argument against two |
| `export_to_pdf(document_id)`, `L67` | `export_to_pdf(self, document: Document)`, `export_service.py:L40` | An integer where a `Document` is declared |
| `export_to_docx(document_id)`, `L75` | `export_to_docx(self, document: Document)`, `:L74` | An integer where a `Document` is declared |

| Defect | Evidence |
| --- | --- |
| Four coroutines are never awaited | All four `DocumentService` methods are declared `async def`, at `document_service.py:L42`, `:L78`, `:L116` and `:L159`, and all four calls at `test_services.py:L15`, `:L22`, `:L29` and `:L34` omit `await`. Each call therefore evaluates to a coroutine object. `assertIsInstance(document, Document)` at `L16` and every assertion after it would fail on the object's type, even after the imports and the argument shapes were corrected |
| One return-type mismatch | Both export methods are annotated `-> str` and return a signed uniform resource locator (`export_service.py:L72`, `:L104`), while the tests assert bytes (`test_services.py:L68`, `:L76`) |
| Five unused imports | `get_db` (`test_api.py:L5`) and `Mock` (`test_services.py:L2`) are imported once and never referenced again. In `test_db.py`, `firestore` (`L3`), `create_engine` (`L4`) and `sessionmaker` (`L5`) are never referenced as names. The first two reappear only inside the patch target strings at `L12-L13`, which `patch` resolves itself |
| No packaging and no test configuration | No `__init__.py`, no `conftest.py`, no `pytest.ini`, no `tox.ini`, no `[tool.pytest]` section, and no Python manifest of any kind |

### Assertion quality and isolation

What the 21 tests would prove after a repair is the other half of the inventory, and for several groups the answer is little. The 21 tests spend 37 assertion expressions
between them, 15 in `test_api.py`, 7 in `test_db.py` and 15 in `test_services.py`. The table covers every test here, then the five isolation weaknesses underneath them.

| Group | Tests | What the assertions prove | What they leave unproven |
| --- | --- | --- | --- |
| Authentication | `test_api.py:L25`, `:L30` | A response carries a key named `access_token` (`L28`), and a wrong password answers 401 (`L32`) | That the token decodes, carries a subject or expiry, or comes with `token_type`. Neither test sends the form encoding the `OAuth2PasswordRequestForm` dependency at `auth.py:L67` requires |
| Document routes | `test_api.py:L35`, `:L40` | `title` round-trips through create and read (`L38`, `L48`) | Ownership, the three router 403 branches at `documents.py:L95`, `:L127` and `:L155`, the service 404 paths, and the list, update and delete routes entirely |
| User and template routes | `test_api.py:L51`, `:L56`, `:L62`, `:L67` | `username` appears in each user response (`L54`, `L59`) and `name` round-trips for templates (`L65`, `L75`) | The token dependency, the profile update route at `users.py:L32-L33`, every validation failure, the list, update and delete routes, and the template router's own import failure |
| Firestore and relational | `test_db.py:L20`, `:L30`, `:L39`, `:L47` | `add` receives the payload (`L27`), a stored dictionary comes back (`L37`), and `execute` and `commit` are each called once (`L44`, `L45`, `L53`) | Which collection or document was addressed: the mock chains at `L22` and `L32` answer identically for any identifier, so `'test_collection'` and `'doc_id'` are never checked. Also the statement text, bound parameters, table name, rollback, and update and delete paths. `L37` and `L54` assert the values configured at `L33` and `L49` |
| Document service | `test_services.py:L13`, `:L20`, `:L26`, `:L32` | Little. `L35` accepts any truthy value, and the attribute assertions target an object the calls never return | Every Firestore interaction, the ownership comparison, and the 403 and 404 paths |
| Collaboration | `test_services.py:L41`, `:L47`, `:L53` | Little. `L45` and `L51` accept any truthy value, and `L57` wraps `all(...)`, which holds for an empty list | Every real method, so `connect`, `disconnect` and `broadcast_change` are untested. An empty collaborator list satisfies `L56-L57` |
| Export | `test_services.py:L64`, `:L72` | The patched name was called once with the argument passed (`L69`, `L77`) | The real upload and signing behaviour. `L68` and `L76` assert the byte strings configured at `L66` and `L74`, so each test verifies its own mock |
| Isolation and ordering | whole directory | Nothing about isolation, and nothing about a test standing alone. Five separate weaknesses carry that verdict, and the table below states each one with its evidence | Everything in the table below |

| Isolation or ordering weakness | Evidence |
| --- | --- |
| Both pytest fixtures declare `scope="module"` with fixed data | `testuser` and `test@example.com` at `test_api.py:L18`, and neither yields nor rolls back, so a repaired run leaves rows behind and a second run collides on any unique constraint |
| `test_login_invalid_credentials` requests no fixture | At `test_api.py:L30`, so it depends on an earlier test having created the user it names |
| `patch.stopall()` stops every patch active in the process | At `test_db.py:L18`, not only the two started at `L12-L13` |
| `test_services.py` declares no `tearDown` | The Pub/Sub and Cloud Storage clients its `setUp` methods open at `L39` and `L61` are never released |
| The two patch targets in `test_db.py` would not isolate the committed adapters | `backend/app/db/firestore.py:L14` binds `Client` at import and `L20` constructs the client during import. `backend/app/db/sql.py:L12` binds `create_engine` with `L16` calling it during import. A patch started later in `setUp` therefore never reaches either binding |

Do not run a repaired suite with production Application Default Credentials. Patch symbols at their use sites and point every client at an isolated test project.

The authors left three markers in place, and this pass preserves all three verbatim. `test_services.py` carries no marker, and no file here carries a to-do marker.

| Marker location | What its guidance asks for |
| --- | --- |
| `test_api.py:L13` | Configure the test database connection. The marker sits inside the `db` fixture body described above |
| `test_api.py:L77` | Add comprehensive cases per endpoint, covering edge cases and error scenarios. The gap shows as the single negative case at `L30` |
| `test_db.py:L56-L58` | Add update, delete and error-handling coverage. The module tests only add and read, at `L20`, `L30`, `L39` and `L47` |

One documentation inaccuracy concerns this directory. The root README project-structure block at `../../README.md:L59-L66` claims a root-level `tests/` directory at `:L65`.
No such directory exists, and the backend tests live here. That README stays out of scope for this pass, so this file records the inaccuracy rather than correcting it. For
the consolidated defect register covering the whole repository, see [the troubleshooting guide](../../docs/troubleshooting.md).

## Usage Examples

Install the test dependencies first, because no committed file declares them. A clean machine answers `ModuleNotFoundError: No module named 'pytest'` before it reaches any
application defect, and `test_api.py` also needs `fastapi` while `test_db.py` needs `google-cloud-firestore` and `SQLAlchemy`. The
[onboarding Testing subsection](../../docs/onboarding.md#testing-what-exists-and-why-no-green-run-is-possible) carries the install line. With those installed, a reader would
reach for pytest from the repository root, then narrow to one module when the first run fails:

```bash
python -m pytest backend/tests -q
python -m pytest backend/tests/test_db.py -q
```

Neither command reaches an assertion. The first fails during collection at `test_api.py:L3`, which imports `app.main` while `sys.path` carries the repository root and no
`app` package sits there, so the error is `ModuleNotFoundError: No module named 'app'`. Put `backend/` on the path and the same line fails one level deeper: the import chain
reaches `backend/app/api/auth.py:L20` and requests a `settings` name that `backend/app/core/config.py` never binds. The second command fails at `test_db.py:L6`, which imports
`backend.db.firestore_operations`. That root resolves as far as `backend`, and `backend/db/` does not exist.

Comparing a declared signature against its call site shows the contract the suite assumes:

```python
# Declared, at backend/app/services/document_service.py:L78
async def get_document(self, document_id: str, user_id: str) -> Document:
    ...

# Called, at backend/tests/test_services.py:L22
document = self.document_service.get_document(document_id)
```

That call omits `user_id` and never awaits the coroutine, so it would yield a coroutine object rather than a `Document` even after the imports resolved.

Two different sets of conditions stand between this directory and a green run. Collection needs the three import roots reachable from one invocation, the six absent modules
created, and `app.main` importable, which means the `settings` singleton restored. Passing needs six further changes:

- asserted routes matched to registered routes
- the three 201 expectations reconciled against handlers that answer 200
- the `set_password`, `get_token`, `add_collaborator`, `remove_collaborator` and `get_collaborators` methods defined
- the six argument shapes corrected
- the four coroutines awaited
- the export patch targets pointed at names that exist

Every item on both lists is a code change, and this
pass makes none of them. For the registered routes and the real signatures, see [the router documentation](../app/api/README.md) and
[the service documentation](../app/services/README.md).
