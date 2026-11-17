"""ROLE: Aircraft manufacturer.
Receives the encrypted aggregate from the third-party server, decrypts only the
combined safety indicators, and calculates aggregate rates and average scores.
"""

import time
from phe import paillier
from common import (
    KEYS_DIR,
    RESULTS_DIR,
    METRICS,
    load_json,
    load_public_key,
    str_to_ciphertext,
    save_json,
)


# Manufacturer loads its private key.
private_key_data = load_json(KEYS_DIR / "private_key.json")
public_key = load_public_key()

# Check that the private key matches the public key used in the project.
if int(private_key_data["n"]) != public_key.n:
    raise SystemExit("Private key does not match the public key used by this project.")

private_key = paillier.PaillierPrivateKey(
    public_key,
    int(private_key_data["p"]),
    int(private_key_data["q"]),
)


# Load the encrypted aggregate produced by the server.
aggregate_message = load_json(
    RESULTS_DIR / "encrypted_aggregate.json"
)

encrypted_aggregate = aggregate_message["ciphertexts"]


# Decrypt the seven aggregate safety indicators.
start = time.perf_counter()

decrypted_totals = {
    metric: int(
        private_key.decrypt(
            str_to_ciphertext(
                public_key,
                encrypted_aggregate[metric]
            )
        )
    )
    for metric in METRICS
}

decrypt_seconds = time.perf_counter() - start


# Total number of flights is needed to calculate rates.
total_flights = decrypted_totals["total_flights"]

if total_flights == 0:
    raise SystemExit(
        "Cannot calculate rates because total_flights is 0."
    )


# Calculate aggregate event rates after decryption.
event_rates_percent = {
    "high_descent_rate_percent":
        100
        * decrypted_totals["high_descent_rate_events"]
        / total_flights,

    "unstable_approach_rate_percent":
        100
        * decrypted_totals["unstable_approach_events"]
        / total_flights,

    "hard_landing_rate_percent":
        100
        * decrypted_totals["hard_landing_events"]
        / total_flights,

    "gpws_warning_rate_percent":
        100
        * decrypted_totals["gpws_warning_events"]
        / total_flights,
}


# Calculate average scores.
average_scores = {
    "average_approach_instability":
        decrypted_totals["approach_instability_score_sum"]
        / total_flights,

    "average_landing_severity":
        decrypted_totals["landing_severity_score_sum"]
        / total_flights,
}


# Save the decrypted aggregate and calculated results.
save_json(
    RESULTS_DIR / "decrypted_aggregate.json",
    {
        "airlines_included":
            aggregate_message["airlines_included"],

        "decrypted_totals":
            decrypted_totals,

        "event_rates_percent":
            event_rates_percent,

        "average_scores":
            average_scores,
    }
)


# Save decryption performance measurements.
save_json(
    RESULTS_DIR / "metrics_decrypt.json",
    {
        "values_decrypted": len(METRICS),

        "decrypt_seconds_total":
            decrypt_seconds,

        "decrypt_seconds_per_value":
            decrypt_seconds / len(METRICS),
    }
)


# Display the manufacturer's results.
print("=== Manufacturer Decryption ===")

print(
    f"Decrypted aggregate from "
    f"{aggregate_message['airlines_included']} airlines"
)

for metric in METRICS:
    print(
        f"{metric}: "
        f"{decrypted_totals[metric]}"
    )


print("\nAggregate Event Rates:")

for name, value in event_rates_percent.items():
    print(
        f"{name}: "
        f"{value:.2f}%"
    )


print("\nAverage Scores:")

for name, value in average_scores.items():
    print(
        f"{name}: "
        f"{value:.2f}"
    )


print(
    f"\nDecrypted {len(METRICS)} values "
    f"in {decrypt_seconds:.6f} seconds"
)

print(
    "Saved results/decrypted_aggregate.json "
    "and results/metrics_decrypt.json"
)