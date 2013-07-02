from wtforms import PasswordField, TextField, Form, validators
from wtfpeewee.orm import model_form
from models import *


UserForm = model_form(User)
SupplierForm = model_form(Supplier)
CustomerForm = model_form(Customer)
ItemForm = model_form(Item, field_args={
    'stock': {
        'validators': [validators.number_range(min=0)]
    },
    'price_buy': {
        'validators': [validators.number_range(min=0)]
    },
    'price_sell': {
        'validators': [validators.number_range(min=0)]
    }
})
PurchaseInvoiceForm = model_form(PurchaseInvoice)
PurchaseInvoiceDetailForm = model_form(PurchaseInvoiceDetail, field_args={
    'quantity': {
        'validators': [validators.number_range(min=0)]
    }
})
SalesInvoiceForm = model_form(SalesInvoice, field_args={
    'discount': {
        'validators': [validators.number_range(min=0, max=100)]
    }
})
SalesInvoiceDetailForm = model_form(SalesInvoiceDetail)

class LoginForm(Form):
    username = TextField()
    password = PasswordField()
