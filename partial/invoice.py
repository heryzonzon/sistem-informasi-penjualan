from router import *
from partial.user import admin_required


@app.route('/invoices/purchase/search')
@login_required
def search_purchase_invoice():
    '''
    query = request.values.get('query', None)

    if query is not None:
        wildcard_query = '%' + query + '%'
        data = PurchaseInvoice.select().where(PurchaseInvoice.name ** wildcard_query)
        return render_template('item/list.html', attr='item',
                               data=data,
                               title='barang',
                               credential=g.credential)
    else:
        abort(404)
    '''
    pass


@app.route('/invoices/purchase/add', methods=['GET', 'POST'])
@login_required
def add_purchase_invoice():
    '''
    data = PurchaseInvoice()

    if request.method == 'GET':
        form = ItemForm(obj=data)
        return render_template('item/edit.html', prev_link='items',
                               form=form,
                               data=None,
                               credential=g.credential)

    else: # POST
        form = ItemForm(request.form, obj=data)

        if form.validate():
            form.populate_obj(data)
            data.save()
            flash('Data barang telah ditambah')
            return redirect(url_for('items'))
        else:
            abort(403)
    '''
    pass


@app.route('/items/<int:id>/delete')
@login_required
def delete_purchase_invoice(id):
    '''
    try:
        data = Item.get(id=id)
        data.delete_instance()
        flash('Data barang telah terhapus')
        return redirect(url_for('items'))
    except:
        abort(404)
    '''
    pass


@app.route('/invoices/purchase/<int:id>')
def edit_purchase_invoice(id):
    pass


@app.route('/invoices/purchase')
def purchase_invoices():
    invoice_purchases = PurchaseInvoice.query.join(
        PurchaseInvoiceDetail,
        Item,
        Supplier
    ).group_by(PurchaseInvoice.id).all()

    invoice_purchase_details = db.session.query(
        PurchaseInvoice.id,
        Item.name,
        Item.price_buy,
        PurchaseInvoiceDetail.quantity,
        (Item.price_buy * PurchaseInvoiceDetail.quantity).label('total_price')
    ).join(PurchaseInvoiceDetail, Item).group_by(PurchaseInvoice.id, Item.id).all()

    invoice_purchase_conclusion = db.session.query(
        PurchaseInvoice.id,
        db.func.sum(PurchaseInvoiceDetail.quantity).label('total_quantity'),
        db.func.sum(Item.price_buy * PurchaseInvoiceDetail.quantity).label('total_price')
    ).join(PurchaseInvoiceDetail, Item).group_by(PurchaseInvoice.id).all()

    return render_template('purchase_invoice/list.html', data=invoice_purchases,
                                                         data_detail=invoice_purchase_details,
                                                         data_conclusion=invoice_purchase_conclusion,
                                                         credential=g.credential)

@app.route('/invoices/sales/<int:id>')
def edit_sales_invoice(id):
    pass


@app.route('/invoices/sales')
def sales_invoices():
    pass

