from json import dumps
import os
# from tkinter.messagebox import NO
from auth.auth import AuthError,requires_auth
from flask import Flask, jsonify, request, abort
from models import Sale_Order, Vendor, Product, Customer, Buy_Order, setup_db, db
from datetime import datetime
from flask_cors import CORS


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    # Vendors

    @app.route('/vendors', methods=['GET'])
    @requires_auth('get:vendor')
    def get_vendor(payload):
        vendors = Vendor.query.all()
        print("ssss")
        vendors = list(map(lambda vendor: vendor.format(), vendors))
        return jsonify({
            "success": True,
            "vendors": vendors
        })
        
    @app.route('/vendors/<text>')
    @requires_auth('get:vendor')
    def get_vendors_by_city_id(payload,text):
        """Get all vendors from one city or by id"""
        
        if text.isnumeric():
           
            vendors = Vendor.query.get(int(text))
            vendors = vendors.format()
        else:
            print("Mark text") 
            vendors = Vendor.query.filter(Vendor.city.like(text))
            vendors = list(map(lambda vendor: vendor.format(), vendors))
           
        if vendors is None:
            abort(404)
        else:
            
            return jsonify({
                'success': True,
                'vendors': vendors,
            }), 200

   

    '''
    POST /vendors
    Creates a new vendors.
    Requires the name address city .
    Example Request:
    curl --request POST 'http://localhost:5000/vendors' \
        --header 'Content-Type: application/json' \
        --data-raw ' {
    "name": "Andrew ",
    "address": "xxx no14",
    "city": "Alton",
    "email": "andrew@farm.br",
    "phone": "047755587"}
    Response:
    {    
        "created": true,
        
    }
    '''
    @app.route('/vendors', methods=['POST'])
    @requires_auth('put:vendor')
    def create_vendors(payload):
        body = request.get_json()
        if body is None:
            abort(400)

        name = body.get('name', None)
        city = body.get('city', None)
        email = body.get('email', None)
        phone = body.get('phone', None)
        address = body.get('address', None)

        if name is None or email is None or phone is None:
            abort(400, "No Name or email or phone")

        vendor = Vendor(
            name=name,
            city=city,
            email=email,
            phone=phone,
            address=address)
        print(vendor)
        try:
            vendor.insert()

            return jsonify({
                "created": True})
        except Exception:
            abort(500)

    @app.route('/vendors/<int:vendor_id>', methods=['DELETE'])
    @requires_auth('delete:vendor')
    def delete_vendor(payload,vendor_id):
        vendor_delete = Vendor.query.filter(
            Vendor.id == vendor_id).one_or_none()

        if Vendor is None:
            abort(404, "Didn't find vendor with this id " + str(vendor_id))
        try :
            vendor_delete.delete()

            return jsonify({
                'success': True,
                'deleted': vendor_id
            })
        except Exception:
            db.session.rollback()
            abort(500)

    @app.route('/vendors/<id>', methods=['PATCH'])
    @requires_auth('patch:vendor')
    def update_vendors(payload,id):
        body = request.get_json()
        print(body)
        print(id)
        if not id:
            abort(400)

        vendor = Vendor.query.filter(Vendor.id == id).one_or_none()

        if not vendor:
            abort(404)
        if 'name' in body:
            vendor.name = body['name']
        if 'address' in body:
            vendor.address = body['address']
        if 'city' in body:
            vendor.city = body['city']
        if 'email' in body:
            vendor.email = body['email']
        if 'phone' in body:
            vendor.phone = body['phone']

        if 'ratings' in body:
            vendor.ratings = body['ratings']

        try:

            vendor.update()
            return jsonify(
                {
                    "updated": True,
                    "vendor": vendor.format(),
                }
            ), 200
        except:
            abort(500)
            
            
     # Products

    @app.route('/products', methods=['GET'])
    @requires_auth('get:product')
    def get_products(payload):
        products = Product.query.all()
        products = list(map(lambda product: product.format(), products))
        return jsonify({
            "success": True,
            "products": products
        })
        
    @app.route('/products/<text>')
    @requires_auth('get:product')
    def get_product_by_name(payload,text):
        """Get all product from name or part of name"""
        
        products = Product.query.filter(Product.name.like('%'+text+'%'))
        products = list(map(lambda product: product.format(), products))
        return jsonify({
                'success': True,
                'product': products,
            }), 200

    @app.route('/products', methods=['POST'])
    @requires_auth('put:product')
    def create_product(payload):
        body = request.get_json()

        if body is None:
            abort(404)

        name = body.get('name', None)
        if not name :
            abort(404)    
        category = body.get('category', None)
        uom = body.get('uom', None)

        product = Product(
            name=name,
            category=category,
            uom=uom)
        
        try :
            product.insert()
    
            return jsonify({
                "created": True
            })
        except Exception:
            abort(500)

    @app.route('/products/<int:product_id>', methods=['DELETE'])
    @requires_auth('delete:product')
    def delete_product(payload,product_id):
        product_delete = Product.query.filter(
            Product.id == product_id).one_or_none()

        if Product is None:
            abort(404, "Didn't find product with this id " + str(product_id))
        try:
            product_delete.delete()

            return jsonify({
            'success': True,
            'deleted': product_id
            })
        except Exception:
            db.session.rollback()
            abort(500)

    # Sale Order

    @app.route('/sale_orders', methods=['GET'])
    @requires_auth('get:sale_order')
    def get_so(payload):
        sos = Sale_Order.query.all()
        sos = list(map(lambda so: so.format(), sos))
        return jsonify({
            "success": True,
            "sale_orders": sos
        })
        
        
    @app.route('/sale_orders/<text>')
    @requires_auth('get:sale_order')
    def get_sale_order_by_product_name(payload,text):
        """Get all sale order  from product name or part of  product name"""
        
        products = Product.query.filter(Product.name.like('%'+text+'%'))
        
        products = list(map(lambda product: product.id, products))
        print(products)
        sale_orders = Sale_Order.query.join(Product).filter(Product.name.like('%'+text+'%'))
        print(sale_orders)
        sale_orders = list(map(lambda so: so.format(), sale_orders))
        return jsonify({
                'success': True,
                'sale_order': sale_orders,
            }), 200

    @app.route('/sale_orders', methods=['POST'])
    @requires_auth('put:sale_order')
    def create_so(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        vendor_id = body.get('vendor_id', None)
        product_id = body.get('product_id', None)
        data_production = body.get('data_production', None)
        qty_total = body.get('qty', None)
        if not vendor_id or not product_id or not qty_total:
            abort(400)
        
        print(vendor_id)
        so = Sale_Order(vendor_id=vendor_id,
                        product_id=product_id,
                        data_production=data_production,
                        data_order=datetime.now(),
                        qty_total=qty_total,
                        qty_remain=qty_total)
        print(so.format())
        try:
            so.insert()

            return jsonify({
                "created": True
                })
        except Exception:
            abort(500)

    @app.route('/sale_orders/<int:sale_order_id>', methods=['DELETE'])
    @requires_auth('delete:sale_order')
    def delete_sale_order(payload,sale_order_id):
        sale_order_delete = Sale_Order.query.filter(
            Sale_Order.id == sale_order_id).one_or_none()

        if sale_order_delete is None:
            abort(404, "Didn't find vendor with this id " +
                  str(sale_order_delete.id))
        try:
            sale_order_delete.delete()

            return jsonify({
                'success': True,
                'deleted': sale_order_delete.id
            })
        except Exception:
            abort(500)

    @app.route('/sale_orders/<id>', methods=['PATCH'])
    @requires_auth('patch:sale_order')
    def update_sale_order(payload,id):
        body = request.get_json()
        print(body)
        print(id)
        if not id:
            abort(400)

        sale_order = Sale_Order.query.filter(Sale_Order.id == id).one_or_none()

        if not sale_order:
            abort(404)

        if 'product_id' in body:
            sale_order.product_id = body['product_id']
        if 'data_production' in body:
            sale_order.address = body['data_production']
        if 'qty_total' in body:
            sale_order.qty_total = body['qty_total']
        if 'qty_remain' in body:
            sale_order.qty_remain = body['qty_remain']
        if 'ratings' in body:
            sale_order.ratings = body['ratings']
        try:
            sale_order.update()
            return jsonify(
                {
                    "updated": True,
                    "sale_order": sale_order.format(),
                }
            ), 200
        except:
            abort(500)

    # Customer

    @app.route('/customers', methods=['GET'])
    @requires_auth('get:customer')
    def get_customers(payload):
        customers = Customer.query.all()
        customers = list(map(lambda customer: customer.format(), customers))
        return jsonify({
            "success": True,
            "customers": customers
        })
        return app
    
    @app.route('/customers/<text>')
    @requires_auth('get:customers')
    def get_customers_by_city_id(payload,text):
        """Get all vendors from one city or by id"""
        
        if text.isnumeric():
            customers = Customer.query.get(int(text))
        else: customers = Customer.query.filter(Customer.city.like(text))

        if customers is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'customers': customers,
            }), 200
    

    @app.route('/customers', methods=['POST'])
    @requires_auth('put:customer')
    def create_customers(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        name = body.get('name', None)
        city = body.get('city', None)
        email = body.get('email', None)
        phone = body.get('phone', None)
        address = body.get('address', None)

        if name is None or email is None or phone is None:
            abort(400, "No Name")

        customer = Customer(name=name,
                            city=city,
                            email=email,
                            phone=phone,
                            address=address)
        try:
            customer.insert()
            return jsonify({
                "created": True
                })
        except Exception:
            abort(500)

    @app.route('/customers/<int:customer_id>', methods=['DELETE'])
    @requires_auth('delete:customer')
    def delete_customer(payload, customer_id):
        customer_delete = Customer.query.filter(
            Customer.id == customer_id).one_or_none()

        if Customer is None:
            abort(404, "Didn't find customer with this id " + str(customer_id))
        try:
            customer_delete.delete()

            return jsonify({
                'success': True,
                'deleted': customer_id
            })
        except Exception:
            abort(500)

    @app.route('/customers/<id>', methods=['PATCH'])
    @requires_auth('patch:customer')
    def update_customers(payload, id):
        body = request.get_json()
        print(body)
        print(id)
        if not id:
            abort(400)

        customer = Customer.query.filter(Customer.id == id).one_or_none()

        if not customer:
            abort(404)
        if 'name' in body:
            customer.name = body['name']
        if 'address' in body:
            customer.address = body['address']
        if 'city' in body:
            customer.city = body['city']
        if 'email' in body:
            customer.email = body['email']
        if 'phone' in body:
            customer.phone = body['phone']
        if 'ratings' in body:
            customer.ratings = body['ratings']

        try:
            customer.update()
            return jsonify(
                {
                    "updated": True,
                    "customer": customer.format(),
                }
            ), 200
        except:
            abort(500)

    # Buy Order

    @app.route('/buy_orders', methods=['GET'])
    @requires_auth('get:buy_order')
    def get_bo(payload):
        bos = Buy_Order.query.all()
        bos = list(map(lambda bo: bo.format(), bos))
        return jsonify({
            "success": True,
            "buy_orders": bos
        })

        return app

    @app.route('/buy_orders', methods=['POST'])
    @requires_auth('put:buy_order')
    def create_bo(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        customer_id = body.get('customer_id', None)
        product_id = body.get('product_id', None)
        sale_order_id = body.get('sale_order_id', None)
        qty = body.get('qty', None)
        
        if customer_id is None or product_id is None or sale_order_id is None:
            abort(400)

        bo = Buy_Order(
            customer_id=customer_id,
            product_id=product_id,
            sale_order_id=sale_order_id,
            data_order=datetime.now(),
            active=True,
            shipping=False,
            payment=False,
            qty=qty)

        so = Sale_Order.query.filter(
            Sale_Order.id == int(sale_order_id)).one_or_none()
        if so.qty_remain >= qty:
            so.qty_remain = so.qty_remain - qty
        else: 
            # need abort
            pass
        so.update()

        print(bo.format())
        try:
            bo.insert()

            return jsonify({
                "created": True })
        except Exception:
            abort(500)

    @app.route('/buy_orders/<int:buy_order_id>', methods=['DELETE'])
    @requires_auth('delete:buy_order')
    def delete_buy_order(payload, buy_order_id):
        buy_order_delete = Buy_Order.query.filter(
            Buy_Order.id == buy_order_id).one_or_none()

        if buy_order_delete is None:
            abort(404, "Didn't find buy order with this id " + str(buy_order_id))
        
        try:
            buy_order_delete.delete()
       
            return jsonify({
                    'success': True,
                    'deleted': buy_order_delete.id
                })
        except Exception:
            abort(500)

    @app.route('/buy_orders/<id>', methods=['PATCH'])
    @requires_auth('patch:buy_order')
    def update_buy_orders(payload, id):
        body = request.get_json()
        print(body)
        print(id)
        if not id:
            abort(400)
        
        buy_order = Buy_Order.query.filter(Buy_Order.id == id).one_or_none()

        if not buy_order:
            abort(404)
        if 'active' in body:
            buy_order.active = body['active']
        if 'payment' in body:
            buy_order.payment = body['address']
        if 'shipping' in body:
            buy_order.shipping = body['shipping']
           
        if 'qty' in body:
            new_qty = int(body['qty'])
            so = Sale_Order.query.filter(
                Sale_Order.id == buy_order.sale_order_id).one_or_none()
            qty_rremain = so.qty_remain + buy_order.qty
            print(f"SS {qty_rremain}")
            if qty_rremain > new_qty:
                so.qty_remain = so.qty_remain - new_qty
                buy_order.qty = new_qty
                print(buy_order)
                so.update()
            else:
                pass

        try:
            print(buy_order.format())
            buy_order.update()
            return jsonify(
                {
                    "updated": True,
                    "buy_order": buy_order.format(),
                }
            ), 200
        except:
            abort(500)
            
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
    
    
    
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
    
    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    
    @app.errorhandler(401)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401
    

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500
        
        
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
