
# WorkForge — Freelance Marketplace

A Django-based platform where freelancers find work and employers post jobs.

## Features

- Register as a Freelancer or Employer
- Post, search and apply to jobs
- Freelancer & employer profiles with ratings and reviews
- Direct messaging between users
- Page view counter on employer profiles
- Django admin panel

## Tech Stack

- Python 3.14 / Django 6.0
- SQLite
- Pillow (avatar uploads)
- python-decouple (environment variables)

## How to Run

**1. Clone the repo**
```bash
git clone <your-repo-url>
cd forge-of-masterpieces
```

**2. Create and activate virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Apply migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Create a superuser**
```bash
python manage.py createsuperuser
```

**6. Run the server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000`
Admin panel: `http://127.0.0.1:8000/admin/`

## Running Tests
```bash
python manage.py test core
```
=======

# Freelance Marketplace﻿ forge-of-masterpieces

A Django web application for connecting freelancers and employers.

## Features
- Custom user model with roles
- Freelancer and employer profiles
- Registration and login
- Home page with statistics
- Freelancer, employer and job pages
- Admin panel support

## Technologies
- Python
- Django
- SQLite
- Bootstrap

## Installation
```bash
git clone <your-repo-link>
cd <repo-name>
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserve
```


## home page demo:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/cd5717e0-ed06-4e9a-a96f-07fb4b65e549" />


## Live demo: [https://your-app.onrender.com](https://forge-of-masterpieces.onrender.com/)

You can use the following test accounts to explore the application:

### Employer
- Username: test_employer
- Password: user12345

### Freelancer
- Username: test_freelancer
- Password: user12345
