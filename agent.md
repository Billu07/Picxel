# agent.md — Project RAM

> **Read this first every session. Update it last every session.**
> Reading order: `agent.md` (where are we) → current phase in `project.md` (what & why) → latest `decision.md` entries (what changed).

| | |
|---|---|
| **Last updated** | 2026-09-15 |
| **Plan version** | `project.md` v1.1 |
| **Current phase** | Phase 0 — Foundations (in progress: steps 1–7 of 15 done) |
| **Overall health** | 🟢 On track. Local foundation verified; waiting on the repo link, then cloud accounts |

---

## Status at a glance

| Phase | Name | Status | Progress |
|---|---|---|---|
| — | Planning | ✅ Done | 100% |
| 0 | Foundations | 🔨 In progress | ~45% (7 of 15 steps) |
| 1 | Detection R&D | ⬜ Not started | — |
| 2 | Inspector MVP & public beta | ⬜ Not started | — |
| 3 | Studio | ⬜ Not started | — |
| 4 | Content, SEO & AdSense | ⬜ Not started | — |
| 5 | Community & collaborators | ⬜ Not started | — |
| 6 | Growth & hardening | ⬜ Backlog | — |

---

## Where we are now
The local foundation is built and verified: app skeleton, branded placeholder pages, security baseline, database + migrations, container, compose stack, CI workflow, and community files.
**Nothing is committed or pushed yet.** Next step: the owner shares the GitHub repository link, and the push account (`billu07`) is signed in.

Verified on 2026-09-15:
- `uv run picxel check` passes: ruff, ruff format, mypy (strict), import contracts (2 kept), pytest
- 38 tests pass (36 app + 2 against real PostgreSQL 17); coverage **92.5%** (gate: 80%)
- Container image builds (419 MB), runs as non-root `picxel`, ExifTool 13.25 present
- Container smoke test: `/api/v1/health`, `/api/v1/version`, `/`, `/static/css/app.css`, API 404 problem+json all correct
- `docker compose run --rm migrate` applies revision `0001`
- All pre-commit hooks pass
- ⚠️ CI workflow is written but **has never run on GitHub**. Expect small fixes on the first run.

---

## Done
- **2026-09-15** — Corrections: subdomain `picxel.autolinium.com`, GitHub account `billu07`, repo-local commit identity `billu07 <billahmasum602@gmail.com>` (D-008)
- **2026-09-15** — Owner confirmations: name Picxel, AGPL-3.0, defaults for the rest (D-003)
- **2026-09-15** — Step 1: git repo (`main`); official AGPL-3.0 `LICENSE`; README, CONTRIBUTING, CODE_OF_CONDUCT (Contributor Covenant 2.1), SECURITY, GOVERNANCE; issue/PR templates; CODEOWNERS; Dependabot
- **2026-09-15** — Step 2: uv project (Python 3.12), ruff, mypy strict, import-linter contracts (incl. the D-001 Studio guardrail), pytest + 80% coverage gate, pre-commit
- **2026-09-15** — Step 3: FastAPI app factory; `/api/v1/health`, `/api/v1/health/ready`, `/api/v1/version`; RFC 9457 errors; request IDs + JSON access logs; CSP nonce + security headers; HSTS on deployed envs
- **2026-09-15** — Step 4: Jinja2 layout, header/footer, logo mark, favicon, home + branded error pages; light/dark design tokens; Tailwind v4.3.3 standalone build (no Node)
- **2026-09-15** — Step 5: 3-stage Dockerfile (non-root, ExifTool) + `compose.yaml` (db, migrate, app) at repo root (D-004)
- **2026-09-15** — Step 6: SQLAlchemy 2 (sync) + psycopg 3 + Alembic baseline `0001` (D-005)
- **2026-09-15** — Step 7: GitHub Actions CI with lint/types/contracts, tests with a Postgres service, pip-audit, container build + smoke test + Trivy scan; actions pinned by commit SHA
- **2026-09-15** — Lessons logged: `127.0.0.1` over `localhost` (D-006); `httpx2` + narrow warning filters (D-007)
- **2026-09-14** — Planning docs; D-000, D-001, D-002

---

## Now — Phase 0 (remaining)

### Owner actions (only you can do these)
- [ ] Share the GitHub repository link (provisionally assumed `https://github.com/billu07/picxel`)
- [ ] Sign in to `billu07` for pushing: type `! gh auth login` in this session. Alternatively, add `autolinium-glitch` as a collaborator on the repo
- [ ] Set up the Code of Conduct contact mailbox (Q11)
- [ ] Create Google Cloud account + billing account (card); project `picxel`
- [ ] Create Neon account
- [ ] Confirm who manages DNS for `autolinium.com` and whether it's on Cloudflare (Q1b)
- [ ] Create Sentry account

### Engineering sequence (in order)
8. [ ] Initial commit, push, first green CI run, then private vulnerability reporting + branch protection *(needs repo link + push access; owner says "commit and publish")*
9. [ ] GCP: Artifact Registry + cleanup policy, Cloud Run staging/prod with caps, budget alerts *(needs GCP account)*
10. [ ] Neon `main` + `staging` branches wired through secrets *(needs Neon account)*
11. [ ] Custom-domain spike (`project.md` §11.2, options A/B/C) → log as next decision ID (D-009)
12. [ ] Cloudflare: DNS for `picxel.autolinium.com` + `picxel-staging.autolinium.com`, SSL Full (strict), rate-limit rule, Turnstile keys, Access on staging *(needs Q1b)*
13. [ ] CD: deploy staging on merge to `main`, production on tag with approval
14. [ ] Brand sprint v0: self-hosted Inter + JetBrains Mono, logo refinement, name availability checks
15. [ ] Competitive teardown (≥ 5 detector sites + Content Credentials verify)

**Phase 0 exit criteria:** `project.md` §18 → Phase 0.

---

## Next up (after Phase 0)
- Phase 1 kickoff: `eval/` harness skeleton + license register template (can start during late Phase 0)
- Shortlist detector backbones (DINOv2, SigLIP 2, OpenCLIP) and check licenses and model cards
- Outline the Learn hub (AdSense needs content lead time)

---

## Open questions (owner input needed)

| # | Question | Blocks | Default if unanswered |
|---|---|---|---|
| **Q12** | GitHub repository link (repo name under `billu07`)? | Step 8 | `billu07/picxel` |
| **Q11** | Code of Conduct contact email (owner is setting one up). `CODE_OF_CONDUCT.md` still has `[INSERT CONTACT METHOD]` | Announcing the repo publicly | Placeholder stays until provided |
| Q13 | Keep `billahmasum602@gmail.com` visible in public commit history, or use GitHub's private `noreply` address for commits? | First commit | Use the email as given |
| Q1b | Who manages DNS for `autolinium.com`, and is it on Cloudflare? (AdSense + `ads.txt` live at the root) | Step 12, Phase 4 | — |
| Q7 | Your legal jurisdiction (legal pages, consent, reporting duties)? | Phase 2 legal pages | — |

Resolved: Q1 subdomain + Q9 spelling → `picxel.autolinium.com` · Q2 keep name · Q3 AGPL-3.0 · Q4 + Q10 GitHub/commit identity `billu07` · Q5 20 h/week · Q6 standalone sub-brand · Q8 owner + Claude (D-003, D-008).

---

## Blockers
- **Repo link + push access** (`gh` is signed in as `autolinium-glitch` only) block step 8.
- Owner cloud accounts block steps 9–13.

---

## Environment state

| Item | State |
|---|---|
| Local folder | `D:\Autolinium V2\Projects\Picxel`: git repo on `main`, **no commits yet**; repo-local identity `billu07 <billahmasum602@gmail.com>` |
| Tooling | uv 0.12.13 (`~/.local/bin`), Python 3.12.14 managed by uv; `.venv` synced |
| Docker | Docker Desktop 29.6.2. Images `picxel:local`, `picxel-migrate`; volume `picxel_pgdata` (db container stopped) |
| GitHub | Owner account `billu07`; repo link pending. Local `gh` CLI signed in as `autolinium-glitch` |
| GCP / Neon / Cloudflare / Sentry | Not created |
| Domain | `picxel.autolinium.com` (staging `picxel-staging.autolinium.com`); DNS not configured |
| Secrets | None. **Never commit secrets.** GitHub Environments + GCP Secret Manager only |

---

## Quick reference
- **Run:** `uv run picxel dev` → http://127.0.0.1:8000
- **All checks:** `uv run picxel check`
- **With Postgres:** `docker compose up db`, then set `PICXEL_TEST_DATABASE_URL=postgresql://picxel:picxel@127.0.0.1:5432/picxel_test`
- **Full stack in Docker:** `docker compose up --build` → http://localhost:8000
- **Single sources of truth:** public URL = `PICXEL_PUBLIC_URL`; repo URL = `app/core/meta.py` `REPOSITORY_URL` (+ `pyproject.toml`, `CODEOWNERS`, issue-template config)
- **Pins to keep in sync:** Tailwind `v4.3.3` (`app/cli.py`); uv image `0.12.13` (`Dockerfile`); GitHub Actions by SHA (Dependabot updates them)
- **Gotchas:** use `127.0.0.1`, never `localhost` (D-006) · TestClient needs `httpx2` (D-007) · uv's "failed to hardlink" warning on the D: drive is harmless (set `UV_LINK_MODE=copy` to silence it)

## Key numbers
- Upload limits: **20 MB**, **50 MP**, 30 s timeout
- Latency: inspect p95 **≤ 5 s** warm · export p95 **≤ 4 s** · cold start ≤ 15 s
- Detector gate: real-photo FPR **≤ 2%** at `T_high`; ECE ≤ 0.05
- Cloud Run caps: min **0**, max **3** instances; budget alerts $1 / $5 / $10
- Current: coverage 92.5% (gate 80%) · image 419 MB · CSS 12.6 KB

---

## Session log (newest first)

### 2026-09-15 — Session 2: Phase 0 local foundation
- **Did:** Recorded owner answers. Installed uv and Python 3.12. Built Phase 0 steps 1–7: community files, tooling, FastAPI skeleton with security baseline, branded placeholder pages + design tokens, Tailwind build, database layer + Alembic, Dockerfile + compose, CI workflow. Verified with `picxel check`, real-Postgres tests, container build + smoke test, compose migration, and pre-commit. Updated `project.md` to v1.1. Then applied owner corrections: `picxel.autolinium.com`, GitHub `billu07`, repo-local commit identity.
- **Decided:** D-003 (owner confirmations), D-004 (Docker files at root), D-005 (sync DB driver), D-006 (127.0.0.1 lesson), D-007 (httpx2 + narrow warning filters), D-008 (corrections).
- **Next session starts with:** owner shares repo link and signs in `billu07` → step 8 (initial commit, push, first CI run, fix anything CI surfaces) → cloud steps once accounts exist.

### 2026-09-14 — Session 1: Kickoff & planning
- **Did:** Reviewed the brief. Declined the detector-evasion core; owner chose Inspector + Studio. Owner approved a GCP billing account. Wrote `project.md` v1.0, `agent.md`, `decision.md`.
- **Decided:** D-001 (scope pivot), D-002 (Cloud Run with billing account).

---

## Update protocol (end of every session)
1. Move finished items to **Done** with the date.
2. Refresh **Now**, **Next up**, **Open questions**, **Blockers**, **Environment state**, and the status table.
3. Add a **Session log** entry: did / decided / next session starts with.
4. If anything deviated from `project.md`: write the `decision.md` entry **first**, then update `project.md`, then reference the D-ID here.
5. Keep this file lean (≤ ~200 lines). When the session log passes ~10 entries, move older entries to `docs/history/sessions.md`.
