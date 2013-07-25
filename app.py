from flask import Flask
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.mongorest import MongoRest

app = Flask(__name__)
app.config.from_object('config')
db = MongoEngine(app)
api = MongoRest(app)
app.session_interface = MongoEngineSessionInterface(db)

from views import *

if __name__ == '__main__':
    app.run(port=3333, threaded=True)
