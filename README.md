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