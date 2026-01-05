Financial Forecasting Automation (FP&A)
Overview

This project demonstrates a lightweight, production-style financial forecasting automation pipeline commonly used in FP&A and Finance Technology teams.
It simulates how monthly actuals are ingested from a data source, transformed using SQL, forecasted using a baseline time-series method, and converted into automated variance reports for financial review.

The goal of this project is to show how Python + SQL can replace manual Excel-based forecasting workflows, enabling scalable, repeatable, and auditable forecasting processes.

Business Problem

Finance teams regularly need to:

Load monthly actuals from a data warehouse

Produce rolling forecasts

Compare forecast vs actual results

Identify variances for management review

Deliver structured Excel outputs on a recurring basis

Manual spreadsheet workflows are error-prone, slow, and difficult to scale.
This project demonstrates a simplified but realistic automation approach that mirrors real FP&A pipelines used in large organizations.

Solution Architecture

The pipeline is designed with clear separation between data, logic, and outputs:

CSV / Source Data
        ↓
     SQLite
        ↓
       SQL
        ↓
   Python Pipeline
        ↓
 Forecast + Variance
        ↓
   Excel Report

Data Model
Input Table: actuals
Column	Type	Description
month	DATE	Month of financial activity
account	TEXT	Cost or revenue category (e.g., Payroll)
amount	FLOAT	Actual amount for the period

The dataset represents monthly actuals, similar to data coming from ERP systems such as SAP, Oracle, or NetSuite.

SQL Layer (Data Extraction)

The SQL layer simulates an enterprise finance data model and is responsible for:

- Monthly aggregation of actuals
- Standardized time ordering
- Lag-based YoY metrics
- Rolling averages for trend analysis
- Baseline forecast generation

CTEs are used to separate data preparation, aggregation, and analytic logic,
mirroring patterns commonly used in production data warehouses.


This step reflects real-world usage where FP&A analysts consume curated views or fact tables rather than raw transactions.

Forecasting Methodology
Baseline Model: Seasonal Naive Forecast

This project uses a Seasonal Naive model, a common FP&A baseline technique:

Forecast for a given month = actual value from the same month last year

Why this approach:

Very common baseline in corporate planning

Easy to explain to finance stakeholders

Strong benchmark for evaluating more advanced models

Requires minimal parameters and no external dependencies

If insufficient historical data exists, the model falls back to using the most recent observed value.

Forecast Horizon

Default forecast horizon: 6 months

Monthly frequency

Automatically generated future periods based on last available actuals

Variance Analysis Logic

Once forecasts are generated, the pipeline automatically calculates:

Variance

variance = actual − forecast


Variance %

variance_pct = variance / forecast


Variance values appear automatically once actuals for forecasted periods become available.

This mirrors real FP&A workflows where:

Forecasts are locked

Actuals arrive monthly

Variance analysis updates without manual recalculation

Output Artifacts
1. CSV Output

outputs/forecast_output.csv

Contains:

month

account

actual_amount

forecast_amount

variance

variance_pct

Useful for:

Further modeling

Data validation

Downstream analytics

2. Excel Report

outputs/variance_report.xlsx

Sheets included:

Sheet: Forecast+Variance

Full time series including:

historical actuals

future forecasts

variance calculations

Sheet: Summary

A compact view showing:

last 3 historical months

next 6 forecast months

grouped by account

This mirrors how FP&A teams prepare review decks and management summaries.

Key Features Demonstrated

SQL-based data extraction layer

Automated monthly aggregation

Time-series forecasting logic

Rolling forecast generation

Variance calculation

Excel report automation

Modular and reusable Python structure

Clear separation between data, logic, and outputs

Getting Started

Prerequisites

Python 3.8 or higher

Installation

1. Install required dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- pandas (>=2.0)
- numpy (>=1.24)
- openpyxl (>=3.1)

Running the Pipeline

Option 1: Run the complete pipeline (Recommended)

```bash
python run.py
```

This will execute both steps in sequence:
1. Load data from CSV to SQLite database
2. Generate forecasts and variance analysis reports

Option 2: Run steps individually

Step 1: Load data to SQLite

```bash
python scr/01_load_to_sqlite.py
```

Step 2: Generate forecast and variance reports

```bash
python scr/02_forecast_and_variance.py
```

Output Files

After running the pipeline, the following files will be generated in the `outputs/` directory:

- `forecast_output.csv` - Complete forecast data with variance calculations
- `variance_report.xlsx` - Excel report with Forecast+Variance and Summary sheets

Technologies Used

Programming & Analytics

Python

pandas

NumPy

Data & Querying

SQLite

SQL

Reporting

Excel (via openpyxl)

Project Structure
fpa-forecast-automation/
│
├── data/
│   ├── actuals.csv
│   └── fpa.db
│
├── sql/
│   ├── monthly_actuals.sql
│   ├── monthly_actuals_enriched.sql
│   └── forecast_baseline.sql
│
├── scr/
│   ├── 01_load_to_sqlite.py
│   └── 02_forecast_and_variance.py
│
├── outputs/
│   ├── forecast_output.csv
│   └── variance_report.xlsx
│
├── run.py
├── requirements.txt
└── README.md