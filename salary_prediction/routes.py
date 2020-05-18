from salary_prediction import salary_prediction_app
import socket
import json
import joblib
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request

ip_address = socket.gethostbyname(socket.gethostname())

#trained_model = joblib.load("model.pkl")
#var_means = pickle.load(open("columns_mean.pkl", "rb" ) )

@salary_prediction_app.route('/')
@salary_prediction_app.route('/index')
def index():
    return ("<H1>Hello, World!</H1> <H2>API IP Address: {} </H2>".format(ip_address))

@app.route('/predict', methods=['POST'])
def predict():
  data = request.get_json()
  df_test = pd.DataFrame(data, index=[0])
  for col, avg_value in var_means.items():
    df_test[col].fillna(avg_value, inplace=True)
  prediction = trained_model.predict(df_test)
  str_pred = np.array2string(prediction)
  return jsonify(str_pred)
