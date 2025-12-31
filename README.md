# Financial Forecasting Automation

A simple FP&A-style forecasting automation project using **SQL + Python**.

This project demonstrates how monthly actuals can be loaded, forecasted, and converted into an automated variance report — similar to workflows used by FP&A and Finance Systems teams.

---

## What This Project Does

- Loads monthly financial actuals into SQLite  
- Uses SQL to aggregate data  
- Generates a rolling forecast (seasonal naive baseline)  
- Calculates forecast vs actual variance  
- Exports results to Excel for reporting  

---

## Data Model

**Table: `actuals`**

| Column  | Description |
|--------|-------------|
| month  | Month of activity |
| account | Cost or revenue category |
| amount | Actual value |

---

## Forecast Logic

- Monthly frequency  
- 6-month forecast horizon  
- Seasonal naive method  
  - Forecast = same month last year  
  - Fallback to last observed value if history is limited  

---

## Outputs

### CSV
`outputs/forecast_output.csv`

Contains:
- month  
- account  
- actual_amount  
- forecast_amount  
- variance  
- variance_pct  

### Excel
`outputs/variance_report.xlsx`

Includes:
- Full forecast + variance table  
- Summary view for recent and future months  

---

## Project Structure

fpa-forecast-automation/
├── data/
│ ├── actuals.csv
│ └── fpa.db
├── sql/
│ └── monthly_actuals.sql
├── src/
│ ├── 01_load_to_sqlite.py
│ └── 02_forecast_and_variance.py
├── outputs/
│ ├── forecast_output.csv
│ └── variance_report.xlsx
└── README.md

---

## How to Run

```bash
python src/01_load_to_sqlite.py
python src/02_forecast_and_variance.py


Tech Stack

Python

pandas

NumPy

SQLite

SQL

Excel (openpyxl)

Notes

This project is intentionally simple and focuses on:

Clean SQL usage

Reproducible forecasting logic

Automated variance reporting

Clear FP&A-style structure

It can be extended with driver-based models, dashboards, or cloud data warehouses.
