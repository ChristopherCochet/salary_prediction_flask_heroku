# Python: Deploying A Salary Prediction Model (Regression) Web API to the Cloud using a Flask App and Heroku

**Project description:** This is a guided project in which we describe concisely how to deploy a regression model (salary prediction) through a cloud API using a flask app and heroku.

<kbd> <img src="images/Model-Flask-Heroku.PNG?raw=true"/> </kbd>

Here are some good Heroku references to review for this projects:
* https://devcenter.heroku.com/categories/heroku-architecture
* https://devcenter.heroku.com/articles/heroku-cli
* https://devcenter.heroku.com/articles/using-the-cli
* https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
* https://www.youtube.com/watch?v=skc-ZEU9kO8
* https://www.kdnuggets.com/2020/05/build-deploy-machine-learning-web-app.html


### Tracking our progress
  - [ ] Train a salary prediction regression model and save the model and preprocessing pipeline 
  - [ ] Create a Python Flask app to expose the regression model through a web API
  - [ ] Test the Flask App locally
  - [ ] Create a Heroku build environment, Deploy and Test the Heroku Flask API to the Cloud

---

# 1. Train a salary prediction regression model and save the model and preprocessing steps

  ## Pre-requisite
  * Python and Scikit-learn environment installed
  * A job description and salary dataset used to train the regresison model
  * [The salary prediction regression modeling code](https://github.com/ChristopherCochet/salary_prediction_flask_heroku/blob/master/model_training/Salary%20Prediction%20-%20Regression.ipynb)

  ## Train and save the salary prediction regression model and the one hot encoder
  * The salary dataset contains salary information based on job descriptions such as level, experience, location, education and other features.  
  * It contains both categorical and numerical features.
  * Pre-processing steps are used including one hot encoding the categorical features - this ohe is saved in pickel format.
  * Different regression models are tested and the best performing model (performance metric is chosen MSE), a Gradient Boosting model, is saved in a pkl format using serialization. 
  
  Saving the preprocessing One Hot Encoder
  
  <kbd> <img src="images/preprocessing_ohe_pickle.PNG?raw=true"> </kbd>

  Saving the Gradient Boosting regression model
  
  <kbd> <img src="images/save_model_pickle.PNG?raw=true"> </kbd>

  Both the saved ohe and the regression model pickle files will be loaded by the Flask API to process incoming data and serve predictions. 

### Tracking our progress
  - [X] Train a salary prediction regression model and save the model and preprocessing pipeline 
  - [ ] Create a Python Flask app to expose the regression model through a web API
  - [ ] Test the Flask App locally
  - [ ] Create a Heroku build environment, Deploy and Test the Heroku Flask API to the Cloud


# 2. Create a Python Flask app to expose the regression model through a web API

  ## Pre-requisite
  * Flask - [we will use this framework to build a Web API used to serve salary predictions from the regression model traine](https://flask.palletsprojects.com/en/1.1.x/)
  * JSON - [we will use JSON to serialize, transmit and receive data to end from our mdeol over the web](https://en.wikipedia.org/wiki/JSON)
  * [JSON Python Module](https://www.youtube.com/watch?v=pTT7HMqDnJw)
  * [RESTful API](https://www.youtube.com/watch?v=7YcW25PHnAA)

  ## What is Flask ?

  > Flask is a popular Python web framework, meaning it is a third-party Python library used for developing web applications.
  > Flask is interconnected to two main parts:
  > * Werkzeug is a utility library meant for usage with the Python language. A Web Server Gateway Interface or WSGI app that can create software items for request,    response, or utility functions.
  > * Jinja is a template engine for Python programming purposes, and it resembles the Django web frameworks templates

  <kbd> <img src="images/flask.jpg?raw=true"/> </kbd>

   ## Create a Python Flask App and expose a Web (RESTful)  API
   Here we expose two endpoints:
   * '/' exposes a simple HTML welcome message and IP address  
   * '/index' exposes the Web API used to serve salary predictions using JSON format 

    ```
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
   
    ```

### Tracking our progress
  - [X] Train a salary prediction regression model and save the model and preprocessing pipeline 
  - [X] Create a Python Flask app to expose the regression model through a web API
  - [ ] Test the Flask App locally
  - [ ] Create a Heroku build environment, Deploy and Test the Heroku Flask API to the Cloud
 
# 3. Test the Flask App and API locally

## Pre-requisite
  * Git clone the following repo containing the python code and environment file

  1 - Activate your python environment and shell
  ```
  (venv) $ pipenv shell
  ```

  2 - Set the FLASK_APP environment variable to the app name
  ```
  (venv) $ set FLASK_APP=set FLASK_APP=salary_prediction/salary_prediction_app.py
  ```

  3 - Launch the flask app locally (localhost, port 5000 by default)
  ```
  (venv) $ flask run
  ```
  <kbd> <img src="images/flask_run.PNG?raw=true"> </kbd>

  4 - Test the Flask '/index' endpoint using a browser. The flask app is running loically on the following port by default: http://127.0.0.1:5000/ 

  <kbd> <img src="images/flask_local_test.PNG?raw=true"> </kbd>

  5 - Test the Flask '/predict' endpoint by using datapoints from our salary prediction test set

  ```
  import socket
  import json
  import joblib
  import requests
  import pandas as pd
  import numpy as np 
  from flask import Flask, jsonify, request

  # build 2 job records to get a salary prediction for
  j_data_list = test_df.iloc[5:7,].to_json(orient='records')
  parsed = json.loads(j_data_list)
  print(json.dumps(parsed, indent=4, sort_keys=True))
  ```
```
# print of the two JSON job records to test
[
    {
        "companyId": "COMP40",
        "degree": "MASTERS",
        "industry": "FINANCE",
        "jobId": "JOB1362685407692",
        "jobType": "CTO",
        "major": "COMPSCI",
        "milesFromMetropolis": 23,
        "yearsExperience": 6
    },
    {
        "companyId": "COMP32",
        "degree": "MASTERS",
        "industry": "SERVICE",
        "jobId": "JOB1362685407693",
        "jobType": "SENIOR",
        "major": "COMPSCI",
        "milesFromMetropolis": 32,
        "yearsExperience": 6
    }
]
```
```
  headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
  # send request to the local flask salary predcition end point
  r = requests.post(f"http://127.0.0.1:5000//predict", data=j_data_list, headers=headers)
  
  # print salary predctions returned
  print(r.text)
```

```
# Salary predictions returned by the flask API for two job descriptions 
"[150.71643399  96.42931186]"
```

## Test Results
Success, we have successfully tested locally the FLask API and predictions served by our model 

### Tracking our progress
  - [X] Train a salary prediction regression model and save the model and preprocessing pipeline 
  - [X] Create a Python Flask app to expose the regression model through a web API
  - [X] Test the Flask App locally
  - [ ] Create a Heroku build environment, Deploy and Test the Heroku Flask API to the Cloud


# 4. Create a Heroku build environment, Deploy and Test the Heroku Flask API to the Cloud

 <kbd> <img src="images/Heroku-Rest-Api.png?raw=true"> </kbd>

## Pre-requisite
  * [Heroku](https://www.heroku.com/what)
  * [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
  * [Heroku CLI installed on your dev machine](https://devcenter.heroku.com/articles/heroku-cli)
  * [Heroku CLI app deployment with git](https://devcenter.heroku.com/articles/git)
  * [Heroku account and login created](https://signup.heroku.com/)
  * Git installed - the Heroku platform uses Git as the primary means for deploying applications  

## What is Heroku ?

  > Heroku is a container-based cloud Platform as a Service (PaaS). Developers use Heroku to deploy, manage, and scale modern apps. 
  > Heroku sits on top of AWS and is specifically designed to make developers lives easier as developers do not have to worry about cloud infrastructure and can focus on the application they are building and want to depoy and scale.

 <kbd> <img src="images/heroku-logo.png?raw=true"> </kbd>

  1 - Log in your Heroku acocunt with the CLI
  ```
  (venv) $ heroku login
  ```

  2 - Go to the salary prediction directory and create an app
  ```
  (venv) $ heroku create
  ```

 <kbd> <img src="images/heroku-create.PNG?raw=true"> </kbd>

  3 - Add the current salary prediction opython code, flask app and seririalized model files to the current local git repo
  ```
  (venv) $ git init 
  (venv) $ git add .
  (venv) $ git commit -am "initial commit"
  (venv) $ git push heroku master
  ```
 
 <kbd> <img src="images/git-add.PNG?raw=true"> </kbd>
  
  3 - Add the current salary prediction opython code, flask app and seririalized model files to the current local git repo
  ```
  (venv) $ git push heroku master
  ```

  4 - Check the deployed heroku app status in the heroku online dashboard UI

  <kbd> <img src="images/heroku-app-dashboard.PNG?raw=true"> </kbd>

  5 - Test the Flask HTML API using a web browser and the Heroku app hostname provided  

  <kbd> <img src="images/flask_heroku_test.PNG?raw=true"> </kbd>

  6 - Test the Flask '/predict' endpoint by using datapoints from our salary prediction test set and the Heroku app hostname

```
  headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
  # send request to the local flask salary predcition end point
  r = r = requests.post(f"https://shrouded-spire-27908.herokuapp.com/predict", data=j_data_list, headers=headers)
  
  # print salary predctions returned
  print(r.text)
```

```
# Salary predictions returned by the flask API for two job descriptions 
"[150.71643399  96.42931186]"
```
6 - Check the Heroku app logs for any errors
We can see in the logs the input JSON job records received and succesfully processed by the /predict flask Heroku endpoint

 ```
  (venv) $ heroku logs
  ```
  <kbd> <img src="images/heroku-logs.PNG?raw=true"> </kbd>

## Test Results
Success !!! We have successfully tested the build and deployment of the Flask API to the cloud with Heroku, predictions served by our model match the ones tested locally 

### Tracking our progress
  - [X] Train a salary prediction regression model and save the model and preprocessing pipeline 
  - [X] Create a Python Flask app to expose the regression model through a web API
  - [X] Test the Flask App locally
  - [X] Create a Heroku build environment, Deploy and Test the Heroku Flask API to the Cloud