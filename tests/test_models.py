import pandas as pd
import numpy as np
from wheatvol.models import fit_model

def test_fit_garch_runs():
    rng = np.random.default_rng(0)
    dates = pd.date_range("2020-01-01", periods=600)
    ret = pd.Series(rng.standard_normal(600), index=dates)
    res = fit_model(ret, vol_model="GARCH", dist="t")
    assert hasattr(res, "params")
