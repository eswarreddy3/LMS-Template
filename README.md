# Backend Setup & OTP Authentication – README

This document records everything done so far to build the backend foundation using **Django + DRF + JWT + OTP**.

---

## 1. Project Structure

```
Template/
│
├── venv/
├── requirements.txt
│
└── backend/
    ├── backend/
    │   ├── settings.py
    │   ├── urls.py
    │   └── ...
    │
    ├── api/
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── serializers.py
    │   ├── utils.py
    │   └── ...
    │
    └── manage.py
```

---

## 2. Virtual Environment Setup

### Create venv

```bash
python3 -m venv venv
```

### Activate venv

Linux / Mac:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## 3. Installed Packages

```bash
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install python-dotenv
pip install psycopg2-binary
pip install djangorestframework-simplejwt
pip install cloudinary
pip install pillow
```

---

## 4. requirements.txt

Created using:

```bash
pip freeze > requirements.txt
```

Purpose:

* Dependency tracking
* Deployment
* Environment recreation

---

## 5. Django Project Setup

```bash
django-admin startproject backend
cd backend
python3 manage.py startapp api
```

Run server:

```bash
python3 manage.py runserver
```

---

## 6. Default Migrations

```bash
python3 manage.py migrate
```

---

## 7. settings.py Configuration

### Installed Apps

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'api',
]
```

---

### Middleware

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]
```

---

### CORS

```python
CORS_ALLOW_ALL_ORIGINS = True
```

---

### DRF + JWT

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

---

## 8. Database Models

### User

* email
* phone
* is_verified
* created_at

### OTP

* user (FK)
* otp
* expires_at

### FormSubmission

* user (FK)
* name
* age
* resume_url
* image_url
* created_at

---

## 9. Migrations

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

---

## 10. API Routing

### App URLs

File: `api/urls.py`

### Project URLs

File: `backend/urls.py`

```python
path('api/', include('api.urls'))
```

---

## 11. OTP Utility Functions

File: `api/utils.py`

* generate_otp()
* get_expiry_time()

---

## 12. Auth APIs

### Send OTP

**POST** `/api/auth/send-otp/`

```json
{
  "email": "test@gmail.com"
}
```

---

### Verify OTP

**POST** `/api/auth/verify-otp/`

```json
{
  "email": "test@gmail.com",
  "otp": "123456"
}
```

Returns:

* Access token
* Refresh token

---

## 13. Current Features Working

* Django backend
* REST APIs
* CORS enabled
* JWT authentication
* OTP login system
* Database models
* Admin panel

---

## 14. Next Phase

* Resume upload
* Image upload
* Cloudinary integration
* JWT-protected form submission
* Ollama chatbot API

---

## 15. How to Run Project

```bash
source venv/bin/activate
cd backend
python3 manage.py runserver
```

---

Maintained by: Eswar
