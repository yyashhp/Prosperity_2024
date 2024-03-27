import pandas as pd
import numpy as np


data = pd.read_csv('tutorial_data.csv')
data.fillna(0, inplace=True)
data = data.reset_index()
data.columns = data.iloc[0]
data = data.drop(0)
data = data.fillna(0)
print(data['timestamp'])
data.to_csv('tutorial_data_cl.csv', index=False)
data_cl = pd.read_csv('tutorial_data_cl.csv')
print(data_cl.head())
print(data_cl.columns)
print(data_cl.index)