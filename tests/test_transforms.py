import pandas as pd
from wheatvol.transforms import log_returns_pct

def test_log_returns_pct_basic():
    df = pd.DataFrame({"Date": pd.date_range("2020-01-01", periods=3), "Close": [100, 105, 110]})
    out = log_returns_pct(df)
    assert out.shape[0] == 2
    assert "ret" in out.columns
