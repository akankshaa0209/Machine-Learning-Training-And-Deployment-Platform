Best order:

1️⃣ Hyperparameter tuning
Use GridSearchCV in scikit-learn

2️⃣ Automatic best model selection
Automatically pick lowest RMSE.

3️⃣ MLflow Model Registry
Register the best model.

4️⃣ Prediction API
Deploy using FastAPI

5️⃣ Docker deployment
Containerize the whole system.

# Automatic best model selection + model registration.

compare models
↓
pick best RMSE
↓
register best model in MLflow

Automatically choose the best model (lowest RMSE) and register it in the MLflow Model Registry.
We’ll use the MLflow Model Registry.
Prefect Flow
↓
Train 3 models
↓
Compare RMSE
↓
Register best model
↓
Deploy

Train Ridge
↓
Train GradientBoosting
↓
Train RandomForest
↓
Compare RMSE
↓
Register BEST model

1️⃣ Import the MLflow sklearn module
At the top of train.py, add: import mlflow.sklearn
This lets MLflow save and register models.

2️⃣ Modify run_models() Function
Right now your function just trains models.
We will modify it to:
Track the best RMSE
Save the best model
Register it

3️⃣ Run Training Again
python -m src.training.train \
--train_file 202206-capitalbikeshare-tripdata.zip \
--valid_file 202205-capitalbikeshare-tripdata.zip

4️⃣ Open MLflow UI

Go to:

http://127.0.0.1:5000

Now click:

Model Registry

You should see a model named:

citibike-duration-model

This means the best model was automatically registered.

5️⃣ What Your Pipeline Now Does

Your system now works like this:

Prefect Pipeline
↓
Train 3 models
↓
Evaluate RMSE
↓
Select best model
↓
Register model in MLflow

Models come from scikit-learn:

Ridge Regression

Gradient Boosting Regressor

Random Forest Regressor

==============
✔ Data pipeline with Prefect
✔ Experiment tracking with MLflow
✔ Multiple model training
✔ Automatic best model selection
✔ Model registry
======================

1️⃣ Hyperparameter tuning

Use GridSearchCV

2️⃣ Prediction API

Deploy model with FastAPI

3️⃣ Docker deployment
4️⃣ Scheduled retraining pipeline
========================
Dataset
↓
DictVectorizer (once)
↓
Train Ridge
Train GradientBoosting
Train ExtraTrees
↓
Compare RMSE
↓
Register best model in MLflow

=================================
Download dataset
↓
Feature engineering
↓
Train Ridge
↓
Train GradientBoosting
↓
Compare RMSE
↓
Register best model

All runs are tracked in MLflow, which is the important part.

This already demonstrates:

✔ experiment tracking
✔ metric logging
✔ model artifacts
✔ best model selection
✔ model registry

Those are core MLOps concepts.
