import pandas as pd
from typing import List, Dict


class SweepEngine:
    """
    ICT Silver Bullet Sweep Detection Engine (Production-ready MVP)
    """

    def __init__(self, lookahead: int = 3, min_displacement: float = 0.0005):
        self.lookahead = lookahead
        self.min_displacement = min_displacement

    # --------------------------
    # PUBLIC API
    # --------------------------
    def detect_buy_side_sweeps(self, df: pd.DataFrame, eqh: List[Dict]) -> List[Dict]:
        return self._detect_sweeps(df, eqh, side="buy")

    def detect_sell_side_sweeps(self, df: pd.DataFrame, eql: List[Dict]) -> List[Dict]:
        return self._detect_sweeps(df, eql, side="sell")

    # --------------------------
    # CORE LOGIC
    # --------------------------
    def _detect_sweeps(self, df: pd.DataFrame, levels: List[Dict], side: str):

        highs = df["high"].values
        lows = df["low"].values
        closes = df["close"].values

        sweeps = []

        for level_data in levels:
            level = float(level_data["level"])

            for i in range(len(df) - self.lookahead):

                sweep_occurred = False

                # --------------------------
                # BUY SIDE SWEEP (highs)
                # --------------------------
                if side == "buy":

                    # 1. breakout wick
                    if highs[i] > level:

                        # 2. must close back below (rejection)
                        if closes[i] < level:

                            # 3. displacement confirmation
                            if self._has_displacement_down(closes, i):

                                sweeps.append({
                                    "type": "buy_side_sweep",
                                    "level": level,
                                    "index": i,
                                    "strength": level_data.get("touches", 0)
                                })

                # --------------------------
                # SELL SIDE SWEEP (lows)
                # --------------------------
                if side == "sell":

                    if lows[i] < level:

                        if closes[i] > level:

                            if self._has_displacement_up(closes, i):

                                sweeps.append({
                                    "type": "sell_side_sweep",
                                    "level": level,
                                    "index": i,
                                    "strength": level_data.get("touches", 0)
                                })

        return self._deduplicate_sweeps(sweeps)

    # --------------------------
    # DISPLACEMENT FILTER
    # --------------------------
    def _has_displacement_down(self, closes, i: int) -> bool:
        if i + 1 >= len(closes):
            return False
        return abs(closes[i + 1] - closes[i]) > self.min_displacement

    def _has_displacement_up(self, closes, i: int) -> bool:
        if i + 1 >= len(closes):
            return False
        return abs(closes[i + 1] - closes[i]) > self.min_displacement

    # --------------------------
    # CLEAN OUTPUT
    # --------------------------
    def _deduplicate_sweeps(self, sweeps: List[Dict]) -> List[Dict]:

        seen = set()
        unique = []

        for s in sweeps:
            key = (s["type"], s["level"], s["index"])

            if key not in seen:
                seen.add(key)
                unique.append(s)

        return sorted(unique, key=lambda x: x["strength"], reverse=True)