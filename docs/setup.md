# Project Setup

This guide walks you through installing and running the UK Tech Insights project locally for development or testing.

---

## 1. Requirements

- Python 3.12+
- PostgreSQL
- Poetry (or alternatively pip & virtualenv)

---

## 2. Clone the Repository

```bash
git clone https://github.com/yourusername/uk-tech-insights.git
cd uk-tech-insights
```

## 3. Create a Virtual Environment

```bash
poetry install
poetry shell
```

Or using pip:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Configure the Environment

```bash
cp .env.example .env
```

**File:** `.env.example`

```makefile
SECRET_KEY=
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=uktech
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
NEWS_API_KEY=
```

## 5. Prepare the Database

```bash
python manage.py makemigrations
python manage.py migrate
```

```bash
python manage.py createsuperuser
```

## 6. Run the Development Server

```bash
python manage.py runserver
```

## 8. Populating the Database

You can manually add data via the Django admin panel at /admin/ or fetch external news data using the instructions in [news](apps/news.md).
