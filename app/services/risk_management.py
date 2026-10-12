from __future__ import annotations

from typing import Dict, Any


class RiskManager:
    def __init__(self, max_position_pct: float = 0.2, max_daily_loss_pct: float = 0.03):
        self.max_position_pct = max_position_pct
        self.max_daily_loss_pct = max_daily_loss_pct

    def get_position_size(self, account_balance: float, signal: str, price: float, confidence: float) -> Dict[str, Any]:
        if price <= 0:
            raise ValueError("Price must be positive")

        max_budget = account_balance * self.max_position_pct
        risk_budget = account_balance * self.max_daily_loss_pct
        confidence_factor = max(min(confidence, 1.0), 0.0)

        if signal == "BUY":
            target_value = max_budget * (0.4 + confidence_factor * 0.6)
        elif signal == "SELL":
            target_value = max_budget * (0.3 + confidence_factor * 0.5)
        else:
            target_value = 0.0

        position_size = max(0.0, min(target_value / price, 1_000_000_000.0))
        stop_loss_price = price * (0.97 if signal == "BUY" else 1.03)

        return {
            "signal": signal,
            "position_size": round(float(position_size), 6),
            "notional_value": round(float(position_size * price), 2),
            "risk_budget": round(float(risk_budget), 2),
            "stop_loss_price": round(float(stop_loss_price), 4),
        }
