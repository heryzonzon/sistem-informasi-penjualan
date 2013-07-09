from router import *
from partial.user import admin_required

class GenerateInvoice:
    def all(self):
        return PurchaseInvoice.query.outerjoin(
            PurchaseInvoiceDetail,
            Item,
            Supplier
        ).group_by(PurchaseInvoice.id).all()

    def filtered(self, query):
        return PurchaseInvoice.query.outerjoin(
            PurchaseInvoiceDetail,
            Item,
            Supplier
        ).group_by(PurchaseInvoice.id).filter(or_(
            PurchaseInvoice.code.contains(query),
            Supplier.name.contains(query)
        )).all()

    def details(self):
        return db.session.query(
            PurchaseInvoice.id,
            Item.name,
            Item.price_buy,
            PurchaseInvoiceDetail.quantity,
            (Item.price_buy * PurchaseInvoiceDetail.quantity).label('total_price')
        ).outerjoin(PurchaseInvoiceDetail, Item).group_by(PurchaseInvoice.id, Item.id).all()

    def conclusion(self):
        return db.session.query(
            PurchaseInvoice.id,
            db.func.sum(PurchaseInvoiceDetail.quantity).label('total_quantity'),
            db.func.sum(Item.price_buy * PurchaseInvoiceDetail.quantity).label('total_price')
        ).join(PurchaseInvoiceDetail, Item).group_by(PurchaseInvoice.id).all()


@app.route('/invoices/purchase')
def purchase_invoices():
    invoice = GenerateInvoice()
    invoice_purchases = invoice.all()
    invoice_purchase_details = invoice.details()
    invoice_purchase_conclusion = invoice.conclusion()

    return render_template('purchase_invoice/list.html', data=invoice_purchases,
                                                         data_detail=invoice_purchase_details,
                                                         data_conclusion=invoice_purchase_conclusion,
                                                         credential=g.credential)


@app.route('/invoices/purchase/search')
@login_required
def search_purchase_invoice():
    query = request.values.get('query', None)

    if query is not None:
        invoice = GenerateInvoice()
        invoice_purchases = invoice.filtered(query)
        invoice_purchase_details = invoice.details()
        invoice_purchase_conclusion = invoice.conclusion()

        return render_template('purchase_invoice/list.html', data=invoice_purchases,
                                                             data_detail=invoice_purchase_details,
                                                             data_conclusion=invoice_purchase_conclusion,
                                                             credential=g.credential)
    else:
        abort(404)


@app.route('/invoices/purchase/<int:id>/delete')
@login_required
def delete_purchase_invoice(id):
    data = Item.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    flash('Data barang telah terhapus')
    return redirect(url_for('purchase_invoices'))


@app.route('/invoices/purchase/<int:id>')
def edit_purchase_invoice(id):
    pass


@app.route('/invoices/sales/<int:id>')
def edit_sales_invoice(id):
    pass


@app.route('/invoices/sales')
def sales_invoices():
    pass

