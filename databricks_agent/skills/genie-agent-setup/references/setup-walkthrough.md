# Genie Agent setup — full walkthrough (reference)

Source: https://docs.databricks.com/aws/en/genie-agents/set-up
(captured 2026-07-21).

## Requirements & limits

- **Unity Catalog:** all data must be registered. **Max 30 tables/views** per
  agent.
- **Compute:** a **Pro or Serverless SQL warehouse** (Serverless recommended
  for performance).
- **Capacity:** up to **10,000 conversations** per agent; up to **10,000
  messages** per conversation.

## Permission matrix

### To create / edit an agent
| Requirement | Detail |
|-------------|--------|
| Entitlement | Databricks SQL |
| Compute | **CAN USE** on ≥1 Pro/Serverless SQL warehouse |
| Data | **SELECT** on the Unity Catalog objects |
| Agent ACL | **CAN EDIT** minimum (creator gets **CAN MANAGE**) |

### Agent ACL levels (for sharing)
`CAN MANAGE` > `CAN EDIT` > `CAN RUN` > `CAN VIEW`.

### For an end user to use the agent
- Consumer access **or** Databricks SQL entitlement.
- **SELECT** on **all** data objects in the agent.
- At least **CAN VIEW / CAN RUN** on the agent.
- **No** direct warehouse permission needed — queries use the embedded author
  credentials.

## Detailed steps

### 1. Create
`Genie Agents` (sidebar) → **New** (upper-right) → select data sources →
**Create**.

### 2. Genie Code seeds context
Launches automatically on creation. Reads your data and suggests descriptions
and example queries. Accept, edit, or request more. Always verify AI-generated
descriptions.

### 3. Query suggestions from history
Genie scans workspace query history for queries associated with your assets. A
notification appears if any are found. In the review dialog:
- Edit the question title.
- View the complete SQL text.
- Accept or reject each suggestion.
- Access queries via the Query History UI (with permission).

Accepted queries become **editable example SQL queries**.

### 4. Data objects — Configure ▸ Data
- **Add** button to add tables/views; trash icon to remove.
- **Overview** tab: columns, data types, descriptions.
- **Sample data** to understand content/context.
- Governance reminder: **"Genie can query tables beyond those explicitly added
  to an agent. Access is controlled by Unity Catalog permissions, not by the
  Genie Agent itself."**

### 5. Settings — Configure ▸ Settings
- **Title** — workspace-browser discoverability.
- **Default Warehouse** — embedded credentials powering all users' queries.
- **Tags** — categorization; governed tags require **ASSIGN**.
- **Thumbnail** — chat landing-page image.
- **Description** — Markdown; context and references.
- **Common Questions** — landing-page examples. Author-defined take priority;
  Genie auto-generates the rest to fill slots.

### 6. Share
- **Specific users/groups:** **Share** → enter principals → set level → optional
  **Copy link**. Individuals/small groups get email notifications.
- **All account users:** **Share** → **All account users** → set level.

**Security note (verbatim intent):** all queries run with the embedded compute
credentials, **but each end user's own data credentials are applied**, so users
see only permitted data. Unity Catalog row-level security and column masks are
enforced automatically per user.

## Lifecycle operations

### Clone
Open agent → kebab (⋯) → **Clone** → optionally set new name/workspace location
→ **Clone**.
- **Copied:** tables, settings, general instructions, example SQL queries, SQL
  functions.
- **Not copied:** chat threads, monitoring data.

### Export to metric view
Open agent → kebab → **Export to metric view** → choose a path → optionally
refine the definition with Genie Code → **Create**.

## Related documentation (swap `/aws/` for your cloud)

- Curate an effective Genie Agent — `/aws/en/genie-agents/best-practices`
- Tune Genie Agent quality — `/aws/en/genie-agents/tune-quality`
- Test and monitor a Genie Agent — `/aws/en/genie-agents/monitor`
- Genie Agent events (audit logs) — `/aws/en/admin/account-settings/audit-logs#ai-bi`
- Use the Genie Agents API — `/aws/en/genie-agents/conversation-api`
- Genie API reference — https://docs.databricks.com/api/workspace/genie
- Use Genie in multi-agent systems — `/aws/en/agents/agent-framework/multi-agent-genie`
