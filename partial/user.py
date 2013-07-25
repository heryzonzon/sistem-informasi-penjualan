from router import *


@app.route('/users')
@login_required
@admin_required
def users():
    return render_template('user/list.html', data=User.query.all(),
                                             credential=g.credential)


@app.route('/users/search')
@login_required
@admin_required
def search_users():
    query = request.values.get('query', None)

    if query is not None:
        data = User.query.filter(User.username.contains(query)).all()
        return render_template('user/list.html', data=data,
                                                 credential=g.credential)
    else:
        abort(404)


@app.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    data = User()

    if request.method == 'GET':
        form = UserForm(obj=data)
        return render_template('user/add.html', form=form,
                                                data=None,
                                                credential=g.credential)

    else: # POST
        form = UserForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.password = sha256_crypt.encrypt(data.password)
            db.session.add(data)
            db.session.commit()
            flash('Data pengguna telah ditambah')
            return redirect(url_for('users'))
        else:
            flash('Nama pengguna sudah ada')
            return redirect(url_for('add_user'))


@app.route('/users/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    data = User.query.get_or_404(id)

    if request.method == 'POST':
        form = UserForm(request.form, obj=data)

        # return error if old password is not match with database
        if not sha256_crypt.verify(request.form['old_password'], data.password):
            flash('Password salah', 'password')
            return redirect(url_for('edit_user', id=id))

        data.username = request.form['username']
        data.password = sha256_crypt.encrypt(request.form['new_password'])

        # set admin status to True if checked
        if 'is_admin' in request.form:
            data.is_admin = True if request.form['is_admin'] == 'y' else False
        else:
            # return error if change admin status for account that is in used
            if request.form['username'] == g.credential['user'].username:
                flash('Status admin tidak bisa diganti karena account ini sedang digunakan', 'admin')
                return redirect(url_for('edit_user', id=id))

            # set admin status to False if unchecked
            data.is_admin = False

        db.session.merge(data)
        db.session.commit()
        flash('Data pengguna telah tersimpan')
        return redirect(url_for('users'))

    elif request.method == 'GET':
        form = UserForm(obj=data)

    return render_template('user/edit.html', form=form,
                                             data=data,
                                             credential=g.credential)


@app.route('/users/<int:id>/delete')
@login_required
@admin_required
def delete_user(id):
    data = User.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    flash('Data pengguna telah terhapus')
    return redirect(url_for('users'))
