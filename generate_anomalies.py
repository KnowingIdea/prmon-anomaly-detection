# Script to generate anomalies for testing prmon using mem-burner

import subprocess
import time

burner_path = "/home/ubuntu/prmon/build/package/tests/mem-burner"

# Start the baseline process
baseline = subprocess.Popen([burner_path, "-m", "500", "-s", "180"])

time.sleep(20)

# Generate anomalies at regular intervals
for i in range(4):
    # Large memory draw
    anomaly = subprocess.Popen([burner_path, "-m", "1500", "-s", "5"])
    time.sleep(15)

    # Starting many processes
    anomaly2 = subprocess.Popen([burner_path, "-m", "500", "-p", "10", "-s", "5"])
    time.sleep(15)
