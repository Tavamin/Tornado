from flask import Flask
from decouple import config

from core.urls import routes
from core.router import Router


app = Flask(__name__)
app.config['SECRET_KEY'] = config('FLASK_SECRET_KEY')
router = Router(app, routes)

if __name__ == '__main__':
    # from core.utils import create_tables
    # create_tables()
    # app.run(debug=True, port=5005)
    ...
