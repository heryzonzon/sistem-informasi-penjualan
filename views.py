from functools import wraps
from flask import render_template, request, flash, redirect, url_for, abort, g, jsonify
from flask.ext.classy import FlaskView
from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user
from passlib.hash import sha256_crypt
from models import *
from app import app
import json
import requests

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'LoginView:index'

# ----------------------------------
# HELPER
# ----------------------------------


@login_manager.user_loader
def load_user(id):
    return User.objects.get(int(id))


def admin_credential(user):
    if user != 'user':
        user_account = User.objects.filter(username == user.username).first()

        if user_account is not None:
            return account.is_admin

    return False


def admin_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if not g.credential['is_admin']:
            abort(403)

        return fn(*args, **kwargs)

    return decorated_view


@app.before_request
def before_request():
    user = current_user
    is_anonymous = user.is_anonymous()
    is_login = not is_anonymous

    if is_anonymous:
        user = 'user'

    is_admin = admin_credential(user)

    g.credential = {
        'user': user,
        'is_login': is_login,
        'is_admin': is_admin,
        'is_anonymous': is_anonymous }

# ----------------------------------
# HOME
# ----------------------------------

class HomeView(FlaskView):
    def index(self):
        return render_template('welcome.html', credential=g.credential)

# ----------------------------------
# ACCOUNT
# ----------------------------------

class LoginView(FlaskView):
    def index(self):
        if not g.credential['is_anonymous']:
            return redirect(url_for('.HomeView:index'))

        return render_template('login.html', credential=g.credential)

    def post(self):
        user = request.form['username']
        pwd = request.form['password']

        fetched_user = User.objects.filter(User.username == user).first() or None

        if fetched_user and sha256_crypt.verify(pwd, fetched_user.password):
            login_user(fetched_user)
            return redirect(url_for('.HomeView:index'))
        else:
            flash('Username atau password salah')
            return redirect(url_for('.LoginView:index'))


class LogoutView(FlaskView):
    @login_required
    def index(self):
        logout_user()
        return redirect(url_for('HomeView:index'))

# ----------------------------------
# USER
# ----------------------------------

class UserView(FlaskView):
    def index(self):
        return render_template('user/list.html', credential=g.credential, data=User.objects.all())

# ----------------------------------
# ITEM
# ----------------------------------

class ItemView(FlaskView):
    def index(self):
        return render_template('item/list.html', credential=g.credential, data=Item.objects.all())

    def new(self):
        return render_template('item/new.html', credential=g.credential, data=Item.objects.all())

    def get(self, id):
        return render_template('item/edit.html', credential=g.credential, data=Item.objects.all())

    def post(self):
        data = json.dumps(request.form)
        hostname = 'http://' + request.host
        req = requests.post(hostname + url_for('items'), data=data)

        if req.status_code == 200:
            return redirect(url_for('ItemView:index'))
        else:
            flash('Kode barcode sudah ada', 'error')
            return redirect(url_for('ItemView:new'))

    def put(self, id):
        data = json.dumps(request.form)
        hostname = 'http://' + request.host
        req = requests.post(hostname + url_for('items'), data=data)

        if req.status_code == 200:
            return redirect(url_for('ItemView:index'))
        else:
            flash('Kode barcode sudah ada', 'error')
            return redirect(url_for('ItemView:new'))

# ----------------------------------
# SUPPLIER
# ----------------------------------

class SupplierView(FlaskView):
    def index(self):
        return render_template('supplier/list.html', credential=g.credential, data=Supplier.objects.all())

# ----------------------------------
# CUSTOMER
# ----------------------------------

class CustomerView(FlaskView):
    def index(self):
        return render_template('customer/list.html', credential=g.credential, data=Customer.objects.all())

# ----------------------------------
# PURCHASE INVOICE
# ----------------------------------

class PurchaseInvoiceView(FlaskView):
    def index(self):
        return render_template('purchase_invoice/list.html', credential=g.credential, data=PurchaseInvoice.objects.all())

# ----------------------------------
# SALE INVOICE
# ----------------------------------

class SaleInvoiceView(FlaskView):
    def index(self):
        # TODO change render template name
        return render_template('purchase_invoice/list.html', credential=g.credential, data=SaleInvoice.objects.all())

# ----------------------------------
# REGISTER VIEW
# ----------------------------------

HomeView.register(app, route_base='/')
LoginView.register(app)
LogoutView.register(app)
UserView.register(app)
ItemView.register(app)
SupplierView.register(app)
CustomerView.register(app)
PurchaseInvoiceView.register(app)
SaleInvoiceView.register(app)
