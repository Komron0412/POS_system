# POS System (Fast Food Management)

A Django-based POS system for fast food restaurants.

## Features
- Categories & Menu Items
- Orders & Combos
- Real-time order status
- Total calculation
- PostgreSQL support

## Setup

```bash
git clone <your-repo-url>
cd POS_system
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Run the project
python manage.py migrate
python manage.py runserver
