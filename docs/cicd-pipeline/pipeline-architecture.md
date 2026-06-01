# CI/CD Pipeline Architecture

This document describes the planned CI/CD pipeline for Wings. It is a living document — steps and tooling will evolve as implementation progresses.

---

## Overview

The pipeline is split into three stages — **Bootstrap**, **Validate**, and **Build** — each as a separate GitHub Actions workflow file. They run in sequence, with each workflow triggering the next via `workflow_run` on success.

```
bootstrap.yml → validate.yml → build.yml → (image in ACR)
                                                │
                                                └──▶ consumed by wings_deployment/
```

**On PRs:** only `validate.yml` runs — no infra, no packaging.
**On push to main:** full chain runs — bootstrap → validate → build.

Deployment is handled by a separate repository (`wings_deployment/`) and is not part of this pipeline. See `docs/deployment.md` at the project root.

---

## Stages

### 1. Bootstrap (`bootstrap.yml`)
**Status: Done**

Provisions shared Azure infrastructure. Idempotent — safe to run on every push.

- Azure Login (Service Principal via `creds` JSON)
- Ensure Resource Group exists (`rg-iw-wings-bootstrap`)
- Ensure ACR exists (`acriwwings01`)

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
3. **Push to ACR** — push versioned image to `acriwwings01`

Triggers on: `workflow_run` → Validate completed successfully on `main`

> Open: Docker build context, image naming convention, versioning script implementation

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

---

## Next Steps

1. ~~Rename `bootstrap-preparation.yml` → `bootstrap.yml`~~ Done
2. ~~Add lint + test pipeline~~ Done
3. ~~Rename `ci.yml` → `validate.yml`, separate from build~~ Done
4. Implement version bump script in `build.yml` (branch prefix → semver)
5. Add Docker build and ACR push to `build.yml`
