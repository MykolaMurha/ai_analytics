---
name: working-with-genie
description: Use when a user asks what Databricks AI/BI Genie is, which Genie experience (Genie One, Genie Code, or Genie Agents) fits their need, how natural-language answers stay governed by Unity Catalog, or how to curate and tune a Genie experience so its generated SQL is accurate and trusted. Covers concepts, trusted assets, and curation/quality best practices — not the click-by-click build (see genie-agent-setup) or the programmatic API (see genie-conversation-api).
---

# Working with Databricks AI/BI Genie

Genie is the Databricks AI experience that lets business users ask questions of
their data in **natural language** and get answers **grounded in
organizational data and governed by Unity Catalog**. This skill covers the
concepts and the curation/quality work that make Genie answers trustworthy.

## The three Genie experiences

Pick the right one before diving in:

- **Genie One** — the simplified natural-language chat surface for business
  users (web + iOS/Android). It answers using the trusted assets that data
  teams configure. Account-level access to shared assets.
- **Genie Code** — the AI coding/data assistant for technical users inside
  notebooks, pipelines, dashboards, and workspace tools. It also assists when
  configuring a Genie Agent (suggests table descriptions and example queries).
- **Genie Agents** — the domain-specific environments that data teams curate
  (trusted data, metrics, business rules, example SQL) which power Genie One
  answers. **"Genie Agent" was formerly called "Genie Space."**

Rule of thumb: business users consume **Genie One**; data teams build **Genie
Agents**; developers use **Genie Code** and the API.

## How answers stay governed

- Data must be in **Unity Catalog**. Genie only ever returns data the querying
  user is permitted to see.
- Queries in a shared agent run with the author's embedded warehouse
  credentials, **but each end user's own data credentials are applied** — so
  **row-level security and column masks are enforced per user**.
- Never design a Genie flow that tries to widen access beyond a user's Unity
  Catalog grants. That is a governance violation, not a feature request.

## Trusted assets — what you curate

An agent's accuracy comes from curated context, not raw tables alone:

- **Table & column metadata** — descriptions and **synonyms** so Genie maps
  business terms to the right fields.
- **Example SQL queries** — the single most powerful lever for teaching Genie
  how to answer complex, multi-part, or ambiguous questions.
- **SQL expressions / measures** — reusable business-metric definitions
  (revenue, active_customers) so metrics are computed consistently.
- **General (text) instructions** — natural-language guidance, used sparingly
  and as a last resort.
- **Benchmarks & verified answers** — question/expected-SQL pairs used to score
  the agent systematically and to lock in known-good answers.

## Curation & quality — the short version

1. **Start small and iterate.** Begin with ≤5 well-annotated tables; expand
   based on real usage in the Monitoring tab.
2. **Prefer structure over prose.** SQL examples and expressions beat text
   instructions; keep text instructions few and specific.
3. **Verify AI-generated metadata** before trusting it.
4. **Pre-join complexity** into views/metric views instead of piling raw tables
   into one agent.
5. **Benchmark before you ship**, and use up/down votes to find gaps.

Full detail — including how to write descriptions, how many examples to add,
the three-tiered instruction approach, common pitfalls, and troubleshooting —
is in the reference files.

## Key limits (verify against live docs)

- Up to **30 tables/views** per agent (aim for ≤5 for focus).
- Requires a **Pro or Serverless SQL warehouse** (Serverless recommended).
- Up to **10,000 conversations** per agent and **10,000 messages** per
  conversation.

## References

- `references/genie-concepts.md` — the three experiences, trusted assets, the
  governance model, and terminology, in depth.
- `references/curation-best-practices.md` — writing descriptions/synonyms,
  example-SQL strategy, the three-tiered instruction approach, benchmarks,
  pitfalls, and troubleshooting.

## Related skills

- Build one: `skills/genie-agent-setup/`
- Automate it: `skills/genie-conversation-api/`
