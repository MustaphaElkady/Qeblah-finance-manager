# Media Finance Manager

A Streamlit-based internal system for media companies to manage clients, packages, contracts, payments, expenses, and profitability reports.

## Features
- Dashboard with key financial metrics
- Client management (add, edit, delete)
- Package management (add, edit, delete)
- Contract management (add, edit, delete)
- Payment tracking (add, edit, delete)
- Expense tracking (add, edit, delete)
- Reports with filters and CSV export
- Basic login protection
- Default package seeding

## Default Login
- Username: `admin`
- Password: `admin123`

You can override these in deployment using environment variables or Streamlit secrets:
- `APP_USERNAME`
- `APP_PASSWORD`

## Installation
```bash
pip install -r requirements.txt
```

## Run locally
```bash
streamlit run Home.py
```

## Seed default packages manually
```bash
python seed.py
```

## Notes
- The app uses SQLite by default for quick setup.
- For production or multi-user usage, PostgreSQL is recommended.
- Back up the database regularly if you are using SQLite.

## Main Files
- `Home.py` — dashboard
- `database.py` — database connection
- `models.py` — database models
- `services.py` — business logic and summaries
- `auth.py` — login logic
- `seed.py` — inserts default packages
- `pages/` — Streamlit pages
