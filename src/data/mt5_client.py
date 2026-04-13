import MetaTrader5 as mt5
from datetime import datetime


class MT5Client:
    def __init__(self):
        self.connected = False

    def connect(self) -> None:
        if not mt5.initialize():
            raise Exception(f"MT5 initialize failed: {mt5.last_error()}")

        self.connected = True
        print("✅ Connected to MT5")

    def shutdown(self) -> None:
        mt5.shutdown()
        self.connected = False
        print("🔌 Disconnected from MT5")

    def get_rates(self, symbol: str, timeframe, count: int = 100):
        if not self.connected:
            raise Exception("MT5 is not connected")

        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)

        if rates is None:
            raise Exception(f"Failed to get rates: {mt5.last_error()}")

        return rates