# 📦 Installation Guide - Skill Swap Network

Complete step-by-step installation guide for the Skill Swap Network Django application.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package manager) - Usually comes with Python
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Virtual Environment** (recommended)

## 🚀 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/rr0h/skill-swap-network.git
cd skill-swap-network
```

### 2. Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt indicating the virtual environment is active.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 4.2.7
- Pillow (for image processing)
- python-decouple (for environment variables)
- django-crispy-forms & crispy-tailwind (for forms)
- django-widget-tweaks (for form widgets)

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
SECRET_KEY=your-secret-key-here-generate-a-new-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (Optional for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Generate a Secret Key:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Create Database and Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the SQLite database and all necessary tables.

### 6. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: admin (or your choice)
- Email: your-email@example.com
- Password: (enter a secure password)

### 7. Create Media Directories

```bash
mkdir media
mkdir media/profile_images
```

**Add a default profile image:**
Download or create a default profile image and save it as:
`media/profile_images/default.jpg`

### 8. Load Sample Data (Optional)

Create sample categories for testing:

```bash
python manage.py shell
```

Then run:

```python
from skills.models import Category

categories = [
    {'name': 'Programming', 'description': 'Software development and coding skills', 'icon': 'fa-code'},
    {'name': 'Design', 'description': 'Graphic design, UI/UX, and creative skills', 'icon': 'fa-palette'},
    {'name': 'Languages', 'description': 'Foreign language learning and teaching', 'icon': 'fa-language'},
    {'name': 'Music', 'description': 'Musical instruments and music theory', 'icon': 'fa-music'},
    {'name': 'Cooking', 'description': 'Culinary arts and cooking techniques', 'icon': 'fa-utensils'},
    {'name': 'Fitness', 'description': 'Physical fitness and wellness', 'icon': 'fa-dumbbell'},
    {'name': 'Photography', 'description': 'Photography and photo editing', 'icon': 'fa-camera'},
    {'name': 'Writing', 'description': 'Creative and technical writing', 'icon': 'fa-pen'},
]

for cat in categories:
    Category.objects.get_or_create(**cat)

print("Sample categories created!")
exit()
```

### 9. Run Development Server

```bash
python manage.py runserver
```

The application will be available at:
- **Main Site:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## 🎯 First Steps After Installation

### 1. Access Admin Panel

1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Explore the admin interface

### 2. Create Your First User Account

1. Go to http://127.0.0.1:8000/users/register/
2. Create a regular user account
3. Complete your profile

### 3. Add Skills and Categories

1. Login to admin panel
2. Add more categories if needed
3. Create some sample skills

### 4. Test the Application

- Browse skills
- Send skill requests
- Accept/reject requests
- Leave reviews
- Check notifications

## 🔧 Troubleshooting

### Issue: Module not found errors

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Database errors

**Solution:**
```bash
# Delete the database and start fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Static files not loading

**Solution:**
```bash
python manage.py collectstatic
```

### Issue: Image upload errors

**Solution:**
Ensure media directories exist:
```bash
mkdir -p media/profile_images
```

### Issue: Permission denied on Linux/Mac

**Solution:**
```bash
chmod +x manage.py
```

## 📱 Running in Production

For production deployment:

1. **Set DEBUG to False** in `.env`:
   ```env
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Use a production database** (PostgreSQL recommended):
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'skillswap_db',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

4. **Use a production server** (Gunicorn + Nginx):
   ```bash
   pip install gunicorn
   gunicorn skillswap.wsgi:application
   ```

5. **Set up HTTPS** with Let's Encrypt

6. **Configure email backend** for real email sending

## 🆘 Getting Help

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/rr0h/skill-swap-network/issues)
2. Review Django documentation
3. Check Python and Django versions
4. Ensure all dependencies are installed

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] Database migrations completed
- [ ] Superuser created
- [ ] Media directories created
- [ ] Development server running
- [ ] Can access admin panel
- [ ] Can create user accounts
- [ ] Can create and browse skills

## 🎉 Success!

If all steps completed successfully, you now have a fully functional Skill Swap Network running locally!

Next steps:
- Customize the design
- Add more features
- Deploy to production
- Share with users

---

**Need help?** Open an issue on GitHub or contact the development team.
