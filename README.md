# Mamaearth Order Data Analysis

This repository contains an end-to-end analysis of Mamaearth order data using **MySQL and Python**. The pipeline covers database setup, SQL reporting, data cleaning, EDA, visualization, and automated narrative generation.

## 1. SQL Setup and Reports

First, create the database tables and load the data using MySQL:

```sql
SOURCE sql/schema.sql;
SOURCE sql/seed_data.sql;
SOURCE sql/reports.sql;
```

Run the files in this order. `schema.sql` creates the required tables, `seed_data.sql` loads the data, and `reports.sql` generates the required SQL reports.

The source CSV files are available in the `data/` folder.

## 2. Python Analysis

Run the cleaning and EDA script:

```bash
python analysis/clean_and_eda.py
```

This cleans the order data, handles duplicates and missing values, calculates order values, and performs the required analysis.

Next, generate the visualizations:

```bash
python analysis/visualize.py
```

The generated charts are saved in the `visualizations/` folder.

**Task 5 of Part 2** creates:

```text
narrator/findings.json
```

This file stores the analysis findings used by the narrative generator.

## 3. Generate the Narrative

To use Gemini, set your API key as an environment variable.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
python narrator/generate_narrative.py
```

Replace `YOUR_API_KEY` with your actual Gemini API key.

The script can also run **without an API key**:

```bash
python narrator/generate_narrative.py
```

In this offline mode, the script uses its fallback path without calling Gemini.

Follow the steps above in order to reproduce the SQL results, analysis, visualizations, findings, and narrative.

