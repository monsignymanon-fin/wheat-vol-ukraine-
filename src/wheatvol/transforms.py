import numpy as np
import pandas as pd

DEF_RET_COL = "ret"

def log_returns_pct(df: pd.DataFrame, price_col: str = "Close") -> pd.DataFrame:
    out = df.copy()
    out[DEF_RET_COL] = 100 * np.log(out[price_col]).diff()
    out = out.dropna(subset=[DEF_RET_COL]).reset_index(drop=True)
    return out

def split_pre_post(df: pd.DataFrame, cutoff: pd.Timestamp) -> tuple[pd.DataFrame, pd.DataFrame]:
    pre = df[df["Date"] < cutoff].copy()
    post = df[df["Date"] >= cutoff].copy()
    return pre, post
