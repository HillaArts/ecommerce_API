# E-Commerce API

Overview
The E-Commerce API is a RESTful API developed using Flask and MySQL. It provides a backend for managing products, users, and orders in an e-commerce application. The API supports user registration and authentication, product management, and order processing.

Features
User Management: Register new users, log in, and manage user accounts.
Product Management: Add, update, delete, and list products.
Order Management: Create, update, delete, and list orders.
JWT Authentication: Secure endpoints with JSON Web Token (JWT) authentication.
Error Handling: Comprehensive error handling for various scenarios.
Prerequisites
Python 3.8 or later
MySQL Server
pip for Python package management
Installation
Clone the Repository
bash
Copy code
git clone <https://github.com/HillaArts/ecommerce-api.git>
cd ecommerce-api
Create a Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies
bash
Copy code
pip install -r requirements.txt
Configure Environment Variables
Create a .env file in the root directory with the following content:

ini
Copy code
SECRET_KEY=your_secret_key
DATABASE_URI=mysql+mysqlconnector://username:password@localhost/ecommerce_db
JWT_SECRET_KEY=your_jwt_secret_key
Replace your_secret_key, username, password, and your_jwt_secret_key with your actual values.

Set Up the Database
Start MySQL Server if it's not running.

Create the Database:

sql
Copy code
CREATE DATABASE ecommerce_db;
Initialize and Migrate the Database:

bash
Copy code
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
Running the Application
To start the Flask development server:

bash
Copy code
export FLASK_APP=app
export FLASK_ENV=development
flask run
Alternatively, you can use Gunicorn for production:

bash
Copy code
gunicorn -w 4 -b 0.0.0.0:8000 app:create_app()
API Endpoints
User Endpoints
Register User

POST /register
Request Body: { "username": "string", "email": "string", "password": "string" }
Response: 201 Created if successful, 400 Bad Request if user already exists.
Login

POST /login
Request Body: { "email": "string", "password": "string" }
Response: 200 OK with JWT token if successful, 401 Unauthorized if credentials are invalid.
Product Endpoints
List Products

GET /products
Response: 200 OK with a list of products.
Create Product

POST /products
Request Body: { "name": "string", "description": "string", "price": number, "stock": number }
Response: 201 Created if successful.
Update Product

PUT /products/<product_id>
Request Body: { "name": "string", "description": "string", "price": number, "stock": number }
Response: 200 OK if successful.
Delete Product

DELETE /products/<product_id>
Response: 200 OK if successful.
Order Endpoints
List Orders

GET /orders
Response: 200 OK with a list of orders for the authenticated user.
Create Order

POST /orders
Request Body: { "total_price": number }
Response: 201 Created if successful.
Update Order

PUT /orders/<order_id>
Request Body: { "status": "string" }
Response: 200 OK if successful.
Delete Order

DELETE /orders/<order_id>
Response: 200 OK if successful.
Testing
To run the tests:

bash
Copy code
python -m unittest discover -s tests
Deployment
For production deployment:

Use a WSGI server like Gunicorn or uWSGI.
Set up a reverse proxy with Nginx or Apache.
Secure the application with HTTPS.
Ensure environment variables are set for configuration.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
If you’d like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

Replace placeholders like yourusername and your_secret_key with actual values specific to your project setup. Adjust the API endpoints and other sections based on any further modifications you make to the project.
