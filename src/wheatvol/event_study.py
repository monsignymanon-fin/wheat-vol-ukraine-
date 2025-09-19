import pandas as pd

def event_windows(df: pd.DataFrame, event_date: pd.Timestamp, window_days: int = 60):
    ev = df.set_index("Date").loc[event_date - pd.Timedelta(days=120): event_date + pd.Timedelta(days=120)].copy()
    ev["abs_ret"] = ev["ret"].abs()
    pre = ev.loc[:event_date - pd.Timedelta(days=1)].tail(window_days)
    post = ev.loc[event_date:].head(window_days)
    return pre.reset_index(), post.reset_index()
