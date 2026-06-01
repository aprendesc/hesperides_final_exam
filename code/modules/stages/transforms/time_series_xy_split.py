"""TimeSeriesXYSplit — Constructs features and target from OHLCV data.

Default behaviour (feature_groups=["sma"]) is identical to the baseline:
one feature, SMA_{sma_window} of daily returns.

Students can enable richer feature groups via the YAML param `feature_groups`.
Available groups and the features they add:

  "sma"        → sma_{sma_window}            (baseline — rolling mean of returns)
  "momentum"   → mom_1d/3d/5d/10d/20d/60d   (price % changes at multiple horizons)
  "rsi"        → rsi_14                      (RSI momentum/mean-reversion indicator)
  "volatility" → vol_5d, vol_20d, atr        (realised vol + intraday range)
  "bollinger"  → bb_pct, bb_width            (position in / width of Bollinger Bands)
  "volume"     → vol_ratio, vol_change        (volume vs its 20-day average)
  "calendar"   → dow                         (day-of-week: 0=Mon … 4=Fri)

Example YAML (students):
  xy_split:
    class: "code.modules.stages.transforms.time_series_xy_split.TimeSeriesXYSplit"
    params:
      target: "binary_direction_1d"
      sma_window: 20
      feature_groups: ["sma", "momentum", "rsi", "volatility", "bollinger", "volume"]
"""

import pandas as pd
import numpy as np


class TimeSeriesXYSplit:
    def __init__(self, target: str = "binary_direction_1d", sma_window: int = 20,
                 feature_groups: list = None, **kwargs):
        self.target = target
        self.sma_window = sma_window
        # Default: only SMA — preserves baseline behaviour
        self.feature_groups = feature_groups if feature_groups is not None else ["sma"]

    def fit(self, X=None, y=None, metadata=None, **kwargs):
        return X, y, metadata or {}

    def transform(self, X, y=None, metadata=None, **kwargs):
        metadata = metadata or {}
        df = X.copy()
        df = df.sort_values("Date").reset_index(drop=True)

        # Daily return — base of most features and all targets
        df["pct_return_1d"] = df["Close"].pct_change()

        # ── Target ────────────────────────────────────────────────────────────
        if self.target == "binary_direction_1d":
            # 1 if tomorrow's close > today's close, else 0
            df["target"] = (df["pct_return_1d"].shift(-1) > 0).astype(int)
        elif self.target == "pct_return_1d":
            df["target"] = df["pct_return_1d"].shift(-1)
        elif self.target == "log_return_1d":
            df["target"] = np.log(df["Close"].shift(-1) / df["Close"])
        else:
            raise ValueError(f"Unknown target: {self.target}")

        feature_cols = []

        # ── Feature groups ─────────────────────────────────────────────────────

        if "sma" in self.feature_groups:
            # Rolling mean of daily returns — baseline feature
            col = f"sma_{self.sma_window}"
            df[col] = df["pct_return_1d"].rolling(window=self.sma_window).mean()
            feature_cols.append(col)

        if "momentum" in self.feature_groups:
            # Price % change over multiple lookback horizons.
            # Empirically shows short-term mean-reversion (negative autocorrelation)
            # and medium-term momentum — useful for tree-based models.
            for w in [1, 3, 5, 10, 20, 60]:
                col = f"mom_{w}d"
                df[col] = df["Close"].pct_change(w)
                feature_cols.append(col)

        if "rsi" in self.feature_groups:
            # RSI(14): classic overbought/oversold indicator.
            # High RSI → mean-reversion signal (slightly bearish next day).
            delta = df["Close"].diff()
            gain = delta.clip(lower=0).rolling(14).mean()
            loss = (-delta.clip(upper=0)).rolling(14).mean()
            df["rsi_14"] = 100 - 100 / (1 + gain / (loss + 1e-9))
            feature_cols.append("rsi_14")

        if "volatility" in self.feature_groups:
            # Realised volatility at two horizons + intraday range proxy.
            # Volatility clustering means current vol predicts near-future vol,
            # which interacts with direction signals (e.g. high-vol bounces).
            df["vol_5d"]  = df["pct_return_1d"].rolling(5).std()
            df["vol_20d"] = df["pct_return_1d"].rolling(20).std()
            # ATR proxy: (High - Low) / Close — intraday fear gauge
            df["atr"] = (df["High"] - df["Low"]) / df["Close"]
            feature_cols.extend(["vol_5d", "vol_20d", "atr"])

        if "bollinger" in self.feature_groups:
            # %B: where today's price sits within the Bollinger Bands (0=low, 1=high).
            # Bandwidth: how wide the bands are — proxy for trend strength.
            sma20 = df["Close"].rolling(20).mean()
            std20 = df["Close"].rolling(20).std()
            bb_upper = sma20 + 2 * std20
            bb_lower = sma20 - 2 * std20
            df["bb_pct"]   = (df["Close"] - bb_lower) / (bb_upper - bb_lower + 1e-9)
            df["bb_width"] = (bb_upper - bb_lower) / (sma20 + 1e-9)
            feature_cols.extend(["bb_pct", "bb_width"])

        if "volume" in self.feature_groups:
            # Volume ratio: today's volume vs its 20-day average.
            # Unusual volume often precedes directional moves.
            df["vol_ratio"]  = df["Volume"] / (df["Volume"].rolling(20).mean() + 1e-9)
            df["vol_change"] = df["Volume"].pct_change()
            feature_cols.extend(["vol_ratio", "vol_change"])

        if "calendar" in self.feature_groups:
            # Day of week (0=Mon, 4=Fri).
            # The Monday effect (lower returns) is one of the oldest market anomalies.
            df["dow"] = pd.to_datetime(df["Date"]).dt.dayofweek
            feature_cols.append("dow")

        # ── Housekeeping ──────────────────────────────────────────────────────
        # Drop rows where any feature or target is NaN
        # (caused by rolling windows and the shift(-1) on the last row)
        df = df.dropna(subset=feature_cols + ["target"]).reset_index(drop=True)

        # Close prices aligned to X/y rows — needed by MetricsSharpe for backtest
        metadata["close_prices"] = df["Close"].values
        metadata["dates"] = df["Date"].values

        y_out = df[["target"]].copy()
        X_out = df[feature_cols].copy()
        # Keep Date for temporal splitting; it will be dropped by TemporalValidationSplit
        X_out["Date"] = df["Date"].values

        return X_out, y_out, metadata
