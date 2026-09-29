# VaR Pack That Disagreed With the Desk

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

Desk 1-day 95% VaR was **$2.48M**. The risk pack printed **$3.11M** after a
shock was applied twice to the same equity book — once in position PnL and
again in the residual overlay.

## The positions

Synthetic book: equities, rates futures, FX forwards. Notional **$420M**.

## The shock

Equity -3% parallel shock. Correct incremental VaR contribution **$2.48M**.

## The break

Double-counted overlay added **$0.63M**. Break report in `output/var_break.csv`.

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_var.py
```
