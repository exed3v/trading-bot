import MetaTrader5 as mt5
from src.data.mt5_client import MT5Client
from src.data.transformer import rates_to_dataframe
import pandas as pd


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
        print("LAST:", df.tail(1))

        # 👇 DEBUG: hora actual NY
        print("NOW:", pd.Timestamp.now(tz="America/New_York"))

        df = rates_to_dataframe(rates)

        print(df.head())

    finally:
        # 4. Cerrar conexión
        client.shutdown()


if __name__ == "__main__":
    main()