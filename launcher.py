#!/usr/bin/env python3
"""
Interactive launcher for Stock Backtester
Makes it easy for non-technical users to run backtests
"""

import os
import sys
import subprocess
from datetime import datetime


def print_header():
    """Print welcome header."""
    print("\n" + "=" * 60)
    print("         STOCK BACKTESTER - INTERACTIVE LAUNCHER")
    print("=" * 60)
    print("\nCompare stock performance against market indices")
    print("over customizable time periods.\n")


def get_tickers():
    """Prompt user for stock tickers."""
    print("Step 1: Enter Stock Tickers")
    print("-" * 40)
    print("Enter one or more stock ticker symbols.")
    print("Examples: AAPL, MSFT, GOOGL, TSLA, AMZN")
    print("\nFor multiple stocks, separate with spaces.")
    print("Example: AAPL MSFT GOOGL\n")

    while True:
        tickers_input = input("Stock ticker(s): ").strip().upper()
        if tickers_input:
            tickers = tickers_input.split()
            print(f"\n✓ Will analyze: {', '.join(tickers)}\n")
            return tickers
        else:
            print("Please enter at least one ticker.\n")


def get_year(prompt, default=None):
    """Prompt user for a year."""
    current_year = datetime.now().year

    while True:
        if default:
            year_input = input(f"{prompt} (default: {default}): ").strip()
            if not year_input:
                return default
        else:
            year_input = input(f"{prompt}: ").strip()

        try:
            year = int(year_input)
            if 1900 <= year <= current_year:
                return year
            else:
                print(f"Please enter a year between 1900 and {current_year}.\n")
        except ValueError:
            print("Please enter a valid year (e.g., 2020).\n")


def get_date_range():
    """Prompt user for date range."""
    print("Step 2: Select Date Range")
    print("-" * 40)
    print("Enter the start and end years for your backtest.\n")

    current_year = datetime.now().year
    default_start = current_year - 5
    default_end = current_year - 1

    start_year = get_year(f"Start year (e.g., {default_start})", default_start)

    while True:
        end_year = get_year(f"End year (e.g., {default_end})", default_end)
        if end_year >= start_year:
            break
        print(f"End year must be >= start year ({start_year}).\n")

    print(f"\n✓ Date range: {start_year} to {end_year}\n")
    return start_year, end_year


def get_index():
    """Prompt user for comparison index."""
    print("Step 3: Choose Comparison Index (Optional)")
    print("-" * 40)
    print("Compare your stock(s) against a market index:\n")
    print("  1. S&P 500 (SP500)")
    print("  2. NASDAQ (NASDAQ)")
    print("  3. Dow Jones (DOW)")
    print("  4. Russell 2000 (RUSSELL2000)")
    print("  5. None (skip comparison)\n")

    indices = {
        "1": "SP500",
        "2": "NASDAQ",
        "3": "DOW",
        "4": "RUSSELL2000",
        "5": None
    }

    while True:
        choice = input("Your choice (1-5, default: 1): ").strip()
        if not choice:
            choice = "1"

        if choice in indices:
            index = indices[choice]
            if index:
                print(f"\n✓ Will compare against: {index}\n")
            else:
                print("\n✓ No index comparison\n")
            return index
        else:
            print("Please enter a number between 1 and 5.\n")


def get_output_dir():
    """Prompt user for output directory."""
    print("Step 4: Output Directory (Optional)")
    print("-" * 40)
    default_dir = "output"
    output_dir = input(f"Output directory (default: {default_dir}): ").strip()

    if not output_dir:
        output_dir = default_dir

    print(f"\n✓ Results will be saved to: {output_dir}\n")
    return output_dir


def confirm_and_run(tickers, start_year, end_year, index, output_dir):
    """Confirm settings and run backtester."""
    print("=" * 60)
    print("BACKTEST CONFIGURATION")
    print("=" * 60)
    print(f"Stock Ticker(s): {', '.join(tickers)}")
    print(f"Date Range: {start_year} - {end_year}")
    print(f"Compare Against: {index if index else 'None'}")
    print(f"Output Directory: {output_dir}")
    print("=" * 60)
    print()

    confirm = input("Run backtest with these settings? (Y/n): ").strip().lower()

    if confirm in ['', 'y', 'yes']:
        # Build command with absolute path to backtester.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backtester_path = os.path.join(script_dir, "backtester.py")

        cmd = [
            sys.executable,
            backtester_path,
            "--tickers"
        ] + tickers + [
            "--start", str(start_year),
            "--end", str(end_year),
            "--output-dir", output_dir
        ]

        if index:
            cmd.extend(["--index", index])

        print("\n" + "=" * 60)
        print("RUNNING BACKTEST...")
        print("=" * 60 + "\n")

        # Run backtester
        try:
            subprocess.run(cmd, check=True, cwd=script_dir)
            print("\n" + "=" * 60)
            print("SUCCESS!")
            print("=" * 60)
            output_path = os.path.join(script_dir, output_dir)
            print(f"\nYour results are saved in: {output_path}")
            print("  - CSV file with metrics")
            print("  - PNG chart showing performance")
            print("\nThank you for using Stock Backtester!")
        except subprocess.CalledProcessError as e:
            print(f"\nError running backtest: {e}")
            return False
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            return False
    else:
        print("\nBacktest cancelled.")
        return False

    return True


def main():
    """Main launcher function."""
    try:
        print_header()

        # Collect user inputs
        tickers = get_tickers()
        start_year, end_year = get_date_range()
        index = get_index()
        output_dir = get_output_dir()

        # Run backtest
        confirm_and_run(tickers, start_year, end_year, index, output_dir)

    except KeyboardInterrupt:
        print("\n\nBacktest cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
