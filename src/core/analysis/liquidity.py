import pandas as pd
from typing import List, Dict


def find_equal_highs(
    df: pd.DataFrame,
    tolerance: float = 0.0001,
    min_touches: int = 2
) -> List[Dict]:

    highs = df["high"].values
    levels = []

    for i in range(len(highs)):

        # 🧹 FIX 2: normalización FX
        base = round(highs[i], 5)

        # 🧹 FIX 1: evitar duplicados
        if any(abs(existing["level"] - base) <= tolerance for existing in levels):
            continue

        touches = []

        for j in range(len(highs)):

            # 🧹 FIX 3: early pruning con bucket
            bucket_i = round(highs[j] / tolerance) * tolerance
            bucket_base = round(base / tolerance) * tolerance

            if abs(bucket_i - bucket_base) <= tolerance:
                touches.append(j)

        if len(touches) >= max(min_touches, 5):
            levels.append({
                "level": base,
                "touches": len(touches),
                "indices": touches
            })

    levels.sort(key=lambda x: x["touches"], reverse=True)

    return levels


def find_equal_lows(
    df: pd.DataFrame,
    tolerance: float = 0.0001,
    min_touches: int = 2
) -> List[Dict]:

    lows = df["low"].values
    levels = []

    for i in range(len(lows)):

        base = round(lows[i], 5)

        if any(abs(existing["level"] - base) <= tolerance for existing in levels):
            continue

        touches = []

        for j in range(len(lows)):

            bucket_i = round(lows[j] / tolerance) * tolerance
            bucket_base = round(base / tolerance) * tolerance

            if abs(bucket_i - bucket_base) <= tolerance:
                touches.append(j)

        if len(touches) >= max(min_touches, 5):
            levels.append({
                "level": base,
                "touches": len(touches),
                "indices": touches
            })

    levels.sort(key=lambda x: x["touches"], reverse=True)

    return levels