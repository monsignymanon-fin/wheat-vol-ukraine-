# wheat-vol-ukraine

**Effet de la guerre en Ukraine (24/02/2022) sur la volatilité du blé**

Analyse de la persistance et de la mémoire longue (GARCH / EGARCH / GJR / FIGARCH), event study autour du 24/02/2022 et backtests de prévision de variance.

## 🗂️ Structure du dépôt
```
wheat-vol-ukraine/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ .pre-commit-config.yaml
├─ pyproject.toml
├─ requirements.txt
├─ Makefile
├─ CITATION.cff
├─ config/
│  └─ config.yaml
├─ data/
│  ├─ README.md
│  └─ wheat.csv        # (ignored if too big)
├─ notebooks/
│  └─ 01_explore.ipynb # (option)
│  └─ wheatvol/
│     ├─ __init__.py
│     ├─ io.py
│     ├─ transforms.py
│     ├─ models.py
│     ├─ forecasting.py
│     ├─ event_study.py
│     ├─ evaluation.py
│     ├─ plots.py
│     └─ cli.py
├─ scripts/
│  ├─ run_fit.py
│  ├─ run_event_study.py
│  └─ run_backtest.py
├─ tests/
│  ├─ test_transforms.py
│  ├─ test_models.py
│  └─ test_event_study.py
└─ .github/
   └─ workflows/
      └─ ci.yml
```

## 🚀 Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .[dev]
pre-commit install
pytest -q

# Placez un CSV à data/wheat.csv (Date, Close), puis :
python scripts/run_fit.py --config config/config.yaml
python scripts/run_event_study.py --config config/config.yaml
python scripts/run_backtest.py --config config/config.yaml
```
(test workflow run)
test: trigger workflow
