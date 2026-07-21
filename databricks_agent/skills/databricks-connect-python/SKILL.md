---
name: databricks-connect-python
description: Use when a user wants to run Spark/DataFrame or PySpark code from a local Python IDE, notebook server, or custom app against Databricks compute (serverless or a classic cluster) using Databricks Connect. Covers virtualenv setup, the exact pip install and version-pinning rules, removing conflicting pyspark, authentication (config profile, env vars, OAuth U2M/M2M, PAT) with its precedence order, building a DatabricksSession for serverless vs cluster, and verifying the connection. Provides a PowerShell env-var setup script and runnable Python examples. Not for the Genie API (see genie-conversation-api).
---

# Databricks Connect for Python

Databricks Connect lets you connect IDEs (PyCharm, VS Code), notebook servers,
and custom apps to Databricks compute, so you write Spark/DataFrame code
locally and it executes on Databricks — **serverless** or a **classic
cluster**.

## Requirements

- **Databricks Runtime 13.3 LTS or above** for classic compute (or serverless
  compute).
- A dedicated **Python virtual environment** per Python version you use.
- Workspace host, and either a config profile / OAuth / PAT (see auth below).
- For classic compute: a **cluster id**. For serverless: nothing beyond auth
  (set `serverless_compute_id = auto`).

## Install

The package **conflicts with `pyspark`** — remove it first, then pin
`databricks-connect` to your cluster's runtime major.minor.

```bash
# 1) fresh virtual environment
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:  source .venv/bin/activate

# 2) remove conflicting pyspark if present
pip show pyspark && pip uninstall -y pyspark

# 3) install, pinning to your runtime (e.g. 17.3.x) with dot-asterisk notation
pip install --upgrade "databricks-connect==17.3.*"
```

Replace `17.3` with your cluster's Databricks Runtime version. With Poetry:
`poetry add databricks-connect@~17.3`. The `==X.Y.*` / `@~X.Y` notation keeps
you on the newest patch of a compatible line.

## Authenticate (do this without hard-coding secrets)

**Never put tokens in code or in this repo.** Choose one, most-secure first:

1. **OAuth U2M** — `databricks auth login --host <host>` (interactive; best for
   humans). Needs only `host` in the profile.
2. **`~/.databrickscfg` profile** — store `host` (+ `token` or OAuth fields) in
   a named profile; reference the profile by name in code.
3. **OAuth M2M** — service principal `client_id` + `client_secret` (best for
   automation).
4. **Environment-variable PAT** — `DATABRICKS_HOST` + `DATABRICKS_TOKEN`
   (+ `DATABRICKS_CLUSTER_ID` or `DATABRICKS_SERVERLESS_COMPUTE_ID=auto`).

To set the env-var path on Windows **without exposing the token**, run the
provided script (it prompts for the token with hidden input and stores
user-scoped variables):

```powershell
# from this skill's folder
powershell -ExecutionPolicy Bypass -File .\scripts\setup_env.ps1
```

### Config precedence (first match wins)
1. `DatabricksSession.builder.remote(...)` explicit args
2. Named Databricks config profile
3. `DATABRICKS_CONFIG_PROFILE` env var
4. Individual env vars (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`, …)
5. `DEFAULT` config profile

## Create a session

**Serverless (recommended, portable):**
```python
from databricks.connect import DatabricksSession
spark = DatabricksSession.builder.serverless(True).getOrCreate()
```

**Classic cluster, explicit:**
```python
from databricks.connect import DatabricksSession
spark = DatabricksSession.builder.remote(
    host="https://<workspace-host>",
    token=my_token,          # supplied at runtime, never hard-coded
    cluster_id="<cluster-id>"
).getOrCreate()
```

**From a named profile:**
```python
spark = DatabricksSession.builder.profile("<profile-name>").getOrCreate()
```

**From env vars / DEFAULT profile (zero args):**
```python
spark = DatabricksSession.builder.getOrCreate()
```

Then use it like any Spark session:
```python
df = spark.read.table("samples.nyctaxi.trips")
df.show(5)
```

## Verify

```bash
python .\scripts\verify_connection.py
```
It prints the Spark/remote version and runs a trivial query, failing loudly
with a diagnosis hint if auth or the version pin is wrong.

## Scripts

- `scripts/setup_env.ps1` — set `DATABRICKS_*` **user-scoped env vars** via
  hidden prompts. Never writes secrets to disk in plaintext files or history.
- `scripts/example_session.py` — serverless + cluster session, DataFrame read
  and an in-memory DataFrame example.
- `scripts/verify_connection.py` — connection smoke test with diagnostics.

## References

- `references/authentication.md` — every auth method, `.databrickscfg` format,
  env-var names, precedence, and OAuth vs PAT, in depth.
- `references/troubleshooting.md` — version-mismatch, pyspark conflict, and
  common connection errors.
