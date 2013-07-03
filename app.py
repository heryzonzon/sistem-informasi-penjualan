from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import filters

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.filters['rupiah'] = filters.to_rupiah
app.jinja_env.filters['datetime'] = filters.format_datetime

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

if __name__ == '__main__':
    from partial.router import *
    app.run()

# TODO
# sidebar kanan utk tampilin statistik
# username to be lowercase and unique
