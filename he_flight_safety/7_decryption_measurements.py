"""ROLE: Evaluation summary for the manufacturer side.
Collects decryption performance and correctness results produced by
the previous Member 4 steps.
"""

from common import (
    RESULTS_DIR,
    load_json,
    save_json,
)


# ---------------------------------------------------------
# 1. Load decryption measurements from Step 5
# ---------------------------------------------------------

decrypt_metrics = load_json(
    RESULTS_DIR / "metrics_decrypt.json"
)


# ---------------------------------------------------------
# 2. Load correctness verification from Step 6
# ---------------------------------------------------------

verification = load_json(
    RESULTS_DIR / "verification.json"
)


# ---------------------------------------------------------
# 3. Build Member 4 evaluation summary
# ---------------------------------------------------------

evaluation_summary = {
    "values_decrypted":
        decrypt_metrics["values_decrypted"],

    "decryption_seconds_total":
        decrypt_metrics["decrypt_seconds_total"],

    "decryption_seconds_per_value":
        decrypt_metrics["decrypt_seconds_per_value"],

    "metrics_verified":
        verification["metrics_checked"],

    "all_metrics_match":
        verification["all_metrics_match"],
}


# ---------------------------------------------------------
# 4. Save the evaluation summary
# ---------------------------------------------------------

save_json(
    RESULTS_DIR / "decryption_measurements.json",
    evaluation_summary
)


# ---------------------------------------------------------
# 5. Display evaluation results
# ---------------------------------------------------------

print("=== Manufacturer-Side Evaluation ===")

print(
    f"Values decrypted: "
    f"{evaluation_summary['values_decrypted']}"
)

print(
    f"Total decryption time: "
    f"{evaluation_summary['decryption_seconds_total']:.6f} seconds"
)

print(
    f"Decryption time per value: "
    f"{evaluation_summary['decryption_seconds_per_value']:.6f} seconds"
)

print(
    f"Metrics verified: "
    f"{evaluation_summary['metrics_verified']}"
)

verification_status = (
    "PASS"
    if evaluation_summary["all_metrics_match"]
    else "FAIL"
)

print(
    f"Correctness verification: "
    f"{verification_status}"
)

print(
    "\nSaved results/decryption_measurements.json"
)