# AI Analytics Demo - Day 1 Summary

This repository now contains the main artifacts produced during the first demo session.

## Results

- Added four AI/data-analysis course presentation decks (`part_1` through `part_4`).
- Added the **Artificial Intelligence Sample** as a source-controlled Power BI Project under `changed presentation/`.
- Changed the dashboard's blue visual treatment to red across the custom theme, base-theme properties, desktop visuals, and mobile layouts.
- Updated 90 color occurrences in 14 Power BI report/theme files while preserving report content, semantic-model logic, bookmarks, and images.
- Added `AGENTS.md` and `CLAUDE.md` with repository structure, working rules, validation guidance, and onboarding context.

## Validation completed

- Verified that the copied PBIP project matched its source files by SHA-256.
- Parsed all 299 report JSON files successfully.
- Confirmed that theme color arrays contain no empty color values.
- Kept Power BI local/session settings excluded through the nested `.gitignore`.

## Opening the dashboard

Use a current version of Microsoft Power BI Desktop for Windows and open:

`changed presentation/Artificial Intelligence Sample.pbip`

The semantic model expects `Contoso - PowerBI Source Data.xlsx` from a machine-specific path. Obtain an equivalent workbook and update the path through **Data source settings** or **Transform data** before refreshing.

For detailed setup and maintenance instructions, see:

- `changed presentation/README.md`
- `AGENTS.md`
- `CLAUDE.md`

## Session commits

- `9a95ea1` - presentations added.
- `0e9dc83` - changed Power BI dashboard added.
- `9162cb2` - agent onboarding documentation added.
