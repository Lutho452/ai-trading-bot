from __future__ import annotations

from typing import List

import pandas as pd

from app.strategies import analyze_signal


class BacktestEngine:
    def __init__(self, data: pd.DataFrame, initial_capital: float = 10000.0, allocation: float = 0.5):
        self.data = data.copy().reset_index(drop=True)
        self.initial_capital = initial_capital
        self.allocation = allocation

    def run(self) -> dict:
        cash = self.initial_capital
        position = 0.0
        equity_curve: List[float] = []
        trade_count = 0
        signal_history: List[str] = []

        for idx, row in self.data.iterrows():
            if idx == 0:
                equity_curve.append(self.initial_capital)
                continue

            recent = self.data.iloc[: idx + 1]
            signal = analyze_signal(recent)["signal"]
            signal_history.append(signal)

            if signal == "BUY" and position == 0:
                notional = cash * self.allocation
                position = notional / float(row["close"])
                cash = cash - notional
                trade_count += 1
            elif signal == "SELL" and position > 0:
                cash = cash + position * float(row["close"])
                position = 0
                trade_count += 1

            portfolio_value = cash + position * float(row["close"])
            equity_curve.append(float(portfolio_value))

        max_drawdown = self._max_drawdown(equity_curve)
        final_value = equity_curve[-1] if equity_curve else self.initial_capital
        total_return_pct = ((final_value - self.initial_capital) / self.initial_capital) * 100

        return {
            "symbol": self.data["symbol"].iloc[0],
            "initial_capital": float(self.initial_capital),
            "final_value": float(final_value),
            "total_return_pct": round(float(total_return_pct), 4),
            "max_drawdown_pct": round(float(max_drawdown), 4),
            "trades": trade_count,
            "signal_history": signal_history,
            "equity_curve": [round(float(x), 2) for x in equity_curve],
        }

    @staticmethod
    def _max_drawdown(values: List[float]) -> float:
        if not values:
            return 0.0

        peak = values[0]
        drawdown = 0.0
        for value in values:
            if value > peak:
                peak = value
            drawdown = max(drawdown, (peak - value) / peak * 100 if peak else 0.0)
        return drawdown
