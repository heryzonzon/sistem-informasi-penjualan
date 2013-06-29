import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

from app import *
from flask import request, abort, flash, redirect, url_for, render_template, g
from flask.ext.login import login_required
from models import *
from forms import *


class InitUser():
    def __init__(self):
        user = g.user
        is_login = False

        if user.is_anonymous():
            user = 'user'
        else:
            is_login = True

        return {'user': user, 'is_login': is_login}
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

from app import *
from flask import request, abort, flash, redirect, url_for, render_template, g
from flask.ext.login import login_required
from models import *
from forms import *

@app.route('/')
def index():
    user = g.user
    is_login = False

    if user.is_anonymous():
        user = 'user'
    else:
        is_login = True

    return render_template('welcome.html', user=user, is_login=is_login, is_admin=login.is_admin(user))

from partial import item, customer, supplier, invoice, transaction, login, user
