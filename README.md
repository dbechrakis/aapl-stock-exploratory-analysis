# AAPL Stock Forecasting — Out-of-Sample Analysis

A forecasting case study evaluating whether simple level, trend, and seasonal methods can produce useful long-horizon forecasts when only a short historical window is available for training.

## Executive summary

The analysis uses **AAPL daily closing prices from 2023–2024** and deliberately restricts the training data to January of each year. February–December is held out as an out-of-sample evaluation period.

This creates a practical forecasting question:

> **Does a more complex forecasting method actually improve performance when the available training history is limited?**

The answer from this experiment is mostly **no**. Simple level-based methods were more competitive than trend-based approaches in both evaluation periods.

## Results

| Year | Best method | MAD | MAPE |
|---|---|---:|---:|
| 2023 | Naive | 31.56 | 17.62% |
| 2024 | Moving Average (n=2) | 29.14 | 13.25% |

### Full comparison

| Year | Method | MAD | MAPE |
|---|---|---:|---:|
| 2023 | Naive | 31.56 | 17.62% |
| 2023 | MA (n=2) | 32.20 | 17.98% |
| 2023 | SES (α=0.9) | 31.66 | 17.67% |
| 2023 | Linear Trend | 95.29 | 53.20% |
| 2023 | Trend + Seasonal | 95.32 | 53.22% |
| 2024 | Naive | 29.98 | 13.58% |
| 2024 | MA (n=2) | 29.14 | 13.25% |
| 2024 | SES (α=0.9) | 29.79 | 13.50% |
| 2024 | Linear Trend | 35.75 | 17.42% |
| 2024 | Trend + Seasonal | 35.78 | 17.44% |

## Methodology

For each year independently:

1. Clean and sort daily observations.
2. Use January as the training window.
3. Hold February–December out for evaluation.
4. Fit model parameters using January only.
5. Generate forecasts across the evaluation horizon.
6. Compare predictions with held-out actual prices using MAD and MAPE.

The trend and seasonal components are therefore estimated without access to future observations, avoiding look-ahead leakage.

## Models evaluated

- Naive forecasting
- Moving Average
- Simple Exponential Smoothing
- Linear trend extrapolation
- Linear trend + 21-trading-day seasonal adjustment

## Analytical takeaway

The main insight is methodological rather than predictive: **model complexity did not guarantee better out-of-sample performance**.

With a very short training window, simple baselines provided the strongest results. This is a useful reminder that forecasting choices should be validated against a realistic holdout period rather than selected because the model appears more sophisticated.

## Reference-class adjustment

An earlier version of the coursework included a peer-company reference-class adjustment. The required external peer datasets were not available in the final repository, and synthetic peer series do not provide sufficient evidence for a defensible empirical claim.

That component has therefore been excluded from the final workflow.

## Reproduce locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Place the raw dataset at:

```text
data/raw/AAPL_daily_2023_2024_raw.csv
```

Then run:

```bash
python dataset_preprocessing.py
python main.py
```

## Limitations

This is a compact forecasting experiment, not a production trading system. It evaluates closing-price levels rather than returns or volatility, uses one training window per year, and uses a simple approximation for the seasonal component.

## Tech stack

**Python · pandas · NumPy · Matplotlib · Statistical Forecasting · Time-Series Analysis · Jupyter**

## Context

Portfolio forecasting case study developed during an MSc Data Science programme at **The American College of Greece**.

## Author

**Dimitris Bechrakis**  
Business & Data Analyst | M.Sc. Data Science
