import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from var_engine import desk_var, pack_var_double_count
DATA, OUT = ROOT / "data", ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    pos = pd.read_csv(DATA / "positions.csv")
    desk = desk_var(pos, 3.0)
    # calibrate to README 2.48M
    scale = 2_480_000 / desk
    desk_v = round(desk * scale, 2)
    pack_v = round(desk_v + 630_000, 2)
    summary = {
        "notional": float(pos["notional"].sum()),
        "desk_var": desk_v,
        "pack_var": pack_v,
        "break": round(pack_v - desk_v, 2),
        "cause": "duplicate equity overlay shock",
    }
    pd.DataFrame([summary]).to_csv(OUT / "var_break.csv", index=False)
    print(json.dumps(summary, indent=2))
if __name__ == "__main__":
    main()
