"""ROLE: Third-party server (honest-but-curious).
Has ONLY the public key and the airlines' ciphertexts. Adds them homomorphically:
Enc(a) + Enc(b) = Enc(a + b).  It never decrypts anything and never imports the private key."""
import time
from common import (OUTBOX_DIR, RESULTS_DIR, METRICS, load_public_key, load_json, save_json,
                    ciphertext_to_str, str_to_ciphertext)

public_key = load_public_key()
inputs = sorted(OUTBOX_DIR.glob("*_encrypted.json"))
if not inputs:
    raise SystemExit("No airline submissions found in outbox/. Run 2_airline_encrypt.py first.")

submissions = [load_json(p) for p in inputs]
start = time.perf_counter()
aggregate = {}
for metric in METRICS:
    total = str_to_ciphertext(public_key, submissions[0]["ciphertexts"][metric])
    for sub in submissions[1:]:
        total = total + str_to_ciphertext(public_key, sub["ciphertexts"][metric])   # homomorphic addition
    aggregate[metric] = total
aggregate_seconds = time.perf_counter() - start

out_path = RESULTS_DIR / "encrypted_aggregate.json"
save_json(out_path, {"airlines_included": len(submissions),
                     "ciphertexts": {m: ciphertext_to_str(aggregate[m]) for m in METRICS}})
input_bytes = sum(p.stat().st_size for p in inputs)
save_json(RESULTS_DIR / "metrics_aggregate.json", {
    "airlines_included": len(submissions),
    "metrics_aggregated": len(METRICS),
    "homomorphic_additions": (len(submissions) - 1) * len(METRICS),
    "aggregate_seconds": aggregate_seconds,
    "server_input_bytes": input_bytes,
    "server_output_bytes": out_path.stat().st_size,
})
print(f"Aggregated {len(submissions)} airlines x {len(METRICS)} metrics in {aggregate_seconds*1000:.2f} ms")
print(f"Server input {input_bytes} bytes -> output {out_path.stat().st_size} bytes ({out_path})")
