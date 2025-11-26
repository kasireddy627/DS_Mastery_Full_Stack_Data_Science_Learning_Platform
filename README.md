# DS Mastery – Data Science Learning Platform

A complete end-to-end Data Science learning website built with Flask, featuring free and paid modules, an admin panel, user authentication, payment integration support, and dynamic content rendering.



## Overview

DS Mastery is a full-stack educational platform designed to help users learn Data Science from beginner to advanced levels.

This platform includes:

* User authentication (login and signup)
* Admin dashboard to manage modules
* Free and paid learning modules
* Dynamic HTML content rendering
* Razorpay-ready payment integration structure
* Course progress tracking
* Responsive UI using Bootstrap



## Key Features

### Authentication

* Secure login and signup
* Password hashing
* Session management using Flask-Login

### Admin Panel

* Add, edit, and delete modules
* Manage module order and visibility
* Mark modules as Free or Paid
* Supports full HTML content

### Learning Modules

* Unlimited module support
* SEO-friendly slugs
* Dynamic content rendering
* Separate free and paid access

### Payments

* Razorpay payment integration structure ready
* Subscription logic included
* Locked module preview for unsubscribed users

### Progress Tracking

* Track module completion
* Save last viewed module
* Extendable to quizzes and certificates

---

## Tech Stack

### Backend

* Python
* Flask
* Flask-Login
* Flask-SQLAlchemy
* Flask-Migrate

### Database

* SQLite (Development)
* PostgreSQL (Recommended for Production)

### Frontend

* HTML, CSS
* Bootstrap 5
* Jinja2 Templates

### Payments

* Razorpay API (Integration Ready)

### Deployment

* Render
* PythonAnywhere
* Railway

---

## Project Structure

```
project/
│── run.py
│── config.py
│── requirements.txt
│── README.md
│── instance/
│     └── app.db
│
├── app/
│     ├── __init__.py
│     ├── main.py
│     ├── admin_ui.py
│     ├── auth.py
│     ├── models.py
│     ├── payments.py
│
│     ├── templates/
│     │     ├── base.html
│     │     ├── home.html
│     │     ├── module.html
│     │     ├── locked_module.html
│     │     ├── admin/
│     │     └── auth/
│
│     └── static/
│           ├── css/
│           ├── js/
│           └── images/
│
└── migrations/
```

---

## How to Run Locally

### 1. Create a Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

If migrations exist:

```bash
flask db upgrade
```

If starting fresh:

```bash
flask db init
flask db migrate
flask db upgrade
```

### 5. Run the Application

```bash
flask run
```

App URL:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Deployment (Render)

1. Push project to GitHub
2. Create a Web Service on Render
3. Build Command:

```bash
pip install -r requirements.txt
```

4. Start Command:

```bash
gunicorn run:app
```

---

## Future Enhancements

* Interactive quizzes
* Certificate generation
* Student analytics dashboard
* Notebook execution support
* MLOps pipeline module
* Recommendation engine

---

## Author

Kambalapalle Kasi Reddy
Data Science Developer and Full Stack Developer

---

## License

All Rights Reserved.
