from flask import Flask
import threading

salary_prediction_app = Flask(__name__)
flask_thread = threading.Thread(target=app.run, kwargs={'host':'0.0.0.0','port':80})
flask_thread.start()

from salary_prediction import routes