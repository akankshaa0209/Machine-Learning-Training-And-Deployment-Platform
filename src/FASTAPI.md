we will add Model Serving so your trained model can be used via an API.
This is how real ML systems expose predictions.

predict.py

We will build a prediction API using FastAPI and load the model from the MLflow registry.

This will make your project look like a complete production ML system.

Training Pipeline
↓
MLflow Model Registry
↓
FastAPI Prediction Service
↓
REST API
↓
Client Application

Example request:

POST /predict

Input

{
"start_station_id": "A",
"end_station_id": "B",
"hour": 10
}

Output

Predicted trip duration

=============issue:
The issue is about the tracking server location used by MLflow.

Right now MLflow says:

tracking URI = sqlite:/C:/Projects/scalable-ml-platform/mlflow.db

But when loading models from:

models:/citibike-duration-model/1

MLflow expects a running tracking server (HTTP).

Why This Happens

Your training script logged the model using a local database:

sqlite:///mlflow.db

But your API service is trying to load the model using model registry, which requires a tracking server.

So we must point both to the same server.

1️⃣ Model Loaded Successfully

You saw:

Model loaded successfully

This means your FastAPI service successfully fetched the model from the MLflow registry.

2️⃣ Model Artifact Location
artifact_path: mlflow-artifacts:/3/models/m-46f7ffbf3ee64cfb91b4d0c697ba7c9c/artifacts

This tells MLflow where the trained model files are stored.

Inside that artifact folder MLflow keeps:

model.pkl
MLmodel
conda.yaml
python_env.yaml

These allow the model to be reproducible anywhere.

3️⃣ Model Flavor

You have two flavors:

python_function
sklearn

Meaning your model can be loaded as:

Generic MLflow model

Native scikit-learn model

Your API is using the pyfunc flavor, which is the recommended production interface.

4️⃣ Environment Reproducibility

MLflow saved:

conda.yaml
python_env.yaml

This ensures anyone can reproduce the environment.

This is very important in real MLOps systems.

5️⃣ Model Size
model_size_bytes: 3268911

≈ 3.2 MB model

Small models like this are perfect for real-time APIs.

Prefect Flow
↓
Model Training
↓
MLflow Model Registry
↓
Champion Model
↓
FastAPI Prediction Service
↓
Client Requests

Using:

Prefect

MLflow

FastAPI

This is already a real MLOps deployment pipeline.
