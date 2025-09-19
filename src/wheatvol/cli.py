from pathlib import Path
import yaml
import pandas as pd
from .io import load_prices
from .transforms import log_returns_pct, split_pre_post
from .models import fit_model, garch_persistence, figarch_d, ljung_box
from .forecasting import rolling_garch_var
from .event_study import event_windows
from .evaluation import mse_variance, qlike
from .plots import save_line

def run_all(cfg_path: str):
    cfg = yaml.safe_load(Path(cfg_path).read_text())
    data_csv = cfg["paths"]["data_csv"]
    cutoff = pd.Timestamp(cfg["cutoff_date"])

    df = load_prices(data_csv)
    df = log_returns_pct(df)

    pre, post = split_pre_post(df, cutoff)

    art_dir = Path(cfg["paths"].get("artifacts_dir", "artifacts"))
    (art_dir / "figures").mkdir(parents=True, exist_ok=True)
    (art_dir / "tables").mkdir(parents=True, exist_ok=True)

    # Fit models pre/post
    summaries = []
    for m in cfg["models"]:
        name, dist = m["name"], m.get("dist", "t")
        res_pre = fit_model(pre["ret"], vol_model=name, dist=dist, figarch_cfg=cfg.get("figarch"))
        res_post= fit_model(post["ret"], vol_model=name, dist=dist, figarch_cfg=cfg.get("figarch"))
        if name == "GARCH":
            pers_pre = garch_persistence(res_pre)
            pers_post = garch_persistence(res_post)
            summaries += [(name, "pre", pers_pre), (name, "post", pers_post)]
        if name == "FIGARCH":
            d_pre = figarch_d(res_pre)
            d_post = figarch_d(res_post)
            summaries += [(name+".d", "pre", d_pre), (name+".d", "post", d_post)]
        # diagnostics
        lb_pre = ljung_box(res_pre)
        lb_post = ljung_box(res_post)
        summaries += [(name+"_LBp", "pre", lb_pre[1]), (name+"_LBp", "post", lb_post[1])]

        # sauvegarder summary texte
        (art_dir/"tables"/f"{name}_pre_summary.txt").write_text(str(res_pre.summary()))
        (art_dir/"tables"/f"{name}_post_summary.txt").write_text(str(res_post.summary()))

    # Event study
    pre_w, post_w = event_windows(df, cutoff, cfg["event_study"]["window_days"])
    pre_mean = pre_w["abs_ret"].mean(); post_mean = post_w["abs_ret"].mean()
    summaries += [("EventAbsMean", "pre", pre_mean), ("EventAbsMean", "post", post_mean)]

    # Rolling forecast (GARCH)
    var_fcst = rolling_garch_var(df["ret"], start_idx=cfg["rolling_forecast"]["start_idx"])
    df_out = df.copy(); df_out["var_garch_1d"] = var_fcst; df_out["sq_ret"] = df_out["ret"]**2
    mse = mse_variance(df_out["sq_ret"], df_out["var_garch_1d"])
    ql  = qlike(df_out["sq_ret"], df_out["var_garch_1d"])
    summaries += [("Backtest_MSE", "all", mse), ("Backtest_QLIKE", "all", ql)]

    # Export tableaux
    import pandas as pd
    pd.DataFrame(summaries, columns=["metric", "segment", "value"]).to_csv(art_dir/"tables"/"summary.csv", index=False)

    # Figures simples
    save_line(df_out, x="Date", ys=["ret"], out=art_dir/"figures"/"returns.png", title="Log-returns (%)")
    save_line(df_out, x="Date", ys=["sq_ret", "var_garch_1d"], out=art_dir/"figures"/"var_backtest.png", title="Squared returns vs 1d GARCH variance")
