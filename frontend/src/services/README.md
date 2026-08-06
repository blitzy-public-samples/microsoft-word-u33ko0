# frontend/src/services

*Line citations in this document use the numbering of each module as committed at `06be74c`. The inline documentation pass added comment lines above every construct, so a symbol now sits lower in the file than its citation says. Each citation names its symbol as well as its line for that reason.*

## Purpose

The directory holds the client's three outbound integration points: document calls over REST (Representational State Transfer), authentication calls, and a Socket.IO collaboration client. `api.ts` builds one shared Axios instance and exports three document functions. `auth.ts` exports three authentication functions that bypass that shared instance and call the bare Axios global. `collaboration.ts` exports a class that wraps a Socket.IO connection. Only `api.ts` has importers anywhere in `frontend/src`, and each of its three importers names a symbol the module never defines.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `createApiClient` | Module-private factory | `api.ts:L7` | Builds an `AxiosInstance`, sets the JSON content type, and attaches both interceptors. Declared `const` with no `export` keyword, so no other module can call it. |
| `api` | Module-private singleton | `api.ts:L36` | Holds the one instance `createApiClient` returns, created once when the module evaluates. |
| `getDocuments` | Exported async function | `api.ts:L38` | Issues `GET /documents` (`api.ts:L39`) and returns `response.data` typed `Document[]`. |
| `createDocument` | Exported async function | `api.ts:L43` | Issues `POST /documents` with the `DocumentCreate` body (`api.ts:L44`) and returns the created document. |
| `updateDocument` | Exported async function | `api.ts:L48` | Issues `PUT /documents/${documentId}` with the `DocumentUpdate` body (`api.ts:L49`) and returns the updated document. |
| `login` | Exported async function | `auth.ts:L5` | Posts `{ email, password }` to `/auth/login` (`auth.ts:L7`), reads `response.data.accessToken` (`auth.ts:L8`), writes it to `localStorage` (`auth.ts:L9`), and returns it. |
| `logout` | Exported async function | `auth.ts:L16` | Posts to `/auth/logout` (`auth.ts:L18`), then removes the stored token (`auth.ts:L19`). |
| `getCurrentUser` | Exported async function | `auth.ts:L25` | Issues `GET /auth/me` (`auth.ts:L27`) and casts the body to `User` (`auth.ts:L28`). |
| `CollaborationService` | Default-exported class | `collaboration.ts:L5`, `:L49` | Opens a Socket.IO connection in its constructor (`collaboration.ts:L10`) and tracks one document id. |
| `joinDocument` | Public method | `collaboration.ts:L22` | Emits `join_document` with the id (`collaboration.ts:L23`) and stores it as the active document. |
| `leaveDocument` | Public method | `collaboration.ts:L28` | Emits `leave_document` when an id is tracked (`collaboration.ts:L30`), then clears it (`collaboration.ts:L31`). |
| `sendChanges` | Public method | `collaboration.ts:L36` | Emits `document_changes` carrying `{ documentId, changes }` (`collaboration.ts:L38-L41`), or throws when no document is active (`collaboration.ts:L43`). |

## Architecture Fit

The directory sits between the routed pages and the server, and it is the only place in `frontend/src` that opens a network connection. The specification places an integration boundary here too. Its `## HIGH-LEVEL ARCHITECTURE DIAGRAM` heading routes the single-page application through an `API Gateway` node (`documentation/Technical Specifications.md:L145`), and no committed file implements that node. The committed code matches the specification's placement of a client-side service tier, and diverges on the transport target.

The endpoint paths make the divergence precise, and they sit between the client and the committed server rather than between the client and declared intent. Under the specification's `## API DESIGN` heading, an `/auth` group declares `POST /login` and `POST /logout` (`documentation/Technical Specifications.md:L408`, `:L413-L414`). A `/documents` group declares `GET /documents` and `POST /documents` (`:L409`, `:L417-L418`). The client follows those four declarations at `auth.ts:L7`, `auth.ts:L18`, `api.ts:L39` and `api.ts:L44`.

The committed server follows none of them. `backend/app/main.py:L49-L52` mounts all four routers with no prefix, so the document routes serve `/` and `/{document_id}` (`backend/app/api/documents.py:L10-L39`). The token route is `POST /token` (`backend/app/api/auth.py:L28`). One path matches neither side. `auth.ts:L27` calls `GET /auth/me`, while the specification declares `GET /users/me` (`documentation/Technical Specifications.md:L424`) and the server exposes `GET /me` (`backend/app/api/users.py:L8`).

For the repository-wide map of these boundaries, see [`docs/architecture-overview.md`](../../../docs/architecture-overview.md).

## Dependencies

Internal dependencies, including imports of names that do not exist:

| Import | Source | Resolves | Used by |
| --- | --- | --- | --- |
| `RootState` | `../store` (`frontend/src/store/index.ts:L12`) | Yes | Read in the request interceptor (`api.ts:L2`, `:L16`). Imported and never referenced in `auth.ts:L2` and `collaboration.ts:L2`. |
| `Document`, `DocumentCreate`, `DocumentUpdate` | `../schema/document` | No. The path resolves and all three names are absent | Annotate all three exports (`api.ts:L3`). `collaboration.ts:L3` imports `Document` and never uses it. |
| `User` | `../schema/user` (`frontend/src/schema/user.ts:L13`) | Yes | Return type of `getCurrentUser` (`auth.ts:L3`, `:L25`). |

`frontend/src/schema/document.ts` exports two schema values and no inferred type alias, which is why the compiler cannot find the three `api.ts:L3` names. The sibling [`../schema/README.md`](../schema/README.md) owns that causal chain. Both schema imports here are contract surface, mapped in [`docs/data-model.md`](../../../docs/data-model.md).

External dependencies:

| Package | Imported at | Declared in `frontend/package.json` | Status |
| --- | --- | --- | --- |
| `axios` | `api.ts:L1`, `auth.ts:L1` | No. The seven runtime dependencies sit at `frontend/package.json:L7-L13` | Imported but undeclared |
| `socket.io-client` | `collaboration.ts:L1` | No | Imported but undeclared |

Three of the thirteen undeclared-package import statements in `frontend/src` originate in this directory. The parent [`../README.md`](../README.md) owns the full decomposition. The two packages carry different specification standing. Under its `## FRAMEWORKS AND LIBRARIES` heading the specification declares Axios as a frontend library (`documentation/Technical Specifications.md:L544`), while no file under `documentation/` names `socket.io-client` at all. Both packages reach external services, described in [`docs/integration-guide.md`](../../../docs/integration-guide.md).

## Configuration

| Setting | Read or declared at | Status | Effect |
| --- | --- | --- | --- |
| `REACT_APP_API_BASE_URL` | Read at `api.ts:L5` | READ-BUT-NEVER-DECLARED | Supplies `baseURL` for the shared instance (`api.ts:L9`). The single `process.env` read in all of `frontend/src`. |
| `REACT_APP_API_URL` | Declared at `infrastructure/docker/docker-compose.yml:L11` as `http://backend:5000` | DECLARED-BUT-NEVER-READ | No module reads the name, so the injected value never reaches the client. |
| `Content-Type: application/json` | Set at `api.ts:L12` | Hard-coded default | Applies to every request the shared instance sends. |
| `localStorage` key `accessToken` | Written at `auth.ts:L9`, removed at `auth.ts:L19` | Hard-coded key | The only client-side token store. No module reads the key back. |
| Socket.IO origin | `io()` at `collaboration.ts:L10` | Implicit | Called with no URL, so the client targets the page origin rather than a configured host. |

The two environment variable names do not match, so `API_BASE_URL` at `api.ts:L5` evaluates to `undefined` and every request from the shared instance resolves against the page origin. Prerequisites and runtime versions live in [`docs/onboarding.md`](../../../docs/onboarding.md).

## Data Flows

One document request travels from a page, through an exported function, into the shared instance, and stops at the request interceptor. `api.ts:L16` reads `(store.getState() as RootState).auth.token`, and the expression fails twice over. No module imports `store` into `api.ts`, so the identifier is undefined at call time. The `auth` property is also absent, because `frontend/src/store/index.ts:L6-L9` registers only the reducer keys `document` and `user`. A reader who adds the missing import still gets a failure on the absent key.

The other two modules do not use the shared instance. `auth.ts:L1` imports the bare Axios global, so its three requests carry neither the configured base URL nor the bearer header. `collaboration.ts` has no importer anywhere in `frontend/src`, so nothing constructs the class and no traffic leaves it.

```mermaid
sequenceDiagram
    participant Page as Page (Editor.tsx)
    participant Fn as getDocuments (api.ts:L38)
    participant Api as api instance (api.ts:L36)
    participant Int as request interceptor (api.ts:L14-L23)
    participant Srv as FastAPI server

    Page->>Fn: call getDocuments()
    Fn->>Api: api.get('/documents') (api.ts:L39)
    Api->>Int: run request interceptor
    Int--xInt: BREAKS at api.ts:L16<br/>store never imported,<br/>no 'auth' reducer key
    Int--xSrv: GET /documents, never sent
    Int-->>Page: rejected promise
    Note over Int,Srv: no request reaches the server
```

## Design Patterns

Three patterns shape the directory. The module-level singleton client appears in `api.ts`, where `createApiClient` runs once at module evaluation and assigns its result to `api` (`api.ts:L36`). Every exported function in the file shares that one instance rather than building its own.

The request interceptor pattern carries bearer token injection. `api.ts:L14-L23` registers a function that reads a token, sets an `Authorization: Bearer` header when one is present (`api.ts:L18`), and returns the config. A second interceptor handles responses at `api.ts:L25-L31`, and passes both branches through unchanged: `api.ts:L26` returns the response as received, and `api.ts:L29` re-rejects the error as received.

The thin service facade pattern covers all three modules. Each exported function wraps exactly one transport call and returns `response.data` with no client-side mapping, caching, or retry. `collaboration.ts` applies the same shape to Socket.IO, where each method wraps a single `emit`.

## Known Limitations

Every item below comes from the committed code. Two of the three modules have no importer, and the third defines one of the four symbols its importers ask for.

`api.ts`:

- `api.ts:L3` imports `Document`, `DocumentCreate` and `DocumentUpdate` from `../schema/document`, and the module exports none of them, so all three annotations fail to resolve.
- `api.ts:L16` reads a `store` binding the module never imports, and reads an `auth` key that `frontend/src/store/index.ts:L6-L9` never registers. Every request through the shared instance fails at the interceptor.
- `createApiClient` at `api.ts:L7` is declared `const` with no `export`, so no other module can build a client.
- The response interceptor at `api.ts:L25-L31` adds no behavior, because both of its branches return their argument unchanged.
- `api.ts:L5` reads `REACT_APP_API_BASE_URL` while `infrastructure/docker/docker-compose.yml:L11` injects `REACT_APP_API_URL`, so `baseURL` is `undefined`.
- Three importers name symbols this module never defines: `getDocument` (`frontend/src/pages/Editor.tsx:L6`), `getTemplates` (`frontend/src/pages/Templates.tsx:L4`) and `updateUserSettings` (`frontend/src/pages/Settings.tsx:L4`). All three imports use the `@/` prefix, which `frontend/tsconfig.json:L10-L16` never maps, so each import fails module resolution before the compiler checks the member name. The parent [`../README.md`](../README.md) owns the alias root cause.
- `api.ts:L48` runs to 110 characters, above the 100-character width the other modules keep.

`auth.ts`:

- `auth.ts:L1` imports the bare Axios global instead of the configured instance, so no request here carries the base URL or the bearer header.
- `auth.ts:L2` imports `RootState` and never references it.
- All three endpoint paths miss the committed server. `auth.ts:L7` calls `/auth/login` against `POST /token` (`backend/app/api/auth.py:L28`), and `auth.ts:L27` calls `/auth/me` against `GET /me` (`backend/app/api/users.py:L8`). No logout route exists anywhere in the backend, so `/auth/logout` at `auth.ts:L18` has no counterpart at all.
- `auth.ts:L8` reads `response.data.accessToken` while `backend/app/api/auth.py:L40` returns `access_token`, so the value stored at `auth.ts:L9` is `undefined`.
- `auth.ts:L19` removes the stored token only after the request succeeds, so a failed logout leaves the token in the browser.
- `auth.ts:L21` logs the logout error and does not rethrow, so the promise resolves and the caller cannot detect the failure.
- `auth.ts:L28` casts the response body to `User` with no validation, so a malformed body passes silently.
- `auth.ts:L12` and `auth.ts:L30` throw generic errors that discard the original cause.
- No module in `frontend/src` imports this file, so none of the three functions runs.

`collaboration.ts`:

- `collaboration.ts:L10` calls `io()` with no URL, so the client connects to the page origin.
- `setupEventListeners` at `collaboration.ts:L14-L19` has a body of comments only, so the client handles no inbound event and can emit without ever receiving.
- `joinDocument`, `leaveDocument` and `sendChanges` (`collaboration.ts:L22`, `:L28`, `:L36`) are each declared `async` and contain no `await`, so every returned promise resolves before any server round trip. The declared type contradicts the runtime behavior.
- The emitted payload does not match the server. `collaboration.ts:L38-L41` sends `{ documentId, changes }` over Socket.IO, while `backend/app/services/collaboration_service.py:L14` declares `connect(self, websocket: WebSocket, document_id: str, user_id: str)` against a FastAPI `WebSocket` and `:L59` declares `broadcast_change(self, document_id: str, change: dict)`. No WebSocket route exists in `backend/app/api/` or `backend/app/main.py`, so the collaboration path is unreachable from both ends.
- `collaboration.ts:L2` imports `RootState` and `collaboration.ts:L3` imports the absent `Document` type, and the module references neither.
- `collaboration.ts:L49` default-exports the class, and no module in `frontend/src` imports the file, so nothing constructs it.
- Three assistance markers left by the module's authors sit at `collaboration.ts:L15` (inbound event listeners in `setupEventListeners`), `collaboration.ts:L21` (`joinDocument`) and `collaboration.ts:L35` (`sendChanges`).

For the repository-wide defect register, see [`docs/troubleshooting.md`](../../../docs/troubleshooting.md).

## Usage Examples

`api.ts` holds the directory's only three real exports. A page imports just one of them, `updateDocument` (`frontend/src/pages/Editor.tsx:L6`), while `getDocuments` and `createDocument` have no importer at all. Each example below matches the declared signature at its cited line.

```typescript
import { getDocuments, createDocument, updateDocument } from '../services/api';

// getDocuments takes no arguments (api.ts:L38).
const documents = await getDocuments();

// createDocument takes one DocumentCreate argument (api.ts:L43).
const created = await createDocument({ title: 'Quarterly report', content: '' });

// updateDocument takes an id and a DocumentUpdate body (api.ts:L48).
const updated = await updateDocument(created.id, { content: 'First paragraph.' });
```

None of the three calls above completes today. The interceptor at `api.ts:L16` throws on the undefined `store` binding before any request leaves the instance. `axios` is also absent from `frontend/package.json:L7-L13`, so the module does not resolve at build time.

The `CollaborationService` class is reachable only through its default export:

```typescript
import CollaborationService from '../services/collaboration';

const collaboration = new CollaborationService();
await collaboration.joinDocument('doc-123'); // collaboration.ts:L22
await collaboration.sendChanges({ blocks: [] }); // collaboration.ts:L36
```

Both calls resolve without reaching a server, because `collaboration.ts:L22` and `:L36` contain no `await` and no WebSocket route exists in `backend/app/api/` or `backend/app/main.py`.

Work this directory needs, ordered so that unblocking comes first:

1. An inferred `Document` type exported from `frontend/src/schema/document.ts`, which the three names at `api.ts:L3` depend on.
2. A single environment variable name shared by `api.ts:L5` and `infrastructure/docker/docker-compose.yml:L11`.
3. A `store` binding and an `auth` reducer key available to `api.ts:L16`.
4. Endpoint paths agreed between `auth.ts:L7`, `:L18`, `:L27` and the committed routers.
5. A server route that terminates the Socket.IO traffic `collaboration.ts:L38-L41` emits.

Each item records a gap rather than a change made here. Setup steps and prerequisites live in [`docs/onboarding.md`](../../../docs/onboarding.md). [`../store/README.md`](../store/README.md) documents the sibling client state.
