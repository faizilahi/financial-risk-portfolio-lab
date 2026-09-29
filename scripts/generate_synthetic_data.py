from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; DATA.mkdir(parents=True, exist_ok=True)
pd.DataFrame([
    {"book": "EQ", "position_id": "P1", "notional": 180_000_000, "sens_1pct": 600_000},
    {"book": "EQ", "position_id": "P2", "notional": 90_000_000, "sens_1pct": 280_000},
    {"book": "RATES", "position_id": "P3", "notional": 100_000_000, "sens_1pct": 40_000},
    {"book": "FX", "position_id": "P4", "notional": 50_000_000, "sens_1pct": 55_000},
]).to_csv(DATA / "positions.csv", index=False)
pd.DataFrame([{"factor": "EQ_SPOT", "shock_pct": -3.0},
              {"factor": "EQ_OVERLAY_DUP", "shock_pct": -3.0, "note": "duplicate overlay"}]).to_csv(
    DATA / "shocks.csv", index=False)
print("positions ready")
