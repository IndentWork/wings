# CI/CD Pipeline Architecture

This document describes the planned CI/CD pipeline for Wings. It is a living document — steps and tooling will evolve as implementation progresses.

---

## Overview

The pipeline is split into three stages — **Bootstrap**, **Build**, and **Deploy** — each as a separate GitHub Actions workflow file. They run in sequence, with each workflow triggering the next via `workflow_run` on success.

```
bootstrap.yml → build.yml → deploy.yml
                             └── Deploy Dev (plan → apply)
                             └── Deploy QA  (plan → apply)
                             └── Deploy Prod (plan → apply)
```

---

## Stages

### 1. Bootstrap (`bootstrap.yml`)
**Status: Done** (currently named `bootstrap-preparation.yml`, to be renamed)

Provisions shared Azure infrastructure. Idempotent — safe to run on every push.

- Azure Login (Service Principal via `creds` JSON)
- Ensure Resource Group exists (`rg-wings-bootstrap`)
- Ensure ACR exists (`acrwingsacr01`)

Triggers on: `push` to `main`, `workflow_dispatch`

---

### 2. Build (`build.yml`)
**Status: Partially done** (lint + test exist in `ci.yml`, to be renamed and extended)

Runs after Bootstrap succeeds. Validates code, packages the app, and pushes the image to ACR.

Jobs (in sequence):
1. **Lint** — black, isort, flake8
2. **Test** — pytest-django
3. **Package** — Docker image build
4. **Version** — tag image (from `pyproject.toml` version or git tag)
5. **Push to ACR** — push versioned image to `acrwingsacr01`

Triggers on: `workflow_run` → Bootstrap completed successfully

> Open: Docker build context, image naming convention, versioning strategy (pyproject.toml vs git tags)

---

### 3. Deploy (`deploy.yml`)
**Status: Not started**

Single workflow with three environment jobs chained in sequence via `needs`.

Jobs (in order):
1. **Deploy Dev** — plan → apply
2. **Deploy QA** — plan → apply (manual approval gate TBD) — `needs: deploy-dev`
3. **Deploy Prod** — plan → apply (manual approval required) — `needs: deploy-qa`

Triggers on: `workflow_run` → Build completed successfully

> Open: Deployment tool (Terraform / Bicep / Azure CLI), environment resource names, approval reviewers for QA and Prod

---

## Sequencing Mechanism

Workflows are chained using GitHub Actions `workflow_run`:

```yaml
on:
  workflow_run:
    workflows: ["Bootstrap"]
    types: [completed]
    branches: [main]

jobs:
  build:
    if: github.event.workflow_run.conclusion == 'success'
```

---

## Workflow Files

| File | Name | Stage | Status |
|------|------|-------|--------|
| `bootstrap.yml` | Bootstrap | 1 | Done (rename pending) |
| `build.yml` | Build | 2 | In progress (rename + extend `ci.yml`) |
| `deploy.yml` | Deploy (Dev → QA → Prod) | 3 | Not started |

---

## Next Steps

1. Rename `bootstrap-preparation.yml` → `bootstrap.yml`
2. Rename `ci.yml` → `build.yml`, trigger via `workflow_run` after Bootstrap
3. Add Docker build, version tagging, and ACR push jobs to `build.yml`
4. Create `deploy.yml` with Dev → QA → Prod jobs in sequence (decide on deployment tool first)
5. Add approval gates for QA and Prod environments
