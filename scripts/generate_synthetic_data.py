"""Synthetic market prices, holdings, and trades for risk teaching."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(314)


def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    tickers = pd.DataFrame(
        {
            "ticker": ["AAA", "BBB", "CCC", "DDD", "ETF-MKT"],
            "sector": ["Tech", "Health", "Energy", "Finance", "Broad"],
            "start_price": [120.0, 85.0, 45.0, 55.0, 100.0],
        }
    )

    dates = pd.bdate_range("2023-01-01", "2024-12-31")
    price_rows = []
    for _, row in tickers.iterrows():
        prices = [row.start_price]
        for _ in range(len(dates) - 1):
            ret = RNG.normal(0.0004, 0.015)
            prices.append(max(1.0, prices[-1] * (1 + ret)))
        for d, px in zip(dates, prices):
            price_rows.append({"date": d, "ticker": row.ticker, "close_price": round(px, 2)})

    prices_df = pd.DataFrame(price_rows)

    holdings = pd.DataFrame(
        {
            "portfolio_id": ["PF01"] * 5,
            "ticker": tickers["ticker"],
            "shares": [500, 400, 300, 600, 1000],
        }
    )

    tx = []
    tid = 1
    for _ in range(120):
        t = RNG.choice(tickers["ticker"])
        d = RNG.choice(dates)
        side = RNG.choice(["BUY", "SELL"])
        qty = int(RNG.integers(10, 150))
        px = prices_df.loc[(prices_df["date"] == d) & (prices_df["ticker"] == t), "close_price"].iloc[0]
        tx.append(
            {
                "trade_id": f"TR{tid:05d}",
                "portfolio_id": "PF01",
                "trade_date": d,
                "ticker": t,
                "side": side,
                "quantity": qty,
                "price": px,
            }
        )
        tid += 1

    tickers.to_csv(out_dir / "dim_security.csv", index=False)
    prices_df.to_csv(out_dir / "fact_price.csv", index=False)
    holdings.to_csv(out_dir / "fact_holdings.csv", index=False)
    pd.DataFrame(tx).to_csv(out_dir / "fact_trade.csv", index=False)
    print(f"Financial synthetic data written to {out_dir}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    main(p.parse_args().out)
