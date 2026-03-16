import subprocess
import time

burner_path = "/home/ubuntu/prmon/build/package/tests/mem-burner"

# Start the baseline process
baseline = subprocess.Popen([burner_path, "-m", "500", "-s", "180"])

time.sleep(20)

for i in range(4):
    anomaly = subprocess.Popen([burner_path, "-m", "1500", "-s", "5"])
    time.sleep(15)
    anomaly2 = subprocess.Popen([burner_path, "-m", "500", "-p", "10", "-s", "5"])
    time.sleep(15)
