from datetime import datetime
import pandas as pd


def get_current_ny_time() -> pd.Timestamp:
    """
    Retorna la hora actual en timezone New York.
    """
    return pd.Timestamp.now(tz="America/New_York")


def is_in_ny_am_session(current_time: pd.Timestamp) -> bool:
    """
    Valida si estamos dentro de la ventana NY AM (10:00 - 11:00).
    """
    start = current_time.replace(hour=10, minute=0, second=0, microsecond=0)
    end = current_time.replace(hour=11, minute=0, second=0, microsecond=0)

    return start <= current_time < end


def is_trading_time(current_time: pd.Timestamp) -> bool:
    return is_in_ny_am_session(current_time)


def is_trading_time_now() -> bool:
    current_time = get_current_ny_time()
    return is_trading_time(current_time)