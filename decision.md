# decision.md — Decision & Deviation Log

> Every move away from `project.md` gets logged here **before** the plan is edited.
> Purpose: never repeat a mistake, and never re-argue a settled decision without new information.

---

## Rules
1. **When to log:** any change to scope, architecture, stack, hosting, data handling, monetization, phase order, targets, or exit criteria; every spike result that picks between options; every mistake, incident, or dead end worth remembering.
2. **Never delete or rewrite an entry.** If a decision changes, add a new entry that supersedes it, and update only the old entry's **Status** line (`Superseded by D-###`).
3. **Numbering:** `D-###`, sequential, entries in chronological order below. Reference IDs in commits and PRs (`refs D-004`) and in `agent.md`.
4. **Evidence over opinion:** link docs, benchmarks, measurements, issues, or PRs.
5. **Every entry ends with a guardrail:** the concrete rule that stops us repeating the mistake.

**Status values:** `Proposed` · `Accepted` · `Superseded by D-###` · `Reverted`
**Types:** Scope · Architecture · Stack · Infra · Data/Privacy · Product · Monetization · Process · Incident/Lesson

---

## Index

| ID | Date | Type | Title | Status |
|---|---|---|---|---|
| D-000 | 2026-09-14 | Process | Baseline plan established (`project.md` v1.0) | Accepted |
| D-001 | 2026-09-14 | Scope | Pivot: no detector evasion → Inspector + Studio | Accepted |
| D-002 | 2026-09-14 | Infra | Hosting on Google Cloud Run with a billing account | Accepted |
| D-003 | 2026-09-15 | Product | Owner confirmations: name, subdomain, license, GitHub account | Accepted; URL + GitHub rows superseded by D-008 |
| D-004 | 2026-09-15 | Architecture | Dockerfile and compose.yaml at the repository root | Accepted |
| D-005 | 2026-09-15 | Stack | Synchronous SQLAlchemy with psycopg 3 (not async) | Accepted |
| D-006 | 2026-09-15 | Incident/Lesson | Use 127.0.0.1, not localhost, for local Postgres | Accepted |
| D-007 | 2026-09-15 | Incident/Lesson | Starlette 1.6 test client needs httpx2; filter warnings narrowly | Accepted |
| D-008 | 2026-09-15 | Product | Corrections: subdomain spelling, GitHub account, commit identity | Accepted |
| D-009 | 2026-09-17 | Incident/Lesson | Apply OS security updates when building the runtime image | Accepted |

---

## Template

```markdown
## D-### — Title
- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Superseded by D-### | Reverted
- **Type:** Scope | Architecture | Stack | Infra | Data/Privacy | Product | Monetization | Process | Incident/Lesson
- **Deviates from:** project.md §X (or "original brief")
- **Decided by:** owner / engineering / both

**Context** — What situation forced a choice?
**Options considered** — Each with pros and cons.
**Decision** — What we chose.
**Reasoning** — Why this option, and why not the others.
**Consequences** — What changes; cost; what gets easier or harder.
**Guardrail / lesson** — The rule that prevents repeating the mistake.
**Revisit if** — The concrete trigger that would reopen this.
**Links** — Docs, benchmarks, PRs.
```

---

## D-000 — Baseline plan established
- **Date:** 2026-09-14
- **Status:** Accepted
- **Type:** Process
- **Deviates from:** — (baseline)
- **Decided by:** both

**Context** — Project kickoff. We need a fixed reference point so every later change is visible and justified.

**Decision** — `project.md` v1.0 is the baseline. It covers the stack, architecture, phases, targets, and exit criteria. Baseline technical choices and their "revisit if" triggers are recorded in `project.md` §7 rather than as separate entries. From here on, any deviation from `project.md` gets a D-entry.

**Guardrail / lesson** — No silent plan changes. If code and `project.md` disagree, either the code is wrong or a decision entry is missing.

**Revisit if** — Never superseded; later changes get their own entries.

---

## D-001 — Pivot: no detector evasion → Inspector + Studio
- **Date:** 2026-09-14
- **Status:** Accepted
- **Type:** Scope
- **Deviates from:** Original brief
- **Decided by:** both (engineering declined the original core; owner chose the replacement direction)

**Context** — The original brief: users upload AI-generated images, and the system applies pixel-level optimization so AI detectors can't catch them when posted on social media ("AI-proofing"). It would be monetized with AdSense and collaborators, and released as open source.

**Options considered**

| Option | Pros | Cons |
|---|---|---|
| **A. Build as briefed (evasion engine)** | Clear hook; some demand from creators | Main use at scale is deepfakes, scam listings, fake profiles, and misinformation. AdSense publisher policies prohibit monetizing sites that help users mislead others ("Enabling dishonest behavior"), which puts the only planned revenue at risk. Meta, TikTok, and YouTube require disclosure of realistic AI content, and AI-labeling regulation keeps tightening. Open source defeats itself here: detector vendors train on the outputs, and robust watermarks are designed to survive pixel edits, so the product's promise decays with every detector update. **Engineering declined to build it.** |
| B. Inspector only | Smallest scope, fastest launch | No creator-side utility; weaker retention |
| C. Authenticity toolkit for photographers | Valuable niche; helps real people who get mislabeled | Small audience; C2PA trust-list complexity |
| **D. Inspector + Studio** | Keeps the brief's "check" and "pixel-level high-quality optimization"; broad audience (fact-checkers, journalists, creators); AdSense-friendly; the open-source transparency is an asset, not a liability | Studio must preserve provenance (extra Phase 3 work); marketing hook is "honest" rather than "undetectable" |

**Decision** — Option D. Option C's core value is folded in as Inspector guidance ("What platforms will see").

**Reasoning** — D keeps nearly everything valuable from the brief: the branded web app, detection, pixel-level quality work, open source, and the revenue model. It removes the one element that is harmful, incompatible with the revenue model, and technically self-defeating. Optimization now targets **how an image survives platform recompression**, not whether a detector notices it.

**Consequences**
- Positioning changes to "the honest image tool": *See what's really in your pixels.*
- Studio must carry forward AI disclosure and C2PA provenance, a launch blocker in `project.md` §9.3
- Guardrail CI tests and an import boundary are added (`project.md` §9.4)
- Audience broadens to fact-checkers, journalists, and moderators, which suits AdSense-friendly content

**Guardrail / lesson — the detector test**
> *If a feature's success metric improves when an AI detector, watermark, or disclosure label fails, it is out of scope.*

Permanently out of scope: adversarial perturbations; watermark removal or degradation; stripping C2PA or IPTC AI disclosures; tuning Studio against detector scores; showing detector before/after scores on Studio outputs.
Enforced by: `project.md` §2 (Principle 1), §3 (non-goals), §9.4 (guardrail tests + `studio` → detector import ban), Risk R7.
Note: removing *personal privacy* metadata (GPS, device serials, camera owner name) is unrelated and stays allowed. AI-disclosure fields are always kept.

**Revisit if** — Not reopened for evasion features. Proposals that sit near this line (e.g. "remove the label from my real photo") must quote this entry and pass the detector test. For authentic photos, the path is provenance (Content Credentials), not removal.

---

## D-002 — Hosting on Google Cloud Run with a billing account
- **Date:** 2026-09-14
- **Status:** Accepted
- **Type:** Infra
- **Deviates from:** Original brief ("some free database for hosting"); the $0 target stays, but a payment card is required
- **Decided by:** owner (approved card) + engineering (recommendation)

**Context** — The app runs ML inference (ONNX models) plus image processing, which needs several GB of RAM per instance. Card-free free tiers either lack the memory or add operational complexity.

**Options considered**

| Option | Pros | Cons |
|---|---|---|
| **Google Cloud Run** (billing account) | Scale-to-zero; generous monthly free tier; up to several GiB RAM; plain containers (portable); first-class CI deploys | Requires a card; costs possible if caps aren't set; cold starts |
| Hugging Face Spaces + separate free web host | No card | Two deployments; Spaces sleep when idle; ads and custom domain have to live elsewhere; more moving parts |
| Render / Koyeb free web services | Simple | ~512 MB RAM, too small for models; aggressive sleeping |
| Oracle Cloud Always Free (ARM VM) | Lots of RAM/CPU, always on | Account provisioning is unreliable; we'd own OS patching, TLS, and scaling; ARM builds |
| Google external HTTPS load balancer for custom domain | Clean domain setup | Fixed monthly cost, so not free |

**Decision** — Cloud Run (staging + production services) behind Cloudflare, with Neon Postgres. The custom-domain method is decided by a Phase 0 spike (→ D-003).

**Reasoning** — Cloud Run is the only option that fits the RAM needs, stays at $0 at launch scale, and keeps a single portable container. The card risk is handled with hard caps rather than by avoiding the platform.

**Consequences** — Day-one cost guardrails are mandatory before any public URL: `max-instances=3`, `min-instances=0`, budget alerts at $1/$5/$10, Artifact Registry cleanup policy, Cloudflare rate limiting + Turnstile (`project.md` §11.3). Small incidental costs (e.g. registry storage beyond the free allowance) may reach cents per month.

**Guardrail / lesson** — No GCP resource is created without its cap and budget alert in place. `min-instances > 0` or raising `max-instances` requires a new decision entry.

**Revisit if** — Monthly bill > $10 without matching revenue; Cloud Run free-tier terms change; sustained traffic makes an always-on host cheaper.

---

## D-003 — Owner confirmations: name, subdomain, license, GitHub account
- **Date:** 2026-09-15
- **Status:** Accepted; production URL and GitHub account rows superseded by D-008
- **Type:** Product
- **Deviates from:** `project.md` v1.0 placeholders and proposed defaults (agent.md Q1–Q8)
- **Decided by:** owner ("go with your recommendations" for everything not answered explicitly)

**Context** — Repo creation and DNS work in Phase 0 needed these answers.

**Decision**

| Topic | Decision | Notes |
|---|---|---|
| Product name | **Picxel** (kept) | Trademark/handle checks still happen in the brand sprint |
| Production URL | **https://pixcel.autolinium.com** | Staging: `pixcel-staging.autolinium.com` (first-level subdomain for Cloudflare Universal SSL). The subdomain is spelled differently from the product name; owner is confirming (agent.md Q9) |
| License | **AGPL-3.0-or-later** for code, CC BY 4.0 for docs | Proposed → accepted |
| GitHub | **Personal account** `autolinium-glitch`, repo `picxel` | Deviates from the "company org" default |
| Weekly time, brand, team (Q5, Q6, Q8) | Defaults: ~20 h/week, standalone sub-brand, owner + Claude | Adopted per owner instruction |

**Consequences** — GitHub Sponsors works on personal accounts. Moving to an organization later is a supported repository transfer (old URLs redirect), but CODEOWNERS, badges, and CI/CD secrets must be updated at that point. AdSense and `ads.txt` sit at the `autolinium.com` root, so whoever manages that domain becomes a Phase 4 dependency.

**Guardrail / lesson** — The public URL is one setting (`PICXEL_PUBLIC_URL`). Application code never hard-codes the domain; only docs and project metadata mention it.

**Revisit if** — The company creates a GitHub organization, or the subdomain spelling changes (Q9).

---

## D-004 — Dockerfile and compose.yaml at the repository root
- **Date:** 2026-09-15
- **Status:** Accepted
- **Type:** Architecture
- **Deviates from:** `project.md` §17 (planned under `infra/`)
- **Decided by:** engineering

**Context** — Standard tooling expects these files at the root: `docker compose up`, `docker build .`, Dependabot's Docker ecosystem at `/`, and Cloud Run source deploys.

**Options considered** — (a) `infra/` as planned: every command needs `-f` flags and a longer README. (b) Root: default commands just work.

**Decision** — `Dockerfile`, `.dockerignore`, and `compose.yaml` live at the root. `infra/` keeps deployment config, Postgres init scripts, and runbooks.

**Consequences** — `project.md` §17 updated (v1.1).

**Guardrail / lesson** — Every command in the README must run from the repository root with no extra flags. That is part of the "running locally in < 10 minutes" promise.

**Revisit if** — We need several images (e.g. a separate inference service). Then move them to `infra/docker/` with a documented bake file.

---

## D-005 — Synchronous SQLAlchemy with psycopg 3 (not async)
- **Date:** 2026-09-15
- **Status:** Accepted
- **Type:** Stack
- **Deviates from:** `project.md` §7 left sync vs. async open; async is the usual FastAPI default
- **Decided by:** engineering

**Context** — FastAPI is async, so async SQLAlchemy is the obvious pick. But the owner develops on Windows, where psycopg 3's async mode can't run on the default event loop. Alembic migrations also need a driver.

**Options considered**

| Option | Pros | Cons |
|---|---|---|
| Async SQLAlchemy + psycopg 3 | One driver, async end to end | Fails on Windows' default event loop → breaks local dev and tests for the owner |
| Async SQLAlchemy + asyncpg, psycopg for Alembic | Works on Windows | Two drivers; separate URL and SSL handling; prepared-statement settings for Neon's pooler |
| **Sync SQLAlchemy + psycopg 3** | One driver for app and Alembic; works on every OS; simplest to debug | Blocking calls must stay off the event loop |

**Decision** — Sync engine with psycopg 3. Endpoints that touch the database are plain `def`, so FastAPI runs them in its threadpool. The engine uses `pool_pre_ping` (Neon scales to zero) and `prepare_threshold=None` (Neon's PgBouncer pooler).

**Reasoning** — Picxel's database work is tiny: one row per analysis, plus feedback and rollups. Image processing, not the database, dominates latency, so async buys nothing measurable and costs portability.

**Consequences** — A sync database call inside an `async def` endpoint would block the event loop, so reviews must check for it.

**Guardrail / lesson** — Database access happens only in sync (`def`) endpoints or through `run_in_threadpool`, never directly inside `async def`.

**Revisit if** — Database time shows up in p95 latency profiles, or a high-concurrency, database-heavy feature arrives (e.g. the public API).

---

## D-006 — Lesson: use 127.0.0.1, not localhost, for local Postgres
- **Date:** 2026-09-15
- **Status:** Accepted
- **Type:** Incident/Lesson
- **Deviates from:** — (local development setup)
- **Decided by:** engineering

**Context** — The two database tests took **266 s** with `postgresql://…@localhost:5432/…` on the owner's Windows machine. The same tests with `127.0.0.1` took **0.5 s** (measured back to back).

**Likely cause** — `compose.yaml` publishes Postgres on `127.0.0.1` only. On Windows, `localhost` resolves to IPv6 `::1` first, and each new connection waits for that attempt to fail before falling back to IPv4. Only the timing difference was verified; the mechanism is inferred.

**Decision** — All local and CI connection strings use `127.0.0.1` (`.env.example`, CI workflow).

**Guardrail / lesson** — Never write `localhost` in database URLs in docs, examples, or CI. If local database work is slow, check the host before anything else.

**Revisit if** — Compose publishes on both IPv4 and IPv6.

---

## D-007 — Lesson: Starlette 1.6 test client needs httpx2; filter warnings narrowly
- **Date:** 2026-09-15
- **Status:** Accepted
- **Type:** Incident/Lesson
- **Deviates from:** — (tooling)
- **Decided by:** engineering

**Context** — pytest runs with `filterwarnings = error`, so deprecations fail the suite. Two surfaced on first run. Starlette 1.6's `TestClient` warns when plain `httpx` is installed ("install `httpx2` instead"). Starlette's own code also touches a deprecated `anyio.abc.BlockingPortal` alias.

**Options considered** — (a) Drop `filterwarnings = error`: hides future breakage. (b) Blanket-ignore `DeprecationWarning`: same problem, quieter. (c) **Fix what we own, filter only what we don't.**

**Decision** — Replace the `httpx` dev dependency with `httpx2`. Add one message-specific ignore for the anyio alias in `pyproject.toml`, with a removal note.

**Guardrail / lesson** — Keep `filterwarnings = error`. A third-party warning gets a targeted, commented ignore, never a blanket one. Re-check the ignore list on every Starlette or anyio upgrade (Dependabot PRs).

**Revisit if** — A Starlette release stops using the deprecated alias. Then delete the ignore.

---

## D-008 — Corrections: subdomain spelling, GitHub account, commit identity
- **Date:** 2026-09-15
- **Status:** Accepted
- **Type:** Product
- **Deviates from:** D-003 (production URL and GitHub account rows)
- **Decided by:** owner

**Context** — Owner answers to agent.md Q9–Q11.

**Decision**

| Topic | Decision | Notes |
|---|---|---|
| Production URL | **https://picxel.autolinium.com**, matching the product name | Staging: `picxel-staging.autolinium.com`. Supersedes D-003's `pixcel` spelling |
| GitHub account | **`billu07`** | Supersedes `autolinium-glitch`. Repository URL is provisionally `https://github.com/billu07/picxel` until the owner shares the link |
| Commit identity | Repo-local git config: `billu07 <billahmasum602@gmail.com>` | Visible in public commit history; the global git config is untouched |
| Code of Conduct contact | **Pending.** Owner is setting up a mailbox | `CODE_OF_CONDUCT.md` keeps its placeholder until then |

**Consequences** — Updated `app/core/meta.py` (`REPOSITORY_URL`), `pyproject.toml` URLs, `CODEOWNERS`, issue-template config, `SECURITY.md`, tests, `project.md`, `agent.md`. The local `gh` CLI is signed in as `autolinium-glitch` only. Pushing to `billu07`'s repository needs that account signed in (`gh auth login`) or collaborator access.

**Guardrail / lesson** — Read domain names and account names back to the owner, letter by letter, before they spread into files. A one-letter swap here touched 9 files. In code, the repository URL lives in one constant (`app.core.meta.REPOSITORY_URL`) and the public URL in one setting (`PICXEL_PUBLIC_URL`).

**Revisit if** — The repository link the owner shares isn't `billu07/picxel`.

*Update 2026-09-17:* the owner shared `https://github.com/Billu07/Picxel`. Files now use that exact spelling.

---

## D-009 — Apply OS security updates when building the runtime image
- **Date:** 2026-09-17
- **Status:** Accepted
- **Type:** Incident/Lesson
- **Deviates from:** — (build policy, discovered by CI)
- **Decided by:** engineering

**Context** — The first CI run on GitHub failed its Trivy scan with 6 fixable HIGH findings, all from packages inherited from `python:3.12-slim`: `gzip` (CVE-2026-41992), `libpcre2-8-0` (CVE-2026-86145, CVE-2026-89157, CVE-2026-89161) and `libsqlite3-0` (CVE-2026-11822, CVE-2026-11824). Published base images lag behind Debian's security archive between rebuilds. Everything else in that run passed, including the container build and smoke test.

**Options considered**

| Option | Verdict |
|---|---|
| Lower the Trivy threshold, or stop failing the build | Rejected: the gate exists to catch exactly this |
| Ignore these specific CVEs | Rejected: fixes were available; the list would grow every month |
| **Upgrade installed packages in the runtime stage at build time** | Chosen |
| Pin the base image by digest | Rejected for now: it freezes security fixes. Dependabot tracks the tag instead |

**Decision** — The runtime stage runs `apt-get upgrade` before installing ExifTool, so every image build picks up current Debian security fixes.

**Consequences** — Builds are slightly less reproducible: the same Dockerfile produces different package versions over time. That is the intended trade-off for a public web service. A rebuild is now also the fix for OS-level CVEs, and Trivy keeps failing CI when fixable HIGH/CRITICAL findings remain.

**Guardrail / lesson** — Never widen the vulnerability gate to make a build pass. Fix the image, or record a specific, time-boxed exception with a reason. Run a container scan locally before pushing image changes.

**Revisit if** — Base-image rebuilds become frequent enough that the upgrade is a no-op, or a reproducible-build requirement arrives (then pin by digest and rebuild on a schedule).
