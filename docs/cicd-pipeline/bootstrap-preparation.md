# Bootstrap Pipeline

## Overview

The bootstrap pipeline is the **first** workflow that runs in the `wings/` repository on push to `main`. Its responsibility is to ensure all foundational Azure infrastructure exists before the build pipeline runs.

It is idempotent — safe to run multiple times. If resources already exist, steps are skipped.

## Trigger

Runs automatically on every push to `main`, and via `workflow_dispatch` for manual runs.

## Pipeline File

`.github/workflows/bootstrap.yml`

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

Checks if `rg-iw-wings-bootstrap` exists in `southindia`.
- **Exists** → skips
- **Not exists** → creates it

### Step 3 — Ensure ACR exists

Checks if `acriwwings01` exists inside `rg-iw-wings-bootstrap`.
- **Exists** → skips
- **Not exists** → creates it with `Basic` SKU

## Configuration

| Variable | Value |
|---|---|
| `RESOURCE_GROUP` | `rg-iw-wings-bootstrap` |
| `ACR_NAME` | `acriwwings01` |
| `LOCATION` | `southindia` |

ACR naming follows the convention `acr<org><project><number>` (alphanumeric only — Azure restriction) — increment the number if additional registries are needed (e.g., `acriwwings02`).

## Position in the pipeline

This is workflow **1 of 3** in the `wings/` CI/CD chain:

| Order | Workflow | Trigger |
|---|---|---|
| 1 | Bootstrap | push to main |
| 2 | Validate | on completion of Bootstrap |
| 3 | Build | on completion of Validate |

Deployment is **not** part of this chain — it lives in the separate `wings_deployment/` repository. See `docs/deployment.md` at the project root.

The next workflow (`validate.yml`) uses `workflow_run` to trigger only after this pipeline completes successfully.
