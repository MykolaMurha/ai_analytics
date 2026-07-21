# Databricks Connect troubleshooting (reference)

Source: Databricks Connect for Python troubleshooting + install guidance
(captured 2026-07-21).

## Version mismatch (most common)

Symptom: connection or protocol errors, or `getOrCreate()` failing unexpectedly.

- The `databricks-connect` **major.minor must match** the cluster's Databricks
  Runtime. Check the cluster's runtime, then:
  ```bash
  pip install --upgrade "databricks-connect==<X.Y>.*"
  ```
- Classic compute requires **Databricks Runtime 13.3 LTS+**.

## `pyspark` conflict

Symptom: `ImportError`, wrong Spark being imported, or ambiguous behavior.

- `databricks-connect` conflicts with `pyspark`. Remove pyspark from the same
  environment:
  ```bash
  pip show pyspark && pip uninstall -y pyspark
  ```
- Always work in a **dedicated virtual environment** to avoid leaking a global
  pyspark into the session.

## Authentication failures

- Confirm which config source is actually winning (precedence order matters —
  explicit `remote()` args beat env vars beat the DEFAULT profile).
- Verify `DATABRICKS_HOST` has the scheme (`https://…`) and no trailing path.
- For serverless, ensure `serverless_compute_id = auto` /
  `DATABRICKS_SERVERLESS_COMPUTE_ID=auto` is set, otherwise the builder looks
  for a `cluster_id`.
- For OAuth U2M, re-run `databricks auth login --host <host>` if the session
  token expired.

## Serverless vs cluster confusion

- If both a `cluster_id` and `serverless_compute_id=auto` are configured,
  serverless wins and `cluster_id` is ignored.
- `DatabricksSession.builder.serverless(True)` forces serverless regardless of
  other config.

## Quick diagnostics

```python
from databricks.sdk.core import Config
cfg = Config()               # resolves via the same precedence
print("host:", cfg.host)     # never print cfg.token
print("auth_type:", cfg.auth_type)
```

Run `scripts/verify_connection.py` for an end-to-end smoke test that fails with
a hint pointing at the likely cause.
