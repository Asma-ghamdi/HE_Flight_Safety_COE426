"""ROLE: Correctness verification.
Computes the same safety indicators directly from the plaintext airline datasets
and compares them with the decrypted Homomorphic Encryption aggregate.
"""

import pandas as pd

from common import (
    AIRLINES,
    DATA_DIR,
    RESULTS_DIR,
    METRICS,
    UNSTABLE_APPROACH_THRESHOLD,
    HARD_LANDING_THRESHOLD,
    load_json,
    save_json,
)


def local_counts(df):
    """Calculate one airline's safety indicators directly from plaintext data."""
    return {
        "total_flights": int(len(df)),

        "high_descent_rate_events":
            int(df["high_descent_rate"].sum()),

        "unstable_approach_events":
            int(
                (
                    df["approach_instability"]
                    >= UNSTABLE_APPROACH_THRESHOLD
                ).sum()
            ),

        "hard_landing_events":
            int(
                (
                    df["landing_severity"]
                    >= HARD_LANDING_THRESHOLD
                ).sum()
            ),

        "gpws_warning_events":
            int(df["gpws_warning"].sum()),

        "approach_instability_score_sum":
            int(df["approach_instability"].sum()),

        "landing_severity_score_sum":
            int(df["landing_severity"].sum()),
    }


# ---------------------------------------------------------
# 1. Calculate plaintext aggregate from all airline datasets
# ---------------------------------------------------------

plaintext_totals = {
    metric: 0
    for metric in METRICS
}

for airline, filename in AIRLINES.items():

    dataset_path = DATA_DIR / filename

    df = pd.read_excel(dataset_path)

    airline_counts = local_counts(df)

    for metric in METRICS:
        plaintext_totals[metric] += airline_counts[metric]


# ---------------------------------------------------------
# 2. Load the aggregate decrypted by the manufacturer
# ---------------------------------------------------------

decrypted_result = load_json(
    RESULTS_DIR / "decrypted_aggregate.json"
)

he_totals = decrypted_result["decrypted_totals"]


# ---------------------------------------------------------
# 3. Compare plaintext totals with decrypted HE totals
# ---------------------------------------------------------

comparison = {}

all_match = True

for metric in METRICS:

    plaintext_value = int(plaintext_totals[metric])
    he_value = int(he_totals[metric])

    match = plaintext_value == he_value

    comparison[metric] = {
        "plaintext": plaintext_value,
        "he_decrypted": he_value,
        "match": match,
    }

    if not match:
        all_match = False


# ---------------------------------------------------------
# 4. Save verification results
# ---------------------------------------------------------

save_json(
    RESULTS_DIR / "verification.json",
    {
        "metrics_checked": len(METRICS),
        "all_metrics_match": all_match,
        "comparison": comparison,
    }
)


# ---------------------------------------------------------
# 5. Display results
# ---------------------------------------------------------

print("=== Plaintext vs HE Verification ===")

for metric in METRICS:

    result = comparison[metric]

    status = "MATCH" if result["match"] else "MISMATCH"

    print(
        f"{metric}: "
        f"plaintext={result['plaintext']} | "
        f"HE={result['he_decrypted']} | "
        f"{status}"
    )


matched_count = sum(
    1
    for result in comparison.values()
    if result["match"]
)

print(
    f"\nVerification result: "
    f"{matched_count}/{len(METRICS)} metrics matched"
)

if all_match:
    print(
        "SUCCESS: Decrypted HE aggregate matches "
        "the plaintext aggregate."
    )
else:
    print(
        "WARNING: One or more metrics do not match."
    )

print(
    "\nSaved results/verification.json"
)