# HistoricalDataEngine
An engine config to bulk backtest csv files using Nautilus Trader



Linux / Gitbash Instructions
```
curl -sSL https://install.python-poetry.org | python3 -
poetry install
poetry run python src/backtesttemplate.py
```

Windows
```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
poetry install
poetry run python src/backtesttemplate.py
```

Put your strategies inside the src/strategies folder and in the main call inside backtesttemplate.py -

To call the strategy do the following:

```
main("NYSE", 'strategies:StrategyName.py',
     'strategies:StrategyConfigClass')

```