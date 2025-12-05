# ⚡ Quick Start Guide - Skill Swap Network

Get up and running with Skill Swap Network in 5 minutes!

## 🚀 Super Quick Setup

```bash
# 1. Clone the repository
git clone https://github.com/rr0h/skill-swap-network.git
cd skill-swap-network

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Create media directories
mkdir -p media/profile_images

# 8. Run server
python manage.py runserver
```

## 🎯 Access Points

- **Main Site:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Dashboard:** http://127.0.0.1:8000/dashboard/

## 📝 First Steps

### 1. Create Sample Categories

```bash
python manage.py shell
```

```python
from skills.models import Category

categories = [
    {'name': 'Programming', 'description': 'Software development', 'icon': 'fa-code'},
    {'name': 'Design', 'description': 'Graphic design', 'icon': 'fa-palette'},
    {'name': 'Languages', 'description': 'Foreign languages', 'icon': 'fa-language'},
    {'name': 'Music', 'description': 'Musical instruments', 'icon': 'fa-music'},
]

for cat in categories:
    Category.objects.get_or_create(**cat)

exit()
```

### 2. Create a Test User

1. Go to http://127.0.0.1:8000/users/register/
2. Fill in the registration form
3. Login with your credentials

### 3. Complete Your Profile

1. Click on your username in the navbar
2. Click "Settings"
3. Add profile picture, bio, location
4. Save changes

### 4. Add Your Skills

1. Go to "My Profile"
2. Click "Add Skill"
3. Choose skill type (Can Teach / Want to Learn)
4. Add skill name and proficiency level

### 5. Create a Skill Listing

1. Click "Add Skill" in the navbar dropdown
2. Fill in skill details:
   - Title
   - Description
   - Category
   - Level
   - Duration
   - Location preference
3. Submit

### 6. Browse and Request Skills

1. Go to "Browse Skills"
2. Use search and filters
3. Click on a skill to view details
4. Click "Request This Skill"
5. Write a message explaining why you want to learn
6. Submit request

### 7. Manage Requests

1. Go to "Requests" in navbar
2. View sent and received requests
3. Accept/reject incoming requests
4. Send messages within requests
5. Mark completed when done

### 8. Leave Reviews

1. After completing an exchange
2. Click "Mark as Completed"
3. Fill in the review form:
   - Overall rating (1-5 stars)
   - Communication rating
   - Knowledge rating
   - Patience rating
   - Written comment
4. Submit review

## 🎨 Customization

### Change Color Scheme

Edit `templates/base.html`:

```css
.gradient-bg {
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

### Add More Categories

```python
python manage.py shell

from skills.models import Category

Category.objects.create(
    name='Your Category',
    description='Category description',
    icon='fa-icon-name'
)
```

### Customize Email Templates

Edit files in `templates/users/`:
- `password_reset_email.html`
- `password_reset_confirm.html`

## 🔧 Common Tasks

### Reset Database

```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Collect Static Files

```bash
python manage.py collectstatic
```

### Create Sample Data

```bash
python manage.py shell

from django.contrib.auth import get_user_model
from skills.models import Skill, Category

User = get_user_model()

# Create test user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)

# Create test skill
category = Category.objects.first()
Skill.objects.create(
    title='Python Programming',
    description='Learn Python from basics to advanced',
    category=category,
    user=user,
    level='intermediate'
)
```

## 📊 View Statistics

### Admin Dashboard
1. Login to admin panel
2. View user, skill, request statistics
3. Monitor system activity

### User Dashboard
1. Login as regular user
2. Go to Dashboard
3. View personal statistics
4. Check activity charts

## 🐛 Troubleshooting

### Port Already in Use

```bash
python manage.py runserver 8001
```

### Static Files Not Loading

```bash
python manage.py collectstatic --clear
```

### Database Locked Error

```bash
# Close all connections and restart server
```

### Image Upload Errors

```bash
# Ensure media directory exists
mkdir -p media/profile_images

# Check permissions
chmod -R 755 media/
```

## 📚 Next Steps

1. ✅ Read [FEATURES.md](FEATURES.md) for complete feature list
2. ✅ Check [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) for database structure
3. ✅ Review [INSTALLATION.md](INSTALLATION.md) for detailed setup
4. ✅ Explore the admin panel
5. ✅ Customize the design
6. ✅ Add your own features
7. ✅ Deploy to production

## 🎉 You're Ready!

Your Skill Swap Network is now running! Start exchanging skills and building your community.

---

**Need Help?** Check the [README.md](README.md) or open an issue on GitHub.
