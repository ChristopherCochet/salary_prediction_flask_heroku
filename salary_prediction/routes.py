from salary_prediction import salary_prediction_app

@salary_prediction_app.route('/')
@salary_prediction_app.route('/index')
def index():
    return "<H1>Hello, World!</H1>"
