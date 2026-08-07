# Onboarding Guide

The `microsoft-word-u33ko0` repository does not run. Three commands complete on a clean machine, and
every path past them stops at a line named below. Completing and succeeding are different outcomes
here: two of the three report success, and the type-checker finishes its work and then exits
non-zero because it found 76 errors. Work through the setup, expect the failures this guide predicts,
then use the closing task list to choose what to repair first.

The [root README](../README.md) is the only other onboarding document here, and six of its statements
contradict the committed tree, one of them only in part. Three sit in the README's installation and run
steps, at `L29`, `L42` and `L55`, so a developer following that file in order hits all three before
reaching any code. For setup, follow this guide instead. The
engagement that produced this file left the root README untouched, and
[decision-log.md](decision-log.md) will record that boundary as conflict C1. That file is planned for a
later checkpoint and is not committed yet.

Onboarding documentation normally ends with a running application, and the committed code cannot
start one. The honest path appears here instead: the commands that work, the exact line where every
remaining path stops, and the change a future contributor would make. Nothing below is fixed, and no
entry describes a repair as done. The pending [decision-log.md](decision-log.md) will record the
deviation as conflict C3.

## How to read this guide

Every factual claim carries a locator in the form `path:Lnn`, and most locators name the symbol at
that line. Read the symbol name as the durable half of the citation. Line numbers move whenever
anyone edits a file above them, and symbol names do not.

Three conventions govern the locators:

- Locators point at the **committed state at the current branch head**, which includes the inline
  documentation added to 44 source files. A locator matches what you see when you open the file
  today.
- Line numbers are **physical**. No original source or configuration file in this repository ends
  with a newline, so `wc -l` reports one line fewer than each of those files contains. The Markdown
  this documentation engagement added does end with a newline, so no README and no file under `docs/`
  carries that discrepancy.
- A range such as `L111-L119` covers every line in the span, inclusive.

Six words carry one fixed meaning throughout this documentation set.

| Term | Meaning |
| ------ | --------- |
| router | A FastAPI `APIRouter` instance |
| handler | A route function carrying a `@router` decorator |
| service | A domain service class under `backend/app/services/` |
| adapter | A persistence module under `backend/app/db/` |
| slice | A Redux Toolkit slice under `frontend/src/store/` |
| marker | A `HUMAN ASSISTANCE NEEDED` comment left by the code's authors |

The three documents under `documentation/` record declared intent rather than committed behaviour.
Anything drawn from them carries the label **declared intent** and a citation by heading name plus
line, because all three use unnumbered headings only. A numbered section citation anywhere in this
set refers to the generated Technical Specification, a separate document, and the text says so when
it does.

## What this application is

The repository implements a browser-based word processor. React and TypeScript build the client,
Python and FastAPI serve the application programming interface (API), and Google Cloud provides
persistence. The [root README](../README.md) states that framing accurately at `L4`.

Six capabilities carry implementing code today. Learn their names before reading any defect list,
because every gap in this guide lands against one of them.

- **Document lifecycle.** Create, read, update and delete, abbreviated CRUD, across five HTTP
  handlers and four service methods.
- **Ownership-based authorization.** Twelve handlers declare bearer authentication, but only three
  document read, update and delete paths attempt owner checks, and current call defects stop them. No
  template object authorization exists. The eleven handlers without an owner check include document
  create and list, both profile handlers and all five template handlers, so a valid token alone
  decides access on each. [troubleshooting.md](troubleshooting.md#g91-the-backend-http-surface)
  carries the locators.
- **Rich-text editing.** Draft.js holds the editor state, and two helpers apply inline and block
  formatting.
- **Templates.** Five handlers and a card gallery on the client.
- **Export to PDF and DOCX.** The upload and version 4 signing sequence is complete in form and
  reaches no bucket. Four independent barriers stop it, and the conversion itself returns a
  placeholder string. [integration-guide.md](integration-guide.md#integration-inventory) lists all
  four.
- **Real-time collaboration.** Designed and never connected. No route reaches the service, and the
  client and the server speak different protocols.

[architecture-overview.md](architecture-overview.md) maps the six top-level directories and the four
tiers they form. Read it next if you want the shape of the system before its setup.

## Prerequisites

**Every command in this guide is written for a POSIX shell on Linux or macOS.** That scope follows
the repository rather than a preference. `scripts/setup_dev_environment.sh:L10` installs packages
through `apt-get`, which ties the only committed setup script to Debian or Ubuntu, and both images
build on Linux bases at `infrastructure/docker/backend.Dockerfile:L2` and
`infrastructure/docker/frontend.Dockerfile:L2`. No committed file targets Windows. On Windows, run
everything inside Windows Subsystem for Linux (WSL) to use the commands unchanged, or substitute the
two PowerShell equivalents named in [the backend setup section](#setting-up-the-backend). The
frontend commands need no substitution, because `npm` and `npx` take the same form on every platform.

Four tools carry a declared version, and each version comes from a committed file. Each also carries a
conflict worth knowing before you install anything. Two more tools are needed and declared nowhere:
Git, to obtain the code, and `zip`, which `scripts/deploy.sh:L19` calls and
`scripts/setup_dev_environment.sh:L10` never installs. The command block below installs all six.

| Tool | Version to install | Where it is declared | Conflict |
| ------ | -------------------- | ---------------------- | ---------- |
| Python | 3.9 | `infrastructure/docker/backend.Dockerfile:L2` pins `python:3.9-slim` | Declared three ways and enforced nowhere. `../README.md:L23` asks for 3.8 or later, and `scripts/setup_dev_environment.sh:L10` installs unpinned `apt-get` packages. No `.python-version` and no dependency manifest exists. 3.9 is also below the floor the current `google-cloud-firestore` release sets, covered below the table |
| Node.js | 14 | `.github/workflows/ci.yml:L17` sets `node-version: '14'`, and `infrastructure/docker/frontend.Dockerfile:L2` pins `node:14-alpine` | Declared three ways and enforced nowhere. `../README.md:L22` asks for 14 or later. `frontend/package.json` declares no `engines` field, and no `.nvmrc` exists |
| PostgreSQL | 13 | `infrastructure/docker/docker-compose.yml:L31` pins `postgres:13` | The database and user Compose provisions disagree with the ones `scripts/setup_dev_environment.sh:L31-L32` creates. [../infrastructure/docker/README.md](../infrastructure/docker/README.md) owns this citation |
| Google Cloud SDK | Latest release from Google's own installer | `../README.md:L24` names the SDK and no version | The declaration pins nothing, and no pin is needed. The SDK is a host tool that ships its own bundled Python, so it takes no part in the resolution below. `backend/app/db/firestore.py:L40` constructs a Firestore client at import time, so Application Default Credentials, usually shortened to ADC, must already resolve before the module loads |

**All three declared runtimes have passed end of life, often written EOL.** Python 3.9 ended support
on 31 October 2025, with 3.9.25 as its final security release. Node 14 ended support on 30 April
2023. PostgreSQL 13 ended support on 13 November 2025, with 13.23 as its final release. None of the
three receives security patches as of 6 August 2026, so a machine built to these declarations runs
unsupported software at every layer. Verification for this documentation set used Python 3.9 and Node
14 anyway, because they are the highest versions the repository documents anywhere.

That end-of-life status changes how you install two of the four tools. A current distribution's own
repositories no longer carry Python 3.9 or Node 14, so install each through its version manager and
the rest through the package manager. The commands below are the full prerequisite set for a Debian
or Ubuntu machine:

```bash
# Tools the distribution still carries. zip is needed by scripts/deploy.sh:L19,
# and the committed setup script never installs it.
sudo apt-get update
sudo apt-get install -y git curl zip build-essential postgresql

# Node 14 through nvm, the Node Version Manager. Install nvm from the installer
# its project publishes, then pin the version this repository declares.
nvm install 14
nvm use 14

# Python 3.9 through pyenv. pyenv resolves "3.9" to the latest 3.9 patch.
pyenv install 3.9
pyenv local 3.9

# Google Cloud SDK, which supplies both the gcloud and gsutil commands
# that scripts/deploy.sh calls.
curl https://sdk.cloud.google.com | bash
```

On macOS, `brew install git curl zip postgresql@13` replaces the first block and
`brew install --cask google-cloud-sdk` replaces the last. The two version managers install and run
identically on both platforms. Using a version manager for the two runtimes also keeps an unsupported
interpreter out of the system path.

Every Python version below is pinned. The repository commits no manifest, so this documentation set
resolved one mutually compatible set for Python 3.9 and records it here rather than leaving the
choice open. Unpinned guidance is not a reproducible clean-machine path, and a fresh resolution on a
later date would install a different and possibly incompatible set. Adding the resolved set to a
committed manifest fell outside this engagement, so the pins live in this document only.

Choosing a newer runtime changes which failures you meet rather than removing them. Current Pydantic
breaks `backend/app/core/config.py:L48` on the first import, and
[the backend setup section](#setting-up-the-backend) records why.

Python 3.9 also conflicts with a package the backend imports. Google's Python client libraries
support only the interpreter versions in active or maintenance support, and the current
`google-cloud-firestore` release requires Python 3.10 or newer. A 3.9 interpreter therefore resolves
`pip install google-cloud-firestore` to an older release rather than failing outright, so the
environment pins an unmaintained client without saying so.
`backend/app/db/firestore.py:L34` and `backend/app/services/document_service.py:L57` both import from
it. [../backend/app/README.md](../backend/app/README.md) states the boundary as a release whose
`Requires-Python` accepts the interpreter in use, for exactly this reason.

PostgreSQL earns a lower priority than the table suggests. `backend/app/db/sql.py:L16-L19` builds an
engine, a session factory and a declarative base, and no module in the repository subclasses that
base, defines a model, or calls the session. The relational path stays dead while Firestore carries
every document write. See [data-model.md](data-model.md#persistence-overview) for the split.

Git is installed above, and the README's clone command still cannot get you the code.
`../README.md:L29` clones `https://github.com/your-organization/microsoft-word.git`, a placeholder
organisation. Clone from wherever this repository actually lives.

## Before you install anything

**No reproducible supported install exists in this repository.** Neither side of the application
pins its dependencies. The frontend commits no lock file, and the backend commits no dependency
manifest and no lock file, so no package set here is pinned, reviewed, or reproducible. Two
developers following the steps below on different days will resolve different package versions, and
neither result has been reviewed for compatibility or for known vulnerabilities.

Treat every install command in this guide as an **isolated diagnostic in a throwaway environment**
rather than as a setup step. The commands are worth running, because they are how the type-check
profile and the import census in this documentation set were measured. They do not produce an
environment to build on.

Three consequences follow, and each one shapes how the next two sections should be read.

- **An unpinned install resolves whatever is current.** Where a table below says a version constraint
  is unestablished, read that as a gap in the repository. It is not a recommendation to accept any
  release. Published advisories affect several of the packages this code imports. `python-jose`
  through 3.3.0 carries CVE-2024-33663, an algorithm confusion weakness with OpenSSH ECDSA and other
  key formats, fixed in 3.4.0. That advisory lands directly on this code.
  `backend/app/core/config.py:L115` declares `ALGORITHM: str` with no allowed-value check, and
  `backend/app/core/security.py:L79` passes the value straight through to `jwt.encode`. Pydantic 1.x,
  `python-multipart` and `celery` each carry published advisories of their own across their release
  histories. None of the four can be assessed here, because no version is pinned.
- **A newer runtime is not automatically safer.** Current releases of FastAPI and of the Google Cloud
  client libraries have moved their supported Python range past 3.9. Meanwhile
  `backend/app/core/config.py:L48` requires Pydantic 1.x. The repository therefore pins no runtime and
  no library set that is simultaneously supported and compatible, and no combination in this guide has
  been verified as both.
- **Nothing here should be used to build a deployable image.** The dependency defects are one class
  among nine in [troubleshooting.md](troubleshooting.md#the-defect-classes), and installing packages
  resolves that class alone.

**Required future work.** A reviewed dependency manifest and a committed lock file on both sides.
Both need a tested compatibility and security matrix behind them, covering the runtime, the framework
and the cryptography packages. That work falls outside this documentation engagement, which adds no
manifest and changes no dependency. Until it lands, no statement in this guide should be read as a
supported configuration.

## Setting up the frontend

`npm ci` cannot run here. npm, the package manager that ships with Node.js, installs strictly from a
lock file when you run `npm ci`, and the repository commits none. `npm install` is the only command
that resolves the declared dependencies, and it resolves them unpinned, so the caveats in
[the section above](#before-you-install-anything) apply to everything below.

```bash
cd frontend
npm install
```

The install succeeds. One observed run resolved 1,532 packages, and that figure follows the registry
rather than this repository, so read it as a sighting rather than a constant. Every `npm ci`
invocation in the repository fails, including both automated ones.

| Invocation | Locator | Why it fails |
| ------------ | --------- | -------------- |
| By hand inside `frontend/` | run directly | No `package-lock.json` is committed, and `npm ci` needs one |
| Continuous integration, shortened to CI | `.github/workflows/ci.yml:L19`, which sets no `working-directory` | The step runs at the repository root, where no `package.json` and no lockfile exist |
| The frontend image build | `infrastructure/docker/frontend.Dockerfile:L11`, after `:L8` copies `package*.json` | The glob matches `package.json` alone |

The CI job therefore stops at its install step, and `npm test` at `.github/workflows/ci.yml:L21` and
`npm run build` at `:L23` never run. The frontend image stops at the same command.

Type-check the client next. The check runs, which makes it the most useful command in the repository
for understanding the client's state.

```bash
cd frontend
npx tsc --noEmit
```

The command reports **76 errors** and emits nothing, because `frontend/tsconfig.json:L25` sets
`noEmit`. The distribution below is the fastest map of what the client needs.

| Code | Count | Meaning | Concentrated in |
| ------ | ------- | --------- | ----------------- |
| `TS2307` | 57 | Cannot find module | 44 from the unmapped `@/` prefix, 13 from the five undeclared packages |
| `TS2305` | 6 | Module has no exported member | 5 from the absent `Document` type family, 1 from `Switch` at `frontend/src/App.tsx:L15` |
| `TS7006` | 5 | Parameter implicitly has an `any` type | Four sites in `frontend/src/services/api.ts`, one in `frontend/src/pages/Editor.tsx` |
| `TS2322` | 4 | Type not assignable | The four `Route` elements at `frontend/src/App.tsx:L52-L55`, which pass the router version 5 `component` prop |
| `TS2614` | 2 | No exported member, import form mismatch | `frontend/src/store/index.ts:L21` and `:L22` |
| `TS2552` | 1 | Cannot find name | `frontend/src/services/api.ts:L142`, an undefined `store` |
| `TS2339` | 1 | Property does not exist on type | `frontend/src/services/api.ts:L142`, reading `.auth` off the store state |

[../frontend/src/README.md](../frontend/src/README.md) owns this profile.

Five packages are required and none is declared, so `npm install` fetches none of them.
`frontend/package.json:L6-L14` declares exactly seven runtime dependencies: `@reduxjs/toolkit`,
`react`, `react-dom`, `react-redux`, `react-router-dom`, `tailwindcss` and `typescript`.

Four of the five are **imported runtime packages**, each named in an `import` statement and therefore
findable by grep and reported by the type-checker.

| Undeclared package | Where the code imports it |
| -------------------- | --------------------------- |
| `draft-js` | Six modules, including `frontend/src/utils/formatting.ts:L13` and `frontend/src/components/DocumentCanvas.tsx:L21` |
| `zod` | Four modules: the three under `frontend/src/schema/`, for example `frontend/src/schema/document.ts:L43`, plus `frontend/src/utils/validation.ts:L13` |
| `axios` | `frontend/src/services/api.ts:L78` and `frontend/src/services/auth.ts:L68` |
| `socket.io-client` | `frontend/src/services/collaboration.ts:L13` |

The fifth is a **required type package with no direct import**. `@types/draft-js` appears in zero
import statements anywhere in `frontend/src/`, and the six `draft-js` importers need it to typecheck
because `draft-js` ships no bundled type declarations. Deriving the dependency set by grepping import
statements therefore finds four packages and misses this one, and the omission surfaces only after the
other four resolve.

Declaring the five falls outside this documentation engagement, so `frontend/package.json` still omits
them. [troubleshooting.md](troubleshooting.md#five-npm-packages-the-manifest-omits) carries the entry
with the same split. Installing them by hand gets you a shorter error list and no working build, for
the reason [the pitfalls section](#common-pitfalls) gives.

Two artifacts appear after the install. `npm install` writes `frontend/package-lock.json` and creates
`frontend/node_modules/`, and the repository tracks neither.

The absent lock file is the defect here, not a preference. A lock file records the exact resolved
version and an integrity hash for every package in the tree, which is what makes an install
reproducible and auditable. Committing a reviewed one is the fix, and it is required future work
rather than something this documentation engagement performs, because adding a dependency artifact
falls outside a documentation change. Two points follow for the file you just generated. The lock
file a single unreviewed `npm install` produces is a record of one machine on one day, so it is not a
substitute for the reviewed artifact the repository needs. Discarding it silently is not the answer
either, and this guide does not ask you to. If you generated it while following these steps, take one
of two deliberate routes. Carry it into the review that adds a manifest, or remove it and record why.
`frontend/node_modules/` is build output and belongs in an ignore rule, and no `.gitignore` is tracked
anywhere in this repository, which
[troubleshooting.md](troubleshooting.md#g95-secrets-state-and-data-retention) records as entry 33.

**An unlocked install is neither reproducible nor auditable.** That is a risk rather than an
inconvenience. `npm install` resolves every declared range and every transitive range to whatever the
registry serves at that moment. Two installs of this one commit can therefore differ across hundreds
of packages, and nothing records which resolution either build used. No integrity hash is stored for a
build either. A published advisory cannot be matched against what a given machine installed, and a
compromised release inside a transitive range enters the tree unremarked. The generated
`frontend/package-lock.json` pins your own machine only, because the repository does not track it.
`frontend/package.json` declares its seven runtime dependencies as ranges rather than exact versions.
Committing a lockfile changes what the pipeline installs, which makes it a repository change rather
than a documentation change, so this pass leaves the manifest as it found it.
[troubleshooting.md](troubleshooting.md#npm-ci-cannot-run-anywhere) carries the entry.

Starting the development server fails. `npm start` runs `react-scripts start`, which resolves modules
through webpack rather than through the `tsconfig` `paths` block, so every `@/` specifier fails there
as well. No server serves the client.

## Setting up the backend

The backend has no dependency manifest. No `requirements.txt`, `pyproject.toml`, `setup.py`,
`setup.cfg`, `tox.ini`, `Pipfile` or `.python-version` exists anywhere in the repository. Two
committed instructions install from a file nobody added: `../README.md:L42` and
`scripts/setup_dev_environment.sh:L26` both run `pip install -r requirements.txt`. A third,
`infrastructure/docker/backend.Dockerfile:L8`, copies the same absent file into the image.

Build a throwaway environment by hand. Use a virtual environment so nothing here touches a system
interpreter, and discard it afterwards.

```bash
cd backend
python3.9 -m venv venv
source venv/bin/activate          # bash, zsh, or any POSIX shell
```

```text
cd backend
py -3.9 -m venv venv
.\venv\Scripts\Activate.ps1       # Windows PowerShell
```

Those are the two commands with a Windows PowerShell equivalent. Outside WSL they read
`py -3.9 -m venv venv` and `venv\Scripts\Activate.ps1`, and every command after them is identical on
all three platforms.

**One authoritative Python dependency inventory exists, and it is not in this file.**
[../backend/app/README.md](../backend/app/README.md) carries it, and it defines the model every
count in this documentation set uses. Seventeen distributions from the Python Package Index (PyPI)
are required: ten named by an `import` statement under `backend/app/`, and seven runtime companions
that no import names. Thirteen of the seventeen have to be named to a package manager, because
`starlette`, `ecdsa`, `rsa` and `pyasn1` arrive transitively. Each row there gives the version
boundary the code establishes and the code fact that establishes it. Every other document in this
set, this one included, defers to that table rather than restating a list, so there is one list to
keep correct. Install from it.

Three categories carry the weight there, and knowing them tells you when each package fails. A
**directly imported** distribution is named by an `import` statement under `backend/app/`, so a
grep finds it and a resolver reports it by name. A **runtime companion** is needed by the running
system while no import names it, which covers `uvicorn`, `starlette`, `python-multipart`, `bcrypt`,
`ecdsa`, `rsa` and `pyasn1`. Four of those seven arrive transitively, and `uvicorn`, `bcrypt` and
`python-multipart` do not, so those three must be named explicitly. `bcrypt` and
`python-multipart` block a route rather than a build, and each surfaces at the first login rather
than at install. A **configuration-selected** distribution is chosen by a configuration value
rather than by code, and the three of those sit outside the seventeen, in the table below.

Reading import statements alone therefore builds an incomplete environment. Ten names are visible
that way and seven are not, and three of those seven still have to be installed by name, so the
build stops once per missing distribution rather than once in total.
[troubleshooting.md](troubleshooting.md#the-progressive-python-dependency-resolution-failure) names
that pattern the progressive dependency-resolution failure and records why import statements cannot
produce a working environment on their own.

`starlette` needs no line in an install command.
`backend/app/services/collaboration_service.py:L36` imports `WebSocket` and `WebSocketDisconnect`
through FastAPI, which re-exports both from Starlette, so the installer resolves it from `fastapi`.
The inventory still lists it, as one of the seven runtime companions, and marks it among the four
that arrive transitively.

Three further distributions are chosen by a configuration value rather than by an import or by a
committed command. The inventory therefore does not count them, and a running environment still needs
them. No code fact fixes the choice, because the value that selects each one is absent from the
repository.

| Distribution | The value that selects it | When it is needed |
| --- | --- | --- |
| A PostgreSQL driver, for example `psycopg2-binary` | The `postgresql://` scheme in `settings.DATABASE_URL`, supplied by `infrastructure/docker/docker-compose.yml:L24` and declared at `backend/app/core/config.py:L118` | `backend/app/db/sql.py:L16` builds an engine at import time, and SQLAlchemy resolves a driver from the scheme in the URL |
| A Redis client | The `redis://` scheme in `settings.REDIS_URL`, declared at `backend/app/core/config.py:L119` | `backend/app/tasks/background_tasks.py:L98` hands Celery that broker URL, and a worker needs the client to attach. [../backend/app/tasks/README.md](../backend/app/tasks/README.md) records that no dependency manifest declares it |
| `cryptography` | An RSA or ECDSA name in `settings.ALGORITHM`, declared as a bare `str` at `backend/app/core/config.py:L115` with no allowed-value check | `backend/app/core/security.py:L79` passes the value straight to `jwt.encode`. A symmetric algorithm such as HS256 needs nothing extra |

**Installing every one of them still leaves the backend unable to import.** Dependencies are
third-party, and all four blockers here are first-party: the absent `settings` instance, the four
router names `backend/app/main.py:L16-L19` imports against the bare `router` each module exports, two
absent modules, and one undefined name. A complete environment moves the first error a run reports
from `ModuleNotFoundError` to the `ImportError` that
[the next section](#where-a-run-stops-with-evidence) traces. Nothing else moves, and no package
install makes this application start.

One command covers the whole set, and it names sixteen distributions: the thirteen of the seventeen
that have to be named, plus the three the table above selects by configuration. The four transitive
arrivals come with them. The `pydantic` upper bound is the one constraint that matters, for the
reason the table above gives.

```bash
pip install \
  "fastapi>=0.89.0" "pydantic>=1.10,<2" "SQLAlchemy>=1.4" \
  python-jose passlib bcrypt python-multipart \
  celery redis psycopg2-binary cryptography uvicorn \
  google-cloud-firestore google-cloud-storage google-cloud-pubsub google-auth
```

`starlette` arrives as a `fastapi` dependency, so the command installs seventeen distributions from
sixteen names.

Configuration needs a `.env` file the repository does not commit.
`backend/app/core/config.py:L121-L124` points `Settings` at `.env`, and neither `.env` nor
`.env.example` exists. None of the nine fields at `backend/app/core/config.py:L111-L119` carries an
explicit default. Pydantic 1.x treats the two `Optional[str]` fields as defaulting to `None`, which
leaves seven values mandatory: `PROJECT_NAME`, `API_V1_STR`, `SECRET_KEY`,
`ACCESS_TOKEN_EXPIRE_MINUTES`, `ALGORITHM`, `DATABASE_URL` and `REDIS_URL`. Supply all seven or
`Settings()` raises a validation error naming every missing key at once.

A file is not the only way to supply them, and the missing `.env` is therefore not a hard stop.
`Settings` extends Pydantic's `BaseSettings`, imported at `backend/app/core/config.py:L48` and
subclassed at `:L51`, which reads each declared field from the process environment and falls back to
the `env_file` named at `:L123`. Exporting the seven names in your shell satisfies the model exactly
as a committed `.env` would. A process environment variable also takes precedence over a file entry of
the same name. `infrastructure/docker/docker-compose.yml:L24` uses that same mechanism, injecting
`DATABASE_URL` as an environment variable rather than a file.
[../infrastructure/docker/README.md](../infrastructure/docker/README.md) carries the full injector
matrix. Whichever source you pick, the six settings the model never declares stay out of reach.
Pydantic 1.x populates only the fields the model declares, and ignores an environment variable that
matches none of them.

Six further settings are read at runtime and declared nowhere, so each raises `AttributeError` at the
point of the read even on a fully supplied environment: `ALLOWED_ORIGINS`, `PROJECT_ID`,
`STORAGE_BUCKET_NAME`, `SIGNED_URL_EXPIRATION`, `EXPORT_BUCKET_NAME` and `DOCUMENT_BUCKET_NAME`.
Adding them to `.env` does not help, because `Settings` declares no field to receive them. Fifteen
settings are in play: nine declared and six read but never declared.
[../backend/app/core/README.md](../backend/app/core/README.md) lists all fifteen with their
classification.

The setup script will not finish, so run the steps above by hand instead.
`scripts/setup_dev_environment.sh` stops or misfires at three points:

- `:L26` installs from the absent `requirements.txt`.
- `:L40` copies the absent `.env.example`.
- `:L47-L48` run `python manage.py makemigrations` and `python manage.py migrate`. Both are Django
  commands, and this is a FastAPI project. `:L55` prints a `manage.py runserver` instruction for the
  same reason.

See [../scripts/README.md](../scripts/README.md).

## What you can actually run today

Three commands complete. Two of them succeed, one completes and reports failure, and every other path
stops.

| Command | Working directory | Result | Exit status |
| --- | --- | --- | --- |
| `npm install` | `frontend/` | Succeeds. One observed run resolved 1,532 packages | Zero |
| `npx tsc --noEmit` | `frontend/` | Completes and reports 76 errors. Emits nothing, per `frontend/tsconfig.json:L25` | Non-zero. The compiler exits non-zero whenever it reports an error, so any script chaining on success stops here |
| The parse check below | repository root | Succeeds. All 18 Python modules under `backend/` parse, so every file is syntactically valid | Zero |

The middle row is worth reading twice. The type-checker runs to completion, which makes it the most
informative command in the repository, and it still fails. Reading "the tool ran" as "the check
passed" is the easiest mistake to make here. That is why this section counts commands that complete
rather than commands that succeed.

Parse the backend without writing anything into the tree:

```bash
python -c "import ast, pathlib; [ast.parse(p.read_text(encoding='utf-8'), str(p)) for p in sorted(pathlib.Path('backend').rglob('*.py'))]"
```

`python -m compileall backend` answers the same question and is not interchangeable with it, because
`compileall` writes a `__pycache__` directory holding a `.pyc` file beside every module it compiles.
The repository commits no `.gitignore` at any path, so those directories appear as untracked entries
in `git status` and can be staged by accident. Use the parse above, or run `compileall` and then delete
what it left:

```bash
python -m compileall backend
find backend -type d -name __pycache__ -prune -exec rm -rf {} +
```

Nothing else runs. No server starts, no test suite passes, neither container builds, and
`terraform init` does not complete. A successful parse proves the syntax valid and says nothing about
whether a module imports, and [the next section](#where-a-run-stops-with-evidence) shows why the two
diverge sharply here.

The flowchart below branches on what you want to do and terminates each branch in the line that stops
it.

```mermaid
graph TD
    START{"What do you<br/>want to do?"}

    START --> A["Install client dependencies"]
    START --> B["Type-check the client"]
    START --> C["Parse the backend"]
    START --> D["Start the client"]
    START --> E["Import the backend"]
    START --> F["Start the server"]
    START --> G["Build a container"]
    START --> H["Run the test suite"]
    START --> I["Apply the Terraform"]

    A --> AOK["Succeeds, exit 0<br/>npm install resolves the tree"]
    B --> BOK["Completes, exit non-zero<br/>tsc --noEmit reports 76 errors"]
    C --> COK["Succeeds, exit 0<br/>all 18 modules parse"]

    D -.->|"webpack ignores the tsconfig paths block"| DNO["Stops<br/>frontend/tsconfig.json:L10-L16<br/>declares no '@/*' alias"]
    E -.->|"ImportError: cannot import name 'settings'"| ENO["Stops<br/>backend/app/api/auth.py:L81<br/>reached from main.py:L16"]
    F -.->|"the application object never imports"| ENO
    G -.->|"npm ci with no lockfile"| GNO1["Stops<br/>infrastructure/docker/frontend.Dockerfile:L11"]
    G -.->|"COPY of an absent requirements.txt"| GNO2["Stops<br/>infrastructure/docker/backend.Dockerfile:L8"]
    H -.->|"'app' is not on sys.path from the repository root"| HNO1["Stops<br/>backend/tests/test_api.py:L3"]
    HNO1 -.->|"then, once backend/ and backend/app/ are on the path"| HNO2["Stops again<br/>6 import targets name no file,<br/>3 services modules resolve only<br/>from backend/app/"]
    I -.->|"three module sources absent"| INO["Stops<br/>infrastructure/terraform/main.tf:L68, :L77, :L86"]

%% A solid edge marks a path that runs to completion, and its node states whether the run succeeded.
%% A dashed, labelled edge marks a path that stops before completing, and every failure node names the
%% file and line that stops it.
```

## Where a run stops, with evidence

Two stopping points block the application itself, one per deployable unit. Neither has a single
cause. Each has one cause that a run reports first, and at least one more waiting behind it. A
developer who repairs only what the error message names meets the next failure straight away. Both
subsections below separate the first hit from what is latent behind it.

### The backend cannot import

`import app.main` raises `ImportError: cannot import name 'settings' from 'app.core.config'`. The
chain has three links:

1. `backend/app/main.py:L16` imports `auth_router` from `app.api.auth`.
2. `backend/app/api/auth.py:L81` imports `settings` from `app.core.config`.
3. `backend/app/core/config.py` defines the `Settings` class at `L51` and the `get_settings()`
   factory at `L126`, and creates no module-level `settings` instance. No `settings =` assignment
   exists at any line in the file.

Eight modules import that absent name: `backend/app/main.py:L20`, `backend/app/api/auth.py:L81`,
`backend/app/db/firestore.py:L36`, `backend/app/db/sql.py:L14`,
`backend/app/services/collaboration_service.py:L39`,
`backend/app/services/document_service.py:L60`, `backend/app/services/export_service.py:L61` and
`backend/app/tasks/background_tasks.py:L92`. Nine module import failures trace to it, because
`app.api.documents` reaches the same name indirectly through the adapter at
`backend/app/db/firestore.py:L36`.

A census imported each of the 15 modules under `backend/app/` in a fresh interpreter. The census ran
with third-party packages present and Pydantic pinned to the 1.x line the code requires. Only **3 of
the 15 modules** import successfully, and 12 fail. The three that import are `app.core.config`,
`app.schema.document` and `app.schema.user`.
[../backend/app/README.md](../backend/app/README.md) owns the census.

Six causes sit behind that one error message, and only the first is visible today. Each row below
surfaces only once every row above it is repaired.

| Order | Cause | Locator | What a run reports now |
| --- | --- | --- | --- |
| First hit | No module-level `settings` instance | `backend/app/core/config.py`, which defines `Settings` at `L51` and `get_settings()` at `L126` and assigns `settings` at no line | `ImportError: cannot import name 'settings' from 'app.core.config'` |
| Second | The absent `app.services.user_service` module | `backend/app/api/auth.py:L83` imports `UserService` from it, and `backend/app/api/users.py:L24` imports it too. No file exists at that path | Nothing. `ModuleNotFoundError` surfaces from the same file the row above stops in, before `main.py` evaluates any router name |
| Third | Four router names that no module exports | `backend/app/main.py:L16-L19` imports `auth_router`, `documents_router`, `users_router` and `templates_router`, and all four modules export the bare name `router` | Nothing. The four `ImportError`s surface one at a time, because each import line stops `main.py` on its own |
| Fourth | Two absent template modules | `backend/app/api/templates.py:L70` imports from `app.schema.template` and `:L71` from `app.services.template_service`, and neither file exists | Nothing. Reached when `backend/app/main.py:L19` executes `app.api.templates` |
| Fifth | The absent `init_db` symbol | `backend/app/main.py:L22` imports `init_db` from `app.db.sql`, which defines `engine`, `SessionLocal`, `Base` and `get_db` and no `init_db` | Nothing. Reached once all four router imports resolve |
| Latent | Undefined names that raise at execution rather than at import | Registered in [troubleshooting.md](troubleshooting.md#the-verified-import-census) | Nothing, and nothing above clears them. `Optional`, `User` and `UserService` in `backend/app/core/security.py`, `asyncio` and `json` in `backend/app/services/collaboration_service.py`, and `datetime` in `backend/app/tasks/background_tasks.py` |

A future contributor cannot stop after two repairs. Adding the `settings` instance clears nine of
the twelve failing modules, and the next error comes from the same file rather than from
`main.py`: `backend/app/api/auth.py:L83` asks for a module nobody wrote. Only once that module
exists do the four router names become the blocker, and two more repairs sit behind them. Plan the
work as the table's order, not as a pair of changes.

One more note on starting the server, because the README sends you to the wrong target.
`../README.md:L54-L55` runs `cd backend` and then `uvicorn main:app --reload`. The application object
sits at `backend/app/main.py:L24`, one directory deeper, so from `backend/` the target reads
`app.main:app`.

### The client cannot typecheck

`tsc --noEmit` reports 76 errors, and 57 of them say the compiler cannot find a module. **The first
hit is an import prefix that nothing maps.** Forty-four import statements, spread across thirteen
modules under `frontend/src/`, use a `@/` prefix, and `frontend/tsconfig.json:L10-L16` declares
five aliases that do not include it:

```text
"paths": {
  "@components/*": ["components/*"],
  "@utils/*": ["utils/*"],
  "@styles/*": ["styles/*"],
  "@hooks/*": ["hooks/*"],
  "@services/*": ["services/*"]
}
```

The prefix accounts for 44 of the 57 module-resolution errors. The four imported undeclared packages
account for the other 13. `@types/draft-js` accounts for none of them, because a package no module
imports produces no module-resolution error.

**A second cause is latent behind it,** so adding `@/*` to that block still would not produce a
working build. `react-scripts` 5.0.1, pinned at `frontend/package.json:L29`, does not translate
`tsconfig` path mappings into webpack module resolution, so the bundler keeps failing on the same
specifiers after the compiler has accepted them. Nothing reports the resolver problem while the
`paths` entry is missing, because no bundle is attempted. A future contributor would need both a
`paths` entry and a resolver change, and
[troubleshooting.md](troubleshooting.md#the-unmapped-import-prefix) carries the entry.

### Everything else

The remaining defects live in [troubleshooting.md](troubleshooting.md), ordered twice over. A
symptom-first index runs in the order a developer meets each problem, and eight taxonomy sections run
from absent modules through platform defects. Open
[the symptom-first index](troubleshooting.md#symptom-first-index) when you hit an error this guide
did not predict. For the eleven separate reasons a deploy fails, read
[deployment-guide.md](deployment-guide.md#why-a-deploy-fails-as-committed).

## Common pitfalls

Four traps cost the most time, and no single file reveals any of them. Each one looks like a local
problem and has a cause somewhere else.

| Pitfall | What you see | Where the cause sits |
| --------- | -------------- | ---------------------- |
| The `@/` import prefix resolves nowhere | 44 of the 57 module-resolution errors, and a client that never bundles | `frontend/tsconfig.json:L10-L16` plus the `react-scripts` pin at `frontend/package.json:L29` |
| `npm ci` cannot run anywhere | The CI job and the frontend image both stop at their install step | `.github/workflows/ci.yml:L19` and `infrastructure/docker/frontend.Dockerfile:L11` |
| Six backend distributions appear in no import statement | The environment build fails again after each fix | [The backend setup section](#setting-up-the-backend) and [the authoritative inventory](../backend/app/README.md) |
| Tailwind CSS never compiles | An interface with no styling at all | No `tailwind.config.js`, no `postcss.config.js` and no committed stylesheet |

**The `@/` prefix.** Forty-four imports across 13 of the 26 frontend modules use it, and adding the alias to
`tsconfig` fixes only the compiler. `react-scripts` 5.0.1 resolves modules through webpack, which
reads no `paths` block, so the bundler keeps failing after the type errors disappear. Budget for two
changes rather than one.

**`npm ci`.** Use `npm install` locally. `npm ci` reads a lockfile and this repository commits none,
so both automated invocations fail before any test or build step runs. Any fix that adds a lockfile
also changes what the pipeline installs, which is why
[troubleshooting.md](troubleshooting.md#npm-ci-cannot-run-anywhere) records the two sites separately.

**The invisible six.** A developer who builds the Python environment by reading import statements
installs ten distributions and stops. Six more surface one at a time, each as execution reaches it:

- `uvicorn` when you try to serve the application.
- `bcrypt` when a password is hashed.
- `python-multipart` when a login form is posted.
- A PostgreSQL driver when the engine at `backend/app/db/sql.py:L16` connects.
- A Redis client when Celery attaches to the broker at `backend/app/tasks/background_tasks.py:L98`.
- `cryptography` when `settings.ALGORITHM` names an asymmetric signing algorithm.

The first three belong to [the authoritative inventory](../backend/app/README.md), which counts them
as one runtime and two conditional entries. The last three are chosen by a configuration value rather
than by an import, so the inventory excludes them.
[The backend setup section](#setting-up-the-backend) names each of those three beside the value that
selects it. Install from both places in one pass.

**Tailwind.** Utility classes appear throughout the components, and nothing compiles them. No Tailwind
configuration, no PostCSS configuration and no stylesheet is committed anywhere, so the classes reach
the browser as unrecognised strings.

Two styling conventions coexist besides, and neither renders. Tailwind utility classes appear in
`frontend/src/components/Header.tsx` and in the body of `frontend/src/pages/Templates.tsx`, while
eight other modules use bespoke semantic class names with no backing stylesheet. See
[troubleshooting.md](troubleshooting.md#tailwind-never-compiles) and
[../frontend/src/components/README.md](../frontend/src/components/README.md).

## How to extend the project

Follow the layering the code already uses. Six kinds of change have an established home, and the
table gives each one its destination and its trap.

| What you are adding | Where it goes | What to watch |
| --------------------- | --------------- | --------------- |
| An HTTP endpoint | A router module under `backend/app/api/`, registered in `backend/app/main.py` | `backend/app/main.py:L125-L128` mounts every router with no prefix, so documents and templates already collide on identical paths. Give a new router a prefix or plan the collision |
| Domain logic | A service class under `backend/app/services/` | 7 of the 9 public service methods are declared `async` and call the synchronous Firestore software development kit (SDK) inside, so the declaration promises concurrency the body does not deliver. The other 2 are the plain `def` export methods at `backend/app/services/export_service.py:L87` and `:L168`, which no caller can await. Pick one form deliberately, because the directory already uses both |
| A persistence call | An adapter function under `backend/app/db/` | No service consumes the four Firestore helpers in `backend/app/db/firestore.py`. Services construct their own client instead, so pick one path deliberately |
| A data contract | Both `backend/app/schema/` and `frontend/src/schema/` | Nothing generates either side from the other. See the trap below |
| Client state | A slice under `frontend/src/store/`, registered in `frontend/src/store/index.ts` | The store registers two reducer keys, and `frontend/src/services/api.ts:L142` reads a third that does not exist |
| A page or a component | `frontend/src/pages/` for a routed screen, `frontend/src/components/` for a reusable piece | Routed pages are declared in `frontend/src/App.tsx`. Several links already target routes the router never declares |

The contract trap deserves naming, because the repository already fell into it. No OpenAPI document
is committed, no client is generated, and no shared schema package spans Python and TypeScript. The
Pydantic definitions under `backend/app/schema/` and the Zod definitions under `frontend/src/schema/`
stay in agreement only while a human keeps them there. Adding a field on one side alone is exactly how
the existing divergences arose, and the ownership field now sits in four positions with none of them
canonical. Change both sides in the same commit, and read
[data-model.md](data-model.md#the-ownership-field-four-positions-none-canonical) before you pick a
field name.

[architecture-overview.md](architecture-overview.md#the-four-tiers) maps the tiers these directories
form. All nineteen module READMEs exist, 19 of 19 with none outstanding, and each one opens with the
responsibility of a single directory.

## Suggested next tasks, ordered

Order matters here, and step 1 unblocks every step below it. No backend change can be exercised while
the package fails to import, and no client change can be verified while the type-checker drowns in
module-resolution noise. Work top to bottom.

The order is not only a dependency order. Steps 1 through 3 turn unreachable code into reachable
code. Step 4 exists because reachable code with no authorization, no rate limit and no input bound is
worse than code that does not run. Fixing an import is quick and visible, and fixing a missing control
is neither, so the second is the one that gets skipped. Step 4 sits ahead of step 5 for the same
reason. Making an integration reachable publishes an interface, and the controls that interface needs
are absent from the committed code rather than merely disabled in it.

1. **Make the backend package import.** Five repairs stand between the committed tree and a
   package that imports, and they surface in a fixed order. Add a module-level `settings` instance
   to `backend/app/core/config.py`, which clears nine of the twelve failing modules. Write
   `app.services.user_service`, which `backend/app/api/auth.py:L83` and
   `backend/app/api/users.py:L24` both import and which fails next, from the same file the first
   error came from. Reconcile the four router names imported at `backend/app/main.py:L16-L19`
   against the bare `router` each module exports. Write `app.schema.template` and
   `app.services.template_service`, which `backend/app/api/templates.py:L70` and `:L71` import.
   Add `init_db` to `app.db.sql`, which `backend/app/main.py:L22` imports and which that module
   does not define. Until all five land, `import app.main` raises before any other work can be
   tested, and the undefined names registered in
   [troubleshooting.md](troubleshooting.md#the-verified-import-census) still raise at execution
   afterwards.
2. **Make the client typecheck.** `frontend/src/schema/document.ts` omits three requested names, not
   one. Export an inferred `Document` type first, following the pattern its sibling already uses at
   `frontend/src/schema/user.ts:L56`, which clears three of the five request positions on its own.
   The names `DocumentCreate` and `DocumentUpdate` need a schema written before a type can be
   inferred, because no Zod object in the module models a creation or an update payload. Then add
   `useAppSelector` and `useAppDispatch` to `frontend/src/store/index.ts`, which seven modules import.
   The three absent document names produce five of the six `TS2305` errors across three modules, and
   each edit removes a whole error class rather than a single line.
3. **Reconcile the field names.** The ownership field exists in four positions, and this
   documentation set names none of them canonical.
   [data-model.md](data-model.md#the-ownership-field-four-positions-none-canonical) lists all four
   with their locators. Do this work after steps 1 and 2, because a package that imports and a client
   that typechecks let you verify the change instead of guessing at it.
4. **Connect the collaboration and export paths.** No route constructs the collaboration service, and
   the export conversion returns a placeholder string.
   [integration-guide.md](integration-guide.md#integration-inventory) gives each of the four external
   integrations one of four reachability labels, and none of the four means a call reaches Google
   Cloud today. Both paths need a route and a caller before either can be tested, so they come last.

The code's authors left a backlog of their own. Thirty-three `HUMAN ASSISTANCE NEEDED` markers and
sixteen `TODO` comments sit across the repository, and each one names a gap its author already knew
about. Read the set as a prioritised list written by the people closest to the code.
[troubleshooting.md](troubleshooting.md#the-complete-marker-and-todo-register) carries the complete
register with a locator for every entry.

A second pair of figures appears elsewhere in this documentation set, and the two pairs count
different things. Twenty-seven markers and fifteen `TODO` comments count the subset living inside the
44 files that received inline documentation, and those two numbers measure a preservation obligation.
Use 33 and 16 when you are counting work to do.

## Related documentation

[docs/README.md](README.md) will index every document in this set once that file lands. Until then,
the list below is the map.

Repository-level documents beside this one:

- [architecture-overview.md](architecture-overview.md), the six-area map and the four tiers
- [troubleshooting.md](troubleshooting.md), every defect in the repository as a numbered register
- [deployment-guide.md](deployment-guide.md), what the infrastructure assets do and why a deploy fails
- [data-model.md](data-model.md), the Pydantic and Zod contracts and every field divergence
- [integration-guide.md](integration-guide.md), each external service under one of four reachability
  labels
- [decision-log.md](decision-log.md), every judgement this engagement made, including conflicts C1
  and C3

Module documentation for the facts this guide draws on:

- [../backend/app/README.md](../backend/app/README.md), the composition root and the import census
- [../backend/app/core/README.md](../backend/app/core/README.md), all fifteen settings with their
  classification
- [../frontend/src/README.md](../frontend/src/README.md), the bootstrap path and the type-check
  profile
- [../frontend/src/components/README.md](../frontend/src/components/README.md), the eight components
  and the two styling conventions
- [../infrastructure/docker/README.md](../infrastructure/docker/README.md), the two Dockerfiles and
  the Compose topology
- [../scripts/README.md](../scripts/README.md), the deploy and setup scripts and their blockers
- [../backend/tests/README.md](../backend/tests/README.md), why the test suite cannot run

Reference material, read and never edited:

- [../README.md](../README.md), the root README. Prerequisites at `L22-L23` are accurate. The
  instructions at `L42` and `L55` name a file and a path the tree does not carry.
- [Technical Specifications](<../documentation/Technical Specifications.md>), declared intent. The
  five level-one headings sit at `L3` INTRODUCTION, `L125` SYSTEM ARCHITECTURE, `L300` SYSTEM DESIGN,
  `L523` TECHNOLOGY STACK and `L620` SECURITY CONSIDERATIONS, and the file carries no numbered section
  anchor.
- [Software Requirements Specifications](<../documentation/Software Requirements Specifications (SRS).md>),
  declared intent. The 30-second auto-save requirement sits under the SAFETY heading at `L540`, at
  `L543`, and the editor implements a five-second debounce at `frontend/src/pages/Editor.tsx:L214`.
