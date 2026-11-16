"""ROLE: Aircraft manufacturer.  Generates the Paillier key pair.
public_key.json  -> given to the airlines and the server
private_key.json -> stays with the manufacturer (Member 4). Never give it to the server."""
import time
from phe import paillier
from common import KEY_BITS, KEYS_DIR, RESULTS_DIR, save_json

start = time.perf_counter()
public_key, private_key = paillier.generate_paillier_keypair(n_length=KEY_BITS)
keygen_seconds = time.perf_counter() - start

save_json(KEYS_DIR / "public_key.json", {"scheme": "paillier", "key_bits": KEY_BITS, "n": str(public_key.n)})
save_json(KEYS_DIR / "private_key.json", {"scheme": "paillier", "key_bits": KEY_BITS, "n": str(public_key.n),
                                          "p": str(private_key.p), "q": str(private_key.q)})
save_json(RESULTS_DIR / "metrics_keygen.json", {"key_bits": KEY_BITS, "keygen_seconds": keygen_seconds})
print(f"Generated {KEY_BITS}-bit Paillier key pair in {keygen_seconds:.3f} s -> keys/")
