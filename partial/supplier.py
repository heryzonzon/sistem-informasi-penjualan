from router import *

@app.route('/suppliers')
@login_required
def suppliers():
    return render_template('supplier/list.html', attr='supplier',
                                                 data=Supplier.select(),
                                                 title='pemasok')


@app.route('/suppliers/search')
@login_required
def search_supplier():
    query = request.values.get('query', None)

    if query is not None:
        wildcard_query = '%' + query + '%'
        data = Supplier.select().where(Supplier.name ** wildcard_query)
        return render_template('supplier/list.html', attr='supplier',
                                                     data=data,
                                                     title='pemasok')
    else:
        abort(404)


@app.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    data = Supplier()

    if request.method == 'GET':
        form = SupplierForm(obj=data)
        return render_template('supplier/edit.html', prev_link='suppliers',
                                                     form=form,
                                                     data=None)

    else: # POST
        form = SupplierForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.save()
            flash('Data pemasok telah ditambah')
            return redirect(url_for('suppliers'))
        else:
            abort(403)


@app.route('/suppliers/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    try:
        data = Supplier.get(id=id)
    except:
        abort(404)

    if request.method == 'POST':
        form = SupplierForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.save()
            flash('Data pemasok telah tersimpan')
            return redirect(url_for('suppliers'))

    elif request.method == 'GET':
        form = SupplierForm(obj=data)

    return render_template('supplier/edit.html', prev_link='suppliers',
                                                 form=form,
                                                 data=data)


@app.route('/suppliers/<int:id>/delete')
@login_required
def delete_supplier(id):
    try:
        data = Supplier.get(id=id)
        data.delete_instance()
        flash('Data pemasok telah terhapus')
        return redirect(url_for('suppliers'))
    except:
        abort(404)
