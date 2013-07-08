from router import *
from models import db
from sqlalchemy.exc import IntegrityError


def invoice_detail_link(invoice, invoice_type):
    return url_for('edit_%s_invoice' % invoice_type, id=invoice.id)


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
    form = ItemForm(obj=data)

    if form.validate_on_submit():
        form.populate_obj(data)
        db.session.add(data)
        db.session.commit()
        flash('Data barang telah ditambah')
        return redirect(url_for('items'))

    return render_template('item/edit.html', form=form,
                                             credential=g.credential)


@app.route('/items/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    data = Item.query.get_or_404(id)
    form = ItemForm(obj=data)

    if form.validate_on_submit():
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

        purchase_invoices = [( invoice_detail_link(invoice, 'purchase'), invoice.code )
                for invoice in PurchaseInvoice.query
                        .join(PurchaseInvoiceDetail, Item)
                        .filter(Item.id == id)
                        .all()]

        sales_invoices = [( invoice_detail_link(invoice, 'sales'), invoice.code )
                for invoice in SalesInvoice.query
                        .join(SalesInvoiceDetail, Item)
                        .filter(Item.id == id)
                        .all()]

        invoices = purchase_invoices + sales_invoices
        pending_item = Item.query.get(id)

        # TODO option to delete all dependent invoice
        return render_template('item/list.html', data=Item.query.all(),
                                                 pending_invoices=invoices,
                                                 pending_item=pending_item.name,
                                                 credential=g.credential)

    return redirect(url_for('items'))
