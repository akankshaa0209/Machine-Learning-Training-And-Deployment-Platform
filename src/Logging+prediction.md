Logging every prediction request into MLflow automatically so you can later detect data drift and model degradation.

# current state: User → API → Model → Prediction

# But in production, companies also store every prediction request so they can analyze:

Data drift

Model performance degradation

Incorrect predictions

This process is called prediction logging.

1️⃣ What “Logging Predictions” Means

When someone calls your API:

{
"rideable_type": "classic_bike",
"trip_distance": 0.47,
"start_end_id": "31950.0_31090.0"
}

Your API returns:

{
"predicted_duration": 9.7
}

But we also store this information somewhere.

Example record:

timestamp rideable_type trip_distance start_end_id prediction
2026-03-11 classic_bike 0.47 31950_31090 9.7

This lets us analyze how the model behaves over time.

2️⃣ Why This Is Important

Imagine your model was trained on data like:

trip_distance duration
0.2 5 min
0.5 10 min
1.0 20 min

But later users start sending:

trip_distance
8 km
12 km
20 km

This is data drift.

Your model was never trained on such values → predictions become wrong.

Monitoring logged predictions helps detect this.

This concept is widely used in MLOps systems.

3️⃣ What Companies Actually Do

Companies like:

Uber

Airbnb

store prediction logs to detect:

Problem Example
Data drift Input data distribution changes
Concept drift Relationship between input and output changes
Model degradation Accuracy drops over time

# architecture:

Client Request
↓
FastAPI Prediction Service
↓
Model Prediction
↓
Prediction Logging
↓
Monitoring System
↓
Drift Detection
↓
Retraining Pipeline

5️⃣ How We Can Do It in Your Project

Your FastAPI API can log predictions to:

MLflow

database

log files

monitoring systems

6️⃣ Later You Can Analyze

MLflow UI will show:

Run trip_distance prediction
Run 1 0.47 9.7
Run 2 0.85 14.3

You can detect patterns like:

Predictions becoming too large

Input values changing

7️⃣ Real Production Monitoring

In advanced systems you add tools like:

Evidently AI

Prometheus

Grafana

These automatically detect drift and trigger retraining.

8️⃣ Why This Is Important for Your Resume

Most ML projects show only:

Train model
Deploy API

But real MLOps projects include monitoring.

So your project would demonstrate:

Training pipeline

Model registry

Deployment

Monitoring

Which is complete ML lifecycle.

## How to store all prediction logs in a dataset table so later you can:

detect data drift

compute real accuracy

trigger automatic retraining.

This is how real production ML platforms work.
