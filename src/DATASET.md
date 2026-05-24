Your pipeline is not tied to CitiBikes — it can work with any tabular dataset as long as you adapt the data preparation step (process_data()).

Right now your project predicts bike ride duration, but the architecture works for any regression problem.

Your stack is:

Prefect → pipeline orchestration

MLflow → experiment tracking

scikit-learn → model training

So you can plug in any dataset that fits structured/tabular ML.

# 1️⃣ California Housing (very popular)

Predict house prices.

Dataset:
California Housing Dataset

Features:

median income

house age

rooms

population

Target:

median_house_value

Why it's good:

simple

clean

widely used in ML tutorials

# 2️⃣ NYC Taxi Trip Duration

Very similar to CitiBike but bigger.

Dataset:
NYC Taxi Trip Duration Dataset

Predict:

trip_duration

Features:

pickup location

dropoff location

passenger count

timestamp

Good because it resembles real ride-sharing systems.

# 3️⃣ House Prices Dataset

Another classic dataset.

Dataset:
House Prices Advanced Regression Techniques

Target:

SalePrice

Features include:

house size

neighborhood

year built

garage type

Good for demonstrating feature engineering.

# 4️⃣ Airline Delay Dataset

Predict flight delay time.

Dataset:
US Flight Delay Dataset

Target example:

arrival_delay

Features:

airline

airport

weather

departure time

# What You Need to Change in the Project

Only one file usually needs changes:

src/data/prepare.py

Your function probably does something like:

select features
create target
split train/validation

Example generic version:

X = df.drop(columns=["target"])
y = df["target"]

X_train, X_valid, y_train, y_valid = train_test_split(
X, y, test_size=0.2, random_state=42
)

As long as you output:
X_train
y_train
X_valid
y_valid
your training pipeline will still work.

# What Makes a Dataset Compatible With Your Pipeline

Your models from scikit-learn expect:

✔ tabular data
✔ numeric or categorical columns
✔ regression target

Examples of targets:

price
duration
sales
temperature
demand

# 👉 NYC Taxi Trip Duration

Because your project becomes:

Ride Duration Prediction Platform

Architecture:

Prefect Pipeline
↓
Feature Engineering
↓
Train Models
↓
MLflow Tracking
↓
Best Model Selection

This looks very realistic on a resume.
