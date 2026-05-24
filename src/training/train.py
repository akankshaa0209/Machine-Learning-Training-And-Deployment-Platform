import os
import time
import argparse
from datetime import datetime

import mlflow
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import mlflow.sklearn #lets MLflow save and register models.
from prefect import flow, task, get_run_logger
from sklearn.impute import SimpleImputer
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from prefect.context import get_run_context
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.pipeline import make_pipeline
from category_encoders import OneHotEncoder
from prefect.task_runners import SequentialTaskRunner
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.feature_extraction import DictVectorizer

from src.data.prepare import process_data

@task(name="Run models")
def run_models(X_train, y_train, X_valid, y_valid):

    best_rmse = float("inf")
    best_model = None
    best_model_name = None

    for model_class in (Ridge, GradientBoostingRegressor):

        with mlflow.start_run():

            mlflow.set_tag("model_name", model_class.__name__)

            if model_class.__name__ == "GradientBoostingRegressor":
                model_instance = model_class(
                    n_estimators=30,
                    learning_rate=0.1,
                    max_depth=3,
                    random_state=42
                )
            else:
                model_instance = model_class(random_state=42)

            # Build pipeline (VERY IMPORTANT)
            model = make_pipeline(
                DictVectorizer(),
                SimpleImputer(strategy="most_frequent"),
                model_instance
            )

            # Train model
            model.fit(X_train.to_dict(orient="records"), y_train)

            # Predictions
            y_pred_train = model.predict(X_train.to_dict(orient="records"))
            y_pred_valid = model.predict(X_valid.to_dict(orient="records"))

            mae_train = mean_absolute_error(y_train, y_pred_train)
            mae_valid = mean_absolute_error(y_valid, y_pred_valid)

            rmse_train = mean_squared_error(y_train, y_pred_train) ** 0.5
            rmse_valid = mean_squared_error(y_valid, y_pred_valid) ** 0.5

            # Log metrics
            mlflow.log_metric("mae_train", mae_train)
            mlflow.log_metric("mae_valid", mae_valid)
            mlflow.log_metric("rmse_train", rmse_train)
            mlflow.log_metric("rmse_valid", rmse_valid)

            # Save model
            from mlflow.models import infer_signature

            signature = infer_signature(
                X_train.to_dict(orient="records"),
                y_pred_train
            )

            mlflow.sklearn.log_model(
                model,
                "model",
                signature=signature
            )

            # Track best model
            if rmse_valid < best_rmse:
                best_rmse = rmse_valid
                best_model = model
                best_model_name = model_class.__name__

    # Register best model
    if best_model:
        mlflow.sklearn.log_model(
            best_model,
            "best_model",
            registered_model_name="citibike-duration-model"
        )

        print(f"Best model: {best_model_name} with RMSE {best_rmse}")

# @task(name="Run models")
# def run_models(X_train, y_train, X_valid, y_valid):

#     from sklearn.feature_extraction import DictVectorizer

#     dv = DictVectorizer()
#     X_train_dict = X_train.to_dict(orient="records")
#     X_valid_dict = X_valid.to_dict(orient="records")

#     X_train_vec = dv.fit_transform(X_train_dict)
#     X_valid_vec = dv.transform(X_valid_dict)

#     best_rmse = float("inf")
#     best_model = None
#     best_model_name = None

#     # for model_class in (Ridge, GradientBoostingRegressor, ExtraTreesRegressor):
#     for model_class in (Ridge, GradientBoostingRegressor):

#         with mlflow.start_run():

#             mlflow.set_tag("model_name", model_class.__name__)

#             if model_class.__name__ == "ExtraTreesRegressor":
#                 model_instance = model_class(
#                     n_estimators=50, #number of trees in the forest halved
#                     n_jobs=-1,  #use all cores for training
#                     random_state=42
#                 )

#             elif model_class.__name__ == "GradientBoostingRegressor":
#                 model_instance = model_class(
#                     n_estimators=30, #number of boosting stages halved
#                     learning_rate=0.1, #learning rate increased
#                     max_depth=3, #max depth of the individual regression estimators reduced
#                     random_state=42
#                 )
#             else:
#                 model_instance = model_class(random_state=42)

#             # Build model
#             model = make_pipeline(
#                 SimpleImputer(),
#                 model_instance
#             )
            

#             model.fit(X_train_vec, y_train)

#             # Predictions
#             y_pred_train = model.predict(X_train_vec)
#             y_pred_valid = model.predict(X_valid_vec)

#             mae_train = mean_absolute_error(y_train, y_pred_train)
#             mae_valid = mean_absolute_error(y_valid, y_pred_valid)

#             rmse_train = mean_squared_error(y_train, y_pred_train) ** 0.5
#             rmse_valid = mean_squared_error(y_valid, y_pred_valid) ** 0.5

#             mlflow.log_metric("mae_train", mae_train)
#             mlflow.log_metric("mae_valid", mae_valid)
#             mlflow.log_metric("rmse_train", rmse_train)
#             mlflow.log_metric("rmse_valid", rmse_valid)

#             # Save model artifact
#             # mlflow.sklearn.log_model(model, "model")
#             from mlflow.models import infer_signature

#             signature = infer_signature(X_train_vec, y_pred_train)

#             mlflow.sklearn.log_model(
#                      model,
#                      "model",
#                      signature=signature
#             )

#             # Check if this is best model
#             if rmse_valid < best_rmse:
#                 best_rmse = rmse_valid
#                 best_model = model
#                 best_model_name = model_class.__name__

#     # Register best model
#     if best_model:
#         mlflow.sklearn.log_model(
#             best_model,
#             "best_model",
#             registered_model_name="citibike-duration-model"
#         )

#         print(f"Best model: {best_model_name} with RMSE {best_rmse}")


# @task(name="Run models")
# def run_models(X_train, y_train, X_valid, y_valid):

#     best_rmse = float("inf")
#     best_model = None
#     best_model_name = None

#     for model_class in (Ridge, GradientBoostingRegressor, ExtraTreesRegressor):

#         with mlflow.start_run():

#             mlflow.set_tag("model_name", model_class.__name__)

#             if model_class.__name__ == "RandomForestRegressor":
#                 model_instance = model_class(
#                     n_estimators=50, #number of trees in the forest halved
#                     n_jobs=-1,  #use all cores for training
#                     random_state=42
#                 )

#             elif model_class.__name__ == "GradientBoostingRegressor":
#                 model_instance = model_class(
#                     n_estimators=30, #number of boosting stages halved
#                     learning_rate=0.1, #learning rate increased
#                     max_depth=3, #max depth of the individual regression estimators reduced
#                     random_state=42
#                 )
#             else:
#                 model_instance = model_class(random_state=42)

#             # Build model
#             model = make_pipeline(
#                 DictVectorizer(),
#                 SimpleImputer(),
#                 model_class(random_state=42),
#             )
            

#             model.fit(X_train.to_dict(orient="records"), y_train)

#             # Predictions
#             y_pred_train = model.predict(X_train.to_dict(orient="records"))
#             y_pred_valid = model.predict(X_valid.to_dict(orient="records"))

#             mae_train = mean_absolute_error(y_train, y_pred_train)
#             mae_valid = mean_absolute_error(y_valid, y_pred_valid)

#             rmse_train = mean_squared_error(y_train, y_pred_train) ** 0.5
#             rmse_valid = mean_squared_error(y_valid, y_pred_valid) ** 0.5

#             mlflow.log_metric("mae_train", mae_train)
#             mlflow.log_metric("mae_valid", mae_valid)
#             mlflow.log_metric("rmse_train", rmse_train)
#             mlflow.log_metric("rmse_valid", rmse_valid)

#             # Save model artifact
#             mlflow.sklearn.log_model(model, "model")

#             # Check if this is best model
#             if rmse_valid < best_rmse:
#                 best_rmse = rmse_valid
#                 best_model = model
#                 best_model_name = model_class.__name__

#     # Register best model
#     if best_model:
#         mlflow.sklearn.log_model(
#             best_model,
#             "best_model",
#             registered_model_name="citibike-duration-model"
#         )

#         print(f"Best model: {best_model_name} with RMSE {best_rmse}")


# @task(name="Run models")
# def run_models(X_train, y_train, X_valid, y_valid):
#     for model_class in (Ridge, GradientBoostingRegressor, RandomForestRegressor):
#         with mlflow.start_run():

#             mlflow.set_tag("model_name", model_class.__name__)

#             # Build and Train model
#             model = make_pipeline(
#                 DictVectorizer(),
#                 SimpleImputer(),
#                 model_class(random_state=42),
#             )
#             model.fit(X_train.to_dict(orient="records"), y_train)

#             # MLflow logging
#             start_time = time.time()
#             y_pred_train = model.predict(X_train.to_dict(orient="records"))
#             y_pred_valid = model.predict(X_valid.to_dict(orient="records"))
#             inference_time = time.time() - start_time

#             mae_train = mean_absolute_error(y_train, y_pred_train)
#             mae_valid = mean_absolute_error(y_valid, y_pred_valid)

#             rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
#             rmse_valid = np.sqrt(mean_squared_error(y_valid, y_pred_valid))

#             # rmse_train = mean_squared_error(y_train, y_pred_train, squared=False)
#             # rmse_valid = mean_squared_error(y_valid, y_pred_valid, squared=False)

#             mlflow.set_tag("author/developer", "PatrickCmd")
#             mlflow.set_tag("Model", f"{model_class}")

#             mlflow.log_metric("mae_train", mae_train)
#             mlflow.log_metric("mae_valid", mae_valid)
#             mlflow.log_metric("rmse_train", rmse_train)
#             mlflow.log_metric("rmse_valid", rmse_valid)
#             mlflow.log_metric(
#                 "inference_time",
#                 inference_time / (len(y_pred_train) + len(y_pred_valid)),
#             )


@flow(name="mlflow-training", task_runner=SequentialTaskRunner())
def main(train_file, valid_file):
    # Set and run experiment
    ctx = get_run_context()
    MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
    EXPERIMENT_NAME = (
        f"citibikes-experiment-{ctx.flow_run.expected_start_time.strftime('%Y-%m-%d')}"
    )

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)
    mlflow.sklearn.autolog() ##to save the models

    logger = get_run_logger()
    logger.info("Process data features for model training and validation")
    X_train, y_train, X_valid, y_valid = process_data(train_file, valid_file)
    logger.info(
        f"Train and Validation df shapes: {X_train.shape}, {y_train.shape}, {X_valid.shape}, {y_valid.shape}"
    )

    # Print feature columns and sample record for FastAPI input schema
    #DictVectorizer → SimpleImputer → Model from scikit-learn pipeline, the feature columns are the original columns from the dataset before vectorization and imputation. These columns represent the raw features that are used as input to the model. The DictVectorizer will convert these categorical features into a format suitable for machine learning models, and the SimpleImputer will handle any missing values in the dataset. However, the original feature columns remain unchanged and are what we want to display for understanding the input schema for FastAPI.
    #DictVectorizer converts dictionary features → numeric vectors, so your API request must match those keys exactly.
    print("\nTraining Feature Columns:")
    print(X_train.columns)

    print("\nSample Training Record:")
    print(X_train.iloc[0].to_dict())

    # Run models
    logger.info("Training models")
    run_models(X_train, y_train, X_valid, y_valid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_file", help="file for training data.")
    parser.add_argument("--valid_file", help="file for validation data.")
    args = parser.parse_args()

    parameters = {
        "train_file": args.train_file,
        "valid_file": args.valid_file,
    }
    main(**parameters)
