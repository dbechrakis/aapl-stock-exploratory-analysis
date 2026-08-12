# AAPL Stock Exploratory Analysis

Statistical exploration and out-of-sample forecasting of Apple (AAPL) daily closing prices across 2023–2024.

## Objective

The project evaluates whether simple level, trend and seasonal forecasting methods can provide useful forecasts for the February–December portion of each year when the model is trained only on January observations.

The analysis compares:

- Naive forecasting
- Moving Average forecasting
- Simple Exponential Smoothing (SES)
- Linear trend extrapolation
- Linear trend + 21-trading-day seasonal adjustment

Forecast performance is evaluated with Mean Absolute Deviation (MAD) and Mean Absolute Percentage Error (MAPE).

## Forecasting Design

For each year independently:

1. Daily AAPL closing prices are cleaned and sorted chronologically.
2. January observations form the training window.
3. February–December observations are held out as the evaluation period.
4. Model parameters are selected using only the January training data.
5. Forecasts are generated for the full February–December horizon.
6. MAD and MAPE are calculated against the held-out actual prices.

The trend and seasonal components are also estimated exclusively from January. This prevents future observations from influencing the forecast construction.

## Project Structure

```text
aapl-stock-exploratory-analysis/
├── data/
│   ├── raw/
│   └── processed/
├── results/
│   ├── 2023/
│   ├── 2024/
│   └── comparison/
├── dataset_preprocessing.py
├── main.py
├── requirements.txt
└── README.md
```

## Reproducibility

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Place the raw AAPL daily dataset at:

```text
data/raw/AAPL_daily_2023_2024_raw.csv
```

Then run:

```bash
python dataset_preprocessing.py
python main.py
```

The processed datasets are written to `data/processed/` and the forecast metrics, forecast tables and comparison plots are written to `results/`.

## Key Analytical Principle

The evaluation is strictly out-of-sample: February–December prices are not used when fitting the January-trained forecasting models.

## Limitations

This is a compact forecasting exercise rather than a production trading system. The evaluation uses one training window per year and focuses on closing-price levels rather than returns, volatility or transaction costs. The 21-trading-day seasonal component is a deliberately simple approximation of a monthly trading cycle.

## Author

Dimitris Bechrakis — M.Sc. Data Science, The American College of Greece
