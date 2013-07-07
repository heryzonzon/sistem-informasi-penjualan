from router import *
from models import db
from sqlalchemy.exc import IntegrityError

@app.route('/items')
@login_required
def items():
    return render_template('item/list.html', data=Item.query.all(),
                                             credential=g.credential)


@app.route('/items/search')
@login_required
def search_item():
    query = request.values.get('query', None)

    if query is not None:
        data = Item.query.filter(Item.name.contains(query))
        return render_template('item/list.html', data=data,
                                                 credential=g.credential)
    else:
        return redirect(url_for('items'))


@app.route('/items/add', methods=['GET', 'POST'])
@login_required
def add_item():
    data = Item()
    form = ItemForm(request.form, obj=data)

    if form.validate_on_submit():
        form.populate_obj(data)
        db.session.add(data)
        db.session.commit()
        flash('Data barang telah ditambah')
        return form.redirect(url_for('items'))

    return render_template('item/edit.html', form=form,
                                             credential=g.credential)


@app.route('/items/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    data = Item.query.get_or_404(id)

    if request.method == 'GET':
        form = ItemForm(obj=data)

    elif request.method == 'POST':
        form = ItemForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            db.session.merge(data)
            db.session.commit()
            flash('Data barang telah tersimpan')
            return redirect(url_for('items'))

    return render_template('item/edit.html', form=form,
                                             data=data,
                                             credential=g.credential)


@app.route('/items/<int:id>/delete')
@login_required
def delete_item(id):
    data = Item.query.get_or_404(id)

    try:
        db.session.delete(data)
        db.session.commit()
        flash('Data barang telah terhapus')
    except IntegrityError:
        db.session.rollback()
        # TODO change to edit_purchase_invoice
        purchase_invoices = [{
            'id': url_for('edit_item', id=invoice.id),
            'code': invoice.code }
                for invoice in PurchaseInvoice.query.filter(Item.id == id).all()]

        sales_invoices = [{
            'id': url_for('edit_item', id=invoice.id),
            'code': invoice.code }
                for invoice in SalesInvoice.query.filter(Item.id == id).all()]

        invoices = purchase_invoices + sales_invoices

        pending_item = Item.query.get(id)

        # TODO option to delete all dependent invoice
        return render_template('item/list.html', data=Item.query.all(),
                                                 pending_invoices=invoices,
                                                 pending_item=pending_item.name,
                                                 credential=g.credential)

    return redirect(url_for('items'))
