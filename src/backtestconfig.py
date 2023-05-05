import os
import shutil
from nautilus_trader.backtest.engine import BacktestEngine, Decimal
from nautilus_trader.backtest.models import FillModel
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig, RiskEngineConfig, ImportableStrategyConfig, \
    BacktestVenueConfig, BacktestDataConfig, BacktestRunConfig
from nautilus_trader.core.rust.model import OmsType, AccountType
from nautilus_trader.data.engine import ParquetDataCatalog
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data.bar import Bar
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Money
from nautilus_trader.persistence.external.core import process_files
from nautilus_trader.persistence.external.readers import TextReader
from nautilus_trader.persistence.migrate import write_objects
from nautilus_trader.test_kit.providers import TestInstrumentProvider

from parser import parser


def engine_config( venue_str: str,
                  instrum: list, strategy_p: str, strategy_config_p: str):

    ls = []

    CATALOG_PATH = "../catalog"

    fill_model = FillModel(
        prob_fill_on_limit=0.2,
        prob_fill_on_stop=0.95,
        prob_slippage=0.5,
        random_seed=42,
    )

    # Configure backtest engine
    config = BacktestEngineConfig(
        trader_id="BACKTESTER-001",
        logging=LoggingConfig(
            bypass_logging=True
        ),
        risk_engine=RiskEngineConfig(
            bypass=True,  # Example of bypassing pre-trade risk checks for backtests
        ),
    )

    NYSE = Venue(venue_str)

    engine = BacktestEngine(config=config)

    engine.add_venue(
        venue=NYSE,
        oms_type=OmsType.HEDGING,  # Venue will generate position IDs
        account_type=AccountType.MARGIN,
        base_currency=USD,  # Standard single-currency account
        starting_balances=[Money(1_000_000, USD)],  # Single-currency or multi-currency accounts
        fill_model=fill_model,
    )

    catalog = ParquetDataCatalog(CATALOG_PATH)

    process_files(
        glob_path="../data/*",
        reader=TextReader(line_parser=parser),
        catalog=catalog,
    )

    for i in instrum:
        instru = TestInstrumentProvider.equity(i, venue_str)
        ### COMMENT OUT THE FOLLOWING LINE
        write_objects(catalog, [instru])

        instrument = catalog.instruments(instrument_ids=[str(instru.id)], as_nautilus=True)[0]

        srs = catalog.bars([instrument.id.value])['bar_type'].drop_duplicates().tolist()

        # print(srs)

        for i in srs:
            # print(instrument.id.value)
            venues_config = [
                BacktestVenueConfig(
                    name="NYSE",
                    oms_type="HEDGING",
                    account_type="MARGIN",
                    base_currency="USD",
                    starting_balances=["1_000_000 USD"],
                )
            ]

            data_config = [
                BacktestDataConfig(
                    catalog_path=str(CATALOG_PATH),
                    data_cls=Bar,
                    instrument_id=instrument.id.value
                )
            ]

            strategies = [
                ImportableStrategyConfig(
                    strategy_path=strategy_p,
                    config_path=strategy_config_p,
                    config=dict(
                        instrument_id=instrument.id.value,
                        bar_type=i,
                        fast_ema_period=10,
                        slow_ema_period=20,
                        trade_size=Decimal(1_00),
                    ),
                ),
            ]

            final_config = BacktestRunConfig(
                engine=BacktestEngineConfig(strategies=strategies),
                data=data_config,
                venues=venues_config,
            )
            ls.append(final_config)

    return ls
