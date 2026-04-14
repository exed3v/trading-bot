import pandas as pd
from typing import List, Dict


class MSSEngine:
    """
    Market Structure Shift Engine (ICT - Production MVP)
    Detecta cambio real de estructura después de un sweep.
    """

    def detect_bullish_mss(
        self,
        df: pd.DataFrame,
        sweeps: List[Dict],
        lookahead: int = 5
    ) -> List[Dict]:

        return self._detect_mss(df, sweeps, direction="bullish", lookahead=lookahead)

    def detect_bearish_mss(
        self,
        df: pd.DataFrame,
        sweeps: List[Dict],
        lookahead: int = 5
    ) -> List[Dict]:

        return self._detect_mss(df, sweeps, direction="bearish", lookahead=lookahead)

    # ----------------------------
    # CORE LOGIC
    # ----------------------------
    def _detect_mss(
        self,
        df: pd.DataFrame,
        sweeps: List[Dict],
        direction: str,
        lookahead: int
    ) -> List[Dict]:

        highs = df["high"].values
        lows = df["low"].values

        mss_events = []

        for sweep in sweeps:

            sweep_index = sweep["index"]

            # rango posterior al sweep
            end = min(len(df), sweep_index + lookahead)

            if direction == "bullish":

                # MSS bullish = break of structure hacia arriba
                for i in range(sweep_index + 1, end):

                    if highs[i] > sweep["level"]:

                        mss_events.append({
                            "type": "bullish_mss",
                            "index": i,
                            "level_broken": sweep["level"],
                            "sweep_index": sweep_index
                        })
                        break

            elif direction == "bearish":

                # MSS bearish = break of structure hacia abajo
                for i in range(sweep_index + 1, end):

                    if lows[i] < sweep["level"]:

                        mss_events.append({
                            "type": "bearish_mss",
                            "index": i,
                            "level_broken": sweep["level"],
                            "sweep_index": sweep_index
                        })
                        break

        return mss_events