from router import *
from partial.user import admin_required

invoice_purchase = PurchaseInvoice.query.join(
    PurchaseInvoiceDetail,
    Item,
    Supplier
).group_by(PurchaseInvoice.id)

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


@app.route('/invoices/purchase/search')
@login_required
def search_purchase_invoice():
    query = request.values.get('query', None)

    if query is not None:
        invoice_purchases = invoice_purchase.filter(or_(
            PurchaseInvoice.code.contains(query),
            Supplier.name.contains(query)
        )).all()

        return render_template('purchase_invoice/list.html', data=invoice_purchases,
                                                             data_detail=invoice_purchase_details,
                                                             data_conclusion=invoice_purchase_conclusion,
                                                             credential=g.credential)
    else:
        abort(404)



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
    invoice_purchases = invoice_purchase.all()

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

