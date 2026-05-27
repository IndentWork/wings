# CHANGELOG


## v0.3.0 (2026-05-27)

### Features

- Add home page
  ([`b5768ee`](https://github.com/IndentWork/wings/commit/b5768ee20aec8d8e6976841bba363ab072b5c622))

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>


## v0.2.3 (2026-05-27)

### Bug Fixes

- Rename ACR from acrwingsacr01 to acrwings01
  ([`6e63019`](https://github.com/IndentWork/wings/commit/6e63019701bdb31f7e702a13f41956df1659aa2f))

Removes the duplicate "acr" in the registry name. The new convention is acrwings<number> (e.g.
  acrwings01, acrwings02) — single resource-type prefix only.

Updates bootstrap.yml and build.yml. Refreshes the bootstrap documentation to match: new ACR name,
  current workflow filename (bootstrap.yml, not bootstrap-preparation.yml), and the actual
  3-workflow chain (Bootstrap → Validate → Build).

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Documentation

- Remove deploy and destroy stages from pipeline architecture
  ([`976f215`](https://github.com/IndentWork/wings/commit/976f215b269f6066a4f1b39d83cf80c9f186aabe))

Deploy and destroy are not part of the wings/ pipeline — they live in wings_deployment/. The doc was
  still describing them as wings/ stages, which is no longer accurate.

Removes: - Stage 4 (Deploy) and Stage 5 (Destroy) sections - deploy.yml and destroy.yml rows from
  the Workflow Files table - Next Steps items 6-8 (deploy and destroy creation) - Deploy/destroy
  boxes from the overview diagram

Adds a pointer to docs/deployment.md at the project root, where the deployment plan now lives.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>


## v0.2.2 (2026-05-26)

### Bug Fixes

- Explicitly set prerelease = false for main branch in PSR
  ([`7f9dcc0`](https://github.com/IndentWork/wings/commit/7f9dcc0164e97c5d5aba6066425957f80f646197))

Ensures all releases from main are stable releases, never beta or pre-release, using PSR v9 branch
  group configuration.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>


## v0.2.1 (2026-05-26)

### Bug Fixes

- Resolve collectstatic failure in Docker build
  ([`d901ea5`](https://github.com/IndentWork/wings/commit/d901ea5b5258f11009370bf4f85c0dcee764bbc4))

- Add STATIC_ROOT to settings.py (required by collectstatic) - Use .venv/bin/python directly instead
  of uv run to avoid re-downloading dev dependencies during image build

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>


## v0.2.0 (2026-05-26)

### Features

- Add Dockerfile and wire ACR push in build pipeline
  ([`3a5dbe1`](https://github.com/IndentWork/wings/commit/3a5dbe1f48cdeda837baaaf65a92ff3f39d348e7))

- Adds Dockerfile using python:3.13-slim, uv, gunicorn on port 8000 - Adds .dockerignore to exclude
  git, venv, env, and test artifacts - Adds gunicorn to project dependencies - Updates build.yml
  package job with real docker build and ACR push - Image tagged with semver version and latest

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add OCI labels to Docker image build
  ([`8205fee`](https://github.com/IndentWork/wings/commit/8205fee08f3f808c44831bac1e783878864f43ed))

Embeds version, commit SHA, source repo, and build timestamp as standard OCI image labels so
  deployment can identify exact image origin.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>


## v0.1.0 (2026-05-26)

### Bug Fixes

- Chain validate after bootstrap via workflow_run
  ([`72ee191`](https://github.com/IndentWork/wings/commit/72ee1915460c79634947693840887634e4da8c13))

Validate now triggers after Bootstrap succeeds on main instead of running in parallel on push. On
  PRs it still runs directly.

Sequence on main: bootstrap → validate → build

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Enable workflow_dispatch and use creds JSON for SP auth
  ([`c4ed6a9`](https://github.com/IndentWork/wings/commit/c4ed6a9d96ffdf56eaf7d77e8629a41d2fdf34a3))

- Adds workflow_dispatch to allow manual triggering from GitHub Actions UI - Fixes azure/login@v2 to
  use creds JSON format (required for SP with client secret)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Pin astral-sh/setup-uv to v8.1.0
  ([`8ff276a`](https://github.com/IndentWork/wings/commit/8ff276ad300f655755d0b817394fafbd538f9062))

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Upgrade actions to Node.js 24 compatible versions
  ([`260355d`](https://github.com/IndentWork/wings/commit/260355d6673d7ff9bded6935bb21b35b7dba7bc7))

actions/checkout v4 → v6 actions/setup-python v5 → v6 astral-sh/setup-uv v5 → v8

Node.js 20 actions are deprecated and will be forced to Node.js 24 by default on June 2nd, 2026.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Use creds JSON for azure/login v3 SP auth
  ([`c258e0e`](https://github.com/IndentWork/wings/commit/c258e0ee1aea50912b5f2d987a55ae4795792c5a))

v3 dropped client-secret as a standalone input; use the creds JSON blob to authenticate with a
  service principal instead of OIDC.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Chores

- Upgrade azure/login to v3 for Node.js 24 support
  ([`68e2441`](https://github.com/IndentWork/wings/commit/68e2441b306da7d116183a7198cb9c67c5d4cdb5))

Resolves deprecation warning. v3 explicitly runs on Node.js 24, which GitHub forces by default
  starting June 2, 2026.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Upgrade azure/login to v3 with updated input format
  ([`42da2b5`](https://github.com/IndentWork/wings/commit/42da2b5835fe644e18522f8d365e191e7ebd21aa))

Replaces the deprecated creds JSON blob with individual client-id, client-secret, tenant-id, and
  subscription-id inputs required by v3.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Documentation

- Add CI/CD pipeline architecture plan
  ([`9c98da3`](https://github.com/IndentWork/wings/commit/9c98da3d41777f50859e743145f603d2aa33ec2e))

Living document outlining the full pipeline design — bootstrap, app, and multi-environment deploy
  (dev, qa, prod). To be updated as each stage is implemented.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add destroy.yml stage to pipeline architecture
  ([`64600cb`](https://github.com/IndentWork/wings/commit/64600cbf6507262a5c566f586028612c3b7672c3))

Documents a manual-trigger-only destroy workflow that tears down Dev, QA, and Prod environments in
  reverse order while preserving bootstrap resources (Resource Group, ACR).

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Consolidate deploy stages into single deploy.yml
  ([`b4910db`](https://github.com/IndentWork/wings/commit/b4910dbb3b20f2f96572c3a5eade83974438b006))

Replace three separate deploy workflow files with one deploy.yml containing Dev, QA, and Prod jobs
  chained via needs.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Update pipeline architecture with Bootstrap/Build/Deploy naming
  ([`5961f1a`](https://github.com/IndentWork/wings/commit/5961f1a024e4fc67b4311725af6c7140012630de))

Renames stages to Bootstrap, Build, and Deploy. Updates workflow file names (bootstrap.yml,
  build.yml, deploy-*.yml) and refreshes next steps.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Features

- Add .env to .gitignore
  ([`9362835`](https://github.com/IndentWork/wings/commit/9362835b4f49aee161ae6979bb764856128a13a7))

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add bootstrap preparation pipeline and docs
  ([`60ebb62`](https://github.com/IndentWork/wings/commit/60ebb62b914d8ae227e1f238624cb67d6fd42805))

Adds GitHub Actions workflow to check/create resource group and ACR on merge to main. Includes
  cicd-pipeline documentation under docs/.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add CI workflow with Django tests and linting
  ([`2884a41`](https://github.com/IndentWork/wings/commit/2884a41e54051ed03ce650a690701b547c02077b))

Adds GitHub Actions CI pipeline with two jobs: - lint: black, isort, flake8 (line length 120) -
  test: Django test runner via uv

Also adds dev dependency group and tool configs in pyproject.toml, .flake8 config file, and
  reformats existing code to pass all checks.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add pytest-django with basic smoke test
  ([`1bf9f9b`](https://github.com/IndentWork/wings/commit/1bf9f9beb2d603cefb982e6ebc58d45e6b8a2566))

Replaces manage.py test runner with pytest-django. Adds pytest and pytest-django to dev
  dependencies, configures DJANGO_SETTINGS_MODULE in pyproject.toml, and adds a smoke test for the
  admin login page.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add python-semantic-release for versioning and changelog
  ([`2fc61e8`](https://github.com/IndentWork/wings/commit/2fc61e820e7806a677d5dca0374d553e44b9e1c3))

- Adds python-semantic-release to dev dependencies - Configures version bump rules in
  pyproject.toml: feat → minor, fix/hotfix/refactor/perf → patch, chore/docs/ci → skip - Updates
  build.yml to run semantic-release as the version job - Package job only runs if a new version was
  released - Adds initial CHANGELOG.md

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Enable GitHub Release creation on version bump
  ([`f7060e6`](https://github.com/IndentWork/wings/commit/f7060e6defd6300654b87bfe77f7ed28a83eef8c))

Sets upload_to_vcs_release = true so python-semantic-release creates a GitHub Release with changelog
  notes alongside the git tag.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Rename and restructure Bootstrap and Build workflows
  ([`366a452`](https://github.com/IndentWork/wings/commit/366a45267733ca87070540b8be4b6f33d4f0127c))

- Rename bootstrap-preparation.yml → bootstrap.yml (name: Bootstrap) - Replace ci.yml → build.yml
  (name: Build) - Build triggers via workflow_run after Bootstrap on main, and on PRs - Lint runs
  before test via needs: [lint] in test job

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Split build into validate and build stages
  ([`d12f53f`](https://github.com/IndentWork/wings/commit/d12f53f54f30da8b6bfabce9c577d00286506df1))

- Rename build.yml → validate.yml (name: Validate) for lint + test - Create new build.yml (name:
  Build) triggered after Validate on main - Build scaffolds version, package, and ACR push jobs
  (implementation pending) - Update pipeline architecture doc to reflect 4-stage pipeline

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
