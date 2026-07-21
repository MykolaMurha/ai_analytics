# Databricks Connect authentication (reference)

Source: https://docs.databricks.com/gcp/en/dev-tools/databricks-connect/
(cluster-config + python install, captured 2026-07-21).

> **Never commit, echo, or log tokens or `.databrickscfg` contents.** Supply
> secrets from the user's environment. Code references them by variable name.

## Configuration precedence (first match wins)

Databricks Connect resolves configuration in this order:

1. `DatabricksSession.builder.remote()` explicit arguments
2. A named Databricks configuration profile
3. `DATABRICKS_CONFIG_PROFILE` environment variable
4. Individual environment variables per property
5. `DEFAULT` configuration profile

## Method 1 — explicit `remote()`

```python
from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.remote(
    host=f"https://{workspace_instance_name}",
    token=retrieve_token(),          # returns the value at runtime
    cluster_id=retrieve_cluster_id()
).getOrCreate()
```

## Method 2 — config profile

```python
from databricks.connect import DatabricksSession
spark = DatabricksSession.builder.profile("<profile-name>").getOrCreate()
```

With an explicit cluster id via the SDK Config:

```python
from databricks.connect import DatabricksSession
from databricks.sdk.core import Config

spark = DatabricksSession.builder.sdkConfig(
    Config(profile="<profile-name>", cluster_id=retrieve_cluster_id())
).getOrCreate()
```

## Method 3 — `DATABRICKS_CONFIG_PROFILE`

```bash
export DATABRICKS_CONFIG_PROFILE="<profile-name>"   # PowerShell: $env:DATABRICKS_CONFIG_PROFILE = "<profile-name>"
```
```python
spark = DatabricksSession.builder.getOrCreate()
```

## Method 4 — individual environment variables

Set:
- `DATABRICKS_HOST`
- `DATABRICKS_TOKEN`
- `DATABRICKS_CLUSTER_ID` (classic compute) **or**
  `DATABRICKS_SERVERLESS_COMPUTE_ID=auto` (serverless; when set, `cluster_id`
  is ignored)

```python
spark = DatabricksSession.builder.getOrCreate()
```

## `.databrickscfg` format

Located at `~/.databrickscfg` (`%USERPROFILE%\.databrickscfg` on Windows).

PAT profile (classic cluster):
```ini
[my-cluster-profile]
host       = https://my-workspace.cloud.databricks.com
token      = <PAT>            ; supplied by the user; never checked in
cluster_id = <cluster-id>
```

Serverless profile:
```ini
[my-serverless-profile]
host                  = https://my-workspace.cloud.databricks.com
token                 = <PAT>
serverless_compute_id = auto
```

## OAuth vs PAT — required fields

| Auth type | Required fields |
|-----------|-----------------|
| **PAT** (personal access token) | `host`, `token` |
| **OAuth U2M** (user-to-machine, interactive) | `host` only — run `databricks auth login --host <host>` |
| **OAuth M2M** (service principal, automation) | `host`, `client_id`, `client_secret` |

Recommendation order: **OAuth U2M** or a **profile** for humans; **OAuth M2M**
for automation; **env-var PAT** only when the other two aren't available. For
serverless, add `serverless_compute_id = auto` (profile) or
`DATABRICKS_SERVERLESS_COMPUTE_ID=auto` (env).

## Serverless vs cluster session builders

```python
# serverless
spark = DatabricksSession.builder.serverless(True).getOrCreate()
# equivalent:
spark = DatabricksSession.builder.remote(serverless=True).getOrCreate()

# classic cluster (relies on resolved config for host/token/cluster_id)
spark = DatabricksSession.builder.getOrCreate()
```
