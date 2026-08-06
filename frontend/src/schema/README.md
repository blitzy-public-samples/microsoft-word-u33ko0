# frontend/src/schema

`document.ts` exports no inferred type, and three modules fail on the omission. The module declares `DocumentSchema` at
`document.ts:L3-L11` and `DocumentVersionSchema` at `document.ts:L13-L19`, and nothing else. Both siblings export theirs:
`user.ts:L13` declares `export type User`, and `template.ts:L12` declares `export type Template`. The three importers that
ask `document.ts` for a type sit at `store/documentSlice.ts:L2`, `services/api.ts:L3` and `services/collaboration.ts:L3`.

Those three sites name five absent type references. `Document` is missing at all three, while `DocumentCreate` and
`DocumentUpdate` are missing at `services/api.ts:L3` alone. All three imports use relative paths, so the module itself
resolves and each import fails on the missing member rather than on the path. Every `Lnn` locator below numbers the frozen
revision `06be74c`, which precedes the documentation pass that added comment blocks to the three modules; current `HEAD`
numbers each file higher.

## Purpose

The directory holds the client-side validation contracts for the three records the browser application exchanges with the
server: a document, a user and a template. Each module declares Zod object schemas, and two of the three also export a
TypeScript type inferred from their schema. No module here reaches the network, reads configuration or holds state.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `DocumentSchema` | Zod object schema | `document.ts:L3-L11` | Seven required fields: `id` L4, `title` L5, `content` L6, `owner_id` L7, `created_at` L8, `updated_at` L9, `collaborators` L10 holding `z.array(z.string())`. |
| `DocumentVersionSchema` | Zod object schema | `document.ts:L13-L19` | Five required fields: `id` L14, `document_id` L15, `content` L16, `created_at` L17, `user_id` L18. |
| `UserSchema` | Zod object schema | `user.ts:L3-L11` | Seven fields: `id` L4, `email` L5 with `.email()`, `username` L6, `full_name` L7 optional, `created_at` L8, `is_active` L9, `is_superuser` L10. |
| `User` | Inferred TypeScript type | `user.ts:L13` | `z.infer<typeof UserSchema>`. Imported by `store/userSlice.ts:L2` and `services/auth.ts:L3`, and both imports resolve. |
| `TemplateSchema` | Zod object schema | `template.ts:L3-L10` | Six required fields: `id` L4, `name` L5, `content` L6, `owner_id` L7, `created_at` L8, `updated_at` L9. |
| `Template` | Inferred TypeScript type | `template.ts:L12` | `z.infer<typeof TemplateSchema>`. No module imports the name. |

`document.ts` and `template.ts` declare no `.optional()` and no `.nullable()` call, so every field in both files is required
and rejects null. `full_name` at `user.ts:L7` is the only optional field here, and `email` at `user.ts:L5` carries the only format check.

## Architecture Fit

The directory forms the client half of the contract boundary between the React application and the FastAPI service. The store
slices, the service clients and the utility modules import these schemas and apply them at their own edges. The directory sits
below every frontend consumer and beside `backend/app/schema/` across the boundary.

The in-repository specification serves as a point of comparison rather than a source of truth for this code. Its
`## DATABASE DESIGN` heading at `documentation/Technical Specifications.md:L315` describes a Firestore Documents collection
holding `document_id`, `title`, `owner_id`, `created_at`, `last_modified` and `content` at L331-L336. `DocumentSchema`
matches that list on `title`, `content`, `owner_id` and `created_at`, names the primary key `id` at `document.ts:L4`, names
the modification timestamp `updated_at` at `document.ts:L9`, and adds `collaborators` at `document.ts:L10`. The same file's
`## API DESIGN` heading at `:L402` describes the endpoints these shapes travel over. See the
[architecture overview](../../../docs/architecture-overview.md) for the wider map and the
[Pydantic contracts](../../../backend/app/schema/README.md) for the server half of this boundary.

## Dependencies

### Internal

The three modules import no internal module. Every relationship below points inward, from a consumer to a schema.

| Consumer | Imported name | Location | Status |
| --- | --- | --- | --- |
| `store/documentSlice.ts` | `Document` | `documentSlice.ts:L2` | Fails. `document.ts` declares no type export. |
| `services/api.ts` | `Document`, `DocumentCreate`, `DocumentUpdate` | `api.ts:L3` | Fails on all three names. |
| `services/collaboration.ts` | `Document` | `collaboration.ts:L3` | Fails on the same missing name. |
| `utils/documentUtils.ts` | `DocumentSchema` | `documentUtils.ts:L2` | Resolves. The schema value exists at `document.ts:L3`. |
| `store/userSlice.ts` | `User` | `userSlice.ts:L2` | Resolves against `user.ts:L13`. |
| `services/auth.ts` | `User` | `auth.ts:L3` | Resolves against `user.ts:L13`. |
| No consumer | `TemplateSchema`, `Template` | `template.ts:L3-L10`, `:L12` | Unused. `pages/Templates.tsx:L1-L6` imports nothing from here. |

### External

| Package | Imported at | Declared in `frontend/package.json` | Status |
| --- | --- | --- | --- |
| `zod` | `document.ts:L1`, `user.ts:L1`, `template.ts:L1` | No | Imported but undeclared |

`frontend/package.json:L6-L14` declares seven runtime dependencies: `@reduxjs/toolkit ^1.9.5` at L7, `react ^18.2.0` at L8,
`react-dom ^18.2.0` at L9, `react-redux ^8.0.5` at L10, `react-router-dom ^6.11.1` at L11, `tailwindcss ^3.3.2` at L12 and
`typescript ^4.9.5` at L13. `zod` is absent, so all three modules resolve their only import to nothing. Three of the
frontend's thirteen undeclared-package resolution errors originate here, and a fourth `zod` import sits at
`utils/validation.ts:L1`. The specification does not name `zod` either: its `## FRAMEWORKS AND LIBRARIES` heading declares
Axios at `documentation/Technical Specifications.md:L544` and Draft.js at `:L545`.

The [frontend source README](../README.md) owns the consolidated register: the full undeclared-package list, the `@/` alias
analysis and the complete type-check profile. The [data model reference](../../../docs/data-model.md) consolidates the drift.

## Configuration

These three modules read no configuration. No `process.env` reference, no imported constant and no schema default appears in
any of the three files, and the frontend's one environment variable read sits elsewhere, at `services/api.ts:L5`.

| Surface | Value | Location |
| --- | --- | --- |
| Environment variables | None | No `process.env` reference in the directory |
| Imported constants | None | The only import in each file is `zod` at L1 |
| Schema defaults | None. No `.default()` call appears. | `document.ts`, `user.ts`, `template.ts` |

## Data Flows

A schema moves one way: a module here declares it, a consumer imports it, and the consumer applies it at its own boundary.
Two paths leave the directory and only the value path works. `utils/documentUtils.ts:L2` imports `DocumentSchema` and
resolves, while the type path is severed at `document.ts`, so the three type importers in the table above receive nothing.

The value path then reaches a broken call. `utils/documentUtils.ts:L13` and `:L30` both call `DocumentSchema.isValid`, and
Zod exposes `parse` and `safeParse` rather than `isValid`. The two sites also disagree on their argument: L13 passes the
JavaScript Object Notation (JSON) string built at L10, while L30 passes the object parsed at L24. The
[utilities README](../utils/README.md) carries the fuller treatment.

## Design Patterns

Schema at the boundary. Each record shape is declared once, in one module, at the edge of the application, and consumers
import the declaration instead of restating it. `pages/Templates.tsx:L8-L13` departs from the pattern with its own `interface Template`.

Runtime validation. A Zod schema is a value, so it checks a shape while the program runs rather than only while the compiler
runs. `utils/validation.ts` applies the same library to field-level checks outside this directory.

Type inference from a runtime schema. `user.ts:L13` and `template.ts:L12` derive a static TypeScript type from their schema
through `z.infer`, so the runtime contract and the static type cannot drift apart inside those two modules. `document.ts`
applies the pattern to neither of its schemas.

## Known Limitations

No artifact keeps the two sides of the contract in agreement. The repository commits no OpenAPI document, generates no
client and ships no shared schema package spanning TypeScript and Python. The Zod definitions here and the Pydantic
definitions in `backend/app/schema/` are maintained by hand, which is how every divergence below arose. The specification
declares no cross-language contract tool either: its `### Shared` heading lists ESLint, Prettier and Git at
`documentation/Technical Specifications.md:L557-L561`.

| Concept | This directory | `backend/app/schema/` | `documentation/Technical Specifications.md` |
| --- | --- | --- | --- |
| document owner | `owner_id` required, `document.ts:L7` | `owner_id: Optional[str] = None`, `document.py:L8` | `owner_id`, L333 and L375 |
| version actor | `user_id`, `document.ts:L18` | `user_id`, `document.py:L27` | Versions subcollection L338-L341 declares no author field |
| modification timestamp | `updated_at`, `document.ts:L9` | `updated_at`, `document.py:L20` | `last_modified`, L335 |
| collaborators | inline `z.array(z.string())`, `document.ts:L10` | absent from all five models | a child of Documents in the diagram, L325 |
| document create payload | absent | `DocumentCreate`, `document.py:L10-L11` | not specified as a payload |
| document update payload | absent | `DocumentUpdate`, `document.py:L13-L15` | not specified as a payload |
| user modification time | absent | `updated_at`, `user.py:L22` | not applicable |
| user credential | absent | `UserCreate.password`, `user.py:L11` | not applicable |
| optional full name | `full_name` optional, `user.ts:L7` | `full_name` optional, `user.py:L8` | `display_name`, L353 |
| template contract | `TemplateSchema`, `template.ts:L3-L10` | no `template.py` exists at all | not specified |
| timestamp representation | `z.date()`, rejects a string | `datetime`, serialized as a string | timestamps |

One row agrees across both code contracts: `full_name` is optional at `user.ts:L7` and at `user.py:L8`. The two still disagree on null, because `Optional[str] = None` emits null and `.optional()` rejects null without `.nullable()` beside it.

- **Ownership carries four positions, and this README names none of them canonical.** `document.ts:L7` declares `owner_id` on
  the document, and `document.ts:L18` declares `user_id` on the version. Across the boundary, `backend/app/schema/document.py:L8`
  declares `owner_id` as optional with a default of `None`, while `backend/app/services/document_service.py:L19` writes and later
  compares `user_id`. Because the server contract makes `owner_id` optional, a document validates with no owner recorded while
  ownership decides access, and the [data model reference](../../../docs/data-model.md) consolidates all four positions.
- **The modification timestamp carries three names.** `updated_at` at `document.ts:L9` and `document.py:L20`, and
  `last_modified` at `documentation/Technical Specifications.md:L335` and `:L377`.
- **`collaborators` exists only on the client.** `document.ts:L10` declares it, and no model in
  `backend/app/schema/document.py` declares the field. The specification's `## DATABASE DESIGN` diagram places Collaborators
  as a child of Documents at `documentation/Technical Specifications.md:L325`.
- **Two server fields have no client counterpart.** `user.py:L22` declares `updated_at` on `User`, and `user.py:L11`
  declares `password` on `UserCreate`. `UserSchema` at `user.ts:L3-L11` models neither.
- **No user contract declares `name` or `avatar`, and four sites read one of them.** `components/Header.tsx:L28` reads
  `currentUser.avatar` and `currentUser.name`, `Header.tsx:L29` reads `currentUser.name`, `pages/Home.tsx:L16` reads
  `currentUser.name`, and `pages/Settings.tsx:L15` reads `currentUser?.name`. The specification names the field
  `display_name` at `documentation/Technical Specifications.md:L353`, a third name, and the [components](../components/README.md) and [pages](../pages/README.md) READMEs cite their own sites.
- **Two incompatible `Template` shapes exist, and the server half is absent.** `TemplateSchema` at `template.ts:L3-L10` and
  the local `interface Template` at `pages/Templates.tsx:L8-L13` share `id` and `name`. The page adds `description` at L11
  and `thumbnail` at L12, and the schema adds `content`, `owner_id`, `created_at` and `updated_at`. No
  `backend/app/schema/template.py` exists, while `backend/app/api/templates.py:L3` imports `Template`, `TemplateCreate` and `TemplateUpdate` from `app.schema.template` and `:L4` imports the absent template service.
- **Six `z.date()` declarations reject the value the wire carries.** `document.ts:L8`, `:L9`, `:L17`, `user.ts:L8`,
  `template.ts:L8` and `:L9` each accept only a `Date` instance, while the server declares `datetime` and JSON carries a datetime as a string.
- **`zod` is imported and undeclared.** `document.ts:L1`, `user.ts:L1` and `template.ts:L1` import the package, and
  `frontend/package.json:L6-L14` omits it. No code in this directory runs until the package is installed.
- **The directory carries no assistance marker and no unfinished-work comment of its own.** The nearest ones sit in the
  consumers, at `utils/documentUtils.ts:L4-L6`, `:L12`, `:L29` and `store/documentSlice.ts:L54`.

The [troubleshooting register](../../../docs/troubleshooting.md) carries every defect above with file and line evidence.

## Usage Examples

No example below runs today, because `frontend/package.json:L6-L14` omits `zod` and the import at `document.ts:L1`,
`user.ts:L1` and `template.ts:L1` resolves to nothing. The [onboarding guide](../../../docs/onboarding.md) has the prerequisites.

Validating a user record uses the safe form, which returns a result object instead of throwing:

```typescript
import { UserSchema, User } from '../schema/user';

const result = UserSchema.safeParse(payload);
const user: User | null = result.success ? result.data : null;
if (!result.success) console.error(result.error.issues);
```

The example matches the declared contract at `user.ts:L3-L11` and `user.ts:L13`. Passing a server response straight
through fails on two fields: `created_at` at `user.ts:L8` declares `z.date()` and receives a string, and `full_name` at
`user.ts:L7` rejects the null that a server declaring `Optional[str] = None` at `user.py:L8` sends.

Importing a document type is not currently possible:

```typescript
import { Document } from '../schema/document';
```

The import fails, because `document.ts` declares two schema values at L3-L11 and L13-L19 and exports no type. The three committed
importers at `store/documentSlice.ts:L2`, `services/api.ts:L3` and `services/collaboration.ts:L3` write this import and fail the
same way. Importing the schema value does work, as `utils/documentUtils.ts:L2` shows.

Three changes would unblock the directory, recorded here rather than performed. First, export an inferred `Document` type from
`document.ts`, which resolves the `Document` reference at all three import sites. Second, export the two write shapes
`DocumentCreate` and `DocumentUpdate` that `services/api.ts:L3` asks for. Third, declare `zod` in `frontend/package.json`.
