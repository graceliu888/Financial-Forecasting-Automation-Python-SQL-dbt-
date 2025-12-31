import sqlite3
import pandas as pd
from pathlib import Path

DATA_CSV = Path("data/actuals.csv")
DB_PATH = Path("data/fpa.db")

def main() -> None:
    df = pd.read_csv(DATA_CSV)
    df["month"] = pd.to_datetime(df["month"]).dt.strftime("%Y-%m-%d")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DROP TABLE IF EXISTS actuals")
        conn.execute("""
            CREATE TABLE actuals (
                month   TEXT NOT NULL,
                account TEXT NOT NULL,
                amount  REAL NOT NULL
            )
        """)
        df.to_sql("actuals", conn, if_exists="append", index=False)

    print(f"Loaded {len(df)} rows into {DB_PATH}")

if __name__ == "__main__":
    main()


# To run the script, use the command:# python src/01_load_to_sqlite.py

