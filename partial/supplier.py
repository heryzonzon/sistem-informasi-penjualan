from router import *
from models import db

class GenerateSupplier:
    def all(self):
        return db.session.query(
            Supplier,
            db.func.count(Item.id).label('item_count')
        ).outerjoin(Item).group_by(Supplier.id).all()

    def filtered(self, query):
        return db.session.query(
            Supplier,
            db.func.count(Item.id).label('item_count')
        ).outerjoin(Item).group_by(Supplier.id).filter(or_(
            Supplier.name.contains(query),
            Supplier.address.contains(query),
            Supplier.contact.contains(query))).all()


@app.route('/suppliers')
@login_required
def suppliers():
    data = GenerateSupplier().all()
    data_detail = Item.query.all()

    return render_template('supplier/list.html', data=data,
                                                 data_detail=data_detail,
                                                 credential=g.credential)


@app.route('/suppliers/search')
@login_required
def search_supplier():
    query = request.values.get('query', None)

    if query is not None:
        data = GenerateSupplier().filtered(query)
        return render_template('supplier/list.html', data=data,
                                                     credential=g.credential)
    else:
        return redirect(url_for('suppliers'))


@app.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    data = Supplier()
    form = SupplierForm(obj=data)

    if form.validate_on_submit():
        form.populate_obj(data)
        db.session.add(data)
        db.session.commit()
        flash('Data pemasok telah ditambah')
        return redirect(url_for('suppliers'))

    return render_template('supplier/edit.html', form=form,
                                                 credential=g.credential)


@app.route('/suppliers/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    data = Supplier.query.get_or_404(id)
    form = SupplierForm(obj=data)

    if form.validate_on_submit():
        form.populate_obj(data)
        db.session.merge(data)
        db.session.commit()
        flash('Data pemasok telah tersimpan')
        return redirect(url_for('suppliers'))

    return render_template('supplier/edit.html', form=form,
                                                 data=data,
                                                 credential=g.credential)


@app.route('/suppliers/<int:id>/delete')
@login_required
def delete_supplier(id):
    data = Supplier.query.get_or_404(id)

    db.session.delete(data)
    db.session.commit()
    flash('Data pemasok telah terhapus')

    return redirect(url_for('suppliers'))
