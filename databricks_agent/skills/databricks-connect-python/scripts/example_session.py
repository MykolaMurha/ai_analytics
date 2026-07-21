"""Databricks Connect for Python — minimal runnable examples.

Shows both serverless and classic-cluster sessions, a table read, and an
in-memory DataFrame. Credentials are resolved from your environment / config
profile (see setup_env.ps1 or `databricks auth login`); nothing is hard-coded.

Requirements:
    python -m venv .venv && .\.venv\Scripts\Activate.ps1   # (Windows)
    pip uninstall -y pyspark                                # avoid conflict
    pip install --upgrade "databricks-connect==<X.Y>.*"     # match your runtime

Run:
    python example_session.py                # serverless (default)
    python example_session.py --mode cluster # classic cluster
    python example_session.py --profile my-profile
"""

from __future__ import annotations

import argparse
import sys


def build_session(mode: str, profile: str | None):
    """Create a DatabricksSession using the requested strategy.

    Secrets are never passed here as literals; they come from the resolved
    config (env vars, named profile, or OAuth session).
    """
    from databricks.connect import DatabricksSession

    if profile:
        # Named ~/.databrickscfg profile (host + token/OAuth + optional compute)
        return DatabricksSession.builder.profile(profile).getOrCreate()

    if mode == "serverless":
        # Portable and recommended. Requires serverless_compute_id=auto in
        # config, or DATABRICKS_SERVERLESS_COMPUTE_ID=auto in the environment.
        return DatabricksSession.builder.serverless(True).getOrCreate()

    # mode == "cluster": rely on resolved config
    # (DATABRICKS_HOST/TOKEN/CLUSTER_ID or a profile). Zero-arg builder uses the
    # standard precedence order.
    return DatabricksSession.builder.getOrCreate()


def main() -> int:
    parser = argparse.ArgumentParser(description="Databricks Connect example")
    parser.add_argument(
        "--mode",
        choices=["serverless", "cluster"],
        default="serverless",
        help="Compute target (default: serverless)",
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="Named ~/.databrickscfg profile; overrides --mode config lookup",
    )
    parser.add_argument(
        "--table",
        default="samples.nyctaxi.trips",
        help="Fully qualified Unity Catalog table to read",
    )
    args = parser.parse_args()

    print(f"Creating session (mode={args.mode}, profile={args.profile})...")
    spark = build_session(args.mode, args.profile)

    # 1) Read a governed table (respects your Unity Catalog permissions).
    print(f"\nReading {args.table}:")
    try:
        spark.read.table(args.table).show(5)
    except Exception as exc:  # noqa: BLE001 - surface the reason plainly
        print(f"  could not read {args.table}: {exc}")

    # 2) Create and show an in-memory DataFrame (no source table needed).
    print("\nIn-memory DataFrame:")
    df = spark.createDataFrame(
        [(1, "genie"), (2, "connect"), (3, "unity-catalog")],
        schema="id INT, name STRING",
    )
    df.orderBy("id").show()

    print("Session OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
