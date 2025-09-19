import numpy as np
import pandas as pd

def mse_variance(sq_ret: pd.Series, var_fcst: pd.Series) -> float:
    return float(np.nanmean((sq_ret - var_fcst) ** 2))

def qlike(sq_ret: pd.Series, var_fcst: pd.Series) -> float:
    return float(np.nanmean(np.log(var_fcst) + sq_ret / var_fcst))
