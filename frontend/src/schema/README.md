# frontend/src/schema

`document.ts` exports no inferred type, and three modules fail on the omission. The module declares `DocumentSchema` at
`document.ts:L65-L73` and `DocumentVersionSchema` at `document.ts:L86-L92`, and nothing else. Both siblings export theirs:
`user.ts:L56` declares `export type User`, and `template.ts:L40` declares `export type Template`. The three importers that
ask `document.ts` for a type sit at `store/documentSlice.ts:L22`, `services/api.ts:L80` and `services/collaboration.ts:L15`.

Those three sites name five absent type references. `Document` is missing at all three, while `DocumentCreate` and
`DocumentUpdate` are missing at `services/api.ts:L80` alone. All three imports use relative paths, so the module itself
resolves and each import fails on the missing member rather than on the path.

## Purpose

The directory declares the client-side contracts for the three records the browser application exchanges with the server: a
document, a user and a template. Each module declares Zod object schemas, and two of the three also export a TypeScript type
inferred from their schema. Consumers take the inferred types and leave the schema values almost entirely unused, so nothing
in the running application validates against them. No module reaches the network, reads configuration or holds state.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `DocumentSchema` | Zod object schema | `document.ts:L65-L73` | Seven required fields: `id` L66, `title` L67, `content` L68, `owner_id` L69, `created_at` L70, `updated_at` L71, `collaborators` L72 holding `z.array(z.string())`. |
| `DocumentVersionSchema` | Zod object schema | `document.ts:L86-L92` | Five required fields: `id` L87, `document_id` L88, `content` L89, `created_at` L90, `user_id` L91. No module imports the value. |
| `UserSchema` | Zod object schema | `user.ts:L37-L45` | Seven fields: `id` L38, `email` L39 with `.email()`, `username` L40, `full_name` L41 optional, `created_at` L42, `is_active` L43, `is_superuser` L44. No module imports the value; only `user.ts:L56` reads it, through `z.infer`. |
| `User` | Inferred TypeScript type | `user.ts:L56` | `z.infer<typeof UserSchema>`. Imported by `store/userSlice.ts:L22` and `services/auth.ts:L70`, and both imports resolve. Both consume the type alone. |
| `TemplateSchema` | Zod object schema | `template.ts:L30-L37` | Six required fields: `id` L31, `name` L32, `content` L33, `owner_id` L34, `created_at` L35, `updated_at` L36. No module imports the value either. |
| `Template` | Inferred TypeScript type | `template.ts:L40` | `z.infer<typeof TemplateSchema>`. No module imports the name. |

`document.ts` and `template.ts` declare no `.optional()` and no `.nullable()` call, so every field in both files is required
and rejects null. `full_name` at `user.ts:L41` is the only optional field here, and `email` at `user.ts:L39` carries the only format check.

## Architecture Fit

The directory forms the client half of the contract boundary between the React application and the FastAPI service. Its
consumers split two ways. The store slices and the service clients import inferred types, which the compiler erases, so no
schema reaches the running program. One module imports a schema value, `utils/documentUtils.ts:L22`, whose two calls name a
method Zod does not define. The directory sits below every frontend consumer, beside `backend/app/schema/` across the
boundary, and enforces nothing at either edge as committed.

The in-repository specification serves as a point of comparison rather than a source of truth for this code. Its
`## DATABASE DESIGN` heading at `documentation/Technical Specifications.md:L315` describes a Firestore Documents collection
holding `document_id`, `title`, `owner_id`, `created_at`, `last_modified` and `content` at L331-L336. `DocumentSchema`
matches that list on `title`, `content`, `owner_id` and `created_at`, names the primary key `id` at `document.ts:L66`, names
the modification timestamp `updated_at` at `document.ts:L71`, and adds `collaborators` at `document.ts:L72`. The
`## API DESIGN` heading at `documentation/Technical Specifications.md:L402` describes the endpoints these shapes travel over.
See the [architecture overview](../../../docs/architecture-overview.md) for the wider map and the
[Pydantic contracts](../../../backend/app/schema/README.md) for the server half of this boundary.

## Dependencies

### Internal

The three modules import no internal module. Every relationship below points inward, from a consumer to a schema.

| Consumer | Imported name | Location | Status |
| --- | --- | --- | --- |
| `store/documentSlice.ts` | `Document` | `documentSlice.ts:L22` | Fails. `document.ts` declares no type export. |
| `services/api.ts` | `Document`, `DocumentCreate`, `DocumentUpdate` | `api.ts:L80` | Fails on all three names. |
| `services/collaboration.ts` | `Document` | `collaboration.ts:L15` | Fails on the same missing name. |
| `utils/documentUtils.ts` | `DocumentSchema` | `documentUtils.ts:L22` | Resolves. The only schema **value** import in the frontend. The value exists at `document.ts:L65`. |
| `store/userSlice.ts` | `User` | `userSlice.ts:L22` | Resolves against `user.ts:L56`. Type only. |
| `services/auth.ts` | `User` | `auth.ts:L70` | Resolves against `user.ts:L56`. Type only. |
| No consumer | `UserSchema`, `DocumentVersionSchema`, `TemplateSchema`, `Template` | `user.ts:L37-L45`, `document.ts:L86-L92`, `template.ts:L30-L37`, `:L40` | Unused. No module imports any of the four. `pages/Templates.tsx:L32-L37` imports nothing from here. |

### External

| Package | Imported at | Declared in `frontend/package.json` | Status |
| --- | --- | --- | --- |
| `zod` | `document.ts:L43`, `user.ts:L15`, `template.ts:L20` | No | Imported but undeclared |

`frontend/package.json:L6-L14` declares seven runtime dependencies and omits `zod`, so all three modules resolve their only
import to nothing. Three of the frontend's thirteen undeclared-package resolution errors originate here, and a fourth `zod`
import sits at `utils/validation.ts:L13`. The specification does not name `zod` either: its `## FRAMEWORKS AND LIBRARIES`
heading declares Axios at `documentation/Technical Specifications.md:L544` and Draft.js at `:L545`.

The [frontend source README](../README.md) owns the consolidated register: the full undeclared-package list, the `@/` alias
analysis and the complete type-check profile. The [data model reference](../../../docs/data-model.md) consolidates the drift.

## Configuration

These three modules read no configuration. No `process.env` reference, no imported constant and no schema default appears in
any of the three files, and the frontend's one environment variable read sits elsewhere, at `services/api.ts:L82`.

| Surface | Value | Location |
| --- | --- | --- |
| Environment variables | None | No `process.env` reference in the directory |
| Imported constants | None | The only import in each file is `zod`, at `document.ts:L43`, `user.ts:L15` and `template.ts:L20` |
| Schema defaults | None. No `.default()` call appears. | `document.ts`, `user.ts`, `template.ts` |

## Data Flows

Two paths leave the directory, and neither delivers a validated value. The type path is severed at `document.ts`, so the three
importers that ask for a document type receive nothing. The two that resolve, `store/userSlice.ts:L22` and
`services/auth.ts:L70`, receive a compile-time type that the emitted JavaScript no longer carries.

The value path resolves and then reaches a broken call. `utils/documentUtils.ts:L22` is the only module anywhere that imports
a schema value, and `:L44` and `:L73` both call `DocumentSchema.isValid`, which Zod does not define. Zod exposes `parse` and
`safeParse` instead. The two sites also disagree on the argument. `L44` passes the JavaScript Object Notation (JSON) string
built at `L41` and `L73` passes the object parsed at `L67`. Neither value is the document record `DocumentSchema` models.
`UserSchema`, `DocumentVersionSchema` and `TemplateSchema` are imported by no module at all, so no third path exists. The
[utilities README](../utils/README.md) carries the fuller treatment.

## Design Patterns

Schema at the boundary, declared but not yet enforced. Each record shape is declared once, in one module, at the edge of the
application, and consumers import the declaration instead of restating it. `pages/Templates.tsx:L61-L66` departs from the
pattern with its own `interface Template`.

Runtime validation, available and unused. A Zod schema is a value, so it can check a shape while the program runs rather than
only while the compiler runs. No consumer here does that: the one attempt, at `utils/documentUtils.ts:L44` and `:L73`, names a
method the library does not expose. `utils/validation.ts:L25` and `:L45` build their own schemas from `zod` directly.

Type inference from a runtime schema. `user.ts:L56` and `template.ts:L40` derive a static TypeScript type from their schema
through `z.infer`, so the runtime contract and the static type cannot drift apart inside those two modules. `document.ts`
applies the pattern to neither of its schemas, which is what severs the type path above.

## Known Limitations

No artifact keeps the two sides of the contract in agreement. The repository commits no OpenAPI document, generates no
client and ships no shared schema package spanning TypeScript and Python. The Zod definitions here and the Pydantic
definitions in `backend/app/schema/` are maintained by hand, so nothing detects a divergence and nothing prevents one. The
table below records the divergences that exist. The repository holds no record of how any of them arose, so manual
synchronization is stated here as the risk that permits drift rather than as its proven cause. The specification declares no
cross-language contract tool either: its `### Shared` heading lists ESLint, Prettier and Git at
`documentation/Technical Specifications.md:L557-L561`.

| Concept | This directory | `backend/app/schema/` | `documentation/Technical Specifications.md` |
| --- | --- | --- | --- |
| document owner | `owner_id` required, `document.ts:L69` | `owner_id: Optional[str] = None`, `document.py:L66` | `owner_id`, L333 and L375 |
| version actor | `user_id`, `document.ts:L91` | `user_id`, `document.py:L135` | Versions subcollection L338-L341 declares no author field |
| modification timestamp | `updated_at`, `document.ts:L71` | `updated_at`, `document.py:L112` | `last_modified`, L335 |
| collaborators | inline `z.array(z.string())`, `document.ts:L72` | absent from all five models | a child of Documents in the diagram, L325 |
| document write payloads | absent | `DocumentCreate`, `document.py:L68-L80`; `DocumentUpdate`, `document.py:L82-L94` | not specified as payloads |
| server-only user fields | absent | `updated_at`, `user.py:L171`; `UserCreate.password`, `user.py:L94` | not applicable |
| optional full name | `full_name` optional, `user.ts:L41` | `full_name` optional, `user.py:L82` | `display_name`, L353 |
| template contract | `TemplateSchema`, `template.ts:L30-L37` | no `template.py` exists at all | not specified |
| timestamp representation | `z.date()`, rejects a string | `datetime`, serialized as a string | timestamps |

One row agrees across both code contracts: `full_name` is optional at `user.ts:L41` and at `user.py:L82`. The two still disagree on null, because `Optional[str] = None` emits null and `.optional()` rejects null without `.nullable()` beside it.

- **Ownership carries four positions, and this README names none of them canonical.** `document.ts:L69` declares `owner_id` on
  the document, and `document.ts:L91` declares `user_id` on the version. Across the boundary, `backend/app/schema/document.py:L66`
  declares `owner_id` as optional with a default of `None`, while `backend/app/services/document_service.py:L116` writes and later
  compares `user_id`. Because the server contract makes `owner_id` optional, a document validates with no owner recorded while
  ownership decides access, and the [data model reference](../../../docs/data-model.md) consolidates all four positions.
- **The modification timestamp carries three names.** `updated_at` at `document.ts:L71` and `document.py:L112`, and
  `last_modified` at `documentation/Technical Specifications.md:L335` and `:L377`.
- **`collaborators` exists only on the client.** `document.ts:L72` declares it, and no model in
  `backend/app/schema/document.py` declares the field. The specification's `## DATABASE DESIGN` diagram places Collaborators
  as a child of Documents at `documentation/Technical Specifications.md:L325`.
- **Two server fields have no client counterpart.** `user.py:L171` declares `updated_at` on `User`, and `user.py:L94`
  declares `password` on `UserCreate`. `UserSchema` at `user.ts:L37-L45` models neither.
- **No user contract declares `name` or `avatar`, and four sites read one of them.** `components/Header.tsx:L77` reads
  `currentUser.avatar` and `currentUser.name`, `Header.tsx:L78` reads `currentUser.name`, `pages/Home.tsx:L59` reads
  `currentUser.name`, and `pages/Settings.tsx:L82` reads `currentUser?.name`. The specification names the field
  `display_name` at `documentation/Technical Specifications.md:L353`, a third name, and the [components](../components/README.md) and [pages](../pages/README.md) READMEs cite their own sites.
- **Two incompatible `Template` shapes exist, and the server half is absent.** `TemplateSchema` at `template.ts:L30-L37` and
  the local `interface Template` at `pages/Templates.tsx:L61-L66` share `id` and `name`. The page adds `description` at L64
  and `thumbnail` at L65, and the schema adds `content`, `owner_id`, `created_at` and `updated_at`. No
  `backend/app/schema/template.py` exists, while `backend/app/api/templates.py:L70` imports `Template`, `TemplateCreate` and `TemplateUpdate` from `app.schema.template` and `:L71` imports the absent template service.
- **Six `z.date()` declarations reject the value the wire carries.** `document.ts:L70`, `:L71`, `:L90`, `user.ts:L42`,
  `template.ts:L35` and `:L36` each accept only a `Date` instance, while the server declares `datetime` and JSON carries a datetime as a string.
- **`zod` is imported and undeclared.** `document.ts:L43`, `user.ts:L15` and `template.ts:L20` import the package, and
  `frontend/package.json:L6-L14` omits it. No code in this directory runs until the package is installed.
- **The directory carries no assistance marker and no unfinished-work comment of its own.** The nearest ones sit in the
  consumers, at `utils/documentUtils.ts:L24-L26`, `:L43`, `:L72` and `store/documentSlice.ts:L171`.

The [troubleshooting register](../../../docs/troubleshooting.md) carries every defect above with file and line evidence.

## Usage Examples

No example below runs today, because `frontend/package.json:L6-L14` omits `zod` and the import at `document.ts:L43`,
`user.ts:L15` and `template.ts:L20` resolves to nothing. The [onboarding guide](../../../docs/onboarding.md) has the prerequisites.

Validating a user record uses the safe form, which returns a result object instead of throwing:

```typescript
import { UserSchema, User } from '../schema/user';

const payload: unknown = { id: 'u-1', email: 'ana@example.com', username: 'ana', created_at: new Date(), is_active: true, is_superuser: false };
const result = UserSchema.safeParse(payload);
const user: User | null = result.success ? result.data : null;
if (!result.success) console.error(result.error.issues);
```

The example matches the declared contract at `user.ts:L37-L45` and `user.ts:L56`. Passing a server response straight through
fails on two fields. `created_at` at `user.ts:L42` declares `z.date()` and receives a string, and `full_name` at
`user.ts:L41` rejects the null that a server declaring `Optional[str] = None` at `user.py:L82` sends.

Importing a document type is not currently possible:

```typescript
import { Document } from '../schema/document';
```

The import fails, because `document.ts` declares two schema values at `L65-L73` and `L86-L92` and exports no type. The three
committed importers at `store/documentSlice.ts:L22`, `services/api.ts:L80` and `services/collaboration.ts:L15` fail the same way.

Three changes would unblock the directory, recorded rather than performed: export an inferred `Document` type from
`document.ts`, export the `DocumentCreate` and `DocumentUpdate` shapes `services/api.ts:L80` asks for, and declare `zod`.
