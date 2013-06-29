from flask.ext.login import current_user, login_user, logout_user
from flask.ext.peewee.utils import check_password

from router import *

@lm.user_loader
def load_user(id):
    id = int(id)
    return User.get(id=id)


def admin_credential(user):
    try:
        user = User.get(username=user)
    except User.DoesNotExist:
        user = None

    if user is None or user.is_admin == False:
        return False

    return True


@app.before_request
def before_request():
    user = current_user
    is_anonymous = user.is_anonymous()
    is_login = False

    if is_anonymous:
        user = 'user'
    else:
        is_login = True

    is_admin = admin_credential(user)

    g.credential = {
        'user': user,
        'is_login': is_login,
        'is_admin': is_admin,
        'is_anonymous': is_anonymous
    }


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not g.credential['is_anonymous']:
        return redirect(url_for('index'))

    form = LoginForm()

    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        try:
            fetched_user = User.get(username=user)
        except User.DoesNotExist:
            fetched_user = None

        if fetched_user and check_password(pwd, fetched_user.password):
            login_user(fetched_user)
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah')

    return render_template('login.html', form=form,
                                         credential=g.credential)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
