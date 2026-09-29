"""Historical simulation VaR, concentration, P&L attribution."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def portfolio_returns(prices: pd.DataFrame, holdings: pd.DataFrame) -> pd.Series:
    wide = prices.pivot(index="date", columns="ticker", values="close_price").sort_index()
    rets = wide.pct_change().dropna()
    w = holdings.set_index("ticker")["shares"]
    w = w / w.sum()
    port = rets.mul(w, axis=1).sum(axis=1)
    return port


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data = root / "data"
    img = root / "docs" / "images"
    img.mkdir(parents=True, exist_ok=True)

    prices = pd.read_csv(data / "fact_price.csv", parse_dates=["date"])
    holdings = pd.read_csv(data / "fact_holdings.csv")
    trades = pd.read_csv(data / "fact_trade.csv", parse_dates=["trade_date"])

    port_rets = portfolio_returns(prices, holdings)
    var_95 = port_rets.quantile(0.05)
    var_99 = port_rets.quantile(0.01)
    summary = pd.DataFrame({"metric": ["VaR_95_daily", "VaR_99_daily"], "value": [var_95, var_99]})
    summary.to_csv(data / "risk_summary.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.hist(port_rets, bins=40, color="#1f77b4", edgecolor="white")
    plt.axvline(var_95, color="red", linestyle="--", label=f"95% VaR {var_95:.4f}")
    plt.title("Portfolio Daily Return Distribution (Synthetic)")
    plt.xlabel("Return")
    plt.legend()
    plt.tight_layout()
    plt.savefig(img / "var_histogram.png", dpi=120)
    plt.close()

    last_px = prices.sort_values("date").groupby("ticker").tail(1)
    mv = holdings.merge(last_px, on="ticker")
    mv["market_value"] = mv["shares"] * mv["close_price"]
    mv["weight"] = mv["market_value"] / mv["market_value"].sum()
    mv.to_csv(data / "concentration.csv", index=False)

    plt.figure(figsize=(7, 5))
    plt.pie(mv["weight"], labels=mv["ticker"], autopct="%1.1f%%")
    plt.title("Portfolio Concentration by Weight (Synthetic)")
    plt.tight_layout()
    plt.savefig(img / "concentration_pie.png", dpi=120)
    plt.close()

    wide = prices.pivot(index="date", columns="ticker", values="close_price").sort_index()
    daily_pnl = wide.diff().iloc[-1] * holdings.set_index("ticker")["shares"]
    attr = daily_pnl.reset_index()
    attr.columns = ["ticker", "pnl_last_day"]
    attr.to_csv(data / "pnl_attribution_last_day.csv", index=False)

    plt.figure(figsize=(8, 5))
    colors = np.where(attr["pnl_last_day"] >= 0, "#2ca02c", "#d62728")
    plt.bar(attr["ticker"], attr["pnl_last_day"], color=colors)
    plt.title("P&L Attribution — Last Trading Day (Synthetic)")
    plt.ylabel("USD")
    plt.tight_layout()
    plt.savefig(img / "pnl_attribution.png", dpi=120)
    plt.close()

    print(summary)
    print("Financial risk analysis complete.")


if __name__ == "__main__":
    main()
