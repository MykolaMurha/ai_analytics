# CLAUDE.md

## Start here

Read `AGENTS.md` again for every task or chat before working in this repository, including delegated work. It is the authoritative operating guide. This file provides a Claude-oriented onboarding summary and does not override `AGENTS.md`.

Unless a direct request specifies another model, agents are expected to use GPT-5.5 with Extra High Intelligence. Notification-style updates can be lightly playful, but technical status, warnings, approvals, errors, review findings, and user decisions must stay unambiguous.

## Project at a glance

The repository contains four binary AI/data-analysis course decks at the root and a source-controlled Power BI Project under `changed presentation/`.

Open the dashboard through:

`changed presentation/Artificial Intelligence Sample.pbip`

The project depends on two adjacent directories:

- `Artificial Intelligence Sample.Report/` — PBIR report source.
- `Artificial Intelligence Sample.SemanticModel/` — TMDL semantic model source.

The report's `definition.pbir` references the model through `../Artificial Intelligence Sample.SemanticModel`. Preserve this relative structure.

## Current dashboard behavior

The dashboard was deliberately converted from a blue treatment to a red treatment:

- 90 blue-hued color occurrences were updated in 14 files.
- The change covers the registered `Fidex5865093615527226.json` theme, the `CY21SU04.json` base theme, explicit desktop visual settings, and mobile-layout settings.
- Shade differences were retained to preserve contrast and hierarchy.
- The custom theme has 480 non-empty `dataColors` entries.
- Embedded images and remotely referenced icons were not recolored.
- Measures, relationships, Power Query logic, bookmarks, report content, and semantic-model behavior were not intentionally changed.
- All 299 report JSON files parsed after the change, and the repository copy matched its source by SHA-256.

Important exception: the Q&A visual `8fa132f0492cab00a1b8` intentionally has an empty `savedUtterance`. Its `cardBackground` is `#BF0000`. Never "repair" that empty saved query as if it were a color.

## Refresh dependency

Nine Excel-backed queries currently point to:

`C:\Users\misewell\OneDrive - Microsoft\Documents\GitHub\ContosoBI\Contoso - Generic\Contoso - PowerBI Source Data.xlsx`

The affected subject tables are Accounts, Campaigns, Cases, Contacts, Industries, Opportunities, Owners, Products, and Territories. A user needs an equivalent workbook and must update the path through Power BI Desktop's **Data source settings** or **Transform data** before refresh. Do not replace it silently with a new machine-specific path.

## Working rules

- Use a current Power BI Desktop for Windows with `.pbip`, PBIR, and TMDL support.
- Treat the `.pptx` files as binary artifacts; verify copied files by size/hash.
- Keep `.Report` and `.SemanticModel` adjacent to the `.pbip` entry point.
- Respect `changed presentation/.gitignore`; never force-add `.pbi/localSettings.json` or other local/session state.
- Avoid broad replacements and wholesale JSON serialization.
- A theme-only edit is insufficient when a visual has an explicit color override; inspect desktop and mobile definitions.
- Do not modify images merely because their names mention a color.
- Preserve existing TMDL whitespace. `git diff --check` can report inherited whitespace; do not turn that into unrelated cleanup.
- Power BI Desktop may generate schema upgrades. Review generated diffs before committing.
- Preserve unrelated worktree changes, stage narrowly, and push only when explicitly requested.

## Verification before handoff

1. Check `.pbip` and `.pbir` relative references.
2. Parse every changed JSON file.
3. Ensure theme/color values are non-empty while preserving intentionally empty non-color fields.
4. Review both desktop and mobile visual definitions.
5. Run `git status --short --branch` and inspect the staged file list.
6. When available, open the project in Power BI Desktop, update the Excel source path, refresh, and visually inspect the report.

No automated repository-wide test suite is documented. JSON validation plus Power BI Desktop review are the primary checks.

## Artifact history

- `9a95ea1` introduced the four presentations (`ai-commited presentations`).
- `0e9dc83` introduced the PBIP dashboard and dashboard README (`power bi dashboard changed by codex`).

Commit hashes are provenance only and may not remain branch tips.
