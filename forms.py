from flask.ext.wtf import PasswordField, TextField, Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import validators
from models import *

UserForm = model_form(User, db.session, Form)
SupplierForm = model_form(Supplier, db.session, Form)
CustomerForm = model_form(Customer, db.session, Form)
ItemForm = model_form(Item, db.session, Form, field_args={
    'stock': { 'validators': [validators.number_range(min=0)] },
    'price_buy': { 'validators': [validators.number_range(min=0)] },
    'price_sell': { 'validators': [validators.number_range(min=0)] }
})
PurchaseInvoiceForm = model_form(PurchaseInvoice, db.session, Form)
PurchaseInvoiceDetailForm = model_form(PurchaseInvoiceDetail, db.session, Form, field_args={
    'quantity': { 'validators': [validators.number_range(min=0)] }
})
SalesInvoiceForm = model_form(SalesInvoice, db.session, Form, field_args={
    'discount': { 'validators': [validators.number_range(min=0, max=100)] }
})
SalesInvoiceDetailForm = model_form(SalesInvoiceDetail, db.session, Form)

class LoginForm(Form):
    username = TextField()
    password = PasswordField()
