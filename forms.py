from flask.ext.wtf import PasswordField, TextField, Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import validators
from models import *

item_form_validators = {
    'stock': { 'validators': [validators.number_range(min=0)] },
    'price_buy': { 'validators': [validators.number_range(min=0)] },
    'price_sell': { 'validators': [validators.number_range(min=0)] }
}

purchase_invoice_detail_validators = {
    'quantity': { 'validators': [validators.number_range(min=0)] }
}

sales_invoice_validators = {
    'discount': { 'validators': [validators.number_range(min=0, max=100)] }
}

UserForm = model_form(User,
                db_session=db.session,
                base_class=Form)

SupplierForm = model_form(Supplier, db_session=db.session,
                                    base_class=Form,
                                    exclude=['items'])

CustomerForm = model_form(Customer, db_session=db.session,
                                    base_class=Form)

ItemForm = model_form(Item, db_session=db.session,
                            base_class=Form, exclude=['purchase_invoices'],
                            field_args=item_form_validators)

PurchaseInvoiceForm = model_form(PurchaseInvoice, db_session=db.session,
                                                  base_class=Form)

PurchaseInvoiceDetailForm = model_form(PurchaseInvoiceDetail, db_session=db.session,
                                                              base_class=Form,
                                                              field_args=purchase_invoice_detail_validators)

SalesInvoiceForm = model_form(SalesInvoice, db_session=db.session,
                                            base_class=Form,
                                            field_args=sales_invoice_validators)

SalesInvoiceDetailForm = model_form(SalesInvoiceDetail, db.session, Form)

class LoginForm(Form):
    username = TextField()
    password = PasswordField()
