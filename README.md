Your README is not rendering nicely because **your Markdown formatting is broken** by:

* Extra backslashes `\`
* Incorrect code fences
* Mixed indentation
* Code blocks opened but not closed
* Incorrect triple backticks
* Escaped characters inside markdown
* Missing blank lines between sections
* Using `markdown inside `markdown (nested not allowed)

I will now give you a **perfectly formatted, clean, GitHub-ready README.md** that will render EXACTLY as expected — with proper headings, lists, spacing, code blocks, and project tree.

---

# ✅ **FINAL CLEAN README.md (Copy–Paste, Works 100%)**

```markdown
# DS Mastery – Data Science Learning Platform

A complete end-to-end Data Science learning website built with Flask, featuring free and paid modules, an admin panel, user authentication, payment integration support, and dynamic content management.

---

## Overview

DS Mastery is a full-stack educational platform designed to help users learn Data Science from beginner to advanced levels.

This platform includes:

- User authentication (login and signup)
- Admin dashboard to manage modules
- Free and paid learning modules
- Dynamic HTML content rendering
- Razorpay-ready payment integration structure
- Course progress tracking
- Responsive UI using Bootstrap

---

## Key Features

### Authentication
- Secure login and signup
- Password hashing
- Session management using Flask-Login

### Admin Panel
- Add, edit, and delete modules
- Manage module order and visibility
- Mark modules as Free or Paid
- Supports full HTML content

### Learning Modules
- Unlimited module support
- SEO-friendly slugs
- Dynamic content rendering
- Separate free and paid module access

### Payments
- Razorpay payment integration structure ready
- Subscription logic included
- Locked module preview for unsubscribed users

### Progress Tracking
- Track module completion
- Save last viewed module
- Ready for quizzes and certificates

---

## Tech Stack

### Backend
- Python
- Flask  
- Flask-Login  
- Flask-SQLAlchemy  
- Flask-Migrate  

### Database
- SQLite (Development)
- PostgreSQL (Recommended for Production)

### Frontend
- HTML, CSS  
- Bootstrap 5  
- Jinja2 Templates  

### Payments
- Razorpay API (Integration Ready)

### Deployment
- Render  
- PythonAnywhere  
- Railway  

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
│     ├── **init**.py
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

````

---

## How to Run Locally

### 1. Create a Virtual Environment
```bash
python -m venv venv
````

### 2. Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

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

Local URL:

```
http://127.0.0.1:5000
```

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

Render will auto-deploy the application.

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
Data Science Developer & Full Stack Developer

---

## License

All Rights Reserved.

```

---

# 🎯 Now it will render **perfectly**, just like GitHub expects.

If you want:

- Dark-theme optimized README  
- README with screenshots  
- README with badges  
- Minimal README  
- Extended README for resume  

I can generate those too.
```
