---
title: Add a single 'make validate' target for the full local check suite
status: completed
created: 2026-08-13
updated: 2026-08-13
issue: #43
---

# Add a single 'make validate' target for the full local check suite

## Objective

Add one `make validate` target that runs the full local check suite (lint, format-check, typecheck, test) in one command, and have `.githooks/pre-commit` call it — so there's a single, reusable entry point instead of chaining individual `make` targets by hand or letting the hook and a manual pre-push check drift apart.

## Context

`development-standards.md` §3 calls for "un script de validación único y reutilizable (`scripts/validate.sh` o `make validate`)... invocado tanto por los git hooks como manualmente antes de un push." Today the repo has the individual pieces (`make lint`, `make format-check`, `make typecheck`, `make test`) and `.github/workflows/ci.yml` runs them as separate jobs, but nothing local aggregates them. `.githooks/pre-commit` currently calls `make lint` and `make format-check` directly (plus a `docker run` for gitleaks) — it doesn't run `typecheck` or `test` at all, so a commit can pass the hook and still fail CI on those two checks. A single `make validate` target closes that gap and gives contributors one command to run before pushing.

## Requirements

### Functional Requirements

- [ ] New `validate` target in `Makefile`: runs `lint`, `format-check`, `typecheck`, `test` in that order
- [ ] Fails fast — if any step fails, `make validate` exits non-zero without necessarily running the remaining steps (native `make` prerequisite behavior: `validate: lint format-check typecheck test` already stops at the first failing prerequisite)
- [ ] `validate` target documented with a `##` comment so it shows up in `make help`
- [ ] `.githooks/pre-commit` calls `make validate` instead of `make lint` + `make format-check` separately
- [ ] gitleaks step in `.githooks/pre-commit` stays as its own step, unchanged — it's a secret scan, not a code-quality check, and doesn't have a `make` target today

### Non-Functional Requirements

- [ ] No change in behavior for CI (`ci.yml` keeps calling the individual targets per job, unchanged) — this is a local-DX addition, not a CI refactor
- [ ] `make validate` must be runnable standalone (`docker compose up -d --wait` dependency already satisfied transitively via each prerequisite target's own `up-d` dependency)

## Architecture

### Components

- `Makefile`: new `validate` target (composed of existing targets as prerequisites, no new logic)
- `.githooks/pre-commit`: updated to call `make validate`

### Data Model

N/A

### External Dependencies

None — reuses existing `lint`, `format-check`, `typecheck`, `test` targets.

## User Stories

See GitHub issue #43 for the full user story and Gherkin acceptance criteria (`gh issue view 43`).

## Testing Strategy

### Unit Tests
N/A — build tooling change, not application code.

### Integration Tests
N/A

### E2E Tests
N/A

### Performance Tests
N/A

**Verification**: run `make validate` locally and confirm it executes lint → format-check → typecheck → test in order; deliberately break one (e.g. a lint violation) and confirm `make validate` stops and exits non-zero; commit a change and confirm the pre-commit hook now runs the full suite via `make validate` instead of just lint/format.

## Boundaries & Constraints

### In Scope
- `validate` target in `Makefile`
- `.githooks/pre-commit` updated to use it

### Out of Scope
- Changing `ci.yml` to call `make validate` instead of individual jobs — CI's per-job parallelism is intentional (§4 of the standard: "jobs independientes y paralelos... facilita ver de un vistazo qué falló"); collapsing them into one sequential `validate` call would lose that
- Adding gitleaks as a `make` target — out of scope for this issue, the hook already invokes it directly via `docker run`
- Graduated validation depth by branch (lightweight on commit, full on push/merge) — noted as a separate, larger behavior change in the standard; not part of this issue

### Technical Constraints
- Must work the same way the existing targets do (Docker-first, via `docker compose exec`) — no new tooling introduced

## Success Criteria

- [ ] `make validate` exists, runs lint + format-check + typecheck + test in order, documented in `make help`
- [ ] `.githooks/pre-commit` calls `make validate` (gitleaks step unchanged)
- [ ] A deliberately introduced lint error causes `make validate` to fail before reaching `test`
- [ ] `git commit` with the updated hook installed runs the full suite, not just lint/format

## Implementation Plan

Small enough (Effort: XS per issue #43) to skip a separate `-plan.md` and go straight to a single-task implementation once this spec is approved.
