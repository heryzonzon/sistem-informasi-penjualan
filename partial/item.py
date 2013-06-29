from router import *

@app.route('/items')
@login_required
def items():
    return render_template('item/list.html', attr='item',
                                             data=Item.select(),
                                             title='barang')


@app.route('/items/search')
@login_required
def search_items():
    query = request.values.get('query', None)

    if query is not None:
        wildcard_query = '%' + query + '%'
        data = Item.select().where(Item.name ** wildcard_query)
        return render_template('item/list.html', attr='item',
                                                 data=data,
                                                 title='barang')
    else:
        abort(404)


@app.route('/items/add', methods=['GET', 'POST'])
@login_required
def add_item():
    data = Item()

    if request.method == 'GET':
        form = ItemForm(obj=data)
        return render_template('item/edit.html', prev_link='items',
                                                 form=form,
                                                 data=None)

    else: # POST
        form = ItemForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.save()
            flash('Data barang telah ditambah')
            return redirect(url_for('items'))
        else:
            abort(403)


@app.route('/items/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    try:
        data = Item.get(id=id)
    except:
        abort(404)

    if request.method == 'POST':
        form = ItemForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.save()
            flash('Data barang telah tersimpan')
            return redirect(url_for('items'))
        else:
            abort(403)

    elif request.method == 'GET':
        form = ItemForm(obj=data)

    return render_template('item/edit.html', prev_link='items',
                                        form=form,
                                        data=data)


@app.route('/items/<int:id>/delete')
@login_required
def delete_item(id):
    try:
        data = Item.get(id=id)
        data.delete_instance()
        flash('Data barang telah terhapus')
        return redirect(url_for('items'))
    except:
        abort(404)