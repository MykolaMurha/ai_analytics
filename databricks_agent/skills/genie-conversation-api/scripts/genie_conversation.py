"""Genie Conversation API — dependency-light REST client.

Sends a question to a Genie space, polls the message to a terminal state with
exponential backoff, prints the natural-language answer and generated SQL, and
fetches the tabular query result.

Auth & config come from the environment (see setup_env.ps1); NO secrets in code:
    DATABRICKS_HOST   e.g. https://dbc-xxxx.cloud.databricks.com
    DATABRICKS_TOKEN  PAT or OAuth access token (Bearer)
    GENIE_SPACE_ID    the Genie Agent (space) id

Requires only `requests`:  pip install requests

Usage:
    python genie_conversation.py --question "Top 5 products by revenue last quarter"
    python genie_conversation.py --question "..." --follow-up "break it down by region"
"""

from __future__ import annotations

import argparse
import os
import sys
import time

import requests

API = "/api/2.0/genie"
TERMINAL = {"COMPLETED", "FAILED", "CANCELLED"}
RESULT_READY = {"PENDING_WAREHOUSE", "EXECUTING_QUERY", "COMPLETED"}


class Genie:
    def __init__(self, host: str, token: str, space_id: str):
        self.base = host.rstrip("/")
        self.space_id = space_id
        self.s = requests.Session()
        self.s.headers.update(
            {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )

    def _url(self, path: str) -> str:
        return f"{self.base}{API}{path}"

    def _req(self, method: str, path: str, **kw) -> dict:
        # simple retry with backoff for transient errors
        delay = 1.0
        for attempt in range(5):
            resp = self.s.request(method, self._url(path), timeout=60, **kw)
            if resp.status_code < 500 and resp.status_code != 429:
                resp.raise_for_status()
                return resp.json() if resp.content else {}
            time.sleep(delay)
            delay = min(delay * 2, 60)
        resp.raise_for_status()
        return {}

    def start_conversation(self, content: str) -> dict:
        return self._req(
            "POST",
            f"/spaces/{self.space_id}/start-conversation",
            json={"content": content},
        )

    def create_message(self, conversation_id: str, content: str) -> dict:
        return self._req(
            "POST",
            f"/spaces/{self.space_id}/conversations/{conversation_id}/messages",
            json={"content": content},
        )

    def get_message(self, conversation_id: str, message_id: str) -> dict:
        return self._req(
            "GET",
            f"/spaces/{self.space_id}/conversations/{conversation_id}/messages/{message_id}",
        )

    def query_result(self, conversation_id: str, message_id: str, attachment_id: str) -> dict:
        return self._req(
            "GET",
            f"/spaces/{self.space_id}/conversations/{conversation_id}"
            f"/messages/{message_id}/attachments/{attachment_id}/query-result",
        )

    def poll(self, conversation_id: str, message_id: str, timeout_s: int = 600) -> dict:
        """Poll until terminal state. Backoff 1s -> 60s, cap total at timeout_s."""
        deadline = time.monotonic() + timeout_s
        delay = 1.0
        while True:
            msg = self.get_message(conversation_id, message_id)
            status = msg.get("status")
            print(f"  status: {status}")
            if status in TERMINAL:
                return msg
            if time.monotonic() > deadline:
                raise TimeoutError(f"Genie message did not finish within {timeout_s}s (last: {status})")
            time.sleep(delay)
            delay = min(delay * 2, 60)


def show_answer(g: Genie, msg: dict) -> None:
    conversation_id = msg.get("conversation_id")
    message_id = msg.get("id") or msg.get("message_id")
    for att in msg.get("attachments", []) or []:
        text = (att.get("text") or {}).get("content")
        if text:
            print(f"\nAnswer:\n{text}")
        query = att.get("query") or {}
        sql = query.get("query") or query.get("sql")
        if sql:
            print(f"\nGenerated SQL:\n{sql}")
        attachment_id = att.get("attachment_id")
        # Only fetch query-results for attachments that actually produced SQL.
        # Text-only attachments also carry an attachment_id but return HTTP 400
        # from the query-result endpoint.
        if sql and attachment_id and msg.get("status") == "COMPLETED":
            try:
                result = g.query_result(conversation_id, message_id, attachment_id)
                _print_result(result)
            except requests.HTTPError as exc:
                print(f"\n(could not fetch query result: {exc})")


def _print_result(result: dict) -> None:
    # The result shape wraps a StatementExecution-style payload.
    data = result.get("statement_response") or result
    schema = (((data.get("manifest") or {}).get("schema") or {}).get("columns")) or []
    rows = (((data.get("result") or {}).get("data_array"))) or []
    if not rows:
        print("\n(no rows returned)")
        return
    cols = [c.get("name", f"c{i}") for i, c in enumerate(schema)]
    print("\nResult (first 20 rows):")
    if cols:
        print("  " + " | ".join(cols))
    for row in rows[:20]:
        print("  " + " | ".join("" if v is None else str(v) for v in row))
    if len(rows) > 20:
        print(f"  ... ({len(rows)} rows total)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Genie Conversation API client")
    parser.add_argument("--question", required=True, help="First question to ask")
    parser.add_argument("--follow-up", default=None, help="Optional follow-up in the same conversation")
    parser.add_argument("--timeout", type=int, default=600, help="Max seconds to wait per message")
    args = parser.parse_args()

    host = os.environ.get("DATABRICKS_HOST")
    token = os.environ.get("DATABRICKS_TOKEN")
    space_id = os.environ.get("GENIE_SPACE_ID")
    missing = [n for n, v in
               (("DATABRICKS_HOST", host), ("DATABRICKS_TOKEN", token), ("GENIE_SPACE_ID", space_id))
               if not v]
    if missing:
        print(f"Missing env vars: {', '.join(missing)}. Run setup_env.ps1 first.")
        return 2

    g = Genie(host, token, space_id)

    print(f"Starting conversation: {args.question!r}")
    started = g.start_conversation(args.question)
    conversation_id = started.get("conversation_id")
    message_id = started.get("message_id") or started.get("id")
    print(f"  conversation_id={conversation_id} message_id={message_id}")

    msg = g.poll(conversation_id, message_id, timeout_s=args.timeout)
    show_answer(g, msg)

    if args.follow_up:
        print(f"\nFollow-up: {args.follow_up!r}")
        fu = g.create_message(conversation_id, args.follow_up)
        fu_message_id = fu.get("message_id") or fu.get("id")
        msg2 = g.poll(conversation_id, fu_message_id, timeout_s=args.timeout)
        show_answer(g, msg2)

    return 0 if msg.get("status") == "COMPLETED" else 1


if __name__ == "__main__":
    sys.exit(main())
