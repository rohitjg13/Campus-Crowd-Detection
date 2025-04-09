from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

data = pd.read_csv(r"mfcc_dataset.csv")

y = data["Crowd_Density"]

x = data[list(i for i in data.acolumns if "MFCC" in i)]

model = RandomForestRegressor(n_estimators=100)
model.fit(x[:400], y[:400])

score = 0
n = 0
for i in range(400, len(x)):
    r = x.iloc[i:i+1]
    score += abs((model.predict(r) - y.iloc[i])**2)
    n += 1

print(score)
