# Databricks Analytics Specialist

A portable **agent bundle** that turns a general assistant into a Databricks
specialist for the natural-language analytics stack: **AI/BI Genie**, **Genie
Agents**, the **Genie Conversation API**, and **Databricks Connect for
Python**.

## What's inside

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Authoritative operating guide (identity, skills, safety, rules). |
| `CLAUDE.md` | Short Claude-oriented onboarding pointer to `AGENTS.md`. |
| `skills/` | One folder per skill; each holds a `SKILL.md` plus `references/` and `scripts/`. |

### Skills

- **`working-with-genie`** — What Genie is (Genie One / Code / Agents), how
  answers stay governed by Unity Catalog, and how to curate and tune a Genie
  experience for accuracy.
- **`genie-agent-setup`** — Step-by-step creation and configuration of a Genie
  Agent: data objects, settings, permissions, sharing, cloning, export.
- **`databricks-connect-python`** — Install and configure Databricks Connect,
  then run Spark/DataFrame code from a local IDE or app against serverless or
  cluster compute. Includes runnable scripts.
- **`genie-conversation-api`** — Drive Genie programmatically over REST or the
  `databricks-sdk`: ask questions, poll to completion, fetch SQL results, and
  manage spaces. Includes a REST client and an SDK example.

## How to use it

1. Point your agent at this folder and have it read `AGENTS.md`.
2. When a task matches a skill, the agent loads that skill's `SKILL.md` and
   pulls in `references/`/`scripts/` as needed.
3. For anything requiring Databricks credentials, run the PowerShell script in
   the relevant skill's `scripts/` folder to set **your own** environment
   variables. **No secrets are stored in this bundle.**

## Prerequisites

- A Databricks workspace with **Unity Catalog** and a **Pro or Serverless SQL
  warehouse**.
- Python 3.10+ in a dedicated virtual environment.
- Optional: the Databricks CLI (`databricks auth login`) and `databricks-sdk`.

## Safety

This bundle **never** contains tokens, secrets, or `.databrickscfg` contents.
Credentials are supplied by the user into their own environment via hidden
prompts in the provided PowerShell scripts, and are referenced in code only by
variable name. See the "Safety and credentials" section of `AGENTS.md`.

## Provenance

Skill content is derived from the official Databricks documentation captured on
2026-07-21. See the "Sources" section of `AGENTS.md` for canonical links.
