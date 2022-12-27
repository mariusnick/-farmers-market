# Description

Farm--Market is an application where farmers can sell their agricultural goods directly to customers online.

Farmers after register, enter data about them as well name, address ,email, phone. Farmers   enter their orders for the sale of products. A sales order contains the product, the initial (total) quantity, the farmer who entered the sales order, the production date of the product
Customers have to register, they enter data about them as well name, address ,email, phone. They can see the sales orders entered. They select the sales order that contains the product they want to buy. Based on a selected sell order they can enter their buy order (purchase order). The buy order contain customer, sale order selected, date, quantity customer wants to buy. On the sales order on which a buy order has been entered, the remaining quantity field will be modified (the quantity from the buy order will be subtracted)

There are three  user roles whith related permissions, which are:
- Vendor: Can view, create, modify a vendors, can view products, can view customers, can view, create, modify sale order and can view buy_order.
- Customer: Can view vendors,can view products, can view, create, modify customers, can view sale_orders, can view, create, modify a buy_orders.
- Manager: Can view, create, delete modify a vendors,can view,can create, delete, modify  products can view, create, delete modify add, modify a customers,can view, create, delete, modify sale_ordes, can view, create, delete, modify buy_orders. 



# Running the API

API endpoints can be accessed  https://farmers--market.herokuapp.com/

Auth0 information for endpoints that require authentication can be found in `auth.sh`.



# API Documentation

 
- All error handlers return a JSON object with the request status and error message.

400
- 400 error handler is returned when request is not correct, url or date are not correct.
```{    "success": false
        "error": 400,
        "message": "bad request"
}
```
401
- 401 error handler is returned when there is an issue with the authentication necessary for the action being requested. 
```
{   "success": false
	"error": 401,
	"message":  "Unauthorized",
	
}
```
403
- 403 error handler occurs when the requested action is not allowed, i.e. incorrect permissions.
```
{   
    "success": false
	"error": 403,
	"message": "Permission not found.",
}
```
404
- 404 error handler occurs when a request resource cannot be found in the database, i.e. an actor with a nonexistent ID is requested.
```
{   "success": false
	"error": 404,
	"message": ""Resource Not Found"",
}
```
422
- 422 error handler is returned when the request contains invalid arguments, i.e. a difficulty level that does not exist.
```
{   "success": false
	"error": 422,
	"message": "unprocessable",
	
}
```
## ENPOINTS

### GET/vendors

- General: 
  - Returns all the vendors.

- Sample Request :  `curl  http://farmers--market.herokuapp.com/vendors` <br>
- Sample Response
```json
   {
    "vendors": [
        {
            "city": "Lin",
            "id": 1,
            "name": "Andrew rex",
            "phone": "047755587",
            "ratings": null
        },
        {
            "city": "Laid",
            "id": 2,
            "name": "George ",
            "phone": "04887755587",
            "ratings": null
        }],
        "success": true
    }
```

### GET /vendors/<text\>

  - If parameter text is nonumeric, the text contains the name of a city, all vendors from that city will be returned .
  If parameter text is numeric one  vendor (whith this id wil retuned)   
  

-  Example Request: `curl http://farmers--market.herokuapp.com/vendors/rye`<br>

```json
       {
    "success": true,
    "vendors": [
        {
            "city": "rye",
            "id": 3,
            "name": "George",
            "phone": "0997755587",
            "ratings": null
        }
    ]
}
```

### DELETE /vendors/<id\>


- General:
  - Deletes a vendor whith id   from database.
  - Request Parameter(in URL): id

-  Example Request: `curl http://farmers--market.herokuapp.com/vendors/5 -X DELETE` <br>

```json
            {"success": "True",
            "deleted": 5
            }
```

### POST /vendors

  - Creates a new vendor to database
  - Request Body( payload): 
 

-  Example Request: `curl http://farmers--market.herokuapp.com/vendors -X POST -H "Content-Type: application/json" -d {
    "name": "Lucas Wees","address": "zzz no14","city": "rye","email": "lucas@farm.br","phone": "06985525587"}'` <br>

- Example Response:
```json
{
    "created": true
}
```

### PATCH '/vendors/<id\>'
        Updates the vendor where <id> is the existing vendor id
        Update the corresponding fields for vendor with id <vendor_id>. Usualy is us for update the raitings
- Example Request:
    curl --location --request PATCH 'http://farmers--market.herokuapp.com/vendors/1' \
        --header 'Content-Type: application/json' \
        --data-raw '{"ratings": "5"}' <br>
- Example Response:
```json
    {
                    "updated": "True",
                    "vendor": {
                            "name": "Lucas rex",
                            "address": "zzz no14",
                            "city": "rye",
                            "email": "lucas@farm.br",
                            "phone": "06985525587",
                            "ratings": "5"}
    }
```

### GET/products

- General: 
  - Returns all the products.

- Sample Request :  `curl http://farmers--market.herokuapp.com/products` <br>
- Sample Response
```json
  {
    "products": [
        {
            "id": 1,
            "name": "pepper"
        }
    ],
    "success": true
}
```

### GET /products/<text\>

  -  The text contains the name of a product, all products containing that name will be returned.
   

-  Example Request: `curl http://farmers--market.herokuapp.com/product/pepper` <br>
-  Example Response:
```json   
    "product": [
        {
            "id": 1,
            "name": "pepper"
        }
    ],
    "success": true
}
```

### DELETE /products/<id\>

- General:
  - Deletes a product whith id   from database.
  - Request Parameter(in URL): id

-  Example Request: 'curl http://farmers--market.herokuapp.com/products/5 -X DELETE` <br>

```json
            {"success": "True",
            "deleted": 5
            }
```

### POST /products

  - Creates a new product to database
  - Request Body( payload): 
 
-  Example Request: `curl http://farmers--market.herokuapp.com/products -X POST -H "Content-Type: application/json" -d '{"name": "tomates","category": "vegetabels","uom": "kg"}'` <br>

 - Example Response :
```json
{
    "created": true
}
```

### PATCH '/products/<id\>'
        Updates the product where <id> is the existing product id
        Update the corresponding fields for product with id <vendor_id>. 
- Example Request:
    `curl --location --request PATCH 'http://farmers--market.herokuapp.com/products/1' \
      --header 'Content-Type: application/json' \
        --data-raw '{"category": "fruit"}`
    
- Example Response:

```json
    {
          
                    "updated": "True",
                    "product": {"name": "tomates",
                              "category": "fruit",
                              "uom": "kg"}
    }
```


### GET/customers

- General: 
  - Returns all the customers.

- Example Request : `curl http://farmers--market.herokuapp.com/customers` <br>
- Example Response:
```json
   {
    "customers": [
        {
            "city": "Lin",
            "id": 1,
            "name": "Andrew rex",
            "phone": "047755587",
            "ratings": null
        },
        {
            "city": "London",
            "id": 2,
            "name": "George ",
            "phone": "04887755587",
            "ratings": null
        }],
        "success": true
    }
```

### GET /customers/<text\>

  - If parameter text is nonumeric, the text contains the name of a city, all customer from that city will be returned .
  If parameter text is numeric one  customer (whith this id wil retuned)   
  

-  Example Request: `curl http://farmers--market.herokuapp.com/customers/london`<br>
- Example Response:
```json
       {
    "success": true,
    "customers": [
        {
            "city": "london",
            "id": 3,
            "name": "George",
            "phone": "0997755587",
            "ratings": null
        }
    ]
}
```

#### DELETE /customers/<int:id\>


- General:
  - Deletes a customer whith id   from database.
  - Request Parameter(in URL): id

-  Example Request: `curl http://farmers--market.herokuapp.com/customers/5 -X DELETE`
- Example Response:
```json
            {"success": "True",
            "deleted": 5
            }
```

#### POST /customers

  - Creates a new customer to database
  - Request Body( payload): 
 
-  Example Request: `curl http://farmers--market.herokuapp.com/customers -X POST -H "Content-Type: application/json" -d '{
    "name": "Lucas Wees",
    "address": "zzz no14",
    "city": "London",
    "email": "lucas@farm.br",
    "phone": "06985525587"}'`

Example Response:
```json
{
    "created": true
}
```

### PATCH '/customers/<id\>'
        Updates the customer where <id> is the existing customer id
        Update the corresponding fields for customer with id <customer_id>. Usualy is us for update the raitings
    Example Request:
    curl --location --request PATCH 'http://farmers--market.herokuapp.com/customers/1' \
        --header 'Content-Type: application/json' \
        --data-raw '{"ratings": "5"}'
    Example Response:
```json
    {
                    "updated": "True",
                    "customer": {
                            "name": "Lucas rex",
                            "address": "zzz no14",
                            "city": "London",
                            "email": "lucas@farm.br",
                            "phone": "06985525587",
                            "ratings": "5"}
    }
```


### GET/sale_orders

- General: 
  - Returns all the sale_orders.

- Example Request :  `curl http://farmers--market.herokuapp.com/sale_orders`
- Example Response:
```json
   {
    "sale_orders": [
        {
            "id": 1,
            "product": 1,
            "qty_remain": 50,
            "ratings": null,
            "vendor": 1
        }
    ],
    "success": true
}
```

### GET /sale_orders/<text\>

  - The text contains the name of a product, all sale orders that contain products with the names in the text will be returned .
  
-  Example Request: `http://farmers--market.herokuapp.com/sale_orders/pepper`<br>
-  Example Response:
```json
  {
    "sale_order": [
        {
            "id": 1,
            "product": 1,
            "qty_remain": 50,
            "ratings": null,
            "vendor": 1
        }
    ],
    "success": true
}
```

### DELETE /sale_orders/<id\>


- General:
  - Deletes a sale order whith id from database.
  - Request Parameter(in URL): id

-  Example Request: `curl http://farmers--market.herokuapp.com/sale_orders/5 -X DELETE`
-  Example Response:
```json
            {"success": "True",
            "deleted": 5
            }
```

### POST /sale_orders

  - Creates a new sale order to database
  - Request Body( payload): 
 
-  Example Request: `curl http://farmers--market.herokuapp.com/sale_orders -X POST -H "Content-Type: application/json" -d '{
    {"vendor_id": 1,"product_id": 1,"qty": 50}'`
- Example Response:
```json
{
    "created": true
}
```

### PATCH '/sale_orders/<id>'
        Updates the sale order where <id> is the existing sale order id
        Update the corresponding fields for sale order with id <customer_id>. Usualy is us for update the raitings
    Example Request:
    curl --location --request PATCH 'http://farmers--market.herokuapp.com/customers/1' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "ratings": "5"
        }'
    Example Response:
```json
    {
          
                    "updated": "True",
                    "customer": {
                                "id": 1,
                                "product": 1,
                                "qty_remain": 50,
                                "vendor": 1,
                                "ratings": "5"}
    }
```

### GET/buy_orders

- General: 
  - Returns all the buy_orders.

- Example Request :  `curl http://farmers--market.herokuapp.com/buy_orders`
- Example Response:
```json
   {
    "buy_orders": [
        {
            "id": 1,
            "customer": 1,
            "product": 1,
            "shipping":false,
        }
    ],
    "success": true
}
```


### DELETE /buy_orders/<int:id\>


- General:
  - Deletes a buy order whith id from database.
  - Request Parameter(in URL): id

-  Example Request: `curl http://farmers--market.herokuapp.com/buy_orders/5 -X DELETE`
-  Example Response:
```json
            {"success": "True",
            "deleted": 5
            }
```

### POST /buy_orders

  - Creates a new buy order to database
  - Request Body( payload): 
 
-  Example Request: `curl http://farmers--market.herokuapp.com/buy_orders -X POST -H "Content-Type: application/json" -d '{
    {"customer_id": 1,"sale_order_id":1,"product_id": 1,"qty": 5}'`
- Example Response:
```json
{
    "created": true
}
```

### PATCH '/buy_orders/<id\>'
        Updates the buy order where <id> is the existing buy order id
        Update the corresponding fields for buy order with id <customer_id>. Usualy we update the payment, shipping, active fields
- Example Request:
    curl --location --request PATCH "http://farmers--market.herokuapp.com/buy_orders/1" \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "shipping": true
        }'
- Example Response:
```json
    {
          
                    "updated": "True",
                    "buy_order": {
                                "id": 1,
                                "customer": 1,
                                "product": 1,
                                "shipping":true,}
    }
```

## Testing


To deploy the tests : 
source test_run.sh and
python test_market.sh  