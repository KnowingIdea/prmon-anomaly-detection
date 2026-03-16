Process Resource Monitoring and Anomaly Detection
Overview
This project explores process resource monitoring and time-series anomaly detection using prmon (Process Monitor). The goal was to generate a baseline resource usage dataset, inject artificial anomalies (memory leaks and process spikes), and successfully identify those anomalies using an unsupervised Machine Learning algorithm.

AI Assistance Disclosure
Tool Used: Google Gemini (Gemini 3.1 Pro)

Purpose: I used Gemini to assist with design decisions (specifically choosing the Isolation Forest algorithm for multi-dimensional anomaly detection), discovering the mathematical reason behind the contamination parameter limits, and generating the initial Python boilerplate for matplotlib and scikit-learn.

Methodology
1. Data Generation and Anomaly Injection
Data was collected using prmon monitoring a custom Python workload. The workload utilizes prmon's built-in C++ mem-burner to create a baseline memory footprint of 500MB.

To create a realistic, repeating pattern of system stress, a loop was used to inject two distinct types of anomalies over a 3-minute period:

Memory Spikes: Sudden allocations of 1500MB for 5 seconds.

Thread/Process Spikes: Spawning 10 concurrent processes holding 500MB total for 5 seconds.

Key Command:

Bash
# Running prmon to sample data every 1 second
prmon --interval 1 --filename anomaly_data.txt -- python3 workload_loop.py
2. Anomaly Detection Approach
I utilized Isolation Forest from the scikit-learn library. This unsupervised model was chosen because it excels at multi-dimensional anomaly detection. A simple statistical threshold (like a Z-score on memory) would easily miss the process-count anomalies, but Isolation Forest evaluates the relationship between multiple features (pss, vmem, nprocs, nthreads) simultaneously.

Core Detection Logic:

Python
from sklearn.ensemble import IsolationForest

# Features fed into the model
features = ['pss', 'vmem', 'nprocs', 'nthreads']
X = df[features]

# Model initialization with a 25% contamination expectation
model = IsolationForest(contamination=0.25, random_state=42)
df['anomaly_label'] = model.fit_predict(X)
Evaluation and Visualizations
(Insert your saved matplotlib image here, e.g., ![Anomaly Graph](graph.png))

The Isolation Forest successfully identified both types of injected anomalies. The top graph shows the model correctly flagging the massive 1500MB PSS memory spikes. The bottom graph demonstrates the model's multi-dimensional capability, correctly flagging the process-count spikes even when the memory footprint remained relatively flat.

Conclusions and Trade-offs
While Isolation Forest proved highly capable, tuning it highlighted several technical trade-offs:

The Contamination Parameter: The model requires a contamination estimate (the expected percentage of anomalies). Initially set to 15%, the model failed to flag all injected peaks because the looped anomalies actually constituted roughly 22% of the dataset's runtime. Increasing the parameter to 25% resolved this, but in a real-world, unpredictable production environment, statically defining this percentage could lead to missed anomalies or false positives.

Transition States: The model occasionally flagged data points on the "slopes" of the memory spikes (the exact second the memory was spinning up or shutting down). Because prmon polls strictly every 1.0 seconds, these halfway-allocated states look highly unusual to the AI. While technically false positives for the "peak" of the anomaly, they accurately reflect anomalous system transition behavior.