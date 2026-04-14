import MetaTrader5 as mt5
import json
import pandas as pd

from src.data.mt5_client import MT5Client
from src.data.transformer import rates_to_dataframe

from src.core.analysis.liquidity import (
    find_equal_highs,
    find_equal_lows
)

from src.core.analysis.sweep import SweepEngine
from src.core.analysis.mss import MSSEngine


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
    sweep_engine = SweepEngine()
    mss_engine = MSSEngine()

    try:
        # 1. Conectar a MT5
        client.connect()

        # 2. Obtener datos
        rates = client.get_rates("EURUSD", mt5.TIMEFRAME_M5, 50)

        # 3. Transformar a DataFrame
        df = rates_to_dataframe(rates)

        # =========================
        # 🧠 LIQUIDITY ENGINE
        # =========================
        eqh = find_equal_highs(df)
        eql = find_equal_lows(df)

        current_price = df["close"].iloc[-1]

        # Context filtering (opcional por ahora)
        buy_side = [l for l in eqh if l["level"] > current_price]
        sell_side = [l for l in eql if l["level"] < current_price]

        # =========================
        # 🐳 SWEEP ENGINE
        # =========================
        buy_sweeps = sweep_engine.detect_buy_side_sweeps(df, eqh)
        sell_sweeps = sweep_engine.detect_sell_side_sweeps(df, eql)

        print("BUY SIDE SWEEPS:", buy_sweeps)
        print("SELL SIDE SWEEPS:", sell_sweeps)

        # =========================
        # 🧠 MSS ENGINE
        # =========================
        bullish_mss = mss_engine.detect_bullish_mss(df, sell_sweeps)
        bearish_mss = mss_engine.detect_bearish_mss(df, buy_sweeps)

        # =========================
        # 📊 DEBUG OUTPUT (MSS)
        # =========================
        print("\n=== BULLISH MSS ===")
        print(bullish_mss)

        print("\n=== BEARISH MSS ===")
        print(bearish_mss)

    finally:
        # 4. Cerrar conexión
        client.shutdown()


if __name__ == "__main__":
    main()