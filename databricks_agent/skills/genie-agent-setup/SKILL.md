---
name: genie-agent-setup
description: Use when a user wants to create, configure, share, clone, or export a Databricks Genie Agent (formerly Genie Space) through the workspace UI — the click-by-click build. Covers prerequisites and permissions, creating the agent, adding/managing Unity Catalog data objects, accepting Genie Code query suggestions, the Settings panel (title, default warehouse, tags, description, common questions), sharing and end-user permissions, cloning, and exporting to a metric view. For concepts/curation strategy use working-with-genie; for programmatic creation use genie-conversation-api.
---

# Set up a Genie Agent

A **Genie Agent** (formerly Genie Space) is the natural-language chat interface
business users use to ask questions of their data. Data analysts configure it
with Unity Catalog data, example SQL, and instructions; end users just chat.

This skill is the **operational build**. For *why* and *how to curate well*,
load `skills/working-with-genie/`.

## Before you start — prerequisites & permissions

To **create or edit** an agent you need:

- **Databricks SQL** workspace entitlement.
- **CAN USE** on at least one **Pro or Serverless SQL warehouse** (Serverless
  recommended).
- **SELECT** on the Unity Catalog data objects you'll add.
- **CAN EDIT** or higher on the agent (creators get **CAN MANAGE**
  automatically).

Hard limits (verify against live docs): **≤30 tables/views** per agent;
**10,000 conversations**; **10,000 messages/conversation**.

## Step-by-step

### 1. Create
1. Click **Genie Agents** in the sidebar.
2. Click **New** (upper-right).
3. Select the data sources to include.
4. Click **Create**.

### 2. Let Genie Code seed context
On creation, **Genie Code launches automatically**, reads your data, and
suggests context (table/column descriptions, example queries). Review and
accept useful suggestions or ask for more. **Verify AI-generated descriptions**
before accepting.

### 3. Review query suggestions
Genie searches workspace query history for queries tied to your data assets. If
found, a notification appears. In the review dialog you can edit question
titles, view full SQL, and accept/reject each. Accepted queries become
**editable example SQL queries** for the agent.

### 4. Manage data objects — Configure ▸ Data
- **Add** tables with the Add button; remove with the trash icon.
- Overview tab shows columns, data types, and descriptions.
- Review **sample data** to confirm context.
- Remember: Genie can query tables beyond those added; **Unity Catalog controls
  access**, not the agent. Add tables for *focus and quality*, not security.

### 5. Configure settings — Configure ▸ Settings

| Setting | What it does |
|---------|--------------|
| **Title** | Shown in the workspace browser; drives discoverability. |
| **Default Warehouse** | Embedded compute credentials that power all queries for all users. |
| **Tags** | Organize/categorize agents (governed tags need ASSIGN permission). |
| **Thumbnail** | Image on the chat landing page. |
| **Description** | Markdown-supported context/references. |
| **Common Questions** | Optional examples on the landing page. Author-defined ones take priority; Genie auto-fills remaining slots. |

### 6. Share / deploy
- **Specific users/groups:** click **Share**, add principals, set permission
  (**CAN MANAGE / CAN EDIT / CAN RUN / CAN VIEW**). Use **Copy link** to share.
  Individuals and small groups get email notifications.
- **All account users:** **Share ▸ All account users**, then set the level.

**End users need:** consumer access or Databricks SQL entitlement; **SELECT**
on all data objects; at least **CAN VIEW/CAN RUN** on the agent. They do **not**
need warehouse permissions (queries use the embedded author credentials), and
their own Unity Catalog grants (incl. row-level security and column masks) are
enforced per user.

## Lifecycle operations

- **Clone:** open agent ▸ kebab (⋯) ▸ **Clone** ▸ optional new name/location ▸
  **Clone**. Copies tables, settings, general instructions, example SQL, and
  SQL functions. **Does not** copy chat threads or monitoring data.
- **Export to metric view:** kebab ▸ **Export to metric view** ▸ pick a path ▸
  (optionally refine with Genie Code) ▸ **Create**.

## After setup

Curate for accuracy (`skills/working-with-genie/`), test with benchmarks, and
automate access (`skills/genie-conversation-api/`).

## References

- `references/setup-walkthrough.md` — full walkthrough with permission matrix,
  sharing details, and lifecycle operations.
- `references/checklist.md` — a copy-paste pre-flight and go-live checklist.
