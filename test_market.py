from datetime import datetime
import os
# from tkinter.messagebox import NO
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from app import create_app
from models import setup_db, Vendor, Product, Customer, Sale_Order, Buy_Order

auth_dict = {"Vendor": {
            "description": "Farmer, person how sell",
            "jwt_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRqWkpMVVNnSEZQcDVQMGNPVlVIUyJ9.eyJpc3MiOiJodHRwczovL2Rldi14NWNzeDNmby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjM3ZTdlMTVjMGY4YWFiZmY2NGE3NTE1IiwiYXVkIjoibWFya2V0IiwiaWF0IjoxNjY5OTE3MzUwLCJleHAiOjE2Njk5ODkzNTAsImF6cCI6ImVadE1jM3dOeEpYRnVVTkNFNDNyMUxpdThGdFhXVHR4Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YnV5X29yZGVyIiwiZ2V0OmN1c3RvbWVyIiwiZ2V0OnByb2R1Y3QiLCJnZXQ6c2FsZV9vcmRlciIsImdldDp2ZW5kb3IiLCJwYXRjaDpzYWxlX29yZGVyIiwicGF0Y2g6dmVuZG9yIiwicHV0OnNhbGVfb3JkZXIiLCJwdXQ6dmVuZG9yIl19.p3sW76kmAnF0viRIxDoDS_pVN0u3qlRbZfLs5I_QeixmdZYPHVEhnWLA7lRtAndmp1M48bDtMQCAUKmCbRlerAIc5yIAr3LqfwnLmqZ8fvlRnWzqG8WRc988bmqkxT7c5aTLftzZMrACU_15HZwIl6fNa0mceuMeqKzK2_srf8XVS3oNMi2TIZ_eB4rRWUwN4xeW0ir62DPa2j2ipapJbN56PLAn7JR0AH4h_QnPGkJXvuQopNpAKmIKr-b0BwathAQ3o7Uv0Ojt8Uwm8Mwpleb9hMhEjacpVezvc5XsrTo-F6RgrJaHt2quHjozsgvnfQAlH46CC7gwiZQTsHasCA"
        },
        "Customer": {
            "description": "Customer, person how buy ",
            "jwt_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRqWkpMVVNnSEZQcDVQMGNPVlVIUyJ9.eyJpc3MiOiJodHRwczovL2Rldi14NWNzeDNmby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjM3ZmMyZGVhOGIyYzJlYzYwYjMyNDQ4IiwiYXVkIjoibWFya2V0IiwiaWF0IjoxNjY5OTE3NDU4LCJleHAiOjE2Njk5ODk0NTgsImF6cCI6ImVadE1jM3dOeEpYRnVVTkNFNDNyMUxpdThGdFhXVHR4Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YnV5X29yZGVyIiwiZ2V0OmN1c3RvbWVyIiwiZ2V0OnByb2R1Y3QiLCJnZXQ6c2FsZV9vcmRlciIsImdldDp2ZW5kb3IiLCJwYXRjaDpidXlfb3JkZXIiLCJwYXRjaDpjdXN0b21lciIsInB1dDpidXlfb3JkZXIiLCJwdXQ6Y3VzdG9tZXIiXX0.j52euFwe7hAgj4cZv00Ddi9BjG4XGsopzIj_45cnTzHV-DkSlylOb8Lysm_yfHX-2aYMo48JKxT7AmBbE46MjOIYlEJIwjAbCjxrBLtob5Zth0VDOlMvAcJ0Dp1KHZ9bZ6_vf6AK3ved1-2pQnDDsV_WwNUirwV8sS36kFJNoUVWhyWUGBWrsWSfptE8MpRLDnr705QIYvVlW1REkB5oXFRWQKHW3rxouaQxILb9crHIG-li2HhZWC7hrugDPu6F4DjwPQlS8L3dwZ-JNgNW89bQMMWu-dfp_Tm88PmNGWzGAgKo3XYwg5nmllcPtt1F0SVMED6_vafZ1oCy0tszww",   
        },
        "Manager": {
            "description": "Administrator ",
            "jwt_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRqWkpMVVNnSEZQcDVQMGNPVlVIUyJ9.eyJpc3MiOiJodHRwczovL2Rldi14NWNzeDNmby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjM4NzAzYzA5YjljNGZlZmZiZjcyNTRjIiwiYXVkIjoibWFya2V0IiwiaWF0IjoxNjY5OTE2ODYwLCJleHAiOjE2Njk5ODg4NjAsImF6cCI6ImVadE1jM3dOeEpYRnVVTkNFNDNyMUxpdThGdFhXVHR4Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YnV5X29yZGVyIiwiZGVsZXRlOmN1c3RvbWVyIiwiZGVsZXRlOnByb2R1Y3QiLCJkZWxldGU6c2FsZV9vcmRlciIsImRlbGV0ZTp2ZW5kb3IiLCJnZXQ6YnV5X29yZGVyIiwiZ2V0OmN1c3RvbWVyIiwiZ2V0OnByb2R1Y3QiLCJnZXQ6c2FsZV9vcmRlciIsImdldDp2ZW5kb3IiLCJwYXRjaDpidXlfb3JkZXIiLCJwYXRjaDpjdXN0b21lciIsInBhdGNoOnByb2R1Y3QiLCJwYXRjaDpzYWxlX29yZGVyIiwicGF0Y2g6dmVuZG9yIiwicHV0OmJ1eV9vcmRlciIsInB1dDpjdXN0b21lciIsInB1dDpwcm9kdWN0IiwicHV0OnNhbGVfb3JkZXIiLCJwdXQ6dmVuZG9yIl19.Sabs1gWpwwGQAiP8N6JEt7ApqYgRh7tLsomLVTdALM__ztvnlclq3kEm0KLzg4l1Q6pJ7Q2jN8gTvXSI28FOmoD5V0vr3PcOwdrUxSiYC0XVojGrlOKplnKZwCCfCNb2Tv3gqR0iRUpT7n8N8leYRbZhPEEKGWwjTcyliJgUSo4ka0Sn7gPVrUpgCLlXfM7pL4suWYs6Y1JwbzwIca99sCzGfWclqAYSJneEXY7wdaZkOmy_yf0nszqUBGZDmamPDLq3IBGkNMis4B_H8ws0cV2rHahJVyuBZyzy2JD-CwMeEY-DWD1vG-g9-wRyMpV8y0gSmETXjkIjGC5P7KRytg",
        }
   }


class MarketTestCase(unittest.TestCase):
    """This class represents the market test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "market_test"
        self.database_path = "postgresql:///{}".format( self.database_name)
        # self.database_path = "postgres:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        # new items
        self.new_vendor = {'name': 'Andrew', 'address': 'xx no14',
                           'city': 'Rye', 'email': 'an@farm.br', 'phone': '04755587'}
        self.new_product = {'name': 'pepper',
                            'category': 'vegetabels', 'uom': 'kg'}
        self.new_customer = {'name': 'Geroge', 'address': 'xx no14',
                             'city': 'London', 'email': 'gre@farm.br', 'phone': '05755587'}
        self.new_sale_order = {'vendor_id': 100,
                               'product_id': 100, 'qty': 50}
        self.new_buy_order = {'customer_id': 100, 'sale_order_id': 100, 'qty': 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            
            # create all tables
            self.db.create_all()
        
            
         # Set up authentication tokens
       
        vendor_jwt = auth_dict["Vendor"]["jwt_token"]
        customer_jwt = auth_dict["Customer"]["jwt_token"]
        manager_jwt = auth_dict["Manager"]["jwt_token"]
        self.auth_headers = {
            "Vendor": f'Bearer {vendor_jwt}',
            "Customer": f'Bearer {customer_jwt}',
            "Manager": f'Bearer {manager_jwt}'
        }


    """
    Vendor
    """

    def test_get_vendor(self):
        header = {
            "Authorization": self.auth_headers["Manager"]
        }
        res = self.client().get("/vendors", headers=header)
        print(res.status_code)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["vendors"])
        self.assertTrue(len(data["vendors"]))
        
    def test_get_vendor_byid(self):
        header = {
            "Authorization": self.auth_headers["Manager"]
        }
        res = self.client().get("/vendors/100", headers=header)
        print(res.status_code)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["vendors"])
        self.assertEqual(len(data["vendors"]),1)

    def test_create_new_vendor(self):
        header = {
            "Authorization": self.auth_headers["Manager"]
        }
        res = self.client().post("/vendors", json=self.new_vendor, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["created"], True)

    def test_update_vendor(self):
        header = {
            "Authorization": self.auth_headers["Manager"]
        }
        update_id_vendors = 100
        new_phone = '99999999'
        res = self.client().patch(
            f'/vendors/{update_id_vendors}',
            json={
                'phone': new_phone,
                'ratings': '4.5'},
        headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['updated'])
        self.assertEqual(data['vendor']['id'], update_id_vendors)
        self.assertEqual(data['vendor']['phone'], new_phone)
        self.assertEqual(data['vendor']['ratings'], '4.5')
        
    def test_delete_vendor(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        res = self.client().get("/vendors", headers=header)
        print(res.status_code)
        data = json.loads(res.data)
        last = len(data['vendors'])-1
        vendor_id = data['vendors'][last]['id']
        res = self.client().delete("/vendors/"+str(vendor_id), headers=header)
        data = json.loads(res.data)
        vendor = Vendor.query.filter(Vendor.id == vendor_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], vendor_id)
        self.assertEqual(vendor, None)

    """
    Customer
    """

    def test_get_customer(self):
        header = {
            "Authorization": self.auth_headers["Manager"]
        }
        res = self.client().get("/customers", headers=header)
        print(res.status_code)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["customers"])
        self.assertTrue(len(data["customers"]))
        
    def test_get_customer_by_city(self):
        header = {"Authorization": self.auth_headers["Manager"]}
        
        res = self.client().get("/customers/Drover", headers=header)
        print(res.status_code)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["customers"])
        self.assertEqual(len(data["customers"]),2)
        
    def test_update_customer(self):
        header = {
            "Authorization": self.auth_headers["Manager"]
        }
        update_id_customer = 100
        new_email = 'lll@l.com'
        res = self.client().patch(
            f'/customers/{update_id_customer}',
            json={
                'email': new_email,
                'ratings': '4.2'},
        headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['updated'])
        self.assertEqual(data['customer']['id'], update_id_customer)
        self.assertEqual(data['customer']['email'], new_email)
        self.assertEqual(data['customer']['ratings'], '4.2')

    def test_create_new_customer(self):
        header = {
            "Authorization": self.auth_headers["Manager"]
        }
        
        res = self.client().post("/customers", json=self.new_customer, headers=header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)

        self.assertTrue(data["created"], True)

    def test_delete_customer(self):
        header = {
            "Authorization": self.auth_headers["Manager"]
        }
        res = self.client().get("/customers", headers=header)
        print(res.status_code)
        data = json.loads(res.data)
        last = len(data['customers'])-1
        customer_id = data['customers'][last]['id']
        res = self.client().delete("/customers/"+str(customer_id), headers=header)
        data = json.loads(res.data)
        customer = Customer.query.filter(Customer.id == customer_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], customer_id)
        self.assertEqual(customer, None)

    """
    Product
    """
    def test_get_product(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        res = self.client().get("/products", headers=header)
        print(res.status_code)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["products"])
        self.assertTrue(len(data["products"]))

    def test_create_new_product(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        res = self.client().post("/products", json=self.new_product, headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

        self.assertTrue(data["created"], True)

    def test_delete_product(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        res = self.client().get("/products", headers=header)
        print(res.status_code)
        data = json.loads(res.data)
        last = len(data['products'])-1
        product_id = data['products'][last]['id']
        res = self.client().delete("/products/"+str(product_id),headers=header)
        data = json.loads(res.data)
        product = Product.query.filter(Product.id == product_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], product_id)
        self.assertEqual(product, None)

    """
    Sale_order
    """

    def test_get_ordersale(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        res = self.client().get("/sale_orders", headers=header)
        print(res.status_code)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["sale_orders"])
        self.assertTrue(len(data["sale_orders"]))

    def test_create_new_sale_order(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        res = self.client().post("/sale_orders", json=self.new_sale_order, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["created"], True)

    def test_delete_sale_order(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        res = self.client().get("/sale_orders", headers=header)
        print(res.status_code)
        data = json.loads(res.data)
        last = len(data['sale_orders'])-1
        sale_order_id = data['sale_orders'][last]['id']
        res = self.client().delete("/sale_orders/"+str(sale_order_id), headers=header)
        data = json.loads(res.data)
        sale_order = Sale_Order.query.filter(
            Sale_Order.id == sale_order_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], sale_order_id)
        self.assertEqual(sale_order, None)
        
    
    def test_update_sale_order(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        update_id_sale_order = 100
        new_qty_remain = 5
        res = self.client().patch(
            f'/sale_orders/{update_id_sale_order}',
            json={
                'qty_remain': new_qty_remain,
                'ratings': '4.8'},headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['updated'])
        self.assertEqual(data['sale_order']['id'], update_id_sale_order)
        self.assertEqual(data['sale_order']['qty_remain'], new_qty_remain)
        self.assertEqual(data['sale_order']['ratings'], '4.8')

    """
    Buy_order
    """

    def test_get_orderbuy(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        res = self.client().get("/buy_orders", headers=header)
        print(res.status_code)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["buy_orders"])
        self.assertTrue(len(data["buy_orders"]))

    def test_create_new_buy_order(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        res = self.client().post("/buy_orders", json=self.new_buy_order, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["created"], True)

    def test_delete_buy_order(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        res = self.client().get("/buy_orders", headers=header)
        print(res.status_code)
        data = json.loads(res.data)
        last = len(data['buy_orders'])-1
        buy_order_id = data['buy_orders'][last]['id']
        res = self.client().delete("/buy_orders/"+str(buy_order_id), headers=header)
        data = json.loads(res.data)
        buy_order = Buy_Order.query.filter(Buy_Order.id == buy_order_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], buy_order_id)
        self.assertEqual(buy_order, None)
        
    def test_update_buy_order(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        update_id_buy_order = 100
        shipping = True
        res = self.client().patch(
            f'/buy_orders/{update_id_buy_order}',
            json={'shipping': shipping}, headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['updated'])
        self.assertEqual(data['buy_order']['id'], update_id_buy_order)
        self.assertEqual(data['buy_order']['shipping'], shipping)
        
        
    def test_get_vendor_fail_401(self):   
        res = self.client().get("/vendors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
    def test_create_new_vendor_fail_400(self):
        header = {
            "Authorization": self.auth_headers["Manager"]
        }
        new_vendor = {'city':'Drover'}    
        res = self.client().post("/vendors", json=new_vendor, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        
    def test_create_new_vendor_403(self):
        header = {
            "Authorization": self.auth_headers["Customer"]
        }
          
        res = self.client().post("/vendors", json=self.new_vendor, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        
        
    def test_create_new_client_fail_400(self):
        header = {
            "Authorization": self.auth_headers["Manager"]
        }
        new_customer = {'city':'Drover'}    
        res = self.client().post("/vendors", json=new_customer, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        
        
    def test_get_customer_fail_401(self):   
        res = self.client().get("/customers")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
    def test_get_product_fail_401(self):
        res = self.client().get("/products")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
    def test_create_new_product_fail_400(self):
        header = {
             "Authorization": self.auth_headers["Manager"]}
        new_product= {'category':'Fruit'}
        res = self.client().post("/products", json=new_product, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        
        
    def test_create_new_sale_order_fail_403(self):
        header = {
             "Authorization": self.auth_headers["Customer"]}
        res = self.client().post("/sale_orders", json=self.new_sale_order, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        
    def test_create_new_sale_buy_fail_403(self):
        header = {
            "Authorization": self.auth_headers["Manager"]}
        new_buy_order = {'customer_id': 100, 'sale_order_id': 250, 'qty': 5}
        res = self.client().post("/buy_orders", json=new_buy_order, headers=header)
        self.assertEqual(res.status_code, 403)
        
        
    def test_create_new_sale_buy_fail_422(self):
        header = {
            "Authorization": self.auth_headers["Manager"]}
        new_buy_order = {'customer_id': 100, 'sale_order_id': 100, 'qty': 250}
        res = self.client().post("/buy_orders", json=new_buy_order, headers=header)
        self.assertEqual(res.status_code, 422)
        
    def test_create_new_sale_buy_fail_403(self):
        header = {
            "Authorization": self.auth_headers["Vendor"]}
        res = self.client().post("/buy_orders", json=self.new_buy_order, headers=header)
        self.assertEqual(res.status_code, 403)
    
    def test_delete_buy_order_fail_403(self):
        header = {
             "Authorization": self.auth_headers["Vendor"]}
        res = self.client().get("/buy_orders", headers=header)
        data = json.loads(res.data)
        last = len(data['buy_orders'])-1
        buy_order_id = data['buy_orders'][last]['id']
        res = self.client().delete("/buy_orders/"+str(buy_order_id), headers=header)
        data = json.loads(res.data)
        buy_order = Buy_Order.query.filter(Buy_Order.id == buy_order_id).one_or_none()
        self.assertEqual(res.status_code, 403)
        
        
    
       

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
