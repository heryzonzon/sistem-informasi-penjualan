from partial.router import *

@app.route('/customers')
@login_required
def customers():
    return render_template('customer/list.html', attr='customer',
                                        data=Customer.select(),
                                        title='pelanggan')


@app.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    data = Customer()

    if request.method == 'GET':
        form = CustomerForm(obj=data)
        return render_template('customer/edit.html', prev_link='customers',
                                            form=form,
                                            data=None)

    else: # POST
        form = CustomerForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.save()
            flash('Data pelanggan telah ditambah')
            return redirect(url_for('customers'))
        else:
            abort(403)


@app.route('/customers/<id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    try:
        data = Customer.get(id=id)
    except:
        abort(404)

    if request.method == 'POST':
        form = CustomerForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.save()
            flash('Data pelanggan telah tersimpan')
            return redirect(url_for('customers'))
        else:
            abort(403)

    elif request.method == 'GET':
        form = CustomerForm(obj=data)

    return render_template('customer/edit.html', prev_link='customers',
                                        form=form,
                                        data=data)


@app.route('/customers/<id>/delete')
@login_required
def delete_customer(id):
    try:
        data = Customer.get(id=id)
        data.delete_instance()
        flash('Data pelanggan telah terhapus')
        return redirect(url_for('customers'))
    except:
        abort(404)