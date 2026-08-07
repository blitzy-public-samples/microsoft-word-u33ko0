# backend/tests

## Purpose

`backend/tests` holds the backend test suite: three modules, 21 tests, and no passing run. Eight tests run under pytest in
`test_api.py`, which exercises the Hypertext Transfer Protocol (HTTP) surface through a FastAPI test client. The other 13 run
under the standard-library `unittest` framework in `test_db.py` and `test_services.py`, which exercise persistence helpers
and domain services. All three modules target an application programming interface (API) the committed application does not
expose, so each fails at import before its first assertion runs.

This pass adds no docstrings and no inline documentation to the three modules. The three existing `HUMAN ASSISTANCE NEEDED`
comments remain verbatim, alongside the nine other comment lines in `test_api.py` and `test_db.py`. Documentation for
this directory lives in this file, and future passes must leave all three modules byte-for-byte unchanged.

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
| `TestExportService` | `unittest.TestCase` | `test_services.py:L59`, `setUp` at `:L60` | Two tests at `:L64` and `:L72` patch `services.export_service.generate_pdf` and `generate_docx`, two module-level names the real module never defines, then assert the bytes the mock was told to return |
| `__main__` guard | Entry point | `test_services.py:L79-L80` | Calls `unittest.main()`, which pytest ignores during collection |

## Architecture Fit

The suite sits outside the application layers and reaches into three of them. `test_api.py` drives the router tier through
its test client, `test_services.py` drives the service tier directly, and `test_db.py` drives a persistence tier the
committed tree does not contain. No test touches the configuration tier or the Celery task tier. For the layer map these
tiers belong to, see [the architecture overview](../../docs/architecture-overview.md).

The suite tracks the specification's route shape rather than the code's, and that one fact explains most of its route
failures. `documentation/Technical Specifications.md` declares four prefixed endpoint groups under
`SYSTEM DESIGN > API DESIGN` at L406-L432: `/auth`, `/documents`, `/users` and `/templates`. `test_api.py` asserts that same
prefixed grouping at L26, L36, L46, L52, L57, L63 and L73. Three of those seven paths correspond to a declared endpoint:
`/auth/login` composes the `/auth` group node at `:L408` with `POST /login` at `:L413`, while `/documents/{id}` and
`/templates/{id}` appear verbatim at `:L419` and `:L430`. The other four do not. `/documents/` and `/templates/` carry a
trailing slash that `:L418` and `:L429` do not declare, and the specification declares neither `POST /users` nor
`GET /users/{id}`, listing only `GET /users/me` at `:L424`, `PUT /users/me` at `:L425` and `GET /users/{id}/documents` at
`:L426`. The committed routers mount with no prefix at `backend/app/main.py:L125-L128`, so the server answers on `/`,
`/{id}`, `/token`, `/register` and `/me`.

Intended behavior per `documentation/Technical Specifications.md`, `SYSTEM DESIGN > API DESIGN`: each resource group answers
under its own prefix. The committed code registers no prefix, and this pass changes neither side.

The specification also names one backend testing framework where this directory uses two. Its `TECHNOLOGY STACK > Backend`
list names Pytest alone, at `documentation/Technical Specifications.md:L553`, while `test_db.py:L9` and
`test_services.py:L9` build on `unittest.TestCase`. That specification mentions testing at three lines only,
`documentation/Technical Specifications.md:L546`, `:L553` and `:L729`, and carries no test-strategy section.

## Dependencies

The three modules name ten internal import targets, and each falls into one of three states. Six name a module that no file
provides. Three name a module that does exist under a different root, so whether the name resolves depends on `sys.path`.
One, `app.main`, resolves and then raises during its own import. The suite checks the document and user contracts described
in [the data model reference](../../docs/data-model.md). The integration guide covers its
[Firestore and SQLAlchemy mocks](../../docs/integration-guide.md).

### Internal

| Import | Site | State |
| --- | --- | --- |
| `app.main.app` | `test_api.py:L3` | Present, path-dependent, and fails during import. `find_spec('app.main')` resolves to `backend/app/main.py` once `backend/` sits on `sys.path`, and importing it then raises through the application chain traced under Data Flows |
| `services.document_service`, `services.collaboration_service`, `services.export_service` | `test_services.py:L3-L5` | Present and path-dependent. All three files exist, and `find_spec` resolves each once `backend/app/` sits on `sys.path`, because `services/` holds no `__init__.py` and so acts as a namespace package |
| `app.models` for `User`, `Document`, `Template` | `test_api.py:L4` | Physically absent. Neither `backend/app/models.py` nor `backend/app/models/` exists |
| `app.database` for `get_db` | `test_api.py:L5` | Physically absent. Neither `backend/app/database.py` nor `backend/app/database/` exists, and the imported name is never used |
| `backend.db.firestore_operations` for `FirestoreOperations` | `test_db.py:L6` | Physically absent. `backend/` does resolve from the repository root as a namespace package, and `backend/db/` does not exist, so the failure is `No module named 'backend.db'`. No `FirestoreOperations` class exists anywhere |
| `backend.db.sql_operations` for `SQLOperations` | `test_db.py:L7` | Physically absent, for the same missing `backend/db/` package. No `SQLOperations` class exists anywhere |
| `models.document`, `models.user` | `test_services.py:L6-L7` | Physically absent. No `models` package or module exists at any import root, including `backend/app/` |

### External

| Package | Imported name | Site |
| --- | --- | --- |
| `pytest` | `pytest` | `test_api.py:L1` |
| `fastapi` | `fastapi.testclient.TestClient` | `test_api.py:L2` |
| `sqlalchemy` | `sqlalchemy.orm.Session`, then `create_engine` and `sqlalchemy.orm.sessionmaker` | `test_api.py:L6`, `test_db.py:L4-L5` |
| `google-cloud-firestore` | `google.cloud.firestore` | `test_db.py:L3` |
| Standard library | `unittest`, `unittest.mock` | `test_db.py:L1-L2`, `test_services.py:L1-L2` |

No manifest declares any of these packages, because the repository contains no Python manifest. `requirements.txt`,
`pyproject.toml`, `setup.py`, `setup.cfg`, `tox.ini`, `Pipfile` and `.python-version` are all absent, so no floor to quote.

## Configuration

Nothing in this directory is configured, so the table records the verified negatives, because an absent input still governs how the suite behaves.

| Configuration input | Read by this suite | Status |
| --- | --- | --- |
| `Settings` fields from `backend/app/core/config.py:L51` | No. No module here imports `app.core.config` | DECLARED, unread by this suite |
| Environment variables | No. Neither `os.environ` nor `os.getenv` appears in any of the three modules | Neither declared nor read |
| pytest configuration | No. `pytest.ini`, `conftest.py`, `tox.ini` and every `[tool.pytest]` host are absent | READ-BUT-NEVER-DECLARED |
| Package roots through `__init__.py` | No. Zero `__init__.py` files exist under `backend/`, so `app`, `backend`, `services` and `backend.tests` resolve as implicit namespace packages when their parent directory sits on the path, and never as regular packages | READ-BUT-NEVER-DECLARED |
| Interpreter `sys.path` and working directory | Yes, implicitly. Every import in all three modules resolves against them | READ-BUT-NEVER-DECLARED |

The last two rows carry the whole configuration surface. Namespace-package resolution is what makes the three `services.*`
imports reachable at all, and no single working directory satisfies all three import roots at once. For prerequisites and
setup steps, see [the onboarding guide](../../docs/onboarding.md), which this file does not restate.

## Data Flows

Where the path stops depends on where the reader stands, and the documented command decides it. From the repository root,
`python -m pytest backend/tests` puts the repository root on `sys.path` and puts nothing else there, so `test_api.py:L3`
raises `ModuleNotFoundError: No module named 'app'` during collection. That failure comes first, before any application code
runs.

Add `backend/` to the path and the next failure appears. `test_api.py:L8` builds one module-level client over the real
application imported at `L3`, so importing the module runs the whole application import chain before pytest collects a single
test. That chain enters `backend/app/main.py:L16`, which imports `auth_router` from `app.api.auth`, and stops at
`backend/app/api/auth.py:L81`, which imports `settings` from `app.core.config`. That configuration module binds only
`Settings` at `L51` and `get_settings` at `L126`, so the name `settings` does not exist and the import raises `ImportError`.
A second import-time cost sits at `backend/app/db/firestore.py:L40`, which constructs a Firestore client and so triggers
Google Cloud credential discovery.

The two `unittest` modules never reach the application. `test_db.py` replaces `google.cloud.firestore.Client` and
`sqlalchemy.create_engine` with mocks at `L12-L13`, so its data flow stays synthetic and touches no real service.
`test_services.py` constructs real service objects in `setUp` at `L11`, `L39` and `L61`, and the three constructors differ.
`DocumentService.__init__` binds the module-level Firestore client at `backend/app/services/document_service.py:L68-L70`,
opening nothing new. `CollaborationService.__init__` opens a Pub/Sub publisher and subscriber at
`collaboration_service.py:L69-L70`, and `ExportService.__init__` opens a Cloud Storage client at `export_service.py:L83`.
Neither module gets that far, because both fail on absent imports first.

## Design Patterns

The suite applies eight patterns, and naming them makes the defect inventory below easier to place. Both pytest fixtures are
module-scoped and neither yields nor releases anything (`test_api.py:L10`, `:L16`). One shared client serves all eight pytest
tests, built at import (`:L8`), rather than one client per test. The `unittest` modules construct their subject per test in
`setUp` (`test_db.py:L11`, `test_services.py:L10`, `:L38`, `:L60`). Patch lifecycle is manual in `test_db.py`, which starts
patches at `L12-L13` and releases them with `patch.stopall()` at `L18`, while `test_services.py` uses the decorator form at
`L63` and `L71`. Mock returns are configured through chained attribute access (`test_db.py:L15`, `:L22-L23`, `:L32-L33`,
`:L49`). A `__main__` guard at `test_services.py:L79-L80` calls `unittest.main()`, which pytest ignores. Every test is
synchronous, though 12 of the 14 route handlers under `backend/app/api/` are declared `async def`. Coverage is almost entirely
happy-path, and `test_login_invalid_credentials` at `test_api.py:L30` is the only negative case among the 21 tests.

## Known Limitations

No test in this directory currently runs. From the repository root, collection stops at `test_api.py:L3`, because `app` is
not on `sys.path`. Configure the path and `test_api.py` fails through the application import chain instead, while `test_db.py`
fails on both of its persistence imports and `test_services.py` fails on the two `models.*` imports. This pass adds no
docstrings and no inline comments to the three modules, by standing instruction, so this README carries every defect below
rather than the source files.

**Three mutually incompatible import roots.** Each root needs a different directory on `sys.path`, and the Resolves column
states what happens once that directory is there.

| Module | Import root | Needs on `sys.path` | Resolves? |
| --- | --- | --- | --- |
| `test_api.py` | `app.*` | `backend/` | `app.main` resolves and then raises `ImportError`; `app.models` and `app.database` do not exist |
| `test_db.py` | `backend.db.*` | repository root | `backend` resolves as a namespace package, and `backend/db/` does not exist, so both imports raise `No module named 'backend.db'` |
| `test_services.py` | bare `services.*` and `models.*` | `backend/app/` | All three `services.*` modules resolve; `models.document` and `models.user` exist at no root |

No single `sys.path` entry or working directory satisfies all three roots at once, so pytest cannot collect the three files
in one run however a reader invokes it. Zero `__init__.py` files exist under `backend/`, so every root that does resolve
resolves as an implicit namespace package.

- **Six imports name a module that no file provides**: `app.models` and `app.database` (`test_api.py:L4-L5`),
  `backend.db.firestore_operations` and `backend.db.sql_operations` (`test_db.py:L6-L7`), and `models.document` with
  `models.user` (`test_services.py:L6-L7`). No `FirestoreOperations` or `SQLOperations` class exists either. The three
  `services.*` imports differ: those files exist at `backend/app/services/`, and only the import root is wrong.
- **A fixture body that is a bare `pass`.** The `db` fixture at `test_api.py:L10-L14` holds two comment lines plus `pass` at
  `L14`, so it yields `None`. `test_user` at `L17` accepts that value as `db: Session`, then calls `db.add(user)` at `L20`
  and `db.commit()` at `L21` against `None`. Four further tests take the same fixture, at `L35`, `L40`, `L62` and `L67`.
- **Methods that no contract declares.** `user.set_password("testpassword")` at `test_api.py:L19`, and `test_user.get_token()`
  at `:L36`, `:L46`, `:L57`, `:L63` and `:L73`. The real `User` is a Pydantic model at `backend/app/schema/user.py:L114` and
  declares neither method.
- **Five required fields omitted.** `User(id=1, username="testuser")` at `test_services.py:L14` supplies two of the seven
  required fields, and the five omissions raise the validation error. `backend/app/schema/user.py` requires `id` (`L169`),
  `created_at` (`L170`), `updated_at` (`L171`), `is_active` (`L172`) and `is_superuser` (`L173`), plus inherited `email`
  (`L80`) and `username` (`L81`). The integer `id` also mismatches the declared `str` hint, which Pydantic 1.x coerces.
- **A field that no contract declares.** `document.owner` at `test_services.py:L18`. The `Document` contract declares
  `owner_id` at `backend/app/schema/document.py:L66` and no `owner`, while `DocumentService` writes `user_id` at
  `backend/app/services/document_service.py:L116`. The assertions on `document.title` (`L17`), `document.id` (`L24`) and
  `document.content` (`L30`) do resolve.
**The request contract, call by call.** `test_api.py` issues eight requests. No test ever issues one today, because the module
fails at import, so the table compares declared contracts rather than observed responses. Column four names the closest
committed endpoint, and column five names the first mismatch a reader would hit after correcting the ones before it.

| Site | Request | Body and headers | Asserted | Closest committed endpoint | First mismatch |
| --- | --- | --- | --- | --- | --- |
| `L26` | `POST /auth/login` | JavaScript Object Notation (JSON) `username` and `password`, no header | 200 with `access_token` | `POST /token`, `backend/app/api/auth.py:L167` | Path. No registered route carries two segments. Correct the path and the encoding still fails: `auth.py:L168` binds `OAuth2PasswordRequestForm`, which reads form fields, so request validation answers 422 before the 200 branch |
| `L31` | `POST /auth/login` | JSON with a wrong password, no header | 401 | `POST /token`, `auth.py:L167` | The same path miss, then the same 422 before the 401 branch at `auth.py:L232` |
| `L36` | `POST /documents/` | JSON `title` and `content`, bearer header from `get_token()` | 201 with `title` | `POST /`, `documents.py:L53` | Path. `main.py:L125-L128` mounts every router with no prefix, so the create route is `/`. The decorator sets no `status_code`, so a success answers 200 rather than 201 |
| `L46` | `GET /documents/{id}` | Bearer header only | 200 with `title` | `GET /{document_id}`, `documents.py:L145` | Path. The `documents` segment is not mounted, and `/{document_id}` collides with the template router's `/{template_id}` at `templates.py:L151` |
| `L52` | `POST /users/` | JSON `username`, `email` and `password`, no header | 201 with `username` | None. `users.py` registers `GET /me` at `L29` and `PUT /me` at `L50` only | No user-creation route exists on that router. Registration lives at `POST /register`, `auth.py:L242`, which answers 200 and takes `UserCreate` |
| `L57` | `GET /users/{id}` | Bearer header only | 200 with `username` | `GET /me`, `users.py:L29` | Contract shape. The server identifies the user from the token dependency, not from a path parameter, so no per-identifier user route exists |
| `L63` | `POST /templates/` | JSON `name` and `content`, bearer header | 201 with `name` | `POST /`, `templates.py:L77` | Path, as at `L36`, plus the same 200-versus-201 gap. The template router also fails to import, at `templates.py:L70-L71` |
| `L73` | `GET /templates/{id}` | Bearer header only | 200 with `name` | `GET /{template_id}`, `templates.py:L151` | Path, plus the collision with `documents.py:L145` over the identical mounted pattern |

Two consequences generalise across the table. Not one asserted path matches a registered path. No handler in any of the four
routers sets `status_code=`, so the three 201 assertions at `L37`, `:L53` and `:L64` face a 200 even after every path is
corrected.

- **Three method names the collaboration service never defines.** `test_services.py` calls `add_collaborator` (`L44`),
  `remove_collaborator` (`L50`) and `get_collaborators` (`L55`), while `CollaborationService` defines only `connect`
  (`backend/app/services/collaboration_service.py:L75`), `disconnect` (`:L173`) and `broadcast_change` (`:L218`).
- **Two patch targets that resolve to nothing.** The `@patch` decorators at `test_services.py:L63` and `:L71` name
  `services.export_service.generate_pdf` and `services.export_service.generate_docx`. The module defines neither name, so
  `patch` raises `AttributeError` when it resolves the target. Neither name is a generator function, and neither would help if
  it existed: `ExportService.export_to_pdf` (`backend/app/services/export_service.py:L87`) and `export_to_docx` (`:L168`)
  upload a literal placeholder string and return a signed link, and call no module-level converter at any point.
- **Six call sites carry the wrong shape**, all in `test_services.py`.

| Call site | Declared signature | What is wrong |
| --- | --- | --- |
| `create_document(user, "Test Document")`, `L15` | `create_document(self, document: DocumentCreate, user_id: str)`, `document_service.py:L72` | Both parameters bind, so nothing is omitted. The `User` binds to `document` and the string `"Test Document"` binds to `user_id`, so both arguments carry the wrong type |
| `get_document(document_id)`, `L22` | `get_document(self, document_id: str, user_id: str)`, `:L123` | One argument against two, and the integer `1` against a `str` hint |
| `update_document(document_id, new_content)`, `L29` | `update_document(self, document_id: str, document: DocumentUpdate, user_id: str)`, `:L183` | Two arguments against three, with a `str` where `DocumentUpdate` is declared |
| `delete_document(document_id)`, `L34` | `delete_document(self, document_id: str, user_id: str)`, `:L252` | One argument against two |
| `export_to_pdf(document_id)`, `L67` | `export_to_pdf(self, document: Document)`, `export_service.py:L87` | An integer where a `Document` is declared |
| `export_to_docx(document_id)`, `L75` | `export_to_docx(self, document: Document)`, `:L168` | An integer where a `Document` is declared |

- **Four coroutines are never awaited.** All four `DocumentService` methods are declared `async def`, at
  `document_service.py:L72`, `:L123`, `:L183` and `:L252`, and all four calls at `test_services.py:L15`, `:L22`, `:L29` and
  `:L34` omit `await`. Each call therefore evaluates to a coroutine object, so `assertIsInstance(document, Document)` at `L16`
  and every assertion after it would fail on the object's type even after the imports and the argument shapes were corrected.
- **One return-type mismatch.** Both export methods are annotated `-> str` and return a signed uniform resource locator
  (`export_service.py:L166`, `:L240`), while the tests assert bytes (`test_services.py:L68`, `:L76`).
- **Five unused imports.** `get_db` (`test_api.py:L5`) and `Mock` (`test_services.py:L2`) are imported once and never
  referenced again. In `test_db.py`, `firestore` (`L3`), `create_engine` (`L4`) and `sessionmaker` (`L5`) are never referenced
  as names. The first two reappear only inside the patch target strings at `L12-L13`, which `patch` resolves itself.
- **No packaging and no test configuration.** No `__init__.py`, no `conftest.py`, no `pytest.ini`, no `tox.ini`, no
  `[tool.pytest]` section, and no Python manifest of any kind.

### Assertion quality and isolation

Naming what fails is only half the inventory. What the 21 assertions would prove after a repair is the other half, and for
several groups the answer is little. The table covers every test in the directory.

| Group | Tests | What the assertions prove | What they leave unproven |
| --- | --- | --- | --- |
| Authentication | `test_api.py:L25`, `:L30` | That a response carries a key named `access_token` (`L28`), and that a wrong password answers 401 (`L32`) | That the token decodes, carries a subject or expiry, or comes with `token_type`. Neither test sends the form encoding `auth.py:L168` requires |
| Document routes | `test_api.py:L35`, `:L40` | That `title` round-trips through create and read (`L38`, `L48`) | Ownership, the 403 and 404 branches at `documents.py:L146-L190`, and the list, update and delete routes entirely |
| User routes | `test_api.py:L51`, `:L56` | That `username` appears in each response body (`L54`, `L59`) | The token dependency, the profile update route at `users.py:L50`, and every validation failure |
| Template routes | `test_api.py:L62`, `:L67` | That `name` round-trips (`L65`, `L75`) | The list, update and delete routes, and the router's own import failure |
| Firestore | `test_db.py:L20`, `:L30` | That `add` receives the payload (`L27`), and that a stored dictionary comes back (`L37`) | Which collection or document was addressed. The mock chains at `L22` and `L32` answer identically for any identifier, so `'test_collection'` and `'doc_id'` are never checked. `L37` asserts the value configured at `L33` |
| Relational | `test_db.py:L39`, `:L47` | That `execute` and `commit` were each called once (`L44`, `L45`, `L53`) | The statement text, the bound parameters, the table name, rollback, and update and delete paths. `L54` asserts the tuple configured at `L49` |
| Document service | `test_services.py:L13`, `:L20`, `:L26`, `:L32` | Little. `L35` accepts any truthy value, and the attribute assertions target an object the calls never return | Every Firestore interaction, the ownership comparison, and the 403 and 404 paths |
| Collaboration | `test_services.py:L41`, `:L47`, `:L53` | Little. `L45` and `L51` accept any truthy value, and `L57` wraps `all(...)`, which holds for an empty list | Every real method, so `connect`, `disconnect` and `broadcast_change` are untested. An empty collaborator list satisfies `L56-L57` |
| Export | `test_services.py:L64`, `:L72` | That the patched name was called once with the argument passed (`L69`, `L77`) | The real upload and signing behaviour. `L68` and `L76` assert the byte strings configured at `L66` and `L74`, so each test verifies its own mock |

Five isolation and ordering weaknesses sit underneath those assertions.

- Both pytest fixtures declare `scope="module"` with fixed data, `testuser` and `test@example.com` at `test_api.py:L18`, and
  neither yields nor rolls back, so a repaired run leaves rows behind and a second run collides on any unique constraint.
- `test_login_invalid_credentials` at `test_api.py:L30` requests no fixture, so it depends on an earlier test having created
  the user it names.
- `patch.stopall()` at `test_db.py:L18` stops every patch active in the process, not only the two started at `L12-L13`.
- `test_services.py` declares no `tearDown`, so the Pub/Sub and Cloud Storage clients its `setUp` methods open at `L39` and
  `L61` are never released.
- The two patch targets in `test_db.py` would not isolate the committed adapters. `backend/app/db/firestore.py:L34` binds
  `Client` at import and `L40` constructs the client during import, and `backend/app/db/sql.py:L12` binds `create_engine` with
  `L16` calling it during import, so a patch started later in `setUp` never reaches either binding.

Do not run a repaired suite with production Application Default Credentials. Patch symbols at their use sites and point every
client at an isolated test project.

The authors left three markers in place, and this pass preserves all three verbatim. `test_services.py` carries no marker,
and no file in this directory carries a to-do marker either.

| Marker location | What its guidance asks for |
| --- | --- |
| `test_api.py:L13` | Configure the test database connection. The marker sits inside the `db` fixture body described above |
| `test_api.py:L77` | Add comprehensive cases per endpoint, covering edge cases and error scenarios. The gap shows as the single negative case at `L30` |
| `test_db.py:L56-L58` | Add update, delete and error-handling coverage. The module tests only add and read, at `L20`, `L30`, `L39` and `L47` |

One documentation inaccuracy concerns this directory. The root README project-structure block at
`../../README.md:L59-L66` claims a root-level `tests/` directory at `:L65`. No such directory exists, and the backend
tests live here. That README stays out of
scope for this pass, so this file records the inaccuracy rather than correcting it. For the consolidated defect register
covering the whole repository, see [the troubleshooting guide](../../docs/troubleshooting.md).

## Usage Examples

A reader wanting to run the suite would reach for pytest from the repository root, then narrow to one module when the first
run fails:

```bash
python -m pytest backend/tests -q
python -m pytest backend/tests/test_db.py -q
```

Neither command reaches an assertion. The first fails during collection at `test_api.py:L3`, which imports `app.main` while
`sys.path` carries the repository root and no `app` package sits there, so the error is
`ModuleNotFoundError: No module named 'app'`. Put `backend/` on the path and the same line fails one level deeper: the import
chain reaches `backend/app/api/auth.py:L81` and requests a `settings` name that `backend/app/core/config.py` never binds. The
second command fails at `test_db.py:L6`, which imports `backend.db.firestore_operations`. That root resolves as far as
`backend`, and `backend/db/` does not exist.

Comparing a declared signature against its call site shows the contract the suite assumes:

```python
# Declared, at backend/app/services/document_service.py:L123
async def get_document(self, document_id: str, user_id: str) -> Document:
    ...

# Called, at backend/tests/test_services.py:L22
document = self.document_service.get_document(document_id)
```

That call omits `user_id` and never awaits the coroutine, so it would yield a coroutine object rather than a `Document` even
after the imports resolved.

Two sets of conditions stand between this directory and a green run, and they are not the same set. Collection needs the three
import roots reachable from one invocation, the six absent modules created, and `app.main` importable, which means the
`settings` singleton restored. Only then do the assertions get a chance. Passing needs more: the asserted routes matched to
registered routes, the three 201 expectations reconciled against handlers that answer 200, and the `set_password`,
`get_token`, `add_collaborator`, `remove_collaborator` and `get_collaborators` methods defined. It also needs the six argument
shapes corrected, the four coroutines awaited, and the export patch targets pointed at names that exist. Every item on both
lists is a code change, and this pass makes none of them. For the registered routes and the real signatures, see
[the router documentation](../app/api/README.md) and [the service documentation](../app/services/README.md).
