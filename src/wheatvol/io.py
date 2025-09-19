import pandas as pd

def load_prices(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, parse_dates=["Date"]).sort_values("Date").dropna()
    if "Close" not in df.columns:
        raise ValueError("CSV must contain 'Date' and 'Close' columns")
    return df
