from datetime import datetime
import os
# from tkinter.messagebox import NO
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Vendor, Product, Customer, Sale_Order, Buy_Order


class MarketTestCase(unittest.TestCase):
    """This class represents the market test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "market_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # new items
        self.new_vendor = {'name': 'Andrew', 'address': 'xx no14',
                           'city': 'Rye', 'email': 'an@farm.br', 'phone': '04755587'}
        self.new_product = {'name': 'pepper',
                            'category': 'vegetabels', 'uom': 'kg'}
        self.new_customer = {'name': 'Geroge', 'address': 'xx no14',
                             'city': 'London', 'email': 'gre@farm.br', 'phone': '05755587'}
        self.new_sale_order = {'vendor_id': 2,
                               'product_id': 1, 'qty_total': 50}
        self.new_buy_order = {'customer_id': 2, 'sale_order_id': 2, 'qty': 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Vendor
    """

    def test_get_vendor(self):
        res = self.client().get("/vendors")
        print(res.status_code)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["vendors"])
        self.assertTrue(len(data["vendors"]))

    def test_create_new_vendor(self):
        res = self.client().post("/vendors", json=self.new_vendor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["created"], True)

    def test_update_vendor(self):
        # header_obj = {
        # "Authorization": self.auth_headers["Casting Director"]
        # }
        update_id_vendors = 2
        new_phone = '99999999'
        res = self.client().patch(
            f'/vendors/{update_id_vendors}',
            json={
                'phone': new_phone,
                'ratings': '4.5'})
        # headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['updated'])
        self.assertEqual(data['vendor']['id'], update_id_vendors)
        self.assertEqual(data['vendor']['phone'], new_phone)
        self.assertEqual(data['vendor']['ratings'], '4.5')

    """
    Customer
    """

    def test_get_customer(self):
        res = self.client().get("/customers")
        print(res.status_code)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["customers"])
        self.assertTrue(len(data["customers"]))
        
    def test_update_customer(self):
        # header_obj = {
        # "Authorization": self.auth_headers["Casting Director"]
        # }
        update_id_customer = 2
        new_email = 'lll@l.com'
        res = self.client().patch(
            f'/customers/{update_id_customer}',
            json={
                'email': new_email,
                'ratings': '4.2'})
        # headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['updated'])
        self.assertEqual(data['customer']['id'], update_id_customer)
        self.assertEqual(data['customer']['email'], new_email)
        self.assertEqual(data['customer']['ratings'], '4.2')

    # def test_create_new_customer(self):
    #     res = self.client().post("/customers", json=self.new_customer)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)

    #     self.assertTrue(data["created"], True)

    # def test_delete_customer(self):
    #     res = self.client().get("/customers")
    #     print(res.status_code)
    #     data = json.loads(res.data)
    #     print(data)
    #     last = len(data['customers'])-1
    #     customer_id = data['customers'][last]['id']
    #     print(customer_id)
    #     res = self.client().delete("/customers/"+str(customer_id))
    #     data = json.loads(res.data)
    #     customer = Customer.query.filter(Customer.id == customer_id).one_or_none()
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], customer_id)
    #     self.assertEqual(customer, None)

    # """
    # Product
    # """
    # def test_get_product(self):
    #     res = self.client().get("/products")
    #     print(res.status_code)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["products"])
    #     self.assertTrue(len(data["products"]))

    def test_create_new_product(self):
        res = self.client().post("/products", json=self.new_product)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

        self.assertTrue(data["created"], True)

    def test_delete_product(self):
        res = self.client().get("/products")
        print(res.status_code)
        data = json.loads(res.data)
        print(data)
        last = len(data['products'])-1
        product_id = data['products'][last]['id']
        print(product_id)
        res = self.client().delete("/products/"+str(product_id))
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
        res = self.client().get("/sale_orders")
        print(res.status_code)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["sale_orders"])
        self.assertTrue(len(data["sale_orders"]))

    def test_create_new_sale_order(self):
        res = self.client().post("/sale_orders", json=self.new_sale_order)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["created"], True)

    def test_delete_sale_order(self):
        res = self.client().get("/sale_orders")
        print(res.status_code)
        data = json.loads(res.data)
        print(data)
        last = len(data['sale_orders'])-1
        sale_order_id = data['sale_orders'][last]['id']
        print(sale_order_id)
        res = self.client().delete("/sale_orders/"+str(sale_order_id))
        data = json.loads(res.data)
        sale_order = Sale_Order.query.filter(
            Sale_Order.id == sale_order_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], sale_order_id)
        self.assertEqual(sale_order, None)
        
    
    def test_update_sale_order(self):
            # header_obj = {
        # "Authorization": self.auth_headers["Casting Director"]
        # }
        update_id_sale_order = 2
        new_qty_remain = 5
        res = self.client().patch(
            f'/sale_orders/{update_id_sale_order}',
            json={
                'qty_remain': new_qty_remain,
                'ratings': '4.8'})
        # headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['updated'])
        self.assertEqual(data['sale_order']['id'], update_id_sale_order)
        self.assertEqual(data['sale_order']['qty_remain'], new_qty_remain)
        self.assertEqual(data['sale_order']['ratings'], '4.8')

    # """
    # Buy_order
    # """

    # def test_get_orderbuy(self):
    #     res = self.client().get("/buy_orders")
    #     print(res.status_code)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["buy_orders"])
    #     self.assertTrue(len(data["buy_orders"]))

    def test_create_new_buy_order(self):
        res = self.client().post("/buy_orders", json=self.new_buy_order)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["created"], True)

    def test_delete_buy_order(self):
        res = self.client().get("/buy_orders")
        print(res.status_code)
        data = json.loads(res.data)
        print(data)
        last = len(data['buy_orders'])-1
        buy_order_id = data['buy_orders'][last]['id']
        print(buy_order_id)
        res = self.client().delete("/buy_orders/"+str(buy_order_id))
        data = json.loads(res.data)
        buy_order = Buy_Order.query.filter(Buy_Order.id == buy_order_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], buy_order_id)
        self.assertEqual(buy_order, None)
        
    def test_update_buy_order(self):
            # header_obj = {
        # "Authorization": self.auth_headers["Casting Director"]
        # }
        update_id_buy_order = 1
        shipping = True
        res = self.client().patch(
            f'/buy_orders/{update_id_buy_order}',
            json={'shipping': shipping})
        # headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['updated'])
        self.assertEqual(data['buy_order']['id'], update_id_buy_order)
        self.assertEqual(data['buy_order']['shipping'], shipping)
        

    # def test_get_paginated_question(self):
    #     res = self.client().get("/questions?page=1")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["totalQuestions"])
    #     self.assertTrue(len(data["questions"]))

    # def test_fail_paginated_question(self):
    #     res = self.client().get("/questions?page=1501")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)

    # def test_delete_vendor(self):
    #     res = self.client().get("/vendors")
    #     print(res.status_code)
    #     data = json.loads(res.data)
    #     last = len(data['vendors'])-1
    #     vendor_id = data['vendors'][last]['id']
    #     res = self.client().delete("/vendors/"+str(vendor_id))
    #     data = json.loads(res.data)
    #     vendor = Vendor.query.filter(Vendor.id == vendor_id).one_or_none()
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], vendor_id)
    #     self.assertEqual(vendor, None)

    # def test_fail_delete_question(self):

    #     res = self.client().delete("/questions/1000")
    #     data = json.loads(res.data)
    #     question = Question.query.filter(Question.id == 10000).one_or_none()
    #     if question is None:
    #         self.assertEqual(res.status_code, 422)
    #         self.assertEqual(data["success"], False)

    # def test_create_new_question(self):
    #     res = self.client().post("/questions", json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["created"])

    # def test_create_question_with_no_data(self):
    #     """Test for ensuring data with empty fields are not processed."""
    #     request_data = {
    #         'question': '',
    #         'answer': '',
    #         'difficulty': '',
    #         'category':'',
    #     }

    #     response = self.client().post('/questions', json=request_data)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')

    # def test_post_questions_search_with_results(self):
    #     res = self.client().post("/questions", json={"searchTerm": "Tom Hanks"})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["totalQuestions"])

    #     self.assertEqual(len(data["questions"]), 1)

    # def test_post_questions_search_no_results(self):
    #     res = self.client().post("/questions", json={"searchTerm": "George Washington"})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertFalse(data["totalQuestions"])
    #     self.assertEqual(len(data["questions"]), 0)

    # def test_fail_search_term_response(self):

    #     request_data = {'searchTerm': ''}

    #     response = self.client().post('/questions', json=request_data)
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')

    # def test_get_category_questions(self):
    #     res = self.client().get("/categories/1/questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["totalQuestions"])
    #     self.assertTrue(len(data["questions"]))

    # def test_post_quizz(self):
    #     res = self.client().post("/quizzes", json={
    #                                             'previous_questions': [1],
    #                                             'quiz_category': 'Entertainment'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["question"])

    # def test_fail_post_quizz(self):
    #     res = self.client().post("/quizzes", json={ })
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
