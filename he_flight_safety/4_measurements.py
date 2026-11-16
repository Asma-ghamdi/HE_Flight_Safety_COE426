"""Collects every measurement into one table: results/member3_measurements.csv (+ prints it)."""
import pandas as pd
from common import AIRLINES, RESULTS_DIR, load_json

rows = [load_json(RESULTS_DIR / f"metrics_encrypt_{a}.json") for a in AIRLINES]
table = pd.DataFrame(rows)
table.to_csv(RESULTS_DIR / "member3_measurements.csv", index=False)
print(table.round(4).to_string(index=False))
print("\nKey generation:", load_json(RESULTS_DIR / "metrics_keygen.json"))
print("Aggregation:   ", load_json(RESULTS_DIR / "metrics_aggregate.json"))
