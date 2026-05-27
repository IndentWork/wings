# CI/CD Pipeline Architecture

This document describes the planned CI/CD pipeline for Wings. It is a living document — steps and tooling will evolve as implementation progresses.

---

## Overview

The pipeline is split into four stages — **Bootstrap**, **Validate**, **Build**, and **Deploy** — each as a separate GitHub Actions workflow file. They run in sequence, with each workflow triggering the next via `workflow_run` on success.

```
bootstrap.yml → validate.yml → build.yml → deploy.yml
                                              └── Deploy Dev  (plan → apply)
                                              └── Deploy QA   (plan → apply)
                                              └── Deploy Prod (plan → apply)

destroy.yml  (manual trigger only)
  └── Destroy Dev
  └── Destroy QA
  └── Destroy Prod
  (bootstrap resources are NOT destroyed)
```

**On PRs:** only `validate.yml` runs — no infra, no packaging.
**On push to main:** full chain runs — bootstrap → validate → build → deploy.

---

## Stages

### 1. Bootstrap (`bootstrap.yml`)
**Status: Done**

Provisions shared Azure infrastructure. Idempotent — safe to run on every push.

- Azure Login (Service Principal via `creds` JSON)
- Ensure Resource Group exists (`rg-wings-bootstrap`)
- Ensure ACR exists (`acrwings01`)

Triggers on: `push` to `main`, `workflow_dispatch`

---

### 2. Validate (`validate.yml`)
**Status: Done**

Validates code quality. Runs on every PR and on push to main.

Jobs (in sequence):
1. **Lint** — black, isort, flake8
2. **Test** — pytest-django

Triggers on: `pull_request` to `main`, `push` to `main`

---

### 3. Build (`build.yml`)
**Status: In progress** (scaffolded; version bump, Docker build, ACR push pending)

Runs only when Validate passes on main. Versions the app, packages it as a Docker image, and pushes to ACR.

Jobs (in sequence):
1. **Version** — bump version in `pyproject.toml` based on branch prefix, update `CHANGELOG.md`, commit and tag
   - `feat/` → minor bump (0.1.0 → 0.2.0)
   - `fix/` or `hotfix/` → patch bump (0.1.0 → 0.1.1)
2. **Package** — Docker image build, tagged with new version
3. **Push to ACR** — push versioned image to `acrwings01`

Triggers on: `workflow_run` → Validate completed successfully on `main`

> Open: Docker build context, image naming convention, versioning script implementation

---

### 4. Deploy (`deploy.yml`)
**Status: Not started**

Single workflow with three environment jobs chained in sequence via `needs`.

Jobs (in order):
1. **Deploy Dev** — plan → apply
2. **Deploy QA** — plan → apply (manual approval gate TBD) — `needs: deploy-dev`
3. **Deploy Prod** — plan → apply (manual approval required) — `needs: deploy-qa`

Triggers on: `workflow_run` → Build completed successfully

> Open: Deployment tool (Terraform / Bicep / Azure CLI), environment resource names, approval reviewers for QA and Prod

---

### 5. Destroy (`destroy.yml`)
**Status: Not started**

Tears down all app environment resources (Dev, QA, Prod). Bootstrap resources (Resource Group, ACR) are intentionally left intact so the pipeline can be re-deployed without reprovisioning shared infra.

Jobs (in order):
1. **Destroy Prod** — destroy prod environment
2. **Destroy QA** — `needs: destroy-prod`
3. **Destroy Dev** — `needs: destroy-qa`

Triggers on: `workflow_dispatch` only — never runs automatically

> Destroy order is prod → qa → dev (reverse of deploy) to avoid dependency issues.

---

## Sequencing Mechanism

Workflows are chained using GitHub Actions `workflow_run`:

```yaml
on:
  workflow_run:
    workflows: ["Validate"]
    types: [completed]
    branches: [main]

jobs:
  version:
    if: github.event.workflow_run.conclusion == 'success'
```

---

## Workflow Files

| File | Name | Purpose | Status |
|------|------|---------|--------|
| `bootstrap.yml` | Bootstrap | Provision Azure infra (RG, ACR) | Done |
| `validate.yml` | Validate | Lint + Test | Done |
| `build.yml` | Build | Version + Package + Push to ACR | In progress |
| `deploy.yml` | Deploy | Deploy Dev → QA → Prod | Not started |
| `destroy.yml` | Destroy | Tear down Dev, QA, Prod environments | Not started |

---

## Next Steps

1. ~~Rename `bootstrap-preparation.yml` → `bootstrap.yml`~~ Done
2. ~~Add lint + test pipeline~~ Done
3. ~~Rename `ci.yml` → `validate.yml`, separate from build~~ Done
4. Implement version bump script in `build.yml` (branch prefix → semver)
5. Add Docker build and ACR push to `build.yml`
6. Create `deploy.yml` with Dev → QA → Prod jobs in sequence (decide on deployment tool first)
7. Add approval gates for QA and Prod environments
8. Create `destroy.yml` (manual trigger, destroys Dev → QA → Prod, leaves bootstrap intact)
