# CI/CD Pipeline Architecture

This document describes the planned CI/CD pipeline for Wings. It is a living document — steps and tooling will evolve as implementation progresses.

---

## Overview

The pipeline is split into three stages — **Bootstrap**, **Build**, and **Deploy** — each as a separate GitHub Actions workflow file. They run in sequence, with each workflow triggering the next via `workflow_run` on success.

```
bootstrap.yml → build.yml → deploy-dev.yml → deploy-qa.yml → deploy-prod.yml
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

### 3. Deploy Dev (`deploy-dev.yml`)
**Status: Not started**

Deploys the versioned image to the dev environment.

Jobs:
1. **Plan** — preview infrastructure/deployment changes
2. **Apply** — deploy to dev

Triggers on: `workflow_run` → Build completed successfully

> Open: Deployment tool (Terraform / Bicep / Azure CLI), dev environment resource names

---

### 4. Deploy QA (`deploy-qa.yml`)
**Status: Not started**

Jobs:
1. **Plan**
2. **Apply** (manual approval gate TBD)

Triggers on: `workflow_run` → Deploy Dev completed successfully

> Open: Manual approval gate decision, QA environment resource names

---

### 5. Deploy Prod (`deploy-prod.yml`)
**Status: Not started**

Jobs:
1. **Plan**
2. **Apply** (manual approval required)

Triggers on: `workflow_run` → Deploy QA completed successfully

> Open: Prod environment resource names, approval reviewers

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
| `deploy-dev.yml` | Deploy Dev | 3 | Not started |
| `deploy-qa.yml` | Deploy QA | 3 | Not started |
| `deploy-prod.yml` | Deploy Prod | 3 | Not started |

---

## Next Steps

1. Rename `bootstrap-preparation.yml` → `bootstrap.yml`
2. Rename `ci.yml` → `build.yml`, trigger via `workflow_run` after Bootstrap
3. Add Docker build, version tagging, and ACR push jobs to `build.yml`
4. Create `deploy-dev.yml` (decide on deployment tool first)
5. Create `deploy-qa.yml` with approval gate
6. Create `deploy-prod.yml` with mandatory approval
