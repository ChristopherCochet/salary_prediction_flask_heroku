from flask import Flask

salary_prediction_app = Flask(__name__)

@salary_prediction_app.route('/')
@salary_prediction_app.route('/index')
def index():
    return "<H1>Hello, World, this is Chris!</H1>"