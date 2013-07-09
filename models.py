from datetime import datetime
from app import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean)

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __unicode__(self):
        return self.username


class Supplier(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    address = db.Column(db.String(50))
    contact = db.Column(db.String(20))
    items = db.relationship('Item', backref='supplier')

    def __unicode__(self):
        return self.name


class Customer(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(50))
    contact = db.Column(db.String(20))
    sales_invoices = db.relationship('SalesInvoice', backref='customer')

    def __unicode__(self):
        return self.name


class Item(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    barcode = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    stock = db.Column(db.SmallInteger, default=0)
    price_buy = db.Column(db.Integer, default=0)
    price_sell = db.Column(db.Integer, default=0)
    supplier_id = db.Column(db.SmallInteger, db.ForeignKey('supplier.id'))
    #purchase_invoices = db.relationship('PurchaseInvoiceDetail', backref='item')

    def __unicode__(self):
        return '%s (Stok: %s)' % (self.name, self.stock)


class PurchaseInvoice(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    items = db.relationship('PurchaseInvoiceDetail', backref='purchase_invoices', cascade='all')

    def __unicode__(self):
        return unicode(self.created_at)


class PurchaseInvoiceDetail(db.Model):
    item_id = db.Column(db.SmallInteger, db.ForeignKey('item.id'), primary_key=True)
    purchase_invoice_id = db.Column(db.SmallInteger, db.ForeignKey('purchase_invoice.id'), primary_key=True)
    quantity = db.Column(db.SmallInteger, default=0)
    item = db.relationship('Item')

    def __unicode__(self):
        return unicode(PurchaseInvoice.query.get(
                        self.purchase_invoice_id).created_at)


class SalesInvoice(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    discount = db.Column(db.Float, default=0)
    customer_id = db.Column(db.SmallInteger, db.ForeignKey('customer.id'))
    items = db.relationship('SalesInvoiceDetail', backref='sales_invoices', cascade='all')

    def __unicode__(self):
        return unicode(self.created_at)


class SalesInvoiceDetail(db.Model):
    item_id = db.Column(db.SmallInteger, db.ForeignKey('item.id'), primary_key=True)
    sales_invoice_id = db.Column(db.SmallInteger, db.ForeignKey('sales_invoice.id'), primary_key=True)
    quantity = db.Column(db.SmallInteger, default=0)
    item = db.relationship('Item')

    def __unicode__(self):
        return unicode(SalesInvoice.query.get(
                        self.sales_invoice_id).created_at)
