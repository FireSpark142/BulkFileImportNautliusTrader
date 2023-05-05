import datetime

import pandas as pd
from nautilus_trader.core.datetime import dt_to_unix_nanos
from nautilus_trader.model.data.bar import Bar, BarType
from nautilus_trader.model.objects import Price, Quantity

def parser(line):
    """ Parser function for hist_data FX data, for use with CSV Reader """
    Datetime, Open, High, Low, Close, Volume, Bar_Type = line.split(b",")
    dt = pd.Timestamp(datetime.datetime.strptime(Datetime.decode()[:19], "%Y-%m-%d %H:%M:%S"), tz='UTC')
    yield Bar(
        BarType.from_str(Bar_Type.decode()[:-1]),
        Price.from_str(Open.decode()),
        Price.from_str(High.decode()),
        Price.from_str(Low.decode()),
        Price.from_str(Close.decode()),
        Quantity.from_str(Volume.decode()),
        dt_to_unix_nanos(dt),
        dt_to_unix_nanos(dt),
    )
