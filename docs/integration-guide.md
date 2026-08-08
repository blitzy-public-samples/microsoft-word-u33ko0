# Integration Guide

**No Firestore, upload, or signed-URL call executes as committed.** The source contains these calls,
but import, configuration, caller, and credential-signing prerequisites fail first.

Four external systems appear in this repository. Google Cloud Firestore has reads and writes written
against it. Google Cloud Storage has export uploads and download-link signing written against it.
Google Cloud Pub/Sub has a full set of publish and subscribe calls whose holding class nothing
constructs. Redis has a broker Uniform Resource Locator (URL) in configuration and no service anywhere
in the committed infrastructure.

Every integration below carries one label, and each label arrives with the evidence that earns it,
including the named prerequisite that stops it. A reader who knows what stands between the code and a
working call can plan an afternoon's work. A reader given four evenly-toned descriptions cannot.

## How to read this guide

Every factual claim below carries a locator in the form `path:Lnn`, and most locators also name the
symbol at that line. Read the symbol name as the durable half of the citation. Line numbers move
whenever anyone edits a file above them, and symbol names do not.

Three conventions govern the locators, matching [troubleshooting.md](troubleshooting.md),
[architecture-overview.md](architecture-overview.md) and [data-model.md](data-model.md) so all four
documents agree:

- Locators point at the committed state at the current branch head, which includes the inline
  documentation added to 44 source files. A locator matches what you see when you open the file
  today, not what an earlier revision held.
- Line numbers are physical. No source file in this repository ends with a newline, so `wc -l`
  reports one line fewer than each file contains.
- A range such as `L154-L164` covers every line in the span, inclusive.

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
name plus line, because all three files use unnumbered headings only.
`documentation/Technical Specifications.md` holds five level-one headings: `L3` INTRODUCTION, `L125`
SYSTEM ARCHITECTURE, `L300` SYSTEM DESIGN, `L523` TECHNOLOGY STACK and `L620` SECURITY
CONSIDERATIONS. A numbered section citation anywhere in this documentation set refers to the
generated Technical Specification, a separate document, and the text says so when it does.

Where this engagement made a judgement, [decision-log.md](decision-log.md) carries the argument. No
rationale lives in this file.

## Integration inventory

Four integrations, four labels, and no overlap between them. No integration earns the strongest label.

| Integration | Client library | Reachability | Entry point | Configuration it reads |
| ------------- | ---------------- | -------------- | ------------- | ------------------------ |
| Google Cloud Firestore | `google-cloud-firestore` | **WIRED, BLOCKED AT IMPORT** | `DocumentService`, constructed by all five document handlers at `backend/app/api/documents.py:L107`, `:L141`, `:L182`, `:L230` and `:L277` | `GOOGLE_CLOUD_PROJECT`, declared at `backend/app/core/config.py:L116` |
| Google Cloud Storage | `google-cloud-storage` | **NOT REACHABLE** | `ExportService.export_to_pdf` at `backend/app/services/export_service.py:L87` and `export_to_docx` at `:L168`, plus the export task at `backend/app/tasks/background_tasks.py:L141-L146`. No handler calls either method, and no producer enqueues the task | `STORAGE_BUCKET_NAME`, `SIGNED_URL_EXPIRATION`, `EXPORT_BUCKET_NAME` and `DOCUMENT_BUCKET_NAME`, none of them declared |
| Google Cloud Pub/Sub | `google-cloud-pubsub` | **SCAFFOLDED ONLY** | `CollaborationService.connect` at `backend/app/services/collaboration_service.py:L75` and `broadcast_change` at `:L218`, and no route constructs that class | `PROJECT_ID`, not declared |
| Redis, as the Celery broker | `celery` | **ABSENT** | `celery_app` at `backend/app/tasks/background_tasks.py:L98`, carrying three tasks | `REDIS_URL`, declared at `backend/app/core/config.py:L119` |

Four labels carry one fixed meaning in this guide and in the rest of the documentation set.

| Label | Meaning |
| ------- | --------- |
| **WIRED, BLOCKED AT IMPORT** | Committed code constructs the client library and issues complete, well-formed calls, and a caller exists, and the module holding it cannot import, so no call runs today |
| **NOT REACHABLE** | Committed code writes the calls, and more than one independent barrier stands between a request and the external system. The entry-point column names them |
| **SCAFFOLDED ONLY** | Committed code constructs the client library and writes the calls, and nothing in the application constructs the class holding them, so no call site can run |
| **ABSENT** | Configuration names the integration and code reads that value, and no committed infrastructure provisions the service |

No label in this table means a call reaches Google Cloud today. One import blocks every one of them.
`app.core.config` declares the `Settings` class and a `get_settings` factory and never creates a
module-level `settings` instance, so any module importing that name raises `ImportError` before a
client is built.

Six modules under `backend/app/` import `settings`, and each one touches an external system either
by constructing a client or by reaching one through a service. Four construct a client directly:

| Module | `settings` import | Client it constructs |
| -------- | ------------------- | ---------------------- |
| `backend/app/db/firestore.py` | `:L36` | Firestore `Client` at `:L40` |
| `backend/app/db/sql.py` | `:L14` | SQLAlchemy `engine` at `:L16`, against `DATABASE_URL` |
| `backend/app/services/export_service.py` | `:L61` | Cloud Storage `Client` at `:L83` |
| `backend/app/tasks/background_tasks.py` | `:L92` | `Celery` on `REDIS_URL` at `:L98`, plus Cloud Storage clients at `:L132` and `:L277` |

The other two reach an external system without constructing a client of their own.
`backend/app/services/collaboration_service.py:L39` imports `settings` and builds Pub/Sub publisher
and subscriber clients at `:L69-L70`, and it reads `settings.PROJECT_ID`, a field `Settings` never
declares. `backend/app/services/document_service.py:L60` imports `settings` and reaches Firestore
through the shared client it binds at `:L70`, so it issues external calls without opening a
connection.

Three further modules import `settings` and reach no external system: `backend/app/main.py:L20`,
`backend/app/api/auth.py:L81` and, through the factory rather than the instance,
`backend/app/core/security.py:L43`. Everything below describes the call the code declares.

- Firestore is the one external system an HTTP handler calls. Five document handlers construct
  `DocumentService`, and each of its four methods issues a Firestore call. No request reaches a
  handler today, because importing the application raises `ImportError` on the absent `settings` name.
- Cloud Storage is reached only from export code. Export objects are the only bytes the repository
  writes to any bucket, no route uploads a document or an image, and no handler calls either export
  method.

### The integration map

No edge in the map below carries traffic today, and the diagram is a map of the calls the committed
code writes rather than a map of live request flow. Two blockers sit in front of every edge.
`backend/app/main.py:L16` reaches `backend/app/api/auth.py:L81`, which asks `app.core.config` for a
`settings` name that module never binds, so importing the application raises `ImportError` and no
route is ever registered. Six of the fifteen settings the code reads are declared nowhere, and no
committed file supplies a value for any of them. Every edge below is dashed, because no seam is
complete. Each edge carries a seam key, and the seam table under the diagram names the call the code
writes and what stands between that call and the external system, including the barriers that outlast
repairing the import chain and the undeclared settings.

```mermaid
graph TD
    accTitle: The integration map, annotated with reachability
    accDescr: Every edge is dashed because no seam carries traffic today. Each edge carries a seam key, and the seam table below the diagram names the calls the code writes and the barriers in front of them.
    BROWSER["Browser client<br/>frontend/src/"]
    SOCK["socket.io-client<br/>collaboration.ts<br/>:L77, io() with<br/>no URL"]
    APP["FastAPI application<br/>main.py:L24"]
    ROUTERS["4 routers,<br/>14 handlers<br/>main.py:L125-L128<br/>no prefix"]
    COLSVC["CollaborationService<br/>collaboration_service<br/>.py:L41, constructed<br/>by no route"]
    DOCSVC["DocumentService<br/>document_service<br/>.py:L62"]
    TASKS["3 Celery tasks<br/>background_tasks.py<br/>:L101, :L152, :L287"]
    EXPSVC["ExportService<br/>export_service<br/>.py:L63"]

    FS[("Google Cloud<br/>Firestore<br/>WIRED, BLOCKED<br/>AT IMPORT")]
    GCS[("Google Cloud<br/>Storage<br/>NOT REACHABLE")]
    PS["Google Cloud<br/>Pub/Sub<br/>SCAFFOLDED ONLY"]
    REDIS[("Redis broker<br/>ABSENT")]

    BROWSER -.->|"S1"| APP
    BROWSER -.->|"S2"| SOCK
    APP -.->|"S3"| ROUTERS
    SOCK -.->|"S4"| COLSVC
    COLSVC -.->|"S5"| PS
    ROUTERS -.->|"S6"| DOCSVC
    ROUTERS -.->|"S7"| TASKS
    DOCSVC -.->|"S8"| FS
    TASKS -.->|"S9"| FS
    TASKS -.->|"S10"| EXPSVC
    TASKS -.->|"S11"| REDIS
    TASKS -.->|"S12"| GCS
    EXPSVC -.->|"S13"| GCS

%% Every edge is dashed, because no seam is complete. Each edge carries a seam key, and the seam
%% table below names the call the code writes and the barriers in front of it, including the ones
%% that outlast repairing the import chain and the undeclared settings.
```

Thirteen seams carry a key in the diagram above. One further fact has no edge, because it is the
absence of a call rather than a call: no route anywhere constructs `CollaborationService`, which the
`COLSVC` node states in place of an edge.

| Seam | Edge | What the committed code writes | What stands in the way |
| ------ | ------ | -------------------------------- | ------------------------ |
| S1 | Browser to FastAPI application | REST over HTTP | Nothing completes. The application cannot import, and past that repair the client still matches no route, because `frontend/src/services/api.ts:L142` throws inside the request interceptor and every document call carries a `/documents` prefix no route declares |
| S2 | Browser to socket.io-client | `io()` at `frontend/src/services/collaboration.ts:L77` | No module imports `collaboration.ts`, so nothing constructs the client class, and `io()` receives no URL |
| S3 | Application to the four routers | `backend/app/main.py:L125-L128` would register four routers | `:L16-L19` import `auth_router`, `documents_router`, `users_router` and `templates_router`, and all four modules export the bare name `router` |
| S4 | socket.io-client to CollaborationService | a Socket.IO connection from the browser | No route joins Socket.IO to the FastAPI WebSocket signature the service declares |
| S5 | CollaborationService to Pub/Sub | subscribe at `backend/app/services/collaboration_service.py:L165`, publish at `:L248` | Neither runs, because nothing constructs the class. `settings.PROJECT_ID` is undeclared at `:L120`, `:L121`, `:L209` and `:L245` |
| S6 | Routers to DocumentService | constructed at `backend/app/api/documents.py:L107`, `:L141`, `:L182`, `:L230` and `:L277` | Every call breaks its signature. `:L108` hands a `User` where `user_id: str` is declared, `:L183`, `:L231` and `:L278` pass one argument to a two-parameter `get_document`, and `:L142` calls `get_documents`, which the class never defines |
| S7 | Routers to the Celery tasks | nothing | No producer. Zero `.delay()` and zero `.apply_async()` call sites exist anywhere |
| S8 | DocumentService to Firestore | set at `backend/app/services/document_service.py:L118`, get at `:L169`, update at `:L246`, delete at `:L284`, all written in full | Each read then builds `Document(**...)` against `created_at` and `updated_at`, required at `backend/app/schema/document.py:L111-L112` and written by nothing |
| S9 | Celery tasks to Firestore | read at `backend/app/tasks/background_tasks.py:L267`, delete at `:L274`, update at `:L317` | No producer runs them |
| S10 | Celery tasks to ExportService | constructed at `backend/app/tasks/background_tasks.py:L131`, then calls `convert_document` at `:L138` | `ExportService` never defines `convert_document` |
| S11 | Celery tasks to the Redis broker | broker URL read at `backend/app/tasks/background_tasks.py:L98` | The URL resolves to no service. No committed infrastructure provisions a broker |
| S12 | Celery tasks to Cloud Storage | upload at `backend/app/tasks/background_tasks.py:L143`, signed URL at `:L146` | Unreachable behind S10, and the signing call passes no version argument, so the client default applies |
| S13 | ExportService to Cloud Storage | upload at `backend/app/services/export_service.py:L157`, V4 signing at `:L160-L164`, both written in full | No handler calls either export method |

## Google Cloud Firestore

**WIRED, BLOCKED AT IMPORT.** Firestore is the only external system a committed HTTP handler calls,
and no call runs today, because the module holding those calls cannot import. Five document handlers construct
`DocumentService` at `backend/app/api/documents.py:L107`, `:L141`, `:L182`, `:L230` and `:L277`, and
each of that class's four methods issues a Firestore call. Firestore also holds every record the
code writes, because the SQLAlchemy path stays declared and unused.
[data-model.md](data-model.md) covers the split.

Two independent access paths exist, and only one of them has a caller.

| Access path | Location | Callers |
| ------------- | ---------- | --------- |
| The adapter's four helpers | `backend/app/db/firestore.py:L42`, `:L70`, `:L92`, `:L110` | None. No module imports any of the four |
| `DocumentService`, calling the client directly | `backend/app/services/document_service.py:L62` | Five document handlers, plus the task module, which constructs the class three times, at `backend/app/tasks/background_tasks.py:L130`, `:L264` and `:L307`, and calls a method on only two of the three, at `:L135` and `:L310`. The instance built at `:L264` is never used |

### The adapter, and why nothing uses it

The adapter builds one client at module scope and exposes four synchronous helpers.
`backend/app/db/firestore.py:L39` resolves Application Default Credentials (ADC) through
`google.auth.default()`, and `:L40` constructs the client with
`Client(project=settings.GOOGLE_CLOUD_PROJECT)`. Both statements run at import time. The four
helpers follow: `get_document` at `:L42`, `create_document` at `:L70`, `update_document` at `:L92`
and `delete_document` at `:L110`.

No module imports any of the four. Three modules import the `db` client instead and call the
Firestore software development kit (SDK) directly: `backend/app/main.py:L21`,
`backend/app/services/document_service.py:L59` and `backend/app/tasks/background_tasks.py:L93`. The
adapter's four helpers therefore sit outside every execution path in the repository.

One annotation on the adapter contradicts the code beneath it. `get_document` declares `-> dict` at
`:L42` and returns `None` at `:L68` when the snapshot does not exist. A caller who trusts the
annotation and subscripts the result raises `TypeError` for a missing document.

None of the four helpers opens a transaction, sets a retry policy, sets a timeout, or catches an
exception. [../backend/app/db/README.md](../backend/app/db/README.md) carries the module detail.

### The service, and the shape of its calls

`DocumentService` holds the shared client at `backend/app/services/document_service.py:L70` and
issues **seven** remote Firestore operations across four methods. The count excludes
`collection()` and `document()`, which build a reference locally and send nothing, so
`:L114`, `:L168`, `:L234` and `:L273` are not remote operations.

| Method | Remote operations | Count | Locators |
|--------|-------------------|-------|----------|
| `create_document` at `:L72` | `set` | 1 | `:L118`, on the reference built at `:L114` |
| `get_document` at `:L123` | `get` | 1 | `:L169`, on the reference built at `:L168` |
| `update_document` at `:L183` | `get`, `update`, then `get` again | 3 | `:L235`, `:L246`, `:L249` |
| `delete_document` at `:L252` | `get`, then `delete` | 2 | `:L274`, `:L284` |

The update path reads, modifies, then reads again, which costs three Firestore operations for one
logical update. The first read at `:L235` supports the existence check at `:L237` and the ownership
comparison at `:L241`. The second read at `:L249` fetches the record the method returns, because
`update()` returns no snapshot.

Every method carries `async def` and every Firestore call inside runs synchronously and blocks. A
declared coroutine that never yields holds the event loop for the duration of each round trip. The
declared type and the runtime behaviour disagree, and the code, not the annotation, describes what
happens. [../backend/app/services/README.md](../backend/app/services/README.md) owns the service
detail.

### What the background tasks touch

Two of the three Celery tasks in `backend/app/tasks/background_tasks.py` reach Firestore, and
neither runs today, because no producer enqueues them. The
[Redis broker section](#redis-broker-for-celery) carries that evidence.

| Task | Firestore work | Locators |
| ------ | ---------------- | ---------- |
| `cleanup_expired_documents` at `:L152` | Queries `documents` on an expiry comparison, deletes the matching document, calls `.delete()` on a `document_permissions` query result, then deletes from `document_metadata` | `:L267`, `:L274`, `:L283`, `:L284` |
| `update_document_statistics` at `:L287` | Reads one document through `DocumentService.get_document`, then updates `documents` with a recomputed word and page count | `:L310`, `:L317` |

`process_document_export` reaches Firestore indirectly rather than through the `db` client, and the
call at `:L135` passes two arguments to a service method that accepts two, so the arity is correct
there. `update_document_statistics` passes one argument at `:L310` to the same two-argument method.

Two faults sit inside that work. `backend/app/tasks/background_tasks.py:L267` calls
`datetime.now()`, and `:L96` imports `timedelta` alone, so the name `datetime` is undefined and the
query raises `NameError` on first execution. `:L321` repeats the same call inside the statistics
update. Separately, `:L283` calls `.delete()` on the value `Query.get()` returns. That value is a
list of snapshots rather than a reference, so the call raises `AttributeError`.
[troubleshooting.md](troubleshooting.md) registers both under
[G3](troubleshooting.md#g3-undefined-names-that-raise-at-execution).

Three collections appear across the code. `documents` is the only one a service writes.
`document_permissions` at `:L283` and `document_metadata` at `:L284` appear in the retention task
alone, and no schema in either language models either of them.
[../backend/app/tasks/README.md](../backend/app/tasks/README.md) carries the task detail.

## Google Cloud Storage and version 4 signed URLs

**NOT REACHABLE.** Export objects are the only bytes this repository writes to any bucket. The
write-and-sign sequence in `ExportService` is written in full and in the right order, and more than
one independent barrier stands in front of it. Three barriers apply: no handler calls either export
method, no route uploads a document, and no route uploads an image. Read the label as a statement
about the shape of the call, not about a successful upload or a usable link. Three
prerequisites stand between the committed code and either outcome, and the two subsections after the
step table name each one.

Two code paths construct a Cloud Storage client. `backend/app/services/export_service.py:L83` builds
one per service instance, and `backend/app/tasks/background_tasks.py:L132` and `:L277` build one per
task invocation.

### The service path signs version 4 URLs

Both export methods are plain synchronous `def`, at `backend/app/services/export_service.py:L87` and
`:L168`. Each resolves a bucket, uploads a payload, signs a link, and returns the link.

| Step | `export_to_pdf` | `export_to_docx` |
| ------ | ----------------- | ------------------ |
| Resolve the bucket from `settings.STORAGE_BUCKET_NAME` | `:L154` | `:L228` |
| Target the object key | `:L155` | `:L229` |
| Upload the payload | `:L157` | `:L231` |
| Sign the link | `:L160-L164` | `:L234-L238` |
| Return the link | `:L166` | `:L240` |

Both signing calls pass `version="v4"`, at `:L161` and `:L235`, and both read the expiry from
`settings.SIGNED_URL_EXPIRATION`, at `:L162` and `:L236`. Both pass `method="GET"`, at `:L163` and
`:L237`.

The payloads are literal placeholder strings. `:L157` uploads `"PDF_CONTENT"` with content type
`application/pdf`, and `:L231` uploads `"DOCX_CONTENT"` with the Office Open XML content type. Both
Multipurpose Internet Mail Extensions (MIME) types are correct for the format each method names. A
browser receiving either object therefore treats eleven or twelve bytes of text as a document.

Conversion does not exist, and each method carries a `TODO` marker recording the gap, at `:L151`,
`:L156`, `:L225` and `:L230`.

No module under `backend/app/` calls either method. The only callers anywhere sit in the test suite,
at `backend/tests/test_services.py:L67` and `:L75`. Both pass the integer identifier `1`, bound at
`:L65` and `:L73`, where the signature declares a `Document`.

### What the upload and the signature each still need

Neither the upload nor the signature completes as committed. Three prerequisites are missing, and they
fail in this order inside `export_to_pdf`.

| Order | Statement | Locator | What it needs |
| ------- | ----------- | --------- | --------------- |
| 1 | `self.storage_client.bucket(settings.STORAGE_BUCKET_NAME)` | `export_service.py:L154` | A declared `STORAGE_BUCKET_NAME`. `Settings` declares nine fields at `backend/app/core/config.py:L111-L119` and this is not among them, so attribute access raises `AttributeError` before any network call |
| 2 | `blob.upload_from_string(...)` | `export_service.py:L157` | Credentials that authenticate and carry write permission on the bucket. `export_service.py:L83` builds `Client()` with no arguments, so the Cloud Storage client runs its own Application Default Credentials lookup, independent of the Firestore lookup at `backend/app/db/firestore.py:L39`, which is the repository's only explicit `default()` call. ADC consults several sources in turn, among them `GOOGLE_APPLICATION_CREDENTIALS`, a `gcloud` user credential in the well-known configuration file, and the metadata server on a Google Cloud instance. No committed file supplies any of them, so what this client resolves is a property of the host |
| 3 | `blob.generate_signed_url(version="v4", ...)` | `export_service.py:L160-L164` | Sign-capable credentials, and an expiry inside the version 4 limit |

Signing is the prerequisite most easily missed, because it needs more than authentication. A version 4
signature is computed locally, so the credentials must be able to sign bytes. Two credential shapes
satisfy that:

- **A service-account private key.** A key file referenced through `GOOGLE_APPLICATION_CREDENTIALS`.
  `backend/app/core/config.py:L117` declares that field as `Optional[str]` with no explicit default,
  which Pydantic 1.x treats as optional with a `None` default, so the contract never requires it.
  No committed `.env` file supplies it. `Config.env_file` at `:L123`
  names the file the repository does not commit.
- **An IAM `signBlob` grant.** Credentials with no private key, such as a metadata-server token on a
  Compute Engine or Cloud Run instance, can sign only by delegating to the IAM Credentials application
  programming interface (API). That path needs the `iam.serviceAccounts.signBlob` permission on the
  signing service account, granted through the Service Account Token Creator role, and the caller must
  pass the signer identity explicitly. Neither the code nor
  `infrastructure/terraform/main.tf` grants that permission or names a signer.

Credentials resolved from a user account through `gcloud auth application-default login` carry neither
a private key nor a signer identity, so `generate_signed_url` raises for a local developer even when
the upload at `export_service.py:L157` succeeds.

The expiry carries its own two constraints. `generate_signed_url` accepts an `int` of seconds, a
`datetime.timedelta`, or an absolute `datetime`, and `export_service.py:L162` passes
`settings.SIGNED_URL_EXPIRATION` with no conversion, so whatever type that field eventually holds is
the type the call receives. A version 4 signature also caps the lifetime at seven days, and a longer
expiry raises `ValueError` rather than returning a short-lived link. `Settings` declares no
`SIGNED_URL_EXPIRATION`, so no committed value can be checked against either constraint. The method
holds no `try` block, so both the `AttributeError` and the `ValueError` reach the caller unchanged, and
step 2 has already written the placeholder object by the time step 3 fails.

### The task path signs differently

`process_document_export` at `backend/app/tasks/background_tasks.py:L101` writes to Cloud Storage
without going through either export method. The task constructs `ExportService` at `:L131`, then
calls `export_service.convert_document(document, export_format)` at `:L138`. `ExportService` never
defines `convert_document`, so the task raises `AttributeError` at that line and reaches none of the
upload work below it, even if something enqueued the task.

The two paths sign links differently. `:L146` calls
`generate_signed_url(expiration=timedelta(hours=1))` with no `version` argument, while the service
passes `version="v4"` at `:L161` and `:L235`. A caller consuming both paths receives links signed
under two different schemes.

Three object-key layouts appear in the committed code, and no two of them agree.

| Path | Object key | Locators |
| ------ | ----------- | ---------- |
| `ExportService` | `exports/{document.id}.pdf` and `exports/{document.id}.docx` | `:L155`, `:L229` |
| `process_document_export` | `exports/{user_id}/{document_id}.{export_format}` | `:L142` |

The two writers disagree with each other. The service layout omits the owner and encodes the format
in the file extension. The task layout partitions by owner and takes the format from a
caller-supplied string that nothing validates. The same export therefore lands in two different
places depending on which path runs.

The third layout is the one that matters most, because it deletes rather than writes.
`backend/app/tasks/background_tasks.py:L279` builds `{user_id}/{doc_id}` and `:L280` calls
`blob.delete()` on it. That key matches neither writer, carrying no `exports/` prefix and no file
extension. The service path produces `exports/{document.id}.pdf` at `export_service.py:L155`, and the
task path produces `exports/{user_id}/{document_id}.{export_format}` at `background_tasks.py:L142`.
Neither shape can be named by the deletion key. The retention sweep would therefore reclaim nothing,
and it reads a third bucket name, `DOCUMENT_BUCKET_NAME`, which no other code path writes to. Three
layouts, three bucket settings, and no agreement between the writers and the deleter.

### Four settings fields, none of them declared

Cloud Storage code reads three bucket names and one expiry value, and `Settings` declares none of
the four.

| Field | Read at | Status |
| ------- | --------- | -------- |
| `STORAGE_BUCKET_NAME` | `export_service.py:L154`, `:L228` | Read but never declared |
| `SIGNED_URL_EXPIRATION` | `export_service.py:L162`, `:L236` | Read but never declared |
| `EXPORT_BUCKET_NAME` | `background_tasks.py:L141` | Read but never declared |
| `DOCUMENT_BUCKET_NAME` | `background_tasks.py:L278` | Read but never declared |

`backend/app/core/config.py:L111-L119` declares nine fields, and the four above appear in none of
them. Attribute access on a Pydantic model raises `AttributeError` for an undeclared field, so each
read fails at the line that makes it. Two further fields share the same status, `ALLOWED_ORIGINS` at
`backend/app/main.py:L118` and `PROJECT_ID` in the collaboration service. Six settings are therefore
read and never declared, against nine that are declared.
[../backend/app/core/README.md](../backend/app/core/README.md) carries the full configuration
census.

One of the four sets the lifetime of a bearer credential, and no committed contract bounds it.
`SIGNED_URL_EXPIRATION` reaches `Blob.generate_signed_url` as the `expiration` argument at
`backend/app/services/export_service.py:L162` and `:L236`. `backend/app/core/config.py` declares no
field of that name, so it carries no type, no default, no `Field` constraint and no validator, and
defined bounds on the value measure zero. That matters more than an ordinary missing setting, because
a version 4 signed URL needs no authentication to redeem. Whoever holds the link holds the object for
as long as the link lives, so the lifetime is the whole of the access control.

One failure mode follows once a value arrives, and one apparent failure mode does not. A unit mistake
passes silently, because the client library reads a bare integer as seconds while a `timedelta` or a
`datetime` means something else, and nothing in the codebase distinguishes the three. An over-long
lifetime does not pass: the client library rejects a version 4 expiry above seven days with
`ValueError`, so a value above that limit mints no link at all. Every value at or below seven days is
accepted with no project policy behind it, which is where the real exposure sits.

No signed URL is generated today. Four barriers stand in front of the gap, in the order execution
meets them. First, the absent `settings` singleton at
`backend/app/services/export_service.py:L61` stops the module at import. Second, the undeclared
`settings.STORAGE_BUCKET_NAME` at `:L154` and `:L228` raises `AttributeError`. Third, the undeclared
`settings.SIGNED_URL_EXPIRATION` at `:L162` and `:L236` raises the same way. Fourth, signing needs a
credential that can sign bytes, and whether the resolved credential supplies one depends on the host.
A service-account key file carries a private key and signs locally. A metadata-server token on a
Compute Engine or Cloud Run instance carries no key. Signing then works only by delegating to
the IAM Credentials API, which needs the `iam.serviceAccounts.signBlob` permission on the signing account and
an explicitly passed signer identity. `export_service.py:L160-L164` and `:L234-L238` pass no
`credentials`, no `service_account_email` and no `access_token`, so the code settles neither the
credential type nor the signing route, and no committed file supplies a credential that would settle
it. Read the gap as one to close before the first link is issued, not as an exposure running now.
The same limitation is recorded against the modules that hold it, in
[../backend/app/core/README.md](../backend/app/core/README.md) and
[../backend/app/services/README.md](../backend/app/services/README.md).

`infrastructure/terraform/main.tf:L50` declares one `google_storage_bucket` resource, and no
committed file connects that bucket's name to any of the four settings fields above.
[deployment-guide.md](deployment-guide.md) covers the infrastructure side.

### Signed-link trust boundary

A signed URL is a bearer credential. Anyone holding the string can fetch the object until the signature
expires, with no account, no token and no further check, so the link is the authorization. Treat every
one of these links as a secret in transit and at rest. The constraints below are absent from the
committed code and become prerequisites the moment a caller reaches the signing calls.

| # | Constraint | Committed state |
| --- | ------------ | ----------------- |
| 1 | A reviewed expiry, short enough to bound exposure | `export_service.py:L162` and `:L236` read `settings.SIGNED_URL_EXPIRATION`, which `Settings` never declares, so no value and no ceiling exists in the repository. `background_tasks.py:L146` hard-codes `timedelta(hours=1)` instead, so the two paths would expire differently even once the field exists |
| 2 | One signing scheme | The service passes `version="v4"` at `:L161` and `:L235`. The task passes no `version` argument at `:L146`. A consumer of both paths receives links signed under two different schemes |
| 3 | An authorization check before a link is minted | Neither export method takes a caller identity. `export_to_pdf` at `:L87` and `export_to_docx` at `:L168` accept a `Document` and sign a link for it, and nothing compares a requesting user against the document's owner first. `process_document_export` at `background_tasks.py:L101` takes `user_id` and puts it to two uses. `:L135` passes it to `document_service.get_document(document_id, user_id)`, an ownership handoff with the right arity that no `await` drives, so the coroutine is created, never executed and discarded, and the comparison inside it never runs. `:L142` then builds the object key from the same value |
| 4 | A signing credential held as a secret | Signing needs a private key or an IAM SignBlob delegation. No committed file supplies either, and `scripts/deploy.sh:L19` would archive a service-account key JSON file sitting in the working tree and `:L23` would upload it. [../scripts/README.md](../scripts/README.md) carries that path |
| 5 | No link in a log or an error | No traced exposure exists today. No committed caller reaches either export method, so no signed URL is produced, and no logging path in the repository receives one. The constraint stands as a prerequisite rather than a finding, because `frontend/src/services/api.ts` and the page handlers log whole error objects, and a link returned through either would land in the console with the rest of the response. [../frontend/src/pages/README.md](../frontend/src/pages/README.md) records that logging behaviour |
| 6 | Object-level access control that the link cannot bypass | `infrastructure/terraform/main.tf:L54` sets `uniform_bucket_level_access = true`, which is the right default. `:L56-L58` enables versioning with no `lifecycle_rule`, so a delete or an overwrite on that bucket archives the current generation and leaves it addressable to anyone able to name it. Whether an export ever lands there is undetermined, because both upload sites read `settings.STORAGE_BUCKET_NAME` (`backend/app/services/export_service.py:L154`, `:L228`) and `Settings` does not declare that field. [../infrastructure/terraform/README.md](../infrastructure/terraform/README.md) carries the bucket detail |

None of the six is changed here. Each is recorded so that whoever makes this path reachable knows what
has to land with it.

## Google Cloud Pub/Sub

**SCAFFOLDED ONLY.** No route constructs `CollaborationService`, so the Pub/Sub fan-out is
unreachable at runtime. The class sits at `backend/app/services/collaboration_service.py:L41`, and a
search of all four routers and `backend/app/main.py` finds no import of the module and no
construction of the class. The only constructor call in the repository sits at
`backend/tests/test_services.py:L39`, reached through a `services.collaboration_service` specifier
whose target file does exist. Two conditions stand between that specifier and a live object. The name
is discoverable only while `backend/app/` sits on the import path, because `services/` holds no
`__init__.py` and acts as an implicit namespace package. Importing it then needs `backend/` on the
path as well, for the module's own `app.*` imports, and stops at
`backend/app/services/collaboration_service.py:L39`, which requests the `settings` name that
`app.core.config` never binds. The same test file calls three methods the class never defines, at
`:L44`, `:L50` and `:L55`. [../backend/tests/README.md](../backend/tests/README.md) carries the full
import-resolution matrix, and
[troubleshooting.md](troubleshooting.md#three-test-imports-that-are-path-dependent-rather-than-absent)
records the same sequence.

Declared intent runs the other way. `documentation/Technical Specifications.md:L292`, under the
DATA-FLOW DIAGRAM heading at `L264`, presents a collaboration service managing real-time updates as
a system component. The same document names Cloud Pub/Sub as the messaging service behind real-time
collaboration, at `:L592` under the THIRD-PARTY SERVICES heading at `L587`. Both statements describe
intent. The committed code holds the calls and no path to them.

### What the service constructs and calls

`__init__` at `:L67` builds both clients and one registry. `:L69` constructs `PublisherClient()`,
`:L70` constructs `SubscriberClient()`, and `:L71` creates `active_connections` as a plain
dictionary. The registry lives in one process and carries no lock, so two workers hold two separate
views of who is connected.

Four Pub/Sub calls exist across three methods.

| Method | Pub/Sub call | Locator |
| -------- | -------------- | --------- |
| `connect` at `:L75` | `create_subscription` | `:L124` |
| `connect` at `:L75` | `subscribe` | `:L165` |
| `disconnect` at `:L173` | `delete_subscription` | `:L211` |
| `broadcast_change` at `:L218` | `publish` | `:L248` |

`connect` registers the socket at `:L117`, then builds a per-document topic path at `:L120` and a
per-document, per-user subscription path at `:L121`. Both paths interpolate `settings.PROJECT_ID`,
and `Settings` never declares that field, so `:L120` raises `AttributeError` before any Pub/Sub call
runs. `disconnect` rebuilds the same subscription path at `:L209`, and `broadcast_change` rebuilds the
same topic path at `:L245`.

### The topic must already exist, and nothing creates it

Two of the four Pub/Sub calls name a topic and require it to exist. `create_subscription` at `:L124`
passes `topic=topic_name`, and Pub/Sub answers `NotFound` when that topic is absent. `publish` at
`:L248` addresses the same path and fails the same way. Neither call creates a topic, and no
`create_topic` call exists anywhere in the repository. The module's own docstring records the gap at
`backend/app/services/collaboration_service.py:L8-L12`.

No committed infrastructure supplies the topic either. Searching all of `infrastructure/` for
`pubsub`, `topic` and `subscription` returns nothing, and `infrastructure/terraform/main.tf` declares
one provider plus four Google Cloud resources with no messaging resource among them. The topic name is
derived per document at `backend/app/services/collaboration_service.py:L120`, so a deployment would
need one topic per document identifier, created outside this repository before any editor connects.

| Call | Locator | Needs a topic | Status without a pre-created topic |
| ------ | --------- | --------------- | ------------------------------------- |
| `create_subscription` | `collaboration_service.py:L124` | Yes, as the `topic` argument | **BLOCKED.** `NotFound`, caught at `:L125`, printed at `:L127`, then `:L128` returns |
| `subscribe` | `collaboration_service.py:L165` | No, it names the subscription | Never reached, because `:L128` returned first |
| `delete_subscription` | `collaboration_service.py:L211` | No, it names the subscription | `NotFound` for a subscription that was never created, caught at `:L212` and printed at `:L214` |
| `publish` | `collaboration_service.py:L248` | Yes, as the destination path | **BLOCKED.** `NotFound`, caught at `:L250`, printed at `:L252`, and the method returns normally |

Creating the topic outside the repository is therefore a prerequisite for the collaboration path.
The prerequisite sits behind the earlier blockers rather than in front of them: no route constructs the class, and
`settings.PROJECT_ID` is undeclared.

### Seven faults inside the collaboration path

- **`asyncio` is undefined, and two further faults sit on the same line.** The callback at
  `backend/app/services/collaboration_service.py:L131` calls
  `asyncio.run(websocket.send_json(message.data))` at `:L163`, and the module imports no
  `asyncio`, so the first delivered message raises `NameError`. Supplying the import exposes the
  second fault: `message.data` is `bytes` on a Pub/Sub message, `WebSocket.send_json` serializes with
  `json.dumps`, and `json.dumps` rejects `bytes`. Nothing decodes the payload, while
  `broadcast_change` encoded it as UTF-8 at `:L248`, so the round trip is unbalanced. The third fault
  is event-loop ownership. `asyncio.run` builds a new loop and closes it on return, while the
  `WebSocket` belongs to the server's already-running loop. `asyncio.run` also refuses outright when
  a loop is already running on the calling thread. The Pub/Sub client invokes the callback on its own thread, so
  none of the three propagates to `connect`.
- **A failed publish is caught and logged, not raised.** `broadcast_change` reads
  `settings.PROJECT_ID` at `:L245`, which sits **above** the `try` at `:L247`, so the undeclared-field
  `AttributeError` propagates to the caller on the first call and nothing is published. That is the
  method's first statement, so it leaves no partial state. Everything after it is guarded: `:L248`
  calls `json.dumps(change)` against a module that imports no `json`, and `:L250` catches every
  exception the body raises while `:L252` prints it. Once `PROJECT_ID` exists, a publish failure
  therefore surfaces as a printed line and a normal `None` return, and a caller cannot tell a
  delivered change from a dropped one.
- **Acknowledgement precedes delivery.** `:L162` calls `message.ack()` and `:L163` then sends the
  data to the socket. A send that fails after the acknowledgement loses the message, because Pub/Sub
  has already been told the message was handled and will not redeliver.
- **Both futures block, and the third method has no future to wait on.** `:L168` calls
  `future.result()` on the streaming pull future, and `:L249` calls `future.result()` on the publish
  future. Neither call passes a timeout, so each blocks the calling thread until the future settles.
  `connect` is declared `async def`, so the block at `:L168` holds the event loop rather than one
  worker thread. `disconnect` creates no future: `:L211` calls `delete_subscription`, which returns
  nothing to wait on, so the method has nothing to block for and nothing to cancel.
- **Two partial states can persist.** `connect` mutates the registry at `:L115-L117` before it touches
  Pub/Sub. `:L124` calls `create_subscription` inside a `try`, and on failure `:L127` prints the error
  and `:L128` returns, leaving the socket registered in `active_connections` with no subscription
  behind it. That connection receives nothing and no later call removes it. `disconnect` removes the
  registry entry at `:L203-L206` before it deletes the subscription, so a caught deletion failure at
  `:L212` leaves a subscription with no registry entry. Neither method compensates, and neither reports
  the state to its caller.

Two markers sit inside this module, above `connect` at `:L73-L74` and above `broadcast_change` at
`:L216-L217`. Both record the code authors' own confidence in the method beneath them. Read them in
place. [../backend/app/services/README.md](../backend/app/services/README.md) carries the service
detail, and [troubleshooting.md](troubleshooting.md) registers the transport gap under
[G7](troubleshooting.md#the-collaboration-path-has-no-route-and-two-protocols).

### Collaboration trust boundary

Being unreachable is not the same as being safe, and this path is neither. The controls listed below do
not exist in the committed code, and each one becomes a prerequisite the moment a route constructs the
service. None of them can be inferred from the current signatures, so a repair that only adds a
WebSocket route would expose every gap at once.

| # | Control | Committed state |
|---|---------|-----------------|
| 1 | Authenticate the connection | `connect` at `:L75` takes `websocket`, `document_id` and `user_id`. It accepts no token, reads no header and calls no dependency, so nothing establishes who is connecting. Every other protected surface in the backend goes through `get_current_user` at `backend/app/api/auth.py:L89`, and this path does not |
| 2 | Authorize the identity against the document | Nothing compares `user_id` against the document's stored owner. `:L115-L117` registers the socket straight from the two string arguments. The document handlers at least attempt an owner check, at `backend/app/api/documents.py:L184`, `:L232` and `:L279` |
| 3 | Validate `document_id` before it names a resource | `:L120`, `:L121` and `:L245` interpolate `document_id` directly into Pub/Sub topic and subscription paths. A caller-supplied string therefore selects the topic it publishes to and the subscription it creates, with no allow-list, no format check and no membership check |
| 4 | Authorize a disconnect | `disconnect` at `:L173` takes the same two unverified strings and removes the entry at `:L204` and `:L206`, then deletes the subscription at `:L211`. Supplying another user's identifiers would drop that user's connection |
| 5 | Validate the event payload | `broadcast_change` at `:L218` declares `change: dict` and publishes it unchanged at `:L248`. No schema constrains the keys, no field is bounded, and no type is checked |
| 6 | Bound the payload size | Nothing limits the size of `change`. A large object is serialized and published as one message, and Pub/Sub rejects a message above its own limit rather than the application refusing it first |
| 7 | Scope the fan-out per recipient | `active_connections[document_id]` maps every registered `user_id` to a socket, and the callback at `:L131` sends each delivered message to the socket at `:L163` with no per-recipient authorization check. One publish reaches every socket registered against that document |
| 8 | Share state across processes | `__init__` at `:L67` builds `active_connections` as a plain dictionary in process memory, and the class docstring records the consequence at `:L44-L46`. A second server process shares none of it, so a fan-out under more than one worker reaches only the subset of clients that landed on the same process |

Read the whole table as future work, not as a change made here. Nothing in this documentation pass
alters the service. The security gates that must land before this integration is made reachable are
ordered in [onboarding.md](onboarding.md), and [troubleshooting.md](troubleshooting.md) registers each
one with its evidence.

## Redis broker for Celery

**ABSENT.** Redis is declared in configuration and exists in no infrastructure, so no Celery task
can be enqueued. The chain is three links long and every link is verifiable.

| Link | Evidence |
| ------ | ---------- |
| Configuration declares the broker URL | `backend/app/core/config.py:L119` declares `REDIS_URL: str` with no default, so the field is required |
| Code wires Celery to that value | `backend/app/tasks/background_tasks.py:L98` builds `Celery('microsoft_word', broker=settings.REDIS_URL)` at module scope |
| No infrastructure provisions Redis | `infrastructure/docker/docker-compose.yml:L3-L39` defines exactly three services, `frontend` at `:L4`, `backend` at `:L17` and `db` at `:L30`. `infrastructure/terraform/main.tf` declares one provider and four Google Cloud resources, a network at `:L19`, a subnetwork at `:L25`, a firewall rule at `:L35` and a storage bucket at `:L50`, and no cache resource. Searching all of `infrastructure/` for `redis` or `memorystore` returns nothing |

Declared intent names the missing piece directly. `documentation/Technical Specifications.md:L584`,
under the DATABASES heading at `L563`, lists Redis on Google Cloud Memorystore in the stack. The
same document lists Celery as the task queue, at `:L554` under the TECHNOLOGY STACK heading at
`L523`. Neither statement reached the infrastructure.

### Three tasks and no producer

Three tasks carry the `@celery_app.task` decorator, at `:L100`, `:L150` and `:L286`.

| Task | Signature | Purpose in the code |
| ------ | ----------- | --------------------- |
| `process_document_export` | `:L101` | Convert a document, upload the object, return a signed link |
| `cleanup_expired_documents` | `:L152` | Delete documents past an expiry date, plus their object and metadata |
| `update_document_statistics` | `:L287` | Recompute a word and page count and write it back |

Nothing enqueues any of the three. A repository-wide search for `.delay(` and for `.apply_async(`
returns zero call sites in `backend/app/`, in `backend/tests/` and in `frontend/src/`. The queue has
three consumers and no producer.

Two further defects sit in the task tier.

- **The daily sweep has no schedule.** `:L150` places `@celery_app.task` above
  `@celery_app.periodic_task(run_every=timedelta(days=1))` at `:L151`. Celery 5 exposes no
  `periodic_task` decorator on an application object. The module therefore raises `AttributeError`
  at that line once the earlier import failures clear, and the retention sweep carries no schedule.
- **No process runs the tasks.** No worker command and no beat command appears anywhere. Compose
  starts three services and none of them is a worker, no Dockerfile declares a worker entry point,
  and `scripts/deploy.sh` starts no worker. `.github/workflows/cd.yml:L19-L20` deploys two App
  Engine descriptors and mentions no queue.

[../backend/app/tasks/README.md](../backend/app/tasks/README.md) carries the task detail, and
[troubleshooting.md](troubleshooting.md) registers the broker gap under
[G8](troubleshooting.md#no-redis-service-backs-the-celery-broker).

## Credential model

Google credentials are designed to resolve at import time, not at first call.
`backend/app/db/firestore.py:L39` calls `google.auth.default()` at module scope, so importing the
adapter would run ADC discovery immediately. Any module that reaches `from app.db.firestore import db`
inherits that requirement, which covers `backend/app/main.py:L21`,
`backend/app/services/document_service.py:L59` and `backend/app/tasks/background_tasks.py:L93`. The
next line, `backend/app/db/firestore.py:L40`, constructs the Firestore client eagerly rather than lazily.

No ADC discovery happens against the committed tree. `backend/app/db/firestore.py:L36` imports
`settings` and raises `ImportError` first, so `:L39` and `:L40` never execute. The credential model
below is the model the code declares.

The database engine behaves the same way in one respect and differently in another.
`backend/app/db/sql.py:L16` calls `create_engine(settings.DATABASE_URL)` at module scope, so
importing that module needs a connection string present in configuration. `create_engine` parses the
URL eagerly, so an unparseable value raises during that same import. Engine construction does not
open a connection, so a parseable value naming an unreachable database passes here and fails at the
first connection instead.

Four surfaces supply credentials, and they do not agree on a single source.

| Surface | What it supplies | Locator |
| --------- | ------------------ | --------- |
| `Settings` | `GOOGLE_CLOUD_PROJECT` and `GOOGLE_APPLICATION_CREDENTIALS`, both `Optional[str]` | `backend/app/core/config.py:L116-L117` |
| The nested `Config` class | An `.env` file as the fallback source, with UTF-8 encoding | `backend/app/core/config.py:L121-L124`, naming `.env` at `:L123` |
| `scripts/deploy.sh` | A guard that exits 1 when `GOOGLE_APPLICATION_CREDENTIALS` is empty, and nothing more. See the note below | `scripts/deploy.sh:L4-L7` |
| `.github/workflows/cd.yml` | A project identifier and a service-account key, both from repository secrets named `GCP_PROJECT_ID` and `GCP_SA_KEY`, passed to `google-github-actions/setup-gcloud`, which does authenticate the CLI | `.github/workflows/cd.yml:L13-L16` |

`scripts/deploy.sh` supplies no credential to any tool. Two credential mechanisms exist and the
script conflates them. `GOOGLE_APPLICATION_CREDENTIALS` configures Application Default Credentials,
which the Google client libraries read, and the `gcloud` and `gsutil` command-line tools read their
own credential store instead. `scripts/deploy.sh:L4-L7` tests only that the variable is non-empty: it
checks no path, validates no key, runs no `gcloud auth activate-service-account --key-file`, and runs
no `gcloud config set project`. Every cloud stage in that script is a CLI invocation rather than a
client-library call, so a passing guard authorizes nothing. The gap first surfaces at
`scripts/deploy.sh:L23`, the `gsutil cp` that is the script's first cloud command, which fails on
missing credentials or a missing default project unless the host already carries an authenticated
`gcloud` configuration. `.github/workflows/cd.yml:L13-L16` is the one path that does authenticate a
CLI, because the `setup-gcloud` action consumes the key rather than an environment variable alone.
[../scripts/README.md](../scripts/README.md) carries the per-stage detail.

No `.env` file is committed, so the fallback source named at `backend/app/core/config.py:L123`
resolves to nothing on a clean checkout. The environment must therefore supply all seven required
fields directly. `Settings` construction raises `ValidationError` when any one of them is missing.
[onboarding.md](onboarding.md) covers what a developer can run without them.

One earlier failure hides all of the above. `backend/app/core/config.py` defines the `Settings`
class at `:L51` and the `get_settings()` factory at `:L126`, and creates no module-level `settings`
instance. Eight modules import that name directly, and nine module-import failures trace back to it,
because `app.main` fails both on its own import at `:L20` and earlier through `app.api.auth`.
`import app.main` therefore raises `ImportError` before any credential call runs. [troubleshooting.md](troubleshooting.md) records the chain under
[G2](troubleshooting.md#the-absent-settings-singleton).

Two counts describe the reach of that single omission. Mixing them overstates the direct damage.
**Eight modules import the `settings` name directly**, at `backend/app/main.py:L20`,
`backend/app/api/auth.py:L81`, `backend/app/db/firestore.py:L36`, `backend/app/db/sql.py:L14`,
`backend/app/services/collaboration_service.py:L39`,
`backend/app/services/document_service.py:L60`, `backend/app/services/export_service.py:L61` and
`backend/app/tasks/background_tasks.py:L92`. A ninth module is affected without importing the name.
`backend/app/core/security.py:L43` imports `get_settings`, which does exist, and calls it at `:L177`,
so that module fails later and for a different reason. The wider count is different again. Modules
affected through the import chain reach twelve of the fifteen under `backend/app/`, because a module
importing any of the eight inherits the failure. Only three import cleanly.

## The four end-to-end workflows and their contract mismatches

Four workflows can be traced as intended workflows, from a page in the browser to a handler on the
server. None of the four runs: the application cannot import, and each workflow carries at least one
contract mismatch of its own, which is what makes tracing them worthwhile. Read each table below as a
pairing of committed client code against committed server code, not as a request that completes. The
application programming interface (API) route inventory belongs to
[../backend/app/api/README.md](../backend/app/api/README.md). That README owns all 14 handlers, the
split of 12 protected against 2 public, and the fact that no handler declares a `status_code`.
Field-level drift belongs to [data-model.md](data-model.md).

One mismatch applies to three of the four workflows, so read it once here.
`backend/app/main.py:L125-L128` mounts all four routers with no prefix. The client prefixes its
document calls with `/documents` at `frontend/src/services/api.ts:L218`, `:L246` and `:L288`, and no
server route carries that segment.

The three prefixed calls do not all fail the same way, and the difference matters when reading a
response. Assume for a moment that the import chain and the client's own blockers are repaired, so
dispatch actually happens:

| Client call | Locator | What the server does with it |
|-------------|---------|------------------------------|
| `GET /documents` | `frontend/src/services/api.ts:L218` | Matches `GET /{document_id}` at `backend/app/api/documents.py:L145`, because `/documents` is a single path segment, so `document_id` binds to the string `documents`. No body follows. That handler raises first: `:L183` passes one argument to the two-parameter `get_document` signature at `backend/app/services/document_service.py:L123`, so a `TypeError` propagates out of the handler and the response is a 500. The declared `Document[]` never meets a document object |
| `POST /documents` | `frontend/src/services/api.ts:L246` | The single-segment shape matches `GET`, `PUT` and `DELETE` at `backend/app/api/documents.py:L145`, `:L188` and `:L237`, and no router declares `POST /{document_id}`. Starlette answers **405 Method Not Allowed** rather than 404 |
| `PUT /documents/${documentId}` | `frontend/src/services/api.ts:L288` | Two path segments, and no two-segment route is registered anywhere in the four routers. The response is **404** |

Every one of the three sits behind earlier blockers, so none is observable today.
[troubleshooting.md](troubleshooting.md#the-client-calls-six-routes-and-no-server-route-matches-any-of-them) carries the
same three outcomes in its route register.

### Register and sign in

The login call diverges from its intended server route in five independent places. Those are the path,
the request origin, the body encoding, the credential field name and the response field name. The table
sets the two sides against each other dimension by dimension, and
[../frontend/src/services/README.md](../frontend/src/services/README.md) carries the same comparison
for all six client call sites.

| Dimension | Client, `login` at `frontend/src/services/auth.ts:L144` | Server, `POST /token` at `backend/app/api/auth.py:L167` |
| --- | --- | --- |
| Method | `POST` | `POST` |
| Path | `/auth/login` | `/token`, since `backend/app/main.py:L125` mounts the router with no prefix |
| Origin | Page origin. `auth.ts:L68` imports the bare `axios` global, which carries no `baseURL` | Wherever the service is served |
| Encoding | JSON. Axios serializes the object literal at `:L146` | `application/x-www-form-urlencoded`, because `:L168` declares `OAuth2PasswordRequestForm` |
| Credential fields | `email` and `password` | `username` and `password` |
| Request headers | No `Authorization` header. `auth.ts` never reaches the interceptor at `api.ts:L140-L146` | The route is public and reads none |
| Response fields | Reads `response.data.accessToken` at `:L147` | Returns `{"access_token": ..., "token_type": "bearer"}` at `:L240` |
| State handoff | Writes the read value to `localStorage` under `accessToken` at `:L148` | None. The server holds no session |

The other two calls in the same module have no working counterpart either.

| Side | What runs | Locator |
| ------ | ----------- | --------- |
| Client | `login` posts to `/auth/login` | `frontend/src/services/auth.ts:L146` |
| Client | Reads `response.data.accessToken` | `:L147` |
| Client | Stores the value under `accessToken` in `localStorage` | `:L148` |
| Client | `logout` posts to `/auth/logout` | `:L194` |
| Client | `getCurrentUser` gets `/auth/me`, then casts with `as User` and no check | `:L239`, `:L240` |
| Server | `POST /register` creates the user, taking a JSON `UserCreate` body | `backend/app/api/auth.py:L243`, decorator at `:L242` |
| Server | `GET /me` returns the caller, behind `get_current_user` | `backend/app/api/users.py:L30`, decorator at `:L29` |

Five mismatches, each of which breaks the workflow on its own:

- **Path.** The client calls `/auth/login`, `/auth/logout` and `/auth/me`. The server exposes
  `POST /token`, `POST /register` and `GET /me`, the last of them on the user router at
  `backend/app/api/users.py:L29`. None of the three client paths matches a registered route, so each
  returns 404 if it is forwarded to FastAPI. Nothing forwards it today. `auth.ts:L68` imports the
  bare `axios` global, which carries no `baseURL`, so each request targets the page origin, and the
  404 comes from whatever serves that origin until a proxy routes `/auth/*` to the API.
  `GET /me` is itself shadowed, which the profile workflow below records.
- **Request encoding.** `frontend/src/services/auth.ts:L146` calls `axios.post` with a plain object,
  and Axios serializes a plain object as JSON with `Content-Type: application/json`. The server
  declares `form_data: OAuth2PasswordRequestForm = Depends()` at `backend/app/api/auth.py:L168`, and
  that dependency reads an `application/x-www-form-urlencoded` body. A JSON body therefore fails
  request validation with 422 before the handler body runs, even if the path were corrected.
- **Credential field name.** The client sends `email` and `password` at
  `frontend/src/services/auth.ts:L146`. `OAuth2PasswordRequestForm` supplies `username` and
  `password`, and `backend/app/api/auth.py:L230` reads `form_data.username`. No `email` field reaches
  the handler, so the two ends disagree on the identifier as well as on the encoding.
- **Token field name.** The server returns `access_token` at `backend/app/api/auth.py:L240`, and the
  client reads `accessToken` at `frontend/src/services/auth.ts:L147`, so the read yields `undefined`.
  `localStorage.setItem` coerces its value to a string, so `:L148` stores the four-character string
  `"undefined"` rather than the value `undefined`, and any later truthiness test on the stored value
  passes.
- **HTTP client.** `frontend/src/services/auth.ts:L68` imports the bare `axios` global and calls it
  directly at `:L146`, `:L194` and `:L239`. The configured instance lives in
  `frontend/src/services/api.ts:L162`, and its request interceptor at `:L140-L146` is the only code
  that attaches an `Authorization` header. Every call in `auth.ts` bypasses that interceptor, so
  `GET /auth/me` carries no bearer token even after a successful login.

No registration screen and no login screen exists. `frontend/src/App.tsx:L52-L55` declares four
routes: `/`, `/editor`, `/templates` and `/settings`. None of the four renders an authentication
form, so a user cannot reach either server route through the interface.

### Open and edit a document with auto-save

| Side | What runs | Locator |
| ------ | ----------- | --------- |
| Client | Imports `getDocument` and `updateDocument` from the API module | `frontend/src/pages/Editor.tsx:L25` |
| Client | Loads the document inside an effect, guarded on the identifier | `:L105-L120`, guard at `:L117`, call at `:L108` |
| Client | Auto-saves inside a second effect | `:L186-L216` |
| Client | Calls `updateDocument(currentDocument.id, { content })` | `:L207` |
| Client | Arms a five-second timer and clears it on cleanup | `:L214`, `:L215` |
| Server | `GET /{document_id}` reads the document | `backend/app/api/documents.py:L146`, decorator at `:L145` |
| Server | `PUT /{document_id}` updates it | `:L189`, decorator at `:L188` |

Four mismatches:

- **`getDocument` does not exist.** `frontend/src/services/api.ts` exports exactly three functions,
  `getDocuments` at `:L217`, `createDocument` at `:L245` and `updateDocument` at `:L287`. The plural
  `getDocuments` is not the singular the editor imports at `Editor.tsx:L25`.
- **Route prefix.** `updateDocument` calls `/documents/${documentId}` at `api.ts:L288`, and the
  document router mounts at the root, so the live path is `/{document_id}`.
- **Ownership field.** The handler reads `document.user_id` at `backend/app/api/documents.py:L184`,
  `:L232` and `:L279`. The Pydantic contract declares `owner_id: Optional[str] = None` on
  `DocumentBase` at `backend/app/schema/document.py:L66`, which `Document` inherits at `:L96`.
  [data-model.md](data-model.md#the-ownership-field-four-positions-none-canonical) names all four
  positions the field takes and names none of them canonical.
- **Auto-save interval.** The code waits five seconds, at `Editor.tsx:L214`.
  `documentation/Software Requirements Specifications (SRS).md:L543`, under the SAFETY heading at
  `L540`, describes an auto-save that fires every thirty seconds. Read the thirty-second figure as
  declared intent and the five-second timer as committed behaviour.

The auto-save effect carries no null guard and no empty-content guard. `:L207` dereferences
`currentDocument.id` with no test, while the sibling load effect does guard, at `:L117`. The effect body
runs on mount, so the timer fires five seconds after the page appears.

**That first firing sends no request.** `currentDocument` comes from the selector at `:L85`, and
`frontend/src/store/documentSlice.ts:L34` initialises `currentDocument` to `null`. Dereferencing
`currentDocument.id` at `:L207` therefore raises `TypeError` inside the client, on the argument
expression, before `updateDocument` is called and before any network activity begins. The `catch` at
`:L208` receives that `TypeError`, `console.error` at `:L209` writes it, and the outstanding-work
comment at `:L210` records the gap. No HTTP request reaches the server, so no server-side effect and no
partial write is possible from this path. The reader of the page sees nothing either way.
[../frontend/src/pages/README.md](../frontend/src/pages/README.md) carries the page detail.

### Browse and select a template

| Side | What runs | Locator |
| ------ | ----------- | --------- |
| Client | Imports `getTemplates` from the API module | `frontend/src/pages/Templates.tsx:L35` |
| Client | Calls it inside a load effect | `:L142` |
| Client | Declares a local `Template` interface | `:L61-L66` |
| Server | Five template handlers | `backend/app/api/templates.py:L78`, `:L119`, `:L152`, `:L196`, `:L255` |

Four mismatches:

- **`getTemplates` does not exist.** `frontend/src/services/api.ts` exports the same three functions
  listed under the previous workflow, at `:L217`, `:L245` and `:L287`, and none of them is
  `getTemplates`.
- **Two incompatible template shapes.** The local interface at `Templates.tsx:L61-L66` declares
  `id`, `name`, `description` and `thumbnail`. The Zod schema at
  `frontend/src/schema/template.ts:L30-L37` declares `id`, `name`, `content`, `owner_id`,
  `created_at` and `updated_at`. Two fields exist only in the interface and four exist only in the
  schema. [data-model.md](data-model.md#two-incompatible-template-shapes) carries the field-level
  comparison.
- **Every template handler is unreachable.** `backend/app/main.py:L126` registers the document
  router and `:L128` registers the template router, both with no prefix. FastAPI matches in
  registration order, and `/{document_id}` and `/{template_id}` compile to the same single-segment
  shape, so the document handler answers first for every single-segment path. The five paths in
  `templates.py` duplicate the five in `documents.py` exactly. The same registration order shadows
  the two profile routes as well, which makes seven of the twelve protected handlers unreachable
  rather than five. See the profile workflow below and
  [troubleshooting.md](troubleshooting.md#document-routes-shadow-the-template-and-profile-routes).
- **Two imported modules do not exist.** `backend/app/api/templates.py:L70` imports `Template`,
  `TemplateCreate` and `TemplateUpdate` from `app.schema.template`, and `:L71` imports
  `TemplateService` from `app.services.template_service`. Neither module is committed, so importing
  the router raises `ModuleNotFoundError`.

### View and update the profile

| Side | What runs | Locator |
| ------ | ----------- | --------- |
| Client | Imports `updateUserSettings` from the API module | `frontend/src/pages/Settings.tsx:L31` |
| Client | Initialises the form from `currentUser?.name` | `:L82` |
| Client | Submits `{ name, email }` | `:L121`, handler at `:L118` |
| Server | `GET /me` returns the caller | `backend/app/api/users.py:L30`, decorator at `:L29` |
| Server | `PUT /me` applies the update | `:L51`, decorator at `:L50` |

Four mismatches:

- **`updateUserSettings` does not exist.** `frontend/src/services/api.ts` exports the same three
  functions at `:L217`, `:L245` and `:L287`, and none of them is `updateUserSettings`.
- **Both profile routes are shadowed.** `/me` is a literal path and still a single segment, so it
  falls inside the pattern the document router already claimed. `backend/app/main.py:L126` registers
  documents ahead of `:L127` profiles, so `GET /{document_id}` at
  `backend/app/api/documents.py:L145` answers `GET /me` and `PUT /{document_id}` at `:L188` answers
  `PUT /me`. A profile fetch reaches the single-document read with `document_id` bound to the literal
  string `me`, and neither handler at `backend/app/api/users.py:L29` or `:L50` ever runs.
- **No contract declares `name`.** The page reads `currentUser?.name` at `Settings.tsx:L82` and
  submits a `name` field at `:L121`. The Pydantic `UserBase` model declares `email`, `username` and
  `full_name` at `backend/app/schema/user.py:L80-L82`, and the Zod `UserSchema` declares the same
  three at `frontend/src/schema/user.ts:L39-L41`. Neither language models a `name` field.
  [data-model.md](data-model.md) carries the field census.
- **Both handlers are synchronous.** `backend/app/api/users.py:L30` and `:L51` are plain `def`, and
  they are the only two of the 14 handlers that are not `async def`. `:L77` calls
  `user_service.update_user(...)` without
  awaiting it, so a coroutine result would be truthy and would pass the check at `:L78` unexecuted.
  The marker at `:L73-L75` records that the `UserService` contract is unverified, and
  `app.services.user_service` is not a committed module.

### The collaboration transport mismatch

The client speaks Socket.IO, the server signature expects a FastAPI `WebSocket`, and no route sits
between them. Neither end can reach the other under any configuration, because the two protocols
differ and no handler bridges them.

| End | Transport | Locator |
| ----- | ----------- | --------- |
| Client | `socket.io-client`, with `io()` called with no URL | `frontend/src/services/collaboration.ts:L13`, call at `:L77` |
| Server | `fastapi.WebSocket` as the first parameter of `connect` | `backend/app/services/collaboration_service.py:L36`, signature at `:L75` |
| Between them | Nothing. No `@app.websocket` route and no `@router.websocket` route exists anywhere | Searched all four routers and `backend/app/main.py` |

The client emits three events, and each has a server method that was clearly meant to receive it.
None of the three pairs can meet, and the reason differs per row.

| Client event | Emitted payload | Nearest server counterpart | Why the pair cannot meet |
| -------------- | ----------------- | ---------------------------- | -------------------------- |
| `join_document` | the bare `documentId` string, at `frontend/src/services/collaboration.ts:L126` | `CollaborationService.connect` at `backend/app/services/collaboration_service.py:L75` | `connect` declares a `WebSocket`, a `document_id` and a `user_id`. The emit carries one string, no socket object and no user identity, and no route delivers it |
| `leave_document` | the bare `currentDocumentId` string, at `:L154` | `CollaborationService.disconnect` at `backend/app/services/collaboration_service.py:L173` | `disconnect` declares `document_id` and `user_id`. The emit carries the identifier alone, and `:L155` clears it straight afterwards with nothing confirming the emit |
| `document_changes` | the envelope `{ documentId, changes }`, at `:L201-L204` | `CollaborationService.broadcast_change` at `backend/app/services/collaboration_service.py:L218` | `broadcast_change` declares `document_id` and a `change` dictionary and publishes `json.dumps(change)` at `:L248`. The client nests the change inside an envelope, so the shapes differ even with a route in place |

Four further facts complete the picture:

- **`io()` receives no URL** at `frontend/src/services/collaboration.ts:L77`, so the client would
  attempt a Socket.IO handshake against the page origin rather than the API host.
- **No inbound event is handled.** `setupEventListeners` at `:L88` runs from the constructor at
  `:L78`, and its body registers no listener. The marker at `:L89-L92` records the gap.
  Collaboration therefore runs one way as written: the client emits and never receives.
- **The client class is never instantiated.** `CollaborationService` is declared at `:L51` and
  default-exported at `:L212`, and no module in `frontend/src/` imports the file.
- **The payload shapes differ.** The client emits `{ documentId, changes }` at `:L201-L204`. The
  server publishes a JSON-encoded change dictionary at
  `backend/app/services/collaboration_service.py:L248`, keyed by whatever the caller passed as
  `change`. No shared artifact reconciles the two.

[../frontend/src/services/README.md](../frontend/src/services/README.md) carries the client detail,
and [architecture-overview.md](architecture-overview.md#system-boundaries) places the boundary in
the wider map.

## Related documentation

[docs/README.md](README.md) is the index for this documentation set. The list below is the same map,
narrowed to the documents this guide leans on.

Repository-level documents beside this one:

- [architecture-overview.md](architecture-overview.md), the six-area map and the four tiers
- [data-model.md](data-model.md), the Pydantic and Zod contracts and every field divergence
- [troubleshooting.md](troubleshooting.md), the same defects as a numbered register
- [deployment-guide.md](deployment-guide.md), what the Terraform, Docker and pipeline assets do
  today
- [onboarding.md](onboarding.md), clean-machine setup and a prioritised task list
- [decision-log.md](decision-log.md), every judgement this engagement made and its reasoning
- [prose-validation.md](prose-validation.md), the writing-clarity verdict for this document set

Module documentation for the directories this guide draws on:

- [../backend/app/db/README.md](../backend/app/db/README.md), the Firestore adapter and the dead
  SQLAlchemy path
- [../backend/app/services/README.md](../backend/app/services/README.md), all three domain services
- [../backend/app/tasks/README.md](../backend/app/tasks/README.md), the Celery application and its
  three tasks
- [../backend/app/api/README.md](../backend/app/api/README.md), the 14 handlers and the path
  collision
- [../backend/app/core/README.md](../backend/app/core/README.md), the configuration census
- [../frontend/src/services/README.md](../frontend/src/services/README.md), the three client
  services
- [../frontend/src/pages/README.md](../frontend/src/pages/README.md), the four routed pages

Declared intent, read as comparison and never as committed behaviour:

- [Technical Specifications](<../documentation/Technical Specifications.md>). Stack material sits
  under the TECHNOLOGY STACK heading at `L523`. Component material sits under the SYSTEM
  ARCHITECTURE heading at `L125`.
- [Software Requirements Specifications](<../documentation/Software Requirements Specifications (SRS).md>).
  The auto-save figure sits under the SAFETY heading at `L540`.
