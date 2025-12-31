import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

DB_PATH = Path("data/fpa.db")
SQL_PATH = Path("sql/monthly_actuals.sql")
OUT_DIR = Path("outputs")

HORIZON_MONTHS = 6  # forecast next N months

def seasonal_naive_forecast(history: pd.Series, horizon: int, season_len: int = 12) -> pd.Series:
    """
    Seasonal Naive: forecast each future month using last year's same month actuals.
    If there is not enough history, fallback to the last observed value.
    """
    if len(history) >= season_len:
        base = history.iloc[-season_len:]
        reps = int(np.ceil(horizon / season_len))
        fc = pd.concat([base] * reps, ignore_index=True).iloc[:horizon]
        return fc
    return pd.Series([history.iloc[-1]] * horizon)

def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    sql = SQL_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(sql, conn)

    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values(["account", "month"])

    outputs = []

    for account, g in df.groupby("account"):
        g = g.sort_values("month").copy()
        g.set_index("month", inplace=True)

        actual = g["actual_amount"]

        last_month = actual.index.max()
        future_months = pd.date_range(
            last_month + pd.offsets.MonthBegin(1),
            periods=HORIZON_MONTHS,
            freq="MS"
        )

        forecast_values = seasonal_naive_forecast(actual, HORIZON_MONTHS, season_len=12).values
        fc = pd.Series(forecast_values, index=future_months, name="forecast_amount")

        out = pd.DataFrame({"actual_amount": actual})
        out["forecast_amount"] = np.nan

        future_df = pd.DataFrame({"actual_amount": np.nan, "forecast_amount": fc})
        out = pd.concat([out, future_df])

        out["account"] = account

        # Variance will be non-null only when actuals exist for the same month as forecast.
        out["variance"] = out["actual_amount"] - out["forecast_amount"]
        out["variance_pct"] = np.where(
            out["forecast_amount"].notna() & (out["forecast_amount"] != 0),
            out["variance"] / out["forecast_amount"],
            np.nan
        )

        outputs.append(out.reset_index().rename(columns={"index": "month"}))

    result = pd.concat(outputs, ignore_index=True)

    forecast_csv = OUT_DIR / "forecast_output.csv"
    result.to_csv(forecast_csv, index=False)

    excel_path = OUT_DIR / "variance_report.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        result.to_excel(writer, sheet_name="Forecast+Variance", index=False)

        result["month"] = pd.to_datetime(result["month"])
        summary = (result
                   .sort_values(["account", "month"])
                   .groupby("account")
                   .tail(3 + HORIZON_MONTHS))
        summary.to_excel(writer, sheet_name="Summary", index=False)

    print("Saved outputs:")
    print(f"- {forecast_csv}")
    print(f"- {excel_path}")

if __name__ == "__main__":
    main()


# To run the script, use the command:# python src/02_forecast_and_variance.py


"""outputs/forecast_output.csv

outputs/variance_report.xlsx """