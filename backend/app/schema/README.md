# backend/app/schema

## Purpose

The package declares the Pydantic models that validate request bodies and shape response payloads at the HyperText Transfer Protocol (HTTP)
boundary. `document.py` declares five models for documents and document versions, and `user.py` declares four models for users plus one
nested configuration class. Documents and users each follow a create, read, update and delete (CRUD) model family, so separate classes carry
the create payload, the patch payload and the read response.

`DocumentVersion` is the exception: it has one model and no create or update variant, because no handler and no service writes a version. No
module here reaches a database, reads configuration or holds state. The application programming interface (API) routers under `app/api/` and
the services under `app/services/` import from this package rather than the reverse. Every `file:Lnn` locator below numbers the file as it
stands at current `HEAD`, using physical line numbering.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `DocumentBase` | Pydantic model | `document.py:L16` | Shared document fields: `title: str` at L26, `content: str` at L27 and `owner_id: Optional[str] = None` at L28. |
| `DocumentCreate` | Pydantic model | `document.py:L30` | Create payload. The body is `pass` at L38, so the class inherits all three `DocumentBase` fields and adds none. |
| `DocumentUpdate` | Pydantic model | `document.py:L40` | Patch payload. Extends `BaseModel` and declares `title` at L49 and `content` at L50, both `Optional[str] = None`. |
| `Document` | Pydantic model | `document.py:L52` | Read response. Extends `DocumentBase` and adds `id: str` at L63, `created_at: datetime` at L64 and `updated_at: datetime` at L65. |
| `DocumentVersion` | Pydantic model | `document.py:L67` | Version record. Extends `BaseModel` with `id` at L81, `document_id` at L82, `content` at L83, `created_at` at L84 and `user_id` at L85. |
| `UserBase` | Pydantic model | `user.py:L17` | Shared user fields: `email: str` at L26, `username: str` at L27 and `full_name: Optional[str] = None` at L28. |
| `UserCreate` | Pydantic model | `user.py:L30` | Registration payload. Extends `UserBase` and adds `password: str` at L38. |
| `UserUpdate` | Pydantic model | `user.py:L40` | Patch payload. Extends `BaseModel` with `email` at L51, `username` at L52, `full_name` at L53 and `password` at L54, all `Optional[str] = None`. |
| `User` | Pydantic model | `user.py:L56` | Read response. Extends `UserBase` and adds `id` at L68, `created_at` at L69, `updated_at` at L70, `is_active: bool` at L71 and `is_superuser: bool` at L72. |
| `Config` | Nested configuration class | `user.py:L74` | Sets `orm_mode = True` at L81 on `User` alone. No document model declares the key. |

## Architecture Fit

Nine `app.schema.*` import statements reach this package from seven modules, and eight resolve. The importers sit at `app/api/auth.py:L21`,
`app/api/documents.py:L17` and `:L20`, `app/api/templates.py:L17` and `:L20`, `app/api/users.py:L13`, `app/services/collaboration_service.py:L17`,
`app/services/document_service.py:L15` and `app/services/export_service.py:L15`. The single failure is `app/api/templates.py:L17`, which imports
`Template`, `TemplateCreate` and `TemplateUpdate` from `app.schema.template`, and no file exists at `backend/app/schema/template.py`. The package
serves the router and service tiers at once, and both depend on it.

Declared intent describes a wider data layer. The `## DATABASE DESIGN` heading at `documentation/Technical Specifications.md:L315` sits under
`# SYSTEM DESIGN` at `:L300`. At `:L317` it pairs Google Cloud Firestore, a NoSQL store of schemaless records, with Google Cloud SQL, a relational
Structured Query Language (SQL) database. Its `### Google Cloud Firestore (NoSQL)` heading at `:L319` lists Documents `:L331-L336`, Versions
`:L338-L341`, Comments `:L343-L348` and Users `:L350-L354`. Its `### Google Cloud SQL (Relational)` heading at `:L356` adds `USERS` `:L365-L370`,
`DOCUMENTS` `:L372-L378`, `TEMPLATES` `:L380-L385`, `DOCUMENT_PERMISSIONS` `:L387-L391` and `TEMPLATE_PERMISSIONS` `:L393-L397`.

The specification places document and user data in both stores. The committed code matches that placement for documents only, because
`services/document_service.py` reads and writes a Firestore `documents` collection. The user contracts here are contract-only. No committed
module persists a user, `api/auth.py:L22` imports the `UserService` that would, and that module does not exist.

`UserBase`, `UserCreate`, `UserUpdate` and `User` shape request and response bodies and nothing else. Templates, document permissions and
template permissions have no model here, and no object-relational mapping (ORM) model exists either.

Two field names also differ. The design declares `last_modified` at
`documentation/Technical Specifications.md:L335` and `:L377`, and `display_name` at
`documentation/Technical Specifications.md:L353` and `:L368`. The committed code calls them
`updated_at` at `document.py:L65`, and `username` at `user.py:L27` plus `full_name` at
`user.py:L28`. See the [architecture overview](../../../docs/architecture-overview.md) for the
tier map and the [package README](../README.md) for the composition root.

## Dependencies

**Internal.** The package imports no first-party module, so every internal relationship below is inbound.

| Module | Locator | Resolves | Symbols |
| --- | --- | --- | --- |
| `app.schema.template` | `app/api/templates.py:L17` | **No.** No file exists at `backend/app/schema/template.py`. | `Template`, `TemplateCreate`, `TemplateUpdate` |
| `app/api/auth.py` | `:L21` | Yes | `User`, `UserCreate` |
| `app/api/documents.py` | `:L17`, `:L20` | Yes | `Document`, `DocumentCreate`, `DocumentUpdate`, and `User` |
| `app/api/templates.py` | `:L20` | Yes | `User` |
| `app/api/users.py` | `:L13` | Yes | `User`, `UserUpdate` |
| `app/services/document_service.py` | `:L15` | Yes | `Document`, `DocumentCreate`, `DocumentUpdate` |
| `app/services/collaboration_service.py` | `:L17` | Yes | `Document` |
| `app/services/export_service.py` | `:L15` | Yes | `Document` |

**External.** No Python dependency manifest is committed anywhere, so the floor below is inferred from a code fact.

| Package | Inferred floor | Establishing evidence |
| --- | --- | --- |
| `pydantic` | 1.x only | `orm_mode = True` at `user.py:L81` is the Pydantic 1.x spelling of the key. Pydantic 2 renamed it to `from_attributes`. |

`typing` at `document.py:L13` and `user.py:L14` and `datetime` at `document.py:L14` and `user.py:L15` ship with Python, so
neither is a third-party dependency. The [data model reference](../../../docs/data-model.md) sets these contracts beside their client-side counterparts.

## Configuration

Neither module reads a setting or an environment variable. Two surfaces still shape validation, and both are declared inside the models themselves, so
the table records the verified negatives alongside them.

| Configuration input | Read by this package | Status |
| --- | --- | --- |
| `Settings` fields from `app/core/config.py:L20` | No. Neither module imports `app.core.config` | DECLARED, unread by this package |
| Environment variables | No. Neither `os.environ` nor `os.getenv` appears in either module | Neither declared nor read |
| Pydantic model config | Yes, one. `class Config` at `user.py:L74` sets `orm_mode = True` at `:L81` | DECLARED, in `user.py` only |
| Field-level constraints through `Field()` | No. No `Field(` call appears in either module, so no length, range or pattern rule is declared | Neither declared nor read |
| Field defaults | Yes, eight, and every one of them is `None`: `document.py:L28`, `:L49`, `:L50` and `user.py:L28`, `:L51`, `:L52`, `:L53`, `:L54` | DECLARED |

The last three rows carry the whole surface. `orm_mode` is what pins the package to Pydantic 1.x, which the Dependencies table above records. The eight
`None` defaults are what let a create payload validate without `owner_id`. No `Field()` rule appears either, which is why no string in either module has
a maximum length. For the settings the rest of the backend expects, see [onboarding](../../../docs/onboarding.md).

## Data Flows

Two paths cross the package, carrying the same models in opposite directions.

Write path. A router parses a JavaScript Object Notation (JSON) request body into `DocumentCreate` or `UserCreate`, and FastAPI validates it against
the declared fields before the handler runs. `app/services/document_service.py:L70` then calls `document.dict()` to flatten the model, adds
`user_id` at `:L71` and `id` at `:L72`, and writes the mapping to Firestore at `:L73`. The path breaks at `:L76`, where `Document(**doc_data)`
fails validation because the assembled mapping carries no `created_at` and no `updated_at`, both of which `document.py:L64-L65` declares as
required.

Read path. A service reads a Firestore mapping and constructs `Document` from it at `app/services/document_service.py:L112` and `:L157`. A router
returns a value annotated `-> Document` or `-> User`, and FastAPI serializes the model back to JSON. `orm_mode = True` at `user.py:L81` is what
would let `User` be built from an object's attributes instead of a mapping, and no code path builds a `User` that way.

## Design Patterns

Schema at the boundary. Every model here validates or serializes at the HTTP edge. None holds business logic, opens a database connection or calls a
service.

The base, create, update and read family. Each record declares a shared base, a create payload, a patch payload and a read response. The user set
sits at `user.py:L17`, `:L30`, `:L40` and `:L56`, and the document set at `document.py:L16`, `:L30`, `:L40` and `:L52`.

Attribute-based construction on the read model. `orm_mode` at `user.py:L74-L81` permits `User` to be populated from an object rather than a
mapping.

Optional-field patch semantics. `DocumentUpdate` at `document.py:L40-L50` and `UserUpdate` at `user.py:L40-L54` declare
every field as `Optional[str] = None`. That pairs with `document.dict(exclude_unset=True)` at
`app/services/document_service.py:L152`, so an untouched field is omitted from the write rather than sent as null.

The family pattern breaks on both patch payloads. `DocumentUpdate` at `document.py:L40` and `UserUpdate` at
`user.py:L40` extend `BaseModel` rather than their family base.

## Known Limitations

No artifact keeps this package and its client-side counterpart in agreement. The repository commits no OpenAPI document, generates no client and
ships no shared schema package spanning Python and TypeScript, so engineers maintain both sides by hand. That mechanism produced every field
divergence below.

The ownership field holds four positions, and this README names none of them canonical.

| Position | Field | Evidence |
| --- | --- | --- |
| Pydantic write and read contract | `owner_id`, optional with a default of `None` | `document.py:L28` |
| Pydantic version contract | `user_id` | `document.py:L85` |
| Service, written then compared | `user_id` | `app/services/document_service.py:L71`, `:L108`, `:L148`, `:L184` |
| Declared intent | `owner_id` | `documentation/Technical Specifications.md:L333`, `:L375`, `:L383` |

Because `owner_id` is optional with a default at `document.py:L28`, a document validates without the field that
authorization depends on. The [data model reference](../../../docs/data-model.md) consolidates all four positions, and
the [decision log](../../../docs/decision-log.md) records at decision row 7 why this documentation names none of
them canonical.

- **Three router sites read a field the read model never declares.** `Document` inherits `owner_id` and declares no
  `user_id`, yet `app/api/documents.py:L94`, `:L126` and `:L154` each read `.user_id` on a `Document`.
- **`created_at` and `updated_at` are required and no service writes either.** `document.py:L64-L65` declares both as
  required `datetime` fields, while `app/services/document_service.py:L70-L73` assembles `doc_data` from `title`,
  `content`, `owner_id`, `user_id` and `id` only. `Document(**doc_data)` at `:L76` fails validation on both fields.
- **`DocumentUpdate` shares no field definition with the create path.** A field added to `DocumentBase` at
  `document.py:L16-L28` reaches `DocumentCreate` and `Document` and never reaches `DocumentUpdate` at `:L40`.
- **`DocumentCreate` adds nothing.** The body is `pass` at `document.py:L38`, so the create payload inherits the
  optional `owner_id` and accepts a client-supplied owner on the request body.
- **No template model exists.** `app/api/templates.py:L17` imports `Template`, `TemplateCreate` and `TemplateUpdate` from
  `app.schema.template`, and `backend/app/schema/` holds only `document.py` and `user.py`.
- **`orm_mode` pins the package to Pydantic 1.x.** `user.py:L74-L81` sets `orm_mode = True`, which Pydantic 2 renamed to `from_attributes`. Under Pydantic 2 the old key raises a `UserWarning` and is then ignored, so attribute-based
  construction stops working while the import itself still succeeds.
- **The read model declares no field for the password hash.** `app/api/auth.py:L134` computes
  `pwd_context.hash(user.password)` and `:L135` passes the result on, while `User` at `user.py:L56-L72` declares no field to carry it. `UserCreate.password` at `user.py:L38` does exist, so the read at `auth.py:L134` resolves correctly.
- **`is_active` and `is_superuser` are declared and never read.** `user.py:L71` and `:L72` declare both on the read
  model, and no code path reads either one.
- **`updated_at` has no counterpart in the client-side user contract.** `user.py:L70` declares it on `User`. That model
  also declares neither `name` nor `avatar`, and the client reads both.
- **Both modules import `List` and never use it.** `document.py:L13` and `user.py:L14` each import `List` beside
  `Optional`, and `List` appears exactly once per file, in that import.
- **`DocumentVersion` has no importer.** `document.py:L67` defines the model, and a search for the name across every
  Python module in the repository returns that definition and nothing else.

The [troubleshooting register](../../../docs/troubleshooting.md) carries each defect above in repository-wide order.

## Usage Examples

Both modules import cleanly, and only three of the fifteen modules under `backend/app/` do. Run the check from the `backend/` directory.

```bash
python -c "import app.schema.document, app.schema.user
print('both modules imported')"
```

Neither module imports the `settings` singleton that `app/core/config.py` never defines, which is why both resolve. Under Pydantic 2 the `user.py`
import also emits a `UserWarning` naming `orm_mode` and still succeeds. Construct each payload against its declared fields, and every keyword
argument below names a field one of the two modules declares.

```python
from app.schema.document import DocumentCreate, DocumentUpdate
from app.schema.user import UserCreate, UserUpdate
# owner_id is optional at document.py:L28, so create validates without it.
new_document = DocumentCreate(title="Q4 report", content="Opening paragraph.")
patch = DocumentUpdate(title="Q4 report, final")     # every field is optional
patch.dict(exclude_unset=True)                       # {'title': 'Q4 report, final'}
# password is declared at user.py:L38
new_user = UserCreate(email="dev@example.com", username="dev", password="Passw0rd@1")
profile_patch = UserUpdate(full_name="Dev Example")
```

Building the read model from what the service assembles fails instead.

```python
from app.schema.document import Document, DocumentCreate
# app/services/document_service.py:L70-L73 assembles exactly this mapping.
doc_data = DocumentCreate(title="Q4 report", content="Opening paragraph.").dict()
doc_data["user_id"] = "user-1"
doc_data["id"] = "doc-1"
Document(**doc_data)  # ValidationError: created_at and updated_at are required
```

That block cannot succeed, because `document.py:L64-L65` requires `created_at` and `updated_at` while the assembled
mapping carries neither. Every create request runs the same construction at `app/services/document_service.py:L76`.
