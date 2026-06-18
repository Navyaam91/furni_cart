# 🛒 Furni Cart — Multi-Vendor E-Commerce Platform

A full-stack multi-vendor e-commerce platform built with Python and Django, featuring secure authentication, role-based access control, payment integration, and cloud media storage.

🔗 **Live Demo**: [View Live](https://furni-cart.onrender.com/)  
💻 **GitHub**: [View Code](https://github.com/Navyaam91/furni_cart)

---

## Features

### Customer
- User registration and secure login
- Browse and search products by keyword
- Filter products by category
- Add to cart and place orders
- Secure online payment via Razorpay

### Seller
- Seller dashboard with inventory management
- Add, edit, and soft-delete products
- Real-time stock tracking
- View and manage incoming orders

### Admin
- Full control over users, sellers, and products
- Monitor all orders and transactions
- Role-based access management

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| Database | PostgreSQL |
| Frontend | JavaScript, Bootstrap |
| Payment | Razorpay API |
| Media Storage | Cloudinary |
| Version Control | Git, GitHub |

---

## Project Structure

```
furni_cart/
├── accounts/        # User authentication and role management
├── products/        # Product listings, categories, filtering
├── cart/            # Cart and order management
├── sellers/         # Seller dashboard and inventory
├── payments/        # Razorpay integration
├── templates/       # HTML templates
├── static/          # CSS, JS, images
└── furni_cart/      # Project settings and URLs
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL
- Razorpay account (for payments)
- Cloudinary account (for media storage)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/furni-cart.git
cd furni-cart
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/furnicart
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run the development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---


## What I Learned

- Building multi-vendor architecture with role-based access in Django
- Integrating third-party payment gateway (Razorpay)
- Managing cloud media storage with Cloudinary
- Designing normalized PostgreSQL database schema
- Implementing soft-delete logic for inventory management

---


---

## License

This project is open source and available under the [MIT License](LICENSE).
