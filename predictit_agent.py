#!/usr/bin/env python3
"""Simple bot that fetches PredictIt prices and simulates trades."""

import requests
import time
import random
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


class PredictItAPI:
    """Lightweight wrapper around the PredictIt public API."""

    def __init__(self, base_url: str = "https://www.predictit.org/api/marketdata"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        # Use a custom user agent so requests are less likely to be blocked
        self.session.headers.update({"User-Agent": "PredictItTradingAgent/1.0"})

    def fetch(self, path: str) -> Dict:
        url = f"{self.base_url}/{path.lstrip('/')}"
        resp = self.session.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def all_markets(self) -> List[Dict]:
        data = self.fetch("all/")
        return data.get("markets", [])

    def market(self, market_id: int) -> Dict:
        return self.fetch(f"markets/{market_id}/")

@dataclass
class Trade:
    timestamp: str
    market: str
    contract: str
    side: str
    price: float
    profit: Optional[float] = None

class PredictItTradingAgent:
    def __init__(self, api: Optional[PredictItAPI] = None):
        self.api = api or PredictItAPI()
        self.positions: Dict[int, Trade] = {}
        self.history: List[Trade] = []

    def fetch_data(self) -> List[Dict]:
        try:
            return self.api.all_markets()
        except Exception as e:
            print(f"Failed to fetch market data: {e}")
            return []

    def choose_contract(self, markets: List[Dict]):
        available = []
        for m in markets:
            for c in m.get("contracts", []):
                if "bestBuyYesCost" in c or "lastTradePrice" in c:
                    available.append((m, c))
        if not available:
            return None, None
        return random.choice(available)

    def trade(self) -> None:
        markets = self.fetch_data()
        market, contract = self.choose_contract(markets)
        if contract is None:
            print("No contracts available.")
            return
        price = contract.get("bestBuyYesCost") or contract.get("lastTradePrice")
        if price is None:
            print("No price for contract.")
            return
        trade = Trade(
            timestamp=datetime.utcnow().isoformat(),
            market=market.get("shortName", market.get("name", "")),
            contract=contract.get("shortName", contract.get("name", "")),
            side="BUY",
            price=price,
        )
        self.positions[contract["id"]] = trade
        self.history.append(trade)
        print(f"Bought {trade.contract} at {trade.price} in market {trade.market}")

    def update(self) -> None:
        markets = self.fetch_data()
        lookup = {c["id"]: c for m in markets for c in m.get("contracts", [])}
        for cid, trade in list(self.positions.items()):
            contract = lookup.get(cid)
            if not contract:
                continue
            price = contract.get("bestBuyYesCost") or contract.get("lastTradePrice")
            if price is None:
                continue
            profit = price - trade.price
            update_trade = Trade(
                timestamp=datetime.utcnow().isoformat(),
                market=trade.market,
                contract=trade.contract,
                side="UPDATE",
                price=price,
                profit=profit,
            )
            self.history.append(update_trade)
            print(
                f"Update {trade.contract}: new price {price}, PnL {profit:.2f}"
            )

    def save_history(self, filename: str = "trading_log.csv") -> None:
        import csv

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "market", "contract", "side", "price", "profit"])
            for t in self.history:
                writer.writerow([
                    t.timestamp,
                    t.market,
                    t.contract,
                    t.side,
                    f"{t.price:.2f}",
                    f"{t.profit:.2f}" if t.profit is not None else "",
                ])
        print(f"Saved log to {filename}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Simulate trades using PredictIt data")
    parser.add_argument("--iterations", type=int, default=3, help="Number of trade/update cycles")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between cycles in seconds")
    parser.add_argument("--log", type=str, default="trading_log.csv", help="CSV file for trade history")
    args = parser.parse_args()

    agent = PredictItTradingAgent()
    for _ in range(args.iterations):
        agent.trade()
        time.sleep(args.delay)
        agent.update()
        time.sleep(args.delay)
    agent.save_history(args.log)


if __name__ == "__main__":
    main()
