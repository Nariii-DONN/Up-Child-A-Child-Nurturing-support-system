🌟 Full-Stack Flask + React + MySQL + JWT + AI + Celery
<!-- PROJECT BANNER --> <p align="center"> <img src="https://dummyimage.com/900x220/000/fff&text=Full+Stack+Flask+%2B+React+Project" alt="Project Banner"> </p> <h2 align="center">🚀 A Complete Full-Stack Web Application with Authentication, Database, AI & Background Tasks</h2> <p align="center"> <b>Built using Flask (Backend), React (Frontend), MySQL (Database), JWT (Auth), AI/ML Models, Celery (Tasks), Redis (Broker)</b> <br /><br /> <a href="#✨-features"><strong>Explore Features »</strong></a> · <a href="#🧰-tech-stack">Tech Stack</a> · <a href="#⚙️-backend-setup-flask">Backend Setup</a> · <a href="#⚛️-frontend-setup-react">Frontend Setup</a> </p> <!-- BADGES --> <p align="center"> <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" /> <img src="https://img.shields.io/badge/Flask-3.x-black?logo=flask" /> <img src="https://img.shields.io/badge/React-18-blue?logo=react" /> <img src="https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql" /> <img src="https://img.shields.io/badge/Node.js-20-green?logo=node.js" /> <img src="https://img.shields.io/badge/JWT-Secured-success?logo=jsonwebtokens" /> <img src="https://img.shields.io/badge/Celery-Async-yellowgreen?logo=celery" /> <img src="https://img.shields.io/badge/Project-Active-brightgreen" /> </p>
✨ Features
🔥 Backend (Flask)

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

🧰 Tech Stack
🖥 Frontend
<p> <img src="https://skillicons.dev/icons?i=react,js,html,css,bootstrap" /> </p>
🔥 Backend
<p> <img src="https://skillicons.dev/icons?i=python,flask,mysql,redis" /> </p>
🤖 Machine Learning
<p> <img src="https://skillicons.dev/icons?i=tensorflow,pytorch" /> </p>
⚙ Tools
<p> <img src="https://skillicons.dev/icons?i=git,github,postman,vscode" /> </p>
📂 Project Structure
Major Project/
│
├── flask_app.py               # Backend Flask app
├── requirements.txt           # Python dependencies
├── .gitignore
├── README.md
│
├── frontend/                  # React frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── node_modules/ (ignored)
│
├── venv/ (ignored)
└── migrations/  (if using Flask-Migrate)

⚙️ Backend Setup (Flask)
1️⃣ Create & activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Setup MySQL Database

Login:

mysql -u root -p


Create DB:

CREATE DATABASE upchild_db;

4️⃣ Run Flask app
python flask_app.py


Backend runs at:
👉 http://127.0.0.1:5000

⚛️ Frontend Setup (React)

Navigate into frontend folder:

cd frontend
npm install
npm start


Frontend runs at:
👉 http://localhost:3000

🔥 Example API Routes
✔ Test API
GET /api/test

✔ Register
POST /register
{
  "name": "Abhigyan",
  "email": "sample@gmail.com",
  "password": "12345"
}

✔ Login
POST /login
{
  "email": "sample@gmail.com",
  "password": "12345"
}

✔ Protected Routes (JWT Required)

/profile

/add_child

/children

🧪 Testing
pytest
pytest --cov

🔐 Environment Variables

Create a .env file:

JWT_SECRET_KEY=super-secret-key
DATABASE_URL=mysql+mysqlconnector://root:<password>@localhost/upchild_db
REDIS_URL=redis://localhost:6379