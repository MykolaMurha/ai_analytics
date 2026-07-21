# Genie Agent go-live checklist (reference)

## Pre-flight (before creating)
- [ ] Data objects registered in **Unity Catalog** with **SELECT** granted.
- [ ] A **Pro or Serverless SQL warehouse** exists and you have **CAN USE**.
- [ ] You have **Databricks SQL** entitlement.
- [ ] Scope decided: which **≤5 focused** tables/views (max 30).

## Build
- [ ] Agent created via **Genie Agents ▸ New**.
- [ ] Genie Code suggestions reviewed; **descriptions verified** (not raw AI).
- [ ] Query-history suggestions triaged into **example SQL queries**.
- [ ] Column **synonyms** added for business terms.
- [ ] Business metrics defined as **SQL expressions/measures**.
- [ ] Text instructions kept **minimal, specific, non-conflicting**.

## Settings
- [ ] **Title** clear and discoverable.
- [ ] **Default Warehouse** set (Serverless preferred).
- [ ] **Description** (Markdown) explains scope + caveats.
- [ ] **Common Questions** seeded with 3–5 good starters.
- [ ] **Tags**/**Thumbnail** set if used.

## Quality gate
- [ ] ≥5 **benchmark questions** with expected SQL; agent **scored**.
- [ ] Generated SQL spot-checked for misinterpretation.
- [ ] Complex joins pre-built into **views/metric views**.

## Access
- [ ] Shared with the right users/groups at the **least** sufficient level
      (CAN VIEW/CAN RUN for consumers).
- [ ] End users confirmed to have **SELECT** on all agent data objects.
- [ ] Row-level security / column masks validated with a test user.

## Post-launch
- [ ] **Monitoring** tab reviewed for real questions.
- [ ] Up/down votes triaged; gaps turned into examples/synonyms.
- [ ] Old conversations pruned if approaching the 10,000 limit.
