"""
Tool script to view SQLite database contents

Usage:
    python view_db.py
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/fpa.db")


def view_database():
    """View database contents"""
    if not DB_PATH.exists():
        print(f"Error: Database file {DB_PATH} does not exist")
        print("Please run first: python scr/01_load_to_sqlite.py")
        return

    conn = sqlite3.connect(DB_PATH)

    # Show all tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("=" * 60)
    print("Database Tables:")
    for table in tables:
        print(f"  - {table[0]}")

    # Show actuals table structure
    print("\n" + "=" * 60)
    print("actuals Table Structure:")
    cursor.execute("PRAGMA table_info(actuals);")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]:<15} {col[2]:<10} {'NOT NULL' if col[3] else ''}")

    # Show data statistics
    cursor.execute("SELECT COUNT(*) FROM actuals")
    count = cursor.fetchone()[0]
    print(f"\nTotal Records: {count}")

    # Show first 10 rows
    print("\n" + "=" * 60)
    print("First 10 Rows:")
    df = pd.read_sql_query("SELECT * FROM actuals LIMIT 10", conn)
    print(df.to_string(index=False))

    # Show data summary
    print("\n" + "=" * 60)
    print("Data Summary (by Account):")
    df_summary = pd.read_sql_query(
        """
        SELECT
            account,
            COUNT(*) as record_count,
            MIN(month) as first_month,
            MAX(month) as last_month,
            SUM(amount) as total_amount,
            AVG(amount) as avg_amount
        FROM actuals
        GROUP BY account
        """,
        conn,
    )
    print(df_summary.to_string(index=False))

    conn.close()
    print("\n" + "=" * 60)
    print("\nTips: You can also use these tools to open the database:")
    print("  - DB Browser for SQLite (Free GUI tool)")
    print("  - VS Code extension: SQLite Viewer")
    print("  - Online tool: https://sqliteviewer.app/")


if __name__ == "__main__":
    view_database()
