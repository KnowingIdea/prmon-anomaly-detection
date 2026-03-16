# Script to detect anomalies in memory usage using Isolation Forest

import pandas as pd
import matplotlib.pyplot as plt # type: ignore
from sklearn.ensemble import IsolationForest # type: ignore

# Read data
df = pd.read_csv('anomaly_data.txt', delim_whitespace=True)
df['pss_mb'] = df['pss'] / 1024
df['vmem_mb'] = df['vmem'] / 1024

# Prepare input features
X = df[['pss_mb', 'vmem_mb', 'nprocs', 'nthreads']]

# Fit Isolation Forest model
model = IsolationForest(contamination=0.35, random_state=2)
df['anomaly'] = model.fit_predict(X)
anomalies = df[df['anomaly'] == -1]

# Plot figure
plt.figure(figsize=(10, 6))

plt.plot(df['wtime'], df['pss_mb'], label='PSS', color='blue')
plt.scatter(anomalies['wtime'], anomalies['pss_mb'], color='red', label='Anomalies', marker='x')

plt.xlabel('Time (s)')
plt.ylabel('Memory (MB)')
plt.title('Detected Anomalies by Memory')
plt.legend()
plt.grid(True)

plt.show()