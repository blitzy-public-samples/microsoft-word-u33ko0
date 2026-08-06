# frontend/src/store

The store never constructs. `index.ts:L2` imports `documentReducer` and `index.ts:L3` imports `userReducer` as named
bindings, while `documentSlice.ts:L52` and `userSlice.ts:L45` export their reducer as the default. Those two lines carry the
directory's only two `TS2614` errors, reported as a missing member because both relative paths resolve.

Thirteen import statements across seven consumer modules also ask this directory for a symbol it never exports, and the two
tables under Known Limitations name every one. Every `Lnn` locator below numbers the frozen revision `06be74c`, which
precedes the documentation pass that added comment blocks to the three modules; current `HEAD` numbers each file higher.

## Purpose

The directory composes the single Redux store for the browser application and owns two state trees, one for documents and
one for the signed-in user. `index.ts` calls `configureStore` and exports the store with two derived types.
`documentSlice.ts` and `userSlice.ts` each declare a Redux Toolkit slice holding its state shape, initial state and
synchronous reducers. No module here reaches the network, reads an environment variable or runs an asynchronous operation.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `index.ts` | Module | `index.ts:L1-L15` | Composition root. `configureStore` at L5-L10 registers two reducer keys, `document` at L7 and `user` at L8, and receives `reducer` alone with no `middleware`, `devTools`, `preloadedState` or `enhancers` option. |
| `RootState` | Exported type | `index.ts:L12` | `ReturnType<typeof store.getState>`. Three service modules import the name and one references it. |
| `AppDispatch` | Exported type | `index.ts:L13` | `typeof store.dispatch`. No module in `frontend/src` imports the name. |
| `store` | Default export | `index.ts:L15` | The module's only default binding. `index.tsx:L5` imports it and `index.tsx:L17` passes it to a React Redux `Provider`. |
| `documentSlice.ts` | Module | `documentSlice.ts:L1-L57` | Declares the `document` slice with four state fields at L4-L9 and six reducers. |
| `setCurrentDocument` | Reducer and action | `documentSlice.ts:L22` | Writes `state.currentDocument` from a `Document` payload. The only action a consumer imports. |
| `addRecentDocument` | Reducer and action | `documentSlice.ts:L25` | Prepends the payload and keeps four earlier entries, so the list holds five at most. |
| `setLoading` | Reducer and action | `documentSlice.ts:L28` | Writes `state.isLoading` from a boolean payload. |
| `setError` | Reducer and action | `documentSlice.ts:L31` | Declares `PayloadAction<string \| null>`, so `setError(null)` clears the document error. |
| `clearCurrentDocument` | Reducer and action | `documentSlice.ts:L34` | Sets `state.currentDocument` to null. Takes no `action` parameter. |
| `clearRecentDocuments` | Reducer and action | `documentSlice.ts:L37` | Empties `state.recentDocuments`. Takes no `action` parameter. |
| Document action creators | Named export | `documentSlice.ts:L43-L50` | Destructures all six creators from `documentSlice.actions`. |
| Document reducer | Default export | `documentSlice.ts:L52` | `documentSlice.reducer`, exported under no other name. |
| `userSlice.ts` | Module | `userSlice.ts:L1-L52` | Declares the `user` slice with four state fields at L4-L9 and four reducers. |
| `setUser` | Reducer and action | `userSlice.ts:L22` | Writes four fields at L23-L26: the user, `isAuthenticated` true, `isLoading` false and a null error. |
| `clearUser` | Reducer and action | `userSlice.ts:L28` | Resets the same four fields at L29-L32. Takes no `action` parameter. |
| `setLoading` | Reducer and action | `userSlice.ts:L34` | Writes `state.isLoading` from a boolean payload. |
| `setError` | Reducer and action | `userSlice.ts:L37` | Declares `PayloadAction<string>`, narrower than `documentSlice.ts:L31`, so no payload clears the user error. Also sets `isLoading` false at L39. |
| User action creators | Named export | `userSlice.ts:L44` | Destructures `setUser`, `clearUser`, `setLoading` and `setError` on one line. |
| User reducer | Default export | `userSlice.ts:L45` | `userSlice.reducer`, exported under no other name. |

## Architecture Fit

The directory sits between the presentation layer and the service clients. Pages and components read state from it and
dispatch actions into it, and the three service modules import its `RootState` type to describe the state they read. The
two slices depend downward on the Zod contracts in `../schema`, and no module here imports a page or a component.

The in-repository specification serves as a point of comparison rather than a source of truth. Its
`## FRAMEWORKS AND LIBRARIES` heading names Redux as the state management library for the frontend at
`documentation/Technical Specifications.md:L542`, and the committed code matches that placement through Redux Toolkit,
declared at `frontend/package.json:L7`. The same file's `### Frontend Components` diagram at `:L183-L199` names fifteen
nodes and includes no state-management node, so the specification names Redux without placing the store in its diagram. See
the [architecture overview](../../../docs/architecture-overview.md) and the [frontend source README](../README.md).

## Dependencies

### Internal

| Importer | Imported name and path | Location | Status |
| --- | --- | --- | --- |
| `index.ts` | `documentReducer` from `./documentSlice` | `index.ts:L2` | Fails. `documentSlice.ts:L52` exports the reducer as the default and declares no `documentReducer`. |
| `index.ts` | `userReducer` from `./userSlice` | `index.ts:L3` | Fails. `userSlice.ts:L45` exports the reducer as the default and declares no `userReducer`. |
| `documentSlice.ts` | `Document` from `../schema/document` | `documentSlice.ts:L2` | Fails. `schema/document.ts` exports two schema values and no inferred type. |
| `userSlice.ts` | `User` from `../schema/user` | `userSlice.ts:L2` | Resolves against `schema/user.ts:L13`. |

One missing export line separates the last two rows. `schema/user.ts:L13` declares `export type User`, so `userSlice.ts:L2`
resolves, and `schema/document.ts` declares no equivalent, so `documentSlice.ts:L2` does not. The
[schema README](../schema/README.md) owns that causal chain, and the
[data model reference](../../../docs/data-model.md) consolidates the contract drift the slices carry.

### External

| Package | Declared in `frontend/package.json` | Imported at | Status |
| --- | --- | --- | --- |
| `@reduxjs/toolkit` | `^1.9.5` at L7 | `index.ts:L1`, `documentSlice.ts:L1`, `userSlice.ts:L1` | Declared and resolving |
| `react-redux` | `^8.0.5` at L10 | Not imported in this directory | Declared. The consuming pages, components and `index.tsx:L3` import it instead. |

The three modules import one third-party package between them, and `frontend/package.json:L7` declares it. The directory
therefore imports no undeclared package, which sets it apart from `../schema`, `../services` and `../utils`.

## Configuration

The three modules read no environment variable and no configuration file. No `process.env` reference appears in any of
them. The values below are the fixed constants the slices hold, and source sets each one.

| Setting | Value | Where set |
| --- | --- | --- |
| Recent-document list length | Five entries at most | `documentSlice.ts:L26` |
| Document slice initial state | `currentDocument` null, `recentDocuments` empty, `isLoading` false, `error` null | `documentSlice.ts:L11-L16`, fields at L12-L15 |
| User slice initial state | `currentUser` null, `isAuthenticated` false, `isLoading` false, `error` null | `userSlice.ts:L11-L16`, fields at L12-L15 |
| Slice names | `'document'` and `'user'` | `documentSlice.ts:L19`, `userSlice.ts:L19` |
| Middleware, dev tools, preloaded state | None passed | `index.ts:L5-L10` |
| Environment variables | None read | No `process.env` reference in the directory |

## Data Flows

One path through the directory is traceable end to end, and a single action drives it. `pages/Editor.tsx:L8` imports
`setCurrentDocument`, `pages/Editor.tsx:L23` dispatches it with the record fetched at `:L21`, and the reducer at
`documentSlice.ts:L22` writes `state.currentDocument`. `RootState` at `index.ts:L12` then types that state for
`services/api.ts:L2`.

The path stops at both ends. No dispatch reaches a reducer, because `index.ts:L2-L3` name reducers the slices do not
export. The read side stops for a second reason: `services/api.ts:L16` reads `.auth.token` off `RootState`, and
`index.ts:L6-L9` registers `document` and `user` only. The other five document actions and all four user actions have no
importer anywhere in `frontend/src`.

```mermaid
graph TD
    RTK["@reduxjs/toolkit configureStore<br/>index.ts:L1"] --> STORE["store<br/>index.ts:L5-L10"]
    DSLICE["documentSlice.ts<br/>reducer is the default export, L52"]
    USLICE["userSlice.ts<br/>reducer is the default export, L45"]
    DSLICE -.->|"index.ts:L2 asks for named documentReducer"| STORE
    USLICE -.->|"index.ts:L3 asks for named userReducer"| STORE
    STORE --> DKEY["reducer key 'document'<br/>index.ts:L7"]
    STORE --> UKEY["reducer key 'user'<br/>index.ts:L8"]
    STORE -.->|"api.ts:L16 reads auth.token"| AKEY["reducer key 'auth'<br/>never registered"]
    STORE --> RS["RootState<br/>index.ts:L12"]
    RS --> SVC["services/api.ts:L2<br/>auth.ts:L2, collaboration.ts:L2"]
%% Dashed edges mark unresolved imports and a reducer key the store never registers
```

## Design Patterns

Unidirectional single store. One `configureStore` call at `index.ts:L5-L10` holds all shared client state, and a consumer
changes that state by dispatching an action rather than by writing to it. `index.tsx:L17` passes the store to a React Redux
`Provider`, the single point where the component tree gains access.

Slice per domain. Each slice declares its state shape, initial state and reducers in one module. `documentSlice.ts:L18-L41`
covers documents and `userSlice.ts:L18-L42` covers the user, and neither slice reads the other's state.

Draft mutation through Immer. Every reducer in both slices assigns to a field on `state` and returns nothing, as
`documentSlice.ts:L23` and `userSlice.ts:L23-L26` show. Redux Toolkit hands the reducer a draft object and derives the next
state from the recorded assignments, so the assignment is the output.

Typed selector composition. `RootState` at `index.ts:L12` derives the state type from the store rather than from a
hand-written interface, so a selector receives the shape the reducer map produces. `pages/Editor.tsx:L15` writes an inline
selector against that shape, reading `state.document.currentDocument`.

## Known Limitations

Every defect below sits in the committed code, and none is repaired here. Two absent hooks and three absent slice members
account for thirteen failing import statements across seven consumer modules, so the tables come first.

Seven modules import a store hook that `index.ts` does not define, each through the `@/store` path:

| # | Importing module | Line | Symbols imported |
| --- | --- | --- | --- |
| 1 | `pages/Editor.tsx` | L7 | `useAppSelector`, `useAppDispatch` |
| 2 | `pages/Settings.tsx` | L5 | `useAppSelector`, `useAppDispatch` |
| 3 | `pages/Templates.tsx` | L5 | `useAppSelector` |
| 4 | `pages/Home.tsx` | L5 | `useAppSelector` |
| 5 | `components/Header.tsx` | L3 | `useAppSelector` |
| 6 | `components/DocumentCanvas.tsx` | L3 | `useAppSelector`, `useAppDispatch` |
| 7 | `components/Toolbar.tsx` | L3 | `useAppDispatch` |

`index.ts:L1-L3` imports nothing from `react-redux`, so the module could not re-export either hook as committed.

Four modules import `selectCurrentUser`, and one also imports `updateUser`, each through `@/store/userSlice`:

| # | Importing module | Line | Symbols imported |
| --- | --- | --- | --- |
| 1 | `pages/Settings.tsx` | L6 | `selectCurrentUser`, `updateUser` |
| 2 | `pages/Templates.tsx` | L6 | `selectCurrentUser` |
| 3 | `pages/Home.tsx` | L6 | `selectCurrentUser` |
| 4 | `components/Header.tsx` | L4 | `selectCurrentUser` |

- **The store never constructs.** `index.ts:L2` and `:L3` import `documentReducer` and `userReducer`, while
  `documentSlice.ts:L52` and `userSlice.ts:L45` export their reducer as the default. Both identifiers appear nowhere else in
  `frontend/src`. The [frontend source README](../README.md) holds the full type-check profile.
- **No `auth` reducer key exists, and a request interceptor reads one.** `index.ts:L6-L9` registers `document` at L7 and
  `user` at L8. `services/api.ts:L16` reads `(store.getState() as RootState).auth.token` for its `Authorization` header.
- **`updateDocument` and `selectCurrentDocument` are absent from `documentSlice.ts`.** `components/DocumentCanvas.tsx:L4`
  imports both and dispatches `updateDocument` at `:L26`, and `components/Toolbar.tsx:L4` imports it and dispatches it at
  `:L15` and `:L20`. The slice exports six creators at `documentSlice.ts:L43-L50` and neither name is among them. A separate
  `updateDocument` is an application programming interface (API) client function at `services/api.ts:L48`, imported at
  `pages/Editor.tsx:L6`; the two names are unrelated.
- **`userSlice.ts` exports neither `selectCurrentUser` nor `updateUser`.** `userSlice.ts:L44` exports `setUser`,
  `clearUser`, `setLoading` and `setError`, and no consumer imports any of those four. Every module reaching for user state
  reaches for one of the two absent names in the table above.
- **`documentSlice.ts:L2` imports a `Document` type that `../schema/document` does not export.** The path resolves and the
  member does not exist. The [schema README](../schema/README.md) traces the chain to the one missing export line.
- **`addRecentDocument` caps the recent list at five, and the literal in the code reads `4`.** `documentSlice.ts:L26`
  prepends the payload to `state.recentDocuments.slice(0, 4)`, keeping four earlier entries beside the new one. No named
  constant carries the limit and no configuration changes it.
- **`AppDispatch` is exported and unused.** `index.ts:L13` declares the type, and no module imports the name. The four
  `useAppDispatch()` call sites at `pages/Editor.tsx:L14`, `pages/Settings.tsx:L13`,
  `components/DocumentCanvas.tsx:L11` and `components/Toolbar.tsx:L11` call the absent hook rather than use the type.
- **The two slices treat a cleared error differently.** `documentSlice.ts:L31` declares `PayloadAction<string | null>`, so
  `setError(null)` clears the document error. `userSlice.ts:L37` declares `PayloadAction<string>`, so no payload clears the
  user error and only `clearUser` at `userSlice.ts:L28` resets it. `userSlice.ts:L39` also sets `isLoading` to `false`,
  which `documentSlice.ts:L31-L33` does not.
- **`App.tsx` imports the store under a name the module does not export.** `frontend/src/App.tsx:L10` writes
  `import { store } from '@/store/index'`, a named import of a default-only export. `frontend/src/index.tsx:L5` writes
  `import store from '@/store'` and gets the form right.
- **Both slices carry an end-of-file assistance marker.** `documentSlice.ts:L54-L57` and `userSlice.ts:L47-L52` each sit
  after the export statements. The user-slice marker names the missing `updateUser` action at `:L50` and the missing
  selectors at `:L51`.

The [troubleshooting register](../../../docs/troubleshooting.md) carries every defect above with file and line evidence.

## Usage Examples

No dispatch below executes today, because `store/index.ts:L2-L3` import reducer names the two slices never export and the
store never constructs. The [onboarding guide](../../../docs/onboarding.md) carries the prerequisites and runtime versions.

Dispatching a document action uses the six creators exported at `documentSlice.ts:L43-L50`, with payload fields from
`DocumentSchema` at `schema/document.ts:L3-L11`:

```typescript
import store from '../store';
import { setCurrentDocument, addRecentDocument, setError } from '../store/documentSlice';

const doc = {
  id: 'doc-1', title: 'Quarterly report', content: '', owner_id: 'user-1',
  created_at: new Date(), updated_at: new Date(), collaborators: [],
};

store.dispatch(setCurrentDocument(doc));
store.dispatch(addRecentDocument(doc));
store.dispatch(setError(null));
```

A sixth `addRecentDocument` dispatch drops the oldest entry, because `documentSlice.ts:L26` retains four. `setError(null)`
clears the document error, because `documentSlice.ts:L31` accepts null.

Dispatching a user action uses the four creators exported on `userSlice.ts:L44`, with payload fields from `UserSchema` at
`schema/user.ts:L3-L11`:

```typescript
import store from '../store';
import { setUser, setLoading, clearUser } from '../store/userSlice';

store.dispatch(setLoading(true));
store.dispatch(setUser({
  id: 'user-1', email: 'editor@example.com', username: 'editor',
  full_name: 'Sample Editor', created_at: new Date(),
  is_active: true, is_superuser: false,
}));
store.dispatch(clearUser());
```

`setUser` also sets `isAuthenticated` to true and clears the error at `userSlice.ts:L24-L26`. `clearUser` at
`userSlice.ts:L28` is the one path that clears the user error.

Three gaps block the directory, recorded here rather than repaired, widest first. `index.ts` lacks the `useAppSelector` and
`useAppDispatch` hooks that seven modules import, and its reducer imports at L2-L3 do not match the default exports at
`documentSlice.ts:L52` and `userSlice.ts:L45`. `documentSlice.ts` lacks the `updateDocument` action that
`components/DocumentCanvas.tsx` and `components/Toolbar.tsx` import. The slices lack the two selectors five modules import.
