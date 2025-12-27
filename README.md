# 🍔 AKA_UKA FAST-FOOD POS System

A premium, modern, and efficient Point of Sale (POS) system designed for fast-food restaurants. Built with Django and vanilla JavaScript, it features a sleek glassmorphism UI and real-time order management.

![POS Dashboard Screenshot](https://raw.githubusercontent.com/Komron0412/POS_system/main/media/readme/dashboard_preview.png) *(Placeholder: Update with actual screenshot after push)*

## ✨ Features

- **🚀 Real-time Dashboard**: Add items to orders instantly without page reloads.
- **🔍 Smart Search**: Real-time menu filtering to find items in milliseconds.
- **📱 Responsive Design**: Optimized for tablets, desktops, and mobile devices.
- **📑 Order Management**:
  - Daily sequence numbering (YYYYMMDD-XXXX).
  - Session-based concurrency (multiple cashiers/tabs support).
  - Automatic total calculations with high precision (Decimal support).
- **📊 Reporting**: End-of-day sales reports with status breakdowns (Completed, Pending, Cancelled).
- **🖨 Receipt Generation**: Clean, printable HTML receipts for customers.
- **🛡 Admin Panel**: Secure back-office for managing menu categories, items, and inventory.

## 🛠 Technology Stack

- **Backend**: Python 3.x, Django 4.2+
- **Database**: PostgreSQL (Production), SQLite (Testing/Dev)
- **Frontend**: HTML5, CSS3 (Custom Glassmorphism Design), Vanilla JavaScript
- **Deployment**: Docker, Nginx, Gunicorn

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Komron0412/POS_system.git
cd POS_system
```

### 2. Setup environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database Migration
```bash
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` to access the dashboard.

## 🐳 Docker Deployment

To deploy using Docker:

```bash
docker-compose up --build -d
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Komron** - [GitHub Profile](https://github.com/Komron0412)
