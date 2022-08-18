from config import config
from flask import Flask
from flask_cors import CORS, cross_origin


# Routes
from routes.auth import Auth
from routes.room import Room
from routes.user import User

app = Flask(__name__)
app.config['CORS_HEADERS'] = ['Content-Type']
CORS(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})

UPLOADED_FOLDER = 'static/files/'

app.config['UPLOADED_FOLDER'] = UPLOADED_FOLDER


def page_not_found(error):
    return "<h1>Not found page </h1>", 404


@app.route('/')
def index():
    return 'Health up'

# Routes
app.register_blueprint(Auth.main, url_prefix='/auth')
app.register_blueprint(Room.main, url_prefix='/room')
app.register_blueprint(User.main, url_prefix='/user')

# Errors
app.register_error_handler(404, page_not_found)


if __name__ == '__main__':
    app.config.from_object(config['development'])

    app.run()
