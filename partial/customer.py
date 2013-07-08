from router import *
from models import db
from sqlalchemy.exc import IntegrityError

@app.route('/customers')
@login_required
def customers():
    return render_template('customer/list.html', data=Customer.query.all(),
                                                 credential=g.credential)


@app.route('/customers/search')
@login_required
def search_customer():
    query = request.values.get('query', None)

    if query is not None:
        data = Customer.query.filter(or_(
            Customer.name.contains(query),
            Customer.address.contains(query),
            Customer.contact.contains(query)))
        return render_template('customer/list.html', data=data,
                                                     credential=g.credential)
    else:
        return redirect(url_for('customers'))


@app.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    data = Customer()
    form = CustomerForm(obj=data)

    if form.validate_on_submit():
        form.populate_obj(data)
        db.session.add(data)
        db.session.commit()
        flash('Data pelanggan telah ditambah')
        return redirect(url_for('customers'))

    return render_template('customer/edit.html', form=form,
                                                 credential=g.credential)


@app.route('/customers/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    data = Customer.query.get_or_404(id)
    form = CustomerForm(obj=data)

    if form.validate_on_submit():
        form.populate_obj(data)
        db.session.merge(data)
        db.session.commit()
        flash('Data pelanggan telah tersimpan')
        return redirect(url_for('customers'))

    return render_template('customer/edit.html', form=form,
                                                 data=data,
                                                 credential=g.credential)


@app.route('/customers/<int:id>/delete')
@login_required
def delete_customer(id):
    data = Customer.query.get_or_404(id)

    try:
        db.session.delete(data)
        db.session.commit()
        flash('Data pelanggan telah terhapus')
    except IntegrityError:
        db.session.rollback()

        purchase_invoices = [( invoice_detail_link(invoice, 'purchase'), invoice.code )
                for invoice in PurchaseInvoice.query
                        .join(PurchaseInvoiceDetail, Customer)
                        .filter(Customer.id == id)
                        .all()]

        sales_invoices = [( invoice_detail_link(invoice, 'sales'), invoice.code )
                for invoice in SalesInvoice.query
                        .join(SalesInvoiceDetail, Customer)
                        .filter(Customer.id == id)
                        .all()]

        invoices = purchase_invoices + sales_invoices
        pending_customer = Customer.query.get(id)

        return render_template('customer/list.html', data=Customer.query.all(),
                                                     pending_invoices=invoices,
                                                     pending_customer=pending_customer,
                                                     credential=g.credential)

    return redirect(url_for('customers'))
    pass
