# AAPL Stock Forecasting Analysis

An out-of-sample forecasting study of Apple (AAPL) daily closing prices across 2023–2024.

## Objective

The project evaluates whether simple level, trend and seasonal forecasting methods can provide useful forecasts for the February–December portion of each year when the model is trained only on January observations.

The analysis compares:

- Naive forecasting
- Moving Average forecasting
- Simple Exponential Smoothing (SES)
- Linear trend extrapolation
- Linear trend + 21-trading-day seasonal adjustment

Forecast performance is evaluated with **Mean Absolute Deviation (MAD)** and **Mean Absolute Percentage Error (MAPE)**.

## Forecasting Design

For each year independently:

1. Daily AAPL closing prices are cleaned and sorted chronologically.
2. January observations form the training window.
3. February–December observations are held out as the evaluation period.
4. Model parameters are selected using only the January training data.
5. Forecasts are generated for the full February–December horizon.
6. MAD and MAPE are calculated against the held-out actual prices.

The trend and seasonal components are estimated exclusively from January. This prevents future observations from influencing the forecast construction.

## Results

| Year | Best method by MAD | MAD | MAPE |
|---|---|---:|---:|
| 2023 | Naive | 31.56 | 17.62% |
| 2024 | Moving Average (n=2) | 29.14 | 13.25% |

The results show an important practical point: with only January available for training, more complex trend-based forecasts do not automatically outperform simple level-based baselines. The simple methods were more competitive in both evaluation periods.

### Full model comparison

| Year | Method | MAD | MAPE |
|---|---|---:|---:|
| 2023 | Naive | 31.56 | 17.62% |
| 2023 | MA (n=2) | 32.20 | 17.98% |
| 2023 | SES (alpha=0.9) | 31.66 | 17.67% |
| 2023 | Linear Trend | 95.29 | 53.20% |
| 2023 | Trend + Seasonal | 95.32 | 53.22% |
| 2024 | Naive | 29.98 | 13.58% |
| 2024 | MA (n=2) | 29.14 | 13.25% |
| 2024 | SES (alpha=0.9) | 29.79 | 13.50% |
| 2024 | Linear Trend | 35.75 | 17.42% |
| 2024 | Trend + Seasonal | 35.78 | 17.44% |

## Reference-Class Adjustment

The original coursework included a reference-class adjustment using ten comparable technology companies. The available project files do not contain the required external peer datasets, while the previous implementation generated synthetic peer series. That approach does not provide sufficient evidence for a defensible empirical claim.

Rather than present synthetic results as real comparable-company evidence, the peer adjustment has been excluded from the final analytical workflow. The repository therefore focuses on the reproducible AAPL forecasting analysis that can be supported directly by the available data.

## Project Structure

```text
aapl-stock-exploratory-analysis/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── AAPL_Forecasting_Analysis.ipynb
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

The processed datasets are written to `data/processed/` and the forecast metrics, forecast tables and comparison outputs are written to `results/`.

## Limitations

This is a compact forecasting exercise rather than a production trading system. The evaluation uses one training window per year and focuses on closing-price levels rather than returns, volatility or transaction costs. The 21-trading-day seasonal component is a deliberately simple approximation of a monthly trading cycle.

## Author

**Dimitris Bechrakis**  
M.Sc. Data Science — The American College of Greece
