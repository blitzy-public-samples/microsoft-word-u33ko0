# backend/app/schema

*Every `file:Lnn` locator below numbers the file as it stands at current `HEAD`, using physical line numbering.*

## Purpose

The package declares the Pydantic models that validate request bodies and shape response payloads at the HyperText
Transfer Protocol (HTTP) boundary. `document.py` declares five models for documents and document versions, and `user.py`
declares four models for users plus one nested configuration class. Documents and users each follow a create, read,
update and delete (CRUD) model family, so separate classes carry the create payload, the patch payload and the read
response. `DocumentVersion` is the exception: it has one model and no create or update variant, because no handler and no
service writes a version. No module here reaches a database, reads configuration or holds state. The application programming interface (API) routers under
`app/api/` and the services under `app/services/` import from this package rather than the reverse.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `DocumentBase` | Pydantic model | `document.py:L57` | Shared document fields: `title: str` at L66, `content: str` at L67 and `owner_id: Optional[str] = None` at L68. |
| `DocumentCreate` | Pydantic model | `document.py:L70` | Create payload. The body is `pass` at L82, so the class inherits all three `DocumentBase` fields and adds none. |
| `DocumentUpdate` | Pydantic model | `document.py:L84` | Patch payload. Extends `BaseModel` and declares `title` at L95 and `content` at L96, both `Optional[str] = None`. |
| `Document` | Pydantic model | `document.py:L98` | Read response. Extends `DocumentBase` and adds `id: str` at L112, `created_at: datetime` at L113 and `updated_at: datetime` at L114. |
| `DocumentVersion` | Pydantic model | `document.py:L116` | Version record. Extends `BaseModel` with `id` at L133, `document_id` at L134, `content` at L135, `created_at` at L136 and `user_id` at L137. |
| `UserBase` | Pydantic model | `user.py:L71` | Shared user fields: `email: str` at L80, `username: str` at L81 and `full_name: Optional[str] = None` at L82. |
| `UserCreate` | Pydantic model | `user.py:L84` | Registration payload. Extends `UserBase` and adds `password: str` at L94. |
| `UserUpdate` | Pydantic model | `user.py:L96` | Patch payload. Extends `BaseModel` with `email` at L109, `username` at L110, `full_name` at L111 and `password` at L112, all `Optional[str] = None`. |
| `User` | Pydantic model | `user.py:L114` | Read response. Extends `UserBase` and adds `id` at L169, `created_at` at L170, `updated_at` at L171, `is_active: bool` at L172 and `is_superuser: bool` at L173. |
| `Config` | Nested configuration class | `user.py:L175` | Sets `orm_mode = True` at L177 on `User` alone. No document model declares the key. |

## Architecture Fit

Nine `app.schema.*` import statements reach this package from seven modules, and eight resolve. The importers sit at
`app/api/auth.py:L85`, `app/api/documents.py:L49` and `:L52`, `app/api/templates.py:L75` and `:L78`, `app/api/users.py:L26`,
`app/services/collaboration_service.py:L38`, `app/services/document_service.py:L60` and
`app/services/export_service.py:L60`. The single failure is `app/api/templates.py:L75`, which imports `Template`,
`TemplateCreate` and `TemplateUpdate` from `app.schema.template`, and no file exists at
`backend/app/schema/template.py`. The package serves the router and service tiers at once, and both depend on it.

Declared intent describes a wider data layer. The `## DATABASE DESIGN` heading at
`documentation/Technical Specifications.md:L315` sits under `# SYSTEM DESIGN` at `:L300`. At `:L317` it pairs Google
Cloud Firestore, a NoSQL store of schemaless records, with Google Cloud SQL, a relational Structured Query Language
(SQL) database. Its `### Google Cloud Firestore (NoSQL)` heading at `:L319` lists Documents `:L331-L336`, Versions
`:L338-L341`, Comments `:L343-L348` and Users `:L350-L354`. Its `### Google Cloud SQL (Relational)` heading at `:L356`
adds `USERS` `:L365-L370`, `DOCUMENTS` `:L372-L378`, `TEMPLATES` `:L380-L385`, `DOCUMENT_PERMISSIONS` `:L387-L391` and
`TEMPLATE_PERMISSIONS` `:L393-L397`.

The specification places document and user data in both stores, and the committed code matches that placement for
documents and users only. Templates, document permissions and template permissions have no model here, and no
object-relational mapping (ORM) model exists either. Two field names also differ. The design declares `last_modified` at
`documentation/Technical Specifications.md:L335` and `:L377`, and `display_name` at
`documentation/Technical Specifications.md:L353` and `:L368`. The committed code calls them `updated_at` at
`document.py:L114`, and `username` at `user.py:L81` plus `full_name` at `user.py:L82`.

Two field names also differ. The design declares `last_modified` at `:L335` and `:L377` and `display_name` at `:L353`
and `:L368`. The committed code calls them `updated_at` at `document.py:L114`, and `username` at `user.py:L81` plus
`full_name` at `user.py:L82`. See the [architecture overview](../../../docs/architecture-overview.md) for the tier map
and the [package README](../README.md) for the composition root.

## Dependencies

**Internal.** The package imports no first-party module, so every internal relationship below is inbound.

| Module | Locator | Resolves | Symbols |
| --- | --- | --- | --- |
| `app.schema.template` | `app/api/templates.py:L75` | **No.** No file exists at `backend/app/schema/template.py`. | `Template`, `TemplateCreate`, `TemplateUpdate` |
| `app/api/auth.py` | `:L85` | Yes | `User`, `UserCreate` |
| `app/api/documents.py` | `:L49`, `:L52` | Yes | `Document`, `DocumentCreate`, `DocumentUpdate`, and `User` |
| `app/api/templates.py` | `:L78` | Yes | `User` |
| `app/api/users.py` | `:L26` | Yes | `User`, `UserUpdate` |
| `app/services/document_service.py` | `:L60` | Yes | `Document`, `DocumentCreate`, `DocumentUpdate` |
| `app/services/collaboration_service.py` | `:L38` | Yes | `Document` |
| `app/services/export_service.py` | `:L60` | Yes | `Document` |

**External.** No Python dependency manifest is committed anywhere, so the floor below is inferred from a code fact.

| Package | Inferred floor | Establishing evidence |
| --- | --- | --- |
| `pydantic` | 1.x only | `orm_mode = True` at `user.py:L177` is the Pydantic 1.x spelling of the key. Pydantic 2 renamed it to `from_attributes`. |

`typing` at `document.py:L54` and `user.py:L68` and `datetime` at `document.py:L55` and `user.py:L69` ship with Python, so
neither is a third-party dependency. The [data model reference](../../../docs/data-model.md) sets these contracts beside their client-side counterparts.

## Configuration

Neither module reads a setting, an environment variable or a constant, so the package has no configuration surface. For
the settings the rest of the backend expects, see [onboarding](../../../docs/onboarding.md).

## Data Flows

Two paths cross the package, carrying the same models in opposite directions.

Write path. A router parses a JavaScript Object Notation (JSON) request body into `DocumentCreate` or `UserCreate`, and
FastAPI validates it against the declared fields before the handler runs. `app/services/document_service.py:L117` then
calls `document.dict()` to flatten the model, adds `user_id` at `:L118` and `id` at `:L119`, and writes the mapping to
Firestore at `:L120`. The path breaks at `:L123`, where `Document(**doc_data)` fails validation because the assembled
mapping carries no `created_at` and no `updated_at`, both of which `document.py:L113-L114` declares as required.

Read path. A service reads a Firestore mapping and constructs `Document` from it at
`app/services/document_service.py:L181` and `:L252`. A router returns a value annotated `-> Document` or `-> User`, and
FastAPI serializes the model back to JSON. `orm_mode = True` at `user.py:L177` is what would let `User` be built from an
object's attributes instead of a mapping, and no code path builds a `User` that way.

## Design Patterns

Schema at the boundary. Every model here validates or serializes at the HTTP edge. None holds business logic, opens a
database connection or calls a service.

The base, create, update and read family. Each record declares a shared base, a create payload, a patch payload and a
read response. The user set sits at `user.py:L71`, `:L84`, `:L96` and `:L114`, and the document set at `document.py:L57`,
`:L70`, `:L84` and `:L98`.

Attribute-based construction on the read model. `orm_mode` at `user.py:L175-L177` permits `User` to be populated from an
object rather than a mapping.

Optional-field patch semantics. `DocumentUpdate` at `document.py:L84-L96` and `UserUpdate` at `user.py:L96-L112` declare
every field as `Optional[str] = None`. That pairs with `document.dict(exclude_unset=True)` at
`app/services/document_service.py:L247`, so an untouched field is omitted from the write rather than sent as null.

The family pattern breaks on both patch payloads. `DocumentUpdate` at `document.py:L84` and `UserUpdate` at
`user.py:L96` extend `BaseModel` rather than their family base.

## Known Limitations

No artifact keeps this package and its client-side counterpart in agreement. The repository commits no OpenAPI document,
generates no client and ships no shared schema package spanning Python and TypeScript, so engineers maintain both sides
by hand. That mechanism produced every field divergence below.

The ownership field holds four positions, and this README names none of them canonical.

| Position | Field | Evidence |
| --- | --- | --- |
| Pydantic write and read contract | `owner_id`, optional with a default of `None` | `document.py:L68` |
| Pydantic version contract | `user_id` | `document.py:L137` |
| Service, written then compared | `user_id` | `app/services/document_service.py:L118`, `:L177`, `:L243`, `:L282` |
| Declared intent | `owner_id` | `documentation/Technical Specifications.md:L333`, `:L375`, `:L383` |

Because `owner_id` is optional with a default at `document.py:L68`, a document validates without the field that
authorization depends on. The [data model reference](../../../docs/data-model.md) consolidates all four positions, and
the planned, not yet committed [decision log](../../../docs/decision-log.md) will record the choice between them.

- **Three router sites read a field the read model never declares.** `Document` inherits `owner_id` and declares no
  `user_id`, yet `app/api/documents.py:L187`, `:L235` and `:L282` each read `.user_id` on a `Document`.
- **`created_at` and `updated_at` are required and no service writes either.** `document.py:L113-L114` declares both as
  required `datetime` fields, while `app/services/document_service.py:L117-L120` assembles `doc_data` from `title`,
  `content`, `owner_id`, `user_id` and `id` only. `Document(**doc_data)` at `:L123` fails validation on both fields.
- **`DocumentUpdate` shares no field definition with the create path.** A field added to `DocumentBase` at
  `document.py:L57-L68` reaches `DocumentCreate` and `Document` and never reaches `DocumentUpdate` at `:L84`.
- **`DocumentCreate` adds nothing.** The body is `pass` at `document.py:L82`, so the create payload inherits the
  optional `owner_id` and accepts a client-supplied owner on the request body.
- **No template model exists.** `app/api/templates.py:L75` imports `Template`, `TemplateCreate` and `TemplateUpdate` from
  `app.schema.template`, and `backend/app/schema/` holds only `document.py` and `user.py`.
- **`orm_mode` pins the package to Pydantic 1.x.** `user.py:L175-L177` sets `orm_mode = True`, which Pydantic 2 renamed to `from_attributes`. Under Pydantic 2 the old key raises a `UserWarning` and is then ignored, so attribute-based
  construction stops working while the import itself still succeeds.
- **The read model declares no field for the password hash.** `app/api/auth.py:L326` computes
  `pwd_context.hash(user.password)` and `:L327` passes the result on, while `User` at `user.py:L114-L173` declares no field to carry it. `UserCreate.password` at `user.py:L94` does exist, so the read at `auth.py:L326` resolves correctly.
- **`is_active` and `is_superuser` are declared and never read.** `user.py:L172` and `:L173` declare both on the read
  model, and no code path reads either one.
- **`updated_at` has no counterpart in the client-side user contract.** `user.py:L171` declares it on `User`. That model
  also declares neither `name` nor `avatar`, and the client reads both.
- **Both modules import `List` and never use it.** `document.py:L54` and `user.py:L68` each import `List` beside
  `Optional`, and `List` appears exactly once per file, in that import.
- **`DocumentVersion` has no importer.** `document.py:L116` defines the model, and a search for the name across every
  Python module in the repository returns that definition and nothing else.

The [troubleshooting register](../../../docs/troubleshooting.md) carries each defect above in repository-wide order.

## Usage Examples

Both modules import cleanly, and only three of the fifteen modules under `backend/app/` do. Run the check from the
`backend/` directory.

```bash
python -c "import app.schema.document, app.schema.user; print('both modules imported')"
```

Neither module imports the `settings` singleton that `app/core/config.py` never defines, which is why both resolve. Under
Pydantic 2 the `user.py` import also emits a `UserWarning` naming `orm_mode` and still succeeds. Construct each payload
against its declared fields, and every keyword argument below names a field one of the two modules declares.

```python
from app.schema.document import DocumentCreate, DocumentUpdate
from app.schema.user import UserCreate, UserUpdate
# owner_id is optional at document.py:L68, so the create payload validates without it.
new_document = DocumentCreate(title="Q4 report", content="Opening paragraph.")
patch = DocumentUpdate(title="Q4 report, final")     # every field is optional
patch.dict(exclude_unset=True)                       # {'title': 'Q4 report, final'}
new_user = UserCreate(email="dev@example.com", username="dev", password="Passw0rd@1")  # password at user.py:L94
profile_patch = UserUpdate(full_name="Dev Example")
```

Building the read model from what the service assembles fails instead.

```python
from app.schema.document import Document, DocumentCreate
# app/services/document_service.py:L117-L120 assembles exactly this mapping.
doc_data = DocumentCreate(title="Q4 report", content="Opening paragraph.").dict()
doc_data["user_id"] = "user-1"
doc_data["id"] = "doc-1"
Document(**doc_data)  # ValidationError: created_at and updated_at are required
```

That block cannot succeed, because `document.py:L113-L114` requires `created_at` and `updated_at` while the assembled
mapping carries neither. Every create request runs the same construction at `app/services/document_service.py:L123`.
