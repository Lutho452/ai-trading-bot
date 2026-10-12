from __future__ import annotations

from typing import Any, Dict

import pandas as pd
from sklearn.linear_model import LogisticRegression

from app.services.feature_engineering import add_technical_features


class StrategyEngine:
    def __init__(self, lookahead: int = 3):
        self.lookahead = lookahead
        self.model = LogisticRegression(max_iter=2000, solver="lbfgs")

    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        enriched = add_technical_features(data)
        if len(enriched) < 5:
            return enriched

        enriched["future_return"] = enriched["close"].shift(-self.lookahead).pct_change().fillna(0)
        enriched["target"] = (enriched["future_return"] > 0).astype(int)
        return enriched

    def train(self, data: pd.DataFrame) -> Dict[str, Any]:
        enriched = self.prepare_features(data)
        feature_columns = [
            "returns",
            "sma_10",
            "sma_30",
            "macd",
            "rsi_14",
            "volatility",
            "bollinger_position",
        ]
        model_data = enriched[feature_columns + ["target"]].dropna()
        if len(model_data) < 10:
            return {"status": "insufficient_data"}

        X = model_data[feature_columns]
        y = model_data["target"]
        self.model.fit(X, y)
        return {"status": "trained", "feature_columns": feature_columns}

    def generate_signal(self, data: pd.DataFrame, account_balance: float = 10000.0) -> Dict[str, Any]:
        enriched = self.prepare_features(data)
        feature_columns = [
            "returns",
            "sma_10",
            "sma_30",
            "macd",
            "rsi_14",
            "volatility",
            "bollinger_position",
        ]

        if enriched.empty:
            return {"signal": "HOLD", "confidence": 0.0, "score": 0.0, "reasons": ["No data"]}

        latest = enriched.iloc[-1]
        sample = enriched[feature_columns].dropna().tail(1)
        heuristic_score = 0.0
        reasons = []

        if latest["sma_10"] > latest["sma_30"]:
            heuristic_score += 1.2
            reasons.append("Trend is upward")
        else:
            heuristic_score -= 1.2
            reasons.append("Trend is downward")

        if latest["rsi_14"] < 30:
            heuristic_score += 1.0
            reasons.append("Oversold RSI")
        elif latest["rsi_14"] > 70:
            heuristic_score -= 1.0
            reasons.append("Overbought RSI")

        if latest["macd"] > 0:
            heuristic_score += 0.6
            reasons.append("Positive MACD")
        elif latest["macd"] < 0:
            heuristic_score -= 0.6
            reasons.append("Negative MACD")

        if latest["volatility"] > 0.02:
            heuristic_score -= 0.5
            reasons.append("High volatility")

        if len(sample) == 0:
            model_score = 0.0
        else:
            try:
                probs = self.model.predict_proba(sample)[0]
                model_score = float(probs[1] - probs[0])
            except Exception:
                model_score = 0.0

        overall_score = heuristic_score * 0.6 + model_score * 1.2

        if overall_score > 0.35:
            signal = "BUY"
        elif overall_score < -0.35:
            signal = "SELL"
        else:
            signal = "HOLD"

        confidence = min(max(abs(overall_score) / 2.0, 0.1), 0.95)
        return {
            "signal": signal,
            "confidence": round(float(confidence), 4),
            "score": round(float(overall_score), 4),
            "price": float(latest["close"]),
            "reasons": reasons,
            "account_balance": float(account_balance),
        }
