# Ethara HQ | Team Task Manager

A hyper-modern, dynamic Team Task Management dashboard built for the web. This project utilizes a robust backend powered by **FastAPI** and **SQLAlchemy**, and a sleek, dynamic frontend driven by **HTMX** and **Tailwind CSS**. It provides an SPA-like experience without the heavy JavaScript frameworks.

## 🚀 Tech Stack

### Backend
* **FastAPI:** High-performance web framework.
* **SQLAlchemy 2.0:** Object Relational Mapper for database interactions.
* **Passlib / Bcrypt:** Secure password hashing.
* **JOSE:** JSON Web Token (JWT) encoding and decoding for secure authentication.

### Frontend
* **Jinja2:** Server-side template rendering.
* **HTMX:** Allows access to AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML.
* **Tailwind CSS:** Utility-first CSS framework for rapid UI development, featuring a custom, hyper-modern light theme with glassmorphism effects.

## ✨ Key Features

1. **Secure Authentication:** Stateless JWT authentication stored safely inside `HttpOnly` cookies to mitigate XSS attacks.
2. **Role-Based Access Control (RBAC):** Two tiers of users: `Command Staff` (Admins) and `Standard Operatives` (Members).
   * Admins can create projects, assign tasks, delete members, and update pinned notes.
   * Members can view tasks, update their task statuses, and view project parameters.
3. **Dynamic Dashboard:** A rich, interactive dashboard with KPI analytics, recent activity feeds, and dedicated scrollable modules.
4. **Interactive Task Matrix:** Real-time task status updates powered by HTMX, preventing full page reloads.

## 🛠️ Local Setup & Installation

### 1. Clone the Repository
Ensure you have Python 3.10+ installed on your system.
```bash
git clone <repository-url>
cd team-task-manager
```

### 2. Set Up Virtual Environment
Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install "fastapi[all]" sqlalchemy passlib bcrypt python-jose python-multipart jinja2 psycopg2-binary
```
*(Note: If you are running locally without Postgres, SQLite is used by default.)*

### 4. Seed the Database
Populate the database with dummy data, projects, and users:
```bash
python seed_db.py
```
> **Note:** The seed script creates an Admin account (`admin@ethara.ai`) and several member accounts. The password for all seeded accounts is **`pass`**.

### 5. Run the Server
Start the Uvicorn ASGI server:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Access the Application
Open your browser and navigate to: [http://localhost:8000](http://localhost:8000)

## 🚢 Deployment (Railway)

This application is strictly configured for deployment on **Railway.app**. 
1. Create a PostgreSQL database on Railway.
2. Link your GitHub repository.
3. The platform will automatically read the `Procfile` and use the built-in `config.py` logic to adapt the `DATABASE_URL` (converting `postgres://` to `postgresql://`).
4. Set the `SECRET_KEY` environment variable in your Railway project settings.
