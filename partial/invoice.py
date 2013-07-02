import json
from flask import jsonify
from peewee import fn, JOIN_LEFT_OUTER
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



@app.route('/invoices/purchase')
def purchase_invoices():
    data = PurchaseInvoice.select(
        Supplier.name,
        fn.Count(PurchaseInvoiceDetail.id).alias('item_count'),
        fn.Count(Item.id).alias('total_item_count'),
        fn.Sum(Item.price_buy).alias('price'),
        # PurchaseInvoice must on bottom to make sure 'id' fetched from this
        PurchaseInvoice)\
    .join(PurchaseInvoiceDetail, JOIN_LEFT_OUTER)\
    .join(Item, JOIN_LEFT_OUTER)\
    .join(Supplier, JOIN_LEFT_OUTER)\
    .group_by(PurchaseInvoice.code)\
    .naive()

    data_detail = {invoice.id: PurchaseInvoiceDetail.select(PurchaseInvoiceDetail, Item)\
        .join(Item, JOIN_LEFT_OUTER)\
        .where(PurchaseInvoiceDetail.purchase_invoice == invoice.id).naive()
          for invoice in data}

    total_quantity = {invoice.id: PurchaseInvoiceDetail.select(
            fn.Sum(PurchaseInvoiceDetail.quantity).alias('value'))\
        .where(PurchaseInvoiceDetail.purchase_invoice == invoice.id)
          for invoice in data}

    total_price = {invoice.id: PurchaseInvoiceDetail.select(
            fn.Sum(Item.price_buy * PurchaseInvoiceDetail.quantity).alias('value'))\
        .join(Item, JOIN_LEFT_OUTER)\
        .where(PurchaseInvoiceDetail.purchase_invoice == invoice.id).naive()
          for invoice in data}

    return render_template('purchase_invoice/list.html', attr='purchase_invoice',
                                                         data=data,
                                                         data_detail=data_detail,
                                                         total_quantity=total_quantity,
                                                         total_price=total_price,
                                                         title='faktur pembelian',
                                                         credential=g.credential)


@app.route('/invoices/sales')
def sales_invoices():
    pass

