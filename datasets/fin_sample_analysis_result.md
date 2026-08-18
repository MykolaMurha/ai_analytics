# Financial Sample — Analysis Brief for Power BI Dashboard

**Source:** `datasets/Financial Sample.csv` · 700 rows × 16 cols · 0 nulls · 0 duplicates
**Grain:** one row = Segment × Country × Product × Discount Band × Month (transaction aggregate, no order ID)
**Period:** 2013-09-01 → 2014-12-01 (16 months, monthly granularity — all dates are the 1st of month)

---

## 1. Data model (star schema for Power BI)

| Table | Columns | Cardinality |
|---|---|---|
| **Fact_Financials** | Units Sold, Manufacturing Price, Sale Price, Gross Sales, Discounts, Sales, COGS, Profit, keys | 700 rows |
| Dim_Segment | Segment | 5: Government, Small Business, Enterprise, Midmarket, Channel Partners |
| Dim_Country | Country | 5: USA, Canada, France, Germany, Mexico |
| Dim_Product | Product, Manufacturing Price | 6: Paseo, VTT, Amarilla, Velo, Montana, Carretera |
| Dim_DiscountBand | Discount Band (ordered: None < Low < Medium < High) | 4 |
| Dim_Date | Date, Year, Month Number, Month Name | 16 months |

**Required cleanup before load:**
1. Column names have leading/trailing spaces (` Product `, ` Sales `, ` Month Name `) → trim.
2. Money columns are **text** (`$1,207,500.00`, `$-`) → strip `$ , ( )`, replace `-` with 0, convert to Decimal.
3. Text values in Segment/Country/Product/Discount Band have padding → trim.
4. `Date` is US format `M/D/YYYY` → set locale on conversion.
5. Drop `Year` / `Month Number` / `Month Name` from fact; use a proper Date table marked as date table (sort Month Name by Month Number).

**Verified identities (safe to use as DAX, no reconciliation risk):**
- `Gross Sales = Units Sold × Sale Price`
- `Sales = Gross Sales − Discounts`
- `Profit = Sales − COGS`

---

## 2. Headline KPIs (whole dataset)

| Index | Value | DAX |
|---|---|---|
| Gross Sales | $127.93M | `SUM([Gross Sales])` |
| Discounts | $9.21M | `SUM([Discounts])` |
| **Net Sales** | **$118.73M** | `SUM([Sales])` |
| COGS | $101.83M | `SUM([COGS])` |
| **Profit** | **$16.89M** | `SUM([Profit])` |
| **Profit Margin %** | **14.2%** | `DIVIDE([Profit],[Net Sales])` |
| Discount Rate % | 7.2% | `DIVIDE([Discounts],[Gross Sales])` |
| Units Sold | 1,125,806 | `SUM([Units Sold])` |
| Avg Transaction Size | $169.6K | `DIVIDE([Net Sales],COUNTROWS(Fact))` |
| Loss-making rows | 58 of 700 (−$777K) | `CALCULATE(COUNTROWS(Fact),[Profit]<0)` |

---

## 3. Top insights to visualize (ranked by business impact)

### INS-1 — Enterprise segment is the loss engine ⚠️ *(headline story)*
Enterprise: **$19.6M net sales (16.5% of revenue) but −$0.61M profit (−3.1% margin)**. It is the **only** loss-making segment and owns **all 58 loss-making rows**. Root cause visible in data: Enterprise sells at a fixed **$125 sale price** while its COGS runs at **103% of sales** — it is priced below cost.
→ Visual: bar chart Profit by Segment with conditional red formatting; drill-through page for Enterprise.

### INS-2 — Profit is concentrated, revenue is not
Government = **44% of sales but 67% of profit** (margin 21.7%). Small Business = 36% of sales but only 24% of profit (9.8% margin). Channel Partners is tiny in revenue (1.5%) but the **most profitable per dollar (73% margin)** — a growth candidate.
→ Visual: dual-axis / scatter "Sales share vs Profit share" by Segment, or matrix with margin heatmap.

### INS-3 — Discount depth destroys margin non-linearly
| Band | Effective discount | Margin % | Profit share |
|---|---|---|---|
| None | 0.0% | 21.9% | 10% |
| Low | 2.5% | 17.9% | 37% |
| Medium | 7.2% | 14.4% | 33% |
| **High** | **12.5%** | **9.1%** | 20% |

High band carries **32% of sales but only 20% of profit**, and 33 of 58 loss rows. **Low band is the sweet spot** (29% of sales → 37% of profit).
→ Visual: waterfall Gross Sales → Discounts → COGS → Profit; column chart Margin % by Discount Band.

### INS-4 — Geography is balanced; do not expect a country story
All 5 countries fall in a narrow band: sales 18–21%, profit 17–22%. Best margin France/Germany (~15.5%), weakest USA (12.0%). Country is a **filter/slicer dimension, not a headline insight**.
→ Visual: map or small bar, secondary position only.

### INS-5 — Product mix is flat; Paseo is the volume driver
Paseo = 28% of sales and 28% of profit (the only real outlier). Remaining 5 products sit at 11–18% each with margins 13–16%. Best margin: Amarilla (15.9%); weakest: Velo (12.6%).
→ Visual: treemap or ranked bar; avoid a full product page.

### INS-6 — Seasonality: Q4 spikes, but YoY is a trap
Peaks: **Oct-2014 $12.4M**, **Dec-2014 $12.0M**, Jun-2014 $9.5M. Troughs: Nov-2014 $5.4M, Mar-2014 $5.6M.
🚨 **2013 contains only Sep–Dec (175 rows); 2014 is complete (525 rows).** Any Year-over-Year or "annual total" measure will be misleading. Use **MoM / rolling 3-month**, or restrict YoY to Sep–Dec comparisons and label it.
→ Visual: line chart Sales + Profit Margin % by month, with a note on partial 2013.

---

## 4. Recommended DAX measures

```
Net Sales        = SUM(Fact[Sales])
Total Profit     = SUM(Fact[Profit])
Profit Margin %  = DIVIDE([Total Profit], [Net Sales])
Discount Rate %  = DIVIDE(SUM(Fact[Discounts]), SUM(Fact[Gross Sales]))
COGS Ratio %     = DIVIDE(SUM(Fact[COGS]), [Net Sales])
Profit per Unit  = DIVIDE([Total Profit], SUM(Fact[Units Sold]))
Loss Making Txns = CALCULATE(COUNTROWS(Fact), Fact[Profit] < 0)
Sales MoM %      = DIVIDE([Net Sales] - CALCULATE([Net Sales], DATEADD(Dim_Date[Date],-1,MONTH)),
                          CALCULATE([Net Sales], DATEADD(Dim_Date[Date],-1,MONTH)))
Sales Rolling 3M = CALCULATE([Net Sales], DATESINPERIOD(Dim_Date[Date], MAX(Dim_Date[Date]), -3, MONTH))
Profit Share %   = DIVIDE([Total Profit], CALCULATE([Total Profit], ALL(Dim_Segment)))
```

---

## 5. Suggested dashboard layout

**Page 1 — Executive Overview**
KPI cards (Net Sales, Profit, Margin %, Units, Discount Rate) → line chart Sales & Margin % by month → profit-bridge waterfall → bar Profit by Segment (red for negative) → map by Country. Slicers: Date, Segment, Country, Product, Discount Band.

**Page 2 — Profitability Deep Dive**
Matrix Segment × Discount Band with Margin % heatmap · scatter Sales vs Margin % (bubble = Units) · table of 58 loss-making transactions · Enterprise drill-through.

**Page 3 — Product & Geography**
Ranked bar Product by Sales/Profit · treemap Country × Product · Units vs Profit-per-unit comparison.

---

## 6. Caveats for the dashboard builder
1. **Partial 2013** — no valid YoY; state the 16-month window on the page.
2. **No customer / order ID** — no retention, basket, or count-of-orders metrics possible.
3. **Sale Price is fixed per Segment**, not per Product (Channel Partners $12, Midmarket $15, Enterprise $125, Small Business $300, Government $7/$20/$350). Price analysis belongs on the Segment axis.
4. Only 700 rows → visuals are dense and fast; no aggregation tables needed.
5. `Manufacturing Price` is a unit-cost attribute of the Product/row, but only ~23% of rows have `COGS ÷ Units = Manufacturing Price` — **do not derive COGS from it**; use the COGS column directly.
