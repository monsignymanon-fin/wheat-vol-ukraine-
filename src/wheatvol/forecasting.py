import numpy as np
import pandas as pd
from arch import arch_model

def rolling_garch_var(y: pd.Series, start_idx: int = 500) -> pd.Series:
    y = y.dropna().values
    var_fcst = np.full_like(y, np.nan, dtype=float)
    for t in range(start_idx, len(y)):
        am = arch_model(y[:t], mean="Constant", vol="GARCH", p=1, q=1, dist="t")
        res = am.fit(disp="off")
        f = res.forecast(horizon=1, reindex=False)
        var_fcst[t] = f.variance.values[-1, 0]
    return pd.Series(var_fcst)
