"""Smoke-test a Databricks Connect setup and diagnose common failures.

Run after configuring credentials (setup_env.ps1, a profile, or OAuth):
    python verify_connection.py
    python verify_connection.py --mode cluster
    python verify_connection.py --profile my-profile

Exits 0 on success, non-zero with a hint on failure. Never prints secrets.
"""

from __future__ import annotations

import argparse
import sys


def diagnose(exc: Exception) -> str:
    text = f"{type(exc).__name__}: {exc}".lower()
    if "pyspark" in text:
        return ("pyspark conflict — run: pip uninstall -y pyspark, then "
                "reinstall databricks-connect in a clean venv.")
    if "version" in text or "protocol" in text or "compatib" in text:
        return ("version mismatch — pin databricks-connect to the cluster's "
                "runtime: pip install 'databricks-connect==<X.Y>.*'.")
    if "auth" in text or "token" in text or "401" in text or "credential" in text:
        return ("authentication — check DATABRICKS_HOST/DATABRICKS_TOKEN, the "
                "named profile, or re-run 'databricks auth login --host <host>'.")
    if "cluster" in text or "serverless" in text or "compute" in text:
        return ("compute target — set DATABRICKS_CLUSTER_ID (cluster) or "
                "DATABRICKS_SERVERLESS_COMPUTE_ID=auto (serverless).")
    return "see references/troubleshooting.md."


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Databricks Connect")
    parser.add_argument("--mode", choices=["serverless", "cluster"], default="serverless")
    parser.add_argument("--profile", default=None)
    args = parser.parse_args()

    # Show resolved host/auth type WITHOUT revealing the token.
    try:
        from databricks.sdk.core import Config
        cfg = Config(profile=args.profile) if args.profile else Config()
        print(f"Resolved host: {cfg.host}")
        print(f"Auth type:     {cfg.auth_type}")
    except Exception as exc:  # noqa: BLE001
        print(f"Could not resolve config: {exc}")
        print(f"Hint: {diagnose(exc)}")
        return 2

    try:
        from databricks.connect import DatabricksSession

        if args.profile:
            spark = DatabricksSession.builder.profile(args.profile).getOrCreate()
        elif args.mode == "serverless":
            spark = DatabricksSession.builder.serverless(True).getOrCreate()
        else:
            spark = DatabricksSession.builder.getOrCreate()

        result = spark.sql("SELECT 1 AS ok").collect()
        assert result and result[0]["ok"] == 1
        print("Connection OK — SELECT 1 returned 1.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Connection FAILED: {exc}")
        print(f"Hint: {diagnose(exc)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
