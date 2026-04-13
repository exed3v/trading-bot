import MetaTrader5 as mt5
import json
import pandas as pd

from src.data.mt5_client import MT5Client
from src.data.transformer import rates_to_dataframe

from src.core.analysis.liquidity import (
    find_equal_highs,
    find_equal_lows
)


# =========================
# 🔧 DEBUG UTILITY
# =========================
def debug_print(title, data):
    print(f"\n=== {title} ===")
    print(json.dumps(data, indent=2, default=str))


# =========================
# 🚀 MAIN FLOW
# =========================
def main():
    client = MT5Client()

    try:
        # 1. Conectar a MT5
        client.connect()

        # 2. Obtener datos
        rates = client.get_rates("EURUSD", mt5.TIMEFRAME_M5, 50)

        # 3. Transformar a DataFrame
        df = rates_to_dataframe(rates)

        # =========================
        # 🧠 MARKET DATA
        # =========================
        eqh = find_equal_highs(df)
        eql = find_equal_lows(df)

        current_price = df["close"].iloc[-1]

        # =========================
        # 🎯 CONTEXT FILTERING
        # =========================
        buy_side = [l for l in eqh if l["level"] > current_price]
        sell_side = [l for l in eql if l["level"] < current_price]

        # =========================
        # 🐞 DEBUG OUTPUT
        # =========================
        debug_print("BUY SIDE LIQUIDITY", buy_side)
        debug_print("SELL SIDE LIQUIDITY", sell_side)

    finally:
        # 4. Cerrar conexión
        client.shutdown()


if __name__ == "__main__":
    main()