from json import dumps
import os
from flask import Flask, jsonify, request, abort
from models import Sale_Order, Vendor, Product, Customer, Buy_Order, setup_db
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
    def get_vendor():
        vendors = Vendor.query.all()
        print("ssss")
        vendors = list(map(lambda vendor: vendor.format(), vendors))
        return jsonify({
            "success": True,
            "vendors": vendors
        })
    # Products

    @app.route('/products', methods=['GET'])
    def get_products():
        products = Product.query.all()
        products = list(map(lambda product: product.format(), products))
        return jsonify({
            "success": True,
            "products": products
        })
    
    @app.route('/products', methods=['POST'])
    def create_product():
        body = request.get_json()
        
        if body is None:
            abort(400)
        
        name = body.get('name', None) 
        category = body.get('category', None)
        uom = body.get('uom', None)
        
        
        product = Product(
                        name=name,
                        category=category,
                        uom=uom)
        print(product.format())

        product.insert()

        return jsonify({
            "created": True
        })
        
        
    @app.route('/products/<int:product_id>', methods=['DELETE'])
    def delete_product(product_id):
        product_delete = Product.query.filter(Product.id == product_id).one_or_none()

        if Product is None:
            abort(404, "Didn't find product with this id " + str(product_id))

        product_delete.delete()

        return jsonify({
            'success': True,
            'deleted': product_id
        })
        
   

    '''
    POST /vendors
    Creates a new auto.
    Requires the title and release date.
    Example Request: (Create)
    curl --location --request POST 'http://localhost:5000/autos' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "title": "Pek Yakında",
            "release_date": "2020-02-19"
        }'
    Example Response:
    {
        "success": true
    }
    '''
    @app.route('/vendors', methods=['POST'])
    def create_vendors():
        body = request.get_json()
        if body is None:
            abort(400)
            
        name = body.get('name', None)
        city = body.get('city', None)
        email = body.get('email', None)
        phone = body.get('phone', None)
        address = body.get('address',None)

        if name is None :
            abort(400, "No Name")

        vendor = Vendor(
                        name=name,
                        city=city,
                        email=email,
                        phone=phone,
                        address=address)
        print(vendor)

        vendor.insert()

        return jsonify({
            "created": True})
        
    @app.route('/vendors/<int:vendor_id>', methods=['DELETE'])
    def delete_vendor(vendor_id):
        vendor_delete = Vendor.query.filter(Vendor.id == vendor_id).one_or_none()

        if Vendor is None:
            abort(404, "Didn't find vendor with this id " + str(vendor_id))

        vendor_delete.delete()

        return jsonify({
            'success': True,
            'deleted': vendor_id
        })
        
    @app.route('/vendors/<id>', methods=['PATCH'])
    # @requires_auth('patch:drinks')
    def update_vendors(id):
        body = request.get_json()
        print(body)
        print(id)
        if not id :
            abort(422)
    
        
        vendor = Vendor.query.filter(Vendor.id == id).one_or_none()
        
        if not vendor:
            abort(422)
        if 'name' in body:
            vendor.name =  body['name']
        if 'address' in body:
            vendor.address =  body['address']
        if 'city' in body:
                vendor.city =  body['city']
        if 'email' in body:
                vendor.email =  body['email']
        if 'phone' in body:
                vendor.phone =  body['phone']
                
        if 'ratings' in body:
                vendor.ratings =  body['ratings']
            
        try :
        
            vendor.update()
            return jsonify(
                            {
                            "updated": True,
                            "vendor":vendor.format(),         
                            }
                        ),200
        except:
            abort(404)




    # Sale Order


    @app.route('/sale_orders', methods=['GET'])
    def get_so():
        sos = Sale_Order.query.all()
        sos = list(map(lambda so: so.format(), sos))
        return jsonify({
            "success": True,
            "sale_orders": sos
        })
        
    @app.route('/sale_orders', methods=['POST'])
    def create_so():
        body = request.get_json()
        
        if body is None:
            abort(400)
        
        vendor_id = body.get('vendor_id', None) 
        product_id = body.get('product_id', None)
        data_production = body.get('data_production', None)
        qty_total = body.get('qty', None)
        print(vendor_id)
        so = Sale_Order(vendor_id=vendor_id,
                        product_id=product_id,
                        data_production=data_production,
                        data_order=datetime.now(),
                        qty_total=qty_total,
                        qty_remain=qty_total)
        print(so.format())

        so.insert()

        return jsonify({
            "created": True
        })

    @app.route('/sale_orders/<int:sale_order_id>', methods=['DELETE'])
    def delete_sale_order(sale_order_id):
        sale_order_delete = Sale_Order.query.filter(Sale_Order.id == sale_order_id).one_or_none()

        if sale_order_delete is None:
            abort(404, "Didn't find vendor with this id " + str(sale_order_delete.id))

        sale_order_delete.delete()

        return jsonify({
            'success': True,
            'deleted': sale_order_delete.id
        })
        
    @app.route('/sale_orders/<id>', methods=['PATCH'])
    # @requires_auth('patch:drinks')
    def update_sale_order(id):
        body = request.get_json()
        print(body)
        print(id)
        if not id :
            abort(422)
         
        sale_order = Sale_Order.query.filter(Sale_Order.id == id).one_or_none()
        
        if not sale_order:
            abort(422)
            
        if 'product_id' in body:
            sale_order.product_id =  body['product_id']
        if 'data_production' in body:
            sale_order.address =  body['data_production']
        if 'qty_total' in body:
                sale_order.qty_total =  body['qty_total']
        if 'qty_remain' in body:
                sale_order.qty_remain =  body['qty_remain']
        if 'ratings' in body:
                sale_order.ratings =  body['ratings']  
        try :
            sale_order.update()
            return jsonify(
                            {
                            "updated": True,
                            "sale_order":sale_order.format(),         
                            }
                        ),200
        except:
            abort(404)
    
            

    # Customer

    @app.route('/customers', methods=['GET'])
    def get_customers():
        customers = Customer.query.all()
        customers = list(map(lambda customer: customer.format(), customers))
        return jsonify({
            "success": True,
            "customers": customers
        })
        return app

    @app.route('/customers', methods=['POST'])
    def create_customers():
        body = request.get_json()
        
        if body is None:
            abort(400)
            
        name = body.get('name', None)
        city = body.get('city', None)
        email = body.get('email', None)
        phone = body.get('phone', None)
        address = body.get('address',None)
       
        if name is None :
            abort(400, "No Name")
        
        customer = Customer(name=name,
                        city=city,
                        email=email,
                        phone=phone,
                        address=address)
       

        customer.insert()

        return jsonify({
            "created": True
        })
        
    @app.route('/customers/<int:customer_id>', methods=['DELETE'])
    def delete_customer(customer_id):
        customer_delete = Customer.query.filter(Customer.id == customer_id).one_or_none()

        if Customer is None:
            abort(404, "Didn't find customer with this id " + str(customer_id))

        customer_delete.delete()

        return jsonify({
            'success': True,
            'deleted': customer_id
        })
        
        
    @app.route('/customers/<id>', methods=['PATCH'])
    # @requires_auth('patch:drinks')
    def update_customers(id):
        body = request.get_json()
        print(body)
        print(id)
        if not id :
            abort(422)
     
        customer = Customer.query.filter(Customer.id == id).one_or_none()
        
        if not customer:
            abort(422)
        if 'name' in body:
            customer.name =  body['name']
        if 'address' in body:
            customer.address =  body['address']
        if 'city' in body:
                customer.city =  body['city']
        if 'email' in body:
                customer.email =  body['email']
        if 'phone' in body:
                customer.phone =  body['phone']
        if 'ratings' in body:
                customer.ratings =  body['ratings']
            
        try :      
            customer.update()
            return jsonify(
                            {
                            "updated": True,
                            "customer":customer.format(),         
                            }
                        ),200
        except:
            abort(404)



    #Buy Order


    @app.route('/buy_orders', methods=['GET'])
    def get_bo():
        bos = Buy_Order.query.all()
        bos = list(map(lambda bo: bo.format(), bos))
        return jsonify({
            "success": True,
            "buy_orders": bos
        })

        return app

    @app.route('/buy_orders', methods=['POST'])
    def create_bo():
        body = request.get_json()
        
        if body is None:
            abort(400)
            
        customer_id = body.get('customer_id', None) 
        product_id = body.get('product_id', None)
        sale_order_id = body.get('sale_order_id', None)
        qty = body.get('qty', None)
        
        bo = Buy_Order(
                        customer_id=customer_id,
                        product_id=product_id,
                        sale_order_id=sale_order_id,
                        data_order=datetime.now(),
                        active = True,
                        shipping = False,
                        payment = False,
                        qty=qty)
        
        so = Sale_Order.query.filter(Sale_Order.id == int(sale_order_id)).one_or_none()
        if so.qty_remain >= qty:
            so.qty_remain = so.qty_remain - qty
        else:
            pass
        so.update()
        
        print(bo.format())

        bo.insert()

        return jsonify({
            "created": True
        })
      

    @app.route('/buy_orders/<int:buy_order_id>', methods=['DELETE'])
    def delete_buy_order(buy_order_id):
        buy_order_delete = Buy_Order.query.filter(Buy_Order.id == buy_order_id).one_or_none()

        if buy_order_delete is None:
            abort(404, "Didn't find buy order with this id " + str(buy_order_id))

        buy_order_delete.delete()

        return jsonify({
            'success': True,
            'deleted': buy_order_delete.id
        })
        
    @app.route('/buy_orders/<id>', methods=['PATCH'])
    # @requires_auth('patch:drinks')
    def update_buy_orders(id):
        body = request.get_json()
        print(body)
        print(id)
        if not id :
            abort(422)
        print("aasASSAAAAASSSAAA")
        buy_order = Buy_Order.query.filter(Buy_Order.id == id).one_or_none()
        
        if not buy_order:
            abort(422)
        if 'active' in body:
            buy_order.active =  body['active']
        if 'payment' in body:
            buy_order.payment =  body['address']
        if 'shipping' in body:
            buy_order.shipping =  body['shipping']
            print("ASSAAAAASSSAAA")
        if 'qty' in body:
            new_qty = int(body['qty'])
            so = Sale_Order.query.filter(Sale_Order.id == buy_order.sale_order_id).one_or_none()
            qty_rremain = so.qty_remain + buy_order.qty 
            print(f"SS {qty_rremain}")
            if qty_rremain > new_qty:
                so.qty_remain = so.qty_remain - new_qty
                buy_order.qty = new_qty
                print('DDDDDD')
                print(buy_order)
                so.update()
            else:
                pass
                
        try :
            print(buy_order.format())
            buy_order.update()
            return jsonify(
                            {
                            "updated": True,
                            "buy_order":buy_order.format(),         
                            }
                        ),200
        except:
            abort(404)

    
    return app


app = create_app()

if __name__ == '__main__':
    app.run()
