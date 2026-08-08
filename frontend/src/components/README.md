# frontend/src/components

## Purpose

Eight React function components live here, and together they supply every part of the editor screen except the routed pages.
`Header` and `Footer` render the application chrome. `Sidebar` renders the panel shell, and `Toolbar` renders the formatting
controls. `DocumentCanvas` and `TextEditor` each wrap a Draft.js editing surface, where Draft.js is the rich-text framework
the editor is built on. `TableEditor` and `ImageEditor` hold insert logic for tables and images and render no interface at
all.

The directory measures 524 lines, 299 of them committed at `06be74c`. Seven of the eight cannot compile, because five modules
and five store symbols they import do not exist. `Footer` is the exception, and the sections below name it as the one clean
reference point.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `Header` | React component, default export | `Header.tsx:L30` | Top navigation bar: branding, three links, and either a profile block or a login link. Propless. |
| `Footer` | React component, default export | `Footer.tsx:L21` | Status bar with five literal values and two zoom buttons. Propless, and the only component here that typechecks. |
| `Sidebar` | React component, default export | `Sidebar.tsx:L22` | Panel shell that renders three child panels unconditionally. Propless. |
| `Toolbar` | React component, default export | `Toolbar.tsx:L34` | Three button groups: inline styles, block styles, and two insert buttons. Propless, and holds no editor state. |
| `TextEditor` | React component, default export | `TextEditor.tsx:L23` | Self-contained Draft.js editor driven by key commands. Propless. No module imports it. |
| `handleKeyCommand` | Internal handler | `TextEditor.tsx:L41` | Maps a Draft.js key command to one of the two formatting helpers, passing both declared arguments. |
| `DocumentCanvas` | React component, default export | `DocumentCanvas.tsx:L34` | Draft.js editor bound to the document in the Redux store. Declared propless, while its one caller passes two props. |
| `handleEditorChange` | Internal handler | `DocumentCanvas.tsx:L57` | Stores the new editor state at `:L58`, then calls the serializer at `:L59` with the wrong type and raises. The dispatch at `:L60` never runs. |
| `TableEditor` | React component, default export | `TableEditor.tsx:L28` | Table insert logic. Takes props. Renders an empty element. |
| `handleInsertTable` | Internal handler | `TableEditor.tsx:L42` | Builds a table and pushes it into the editor state. Defined and never called. |
| `ImageEditor` | React component, default export | `ImageEditor.tsx:L29` | Image insert logic. Takes props. Renders an empty element. |
| `handleInsertImage` | Internal handler | `ImageEditor.tsx:L41` | Creates an `IMAGE` entity and inserts an atomic block. Defined and never called. |
| `TableEditorProps` | Props interface, not exported | `TableEditor.tsx:L15-L17` | Declares one required member, `editorState: EditorState`. |
| `ImageEditorProps` | Props interface, not exported | `ImageEditor.tsx:L15-L17` | Declares one required member, `editorState: EditorState`. |

Only `TableEditor` and `ImageEditor` declare a props interface, and the other six are propless. `DocumentCanvas` is the one
whose propless declaration contradicts its caller, which Known Limitations reads against
`frontend/src/pages/Editor.tsx:L102`.

## Architecture Fit

These components sit below the routed pages and above the Redux store and the shared utilities.
`frontend/src/pages/Editor.tsx` composes three of them, rendering `Toolbar` at `Editor.tsx:L100`, `DocumentCanvas` at
`Editor.tsx:L102` and `Sidebar` at `Editor.tsx:L103`. `frontend/src/App.tsx` composes the chrome, rendering `Header` at
`App.tsx:L38` and `Footer` at `App.tsx:L47`.

The container and presentational split is partial, because three of the eight reach the store themselves rather than taking
data from the page that renders them. `Header.tsx:L31` selects the current user, `Toolbar.tsx:L35` takes a dispatcher, and
`DocumentCanvas.tsx:L35-L36` takes both. See [the architecture overview](../../../docs/architecture-overview.md) for the
wider system and [the frontend source README](../README.md) for the routing above it.

The committed layout differs from the declared design, and each difference is checkable. Intended behavior per
documentation/Technical Specifications.md, "USER INTERFACE DESIGN" heading: `App` composes `Header`, `Toolbar`,
`DocumentCanvas`, `Sidebar` and `Footer` (`Technical Specifications.md:L455-L459`). `TextEditor`, `TableEditor` and
`ImageEditor` sit under `DocumentCanvas` (`:L470-L472`). `StylesPanel`, `CommentsPanel` and `VersionHistoryPanel` sit under
`Sidebar` (`:L474-L476`), and `StatusBar` and `ZoomControls` sit under `Footer` (`:L478-L479`).

The committed code matches that placement for `Header` and `Footer` and departs from it elsewhere. `App.tsx` renders only the
chrome, so `Toolbar`, `DocumentCanvas` and `Sidebar` reach the screen through `pages/Editor.tsx` instead.
`DocumentCanvas.tsx:L65` renders a Draft.js `Editor` directly and composes no child, so `TextEditor`, `TableEditor` and
`ImageEditor` sit outside it. `Sidebar.tsx:L10-L12` imports `StylePanel`, `CommentPanel` and `RevisionPanel`, three names
that differ from the three the diagram declares, and all three modules are absent. `Footer.tsx` inlines its status and zoom
markup rather than composing two children.

Two further statements of intent have no committed counterpart. The `ToolbarProps` interface at `Technical
Specifications.md:L487-L491` declares `onBoldClick`, `onItalicClick` and `onUnderlineClick`, and `:L493` types the component
`React.FC<ToolbarProps>`. The committed `Toolbar` at `Toolbar.tsx:L34` is propless and reaches the store through a dispatch.
`Technical Specifications.md:L521` declares that the interface will follow Fluent Design System principles.
`frontend/package.json` declares no component library and no design system.

## Dependencies

### Internal

| Import | Imported at | State |
| --- | --- | --- |
| `@/components/StylePanel` | `Sidebar.tsx:L10` | Module absent |
| `@/components/CommentPanel` | `Sidebar.tsx:L11` | Module absent |
| `@/components/RevisionPanel` | `Sidebar.tsx:L12` | Module absent |
| `@/utils/tableUtils` | `TableEditor.tsx:L12` | Module absent |
| `@/utils/imageUtils` | `ImageEditor.tsx:L12` | Module absent |
| `useAppSelector` | `Header.tsx:L12`, `DocumentCanvas.tsx:L16` | Symbol absent from `@/store` |
| `useAppDispatch` | `Toolbar.tsx:L16`, `DocumentCanvas.tsx:L16` | Symbol absent from `@/store` |
| `selectCurrentUser` | `Header.tsx:L13` | Symbol absent from `@/store/userSlice` |
| `selectCurrentDocument` | `DocumentCanvas.tsx:L17` | Symbol absent from `@/store/documentSlice` |
| `updateDocument` | `Toolbar.tsx:L17`, `DocumentCanvas.tsx:L17` | Symbol absent from `@/store/documentSlice` |
| `@/utils/formatting` | `Toolbar.tsx:L15`, `TextEditor.tsx:L16` | Module present, both functions exported |
| `@/utils/documentUtils` | `DocumentCanvas.tsx:L18` | Module present, both functions exported |

The five absent symbols are absent by inspection of the modules that would export them. `frontend/src/store/index.ts` exports
exactly three names, and neither hook is among them: `RootState` at `store/index.ts:L32`, `AppDispatch` at `:L34`, and
`store` as a default at `:L36`. `frontend/src/store/documentSlice.ts:L84` destructures exactly `setCurrentDocument`,
`addRecentDocument`, `setLoading`, `setError`, `clearCurrentDocument` and `clearRecentDocuments`, so it publishes no
`updateDocument` action and no `selectCurrentDocument` selector. `frontend/src/store/userSlice.ts:L75` destructures exactly
`setUser`, `clearUser`, `setLoading` and `setError`, so it publishes no `selectCurrentUser`. See [the store
README](../store/README.md) and [the utils README](../utils/README.md) for those two directories.

Every specifier in the table above carries the `@/` prefix, and `frontend/tsconfig.json:L10-L16` declares five path aliases
that do not include it: `@components/*`, `@utils/*`, `@styles/*`, `@hooks/*` and `@services/*`. Each `@/` specifier therefore
fails to resolve, which masks every symbol-level fault behind a module-level one.

### External

| Package | Declared | How this directory needs it |
| --- | --- | --- |
| `react ^18.2.0` | `frontend/package.json:L8` | Imported by all eight components |
| `react-redux ^8.0.5` | `frontend/package.json:L10` | Reached indirectly, through the absent store hooks |
| `react-router-dom ^6.11.1` | `frontend/package.json:L11` | Imported at `Header.tsx:L11`, for `Link` |
| `draft-js` | Absent from the manifest | Imported at `DocumentCanvas.tsx:L15`, `ImageEditor.tsx:L11`, `TableEditor.tsx:L11` and `TextEditor.tsx:L15` |
| `@types/draft-js` | Absent from the manifest | Not imported anywhere. Required as a development dependency, because `draft-js` ships no TypeScript declarations of its own |

The two Draft.js packages are undeclared for different reasons, and the distinction matters when somebody repairs the
manifest. `draft-js` is a **runtime import**: four modules in this directory name it in an `import` statement, and six name
it across `frontend/src/` as a whole. `@types/draft-js` is a **type-declaration package** that no source file imports.
TypeScript resolves the `draft-js` declarations from it rather than from an import, so a grep for the name finds nothing
while `tsc` still needs the package installed.

`frontend/package.json:L6-L14` lists exactly seven runtime dependencies: `@reduxjs/toolkit`, `react`, `react-dom`,
`react-redux`, `react-router-dom`, `tailwindcss` and `typescript`. Neither Draft.js package appears there or in the
development dependencies. Four of the thirteen undeclared-package `TS2307` errors originate here, one for each module that
imports `draft-js`. See [the frontend source README](../README.md) for the repository-wide error profile, which this file
does not restate. The `FRAMEWORKS AND LIBRARIES` heading in `documentation/Technical Specifications.md` lists Draft.js as a
frontend library at `:L545`, while the manifest declares it nowhere.

`Header` and `DocumentCanvas` each read a contract that the server side also models. See [the data model
reference](../../../docs/data-model.md) for the field drift they inherit.

## Configuration

No component in this directory reads `process.env`, and none takes a configuration file, an environment variable or a
build-time constant. The nearest equivalent is a set of literal display values in `Footer.tsx`, which a reader is likely to
mistake for computed state.

| Value | Location | Note |
| --- | --- | --- |
| `Words: 0` | `Footer.tsx:L25` | Literal text, not a computed word count |
| `Pages: 1` | `Footer.tsx:L26` | Literal text, not a computed page count |
| `100%` | `Footer.tsx:L30` | Literal zoom level |
| `Last saved: Just now` | `Footer.tsx:L34` | Literal text, unconnected to any save path |
| `Collaborators: 1` | `Footer.tsx:L35` | Literal text, unconnected to any collaboration path |
| Zoom out and zoom in buttons | `Footer.tsx:L29`, `:L31` | Neither declares `onClick`, so clicking does nothing |

All five values are hard-coded, and no handler connects either zoom button to the level.

## Data Flows

The Draft.js `EditorState`, an immutable snapshot of editor content plus selection, is the one value moving through this
directory, and `DocumentCanvas` alone moves it in both directions. A load effect reads `currentDocument.content` from the
Redux store, passes the string to `deserializeDocument` at `DocumentCanvas.tsx:L42`, then hands the result to
`EditorState.createWithContent` at `DocumentCanvas.tsx:L43`.

The reverse path stops at its first step. `DocumentCanvas.tsx:L58` replaces the local editor state, then `:L59` calls
`serializeDocument` with the `ContentState` that `getCurrentContent()` returned, while `documentUtils.ts:L29` declares that
parameter an `EditorState`. The helper's first statement reads `getCurrentContent` on the value it received, and a
`ContentState` declares no such method, so the call raises a `TypeError` before any conversion runs. Nothing downstream
executes: no `convertToRaw`, no `JSON.stringify`, and no dispatch at `DocumentCanvas.tsx:L60`. Both directions carry a type
error, and Known Limitations reads the two together, while [the pages README](../pages/README.md) covers the page that mounts
these components.

```mermaid
graph TD
    accTitle: The editor component tree and the EditorState journey
    accDescr: Dashed edges mark a relationship that cannot resolve, including the three named imports of default exports the page uses, the store read through an absent hook, and the two inverse type errors on the outbound and inbound halves of one round trip. The thick edge marks the one helper call supplying both declared arguments. A solid edge downstream of a dashed one describes intended shape only, because nothing past the first dashed edge runs. Every node names its own file.
    PAGE["pages/Editor.tsx<br/>renders at<br/>Editor.tsx:L100-L103"]
    STORE["Redux store<br/>currentDocument<br/>.content"]
    PAGE -.->|"named import of a<br/>default export,<br/>Editor.tsx:L13"| TB["Toolbar<br/>Toolbar.tsx:L34"]
    PAGE -.->|"named import of a<br/>default export,<br/>Editor.tsx:L15"| SB["Sidebar<br/>Sidebar.tsx:L22"]
    PAGE -.->|"named import of a<br/>default export,<br/>Editor.tsx:L14, and<br/>two props to a<br/>propless component"| DC["DocumentCanvas<br/>DocumentCanvas.tsx:L34"]
    STORE -.->|"read through<br/>useAppSelector, which<br/>the store folder does<br/>not export"| DC
    DC --> DES["deserializeDocument<br/>documentUtils.ts:L49,<br/>returns an EditorState"]
    DES -.->|"FIRST INVERSION:<br/>DocumentCanvas.tsx:L42<br/>and :L43 send an<br/>EditorState where a<br/>ContentState belongs"| CWC["EditorState<br/>.createWithContent<br/>DocumentCanvas.tsx:L43"]
    CWC --> ED["Draft.js Editor<br/>rendered at<br/>DocumentCanvas.tsx:L65"]
    ED --> GCC["getCurrentContent()<br/>returns a<br/>ContentState"]
    GCC -.->|"SECOND INVERSION,<br/>TERMINAL:<br/>DocumentCanvas.tsx:L59<br/>sends a ContentState<br/>where an EditorState<br/>belongs, so the helper<br/>raises on<br/>getCurrentContent"| SER["serializeDocument<br/>documentUtils.ts:L29,<br/>accepts an EditorState"]
    SER -.->|"never reached:<br/>no convertToRaw,<br/>no JSON.stringify,<br/>no dispatch"| DIS["dispatch<br/>DocumentCanvas.tsx:L60"]

    TE["TextEditor<br/>TextEditor.tsx:L23"]
    PAGE -.->|"no module<br/>imports TextEditor"| TE
    TE ==>|"TextEditor.tsx:L48<br/>and :L55 pass<br/>both arguments"| FMT["utils/formatting.ts<br/>:L24 and :L45 declare<br/>two parameters each"]
    TB -.->|"Toolbar.tsx:L45<br/>and :L56 pass<br/>one argument"| FMT
    SB -.->|"Sidebar.tsx:L10, :L11<br/>and :L12, all three<br/>modules absent"| SP["StylePanel,<br/>CommentPanel,<br/>RevisionPanel"]
    ORPH["TableEditor.tsx:L28 and ImageEditor.tsx:L29<br/>no module imports either, and<br/>TableEditor.tsx:L12 and ImageEditor.tsx:L12<br/>import utils/tableUtils and utils/imageUtils,<br/>which are absent modules"]

%% Dashed edges mark a relationship that cannot resolve or a type that does not match.
%% The thick edge marks the one helper call supplying both declared arguments.
```

## Design Patterns

**Container and presentational split, with store access through hooks and selectors.** `DocumentCanvas` and `Toolbar` reach
the Redux store directly, at `DocumentCanvas.tsx:L35-L36` and `Toolbar.tsx:L35`, and `Header` reads it at `Header.tsx:L31`.
Each of the three calls a typed hook at module scope and passes a named selector to it rather than receiving data as props.
`Footer`, `TextEditor`, `TableEditor` and `ImageEditor` hold no store connection, and `Footer.tsx` imports nothing beyond
React.

**Controlled Draft.js editor state.** `TextEditor.tsx:L24` and `DocumentCanvas.tsx:L37` each seed local state with
`EditorState.createEmpty()` and pass that state to the Draft.js `Editor` with an `onChange` callback. The editor holds no
state of its own, so every keystroke returns through the component.

**Atomic block insertion.** `ImageEditor.tsx:L43-L52` creates an immutable `IMAGE` entity on the content state, reads the
generated entity key at `:L48`, and calls `AtomicBlockUtils.insertAtomicBlock` at `:L52` to place the block. Draft.js renders
an atomic block through a block renderer the editor supplies.

## Known Limitations

### The two formatting-helper call sites

`Toolbar` and `TextEditor` call the same two helpers, and the two call sites disagree on argument count. Both helper
signatures declare two parameters and return an `EditorState`:

- `formatting.ts:L24` declares `applyInlineStyle(editorState: EditorState, inlineStyle: string): EditorState`, returning the
pushed state at `formatting.ts:L34`.
- `formatting.ts:L45` declares `applyBlockStyle(editorState: EditorState, blockType: string): EditorState`, returning the
pushed state at `formatting.ts:L55`.

`TextEditor` supplies both declared arguments. `TextEditor.tsx:L48` calls `applyInlineStyle(editorState, command)` and `:L55`
calls `applyBlockStyle(editorState, command)`. Its block-type cases at `:L50-L54` name `header-one`, `header-two`,
`blockquote`, `unordered-list-item` and `ordered-list-item`, which are the spellings `Modifier.setBlockType` accepts.

`Toolbar` supplies one argument to each. `Toolbar.tsx:L45` calls `applyInlineStyle(style)` and `:L56` calls
`applyBlockStyle(style)`, so the style string lands in the `editorState` position. Its constants are lowercase throughout.
`:L74`, `:L75` and `:L76` pass `'bold'`, `'italic'` and `'underline'`, where Draft.js names inline styles `BOLD`, `ITALIC`
and `UNDERLINE`. `:L79`, `:L80` and `:L81` pass `'paragraph'`, `'heading1'` and `'heading2'`, where Draft.js names those
block types `unstyled`, `header-one` and `header-two`.

The contrast covers argument count and block-type spelling, and it stops there. `TextEditor.tsx:L45-L47` matches the
lowercase `bold`, `italic` and `underline` key commands and forwards each one unchanged into the `inlineStyle` parameter.
Those three values therefore reach the helper under the key-command spelling rather than the inline-style spelling.
`TextEditor` is correct on argument count and on block types, and is not a canonical reference for every constant.

Two further facts belong to the same reading. Both helpers declare an `EditorState` return, so `Toolbar.tsx:L45` and `:L56`
bind that declared type to a variable named `updatedContent` and dispatch it as a `content` value. `Toolbar` also holds no
editor state: `:L35` is its only hook call, and the file declares no `useState`, no `useRef` and no editor-state selector, so
nothing supplies the first argument.

### The DocumentCanvas type inversion

`frontend/src/utils/documentUtils.ts:L49` declares `deserializeDocument(serializedContent: string): EditorState`, and `:L29`
declares `serializeDocument(editorState: EditorState): string`. `DocumentCanvas` inverts both. `DocumentCanvas.tsx:L42` binds
the `EditorState` that `deserializeDocument` returns to a variable named `contentState`, and `:L43` passes that value to
`EditorState.createWithContent()`, which accepts a `ContentState`. `:L59` passes `newEditorState.getCurrentContent()`, a
`ContentState`, to `serializeDocument`, which accepts an `EditorState`. The two errors are exact inverses, so correcting
either one alone moves the other further from its declared type.

`DocumentCanvas.tsx:L15` already imports `ContentState`, the type `EditorState.createWithContent()` accepts, and leaves it
unreferenced. Four further facts apply. `:L34` declares a propless `React.FC` while `frontend/src/pages/Editor.tsx:L102`
passes `content` and `onContentChange`.

The change handler pays no serialization cost, because `DocumentCanvas.tsx:L59` raises before the helper converts anything.
No JavaScript Object Notation (JSON) string is built, and the dispatch at `:L60` never runs on any keystroke. `:L16` and
`:L17` import the four absent store symbols, and an assistance marker sits at `:L20`.

### Per-component limitations

**`Header.tsx`, 66 lines.** `Header.tsx:L37` renders `/microsoft-word-logo.png`, and that asset does not exist, because
`frontend/public/` holds only `index.html`. Two of the four links reach a declared route: `Header.tsx:L43` targets `/` and
`:L45` targets `/templates`, declared at `App.tsx:L41` and `:L43`. The other two reach nothing, because `Header.tsx:L44`
targets `/documents` and `:L56` targets `/login`, and `App.tsx` declares neither.

`Header.tsx:L52` reads `currentUser.avatar` and `currentUser.name`, and `:L53` reads `currentUser.name` again. `UserSchema`
declares neither field, and models `username` at `frontend/src/schema/user.ts:L22` and optional `full_name` at
`schema/user.ts:L23`. `Header.tsx:L12` and `:L13` import the absent `useAppSelector` and `selectCurrentUser`.

**`Footer.tsx`, 41 lines.** The file imports nothing beyond React, so it typechecks cleanly and is the one working reference
point here. Its five status values are literal text, listed under Configuration above, and the zoom buttons at
`Footer.tsx:L29` and `:L31` declare no `onClick`.

**`Sidebar.tsx`, 32 lines.** The sidebar cannot render, because all three panel modules are absent. `Sidebar.tsx:L10`, `:L11`
and `:L12` import `@/components/StylePanel`, `@/components/CommentPanel` and `@/components/RevisionPanel`, and `:L25`, `:L26`
and `:L27` render all three behind no guard.

**`TableEditor.tsx`, 75 lines.** `TableEditor.tsx:L12` imports `insertTable`, `deleteTable` and `modifyTable` from the absent
`@/utils/tableUtils`, and `deleteTable` and `modifyTable` are never referenced. `handleInsertTable` at `:L42` is defined and
never called.

`:L50-L54` passes the value `insertTable(rows, columns)` returns at `:L47` as the third argument to `Modifier.replaceText`,
which requires a string. `:L68-L72` returns an empty element holding only a JavaScript XML (JSX) comment at `:L70`. An
assistance marker sits at `:L29`.

**`ImageEditor.tsx`, 67 lines.** `ImageEditor.tsx:L12` imports `resizeImage` and `cropImage` from the absent
`@/utils/imageUtils`, and neither is referenced. `handleInsertImage` at `:L41` is defined and never called. `:L43-L47`
creates an `IMAGE` entity and `:L52` calls `AtomicBlockUtils.insertAtomicBlock`, and no `blockRendererFn` exists anywhere in
the tree, so an atomic image block would not render.

No upload route exists anywhere in the repository to receive image bytes, and `:L61-L63` returns an empty element. Two
assistance markers sit in this file, at `:L30` and `:L59`.

**`TextEditor.tsx`, 78 lines.** No module imports this component, so no page mounts it. `frontend/src/pages/Editor.tsx:L102`
renders `DocumentCanvas` instead, which makes `DocumentCanvas` the editor a reader reaches. `handleKeyCommand` at
`TextEditor.tsx:L41` is the file's second documentable construct, and an assistance marker sits at `:L26`.

One import defect spans the boundary with the pages directory. `frontend/src/pages/Editor.tsx:L12-L15` imports `Header`,
`Toolbar`, `DocumentCanvas` and `Sidebar` as named imports, against four modules that export only defaults, while
`App.tsx:L14-L15` imports `Header` and `Footer` correctly as defaults. The named-import fault stays masked, because the `@/`
specifier does not resolve at all, so the checker reports `TS2307` rather than `TS2614`.

### Accessibility

Every item below is read from the committed markup rather than from a running page, because the client does not bundle. Three
positives hold: `Header.tsx:L34` uses a semantic `header` element and `:L41` a `nav`, `Footer.tsx:L23` uses a semantic
`footer`, and the logo image at `Header.tsx:L37` carries meaningful `alt` text. Every interactive control here is a native
`button`, a React Router `Link` rendering an anchor, or a Draft.js `Editor`, so each is keyboard reachable. The defects:

- **`Header` renders twice per route, so every route exposes two unnamed navigation landmarks.** `App.tsx:L38` renders one
`Header`, and each page renders its own at `pages/Home.tsx:L32`, `pages/Editor.tsx:L98`, `pages/Templates.tsx:L78` and
`pages/Settings.tsx:L61`. Both copies present the same `nav` at `Header.tsx:L41` with no `aria-label`, so assistive
technology announces two identical navigation regions and a reader cannot tell them apart. Distinct accessible names on each
`nav` are required, and the duplicate render is the defect to remove first. `Footer.tsx:L23` duplicates the `contentinfo`
landmark the same way on three of the four routes.
- **Neither Draft.js editor receives an accessible name.** `DocumentCanvas.tsx:L65-L69` and `TextEditor.tsx:L70-L74` render
`Editor` with no `aria-label`, no `aria-labelledby` and no associated `label`, so assistive technology announces an
unlabelled text box.
- **The toolbar is not identified as a toolbar and has no name.** `Toolbar.tsx:L72` sets `className="toolbar"` alone, with no
`role="toolbar"` and no `aria-label`. The three group wrappers at `:L73`, `:L78` and `:L83` carry no `role="group"` and no
name, so the eight buttons present as one flat list.
- **The six style buttons expose no pressed state.** `Toolbar.tsx:L74-L76` and `:L79-L81` declare no `aria-pressed`, so a
screen reader cannot report whether a style is active. The component holds no `editorState`, so no state exists to report.
- **Two controls look active and do nothing, without saying so.** The insert buttons at `Toolbar.tsx:L84` and `:L85` call
`handleInsert`, whose body reaches `console.log` only, and neither carries `disabled` or `aria-disabled`.
- **Both zoom controls carry punctuation-only names and no handler.** `Footer.tsx:L29` labels its button `-` and `:L31`
labels its button `+`, which a screen reader announces as punctuation or skips. Neither declares `onClick`, and neither
carries `disabled`.
- **No focus or disabled treatment is authored anywhere,** because no stylesheet is committed. Browsers would apply their
default focus ring, and nothing here removes or replaces it. No project-authored rendered style exists either, so no contrast
ratio is measurable and none is asserted.

### Styling

Two styling conventions coexist here, and no authored rule backs either one. Tailwind utility classes appear in `Header.tsx`,
across twelve `className` attributes. Bespoke semantic class names with no backing stylesheet appear in `Footer.tsx`,
`Sidebar.tsx`, `Toolbar.tsx` and `DocumentCanvas.tsx`, while `TextEditor.tsx`, `TableEditor.tsx` and `ImageEditor.tsx` set no
`className` at all. No `tailwind.config.js`, no `postcss.config.js` and no Cascading Style Sheets (CSS) file is committed, so
no authored styling would apply under either convention once the build blockers clear. With no component library declared in
`frontend/package.json`, the divergence is a styling inconsistency rather than a compliance gap.

### Markers and outstanding work

Six assistance markers and one outstanding-work comment sit in this directory, and each is the authors' own record of
unfinished work. The markers sit at `Toolbar.tsx:L19`, `TextEditor.tsx:L26`, `DocumentCanvas.tsx:L20`, `TableEditor.tsx:L29`,
`ImageEditor.tsx:L30` and `ImageEditor.tsx:L59`. The last of those sits inside the return statement opened at `:L58`, which
is why a reader scanning the top of that file misses it. The outstanding-work comment is at `Toolbar.tsx:L67`, inside the
`handleInsert` handler both insert buttons call, and `Header.tsx`, `Footer.tsx` and `Sidebar.tsx` carry neither.

See [the troubleshooting register](../../../docs/troubleshooting.md) for the whole repository.

## Usage Examples

The two formatting-helper call sites read most clearly side by side. Both helpers declare two parameters, at
`frontend/src/utils/formatting.ts:L24` and `formatting.ts:L45`.

```tsx
// TextEditor.tsx:L48 and L55 supply both declared arguments.
newState = applyInlineStyle(editorState, command);
newState = applyBlockStyle(editorState, command);

// Toolbar.tsx:L45 and L56 supply one, so the style string lands in the editorState position.
const updatedContent = applyInlineStyle(style);
```

Neither snippet runs today. `draft-js` is absent from `frontend/package.json:L6-L14`, and the `@/` specifiers at
`Toolbar.tsx:L15` and `TextEditor.tsx:L16` match no `frontend/tsconfig.json` alias.

```tsx
// pages/Editor.tsx:L102, against the propless React.FC at DocumentCanvas.tsx:L34.
<DocumentCanvas content={content} onContentChange={handleContentChange} />
```

That line does not run either, because `DocumentCanvas.tsx:L16` imports `useAppSelector` and `useAppDispatch`, which
`frontend/src/store/index.ts` never defines.

Extending this directory needs the absent pieces first. Two store hooks come first, `useAppSelector` and `useAppDispatch` in
`store/index.ts`. The `updateDocument` action and the `selectCurrentDocument` and `selectCurrentUser` selectors follow, in
the two slices.

The five absent modules come last: the three panels `Sidebar.tsx:L10-L12` imports, and the two utilities
`TableEditor.tsx:L12` and `ImageEditor.tsx:L12` import. Each entry records what the committed code needs, and this
documentation changes none of it. See [the onboarding guide](../../../docs/onboarding.md) for prerequisites and setup.
