from flask import Flask
import threading
import socket


salary_prediction_app = Flask(__name__)
flask_thread = threading.Thread(target=salary_prediction_app.run, kwargs={'host':socket.gethostname(),'port':8000})
flask_thread.start()

from salary_prediction import routes