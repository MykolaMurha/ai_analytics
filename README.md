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

---

# AI Analytics Demo - Day 2 Summary

Day 2 built and **live-validated** a **Databricks Analytics Specialist** — a portable, skill-based agent that helps you work with Databricks AI/BI Genie and Databricks Connect for Python. All of its artifacts live under [`databricks_agent/`](databricks_agent).

## Session overview

- Turned a short XML brief (`databricks_agent_creator_promt.xml`) into a complete agent bundle under `databricks_agent/`:
  - `AGENTS.md` + `CLAUDE.md` (operating guide + onboarding) and a bundle `README.md`.
  - Four **skills**, each with a `SKILL.md`, a `references/` folder, and runnable `scripts/`:
    1. `working-with-genie` — what Genie is and how to curate it for accurate answers.
    2. `genie-agent-setup` — create and configure a Genie Agent step by step.
    3. `databricks-connect-python` — run Python/Spark against Databricks compute.
    4. `genie-conversation-api` — drive Genie over REST or the `databricks-sdk`.
- **Verified every skill end-to-end against a real workspace:**
  - Genie Conversation API: asked *"Which product sold the most units?"* and got generated SQL plus the answer (`Golden Gate Ginger — 3,865 units`).
  - Databricks Connect (serverless): ran `SELECT 1` and a real read of `samples.nyctaxi.trips`.
  - Found and fixed a real bug (query results were being fetched for non-SQL attachments, causing an HTTP 400) and documented that the live Genie status flow is richer than the docs suggest.
- Added `show_data.py`, a one-file beginner demo that prints rows from a Databricks table.

## How a junior data analyst sets up and uses the agent locally

Do this once, on your local Windows machine, in **PowerShell**. **You never put secrets in code or files** — credentials go into environment variables.

### What you need first
- **Windows** with **PowerShell**.
- **Python 3.10+** installed (check with `python --version`).
- Access to a **Databricks workspace** that has **Unity Catalog** and a **Pro or Serverless SQL warehouse**.
- A **Genie Agent** (also called a Genie *space*) you can open in that workspace.

### Step 1 — Get your Databricks host URL
1. Open your Databricks workspace in a browser and log in.
2. Look at the address bar. Your host is the start of the URL, for example:
   - AWS: `https://dbc-xxxxxxxx-xxxx.cloud.databricks.com`
   - Azure: `https://adb-xxxxxxxxxxxx.xx.azuredatabricks.net`
   - GCP: `https://xxxxxxxx.gcp.databricks.com`
3. Copy it exactly — keep `https://` and **remove anything after `.com` / `.net`** (no trailing slash).

### Step 2 — Create a Personal Access Token (PAT)
1. In Databricks, click your **email/username** in the top-right corner, then **Settings**.
2. Go to **Developer** → **Access tokens** → **Manage** → **Generate new token**.
3. Add a comment (e.g. `local agent`) and a lifetime, then click **Generate**.
4. **Copy the token immediately** — it is shown only once. It starts with `dapi...`.
5. Treat it like a password: never paste it into files, screenshots, chat, or git.

### Step 3 — Get your Genie Agent (space) id
1. In the Databricks sidebar, open **Genie** (or **Genie Agents**).
2. Open the agent you want to use.
3. Look at the browser URL — it contains a 32-character id, for example
   `.../genie/rooms/01f17f0ae4ea105ead7924299f53a49e`.
   That id (`01f1...`) is your **GENIE_SPACE_ID**.
   *(In the Day 2 demo we used the built-in "Bakehouse Sales Starter Space".)*
4. *Optional:* a **SQL Warehouse id** (**SQL Warehouses** → open a warehouse → the id is in its URL and connection details). Only needed if your Genie space has no default warehouse.

### Step 4 — Store your settings as environment variables (no secrets in code)
The agent ships PowerShell scripts that prompt for these values (the token is typed **hidden**) and save them as **user-scoped** environment variables. Run the one(s) you need:

- **For the Genie API:**
  ```powershell
  powershell -ExecutionPolicy Bypass -File "C:\courses\ai_analytics\databricks_agent\skills\genie-conversation-api\scripts\setup_env.ps1"
  ```
  Enter your **host**, **Genie space id**, (optional warehouse id), then choose **y** and enter your **PAT**.

- **For Databricks Connect:**
  ```powershell
  powershell -ExecutionPolicy Bypass -File "C:\courses\ai_analytics\databricks_agent\skills\databricks-connect-python\scripts\setup_env.ps1"
  ```
  Enter your **host**, choose **S** for **Serverless** (recommended), then enter your **PAT**.

These set `DATABRICKS_HOST`, `DATABRICKS_TOKEN`, `GENIE_SPACE_ID`, and `DATABRICKS_SERVERLESS_COMPUTE_ID=auto`.
**Close this PowerShell window and open a new one** so the variables load.

You can re-check them at any time — non-secret values print, the token stays hidden:
```powershell
'DATABRICKS_HOST','GENIE_SPACE_ID','DATABRICKS_SERVERLESS_COMPUTE_ID' | ForEach-Object { "$_ = " + [Environment]::GetEnvironmentVariable($_, 'User') }
if ([Environment]::GetEnvironmentVariable('DATABRICKS_TOKEN','User')) { "DATABRICKS_TOKEN = (set, hidden)" }
```

### Step 5 — Create an isolated Python "sandbox" and install the packages
Your main Python may already have `pyspark`, which **conflicts** with Databricks Connect, so use a separate virtual environment. In a **new** PowerShell window:
```powershell
cd C:\courses\ai_analytics
python -m venv databricks_agent\.venv
databricks_agent\.venv\Scripts\python.exe -m pip install --upgrade pip
databricks_agent\.venv\Scripts\python.exe -m pip install databricks-connect databricks-sdk requests
```
*(If `python` isn't found, use the full path to your Python, e.g. `C:\Python311\python.exe -m venv ...`.)*

### Step 6 — Run it and see data
- **Easiest — the one-file demo** (prints 10 rows from a sample table):
  ```powershell
  cd C:\courses\ai_analytics
  databricks_agent\.venv\Scripts\python.exe show_data.py
  ```
- **Ask Genie a question in plain English:**
  ```powershell
  databricks_agent\.venv\Scripts\python.exe databricks_agent\skills\genie-conversation-api\scripts\genie_conversation.py --question "Which product sold the most units?"
  ```
- **Smoke-test the Databricks Connect setup:**
  ```powershell
  databricks_agent\.venv\Scripts\python.exe databricks_agent\skills\databricks-connect-python\scripts\verify_connection.py --mode serverless
  ```

The first run takes ~30 seconds while serverless compute starts. If a command reports missing settings, open a fresh PowerShell (so the Step 4 variables load), or paste this loader first:
```powershell
foreach ($n in 'DATABRICKS_HOST','DATABRICKS_TOKEN','GENIE_SPACE_ID','DATABRICKS_SERVERLESS_COMPUTE_ID') { $v=[Environment]::GetEnvironmentVariable($n,'User'); if($v){ Set-Item "Env:$n" $v } }
```

### Where to learn more
- Start at [`databricks_agent/AGENTS.md`](databricks_agent/AGENTS.md) — the agent's operating guide.
- Each capability has its own `SKILL.md` under `databricks_agent/skills/<skill>/`, with references and runnable scripts.

## Safety notes
- Your PAT lives **only** in your user environment variables — never in the repo.
- The Python sandbox (`databricks_agent/.venv`) and any `.env` / `.databrickscfg` files are **git-ignored**.
- Rotate or delete your PAT in Databricks (**Settings → Developer → Access tokens**) when you no longer need it.

## Session commits (Day 2)
- `fca09ac` - Databricks agent creation prompt added.
- `746c46a` - Databricks Analytics Specialist agent bundle initialized (skills, docs, scripts).
- this commit - Day 2 summary and local setup guide (plus the `show_data.py` demo).
