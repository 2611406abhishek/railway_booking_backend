# Railway Booking Backend

This repository contains the backend code for a **Railway Booking System** similar to IRCTC. The system allows users to register, login, book train tickets, and check seat availability. Admins can manage trains through secure APIs.

## 🚀 Features
- **User Registration & Login** with Token Authentication
- **Role-Based Access:** Admin and Regular Users
- **Train Management (CRUD Operations)** for Admins
- **Seat Booking** with Race Condition Handling
- **Check Seat Availability**
- **Booking Details for Users**

---

## ⚙️ Tech Stack
- **Backend Framework:** Django Rest Framework (DRF)
- **Database:** PostgreSQL
- **Authentication:** Token-Based

---

## 🗂️ Project Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/2611406abhishek/railway_booking_backend.git
cd railway_booking_backend
```

### 2️⃣ Create & Activate Virtual Environment
```bash
python -m venv env
source env/bin/activate   # For Linux/Mac
# OR
env\Scripts\activate      # For Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure PostgreSQL Database
Make sure PostgreSQL is installed and running.

Update `settings.py` with your PostgreSQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway_db',        # Database name
        'USER': 'postgres',          # PostgreSQL user
        'PASSWORD': 'your_password', # PostgreSQL password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7️⃣ Run the Server
```bash
python manage.py runserver
```

Server will run at: **http://127.0.0.1:8000/**

---

## 🔐 API Documentation

### User APIs

#### ✅ **Register User**
- **Endpoint:** `POST /api/register/`
- **Request Body:**
```json
{
    "username": "john",
    "password": "johnspassword",
    "email": "john@example.com"
}
```

#### 🔑 **Login User**
- **Endpoint:** `POST /api/login/`
- **Request Body:**
```json
{
    "username": "john",
    "password": "johnspassword"
}
```
- **Response:** Returns an **Authentication Token**

---

### Admin APIs *(Require Token + API Key)*
- **Headers:**
  - `Authorization: Token <admin_token>`
  - `X-API-KEY: mysecretadminkey`

#### 🚄 **Add Train**
- **Endpoint:** `POST /api/admin/trains/`
- **Request Body:**
```json
{
    "train_number": "TRAIN124",
    "source": "CityA",
    "destination": "CityB",
    "total_seats": 100,
    "available_seats": 100
}
```

#### 📋 **List Trains**
- **Endpoint:** `GET /api/admin/trains/`

#### ✏️ **Update Train**
- **Endpoint:** `PUT /api/admin/trains/{id}/`
- **Request Body:**
```json
{
    "train_number": "TRAIN123",
    "source": "CityA",
    "destination": "CityB",
    "total_seats": 110
}
```

#### ❌ **Delete Train**
- **Endpoint:** `DELETE /api/admin/trains/{id}/`

---

### Booking APIs

#### 📊 **Get Seat Availability**
- **Endpoint:** `GET /api/trains/?source=CityA&destination=CityB`

#### 🎟️ **Book Seat**
- **Endpoint:** `POST /api/bookings/`
- **Request Body:**
```json
{
  "train_id": 1
}
```

#### 📄 **Get Booking Details**
- **Endpoint:** `GET /api/bookings/{id}/`

---

## 🔐 Security
- **Admin Endpoints:** Require both `Token` and `X-API-KEY`
- **User Endpoints:** Require `Token` only
- **Concurrency Handling:** Atomic transactions with row-level locking during seat booking

---

## 🙌 Contributing
1. Fork this repository
2. Create your feature branch (`git checkout -b feature-xyz`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-xyz`)
5. Open a pull request

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).

---

## 📧 Contact
For queries, feel free to reach out at: [your_email@example.com]

