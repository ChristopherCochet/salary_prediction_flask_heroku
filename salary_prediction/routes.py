
import socket
import json
import joblib
import logging
import requests
import pandas as pd
import numpy as np
import warnings

from salary_prediction import salary_prediction_app
#from sklearn.ensemble import GradientBoostingRegressor
from flask import Flask, jsonify, request

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.DEBUG)

def one_hot_encode_feature_df(df, cat_vars=None, num_vars=None, ohe = None):
    '''performs one-hot encoding on all categorical variables and combines result with continous variables'''
    cat_df = pd.DataFrame(ohe.transform(df[cat_vars]), columns = ohe.get_feature_names())       
    num_df = df[num_vars].apply(pd.to_numeric)
    df = pd.concat([cat_df, num_df], axis=1)
    return df

#define columns
salary_col = ['jobId',
 'companyId',
 'jobType',
 'degree',
 'major',
 'industry',
 'yearsExperience',
 'milesFromMetropolis']

categorical_vars = ['companyId', 'jobType', 'degree', 'major', 'industry']
numeric_vars = ['yearsExperience', 'milesFromMetropolis']

ip_address = socket.gethostbyname(socket.gethostname())

# load model
salary_prediction_model = joblib.load("salary_prediction/salary_prediction_model.pkl")
# load ohe
salary_prediction_ohe = joblib.load("salary_prediction/salary_prediction_ohe.pkl")


@salary_prediction_app.route('/')
@salary_prediction_app.route('/index')
def index():
    return ("<H1>Salary Prediction End Point!</H1> <H2>API IP Address: {} </H2>".format(ip_address))

@salary_prediction_app.route('/predict', methods=['POST'])
def predict():
  data_unseen = request.get_json()
  logging.debug(data_unseen)
  df_unseen = pd.DataFrame(data_unseen, columns = salary_col)
  logging.debug(df_unseen)
  df_unseen = one_hot_encode_feature_df(df_unseen, cat_vars=categorical_vars, num_vars=numeric_vars, ohe = salary_prediction_ohe)
  logging.debug(df_unseen)

  prediction = salary_prediction_model.predict(df_unseen)
  str_pred = np.array2string(prediction)
  return jsonify(str_pred)
