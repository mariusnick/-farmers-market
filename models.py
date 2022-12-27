import os
import json
from xmlrpc.client import Boolean, DateTime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from flask_migrate import Migrate
from sqlalchemy.orm import relationship

from flask_sqlalchemy import SQLAlchemy
import json

# database_path = os.environ['DATABASE_URL']

database_name = "market"
# database_path = "postgresql://{}:{}@{}/{}".format(
    # 'postgres', '123', 'localhost:5432', database_name)
database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
                      


'''
Vendor

'''


class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = Column(db.Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    city = Column(String)
    email = Column(String)
    phone = Column(String)
    ratings = Column(String)
    #orders = db.relationship('Sale_Order', backref='list', lazy=True)

    def __init__(self, name, address, city, email, phone):
        self.name = name
        self.address = address
        self.city = city
        self.email = email
        self.phone = phone

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'phone':self.phone,
            'ratings': self.ratings}


class Product(db.Model):
    __tablename__ = 'product'
    id = Column(db.Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    uom = Column(String)

    def __init__(self, name, category, uom):
        self.name = name
        self.category = category
        self.uom = uom

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name}


class Sale_Order(db.Model):
    __tablename__ = 'sale_order'

    id = Column(db.Integer, primary_key=True)
    vendor_id = Column(Integer, ForeignKey('vendor.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    data_production = Column(DateTime)
    data_order = Column(DateTime)
    qty_total = Column(Integer)
    qty_remain = Column(Integer)
    ratings = Column(String)

    def __init__(self, vendor_id, product_id, data_production,data_order,qty_total,qty_remain):
       
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.data_production = data_production
        self.data_order = data_order
        self.qty_remain = qty_remain
        self.qty_total = qty_total

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'vendor': self.vendor_id,
            'product': self.product_id,
            'qty_remain':self.qty_remain,
            'ratings':self.ratings}


class Customer(db.Model):
    __tablename__ = 'customer'

    id = Column(db.Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    city = Column(String)
    email = Column(String)
    phone = Column(String)
    ratings = Column(String)
    # orders = db.relationship('Buy_Order', backref='list', lazy=True)
    
    def __init__(self, name, address, city, email, phone):
       
        self.name = name
        self.address = address
        self.city = city
        self.email = email
        self.phone = phone
        

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'email':self.email,
            'ratings':self.ratings
            }


class Buy_Order(db.Model):
    __tablename__ = 'buy_order'

    id = Column(db.Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('vendor.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    sale_order_id = Column(Integer, ForeignKey('sale_order.id'))
    payment = Column(db.Boolean)
    shipping = Column(db.Boolean)
    active = Column(db.Boolean)
    data_order = Column(DateTime)
    qty = Column(Integer)

    def __init__(self, customer_id,sale_order_id,product_id,payment,shipping,active,data_order,qty):
        
        self.customer_id = customer_id
        self.sale_order_id = sale_order_id
        self.product_id = product_id
        self.payment = payment
        self.shipping = shipping
        self.active = active
        self.data_order = data_order
        self.qty = qty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'customer': self.customer_id,
            'product': self.product_id,
            'shipping':self.shipping,
            }










