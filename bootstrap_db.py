from passlib.hash import sha256_crypt
from models import *

def initdb():
    db.drop_all()
    db.create_all()

    user1 = User(username='ryan', password=sha256_crypt.encrypt('1234'), is_admin=True)
    user2 = User(username='tes', password=sha256_crypt.encrypt('aja'), is_admin=False)

    supplier1 = Supplier(name='pt asri', address='dak tau')
    supplier2 = Supplier(name='pt irsa', contact='13123')

    customer1 = Customer(name='pelanggan pertama', contact='123342')
    customer2 = Customer(name='pelanggan kedua')

    item1 = Item(barcode='I123', name='emping', price_buy=10000, price_sell=15000, stock=5, supplier=supplier1)
    item2 = Item(barcode='I124', name='nasi gemuk', price_buy=15000, price_sell=25000, stock=8, supplier=supplier2)
    item3 = Item(barcode='5124', name='nasi kucing', price_buy=1500, price_sell=22000, stock=2, supplier=supplier2)

    pid1 = PurchaseInvoiceDetail(item=item1, quantity=2)
    pid2 = PurchaseInvoiceDetail(item=item2, quantity=3)
    pid3 = PurchaseInvoiceDetail(item=item3, quantity=3)
    pid4 = PurchaseInvoiceDetail(item=item1, quantity=4)
    pid5 = PurchaseInvoiceDetail(item=item3, quantity=3)

    pi1 = PurchaseInvoice(code='FB123', items=[pid1, pid3])
    pi2 = PurchaseInvoice(code='FB124', items=[pid2, pid4, pid5])

    sid1 = SalesInvoiceDetail(item=item1, quantity=3)
    sid2 = SalesInvoiceDetail(item=item2, quantity=5)
    sid3 = SalesInvoiceDetail(item=item1, quantity=4)
    sid4 = SalesInvoiceDetail(item=item2, quantity=2)

    si1 = SalesInvoice(code='FJ423', items=[sid1, sid2])
    si2 = SalesInvoice(code='FJ425', items=[sid3, sid4])

    db.session.add_all([
        user1, user2, supplier1, supplier2, item1, item2, item3,
        pid1, pid2, pid3, pid4, pid5, sid1, sid2, sid3, sid4,
        pi1, pi2, si1, si2
    ])

    db.session.commit()
