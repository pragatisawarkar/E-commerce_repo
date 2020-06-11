'''

1)create customer
	POST----http://127.0.0.1:8000/customer_create

2)create vendor

  POST---- http://127.0.0.1:8000/vendor_create

3) customer login
   POST-----http://127.0.0.1:8000/customer_login

4) vendor login
   POST-----http://127.0.0.1:8000/vendor_login

5) user_role_create---customer

   POST----http://127.0.0.1:8000/user_role_create

6) user_role_create---vendor

  POST----http://127.0.0.1:8000/user_role_create

7) product_create

   POST----http://127.0.0.1:8000/product_create
   header--- [{"key":"Authorization","value":"Token 21e307744188a0952758a93c1e2d6765e258d703",}]

8)place_order

POST - ---http: // 127.0.0.1:8000/accept_order

header - -- [{"key": "Authorization", "value": "Token 21e307744188a0952758a93c1e2d6765e258d703", }]

'''''
