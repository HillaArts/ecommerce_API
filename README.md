# This project is a simple ecommerce API built using Flask and MySQL, which provides endpoints for user management, product management, and order management. The API supports both admin and client roles with JWT-based authentication and authorization

Table of Contents
Features
Getting Started
API Endpoints
Models
Security
Technologies
Development
Testing
Deployment
Features
User Management: Admin and client user registration, login, and user management.
Product Management: Create, update, retrieve, and delete products.
Order Management: Place, retrieve, update, and delete orders.
JWT Authentication: Secure endpoints with JWT tokens.
Role-based Access Control: Different endpoints for admin and client users.
Getting Started
Prerequisites
Python 3.8+
MySQL database
Virtualenv or any environment management tool
Flask and required dependencies
Installation
Clone the repository:

bash
Copy code
git clone <https://github.com/HillaArts/ecommerce-api.git>
cd ecommerce-api
Create a virtual environment and activate it:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required  dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the database:

bash
Copy code
flask db init
flask db migrate
flask db upgrade
Run the application:

bash
Copy code
flask run
The API will be available at <http://localhost:5000>.

API Endpoints
Authentication Endpoints
Register Admin: POST /auth/register/admin
Register Client: POST /auth/register/client
Login Admin: POST /auth/login/admin
Login Client: POST /auth/login/client
Delete Admin: DELETE /auth/delete/admin/{user_id}
Delete Client: DELETE /auth/delete/client/{user_id}
List Admin Users: GET /auth/users/admin
List Client Users: GET /auth/users/client
Product Endpoints
Retrieve All Products: GET /products/
Create Product: POST /products/
Get Product Details: GET /products/{product_id}
Update Product: PUT /products/{product_id}
Delete Product: DELETE /products/{product_id}
Order Endpoints
Retrieve All Orders: GET /orders/
Place New Order: POST /orders/
Get Order Details: GET /orders/{order_id}
Update Order: PUT /orders/{order_id}
Delete Order: DELETE /orders/{order_id}
Models
Product
yaml
Copy code
Product:
  id: integer
  name: string
  description: string
  price: float
  stock: integer
  created_at: datetime
Order
yaml
Copy code
Order:
  id: integer
  user_id: integer
  total_price: float
  created_at: datetime
  status: string
  products: list of OrderProduct
OrderProduct
yaml
Copy code
OrderProduct:
  order_id: integer
  product_id: integer
  quantity: integer
  price_at_order: float
Security
The API uses JWT-based authentication. To access secured endpoints, you need to include the JWT token in the Authorization header as follows:

bash
Copy code
Authorization: Bearer <your_token_here>
Technologies
Flask: A lightweight WSGI web application framework.
MySQL: Relational database management system.
Flask-JWT-Extended: JWT support for Flask.
Swagger: API documentation.
Development
To run the development server:

bash
Copy code
flask run
To create new migrations:

bash
Copy code
flask db migrate -m "Migration message"
flask db upgrade
Testing
To run the tests:

bash
Copy code
pytest
Deployment
Deploy on Heroku
Create a new Heroku app:

bash
Copy code
heroku create your-app-name
Push the code to Heroku:

bash
Copy code
git push heroku main
Set up environment variables on Heroku:

bash
Copy code
heroku config:set FLASK_APP=run.py
heroku config:set FLASK_ENV=production
Access your application at <https://your-app-name.herokuapp.com>.

This README provides a detailed overview of the project, instructions for setup, and an outline of the available API endpoints based on the Swagger specification.
