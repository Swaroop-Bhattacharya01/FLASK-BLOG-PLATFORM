# 📝 Flask Blog Platform

A full-stack blog web application built using **Flask**, featuring user authentication, CRUD blog posts, profile management, and deployment on **Render**.

🔗 **Live Demo:**  
https://flask-blog-platform-1.onrender.com

🔗 **GitHub Repository:**  
https://github.com/Swaroop-Bhattacharya01/FLASK-BLOG-PLATFORM

---

## 🚀 Features

- User Registration & Login
- Secure Password Hashing (Flask-Bcrypt)
- User Sessions (Flask-Login)
- Create, Read, Update, Delete (CRUD) Blog Posts
- User Profiles with Profile Picture Upload
- Pagination for Blog Posts
- Deployed on Render using Gunicorn
- SQLite Database (SQLAlchemy ORM)

---

## ⚙️ Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS (Jinja2 Templates)
- **Database:** SQLite + SQLAlchemy
- **Authentication:** Flask-Login
- **Forms & Validation:** Flask-WTF
- **Password Security:** Flask-Bcrypt
- **Email Service:** Flask-Mail (SMTP)
- **Deployment:** Render
- **WSGI Server:** Gunicorn

---

## 📂 Project Structure

FLASK-BLOG-PLATFORM/
│
├── app/
│ ├── init.py
│ ├── routes.py
│ ├── models.py
│ ├── forms.py
│ ├── static/
│ │ ├── main.css
│ │ └── profile_pics/
│ └── templates/
│
├── run.py
├── requirements.txt
└── README.md

yaml
Copy code

---

## 🔐 Environment Variables

The following environment variables are required (configured on Render):

EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password
SECRET_KEY=your_secret_key

yaml
Copy code

---

## ❗ Known Limitation

### 🔴 Password Reset Email (Production)

- The **password reset feature works locally**, but  
- **Does NOT work on Render production deployment**

**Reason:**
Render’s free tier does not reliably support outbound SMTP connections to Gmail, which causes the email-sending process to time out.

**Impact:**
- Password reset requests result in a server error
- Core application functionality remains unaffected

✅ This limitation is documented intentionally and does not affect authentication, posting, or user management.

---

## 🛠️ Local Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/Swaroop-Bhattacharya01/FLASK-BLOG-PLATFORM.git
2.Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate 

3.Install dependencies

pip install -r requirements.txt

4.Run the application

python run.py
