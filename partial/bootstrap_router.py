

def bootstrap_router(attr_list):
    for attr in attr_list:
        template = '''
from router import *

@app.route('/%(route)ss')
def %(route)ss():
    return render_template('%(route)s/list.html', attr='%(route)s',
                                        data=%(cls)s.select(),
                                        title='%(title)s')


@app.route('/%(route)ss/add', methods=['GET', 'POST'])
def add_%(route)s():
    data = %(cls)s()

    if request.method == 'GET':
        form = %(cls)sForm(obj=data)
        return render_template('%(route)s/edit.html', prev_link='%(route)ss',
                                            form=form,
                                            data=None)

    else: # POST
        form = %(cls)sForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.save()
            flash('Data %(title)s telah ditambah')
            return redirect(url_for('%(route)ss'))
        else:
            abort(403)


@app.route('/%(route)ss/<id>', methods=['GET', 'POST'])
def edit_%(route)s(id):
    try:
        data = %(cls)s.get(id=id)
    except:
        abort(404)

    if request.method == 'POST':
        form = %(cls)sForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.save()
            flash('Data %(title)s telah tersimpan')
            return redirect(url_for('%(route)ss'))
        else:
            abort(403)

    elif request.method == 'GET':
        form = %(cls)sForm(obj=data)

    return render_template('%(route)s/edit.html', prev_link='%(route)ss',
                                        form=form,
                                        data=data)


@app.route('/%(route)ss/<id>/delete')
def delete_%(route)s(id):
    try:
        data = %(cls)s.get(id=id)
        data.delete_instance()
        flash('Data %(title)s telah terhapus')
        return redirect(url_for('%(route)ss'))
    except:
        abort(404)
        ''' % attr

        open(attr['route'] + 'user.py', 'w').write(template.strip())


col = [
    {'route': 'item',
     'cls': 'Item',
     'title': 'barang'},

    {'route': 'supplier',
     'cls': 'Supplier',
     'title': 'pemasok'},

    {'route': 'customer',
     'cls': 'Customer',
     'title': 'pelanggan'},
]

bootstrap_router(col)
