# Privacy-Preserving Flight Safety Analysis Using Homomorphic Encryption

## Overview

This project demonstrates privacy-preserving collaborative flight safety analysis using Paillier Homomorphic Encryption.

Three simulated airlines calculate selected safety indicators locally, encrypt them using a shared public key, and send the encrypted values to an external processing server. The server aggregates the ciphertexts without accessing the plaintext values. The aircraft manufacturer then decrypts only the combined aggregate results.

The prototype also verifies that the decrypted HE results match conventional plaintext aggregation.

## Setup

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run the Project

### Encryption and Aggregation

```bash
python run_encryption.py
```

This performs:

- Paillier key generation
- Local safety-indicator calculation
- Airline encryption
- Encrypted server aggregation
- Encryption and aggregation measurements

> Re-running key generation creates a new key pair, so encryption and aggregation must be run again before decryption.

### Decryption and Verification

```bash
python run_decryption.py
```

This performs:

- Manufacturer decryption
- Aggregate event-rate calculation
- Plaintext comparison
- Correctness verification
- Decryption measurements

A successful run should show:

```text
Verification result: 7/7 metrics matched
Correctness verification: PASS
```

## Main Files

```text
1_keygen.py
2_airline_encrypt.py
3_server_aggregate.py
4_measurements.py
5_manufacturer_decrypt.py
6_plaintext_verify.py
7_decryption_measurements.py

run_encryption.py
run_decryption.py
```

## Main Directories

```text
data/       Synthetic airline datasets
keys/       Paillier public/private keys
outbox/     Encrypted airline contributions
results/    Aggregates, verification results, and measurements
```

## Safety Indicators

The prototype uses seven indicators:

- Total flights
- High descent rate events
- Unstable approach events
- Hard landing events
- GPWS warning events
- Approach instability score sum
- Landing severity score sum

## Privacy Model

The external processing server is assumed to be **honest-but-curious**. It performs the required encrypted aggregation but does not possess the private key and therefore cannot directly decrypt the airlines' individual safety indicators.
## Interactive Demo

`demo/index.html` is a click-through visualization of the whole workflow: key generation, public-key distribution, local encryption by each airline, encrypted aggregation at the third-party server, and decryption by the manufacturer. A **Without HE** mode shows the plaintext baseline for comparison.

Open `demo/index.html` in a browser. Click (or press →) to advance one step and press **R** to restart. Use **Upload Excel files** to run the pipeline live on your own airline datasets, which need the same columns as `data/`.

See [`demo/README.md`](demo/README.md) for details.
