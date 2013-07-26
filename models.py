from app import db, api
from datetime import datetime
from flask.ext.mongorest import operators as ops
from flask.ext.mongorest.methods import Create, Update, Fetch, List, Delete
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest.resources import Resource


# Data schema
class User(db.Document):
    username = db.StringField(max_length=30, required=True, unique=True)
    password = db.StringField(max_length=30, required=True)
    is_admin = db.BooleanField()

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


class Item(db.Document):
    barcode = db.StringField(max_length=10, required=True, unique=True)
    name = db.StringField(max_length=30, required=True, unique=True)
    stock = db.IntField(default=0, min_value=0, required=True)
    price_buy = db.IntField(default=0, min_value=0, required=True)
    price_sell = db.IntField(default=0, min_value=0, required=True)


class Supplier(db.Document):
    name = db.StringField(max_length=30, required=True, unique=True)
    address = db.StringField(max_length=50)
    contact = db.StringField(max_length=20)
    items = db.ReferenceField(Item)


class PurchaseInvoiceDetail(db.EmbeddedDocument):
    item = db.ReferenceField(Item)
    quantity = db.IntField(default=0, min_value=0, required=True)


class PurchaseInvoice(db.Document):
    code = db.StringField(max_length=10, required=True, unique=True)
    created_at = db.DateTimeField(default=datetime.now)
    details = db.ListField(db.EmbeddedDocumentField(PurchaseInvoiceDetail))


class SaleInvoiceDetail(db.EmbeddedDocument):
    quantity = db.IntField(default=0, min_value=0, required=True)


class SaleInvoice(db.Document):
    code = db.StringField(max_length=10, required=True, unique=True)
    created_at = db.DateTimeField(default=datetime.now)
    discount = db.FloatField(default=0, min_value=0, max_value=0, required=True)
    details = db.EmbeddedDocumentField(SaleInvoiceDetail)


class Customer(db.Document):
    name = db.StringField(max_length=30, required=True)
    address = db.StringField(max_length=50)
    contact = db.StringField(max_length=20)
    invoices = db.ReferenceField(SaleInvoice)


# Resource
class UserResource(Resource):
    document = User

class ItemResource(Resource):
    document = Item

class SupplierResource(Resource):
    document = Supplier

class PurchaseInvoiceDetailResource(Resource):
    document = PurchaseInvoiceDetail

class PurchaseInvoiceResource(Resource):
    document = PurchaseInvoice
    related_resources = {
        'details': PurchaseInvoiceDetailResource
    }

class SaleInvoiceResource(Resource):
    document = SaleInvoice

class SaleInvoiceDetailResource(Resource):
    document = SaleInvoiceDetail

class CustomerResource(Resource):
    document = Customer


# Register API
@api.register(name='users', url='/api/users/')
class UserView(ResourceView):
    resource = UserResource
    methods = [Create, Update, Fetch, List, Delete]


@api.register(name='items', url='/api/items/')
class ItemView(ResourceView):
    resource = ItemResource
    methods = [Create, Update, Fetch, List, Delete]


@api.register(name='suppliers', url='/api/suppliers/')
class SupplierView(ResourceView):
    resource = SupplierResource
    methods = [Create, Update, Fetch, List, Delete]


@api.register(name='customers', url='/api/customers/')
class CustomerView(ResourceView):
    resource = CustomerResource
    methods = [Create, Update, Fetch, List, Delete]


@api.register(name='purchase_invoices', url='/api/invoices/purchase/')
class PurchaseInvoiceView(ResourceView):
    resource = PurchaseInvoiceResource
    methods = [Create, Update, Fetch, List]
