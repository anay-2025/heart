import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

import warnings
warnings.filterwarnings("ignore")

# Load Data

df = pd.read_csv("heart.csv")

# Edit Data

df.drop_duplicates(inplace=True)

df.dropna(inplace=True)

df.reset_index(drop=True, inplace=True)

categorical_cols = [
    "cp",
    "restecg",
    "slope",
    "thal",
    "ca"
]

df_original = df
df = pd.get_dummies(
    df,
    columns=categorical_cols,
    drop_first=True
)

X = df.drop(["num", "target_binary"], axis=1)
y = df["target_binary"]

# Save features 

pickle.dump(X.columns.tolist(), open("columns.pkl", "wb"))

# Data for train and test

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Scaling the data

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model

model = LogisticRegression()
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))

