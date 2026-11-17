"""Run the complete manufacturer-side workflow."""

import subprocess
import sys


steps = [
    "5_manufacturer_decrypt.py",
    "6_plaintext_verify.py",
    "7_decryption_measurements.py",
]


for step in steps:
    print(f"\n=== Running {step} ===")

    result = subprocess.run(
        [sys.executable, step],
        check=True
    )