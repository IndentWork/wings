# CI/CD Pipeline Architecture

This document describes the planned CI/CD pipeline for Wings. It is a living document — steps and tooling will evolve as implementation progresses.

---

## Overview

The pipeline is split into separate GitHub Actions workflow files that run in sequence. Each workflow triggers the next via `workflow_run` on success.

```
bootstrap.yml → app.yml → deploy-dev.yml → deploy-qa.yml → deploy-prod.yml
```

---

## Stages

### 1. Bootstrap (`bootstrap.yml`)
**Status: Done**

Provisions shared Azure infrastructure. Idempotent — safe to run on every push.

- Azure Login (Service Principal via `creds` JSON)
- Ensure Resource Group exists (`rg-wings-bootstrap`)
- Ensure ACR exists (`acrwingsacr01`)

Triggers on: `push` to `main`, `workflow_dispatch`

---

### 2. App Pipeline (`app.yml`)
**Status: Partially done (lint + test exist in `ci.yml`)**

Runs after bootstrap succeeds. Validates code, packages the app, and pushes the image to ACR.

Steps (in sequence):
1. **Lint** — black, isort, flake8
2. **Test** — pytest-django
3. **Package** — Docker image build
4. **Version** — tag image (from `pyproject.toml` version or git tag)
5. **Push to ACR** — push versioned image to `acrwingsacr01`

Triggers on: `workflow_run` → bootstrap completed successfully

> Open: Docker build context, image naming convention, versioning strategy (pyproject.toml vs git tags)

---

### 3. Deploy Dev (`deploy-dev.yml`)
**Status: Not started**

Deploys the versioned image to the dev environment.

Steps:
1. **Plan** — preview infrastructure/deployment changes
2. **Apply** — deploy to dev

Triggers on: `workflow_run` → app pipeline completed successfully

> Open: Deployment tool (Terraform / Bicep / Azure CLI), dev environment resource names

---

### 4. Deploy QA (`deploy-qa.yml`)
**Status: Not started**

Steps:
1. **Plan**
2. **Apply** (manual approval gate TBD)

Triggers on: `workflow_run` → deploy-dev completed successfully

> Open: Manual approval gate decision, QA environment resource names

---

### 5. Deploy Prod (`deploy-prod.yml`)
**Status: Not started**

Steps:
1. **Plan**
2. **Apply** (manual approval required)

Triggers on: `workflow_run` → deploy-qa completed successfully

> Open: Prod environment resource names, approval reviewers

---

## Sequencing Mechanism

Separate workflow files are chained using GitHub Actions `workflow_run`:

```yaml
on:
  workflow_run:
    workflows: ["Bootstrap Preparation"]
    types: [completed]
    branches: [main]

jobs:
  app:
    if: github.event.workflow_run.conclusion == 'success'
```

---

## Current Workflow Files

| File | Purpose | Status |
|------|---------|--------|
| `bootstrap-preparation.yml` | Azure infra bootstrap | Done |
| `ci.yml` | Lint + Test | Done (to be replaced by `app.yml`) |

---

## Next Steps

1. Restructure `ci.yml` → `app.yml`, trigger via `workflow_run` after bootstrap
2. Add Docker build, version tagging, and ACR push to `app.yml`
3. Create `deploy-dev.yml` (decide on deployment tool first)
4. Create `deploy-qa.yml` with approval gate
5. Create `deploy-prod.yml` with mandatory approval
