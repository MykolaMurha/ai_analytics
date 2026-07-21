"""Genie Conversation API via the official databricks-sdk.

The SDK's *_and_wait helpers handle polling for you, so this is the shortest
path to a working integration. Auth/config are resolved by WorkspaceClient from
the environment or a config profile — NO secrets in code.

    DATABRICKS_HOST   e.g. https://dbc-xxxx.cloud.databricks.com
    DATABRICKS_TOKEN  PAT or OAuth token   (or use a profile / `databricks auth login`)
    GENIE_SPACE_ID    the Genie Agent (space) id

Install:  pip install databricks-sdk

Usage:
    python genie_sdk_example.py --question "Top 5 products by revenue last quarter"
    python genie_sdk_example.py --question "..." --follow-up "break it down by region"
"""

from __future__ import annotations

import argparse
import os
import sys


def render(w, space_id, msg) -> None:
    """Print the text answer, SQL, and (if present) the tabular result."""
    for att in (msg.attachments or []):
        if att.text and att.text.content:
            print(f"\nAnswer:\n{att.text.content}")
        has_sql = bool(att.query and getattr(att.query, "query", None))
        if has_sql:
            print(f"\nGenerated SQL:\n{att.query.query}")
        # Only SQL-bearing attachments have fetchable query results.
        if has_sql and att.attachment_id and str(getattr(msg, "status", "")).endswith("COMPLETED"):
            try:
                res = w.genie.get_message_attachment_query_result(
                    space_id=space_id,
                    conversation_id=msg.conversation_id,
                    message_id=msg.id,
                    attachment_id=att.attachment_id,
                )
                sr = res.statement_response
                rows = (sr.result.data_array if sr and sr.result else None) or []
                cols = ([c.name for c in sr.manifest.schema.columns]
                        if sr and sr.manifest and sr.manifest.schema else [])
                if rows:
                    print("\nResult (first 20 rows):")
                    if cols:
                        print("  " + " | ".join(cols))
                    for row in rows[:20]:
                        print("  " + " | ".join("" if v is None else str(v) for v in row))
                    if len(rows) > 20:
                        print(f"  ... ({len(rows)} rows total)")
                else:
                    print("\n(no rows returned)")
            except Exception as exc:  # noqa: BLE001
                print(f"\n(could not fetch query result: {exc})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Genie via databricks-sdk")
    parser.add_argument("--question", required=True)
    parser.add_argument("--follow-up", default=None)
    args = parser.parse_args()

    space_id = os.environ.get("GENIE_SPACE_ID")
    if not space_id:
        print("Missing GENIE_SPACE_ID. Run setup_env.ps1 first.")
        return 2

    from databricks.sdk import WorkspaceClient

    # Resolves auth from env vars / profile / OAuth session.
    w = WorkspaceClient()

    print(f"Asking: {args.question!r}")
    msg = w.genie.start_conversation_and_wait(space_id=space_id, content=args.question)
    render(w, space_id, msg)

    if args.follow_up:
        print(f"\nFollow-up: {args.follow_up!r}")
        msg2 = w.genie.create_message_and_wait(
            space_id=space_id,
            conversation_id=msg.conversation_id,
            content=args.follow_up,
        )
        render(w, space_id, msg2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
