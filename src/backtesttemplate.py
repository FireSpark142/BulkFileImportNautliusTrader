from nautilus_trader.backtest.node import BacktestNode
from pathlib import Path
import pandas as pd
from instruhandler import instruhandle
from reporting import report
from backtestconfig import engine_config


def main(venue_str, strategy_p: str, strategy_config_p: str):
    intsr = instruhandle("../data")
    config = engine_config(venue_str, intsr, strategy_p, strategy_config_p)

    test = BacktestNode(config)

    test.run()

    enginels = test.get_engines()
    for l in enginels:
        report(l)



    ls = []
    p2 = "../reports/"
    root_directory = Path(p2)
    for d in root_directory.glob("*"):
        df = pd.read_csv(str(d))
        ls.append(df)
    dd = pd.concat(ls).dropna().mean()

    dd.to_csv('final_reports/final_results.csv', header=False)


main("NYSE", 'strategies:EMACross.py',
     'strategies:EMACrossConfig')
