# Data

The repository separates raw source data from processed analysis files.

- `raw/` contains the source AAPL daily dataset used by the preprocessing script.
- `processed/` contains the cleaned year-level datasets consumed by the forecasting workflow.

The large raw dataset is intentionally not duplicated in the public repository. Place the source file at `data/raw/AAPL_daily_2023_2024_raw.csv` before running the preprocessing step.