import pandas as pd


def rates_to_dataframe(rates) -> pd.DataFrame:
    df = pd.DataFrame(rates)

    # ❌ NO usar utc=True
    df['time'] = pd.to_datetime(df['time'], unit='s')

    # ⚠️ Definir timezone del broker manualmente
    df['time'] = df['time'].dt.tz_localize('Etc/GMT-3')  # ajustar si hace falta

    # Convertir a NY
    df['time'] = df['time'].dt.tz_convert('America/New_York')

    df = df.sort_values(by='time')
    df.set_index('time', inplace=True)

    return df