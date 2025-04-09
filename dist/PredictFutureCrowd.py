import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from datetime import datetime
import pickle
import os

def train_and_save_model(file_path):
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)
    
    df['Date_Time'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['Hour'] = df['Date_Time'].dt.hour
    df['Minute'] = df['Date_Time'].dt.minute
    df['Day_of_Week'] = df['Date_Time'].dt.dayofweek
    df['Day_of_Month'] = df['Date_Time'].dt.day
    df['Month'] = df['Date_Time'].dt.month
    
    aggregated_df = df.groupby(['Date_Time', 'Hour', 'Minute', 'Day_of_Week', 'Day_of_Month', 'Month'])['Crowd_Density'].mean().reset_index()
    
    features = ['Hour', 'Minute', 'Day_of_Week', 'Day_of_Month', 'Month']
    X = aggregated_df[features].values
    y = aggregated_df['Crowd_Density'].values
    
    X_scaler = MinMaxScaler()
    X_scaled = X_scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Training R² Score: {train_score:.4f}")
    print(f"Testing R² Score: {test_score:.4f}")
    
    print("Saving model and scaler...")
    with open('crowd_density_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    with open('X_scaler.pkl', 'wb') as f:
        pickle.dump(X_scaler, f)

    print("Model and scaler saved successfully!")
    return model, X_scaler

def load_model():
    try:
        print("Loading saved model and scaler...")
        with open('crowd_density_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        with open('X_scaler.pkl', 'rb') as f:
            X_scaler = pickle.load(f)
        
        print("Model and scaler loaded successfully!")
        return model, X_scaler
    except FileNotFoundError:
        print("Error: Model files not found. Please train the model first.")
        return None, None

def predict_crowd_density(model, X_scaler, day, time):
    if model is None or X_scaler is None:
        print("Error: Model not loaded. Please load or train the model first.")
        return None
        
    try:
        date_time = datetime.strptime(f"2025-04-01 {time}", "%Y-%m-%d %I:%M %p")
    except ValueError:
        try:
            date_time = datetime.strptime(f"2025-04-01 {time}", "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError(
                "Time format not recognized. Please use either '09:00 AM' format or '13:00' format."
            )
    
    days_map = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    day_of_week = days_map.get(day.lower(), date_time.weekday())
    
    features = [
        date_time.hour,
        date_time.minute,
        day_of_week,
        date_time.day,
        date_time.month
    ]
    
    features_scaled = X_scaler.transform(np.array(features).reshape(1, -1))
    
    prediction = model.predict(features_scaled)
    
    return prediction[0]

if __name__ == "__main__":
    print("Crowd Density Prediction Tool")
    print("-----------------------------")
    
    model, X_scaler = load_model()
    
    while True:
        print("\n===== Crowd Density Prediction =====")
        print("1. Train new model")
        print("2. Make prediction")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            file_path = input("Enter the path to your CSV file: ")
            if os.path.exists(file_path):
                model, X_scaler = train_and_save_model(file_path)
            else:
                print("Error: File not found!")
                
        elif choice == '2':
            if model is None:
                model, X_scaler = load_model()
                
            if model is not None:
                day = input("Enter day (e.g., Monday, Tuesday): ")
                time = input("Enter time (e.g., 09:00 AM or 13:00): ")
                
                try:
                    density = predict_crowd_density(model, X_scaler, day, time)
                    print(f"Predicted crowd density: {density:.2f}")
                except Exception as e:
                    print(f"Error: {e}")
            
        elif choice == '3':
            print("Exiting program.")
            break
            
        else:
            print("Invalid choice. Please try again.")