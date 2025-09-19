# wheat-vol-ukraine

**Effet de la guerre en Ukraine (24/02/2022) sur la volatilité du blé**

Analyse de la persistance et de la mémoire longue (GARCH / EGARCH / GJR / FIGARCH), event study autour du 24/02/2022 et backtests de prévision de variance.

---

## Structure du dépôt
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
│ └─ config.yaml
├─ data/
│ ├─ README.md
│ └─ wheat.csv # (optionnel; ignoré par git si volumineux)
├─ notebooks/
│ └─ 01_explore.ipynb # (optionnel)
├─ src/
│ └─ wheatvol/
│ ├─ init.py
│ ├─ io.py
│ ├─ transforms.py
│ ├─ models.py
│ ├─ forecasting.py
│ ├─ event_study.py
│ ├─ evaluation.py
│ ├─ plots.py
│ └─ cli.py
├─ scripts/
│ ├─ run_fit.py
│ ├─ run_event_study.py
│ └─ run_backtest.py
├─ tests/
│ ├─ test_transforms.py
│ ├─ test_models.py
│ └─ test_event_study.py
└─ .github/
└─ workflows/
└─ ci.yml


---

## Quickstart

```bash
# Créer l'environnement Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .[dev]
pre-commit install
pytest -q

# Préparer les données
# Placez un CSV à data/wheat.csv avec les colonnes Date, Close

# Lancer le fit baseline (GARCH/EGARCH/FIGARCH)
python scripts/run_fit.py --config config/config.yaml

# Event study ±N jours autour du 24/02/2022
python scripts/run_event_study.py --config config/config.yaml

# Backtest rolling (1-step variance) + métriques
python scripts/run_backtest.py --config config/config.yaml
