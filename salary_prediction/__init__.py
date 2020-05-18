from flask import Flask
import threading
import socket


salary_prediction_app = Flask(__name__)
flask_thread = threading.Thread(target=salary_prediction_app.run, kwargs={'host':'0.0.0.0','port':8000})
flask_thread.start()

from salary_prediction import routes