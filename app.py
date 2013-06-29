from flask import Flask
from flask.ext.peewee.db import Database
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = Database(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

if __name__ == '__main__':
    from partial.router import *
    app.run(port=2223)

# TODO
# logo pd teman ban
# sidebar kanan utk tampilin statistik