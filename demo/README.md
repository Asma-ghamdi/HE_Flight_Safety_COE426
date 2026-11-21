# Interactive Demo

`index.html` is a self-contained, click-through visualization of the full HE workflow:
Airbus (manufacturer) → airlines → third-party processor → back to Airbus.

## How to run

Open `demo/index.html` in any modern browser (Chrome, Edge, Safari, Firefox). Nothing to install.
An internet connection is only needed for the fonts; the Excel reader is built into the page.

## Controls

| Action | How |
|---|---|
| Next step | Click anywhere, or press → / ↓ / Space / Enter / Page Down (presentation clickers work) |
| Restart | Press **R**, or click **↻ Restart** |
| Switch mode | **With HE** (8 steps) / **Without HE** (3 steps, plaintext baseline) |
| Use your own data | **Upload Excel files**, or drag a file onto an airline card |

## Steps (With HE)

1. Key generation: Airbus holds the 2048-bit Paillier key pair
2. Public key distribution: pk goes to every airline and the processor
3. Local computation: each airline computes its 7 safety indicators
4. Encryption: each indicator is encrypted with the public key
5. Sending ciphertexts: only ciphertexts reach the processor
6. Encrypted aggregation: ciphertexts are multiplied, which adds the hidden values
7. Encrypted aggregate is sent to Airbus
8. Decryption & analysis: Airbus decrypts the totals and checks them against plaintext aggregation (7/7)

## Data sources

**Default (no upload):** replays the backend run stored in this repo:
the key from `he_flight_safety/keys/`, airline datasets from `he_flight_safety/data/`,
ciphertexts from `he_flight_safety/outbox/`, and measurements from `he_flight_safety/results/`.
The aggregation in step 6 is recomputed in the browser and matches `results/encrypted_aggregate.json` exactly.

**Uploaded Excel files:** the demo runs live on the uploaded data.
- Files map to airlines by name (`emirates`, `saudia`, `qatar`), or by dropping a file on a card.
- Required columns (same as `2_airline_encrypt.py`):
  `flight_id`, `high_descent_rate`, `approach_instability`, `landing_severity`, `gpws_warning`
- Indicators use the same rules and thresholds as `common.py` (score ≥ 7 = event).
- Encryption uses the repo's 2048-bit public key (`n` from `keys/public_key.json`), with fresh randomness per value, the same as `phe`.
- Decryption uses the repo's private key with CRT, the same approach as `phe`.

The browser runs the same algorithm and key as the Python backend (re-implemented in JavaScript
with BigInt), so ciphertexts produced in the demo can be decrypted by the Python code and vice versa.

> Note: if the key pair is regenerated with `1_keygen.py`, the demo page must be rebuilt with the new
> key and outbox files, because the default replay embeds the current run.
