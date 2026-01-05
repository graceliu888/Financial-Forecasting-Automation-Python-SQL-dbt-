"""
Main runner script - Run the complete financial forecasting automation pipeline

Usage:
    python run.py
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Run the complete forecasting pipeline"""
    script_dir = Path(__file__).parent

    print("=" * 60)
    print("Financial Forecasting Automation Pipeline")
    print("=" * 60)

    # Step 1: Load data to SQLite
    print("\n[Step 1/2] Loading data to SQLite...")
    script1 = script_dir / "scr" / "01_load_to_sqlite.py"
    result1 = subprocess.run(
        [sys.executable, str(script1)], capture_output=True, text=True
    )
    if result1.returncode != 0:
        print("Error: Step 1 failed")
        print(result1.stderr)
        sys.exit(1)
    print(result1.stdout.strip())

    # Step 2: Generate forecast and variance analysis
    print("\n[Step 2/2] Generating forecast and variance analysis...")
    script2 = script_dir / "scr" / "02_forecast_and_variance.py"
    result2 = subprocess.run(
        [sys.executable, str(script2)], capture_output=True, text=True
    )
    if result2.returncode != 0:
        print("Error: Step 2 failed")
        print(result2.stderr)
        sys.exit(1)
    print(result2.stdout.strip())

    print("\n" + "=" * 60)
    print("Pipeline completed! Output files:")
    print("  - outputs/forecast_output.csv")
    print("  - outputs/variance_report.xlsx")
    print("=" * 60)


if __name__ == "__main__":
    main()
