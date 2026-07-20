# Changed Power BI Dashboard

This folder contains the **Artificial Intelligence Sample** as a Power BI Project (`.pbip`). The project includes both the report definition and its semantic model in source-control-friendly formats.

## Changes made

- Changed blue dashboard colors to corresponding red shades.
- Updated the custom report theme and the Power BI base-theme color properties used by the report.
- Updated explicit visual-level colors in desktop and mobile layouts.
- Preserved existing contrast differences between dark, medium, and bright dashboard elements.
- Left report content, measures, relationships, embedded images, and semantic-model logic unchanged.

The color update affected 90 color occurrences across 14 report and theme files. All report JSON files were parsed successfully after the change.

## Folder contents

- `Artificial Intelligence Sample.pbip` — project entry point.
- `Artificial Intelligence Sample.Report/` — report pages, visuals, layouts, bookmarks, themes, and static resources.
- `Artificial Intelligence Sample.SemanticModel/` — TMDL semantic-model definitions, measures, relationships, and Power Query expressions.

## Tools and prerequisites

- **Microsoft Power BI Desktop for Windows**, using a current release that supports Power BI Project (`.pbip`), PBIR report definitions, and TMDL semantic models.
- **Microsoft Excel source workbook** used by the semantic model. The current Power Query definitions reference:
  `C:\Users\misewell\OneDrive - Microsoft\Documents\GitHub\ContosoBI\Contoso - Generic\Contoso - PowerBI Source Data.xlsx`
- Access to an equivalent copy of that workbook and permission to update the data-source path in Power BI Desktop before refreshing.
- **Git** is optional for opening the dashboard but is needed to track and contribute project-file changes.

## How to use

1. Open `Artificial Intelligence Sample.pbip` in Power BI Desktop.
2. If prompted, open **Data source settings** or **Transform data** and replace the existing Excel workbook path with the location of your local source workbook.
3. Apply the data-source change and refresh the semantic model.
4. Review the report pages in desktop and mobile layouts.
5. Save the project. Power BI Desktop may update project-schema metadata when opened in a newer release, so review those file changes before committing them.
