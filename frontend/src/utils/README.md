# `frontend/src/utils`

## Purpose

Three modules hold pure helper functions that the component layer calls. `formatting.ts` applies Draft.js inline and block styles, `validation.ts`
checks credentials against Zod schemas, and `documentUtils.ts` converts Draft.js content to and from a JavaScript Object Notation (JSON) string. All
six exported functions are synchronous, take their inputs as arguments, and return a value. None writes to the Redux store, the network, or the
browser, and no module here holds state.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `applyInlineStyle` | Exported function | `formatting.ts:L31` | Applies an inline style to the current selection. Declares two parameters, reads content and selection at `:L32-L33`, calls `Modifier.applyInlineStyle` at `:L35-L39`, and returns a new `EditorState` from `EditorState.push` with change type `'apply-inline-style'` at `:L41`. |
| `applyBlockStyle` | Exported function | `formatting.ts:L61` | Sets the block type of the current selection. Declares two parameters, reads content and selection at `:L62-L63`, calls `Modifier.setBlockType` at `:L65-L69`, and returns a new `EditorState` from `EditorState.push` with change type `'change-block-type'` at `:L71`. |
| `validateEmail` | Exported arrow function | `validation.ts:L24` | Checks one string against `z.string().email()` at `:L25` and returns the `safeParse` `.success` flag at `:L26`. |
| `validatePassword` | Exported arrow function | `validation.ts:L44` | Checks one string against the policy built at `:L45-L49` and returns the `.success` flag at `:L50`. |
| `serializeDocument` | Exported function | `documentUtils.ts:L39` | Declares an `EditorState` parameter, converts its content with `convertToRaw` at `:L40`, and returns the `JSON.stringify` value built at `:L41`. |
| `deserializeDocument` | Exported function | `documentUtils.ts:L63` | Parses JSON text at `:L67`, rebuilds a `ContentState` with `convertFromRaw` at `:L77`, and returns an `EditorState` from `:L78`. |

## Architecture Fit

The directory sits below the component layer and depends on nothing inside the application except one schema. `frontend/src/components/Toolbar.tsx`,
`TextEditor.tsx` and `DocumentCanvas.tsx` are the only modules that import from here, all three for the Draft.js editing surface. `validation.ts`
has no caller anywhere under `frontend/src`.

The specification's `Frontend Components` diagram, under its `COMPONENT DIAGRAMS` heading at `documentation/Technical Specifications.md:L183-L199`,
names fifteen components and no utility module. Three components it does name, `Toolbar`, `DocumentCanvas` and `TextEditor`, import from this
directory in the committed code. The specification keeps formatting and serialization inside those components, and the committed code factors the
same steps into these six functions. For the wider layer map, see
[`../../../docs/architecture-overview.md`](../../../docs/architecture-overview.md).

## Dependencies

### Internal

| Module | Imported symbol | Location | Status |
| --- | --- | --- | --- |
| `../schema/document` | `DocumentSchema` | `documentUtils.ts:L22` | Resolves. The specifier is relative, so the `@/` prefix that breaks imports across the rest of the frontend does not apply. See [`../../../docs/data-model.md`](../../../docs/data-model.md) for the contract and [`../schema/README.md`](../schema/README.md) for the module. |

`formatting.ts` and `validation.ts` import nothing internal, and no import here names a module that does not exist. The failures in this directory
are packaging and contract failures rather than missing-module failures.

### External

| Package | Declared version | Imported at | Status |
| --- | --- | --- | --- |
| `draft-js` | None declared | `formatting.ts:L13`, `documentUtils.ts:L21` | Imported but undeclared. The seven runtime dependencies at `frontend/package.json:L6-L14` are `@reduxjs/toolkit`, `react`, `react-dom`, `react-redux`, `react-router-dom`, `tailwindcss` and `typescript`. `@types/draft-js` is absent from the development dependencies at `:L15-L30`. |
| `zod` | None declared | `validation.ts:L13` | Imported but undeclared. Absent from both dependency blocks at `frontend/package.json:L6-L30`. |

The specification does declare Draft.js, at `documentation/Technical Specifications.md:L545` under its `FRAMEWORKS AND LIBRARIES` heading, while a
case-insensitive search for `zod` across `documentation/` returns nothing. Three of the frontend's module-resolution failures trace to this
directory: the two `draft-js` imports and the one `zod` import. [`../README.md`](../README.md) carries the consolidated package register and the
repository-wide type-check figures.

## Configuration

No module here reads an environment variable or a settings object. The one set of tunable values is the password policy, hard-coded inside
`validatePassword`.

| Constraint | Value | Location |
| --- | --- | --- |
| Minimum length | 8 characters | `validation.ts:L46` |
| Required character classes | One lowercase letter, one uppercase letter and one digit, through the `(?=.*[a-z])`, `(?=.*[A-Z])` and `(?=.*\d)` lookaheads | `validation.ts:L47` |
| Required special character | At least one of `@$!%*?&`, through the `(?=.*[@$!%*?&])` lookahead | `validation.ts:L47` |
| Permitted character set | `[A-Za-z\d@$!%*?&]{8,}`, anchored across the whole value | `validation.ts:L47` |

The last row constrains every character rather than only the first eight, so `Passw0rd@#` satisfies all four lookaheads and still fails on the `#`.
`validateEmail` takes no configuration and applies Zod's built-in rule at `validation.ts:L25`.

## Data Flows

Two flows run through this directory, and each carries an `EditorState`, which is Draft.js's immutable snapshot of editor content plus selection.

**Formatting flow.** A caller passes an `EditorState` and a style name to `applyInlineStyle` at `formatting.ts:L31` or to `applyBlockStyle` at
`:L61`. Each function reads the content and the selection, hands both to a `Modifier` call, and returns a new snapshot from `EditorState.push`. The
input snapshot is never changed.

**Serialization flow.** `serializeDocument` at `documentUtils.ts:L39` turns editor content into JSON text through `convertToRaw` and
`JSON.stringify`. `deserializeDocument` at `:L20` runs the reverse through `JSON.parse` at `:L24`, `convertFromRaw` at `:L34`, and
`EditorState.createWithContent` at `:L35`.

> **Data-flow note.** Neither flow completes as committed, and the two break in different places. The formatting flow breaks
> outside this directory, at the one-argument calls in `frontend/src/components/Toolbar.tsx:L62` and `:L67`. The
> serialization flow breaks inside this directory. `DocumentSchema.isValid` at `documentUtils.ts:L44` and `:L73` names no
> Zod member, so each call raises a `TypeError` before the return at `:L48` and before `convertFromRaw` at `:L77`.

## Design Patterns

**Pure transformation.** All four Draft.js helpers take state as an argument and return a new value: `formatting.ts:L31` and `:L61`,
`documentUtils.ts:L39` and `:L63`. The two formatting helpers return the result of `EditorState.push`, which is a fresh snapshot rather than the one
passed in.

**Named change types.** Both formatting helpers label their edit for the Draft.js undo stack, passing `'apply-inline-style'` at `formatting.ts:L41`
and `'change-block-type'` at `:L71`.

**Validate at the boundary, reporting a boolean.** Both credential checks build a schema, run it against untrusted input, and report the outcome as
a boolean at `validation.ts:L26` and `:L50`. `documentUtils.ts` guards its two returns at `:L44` and `:L73` against `DocumentSchema`, though
`isValid` names no Zod member so neither guard compares anything.

## Known Limitations

`validation.ts` is the one module here whose own logic holds up: both functions match their declared signatures, and both call real Zod methods. The
module still does not compile as committed, because `validation.ts:L13` imports `zod` while `frontend/package.json:L6-L14` declares seven runtime
dependencies and omits it, so a type check reports `TS2307` against that line. Read the module as logic-correct once the dependency is installed
rather than as defect-free today. The other two modules carry faults in their own logic, and their callers add more.
[`../components/README.md`](../components/README.md) covers the component side of every shared fault.

- **`SelectionState` is imported and never used.** `formatting.ts:L13` names `SelectionState` in its `draft-js` import, and nothing in the file
  references the symbol.
- **The two-argument contract has one compliant caller and one violating caller.** `applyInlineStyle` at `formatting.ts:L31` and `applyBlockStyle`
  at `:L61` each declare two parameters. `frontend/src/components/TextEditor.tsx:L109` and `:L116` pass both. `Toolbar.tsx:L62` and `:L67` pass one,
  so the style name binds to `editorState` and the second parameter stays `undefined`.
- **The violating caller's style names do not match Draft.js.** `Toolbar.tsx:L79-L81` and `:L84-L86` pass lowercase names such as `'bold'` and
  `'heading1'` that Draft.js does not define. `TextEditor.tsx:L111-L115` passes accepted block types such as `header-one`.
- **Both credential checks discard their own messages.** `validation.ts:L26` and `:L50` return `.success` only, so the strings configured at `:L46`
  and `:L48` never reach a caller.
- **No module calls either credential check.** A search across `frontend/src` finds `validateEmail` and `validatePassword` only at their
  declarations, `validation.ts:L24` and `:L44`. No registration or sign-in interface exists to call them.
- **`DocumentSchema.isValid` carries three faults, at `documentUtils.ts:L44` and `:L73`.** First, `isValid` is not a member of a Zod object schema.
  `DocumentSchema` is built with `z.object` at `frontend/src/schema/document.ts:L65-L73`, and a Zod object exposes `parse` and `safeParse`. Reading
  `.isValid` therefore yields `undefined`, and calling it raises a `TypeError` before the guarded `Error` at `documentUtils.ts:L45` or `:L74` can
  throw. Second, the schema models the wrong shape, declaring the metadata fields `id`, `title`, `content`, `owner_id`, `created_at`, `updated_at`
  and `collaborators`, while `convertToRaw` produces Draft.js raw content shaped `{ blocks, entityMap }`. Third, `documentUtils.ts:L44` passes the
  JSON string while `documentUtils.ts:L73` passes the parsed object, so the two sites check different kinds of value.
- **The one caller inverts both signatures, and the two errors are exact inverses.** `serializeDocument` at `documentUtils.ts:L39` declares an
  `EditorState` parameter, and `deserializeDocument` at `:L63` declares an `EditorState` return. `frontend/src/components/DocumentCanvas.tsx:L116`
  binds the returned `EditorState` to a variable named `contentState`, then `:L117` hands it to `EditorState.createWithContent()`, which accepts a
  `ContentState`. `:L163` passes a `ContentState` from `getCurrentContent()` into `serializeDocument`. Correcting either site alone, in the direction
  its own variable name suggests, breaks the other.
- **Both external packages are imported and undeclared.** `draft-js` at `formatting.ts:L13` and `documentUtils.ts:L21`, and `zod` at
  `validation.ts:L13`, appear in neither dependency block of `frontend/package.json:L6-L30`. No function here runs until both are declared and
  installed.
- **The authors recorded outstanding work at three points in `documentUtils.ts`.** The assistance marker at `:L24-L26` asks for error handling,
  edge-case management, and correct `DocumentSchema` validation. The two deferred-work comments at `:L43` and `:L72` sit directly above the two
  `isValid` calls and repeat that request.

Four repairs would unblock the directory, and this documentation pass performs none of them. `frontend/package.json` needs `draft-js`,
`@types/draft-js` and `zod`. The two `isValid` calls need the correct `DocumentSchema` validation that the marker at `documentUtils.ts:L24-L26` asks
for. `Toolbar.tsx:L62` and `:L67` need a second argument. `DocumentCanvas.tsx:L116-L117` and `:L163` need a matched correction.

For the repository-wide register see [`../../../docs/troubleshooting.md`](../../../docs/troubleshooting.md), and for prerequisites and setup order
see [`../../../docs/onboarding.md`](../../../docs/onboarding.md).

## Usage Examples

**Formatting helpers.** Both calls pass the editor state first and the style name second, which is the arity and the order declared at
`formatting.ts:L31` and `:L61`.

```typescript
import { EditorState } from 'draft-js';
import { applyInlineStyle, applyBlockStyle } from './formatting';

const editorState = EditorState.createEmpty();

// Bold the current selection. Draft.js spells inline styles in upper case.
const bolded = applyInlineStyle(editorState, 'BOLD');

// Promote the current block to a first-level heading.
const headed = applyBlockStyle(editorState, 'header-one');
```

`frontend/src/components/TextEditor.tsx:L109` and `:L116` supply both arguments in this order, though they forward the
lowercase key command rather than an upper-case inline style. Cannot run: the undeclared `draft-js` import at `formatting.ts:L13` stops the module from resolving.

**Credential checks.** Each function takes one string and returns one boolean, per `validation.ts:L24` and `:L44`.

```typescript
import { validateEmail, validatePassword } from './validation';

validateEmail('editor@example.com');   // true
validateEmail('editor@example');       // false, no top-level domain

// Disposable test-only literals. Not credentials.
validatePassword('nOtARealPass@9');    // true, meets every constraint above
validatePassword('nOtARealPass@#9');   // false, '#' sits outside the permitted set
validatePassword('nOt@9');             // false, shorter than eight characters
```

Cannot run: the undeclared `zod` import at `validation.ts:L13` stops the module from resolving. Neither call reports why a value failed, because
both functions return `.success` alone.

**Serialization round trip.** `serializeDocument` at `documentUtils.ts:L39` accepts an `EditorState`, and `deserializeDocument` at `:L63` returns
one.

```typescript
import { EditorState } from 'draft-js';
import { serializeDocument, deserializeDocument } from './documentUtils';

const editorState = EditorState.createEmpty();
const json = serializeDocument(editorState);   // pass the state, not its ContentState
const restored = deserializeDocument(json);    // bind the return as an EditorState
```

Cannot run: `DocumentSchema.isValid` at `documentUtils.ts:L44` and `:L73` names no Zod member, so each function raises a `TypeError` before
returning.
