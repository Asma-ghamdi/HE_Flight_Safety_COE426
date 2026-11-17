"""Run the complete encryption and encrypted aggregation workflow."""
import subprocess, sys
from common import AIRLINES

steps = [["1_keygen.py"]] + [["2_airline_encrypt.py", a] for a in AIRLINES] + [["3_server_aggregate.py"], ["4_measurements.py"]]
for step in steps:
    print(f"\n===== python {' '.join(step)} =====")
    subprocess.run([sys.executable, *step], check=True)
