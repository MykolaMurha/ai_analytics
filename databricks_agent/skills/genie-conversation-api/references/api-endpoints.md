# Genie Conversation API — endpoints (reference)

Source: https://docs.databricks.com/aws/en/genie-agents/conversation-api and
the Genie REST reference https://docs.databricks.com/api/workspace/genie
(captured 2026-07-21). All paths are versioned `/api/2.0/genie/...`. "Space" ==
"Agent".

## Authentication

- Header: `Authorization: Bearer <token>`.
- **OAuth U2M** — interactive/browser, for production with active users.
- **OAuth M2M** — service principal (no browser), for automation. The principal
  needs permissions on the target data and SQL warehouse.
- **PAT** — personal access token.

## Conversation endpoints

### Start a conversation
`POST /api/2.0/genie/spaces/{space_id}/start-conversation`
```json
{ "content": "<question>", "enable_visualization": true }
```
`enable_visualization` is optional (Beta). Response includes `conversation_id`
and `message_id`.

### Get a message (poll this)
`GET /api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}`
Returns status and `attachments`. Documented status flow:
`IN_PROGRESS → PENDING_WAREHOUSE → EXECUTING_QUERY → COMPLETED`
(or `FAILED` / `CANCELLED`).

**Observed in practice (2026-07-21):** the API emits more granular
intermediate states than the docs list — e.g. `FETCHING_METADATA`,
`FILTERING_CONTEXT`, `ASKING_AI`, `PENDING_WAREHOUSE` — and may repeat or
reorder them. Do **not** hard-code the intermediate sequence. Treat any status
not in the terminal set (`COMPLETED` / `FAILED` / `CANCELLED`) as "keep
polling."

### Create a follow-up message (multi-turn)
`POST /api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages`
```json
{ "content": "<follow-up question>" }
```
Retains context from previous messages in the conversation.

### Get query results (tabular)
`GET /api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}/attachments/{attachment_id}/query-result`
Returns the result set from the generated SQL.

### Get visualization results (Beta)
`GET /api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}/attachments/{attachment_id}/download-visualization`
Not supported on Private Link workspaces.

### Message comments
- Create: `POST .../messages/{message_id}/comments` — `{ "content": "<text>" }`
- List:   `GET  .../messages/{message_id}/comments`

## Conversation management

- List conversations: `GET /api/2.0/genie/spaces/{space_id}/conversations`
  (`include_all=true` requires CAN MANAGE; returns all users' conversations).
- List messages in a thread:
  `GET /api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages`
- Delete a conversation:
  `DELETE /api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}`
  (prune to stay under the 10,000-conversation limit).

## Space (agent) management

- List spaces: `GET /api/2.0/genie/spaces` (returns `space_id`s).
- Get space: `GET /api/2.0/genie/spaces/{space_id}?include_serialized_space=true`
  (`include_serialized_space` returns full config; Beta).
- Create space: `POST /api/2.0/genie/spaces`
  ```json
  {
    "serialized_space": "<JSON string>",
    "title": "...",
    "description": "...",
    "warehouse_id": "...",
    "parent_path": "..."
  }
  ```
- Update space: `PUT /api/2.0/genie/spaces/{space_id}` (via `serialized_space`).

## Attachment / response structure

`attachments` is an array; each item may contain:
- `text` — natural-language response (`text.content`).
- `query` — generated SQL statement.
  - `query.parameters` — present when the answer came from a **trusted asset**.
- `attachment_id` — reference used to fetch the query result.
- `query_attachments` — `GenieQueryAttachments` with step-by-step reasoning
  traces.
- `viz` — `GenieVizAttachment` (only when `enable_visualization: true`).

### Retrieval pattern
1. Poll the message until status is **PENDING_WAREHOUSE** or later.
2. Extract `attachment_id` from an attachment that **contains a `query`**.
3. Call the **query-result** endpoint with that `attachment_id`.

> A message can have multiple attachments (e.g. a SQL/query attachment plus a
> separate text attachment). Only **SQL-bearing** attachments have results —
> calling the query-result endpoint for a text-only attachment_id returns
> **HTTP 400**. Verified against the "Bakehouse Sales Starter Space" sample.

## Polling & resilience

- Poll every **1–5s**; exponential backoff to a **60s** max; cap total at
  **~10 min**.
- Stop on **COMPLETED / FAILED / CANCELLED**.
- No documented hard rate limits → implement retry-with-backoff and log all
  responses for debugging and cost tracking.

## `databricks-sdk` equivalents

```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()

w.genie.start_conversation(space_id=..., content=...)
w.genie.start_conversation_and_wait(space_id=..., content=...)   # polls for you
w.genie.create_message(space_id=..., conversation_id=..., content=...)
w.genie.create_message_and_wait(space_id=..., conversation_id=..., content=...)
w.genie.get_message(space_id=..., conversation_id=..., message_id=...)
w.genie.get_message_attachment_query_result(
    space_id=..., conversation_id=..., message_id=..., attachment_id=...)
w.genie.list_spaces()
w.genie.get_space(space_id=..., include_serialized_space=True)
```
