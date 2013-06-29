from partial.router import *

@app.route('/users')
@login_required
def users():
    return render_template('user/list.html', attr='user',
                                             data=User.select(),
                                             title='pengguna',
                                             credential=g.credential)


@app.route('/users/search')
@login_required
def search_users():
    query = request.values.get('query', None)

    if query is not None:
        wildcard_query = '%' + query + '%'
        data = User.select().where(User.username ** wildcard_query)
        return render_template('user/list.html', attr='user',
                                                 data=data,
                                                 title='pengguna',
                                                 credential=g.credential)
    else:
        abort(404)


@app.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    data = User()

    if request.method == 'GET':
        form = UserForm(obj=data)
        return render_template('user/edit.html', prev_link='users',
                                                 form=form,
                                                 data=None,
                                                 credential=g.credential)

    else: # POST
        form = UserForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.save()
            flash('Data pengguna telah ditambah')
            return redirect(url_for('users'))
        else:
            abort(403)


@app.route('/users/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    try:
        data = User.get(id=id)
    except:
        abort(404)

    if request.method == 'POST':
        form = UserForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.save()
            flash('Data pengguna telah tersimpan')
            return redirect(url_for('users'))
        else:
            abort(403)

    elif request.method == 'GET':
        form = UserForm(obj=data)

    return render_template('user/edit.html', prev_link='users',
                                             form=form,
                                             data=data,
                                             credential=g.credential)


@app.route('/users/<int:id>/delete')
@login_required
def delete_user(id):
    try:
        data = User.get(id=id)
        data.delete_instance()
        flash('Data pengguna telah terhapus')
        return redirect(url_for('users'))
    except:
        abort(404)