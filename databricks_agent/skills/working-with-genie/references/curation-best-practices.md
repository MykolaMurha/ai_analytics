# Curating an effective Genie Agent (reference)

Source: https://docs.databricks.com/aws/en/genie-agents/best-practices
(captured 2026-07-21), plus the "tune quality" guidance.

The goal: maximize the share of questions Genie answers **correctly and
consistently**. Accuracy comes from curated context, tested with benchmarks,
refined from real usage.

## 1. Table & column metadata

- **Quality descriptions in Unity Catalog are foundational and critical.** Use
  clear, precise, unambiguous column names and descriptions.
- **Verify AI-generated descriptions** before accepting them — they are a
  starting point, not ground truth.
- Add **synonyms** and custom metadata scoped to the agent so Genie recognizes
  related business terms (e.g. "revenue" ≈ "sales", "net_amount") and maps user
  phrasing to the correct fields.
- Enable **prompt/value matching** (Genie provides this) so it can match column
  values and correct spelling in user prompts.

## 2. Example SQL queries — your strongest lever

- Example SQL is more reliable and maintainable than plain-text instructions
  for defining query patterns. **Prefer structure over prose.**
- Use examples to teach Genie **complex, multi-part, or ambiguous** patterns —
  not trivial single-table selects it can already handle.
- Prioritize:
  - Hard-to-interpret, multi-step business scenarios.
  - Common ambiguous prompts users actually ask.
  - Real questions that need specialized joins or logic.
- A well-curated agent typically has **at least ~5 example SQL queries** and
  grows them from observed usage. (Guidance emphasizes strategic coverage over
  a hard count.)

## 3. General (text) instructions — use sparingly

Keep instructions **limited and focused**. Too many instructions reduce
effectiveness because Genie struggles to prioritize them in longer
conversations.

**Three-tiered approach (best → last resort):**
1. **SQL expressions / measures** for business metrics (revenue,
   active_customers) — define once, reuse everywhere.
2. **Example SQL** for complex multi-step questions.
3. **Text instructions only as a last resort**, for guidance that genuinely
   needs natural-language explanation.

**Be specific.** Avoid vague rules like "ask clarifying questions when needed."
Instead specify: the triggering condition, the missing detail, the required
action, and an example clarification.

**Avoid conflicts.** Ensure instructions, examples, and expressions don't
contradict each other.

## 4. Benchmarks & verified answers

- Convert reviewed questions into **benchmark questions** (question + expected
  SQL) to **test and score the agent's overall accuracy systematically.**
- Test **variations and different phrasings** of the same intent to measure
  reliability.
- Integrate **user feedback**: business users upvote correct answers and
  downvote errors; use votes to find gaps and refine instructions.
- **Benchmark before shipping** and re-run after changes to catch regressions.

## 5. Common pitfalls

- **Over-scoping** — include only necessary tables. Aim for **≤5**; hard max is
  **30**. More tables = more ambiguity.
- **Conflicting guidance** across instruction types.
- **Trusting AI-generated metadata** without verification.
- **Too many text instructions** — they dilute effectiveness.
- **Ignored context** — dashboard filters do **not** carry over when you link
  an existing agent to a dashboard.

## 6. Troubleshooting workflow

- **Start small and iterate** — minimal setup first, expand from real feedback.
- **Domain expertise required** — have SQL-proficient analysts define the agent;
  they understand both the data and the business questions.
- **Monitor real usage** — the Monitoring tab shows the actual questions users
  ask; curate toward them.
- **Examine generated SQL** — read Genie's SQL output for misinterpretations,
  then fix with a synonym, expression, or example.
- **Pre-join complexity** — build views/metric views to simplify multi-table
  relationships before adding them to the agent.

## Quick curation checklist

- [ ] ≤5 focused, well-described Unity Catalog tables/views (max 30)
- [ ] Column descriptions + synonyms verified (not raw AI output)
- [ ] Business metrics defined as SQL expressions/measures
- [ ] ≥5 example SQL queries covering complex/ambiguous patterns
- [ ] Text instructions minimal, specific, non-conflicting
- [ ] ≥5 benchmark questions with expected SQL; agent scored
- [ ] Monitoring reviewed; up/down votes triaged
