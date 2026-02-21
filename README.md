# 💸 MiniVenmo: Social Payment System

A hybrid **Django/FastAPI** architecture for social payments. Features include user balance management, symmetric friendships, and a dynamic activity feed.

## 🏗 System Design
* **Django (Port 8000):** Main API, Database management, and Feed logic.
* **FastAPI (Port 8001):** High-precision payment microservice for balance/card processing.



## 🚀 Quick Start

### 1. Setup Environment
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Prepare database

python manage.py makemigrations
python manage.py migrate

### 3. Run Application

Open two terminals:

Terminal 1 (Microservice): uvicorn paymentMicroService:app --port 8001

Terminal 2 (Django API): python manage.py runserver


## 📄4.Testing

# Test Django Core (includes Feed and Payment logic)
python manage.py test

# Test FastAPI Microservice (precision and card validation)
pytest paymentMicroServiceTests.py

## 5. 📍 Key Endpoints

POST /api/users/ : Create user (user_name, balance)

POST /api/users/{id}/add_friend/ : Create mutual friendship

POST /api/payments/ : Execute payment logic

GET  /api/feed/ : View formatted activity feed (Paginated)