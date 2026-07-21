# Genie concepts (reference)

Source: https://docs.databricks.com/aws/en/genie/ (captured 2026-07-21).

## What Genie is

Genie is "the Databricks AI experience for users." It lets people ask questions
of their data in natural language, explore AI/BI dashboards, and run Databricks
Apps. Every response is **grounded in organizational data and governed through
Unity Catalog** — Genie is not a general chatbot; it answers from your governed
warehouse.

## The three integrated experiences

### Genie One
- Simplified interface for **business users** to discover and interact with
  data assets.
- Natural-language queries against organizational data.
- Account-level access to assets shared across workspaces.
- Mobile access on iOS and Android.
- Inline suggestions and agentic task capabilities.
- (Free through July 31, 2026 per the captured docs — pricing changes; verify.)

### Genie Code
- AI coding/data assistant for **developers and technical practitioners**.
- Available across notebooks, pipelines, dashboards, and workspace tools.
- Supports custom workspace-level and personal instructions.
- Launches automatically when you create a Genie Agent and suggests context
  (table descriptions, example queries) to improve answer accuracy.
- (Pay-as-you-go billing model per the captured docs, with a monthly free
  allowance — verify current terms.)

### Genie Agents (formerly Genie Spaces)
- Domain-specific environments **configured by data teams**.
- Establish "trusted data, metrics, and business rules that power Genie One
  answers."
- Support dataset configuration, sample queries, and custom instructions.
- Quality tuning via metrics, business rules, and verified answers.

## Terminology note

Databricks renamed **Genie Space → Genie Agent**. Older docs, URLs, API paths
(`/api/2.0/genie/spaces/...`), and SDK methods (`w.genie.*`, `space_id`) still
use "space." Treat "space" and "agent" as the same object when reading the API.

## The governance model (important)

- **Unity Catalog is the source of truth.** Only tables/views registered in
  Unity Catalog can be used, and access is controlled by Unity Catalog — not by
  the Genie Agent itself. Genie can query tables beyond those explicitly added
  to an agent if the user has permission.
- **Embedded author credentials power the warehouse**, so end users don't need
  direct warehouse permissions.
- **Per-user data credentials still apply to every query**, so users see only
  data they're entitled to. Row-level security and column masks defined in
  Unity Catalog are enforced automatically, per user.

Design implication: an agent is a curation/UX layer, not a security boundary.
Never rely on "not adding a table" to hide data, and never try to widen access.

## Admin & cost controls

- Admins get budget and cost-control management for Genie usage.
- Genie Agent events are captured in audit logs (see the AI/BI section of
  account audit logging) for usage tracking and governance.

## Where each experience fits

| Persona | Experience | Typical action |
|---------|------------|----------------|
| Business user | Genie One | Ask a question, read the answer/chart |
| Data analyst / team | Genie Agent | Curate tables, examples, metrics, benchmarks |
| Developer | Genie Code + API | Build, embed, and automate Genie |
