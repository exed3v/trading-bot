import MetaTrader5 as mt5
from src.data.mt5_client import MT5Client
from src.data.transformer import rates_to_dataframe
import pandas as pd
from src.core.session.session_filter import is_trading_time, is_in_ny_am_session, is_trading_time_now
from src.core.strategy.liquidity import find_equal_highs, find_equal_lows


def main():
    client = MT5Client()

    try:
        # 1. Conectar
        client.connect()

        # 2. Obtener velas EURUSD M5
        rates = client.get_rates("EURUSD", mt5.TIMEFRAME_M5, 50)

        # 3. Mostrar resultados
        # print(f"📊 Velas obtenidas: {len(rates)}")

        # for candle in rates[:5]:
        #     print(candle)

        df = rates_to_dataframe(rates)

        # 👇 DEBUG: última vela
        # print("LAST:", df.tail(1))

        # 👇 DEBUG: hora actual NY
        # print("NOW:", pd.Timestamp.now(tz="America/New_York"))

        # print("IS TRADING TIME:", is_trading_time())

        fake_time = pd.Timestamp("2026-04-13 10:30:00", tz="America/New_York")

        # 👇 DEBUG: para ver si se ejecuta en la ventana 10M a 11AM
        # print("FAKE TIME:", fake_time)
        # print("IN SESSION:", is_in_ny_am_session(fake_time))
        # print("TRADING TIME:", is_trading_time(fake_time))
        # print("NOW:", is_trading_time_now())

        # 👇 DEBUG: Datos de MT5
        # print(df.head())

        eqh = find_equal_highs(df)
        eql = find_equal_lows(df)

        print("EQH:", eqh[:3])
        print("EQL:", eql[:3])

    finally:
        # 4. Cerrar conexión
        client.shutdown()


if __name__ == "__main__":
    main()