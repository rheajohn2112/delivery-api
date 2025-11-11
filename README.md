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
