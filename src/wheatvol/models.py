from arch.univariate import ConstantMean, EGARCH, GARCH, FIGARCH, Normal, StudentsT, SkewStudent
from statsmodels.stats.diagnostic import acorr_ljungbox
import pandas as pd

DIST_MAP = {"normal": Normal, "t": StudentsT, "skewt": SkewStudent}

def fit_model(series: pd.Series, vol_model: str = "GARCH", dist: str = "t", figarch_cfg: dict | None = None):
    y = series.dropna()
    cm = ConstantMean(y)
    if vol_model == "GARCH":
        cm.volatility = GARCH(p=1, q=1)
    elif vol_model == "EGARCH":
        cm.volatility = EGARCH(p=1, o=1, q=1)
    elif vol_model == "FIGARCH":
        p = (figarch_cfg or {}).get("p", 1)
        q = (figarch_cfg or {}).get("q", 1)
        d_init = (figarch_cfg or {}).get("d_init", 0.2)
        cm.volatility = FIGARCH(p=p, q=q, d=d_init)
    else:
        raise ValueError("Unknown vol_model")

    cm.distribution = DIST_MAP.get(dist, StudentsT)()
    res = cm.fit(disp="off")
    return res

def garch_persistence(res) -> float:
    p = res.params
    alpha = p[[k for k in p.index if "alpha" in k]].sum()
    beta = p[[k for k in p.index if "beta" in k]].sum()
    return float(alpha + beta)

def figarch_d(res) -> float | float:
    p = res.params
    d_names = [k for k in p.index if k.lower().endswith(".d") or k.lower() == "d"]
    return float(p[d_names[0]]) if d_names else float("nan")

def ljung_box(res, lags: int = 20) -> tuple[float, float]:
    resid = res.std_resid.dropna()
    lb = acorr_ljungbox(resid, lags=[lags], return_df=True)
    row = lb.iloc[0]
    return float(row["lb_stat"]), float(row["lb_pvalue"])
