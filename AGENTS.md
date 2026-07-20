# AGENTS.md

## Purpose

This repository contains AI/data-analysis course presentations and a source-controlled Power BI Project. Treat the Power BI Project (`.pbip`) as a structured source tree, not as a single opaque dashboard file.

Read this file before changing repository content. Keep work scoped to the requested artifact and preserve unrelated files and user changes.

## Agent runtime and communication

- Re-read this `AGENTS.md` for every project task or chat, including work delegated by another agent.
- Unless a direct request specifies a different model, agents should run with GPT-5.5 and Extra High Intelligence.
- Submit acknowledgements and other notification-style updates may use a short, lightly playful voice when appropriate.
- Keep technical status, warnings, approvals, errors, review findings, and user decisions clear first; personality is secondary to precision.

## Repository layout

- `part_1_dataart_ai_data_analysis.pptx`
- `part_2_dataart_ai_data_analysis.pptx`
- `part_3_dataart_ai_data_analysis.pptx`
- `part_4_dataart_ai_data_analysis.pptx`
  - Binary course-presentation files stored at the repository root.
- `changed presentation/`
  - `Artificial Intelligence Sample.pbip` — Power BI project entry point.
  - `Artificial Intelligence Sample.Report/` — PBIR report definition, pages, visuals, bookmarks, themes, and static resources.
  - `Artificial Intelligence Sample.SemanticModel/` — TMDL semantic model, measures, relationships, and Power Query expressions.
  - `README.md` — end-user instructions, change summary, prerequisites, and refresh guidance.
  - `.gitignore` — excludes Power BI local/session settings that should not be committed.

The report points to the semantic model by the relative path `../Artificial Intelligence Sample.SemanticModel`. Do not flatten, rename, or separate these folders without updating and validating that reference.

## Known dashboard state

The dashboard is the **Artificial Intelligence Sample**. Its visual color treatment was changed from blue to red before it was added to this repository.

- 90 blue-hued color occurrences were changed across 14 report/theme files.
- Changes cover the registered custom theme, Power BI base-theme properties, explicit desktop visual colors, and mobile-layout visual colors.
- The registered custom theme is `Artificial Intelligence Sample.Report/StaticResources/RegisteredResources/Fidex5865093615527226.json`.
- The base theme is `Artificial Intelligence Sample.Report/StaticResources/SharedResources/BaseThemes/CY21SU04.json`.
- Dark, medium, and bright shades were retained as red variants to preserve hierarchy and contrast.
- Report content, measures, relationships, Power Query logic, bookmarks, embedded images, and other semantic-model behavior were not intentionally changed.
- The custom theme contains 480 non-empty `dataColors` values. Base-theme color values are also non-empty.
- In the Q&A visual `8fa132f0492cab00a1b8`, `savedUtterance` is intentionally empty. Its `cardBackground` is red (`#BF0000`). Do not treat the empty saved query as a missing color.
- Image or icon names that contain color words are labels, not necessarily editable dashboard color properties. Embedded and remotely referenced images were not recolored.

All 299 JSON files in the report source parsed successfully after the color update. The copied dashboard was also hash-checked against its source before it was committed.

## Data-source dependency

The semantic model reads an Excel workbook through Power Query. Several TMDL tables currently reference this machine-specific path:

`C:\Users\misewell\OneDrive - Microsoft\Documents\GitHub\ContosoBI\Contoso - Generic\Contoso - PowerBI Source Data.xlsx`

The affected model includes Excel-backed queries for Accounts, Campaigns, Cases, Contacts, Industries, Opportunities, Owners, Products, and Territories.

Opening the report does not guarantee that refresh will succeed. To refresh:

1. Obtain an equivalent `Contoso - PowerBI Source Data.xlsx` workbook.
2. Open `changed presentation/Artificial Intelligence Sample.pbip` in Power BI Desktop.
3. Use **Data source settings** or **Transform data** to replace the stored workbook path.
4. Apply the change and refresh the model.

Do not silently replace the source path with another developer's absolute path. Prefer a deliberate, documented data-source change.

## Required tools

- Microsoft Power BI Desktop for Windows, using a current release that supports `.pbip`, PBIR report definitions, and TMDL semantic models.
- The referenced Excel source workbook, or an equivalent compatible workbook, for data refresh.
- Git for reviewing and contributing source changes.
- PowerShell is suitable for read-only validation of JSON and repository state.

Power BI Desktop may migrate schema metadata when a project is opened with a newer release. Review those generated changes before committing them.

## Editing rules

### Power BI Project

- Preserve the `.pbip`, `.Report`, and `.SemanticModel` relationship and relative paths.
- Keep local Power BI files excluded by the nested `.gitignore`; do not force-add ignored `.pbi/localSettings.json` files.
- Edit report/theme color properties as exact JSON values. Do not use a broad text replacement that can alter queries, labels, IDs, URLs, or intentionally empty strings.
- When changing colors, inspect the custom theme, base theme, explicit visual properties, and mobile layouts. Theme-only changes may not override hard-coded visual colors.
- Do not recolor raster images or remote icon assets unless the request explicitly includes image editing.
- Preserve TMDL formatting and existing whitespace. `git diff --check` reports inherited trailing whitespace and blank lines in several TMDL files; do not normalize unrelated model files as incidental cleanup.
- Avoid wholesale JSON reserialization. It creates noisy diffs and can change formatting or metadata ordering.

### Presentations

- Treat `.pptx` files as binary artifacts.
- Do not attempt text-based edits or line-oriented merges.
- After copying or replacing a presentation, verify its filename, size, and preferably SHA-256 hash.

### General Git hygiene

- `main` tracks `origin/main`.
- Inspect `git status --short --branch` before and after work.
- Stage only the files required by the task; verify the staged path list before committing.
- Preserve unrelated changes in a dirty worktree.
- Do not commit Power BI local/session state.
- Do not push unless the task explicitly requests it.

## Validation checklist

For Power BI source changes:

1. Confirm `Artificial Intelligence Sample.pbip` still points to `Artificial Intelligence Sample.Report`.
2. Confirm `definition.pbir` still points to `../Artificial Intelligence Sample.SemanticModel`.
3. Parse all changed JSON files; no parse error is acceptable.
4. Check theme `dataColors` arrays and color properties for empty values introduced accidentally.
5. Distinguish intentionally empty non-color properties, especially the Q&A `savedUtterance`, from invalid color values.
6. Review desktop and mobile visual definitions.
7. Open the `.pbip` project in Power BI Desktop for final visual/refresh validation when Power BI Desktop and the source workbook are available.
8. Review `git diff` and the staged file list for scope.

Example JSON parse check in PowerShell:

```powershell
$report = 'changed presentation\Artificial Intelligence Sample.Report'
$errors = @()
Get-ChildItem -LiteralPath $report -File -Recurse -Filter *.json | ForEach-Object {
    try {
        $null = Get-Content -Raw -LiteralPath $_.FullName | ConvertFrom-Json
    }
    catch {
        $errors += $_.FullName
    }
}
if ($errors.Count -gt 0) {
    $errors
    throw "Power BI JSON validation failed."
}
```

There is no repository-wide automated test suite currently documented. Structural JSON checks and Power BI Desktop validation are the relevant verification routes for the dashboard.

## Session provenance

- `9a95ea1` — added the four course presentations with commit message `ai-commited presentations`.
- `0e9dc83` — added the changed PBIP dashboard and its README with commit message `power bi dashboard changed by codex`.

These hashes document how the current artifacts entered the repository; do not depend on them as permanent branch tips.
