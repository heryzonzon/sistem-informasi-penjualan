from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean)

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
    name = db.Column(db.String(30))
    address = db.Column(db.String(50), nullable=True)
    contact = db.Column(db.String(20), nullable=True)

    def __unicode__(self):
        return self.name


class Customer(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(30))
    address = db.Column(db.String(50), nullable=True)
    contact = db.Column(db.String(20), nullable=True)

    def __unicode__(self):
        return self.name


class Item(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    barcode = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(30))
    stock = db.Column(db.SmallInteger, default=0)
    price_buy = db.Column(db.Integer, default=0)
    price_sell = db.Column(db.Integer, default=0)
    supplier_id = db.Column(db.SmallInteger, db.ForeignKey('supplier.id'), nullable=True)

    def __unicode__(self):
        return '%s (Stok: %s)' % (self.name, self.stock)


class PurchaseInvoice(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    items = db.relationship('PurchaseInvoiceDetail', backref='purchase_invoice')

    def __unicode__(self):
        return self.created_at


class PurchaseInvoiceDetail(db.Model):
    item_id = db.Column(db.SmallInteger, db.ForeignKey('item.id'), primary_key=True)
    purchase_invoice_id = db.Column(db.SmallInteger, db.ForeignKey('purchase_invoice.id'), primary_key=True)
    quantity = db.Column(db.SmallInteger, default=0)
    item = db.relationship('Item', backref='purchase_invoice_items')


class SalesInvoice(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    discount = db.Column(db.Float, default=0)
    items = db.relationship('SalesInvoiceDetail', backref='sales_invoices')

    def __unicode__(self):
        return self.created_at


class SalesInvoiceDetail(db.Model):
    item_id = db.Column(db.SmallInteger, db.ForeignKey('item.id'), primary_key=True)
    sales_invoice_id = db.Column(db.SmallInteger, db.ForeignKey('sales_invoice.id'), primary_key=True)
    quantity = db.Column(db.SmallInteger, default=0)
    item = db.relationship('Item', backref='sales_invoice_items')


db.create_all()
