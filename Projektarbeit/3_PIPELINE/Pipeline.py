import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import cross_val_score




data = pd.read_csv('vehicle_emissions.csv')  

X = data.drop(["CO2_Emissions"], axis=1)
y = data["CO2_Emissions"]



numerical_cols = ["Model_Year", "Engine_Size", "Cylinders", "Fuel_Consumption_in_City(L/100 km)", "Fuel_Consumption_in_City_Hwy(L/100 km)", "Fuel_Consumption_comb(L/100km)", "Smog_Level"]
categorical_cols = ["Make", "Model", "Transmission", "Vehicle_Class"]

numerical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="mean")),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="most_frequent")),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', numerical_pipeline, numerical_cols),
    ('cat', categorical_pipeline, categorical_cols)
])


pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor())
])

scores = cross_val_score(pipeline, X, y, cv=5)

print(scores)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline.fit(X_train, y_train)

prediction = pipeline.predict(X_test)

mse = mean_squared_error(y_test, prediction)
mae = mean_absolute_error(y_test, prediction)
r2  = r2_score(y_test, prediction)
rsme = np.sqrt(mse)


train_prediction = pipeline.predict(X_train)


mse_train = mean_squared_error(y_train, train_prediction)
mae_train = mean_absolute_error(y_train, train_prediction)
r2_train  = r2_score(y_train, train_prediction)
rmse_train = np.sqrt(mse_train)

print(f"Training R-squared: {r2_train}")
print(f"Test R-squared: {r2}")

print(f"Mean Squared Error: {rsme}")
print(f"Mean Absolute Error: {mae}")
print(f"R-squared: {r2}")




joblib.dump(pipeline, 'co2_model.joblib')  

