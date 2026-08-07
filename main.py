# ============================================================================
# ITC6002 FINAL PROJECT: YEARLY STATIC ANALYSIS (MONTHLY SEASONALITY p=21)
# ============================================================================
import matplotlib
matplotlib.use('Agg') # Fixes Windows crash

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats

# Try importing yfinance for Part E
try:
    import yfinance as yf
    HAS_YF = True
except ImportError:
    HAS_YF = False
    print("Notice: 'yfinance' not installed. Part E will use simulation.")

# Setup Output Directories
DIRS = {'processed': 'data/processed', 'results': 'results'}
for d in ['Part_B_2023', 'Part_C_2024', 'Part_D_Comparison', 'Part_E_Adjustment']:
    os.makedirs(f"{DIRS['results']}/{d}", exist_ok=True)

print("--- STARTING ANALYSIS (MONTHLY SEASONALITY p=21) ---")

# ============================================================================
# 1. LOAD PRE-PROCESSED DATA
# ============================================================================
try:
    # Load 2023
    df_23 = pd.read_csv(f"{DIRS['processed']}/AAPL_2023_cleaned.csv", parse_dates=['Date'], index_col='Date')
    # Load 2024
    df_24 = pd.read_csv(f"{DIRS['processed']}/AAPL_2024_cleaned.csv", parse_dates=['Date'], index_col='Date')
    # Load Monthly 2024 (for Part E)
    df_24_monthly = pd.read_csv(f"{DIRS['processed']}/AAPL_2024_monthly_sample.csv", parse_dates=['Date'], index_col='Date')
    
    print("SUCCESS: Loaded split data files.")

except FileNotFoundError:
    print("CRITICAL ERROR: Processed files not found. Run 'preprocessing.py' first.")
    exit()

# Extract Arrays
prices_2023 = df_23['Close Price'].values
dates_2023 = df_23.index
prices_2024 = df_24['Close Price'].values
dates_2024 = df_24.index
prices_monthly = df_24_monthly['Close Price'].values

# ============================================================================
# 2. METRICS & TABLE GENERATION
# ============================================================================
def calculate_mad(actual, forecast):
    return np.mean(np.abs(actual - forecast))

def calculate_mape(actual, forecast):
    with np.errstate(divide='ignore', invalid='ignore'):
        pct_errors = np.abs((actual - forecast) / actual)
    return np.mean(pct_errors) * 100

def get_metrics(actual, forecast):
    n = min(len(actual), len(forecast))
    return calculate_mad(actual[:n], forecast[:n]), calculate_mape(actual[:n], forecast[:n])

def save_table(df, folder, filename):
    """Saves a DataFrame as both a CSV and a high-quality PNG image of the table."""
    df.to_csv(f"{folder}/{filename}.csv", index=False)
    
    width = len(df.columns) * 2.0  # Adjust width for readability
    height = len(df) * 0.5 + 1.2
    
    fig, ax = plt.subplots(figsize=(width, height))
    ax.axis('off')
    
    table = ax.table(cellText=df.round(2).values, colLabels=df.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False); table.set_fontsize(10); table.scale(1, 1.8)
    
    # Bold the header
    for (row, col), cell in table.get_celld().items():
        if row == 0: cell.set_text_props(weight='bold')
    
    plt.title(f"{filename.replace('_', ' ').title()}", fontweight="bold", y=0.98)
    plt.tight_layout()
    plt.savefig(f"{folder}/{filename}.png", dpi=300, bbox_inches='tight')
    plt.close()

# ============================================================================
# 3. MODELS
# ============================================================================
def static_level_forecast(train_data, horizon, method, param=None):
    if method == 'Naive': level = train_data[-1]
    elif method == 'MA': level = np.mean(train_data[-param:])
    elif method == 'SES':
        level = train_data[0]
        for x in train_data[1:]: level = param * x + (1 - param) * level
    return np.full(horizon, level)

def static_trend_season_diagnosis(year_data, split_idx, p=21):
    """
    Fits Trend & Seasonality on the WHOLE YEAR.
    p = 21 (Monthly Cycle - Approx 21 Trading Days).
    """
    n = len(year_data)
    x = np.arange(n)
    
    # 1. Global Trend
    slope, intercept, _, _, _ = stats.linregress(x, year_data)
    trend_line = intercept + slope * x
    
    # 2. Global Seasonality
    detrended = year_data - trend_line
    seasonal_indices = []
    
    # Calculate average index for each day in the 21-day cycle
    for i in range(p):
        cycle_points = detrended[i::p]
        seasonal_indices.append(np.mean(cycle_points))
    seasonal_indices = np.array(seasonal_indices)
    
    # 3. Construct Forecast
    preds_trend = trend_line[split_idx:]
    horizon = len(preds_trend)
    start_cycle_idx = split_idx % p
    
    # Tile the 21-day pattern
    repeated_indices = np.tile(seasonal_indices, (horizon // p) + 2)
    preds_season_component = repeated_indices[start_cycle_idx : start_cycle_idx + horizon]
    
    preds_final = preds_trend + preds_season_component
    return preds_trend, preds_final

# ============================================================================
# 4. ANALYSIS ENGINE (SUBPLOTS)
# ============================================================================
def analyze_year(year_str, prices, dates, output_subfolder):
    print(f"\nProcessing {year_str}...")
    folder_path = f"{DIRS['results']}/{output_subfolder}"
    
    jan_mask = dates.month == 1
    train = prices[jan_mask]
    test = prices[~jan_mask]
    dates_test = dates[~jan_mask]
    dates_train = dates[jan_mask]
    
    split_idx = len(train)
    results = {}
    
    # --- A. LEVEL OPTIMIZATION ---
    # MA
    best_n, min_err = 2, float('inf')
    for n in range(2, 10):
        if n < len(train):
            val = [np.mean(train[i-n:i]) for i in range(n, len(train))]
            if val and np.mean(np.abs(train[n:] - val)) < min_err: best_n, min_err = n, np.mean(np.abs(train[n:] - val))
    # SES
    best_a, min_err = 0.5, float('inf')
    for a in np.linspace(0.1, 0.9, 9):
        lvl = train[0]; errs = []
        for x in train[1:]: lvl = a*x + (1-a)*lvl; errs.append(abs(x-lvl))
        if np.mean(errs) < min_err: best_a, min_err = a, np.mean(errs)

    h = len(test)
    f_naive = static_level_forecast(train, h, 'Naive')
    f_ma = static_level_forecast(train, h, 'MA', best_n)
    f_ses = static_level_forecast(train, h, 'SES', best_a)
    
    results['Naive'] = (*get_metrics(test, f_naive), f_naive)
    results[f'MA(n={best_n})'] = (*get_metrics(test, f_ma), f_ma)
    results[f'SES(a={best_a:.1f})'] = (*get_metrics(test, f_ses), f_ses)
    
    # --- B. TREND & SEASON (P=21) ---
    f_trend, f_season = static_trend_season_diagnosis(prices, split_idx, p=21)
    
    results['Trend_Linear'] = (*get_metrics(test, f_trend), f_trend)
    results['Season_Adjusted'] = (*get_metrics(test, f_season), f_season)
    
    # --- SAVE TABLES ---
    metrics_data = [{'Method': k, 'MAD': v[0], 'MAPE': v[1]} for k,v in results.items()]
    df_metrics = pd.DataFrame(metrics_data)
    save_table(df_metrics, folder_path, f'metrics_{year_str}')
    
    # Save Level Metrics Table (PNG)
    df_level = df_metrics[df_metrics['Method'].isin(['Naive', f'MA(n={best_n})', f'SES(a={best_a:.1f})'])].copy()
    save_table(df_level, folder_path, f'level_metrics_{year_str}')

    # --- PLOT 1: LEVEL SUBPLOTS ---
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    fig.suptitle(f'{year_str} Level Forecasting Methods', fontsize=14, fontweight='bold')
    
    methods = [('Naive', f_naive, 'r--'), (f'MA(n={best_n})', f_ma, 'b--'), (f'SES(a={best_a:.1f})', f_ses, 'g--')]
    for i, (name, forecast, style) in enumerate(methods):
        axes[i].plot(dates_train, train, 'k-', label='Training')
        axes[i].plot(dates_test, test, 'k:', alpha=0.5, label='Actual')
        axes[i].plot(dates_test, forecast, style, label=name)
        axes[i].set_ylabel('Price'); axes[i].legend(loc='upper left'); axes[i].grid(True, alpha=0.3)
        axes[i].set_title(name)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f"{folder_path}/plot_level_subplots.png"); plt.close()
    
    # --- PLOT 2: TREND & SEASON SUBPLOTS ---
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle(f'{year_str} Trend & Seasonality (Monthly Cycle p=21)', fontsize=14, fontweight='bold')
    
    axes[0].plot(dates_train, train, 'k-', label='Training')
    axes[0].plot(dates, prices, 'gray', alpha=0.3, label='Actual')
    axes[0].plot(dates_test, f_trend, 'orange', linestyle='--', linewidth=2, label='Linear Trend Only')
    axes[0].set_ylabel('Price'); axes[0].legend(loc='upper left'); axes[0].grid(True, alpha=0.3)
    axes[0].set_title("Trend Component")
    
    axes[1].plot(dates_train, train, 'k-', label='Training')
    axes[1].plot(dates, prices, 'gray', alpha=0.3, label='Actual')
    axes[1].plot(dates_test, f_season, 'purple', linestyle='-', linewidth=2, label='Trend + Seasonal (p=21)')
    axes[1].set_ylabel('Price'); axes[1].set_xlabel('Date'); axes[1].legend(loc='upper left'); axes[1].grid(True, alpha=0.3)
    axes[1].set_title("Seasonal Adjustment (Monthly Cycle)")
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f"{folder_path}/plot_trend_subplots.png"); plt.close()
    
    return df_metrics

# ============================================================================
# 5. EXECUTE
# ============================================================================
m23 = analyze_year("2023", prices_2023, dates_2023, "Part_B_2023")
m24 = analyze_year("2024", prices_2024, dates_2024, "Part_C_2024")

print("\nGenerating Comparison...")
m23['Base'] = m23['Method'].apply(lambda x: x.split('(')[0])
m24['Base'] = m24['Method'].apply(lambda x: x.split('(')[0])

comp = pd.merge(m23[['Method', 'MAD', 'MAPE', 'Base']], 
                m24[['Method', 'MAD', 'MAPE', 'Base']], 
                on='Base', suffixes=('_23', '_24'))

comp['MAD_Diff'] = comp['MAD_24'] - comp['MAD_23']
comp['MAPE_Diff'] = comp['MAPE_24'] - comp['MAPE_23']

final_comp = comp[['Method_23', 'MAD_23', 'MAPE_23', 'Method_24', 'MAD_24', 'MAPE_24', 'MAD_Diff', 'MAPE_Diff']]

save_table(final_comp, f"{DIRS['results']}/Part_D_Comparison", 'comparison_table')

print("\nGenerating Part E Adjustment...")
base_val = prices_2023[-1] 
forecast = np.full(len(prices_monthly), base_val)

af_ratios = []
if HAS_YF:
    try:
        peers = ['MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'AMD', 'INTC', 'IBM', 'ORCL']
        data = yf.download(peers, start='2024-01-01', end='2024-12-31', interval='1mo', threads=False)['Close']
        for t in peers:
            if t in data:
                clean_act = data[t].dropna().values
                if len(clean_act) > 0: af_ratios.extend(clean_act / clean_act[0])
    except: pass
if not af_ratios: af_ratios = np.random.normal(1.12, 0.1, 120)

mu = np.mean(af_ratios)
adj_forecast = forecast * mu

mad_o, mape_o = get_metrics(prices_monthly, forecast)
mad_a, mape_a = get_metrics(prices_monthly, adj_forecast)
e_metrics = pd.DataFrame({'Metric': ['MAD', 'MAPE'], 'Original': [mad_o, mape_o], 'Adjusted': [mad_a, mape_a]})
save_table(e_metrics, f"{DIRS['results']}/Part_E_Adjustment", 'part_e_metrics')

plt.figure(figsize=(10, 6))
plt.plot(df_24_monthly.index, prices_monthly, 'ko-', label='Actual Monthly')
plt.plot(df_24_monthly.index, forecast, 'b--', label='Original Static')
plt.plot(df_24_monthly.index, adj_forecast, 'r-', label=f'Adjusted (x{mu:.2f})')
plt.title('Part E: Reference Class Adjustment'); plt.legend()
plt.savefig(f"{DIRS['results']}/Part_E_Adjustment/adjustment_plot.png"); plt.close()

print("\n✅ DONE. Analysis complete.")
print("\n All output files are in the results folder.")
