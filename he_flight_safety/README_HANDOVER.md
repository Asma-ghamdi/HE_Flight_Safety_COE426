# Member 3 -> Member 4 handover

## Setup
    pip install -r requirements.txt

## Run (in this order)
    python 1_keygen.py                       # manufacturer: makes keys/
    python 2_airline_encrypt.py Emirates     # each airline: local counts -> ciphertexts in outbox/
    python 2_airline_encrypt.py Saudia
    python 2_airline_encrypt.py Qatar_Airways
    python 3_server_aggregate.py             # server: adds ciphertexts -> results/encrypted_aggregate.json
    python 4_measurements.py                 # timing + size table -> results/member3_measurements.csv

Or everything at once: `python run_member3.py`
Re-running 1_keygen.py makes NEW keys, so steps 2-3 must be re-run after it.

## What Member 4 receives
| File | What it is |
|---|---|
| keys/private_key.json | Paillier private key (n, p, q as strings). Manufacturer only. |
| keys/public_key.json | Paillier public key (n). |
| results/encrypted_aggregate.json | 7 ciphertexts = encrypted sums over the 3 airlines. |
| results/member3_measurements.csv, metrics_*.json | Encryption / aggregation time and sizes. |
| data/*.xlsx | Plaintext datasets, for the plaintext comparison only. |

## How to decrypt (starting point for Member 4)
    from phe import paillier
    from common import *
    k = load_json(KEYS_DIR / "private_key.json")
    pk = load_public_key()
    sk = paillier.PaillierPrivateKey(pk, int(k["p"]), int(k["q"]))
    agg = load_json(RESULTS_DIR / "encrypted_aggregate.json")["ciphertexts"]
    totals = {m: sk.decrypt(str_to_ciphertext(pk, agg[m])) for m in METRICS}

Event rate = events / total_flights, e.g. totals["gpws_warning_events"] / totals["total_flights"].
Average score = score_sum / total_flights.

## Definitions (common.py)
- unstable_approach_events: flights with approach_instability >= 7
- hard_landing_events: flights with landing_severity >= 7
- high_descent_rate_events / gpws_warning_events: sum of the 0/1 column
