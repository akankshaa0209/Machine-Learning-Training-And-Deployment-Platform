from fastapi import FastAPI
import mlflow
import mlflow.pyfunc
import pandas as pd

mlflow.set_tracking_uri("http://localhost:5000")

app = FastAPI()

# Load the model from MLflow Model Registry/ production stage
# model = mlflow.pyfunc.load_model("models:/citibike-duration-model/1")
# model = mlflow.pyfunc.load_model("models:/citibike-duration-model/Production")
model = mlflow.pyfunc.load_model("models:/citibike-duration-model@champion")

# print("Loaded model:", model.metadata.run_id)
print("Model loaded successfully")
print(model.metadata)

@app.get("/")
def home():
    return {"message": "Citibike duration prediction API"}

@app.post("/predict")
def predict(data: dict):

    # df = pd.DataFrame([data])

    # prediction = model.predict(df)

    prediction = model.predict([data])

    # log prediction
    with mlflow.start_run(nested=True):

        # log input parameters
        mlflow.log_param("rideable_type", data["rideable_type"])
        mlflow.log_param("trip_distance", data["trip_distance"])
        mlflow.log_param("start_end_id", data["start_end_id"])

        # log prediction
        mlflow.log_metric("predicted_duration", float(prediction))

    return {"predicted_duration": float(prediction[0])}