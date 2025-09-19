import pandas as pd
from wheatvol.event_study import event_windows

def test_event_windows_split():
    dates = pd.date_range("2022-02-01", "2022-04-01", freq="D")
    df = pd.DataFrame({"Date": dates, "ret": 0.0})
    pre, post = event_windows(df, pd.Timestamp("2022-02-24"), 5)
    assert len(pre) <= 5 and len(post) <= 5
