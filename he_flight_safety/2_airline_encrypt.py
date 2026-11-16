"""ROLE: One airline.  Usage: python 2_airline_encrypt.py Emirates
Reads its own private dataset, counts safety events LOCALLY, encrypts every count
with the manufacturer's public key, and writes only ciphertexts to outbox/."""
import sys
import time
import json
import pandas as pd
from common import (AIRLINES, DATA_DIR, OUTBOX_DIR, RESULTS_DIR, METRICS, UNSTABLE_APPROACH_THRESHOLD,
                    HARD_LANDING_THRESHOLD, load_public_key, ciphertext_to_str, save_json)


def local_counts(df):
    """Plaintext step - happens inside the airline, never leaves it."""
    return {
        "total_flights": int(len(df)),
        "high_descent_rate_events": int(df["high_descent_rate"].sum()),
        "unstable_approach_events": int((df["approach_instability"] >= UNSTABLE_APPROACH_THRESHOLD).sum()),
        "hard_landing_events": int((df["landing_severity"] >= HARD_LANDING_THRESHOLD).sum()),
        "gpws_warning_events": int(df["gpws_warning"].sum()),
        "approach_instability_score_sum": int(df["approach_instability"].sum()),
        "landing_severity_score_sum": int(df["landing_severity"].sum()),
    }


def main(airline):
    dataset_path = DATA_DIR / AIRLINES[airline]
    df = pd.read_excel(dataset_path)
    counts = local_counts(df)
    public_key = load_public_key()

    start = time.perf_counter()
    encrypted = {m: public_key.encrypt(counts[m]) for m in METRICS}   # fresh randomness per value
    encrypt_seconds = time.perf_counter() - start

    message = {"airline": airline, "ciphertexts": {m: ciphertext_to_str(encrypted[m]) for m in METRICS}}
    out_path = OUTBOX_DIR / f"{airline}_encrypted.json"
    save_json(out_path, message)

    plaintext_bytes = len(json.dumps(counts).encode())
    save_json(RESULTS_DIR / f"metrics_encrypt_{airline}.json", {
        "airline": airline,
        "flights": counts["total_flights"],
        "values_encrypted": len(METRICS),
        "encrypt_seconds_total": encrypt_seconds,
        "encrypt_seconds_per_value": encrypt_seconds / len(METRICS),
        "input_dataset_bytes": dataset_path.stat().st_size,
        "plaintext_counts_bytes": plaintext_bytes,
        "encrypted_message_bytes": out_path.stat().st_size,
        "expansion_factor": out_path.stat().st_size / plaintext_bytes,
    })
    print(f"[{airline}] local plaintext counts (private): {counts}")
    print(f"[{airline}] encrypted {len(METRICS)} values in {encrypt_seconds:.3f} s -> {out_path.name}")
    print(f"[{airline}] what the server sees for total_flights: {message['ciphertexts']['total_flights'][:60]}...")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in AIRLINES:
        sys.exit(f"Usage: python 2_airline_encrypt.py <{'|'.join(AIRLINES)}>")
    main(sys.argv[1])
