---
name: genie-conversation-api
description: Use when a user wants to drive Databricks Genie programmatically — ask a Genie Agent (space) questions over REST or the databricks-sdk, poll a message to completion, fetch the generated SQL and tabular query results, hold multi-turn conversations, or import/export/manage spaces via serialized_space. Covers all endpoints and paths, the message status workflow and polling strategy, attachment/result retrieval, authentication (OAuth U2M/M2M, PAT), the serialized_space schema and validation rules, and rate-limit/retry best practices. Provides a PowerShell env-var script, a runnable REST client, and an SDK example. For the UI build use genie-agent-setup.
---

# Genie Conversation API

Drive a Genie Agent from code: send a natural-language question to a space,
poll until the answer is ready, then read the generated SQL and its tabular
results. Two surfaces: **REST** (`/api/2.0/genie/...`) and the **`databricks-sdk`**
(`WorkspaceClient.genie`). "Space" and "Agent" are the same object.

## Prerequisites

- A Databricks workspace with **SQL** entitlement.
- At least **CAN USE** on a **Pro or Serverless SQL warehouse**.
- The **workspace host** and the target **`space_id`** (from the agent URL or
  `GET /api/2.0/genie/spaces`).
- Auth: **OAuth U2M** (interactive), **OAuth M2M** (service principal, for
  automation), or a **PAT**. Header: `Authorization: Bearer <token>`.
  A service principal needs permissions on the target data and SQL warehouse.

Set credentials without exposing them:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_env.ps1
```

## The core loop

1. **Start a conversation** with your first question →
   `POST /api/2.0/genie/spaces/{space_id}/start-conversation`
   body `{"content": "<question>"}` → returns `conversation_id` + `message_id`.
2. **Poll the message** →
   `GET /api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}`
   until status is terminal.
3. **Read results** — from the message's `attachments`:
   - `text` — natural-language answer.
   - `query` — generated SQL (+ `parameters` if a trusted asset was used).
   - `attachment_id` — use it to fetch the table:
     `GET .../messages/{message_id}/attachments/{attachment_id}/query-result`
4. **Follow up (multi-turn)** →
   `POST .../conversations/{conversation_id}/messages` body `{"content": "..."}`.

### Message status workflow
```
IN_PROGRESS → PENDING_WAREHOUSE → EXECUTING_QUERY → COMPLETED
                                                   ↘ FAILED / CANCELLED
```
The real API emits more granular intermediate states than the docs list
(e.g. `FETCHING_METADATA`, `FILTERING_CONTEXT`, `ASKING_AI`), so **don't
hard-code the sequence** — treat any non-terminal status as "keep polling" and
stop only on **COMPLETED**, **FAILED**, or **CANCELLED**. To fetch query
results, wait until at least PENDING_WAREHOUSE, take the `attachment_id` from an
attachment that **contains a `query`** (text-only attachments return HTTP 400),
then call the query-result endpoint.

### Polling strategy
Poll every **1–5s**, back off exponentially up to **60s**, cap total wait at
**~10 minutes**. Always implement retry-with-backoff; the docs give no explicit
rate limits, so be defensive and log responses.

## Python — the fast path (SDK)

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()  # resolves auth from env/profile — no secrets in code

# start + wait handles polling for you
msg = w.genie.start_conversation_and_wait(space_id=SPACE_ID, content="Top 5 products by revenue last quarter")
print(msg.attachments[0].text.content if msg.attachments else "(no text)")

# follow-up in the same conversation
msg2 = w.genie.create_message_and_wait(
    space_id=SPACE_ID, conversation_id=msg.conversation_id,
    content="Now break that down by region",
)
```
Fetch tabular results with `w.genie.get_message_attachment_query_result(...)`.
See `scripts/genie_sdk_example.py`.

For a dependency-free version, `scripts/genie_conversation.py` implements the
same loop with `requests` and explicit polling.

## Managing spaces programmatically

- List: `GET /api/2.0/genie/spaces`
- Get (full config): `GET /api/2.0/genie/spaces/{space_id}?include_serialized_space=true`
- Create: `POST /api/2.0/genie/spaces` with `serialized_space`, `title`,
  `description`, `warehouse_id`, `parent_path`
- Update: `PUT /api/2.0/genie/spaces/{space_id}` with `serialized_space`

`serialized_space` is a strict JSON string (tables, instructions, example SQL,
join specs, snippets, benchmarks) with **32-char hex IDs**, **sorting**, and
**uniqueness** rules — see `references/serialized-space.md` before generating one.

## Best practices

- **New conversation per session/task** — reusing context across unrelated
  questions reduces accuracy.
- **Prune conversations** to stay under the 10,000/space limit
  (`DELETE .../conversations/{conversation_id}`).
- **Retry with exponential backoff**; **log** responses for debugging and cost.
- Curate the agent well (`skills/working-with-genie/`) — API quality mirrors
  curation quality.

## References

- `references/api-endpoints.md` — every endpoint, path, params, and the
  attachment/response structure.
- `references/serialized-space.md` — full `serialized_space` schema and all
  validation rules (IDs, sorting, uniqueness, size limits).

## Scripts

- `scripts/setup_env.ps1` — set `DATABRICKS_HOST`, `GENIE_SPACE_ID`, and (if
  PAT) `DATABRICKS_TOKEN` as user-scoped env vars via hidden prompts.
- `scripts/genie_conversation.py` — dependency-light REST client with polling,
  backoff, and query-result retrieval.
- `scripts/genie_sdk_example.py` — the same flow via `databricks-sdk`.
