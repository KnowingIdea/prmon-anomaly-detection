import pandas as pd
import matplotlib.pyplot as plt # type: ignore

df = pd.read_csv('anomaly_data.txt', delim_whitespace=True)

df['pss_mb'] = df['pss'] / 1024
df['vmem_mb'] = df['vmem'] / 1024

plt.figure(figsize=(10, 6))

plt.plot(df['wtime'], df['pss_mb'], label = 'PSS', color = 'blue')
plt.plot(df['wtime'], df['vmem_mb'], label = 'Memory', color = 'red')

plt.xlabel('Time (s)')
plt.ylabel('Memory (MB)')
plt.title('Memory Usage Over Time (Anomaly)')
plt.legend()
plt.grid(True)

plt.show()