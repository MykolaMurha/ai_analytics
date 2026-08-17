# Financial Sample — Power BI Project (PBIP)

Built from `fin_sample_analysis_result.md` (design concept) and `Financial Sample.csv` (source data).

## Open it

```bash
start "" "C:\courses\ai_analytics\datasets\dashboard\FinancialSample.pbip"
```

Requires **Power BI Desktop** with *File → Options → Preview features → Power BI Project (.pbip) save option* enabled (default on in current builds). Detected at `C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe`.

On first open the model refreshes from the CSV — expect a "Native database query / file access" permission prompt; approve it.

## Layout

```
FinancialSample.pbip                  project entry point
FinancialSample.SemanticModel/        TMDL model (data + DAX)
  definition/model.tmdl               model props, auto date/time disabled
  definition/expressions.tmdl         CsvPath parameter
  definition/relationships.tmdl       5 star-schema relationships
  definition/tables/*.tmdl            7 tables
  definition/cultures/en-US.tmdl      linguistic metadata
FinancialSample.Report/               PBIR report (3 pages, 29 visuals)
  definition/version.json             PBIR definition version (required — 1.0.0)
  definition/report.json              theme + layout options
  definition/pages/pages.json         page order
  definition/pages/<Page>/visuals/<Visual>/visual.json
```

## Changing the data source

The CSV path is a **Power Query parameter**, not a hardcoded step. Change it in one of two places:

- Power BI Desktop → *Transform data → Manage parameters → CsvPath*
- or edit `FinancialSample.SemanticModel/definition/expressions.tmdl`

Current value: `C:\courses\ai_analytics\datasets\Financial Sample.csv`

## Model (star schema)

| Table | Type | Notes |
|---|---|---|
| `SourceData` | shared M expression | all CSV cleaning happens once, here; not loaded as a table |
| `Financials` | M — `SourceData` | 700 rows, fact |
| `Dim_Segment` / `Dim_Country` / `Dim_Product` | M — `Table.Distinct` over `SourceData` | sorted alphabetically |
| `Dim_DiscountBand` | M — distinct + derived `Band Order` | hidden `Band Order` sorts bands None → Low → Medium → High |
| `Dim_Date` | DAX calculated | `CALENDAR(2013-09-01, 2014-12-31)`, marked as date table (`dataCategory: Time` + `isKey`) |
| `Dim_Bridge` | DAX `DATATABLE` | **disconnected** — drives the waterfall bridge |

All relationships are many-to-one, single-direction, dim → fact.

### Why the dimensions are built in Power Query, not DAX

The obvious way to write these dimensions is `DISTINCT(Financials[Segment])` as a DAX calculated
table. **Power BI Desktop rejects that here.** A calculated table derived from `Financials` that is
then related back to `Financials` fails to load with:

> Relationship '…' uses an invalid column ID *n*.

`Dim_Date` stays a calculated table because its `CALENDAR(...)` expression has hard-coded bounds and
therefore does not reference `Financials` — no dependency, no error. That is also why the date range
is literal rather than derived from `MIN`/`MAX` of the fact: making it dynamic would reintroduce the
dependency and break the model. **Extend the `CALENDAR(DATE(2013, 9, 1), DATE(2014, 12, 31))` bounds
by hand if the source data ever covers a wider period.**

Building the dimensions in M avoids the dependency entirely and is the more conventional modelling
choice anyway — dimensions come from the source, not from the fact table.

### Power Query cleanup applied

Implements every step from section 1 of the analysis brief:

1. `Table.TransformColumnNames(_, Text.Trim)` — fixes ` Product `, ` Sales `, ` Month Name `
2. Money columns: strip `$`, `,`, spaces → `Number.FromText(_, "en-US")`. Handles the `-$7,590.00` leading-minus negatives present in the file.
3. `Text.Trim` on Segment / Country / Product / Discount Band
4. `Date` parsed with explicit `"en-US"` culture (source is `M/D/YYYY`)
5. `Year`, `Month Number`, `Month Name` dropped from the fact — Dim_Date supplies them
6. `Units Sold` kept as **decimal**, not integer — the source contains fractional units (e.g. `1618.5`); rounding would corrupt totals

## Measures (19, all on `Financials`)

| Measure | Purpose |
|---|---|
| `Net Sales`, `Total Gross Sales`, `Total Discounts`, `Total COGS`, `Total Profit`, `Total Units`, `Transactions` | base sums |
| `Profit Margin %` | `DIVIDE([Total Profit], [Net Sales])` |
| `Discount Rate %` | `DIVIDE([Total Discounts], [Total Gross Sales])` |
| `COGS Ratio %` | exposes the Enterprise >100% problem |
| `Profit per Unit`, `Avg Transaction Size` | unit economics |
| `Loss Making Txns`, `Loss Amount` | isolate the 58 negative-profit rows |
| `Sales MoM %`, `Sales Rolling 3M` | time trend — used instead of YoY (see caveat) |
| `Profit Share %`, `Sales Share %` | contribution vs. `ALLSELECTED()` |
| `Bridge Value` | `SWITCH` over `Dim_Bridge[Step]`, negating Discounts and COGS |

Measure names deliberately differ from column names (`Net Sales` vs the `Sales` column) — Power BI forbids collisions inside one table.

## Pages

**1 — Executive Overview.** Left filter rail (Segment, Country, Product, Discount Band, Date) · 5 KPI cards · combo chart Net Sales column + Profit Margin % line by month · profit bridge waterfall · Profit by Segment · Net Sales by Country · Margin % by Discount Band.

**2 — Profitability Deep Dive.** Matrix Segment × Discount Band (Profit + Margin %) · scatter Revenue vs Margin % sized by units · loss-combination table · loss count/amount cards · Profit per Unit by Segment.

**3 — Product & Geography.** Net Sales + Profit by Product · treemap Country × Product · filled map of Profit by Country · Profit per Unit by Product.

### The waterfall

Steps are Gross Sales → −Discounts → −COGS. The waterfall's built-in **Total bar equals Profit**, so Profit is deliberately *not* a fourth step — adding it would double-count.

### The loss table

No visual-level filter is used. `Loss Making Txns` and `Loss Amount` return BLANK for combinations with no losses, and the table visual hides all-blank rows automatically — so the table self-filters to loss-making combinations only.

## Caveats carried over from the analysis

1. **No YoY measure is included, by design.** 2013 covers only Sep–Dec (175 rows) against a full 2014 (525 rows). Any YoY or annual total would mislead. Use `Sales MoM %` / `Sales Rolling 3M`.
2. **Sale Price is fixed per Segment**, not per Product — price analysis belongs on the Segment axis.
3. **COGS is taken from the column, never derived** from `Manufacturing Price` (that identity holds for only ~23% of rows).
4. The filled map needs internet access for Bing geocoding. Offline it renders empty; the Country bar chart on page 1 covers the same ground.

## Verification performed

- All 41 JSON/`.pbip`/`.pbir`/`.pbism`/`.platform` files parse.
- **Schema-validated against Power BI Desktop's own bundled PBIR schemas** (extracted from
  `bin\WebView2Resources\minerva\scripts\desktop.schema.json.*.min.js` in the installed
  Desktop 2.155). 35 report files checked — `version.json`, `report.json`, `pages.json`,
  3 × `page.json`, 29 × `visual.json` — **0 errors**.
  The report targets the **v2 PBIR generation** — `version.json` declares `2.0.0`, with
  `report` 3.3.0, `page` 2.1.0, `visualContainer` 2.10.0, `pagesMetadata` 1.1.0,
  `versionMetadata` 1.0.0. This matches what Desktop 2.155 writes; the older major-1
  generation passes schema validation but Desktop fails to render it
  (`Cannot read properties of undefined (reading 'visualContainers')`).
- All **50** report field references resolve to a real table + column/measure in the TMDL model.
- CSV number/date formats inspected directly before writing the M query.

- **The TMDL model deserializes through Microsoft's own parser** —
  `Microsoft.AnalysisServices.TmdlSerializer.DeserializeDatabaseFromFolder`, loaded from
  `bin\Microsoft.PowerBI.Amo.dll` in the installed Desktop. Result: 7 tables, 5 relationships,
  compatibility level 1600, 2 shared expressions, all 5 relationships binding to the correct
  columns, and every table and column carrying a `lineageTag`.

Not verified: DAX evaluation and visual rendering, which only happen once the model refreshes
in Desktop.

### Conventions taken from a Desktop-authored project

The model deliberately mirrors the structure Power BI Desktop itself writes:

| Convention | Why |
|---|---|
| `lineageTag` GUID on every table, column and measure | persistent object identity — relationships and report bindings resolve against it |
| `compatibilityLevel: 1600` | matches what current Desktop emits |
| `definition/cultures/en-US.tmdl` + `ref cultureInfo en-US` | Desktop expects the culture object |
| `annotation PBI_ProTooling = ["DevMode"]` | marks the model as PBIP dev-mode authored |
| GUID relationship names | Desktop names relationships by GUID, not by label |
| no explicit `mode:` on partitions | import is the default; Desktop omits it |

`lineageTag`s are generated deterministically (UUID-v5 over the object path), so regenerating the
project keeps object identity stable and does not break report field bindings.

### Theme

`report.json` carries an empty `themeCollection`, so the report uses Desktop's default theme —
the same thing the reference project does. Apply a theme from *View → Themes* if you want one.
