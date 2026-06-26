# 🏥 Patient Management System

A full-stack Patient Management System built using **FastAPI** for the backend and **Streamlit** for the frontend.

This project demonstrates CRUD operations, API development, and frontend-backend integration.

---

## 🚀 Features

* View all patients
* View a single patient
* Sort patients
* Create a new patient
* Update patient details
* Delete patients
* FastAPI backend
* Streamlit frontend
* JSON file used as the database

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

### Frontend

* Streamlit

### Database

* JSON

---

## 📂 Project Structure

```
Patient-Management-System
│
├── backend
│   ├── main.py
│   ├── patients.json
│
├── frontend
│   ├── frontend.py
│
├── screenshots
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Patient-Management-System.git
```

Move into the project

```bash
cd Patient-Management-System
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn backend.main:app --reload
```

Run Streamlit

```bash
streamlit run frontend/frontend.py
```

---

## API Endpoints

| Method | Endpoint       | Description      |
| ------ | -------------- | ---------------- |
| GET    | /              | Home             |
| GET    | /patients      | Get all patients |
| GET    | /patients/{id} | Get one patient  |
| POST   | /patients      | Create patient   |
| PUT    | /patients/{id} | Update patient   |
| DELETE | /patients/{id} | Delete patient   |

---

## Future Improvements

* PostgreSQL Database
* SQLAlchemy ORM
* JWT Authentication
* User Login & Signup
* Docker Support
* Cloud Deployment
* React Frontend

---

## Author

Priyanshi Jain
# Patient-Management-System-FastAPI
A full-stack Patient Management System built with FastAPI and Streamlit demonstrating CRUD operations, API development, and frontend-backend integration.
