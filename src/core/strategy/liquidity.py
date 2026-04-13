import pandas as pd
from typing import List, Dict


def find_equal_highs(
    df: pd.DataFrame,
    tolerance: float = 0.0001,
    min_touches: int = 2
) -> List[Dict]:
    """
    Detecta zonas de equal highs (liquidez).
    """
    highs = df['high'].values
    levels = []

    for i in range(len(highs)):
        base = highs[i]
        touches = []

        for j in range(len(highs)):
            if abs(highs[j] - base) <= tolerance:
                touches.append(j)

        if len(touches) >= min_touches:
            levels.append({
                "level": base,
                "touches": len(touches),
                "indices": touches
            })

    return levels


def find_equal_lows(
    df: pd.DataFrame,
    tolerance: float = 0.0001,
    min_touches: int = 2
) -> List[Dict]:
    """
    Detecta zonas de equal lows (liquidez).
    """
    lows = df['low'].values
    levels = []

    for i in range(len(lows)):
        base = lows[i]
        touches = []

        for j in range(len(lows)):
            if abs(lows[j] - base) <= tolerance:
                touches.append(j)

        if len(touches) >= min_touches:
            levels.append({
                "level": base,
                "touches": len(touches),
                "indices": touches
            })

    return levels