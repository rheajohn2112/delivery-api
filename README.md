# 🚚 Delivery Tracking API (Flask + JWT + SQLAlchemy)

A RESTful **Delivery Management API** built using **Flask**, **JWT Authentication**, and **SQLAlchemy**, designed to handle delivery tracking, user roles, and data management efficiently.  
This project demonstrates API design, database modeling, and secure authentication for both admin and user roles.

---

## 🌐 Live Demo

**Base URL:** [https://delivery-api-ce9q.onrender.com](https://delivery-api-ce9q.onrender.com)

You can visit this URL to confirm that the API is live.  
Protected endpoints (like `/delivery`) require JWT authentication and can be tested via **Postman**.

---

## ⚙️ Tech Stack

- **Backend:** Flask (Python)  
- **Database:** SQLite (via SQLAlchemy)  
- **Authentication:** JWT (Flask-JWT-Extended)  
- **Hosting:** Render  
- **Environment:** `.env` for secret key management  

---

## 🧩 Key Features

✅ Secure JWT-based authentication  
✅ Role-based access control (Admin vs User)  
✅ Full CRUD operations for delivery records  
✅ Query filtering and sorting using query parameters  
✅ SQLite persistence with SQLAlchemy ORM  
✅ Cloud deployment on Render  

---

## 🏗️ Project Setup (Local)

To run locally:

```bash
git clone https://github.com/rheajohn2112/delivery-api.git
cd delivery-api
pip install -r requirements.txt
python
>>> from api import db
>>> db.create_all()
exit()
python api.py
Your app should now be live on:
👉 http://127.0.0.1:5000/

## 🔑 Environment Variables (.env)

Create a .env file in your project root and add:

JWT_SECRET_KEY=your_secret_key_here

## 📂 Folder Structure
📦 delivery-api
├── api.py
├── requirements.txt
├── .env
├── instance/
│   └── data.db
└── .venv/

📍 API Endpoints
🏠 Root

GET /
Returns a message confirming API status.

{
  "message": "Delivery API is running successfully!"
}

👤 User Management
Register User

POST /register
Registers a new user (default role = user).

Body Example:

{
  "username": "john",
  "password": "12345",
  "role": "admin"
}


Response:

{
  "message": "User john added with role admin!"
}

Login User

POST /login
Authenticates a user and returns a JWT token.

Body Example:

{
  "username": "john",
  "password": "12345"
}


Response:

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR..."
}


Use this token in Postman:

Authorization: Bearer <your_access_token_here>

📦 Delivery Management

⚠️ All delivery endpoints require JWT authentication.
Admin role is required for POST, PUT, and DELETE.

Add Deliveries (Admin Only)

POST /delivery

Body Example:

[
  {
    "packageid": "P001",
    "client_name": "Alice",
    "origin": "Mumbai",
    "destination": "Bangalore",
    "status": "In Transit",
    "expected_delivery_date": "2025-11-15",
    "actual_delivery_date": null,
    "on_time": true
  }
]

Get All Deliveries

GET /delivery?status=Delivered&sort_by=client_name&sort_order=asc

Filters deliveries by query params.
Available filters: status, client_name, origin, destination, on_time.

Sorting parameters:

sort_by → any valid column name (e.g., client_name, status)

sort_order → asc or desc

Get Delivery by ID

GET /delivery/<id>

Example:
/delivery/1

Update Delivery (Admin Only)

PUT /delivery/<id>

Body Example:

{
  "status": "Delivered",
  "actual_delivery_date": "2025-11-10",
  "on_time": true
}

Delete Delivery (Admin Only)

DELETE /delivery/<id>

Deletes a delivery record by ID.

🧠 Example Usage Flow

1️⃣ Register a new admin user
2️⃣ Login to get a JWT access token
3️⃣ Use that token to:

Add new delivery records

Fetch and filter deliveries

Update or delete records as needed

🚀 Future Enhancements

Add pagination for large datasets

Add user profile management

Integrate external shipment tracking API

Include automated testing and CI/CD setup
