from __future__ import annotations

from typing import Dict, List


class PortfolioService:
    def __init__(self, initial_cash: float = 10000.0):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, float] = {}

    def buy(self, symbol: str, quantity: float, price: float) -> Dict[str, float]:
        cost = quantity * price
        if cost > self.cash:
            raise ValueError("Not enough cash to buy")
        self.cash -= cost
        self.positions[symbol] = self.positions.get(symbol, 0.0) + quantity
        return {"symbol": symbol, "quantity": quantity, "cost": cost}

    def sell(self, symbol: str, quantity: float, price: float) -> Dict[str, float]:
        if self.positions.get(symbol, 0.0) < quantity:
            raise ValueError("Not enough position to sell")
        self.positions[symbol] = self.positions.get(symbol, 0.0) - quantity
        if self.positions[symbol] == 0:
            del self.positions[symbol]
        proceeds = quantity * price
        self.cash += proceeds
        return {"symbol": symbol, "quantity": quantity, "proceeds": proceeds}

    def summary(self) -> Dict[str, object]:
        total_value = self.cash + sum(qty * 0.0 for qty in self.positions.values())
        return {
            "cash": self.cash,
            "positions": self.positions,
            "total_value": total_value,
            "initial_cash": self.initial_cash,
        }
