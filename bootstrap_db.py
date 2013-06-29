#from app import auth
#auth.User.create(username='admin', password='admin', email='info@admin.com', admin=True, active=True)
#!/usr/bin/env python2

import os
from flask_peewee.utils import make_password
from models import *

try:
    os.remove('db.sqlite')
except:
    pass

seed_table()

User.create(username='ryan', password=make_password('1234'), is_admin=True)
User.create(username='tes', password=make_password('aja'), is_admin=False)

s1 = Supplier.create(name='pt asri', address='dak tau')
s2 = Supplier.create(name='pt irsa', contact='13123')

Customer.create(name='pelanggan pertama', contact='123342')
Customer.create(name='pelanggan kedua')

i1 = Item.create(barcode='I123', name='emping', stock=5, supplier=s1)
i2 = Item.create(barcode='I124', name='nasi gemuk', stock=8, supplier=s2)

bi1 = PurchaseInvoice.create(code='FB123')
PurchaseInvoiceDetail.create(purchase_invoice=bi1, item=i1)
PurchaseInvoiceDetail.create(purchase_invoice=bi1, item=i2)

si1 = SalesInvoice.create(code='FJ423')
SalesInvoiceDetail.create(sales_invoice=si1, item=i1)
SalesInvoiceDetail.create(sales_invoice=si1, item=i2)
