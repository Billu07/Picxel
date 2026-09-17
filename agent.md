# agent.md — Project RAM

> **Read this first every session. Update it last every session.**
> Reading order: `agent.md` (where are we) → current phase in `project.md` (what & why) → latest `decision.md` entries (what changed).

| | |
|---|---|
| **Last updated** | 2026-09-17 |
| **Plan version** | `project.md` v1.1 |
| **Current phase** | Phase 0 — Foundations (steps 1–8 of 15 done) |
| **Repository** | https://github.com/Billu07/Picxel — public, CI green on `main` |
| **Overall health** | 🟢 On track. Code is live and verified; cloud setup waits on owner accounts |

---

## Status at a glance

| Phase | Name | Status | Progress |
|---|---|---|---|
| — | Planning | ✅ Done | 100% |
| 0 | Foundations | 🔨 In progress | ~55% (8 of 15 steps) |
| 1 | Detection R&D | ⬜ Not started | — |
| 2 | Inspector MVP & public beta | ⬜ Not started | — |
| 3 | Studio | ⬜ Not started | — |
| 4 | Content, SEO & AdSense | ⬜ Not started | — |
| 5 | Community & collaborators | ⬜ Not started | — |
| 6 | Growth & hardening | ⬜ Backlog | — |

---

## Where we are now
The foundation is published and CI is green. `main` has two commits:
- `672c14c` — Phase 0 scaffold (81 files)
- `b744b8c` — Debian security updates in the runtime image (D-009)

CI run `35192175538` passed all four jobs: lint/types/contracts, tests against PostgreSQL, dependency audit, and container build + smoke test + Trivy scan.

Local verification (2026-09-15 to 2026-09-17): `uv run picxel check` green · 38 tests, coverage 92.5% · image builds and serves · `docker compose run --rm migrate` applies revision `0001` · all pre-commit hooks pass.

---

## Done
- **2026-09-17** — Repository published at `Billu07/Picxel`; first CI run surfaced 6 fixable HIGH CVEs in the base image; fixed and re-pushed; **CI green** (D-009)
- **2026-09-15** — Corrections: subdomain `picxel.autolinium.com`, GitHub `Billu07`, repo-local commit identity (D-008)
- **2026-09-15** — Owner confirmations: name Picxel, AGPL-3.0, defaults for the rest (D-003)
- **2026-09-15** — Step 1: git repo; AGPL-3.0 `LICENSE`; README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, GOVERNANCE; issue/PR templates; CODEOWNERS; Dependabot
- **2026-09-15** — Step 2: uv project (Python 3.12), ruff, mypy strict, import contracts (incl. the D-001 Studio guardrail), pytest + 80% coverage gate, pre-commit
- **2026-09-15** — Step 3: FastAPI app factory; health, readiness, version endpoints; RFC 9457 errors; request IDs + JSON access logs; CSP nonce + security headers
- **2026-09-15** — Step 4: Jinja2 layout, header/footer, logo mark, favicon, home + branded error pages; light/dark tokens; Tailwind v4.3.3 standalone build
- **2026-09-15** — Step 5: 3-stage Dockerfile (non-root, ExifTool) + `compose.yaml` at repo root (D-004)
- **2026-09-15** — Step 6: SQLAlchemy 2 (sync) + psycopg 3 + Alembic baseline `0001` (D-005)
- **2026-09-15** — Step 7: GitHub Actions CI; actions pinned by commit SHA
- **2026-09-15** — Lessons logged: `127.0.0.1` over `localhost` (D-006); `httpx2` + narrow warning filters (D-007)
- **2026-09-14** — Planning docs; D-000, D-001, D-002

---

## Now — Phase 0 (remaining)

### Owner actions (only you can do these)
- [ ] **Repo settings** at github.com/Billu07/Picxel → Settings (the CLI here is read-only, see Environment):
  - [ ] Security → enable **private vulnerability reporting** (`SECURITY.md` points people to it)
  - [ ] Rules/Branches → protect `main`: require a pull request, require CI checks to pass
- [ ] Set up the Code of Conduct contact mailbox (Q11)
- [ ] Create Google Cloud account + billing account (card); project `picxel`
- [ ] Create Neon account
- [ ] Confirm who manages DNS for `autolinium.com` and whether it's on Cloudflare (Q1b)
- [ ] Create Sentry account
- [ ] Optional: review Dependabot pull requests as they appear

### Engineering sequence (in order)
9. [ ] GCP: Artifact Registry + cleanup policy, Cloud Run staging/prod with caps, budget alerts *(needs GCP account)*
10. [ ] Neon `main` + `staging` branches wired through secrets *(needs Neon account)*
11. [ ] Custom-domain spike (`project.md` §11.2, options A/B/C) → log as D-010
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
| **Q11** | Code of Conduct contact email (owner is setting one up). `CODE_OF_CONDUCT.md` still has `[INSERT CONTACT METHOD]` | Announcing the repo publicly | Placeholder stays |
| Q1b | Who manages DNS for `autolinium.com`, and is it on Cloudflare? (AdSense + `ads.txt` live at the root) | Steps 11–12, Phase 4 | — |
| Q7 | Your legal jurisdiction (legal pages, consent, reporting duties)? | Phase 2 legal pages | — |

Resolved: Q1 + Q9 subdomain `picxel.autolinium.com` · Q2 keep name · Q3 AGPL-3.0 · Q4 + Q10 GitHub `Billu07` · Q5 20 h/week · Q6 standalone sub-brand · Q8 owner + Claude · Q12 repo link (D-003, D-008).
Note: commits carry `billahmasum602@gmail.com`, now public in the repo history. Switching to a GitHub `noreply` address later would only apply to new commits.

---

## Blockers
- Repo settings (vulnerability reporting, branch protection) need the owner or a CLI login as `Billu07`.
- Owner cloud accounts block steps 9–13.

---

## Environment state

| Item | State |
|---|---|
| Local folder | `D:\Autolinium V2\Projects\Picxel`: `main` tracking `origin/main`; identity `billu07 <billahmasum602@gmail.com>` (repo-local) |
| GitHub | `Billu07/Picxel`, public, CI green. Local `gh` CLI is signed in as `autolinium-glitch` → **read-only** on this repo; `git push` works through Git Credential Manager |
| Tooling | uv 0.12.13 (`~/.local/bin`), Python 3.12.14 managed by uv; `.venv` synced |
| Docker | Docker Desktop 29.6.2; its engine crashed once during a local Trivy scan and was restarted. Images `picxel:local`, `picxel-migrate`; volume `picxel_pgdata` (db stopped) |
| GCP / Neon / Cloudflare / Sentry | Not created |
| Domain | `picxel.autolinium.com` (staging `picxel-staging.autolinium.com`); DNS not configured |
| Secrets | None. **Never commit secrets.** GitHub Environments + GCP Secret Manager only |

---

## Quick reference
- **Run:** `uv run picxel dev` → http://127.0.0.1:8000
- **All checks:** `uv run picxel check`
- **With Postgres:** `docker compose up db`, then `PICXEL_TEST_DATABASE_URL=postgresql://picxel:picxel@127.0.0.1:5432/picxel_test`
- **Full stack in Docker:** `docker compose up --build` → http://localhost:8000
- **Single sources of truth:** public URL = `PICXEL_PUBLIC_URL`; repo URL = `app/core/meta.py` `REPOSITORY_URL` (+ `pyproject.toml`, `CODEOWNERS`, issue-template config)
- **Pins to keep in sync:** Tailwind `v4.3.3` (`app/cli.py`); uv image `0.12.13` (`Dockerfile`); GitHub Actions by SHA (Dependabot updates them)
- **Gotchas:** use `127.0.0.1`, never `localhost` (D-006) · TestClient needs `httpx2` (D-007) · a shell without a terminal can't prompt for git credentials: push with `GCM_GUI_PROMPT=1` and `credential.guiPrompt=true` so the credential window appears · uv's "failed to hardlink" warning on the D: drive is harmless

## Key numbers
- Upload limits: **20 MB**, **50 MP**, 30 s timeout
- Latency: inspect p95 **≤ 5 s** warm · export p95 **≤ 4 s** · cold start ≤ 15 s
- Detector gate: real-photo FPR **≤ 2%** at `T_high`; ECE ≤ 0.05
- Cloud Run caps: min **0**, max **3** instances; budget alerts $1 / $5 / $10
- Current: coverage 92.5% (gate 80%) · CI ~1 min · CSS 12.6 KB

---

## Session log (newest first)

### 2026-09-17 — Session 3: Published the repository, CI green
- **Did:** Corrected the repo URL casing to `Billu07/Picxel`. Committed the Phase 0 scaffold (`672c14c`, 81 files) and pushed to GitHub. First CI run failed only on the Trivy image scan (6 fixable HIGH CVEs in base-image packages); added Debian security updates to the runtime stage and pushed `b744b8c`; CI now green. Logged D-009.
- **Notes:** The `gh` CLI can't change repo settings (read-only account), so branch protection and private vulnerability reporting are owner tasks. Docker Desktop's engine crashed mid-scan and was restarted.
- **Next session starts with:** owner's cloud accounts → step 9 (GCP: Artifact Registry, Cloud Run services with caps, budget alerts), then Neon and the domain spike (D-010).

### 2026-09-15 — Session 2: Phase 0 local foundation
- **Did:** Built Phase 0 steps 1–7: community files, tooling, FastAPI skeleton with security baseline, branded placeholder pages + design tokens, Tailwind build, database layer + Alembic, Dockerfile + compose, CI workflow. Verified with `picxel check`, real-Postgres tests, container build + smoke test, compose migration, pre-commit. Updated `project.md` to v1.1.
- **Decided:** D-003, D-004, D-005, D-006, D-007, D-008.

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
