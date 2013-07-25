import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

from app import *
from flask import request, abort, flash, redirect, url_for, render_template, g
from flask.ext.login import login_required
from models import User
#from forms import *


@app.route('/')
def index():
    return render_template('welcome.html', credential=g.credential)

#from partial import item
