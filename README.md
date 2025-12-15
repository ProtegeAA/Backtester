# Stock Backtester

A Python CLI tool to backtest stock performance against market indices over customizable time periods.

## Features

- Compare one or more stock tickers
- Flexible date range (start/end year)
- Compare against major indices (S&P 500, NASDAQ, Dow Jones, Russell 2000)
- Performance metrics: Total Return, Annualized Return, Volatility, Max Drawdown, Sharpe Ratio
- Generates normalized performance charts
- Exports results to CSV

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/Backtester.git
cd Backtester
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Single stock
python backtester.py --tickers AAPL --start 2020 --end 2024

# Single stock vs S&P 500
python backtester.py --tickers AAPL --start 2020 --end 2024 --index SP500

# Multiple stocks
python backtester.py --tickers AAPL MSFT GOOGL --start 2015 --end 2024

# Compare against NASDAQ
python backtester.py --tickers TSLA --start 2019 --end 2024 --index NASDAQ
```

### Options

| Flag | Description |
|------|-------------|
| `--tickers`, `-t` | Stock ticker symbol(s) to analyze |
| `--start`, `-s` | Start year |
| `--end`, `-e` | End year |
| `--index`, `-i` | Index to compare (SP500, NASDAQ, DOW, RUSSELL2000) |
| `--output-dir`, `-o` | Output directory (default: output) |

## Output

- **Terminal**: Performance metrics table
- **CSV**: `output/backtest_YYYY_YYYY.csv`
- **Chart**: `output/performance_YYYY_YYYY.png`

## Example Output

```
================================================================================
PERFORMANCE METRICS
================================================================================
Ticker  Total Return (%)  Annualized Return (%)  Volatility (%)  Max Drawdown (%)  Sharpe Ratio
  AAPL            246.45                  28.29           31.69            -31.43          0.77
 SP500             81.31                  12.67           21.35            -33.92          0.41
================================================================================
```

## License

MIT
