# Up-Child-A-Child-Nurturing-support-system
Up-Child is a child development and nurturing support platform aimed at empowering parents and caregivers with tools for growth tracking, activity management, progress monitoring, and personalized child-care recommendations to foster holistic development.


🌟 Full-Stack Flask + React + MySQL + JWT + AI + Celery

🚀 A Complete Full-Stack Web Application with Authentication, Database, AI & Background Tasks
Built using Flask (Backend), React (Frontend), MySQL (Database), JWT (Auth), AI/ML Models, Celery (Tasks), Redis (Broker)

Explore Features » · Tech Stack · Backend Setup · Frontend Setup

       

✨ Features 🔥 Backend (Flask)

User Registration & Login

JWT Authentication

Protected API Routes

MySQL Database Integration

SQLAlchemy ORM

Secure Password Hashing

Admin/User Access

Test API & Health routes

⚛️ Frontend (React)

Login & Register pages

Protected routes using React Router

Dashboard page

Add Child form

View Child list

Axios for API calls

🧠 Machine Learning Integration

TensorFlow CPU

PyTorch

Transformers for NLP

Scikit-Learn

🎯 Background Jobs

Celery task runner

Redis as message broker

🔐 Security

JWT tokens

CORS protection

Sanitized SQL inputs

🚀 Deployment Ready

Gunicorn + Gevent workers

Production requirements.txt

Clean project structure

🧰 Tech Stack 🖥 Frontend



🔥 Backend


🤖 Machine Learning


⚙ Tools


📂 Project Structure Major Project/ │ ├── flask_app.py # Backend Flask app ├── requirements.txt # Python dependencies ├── .gitignore ├── README.md │ ├── frontend/ # React frontend │ ├── src/ │ ├── public/ │ ├── package.json │ └── node_modules/ (ignored) │ ├── venv/ (ignored) └── migrations/ (if using Flask-Migrate)
⚙️ Backend Setup (Flask) 1️⃣ Create & activate virtual environment python -m venv venv venv\Scripts\activate # Windows source venv/bin/activate # Mac/Linux

2️⃣ Install dependencies pip install -r requirements.txt

3️⃣ Setup MySQL Database

Login:

mysql -u root -p

Create DB:

CREATE DATABASE upchild_db;

4️⃣ Run Flask app python flask_app.py

Backend runs at: 👉 http://127.0.0.1:5000

⚛️ Frontend Setup (React)

Navigate into frontend folder:

cd frontend npm install npm start

Frontend runs at: 👉 http://localhost:3000

🔥 Example API Routes ✔ Test API GET /api/test

✔ Register POST /register { "name": "Abhigyan", "email": "sample@gmail.com", "password": "12345" }

✔ Login POST /login { "email": "sample@gmail.com", "password": "12345" }

✔ Protected Routes (JWT Required)

/profile

/add_child

/children

🧪 Testing pytest pytest --cov

🔐 Environment Variables

Create a .env file:

JWT_SECRET_KEY=super-secret-key DATABASE_URL=mysql+mysqlconnector://root:@localhost/upchild_db REDIS_URL=redis://localhost:6379
