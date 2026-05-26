# Bootstrap Preparation Pipeline

## Overview

The bootstrap preparation pipeline is the **first pipeline** that runs after a merge to `main`. Its responsibility is to ensure all foundational Azure infrastructure exists before any build or deployment pipeline runs.

It is idempotent — safe to run multiple times. If resources already exist, steps are skipped.

## Trigger

Runs automatically on every push to `main` (i.e., after a PR is merged).

## Pipeline File

`.github/workflows/bootstrap-preparation.yml`

## Sequential Steps

```
push to main
     │
     ▼
1. Azure Login
     │
     ▼
2. Ensure Resource Group exists
     │
     ▼
3. Ensure ACR exists
```

### Step 1 — Azure Login

Authenticates to Azure using the service principal `wings-github-actions-sp` via credentials stored in GitHub Secrets.

| Secret | Purpose |
|---|---|
| `AZURE_CLIENT_ID` | Service principal app ID |
| `AZURE_CLIENT_SECRET` | Service principal password |
| `AZURE_TENANT_ID` | Azure AD tenant |
| `AZURE_SUBSCRIPTION_ID` | Target subscription |

### Step 2 — Ensure Resource Group exists

Checks if `rg-wings-bootstrap` exists in `southindia`.
- **Exists** → skips
- **Not exists** → creates it

### Step 3 — Ensure ACR exists

Checks if `acrwingsacr01` exists inside `rg-wings-bootstrap`.
- **Exists** → skips
- **Not exists** → creates it with `Basic` SKU

## Configuration

| Variable | Value |
|---|---|
| `RESOURCE_GROUP` | `rg-wings-bootstrap` |
| `ACR_NAME` | `acrwingsacr01` |
| `LOCATION` | `southindia` |

ACR naming follows the convention `acrwingsacr<number>` — increment the number if additional registries are needed (e.g., `acrwingsacr02`).

## Pipeline Sequence

This is pipeline **1 of 3** in the merge sequence:

| Order | Pipeline | Trigger |
|---|---|---|
| 1 | Bootstrap Preparation | push to main |
| 2 | Build & Push | on completion of Bootstrap Preparation |
| 3 | Deploy | on completion of Build & Push |

The next pipeline (`build-push.yml`) uses `workflow_run` to trigger only after this pipeline completes successfully.
