import pandas as pd
import numpy as np
import os

# Create a directory for the processed datasets
output_dir = 'AAPL_processed_datasets'
os.makedirs(output_dir, exist_ok=True)

# Load the raw data
df = pd.read_csv('AAPL_daily_2023_2024_raw.csv')

print("Original data shape:", df.shape)
print("First few rows of raw data:")
print(df.head(3))

# Step 1: Fix column headers and remove bad rows
df_clean = df.copy()
df_clean = df_clean.drop(0).reset_index(drop=True)
df_clean.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']

# Step 2: Convert data types
df_clean['Date'] = pd.to_datetime(df_clean['Date'])
numeric_columns = ['Close', 'High', 'Low', 'Open', 'Volume']
for col in numeric_columns:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

# Remove any missing values
df_clean = df_clean.dropna()

print(f"\nCleaned data shape: {df_clean.shape}")

# Step 3: Create main forecasting dataset and rename 'Close' to 'Price'
# REASON: We're forecasting the daily closing price, so 'Price' is more intuitive
forecast_df = df_clean[['Date', 'Close']].copy()
forecast_df = forecast_df.rename(columns={'Close': 'Price'})  # Renamed for clarity
forecast_df = forecast_df.sort_values('Date').reset_index(drop=True)

# Step 4: Split into years
year_2023 = forecast_df[forecast_df['Date'].dt.year == 2023].copy()
year_2024 = forecast_df[forecast_df['Date'].dt.year == 2024].copy()

# Step 5: Split each year into January vs Feb-Dec
jan_2023 = year_2023[year_2023['Date'].dt.month == 1].copy()
feb_dec_2023 = year_2023[year_2023['Date'].dt.month > 1].copy()

jan_2024 = year_2024[year_2024['Date'].dt.month == 1].copy()
feb_dec_2024 = year_2024[year_2024['Date'].dt.month > 1].copy()

# Step 6: Export all datasets as separate CSV files

# Main cleaned dataset
forecast_df.to_csv(f'{output_dir}/AAPL_clean_full.csv', index=False)
print(f"✓ Full cleaned dataset: {len(forecast_df)} rows")

# Year datasets
year_2023.to_csv(f'{output_dir}/AAPL_2023_full.csv', index=False)
year_2024.to_csv(f'{output_dir}/AAPL_2024_full.csv', index=False)
print(f"✓ Year 2023: {len(year_2023)} rows")
print(f"✓ Year 2024: {len(year_2024)} rows")

# Monthly splits for forecasting
jan_2023.to_csv(f'{output_dir}/AAPL_jan_2023.csv', index=False)
feb_dec_2023.to_csv(f'{output_dir}/AAPL_feb_dec_2023.csv', index=False)
jan_2024.to_csv(f'{output_dir}/AAPL_jan_2024.csv', index=False)
feb_dec_2024.to_csv(f'{output_dir}/AAPL_feb_dec_2024.csv', index=False)

print(f"✓ January 2023: {len(jan_2023)} rows")
print(f"✓ February-December 2023: {len(feb_dec_2023)} rows")
print(f"✓ January 2024: {len(jan_2024)} rows")
print(f"✓ February-December 2024: {len(feb_dec_2024)} rows")

# Step 7: Also create datasets with only the first day of each month (for Part E)
first_day_2023 = year_2023[year_2023['Date'].dt.day == 1].copy()
first_day_2024 = year_2024[year_2024['Date'].dt.day == 1].copy()

first_day_2023.to_csv(f'{output_dir}/AAPL_first_day_month_2023.csv', index=False)
first_day_2024.to_csv(f'{output_dir}/AAPL_first_day_month_2024.csv', index=False)

print(f"✓ First day of each month 2023: {len(first_day_2023)} rows")
print(f"✓ First day of each month 2024: {len(first_day_2024)} rows")

# Step 8: Create a summary file with explanation
summary = {
    'Dataset': [
        'Full Cleaned Data',
        'Year 2023 Full',
        'Year 2024 Full', 
        'January 2023',
        'Feb-Dec 2023',
        'January 2024',
        'Feb-Dec 2024',
        'First Day Each Month 2023',
        'First Day Each Month 2024'
    ],
    'Rows': [
        len(forecast_df),
        len(year_2023),
        len(year_2024),
        len(jan_2023),
        len(feb_dec_2023),
        len(jan_2024),
        len(feb_dec_2024),
        len(first_day_2023),
        len(first_day_2024)
    ],
    'Date Range': [
        f"{forecast_df['Date'].min().date()} to {forecast_df['Date'].max().date()}",
        f"{year_2023['Date'].min().date()} to {year_2023['Date'].max().date()}",
        f"{year_2024['Date'].min().date()} to {year_2024['Date'].max().date()}",
        f"{jan_2023['Date'].min().date()} to {jan_2023['Date'].max().date()}",
        f"{feb_dec_2023['Date'].min().date()} to {feb_dec_2023['Date'].max().date()}",
        f"{jan_2024['Date'].min().date()} to {jan_2024['Date'].max().date()}",
        f"{feb_dec_2024['Date'].min().date()} to {feb_dec_2024['Date'].max().date()}",
        f"{first_day_2023['Date'].min().date()} to {first_day_2023['Date'].max().date()}",
        f"{first_day_2024['Date'].min().date()} to {first_day_2024['Date'].max().date()}"
    ],
    'Note': [
        'Daily closing prices renamed from "Close" to "Price" for clarity',
        '2023 daily prices for Year 1 forecasting',
        '2024 daily prices for Year 2 forecasting',
        'Base data for forecasting Feb-Dec 2023',
        'Actual data to compare forecasts against',
        'Base data for forecasting Feb-Dec 2024',
        'Actual data to compare forecasts against',
        'Monthly data points for Part E analysis',
        'Monthly data points for Part E analysis'
    ]
}

summary_df = pd.DataFrame(summary)
summary_df.to_csv(f'{output_dir}/dataset_summary.csv', index=False)

print(f"\n🎉 All datasets exported to '{output_dir}' folder!")
print("\nDataset Summary:")
print(summary_df.to_string(index=False))

# Verify files were created and show column names
print(f"\n📁 Files created in '{output_dir}':")
for file in os.listdir(output_dir):
    file_path = os.path.join(output_dir, file)
    file_size = os.path.getsize(file_path)
    if file.endswith('.csv') and file != 'dataset_summary.csv':
        sample_df = pd.read_csv(file_path, nrows=1)
        print(f"  - {file} ({file_size} bytes) | Columns: {list(sample_df.columns)}")
    else:
        print(f"  - {file} ({file_size} bytes)")

# Additional explanation
print(f"\n📝 **Column Renaming Explanation:**")
print(f"   - Original column 'Close' was renamed to 'Price'")
print(f"   - Reason: We're forecasting daily closing prices, so 'Price' is more intuitive")
print(f"   - This makes the datasets clearer for analysis and reporting")
print(f"   - All datasets now have consistent columns: ['Date', 'Price']")
