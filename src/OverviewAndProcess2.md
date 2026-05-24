echo. > src/data/**init**.py  
rmdir /s /q .ipynb_checkpoints

pip install tqdm
pip install haversine

python -m pip install --upgrade pip
pip install requirements.txt
pip freeze > requirements.txt

//python src/training/train.p = wont run
python -m src.training.train
at first= failed to est connection because the target machine actively refused it

so 1) run: mlflow ui
2)had to modify train.py and prepare.py
3)python -m src.training.train --train_file 202206-capitalbikeshare-tripdata.zip --valid_file 202205-capitalbikeshare-tripdata.zip

This will:

1️⃣ Process data
2️⃣ Train 3 models
3️⃣ Log experiments to MLflow

Models trained:

Ridge Regression

Gradient Boosting Regressor

Random Forest Regressor

other models:

# Use ExtraTreesRegressor.

from sklearn.ensemble import ExtraTreesRegressor
Why it's faster:

trees are more randomized

less computation during splits

parallelized with n_jobs

# Another Fast Model: SGD Regressor

from sklearn.linear_model import SGDRegressor
Use SGDRegressor.

This is extremely fast for large datasets.

# from sklearn.tree import DecisionTreeRegressor

predicts bike ride duration, but the architecture works for any regression problem.
Tech stack is:
Prefect → pipeline orchestration
MLflow → experiment tracking
scikit-learn → model training
So you can plug in any dataset that fits structured/tabular ML.

steps in a machine-learning pipeline built using scikit-learn. They prepare your data and then train the model.

They usually appear inside a pipeline like:

model = make_pipeline(
DictVectorizer(), converts Python dictionaries into numeric feature vectors.
SimpleImputer(), It fills missing values (NaN) in your data.
model_class(random_state=42), This is the actual machine learning model. random_state=42 ensures reproducibility.
)

Raw dictionary data
↓
DictVectorizer
↓
SimpleImputer
↓
Machine Learning Model
↓
Prediction

data → feature encoding → missing value fix → model training

====ABOUT MLFLOW===

# 1 An experiment groups multiple training runs for the same problem.

Each time you run:
python -m src.training.train ...
MLflow creates a new run inside this experiment.

# 2 Each row in the table is a single model training run.

This means:a model was trained
parameters were recorded
metrics were logged
artifacts (models, plots) were saved

Your script trains 3 models: (train.py) (come from scikit-learn)
Ridge Regression
Gradient Boosting Regressor
Random Forest
MLflow creates one run per model.

where trained models saved : col:model:mlflow saved the trained pipeline as an artifact.
model/
MLmodel
model.pkl
conda.yaml

What Those Files Mean

Inside each model folder you showed:

model.pkl

→ serialized model (pickle)

MLmodel

→ metadata describing the model

requirements.txt

→ dependencies to load the model

conda.yaml

→ environment reproducibility

This is the MLflow Model Format.

this is the trained piepline:
DictVectorizer
→ SimpleImputer
→ Model

mlflow.sklearn.autolog() ##to save the models
model, params, metrics, artifacts, feature pipeline.

So every run corresponds to one of those models.

# 3 Duration Column

This is how long the training run took.
This includes:feature transformation,model training,evaluation

# 4 Source Column

C:\Projects\scalable-ml-platform
This shows where the training code ran from.

# 5 Models Column

This means MLflow saved the trained model as an artifact.
Artifacts include:trained models, plots,feature transformers,data files
These are stored in MLflow's artifact store.

# 6 What Happens If You Click a Run

If you click a run like: judicious-cod-88
You will see:Metrics
Example:
mae_train
mae_valid
rmse_train
rmse_valid
inference_time
These tell you how good the model is.

Parameters
Example:
model type
hyperparameters
These describe how the model was trained.

Artifacts
Example:
model.pkl
pipeline.pkl
These are saved models you can deploy.

# 7 Why This Is Powerful

This solves a huge ML problem: When training many models, people usually lose track of: which model performed best
which hyperparameters were used
which dataset was used
MLflow tracks everything automatically.
You can compare experiments like this:
Model A RMSE = 0.78
Model B RMSE = 0.65
Model C RMSE = 0.72
Then deploy the best model.

# 8 production-style ML workflow:

Prefect Flow
↓
Data Processing
↓
Train Multiple Models
↓
Log Metrics
↓
Store Models
↓
MLflow Experiment UI

You just built a real MLOps pipeline using:

Prefect

MLflow

scikit-learn

# 9 Next steps:

1️⃣ Model Registry (version models)
2️⃣ FastAPI inference API
3️⃣ Docker deployment
4️⃣ CI/CD for retraining

That turns this into a production ML platform.

# 10 Understanding and interpreting the metrics for best model:

any successful run: Metrics, Parameters, Artifacts

Metrics:
mae_train
mae_valid
rmse_train
rmse_valid
inference_time

MAE (Mean Absolute Error): MAE = average(|actual - predicted|)
lower is better.

RMSE (Root Mean Squared Error): RMSE = sqrt(mean((actual - predicted)^2))
Lower is better.

Train vs Validation metrics: tell if model is overfitting.
mae_train
mae_valid
rmse_train
rmse_valid

Good Model
rmse_train = 5.1
rmse_valid = 5.4
Training and validation are close.
Model generalizes well.

Overfitting Model
rmse_train = 2.1
rmse_valid = 12.4
Model memorized training data
but performs badly on new data
Bad model.

Underfitting Model
rmse_train = 15
rmse_valid = 16
Model too simple
cannot learn patterns
Also bad.

Inference Time: prediction_time / number_of_samples
In production systems like:
ride prediction
recommendation systems
fraud detection
we need fast predictions.

In general, for all trained models we compare validation metrics (rmse_valid) and pick the model among those.

After selecting best model: MOdel registry.
Best Model
↓
Register Model
↓
Version Control
↓
Deploy API

Prefect Flow
↓
Feature Engineering
↓
Train Multiple Models
↓
Evaluate Metrics
↓
Log Experiments
↓
MLflow UI

That workflow is exactly why tools like:MLflow,Weights & Biases exist.
train multiple models
↓
log experiments
↓
compare metrics
↓
choose best model

==============================

1. mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts --host 0.0.0.0 --port 5000
2. python -m src.training.train --train_file 202206-capitalbikeshare-tripdata.zip --valid_file 202205-capitalbikeshare-tripdata.zip
   promote mode
3. uvicorn service.predict:app --reload
