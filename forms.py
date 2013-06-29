from wtforms import PasswordField, TextField, Form
from wtfpeewee.orm import model_form

from models import *


UserForm = model_form(User)
SupplierForm = model_form(Supplier)
CustomerForm = model_form(Customer)
ItemForm = model_form(Item)
PurchaseInvoiceForm = model_form(PurchaseInvoice)
PurchaseInvoiceDetailForm = model_form(PurchaseInvoiceDetail)
SalesInvoiceForm = model_form(SalesInvoice)
SalesInvoiceDetailForm = model_form(SalesInvoiceDetail)

class LoginForm(Form):
    username = TextField()
    password = PasswordField()