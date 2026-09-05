# AAPL Stock Forecasting — Out-of-Sample Analysis

A forecasting case study evaluating whether simple level, trend, and seasonal methods can produce useful long-horizon forecasts when only a short historical window is available for training.

## Executive summary

The analysis uses **AAPL daily closing prices from 2023–2024** and deliberately restricts the training data to January of each year. February–December is held out as an out-of-sample evaluation period.

This creates a practical forecasting question:

> **Does a more complex forecasting method actually improve performance when the available training history is limited?**

The earlier run favoured simple level-based methods. That ranking is provisional until the corrected workflow is rerun on the original source CSV.

## Validation status

**The historical MAD/MAPE table is withdrawn pending rerun.** The source Yahoo Finance CSV is not committed, so the previous numbers cannot be independently reproduced from this checkout. A fresh Yahoo request was rate-limited during review; a different provider or adjusted-price series would not establish reproduction of the original experiment.

The code now scores SES forecasts **before updating with the observed value**. Moving-average windows are compared on a common set of training dates. These changes can alter selected parameters and held-out results. Unit tests validate these forecasting rules; they do not validate historical AAPL scores.

The report and presentation are archived coursework artifacts with superseded methods/results. They are retained as history, not current evidence. The original report credits Nikitas Valtadoros, David Frederick and Dimitrios Bechrakis; task-level ownership is not documented.

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

The experiment tests whether complexity improves held-out performance; the current ranking must be regenerated after the tuning corrections.

A very short training window makes simple baselines essential comparisons. This is a useful reminder that forecasting choices should be validated against a realistic holdout period rather than selected because the model appears more sophisticated.

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
