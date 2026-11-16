"""Shared settings and helpers used by every role (manufacturer, airline, server)."""
import json
from pathlib import Path
from phe import paillier

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"        # each airline's private plaintext dataset
KEYS_DIR = ROOT / "keys"        # public_key.json (shared) / private_key.json (manufacturer only)
OUTBOX_DIR = ROOT / "outbox"    # what airlines send to the server (ciphertexts only)
RESULTS_DIR = ROOT / "results"  # encrypted aggregate + measurements

KEY_BITS = 2048                 # Paillier modulus size

AIRLINES = {
    "Emirates": "Emirates_flight_safety_dataset.xlsx",
    "Saudia": "Saudia_flight_safety_dataset.xlsx",
    "Qatar_Airways": "Qatar_Airways_flight_safety_dataset.xlsx",
}

# A flight counts as an "event" when its 0-10 score reaches the threshold.
# TEAM DECISION: change these two numbers if the team agrees on other cut-offs.
UNSTABLE_APPROACH_THRESHOLD = 7
HARD_LANDING_THRESHOLD = 7

# The exact list (and order) of values every airline encrypts.
METRICS = [
    "total_flights",
    "high_descent_rate_events",
    "unstable_approach_events",
    "hard_landing_events",
    "gpws_warning_events",
    "approach_instability_score_sum",
    "landing_severity_score_sum",
]


def save_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2))


def load_json(path):
    return json.loads(Path(path).read_text())


def load_public_key():
    return paillier.PaillierPublicKey(n=int(load_json(KEYS_DIR / "public_key.json")["n"]))


def ciphertext_to_str(enc):
    """EncryptedNumber -> decimal string (JSON cannot hold 4096-bit integers safely)."""
    return str(enc.ciphertext(be_secure=False))


def str_to_ciphertext(public_key, text):
    return paillier.EncryptedNumber(public_key, int(text), 0)
