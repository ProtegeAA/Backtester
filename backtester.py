#!/usr/bin/env python3
"""
Stock Backtester - Compare stock performance against market indices.
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


INDEX_MAPPING = {
    "SP500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW": "^DJI",
    "RUSSELL2000": "^RUT",
}

RISK_FREE_RATE = 0.04  # 4% annual risk-free rate


def parse_args():
    parser = argparse.ArgumentParser(
        description="Backtest stock performance against market indices."
    )
    parser.add_argument(
        "--tickers",
        "-t",
        nargs="+",
        required=True,
        help="Stock ticker symbol(s) to analyze (e.g., AAPL MSFT GOOGL)",
    )
    parser.add_argument(
        "--start",
        "-s",
        type=int,
        required=True,
        help="Start year (e.g., 2020)",
    )
    parser.add_argument(
        "--end",
        "-e",
        type=int,
        required=True,
        help="End year (e.g., 2024)",
    )
    parser.add_argument(
        "--index",
        "-i",
        choices=list(INDEX_MAPPING.keys()),
        help="Index to compare against (SP500, NASDAQ, DOW, RUSSELL2000)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="output",
        help="Directory for output files (default: output)",
    )
    return parser.parse_args()


def fetch_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch historical price data for a ticker."""
    print(f"Fetching data for {ticker}...")
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if data.empty:
        raise ValueError(f"No data found for {ticker}")
    return data


def calculate_metrics(prices: pd.Series, name: str) -> dict:
    """Calculate performance metrics for a price series."""
    # Daily returns
    daily_returns = prices.pct_change().dropna()

    # Total return
    total_return = (prices.iloc[-1] / prices.iloc[0] - 1) * 100

    # Annualized return
    years = len(prices) / 252  # Trading days per year
    annualized_return = ((1 + total_return / 100) ** (1 / years) - 1) * 100

    # Volatility (annualized)
    volatility = daily_returns.std() * (252 ** 0.5) * 100

    # Maximum drawdown
    cumulative = (1 + daily_returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100

    # Sharpe ratio
    excess_return = annualized_return / 100 - RISK_FREE_RATE
    sharpe_ratio = excess_return / (volatility / 100) if volatility > 0 else 0

    return {
        "Ticker": name,
        "Total Return (%)": round(total_return, 2),
        "Annualized Return (%)": round(annualized_return, 2),
        "Volatility (%)": round(volatility, 2),
        "Max Drawdown (%)": round(max_drawdown, 2),
        "Sharpe Ratio": round(sharpe_ratio, 2),
    }


def display_results(results: list[dict]):
    """Display results in a formatted table."""
    df = pd.DataFrame(results)
    print("\n" + "=" * 80)
    print("PERFORMANCE METRICS")
    print("=" * 80)
    print(df.to_string(index=False))
    print("=" * 80 + "\n")


def save_csv(results: list[dict], output_dir: str, start_year: int, end_year: int):
    """Save results to CSV file."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"backtest_{start_year}_{end_year}.csv"
    filepath = os.path.join(output_dir, filename)
    df = pd.DataFrame(results)
    df.to_csv(filepath, index=False)
    print(f"Results saved to: {filepath}")


def generate_chart(
    price_data: dict[str, pd.Series],
    output_dir: str,
    start_year: int,
    end_year: int,
):
    """Generate normalized performance chart."""
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(12, 6))

    for name, prices in price_data.items():
        # Normalize to 100 at start
        normalized = prices / prices.iloc[0] * 100
        plt.plot(normalized.index, normalized.values, label=name, linewidth=1.5)

    plt.title(f"Performance Comparison ({start_year} - {end_year})")
    plt.xlabel("Date")
    plt.ylabel("Normalized Price (Start = 100)")
    plt.legend(loc="upper left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    filename = f"performance_{start_year}_{end_year}.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"Chart saved to: {filepath}")


def main():
    args = parse_args()

    # Validate date range
    if args.start > args.end:
        print(f"Error: Start year ({args.start}) must be less than or equal to end year ({args.end})")
        return

    # Build date range
    start_date = f"{args.start}-01-01"
    end_date = f"{args.end}-12-31"

    print(f"\nBacktesting from {args.start} to {args.end}")
    print(f"Tickers: {', '.join(args.tickers)}")
    if args.index:
        print(f"Comparing against: {args.index}")
    print()

    # Collect all tickers to fetch
    tickers_to_fetch = list(args.tickers)
    if args.index:
        tickers_to_fetch.append(INDEX_MAPPING[args.index])

    # Fetch data and calculate metrics
    results = []
    price_data = {}

    for ticker in args.tickers:
        try:
            data = fetch_data(ticker, start_date, end_date)
            prices = data["Close"].squeeze()
            metrics = calculate_metrics(prices, ticker)
            results.append(metrics)
            price_data[ticker] = prices
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    # Fetch index data if specified
    if args.index:
        try:
            index_ticker = INDEX_MAPPING[args.index]
            data = fetch_data(index_ticker, start_date, end_date)
            prices = data["Close"].squeeze()
            metrics = calculate_metrics(prices, args.index)
            results.append(metrics)
            price_data[args.index] = prices
        except Exception as e:
            print(f"Error fetching {args.index}: {e}")

    if not results:
        print("No data to analyze. Exiting.")
        return

    # Display results
    display_results(results)

    # Save CSV
    save_csv(results, args.output_dir, args.start, args.end)

    # Generate chart
    generate_chart(price_data, args.output_dir, args.start, args.end)

    print("Backtest complete!")


if __name__ == "__main__":
    main()
