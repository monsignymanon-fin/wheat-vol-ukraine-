.PHONY: setup test fit event backtest

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && pip install -e .[dev] && pre-commit install

test:
	pytest -q

fit:
	python scripts/run_fit.py --config config/config.yaml

event:
	python scripts/run_event_study.py --config config/config.yaml

backtest:
	python scripts/run_backtest.py --config config/config.yaml
