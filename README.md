```markdown

\# DS Mastery – Data Science Learning Platform  

A complete end-to-end Data Science learning website built with Flask, featuring free and paid modules, an admin panel, user authentication, payment integration, and dynamic content management.







\## Overview  

DS Mastery is a full-stack educational platform designed to teach Data Science from beginner basics to advanced MLOps.  

The platform includes:



\- User authentication (login and signup)

\- Admin dashboard to manage modules

\- Free and paid learning modules

\- Razorpay-ready payment integration

\- Rich HTML content rendering

\- Course progress tracking

\- Responsive UI using Bootstrap







\## Key Features  



\### Authentication  

\- Secure login and signup  

\- Password hashing  

\- Session management using Flask-Login  



\### Admin Panel  

\- Add, edit, and delete modules  

\- Manage module order and visibility  

\- Mark modules as free or paid  

\- Rich text (HTML) content support  



\### Learning Modules  

\- Unlimited modules support  

\- SEO-friendly slugs  

\- Dynamic rendering of module content  

\- Separate paid and free access handling  



\### Payments  

\- Razorpay integration structure ready  

\- Subscription logic included  

\- Locked module preview for non-subscribers  



\### Progress Tracking  

\- Track module completion  

\- Save last viewed module  

\- Ready for quizzes and certificates  







\## Tech Stack  



\*\*Backend:\*\*  

\- Python  

\- Flask  

\- Flask-Login  

\- Flask-SQLAlchemy  

\- Flask-Migrate  



\*\*Database:\*\*  

\- SQLite (development)  

\- PostgreSQL recommended for production  



\*\*Frontend:\*\*  

\- HTML, CSS  

\- Bootstrap 5  

\- Jinja2 Templates  



\*\*Payments:\*\*  

\- Razorpay API (integration ready)



\*\*Deployment:\*\*  

\- Render, PythonAnywhere, Railway







\## Project Structure  



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

│     ├── \*\*init\*\*.py

│     ├── main.py

│     ├── admin\_ui.py

│     ├── auth.py

│     ├── models.py

│     ├── payments.py

│     │

│     ├── templates/

│     │     ├── base.html

│     │     ├── home.html

│     │     ├── module.html

│     │     ├── admin/

│     │     └── auth/

│     │

│     └── static/

│           ├── css/

│           ├── js/

│           └── images/

│

└── migrations/



````







\## How to Run Locally  



\### 1. Create a Virtual Environment  

```bash

python -m venv venv

````



\### 2. Activate Environment



Windows:



```bash

venv\\Scripts\\activate

```



Mac/Linux:



```bash

source venv/bin/activate

```



\### 3. Install Dependencies



```bash

pip install -r requirements.txt

```



\### 4. Initialize Database



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



\### 5. Start Application



```bash

flask run

```



Application runs at:



```

http://127.0.0.1:5000

```







\## Deployment (Render)



1\. Push project to GitHub

2\. Create a new Web Service on Render

3\. Build Command:



```bash

pip install -r requirements.txt

```



4\. Start Command:



```bash

gunicorn run:app

```



Render will automatically configure the environment.







\## Future Enhancements



\* Interactive quizzes

\* Certificate generation

\* Student dashboard

\* Notebook execution support

\* MLOps pipeline module

\* Recommendation engine







\## Author



Kambalapalle Kasi Reddy

Data Science Developer and Full Stack Developer







\## License



All Rights Reserved



```markdown

