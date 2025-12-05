# 🎓 Skill Swap Network

A fully functional, aesthetically designed Skill Swap Network web application built with Django, SQLite, HTML, CSS, and JavaScript. Exchange skills with others, discover categories, send swap requests, and provide ratings.

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-38bdf8)

## ✨ Features

### 👤 User Management
- Secure signup, login, logout with Django authentication
- User profiles with image, bio, skills offered/wanted
- Password reset & email verification
- Profile completion progress tracking

### 🧠 Skill Management
- Post skills to teach or learn
- Search by keyword, category, location
- Detailed skill pages with ratings/reviews
- Skill recommendations based on interests

### 🗂️ Category System
- Dynamic category browsing
- Category-based skill filtering
- Visual category cards on dashboard

### 🔄 Skill Exchange Requests
- Send/receive skill swap requests
- Accept/reject functionality
- Track status: Pending, Accepted, Completed, Cancelled
- In-request messaging system

### ⭐ Ratings & Reviews
- 1-5 star rating system
- Written reviews after completion
- Aggregated ratings on profiles

### 📊 Dashboard
- Personalized recommendations
- Incoming/outgoing request tracking
- Activity visualizations with Chart.js
- Beautiful card-based design

### 🔔 Notifications
- Real-time notifications for requests
- Rating notifications
- Request status updates

### 🔒 Security
- CSRF protection
- Input validation & sanitization
- Role-based access control
- Secure password handling

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/rr0h/skill-swap-network.git
cd skill-swap-network
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

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Load sample data (optional)**
```bash
python manage.py loaddata sample_data.json
```

8. **Run development server**
```bash
python manage.py runserver
```

9. **Access the application**
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
skill-swap-network/
├── skillswap/              # Main project directory
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                  # User management app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── templates/
├── skills/                 # Skill management app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── templates/
├── requests/               # Request management app
│   ├── models.py
│   ├── views.py
│   └── templates/
├── reviews/                # Rating & review app
│   ├── models.py
│   ├── views.py
│   └── templates/
├── dashboard/              # Dashboard app
│   ├── views.py
│   └── templates/
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                  # User uploaded files
├── templates/              # Global templates
│   ├── base.html
│   └── navbar.html
├── manage.py
├── requirements.txt
└── README.md
```

## 🗄️ Database Schema

### Users
- Custom User model extending AbstractUser
- Profile fields: bio, profile_image, location
- Skills offered/wanted (ManyToMany)

### Skills
- Title, description, category
- User (ForeignKey)
- Created/updated timestamps
- Average rating

### Categories
- Name, description, icon
- Skill count

### Requests
- Sender, receiver (ForeignKey to User)
- Skill (ForeignKey)
- Status: Pending, Accepted, Completed, Cancelled
- Messages (related model)

### Reviews
- User (reviewer), skill, rating (1-5)
- Comment, timestamp

### Notifications
- User, message, type, read status
- Timestamp

## 🎨 UI/UX Design

- **Color Scheme**: Blue, purple, white gradients
- **Framework**: TailwindCSS
- **Icons**: FontAwesome
- **Charts**: Chart.js for analytics
- **Responsive**: Mobile-first design
- **Components**: Card-based layout with hover effects

## 🔧 Tech Stack

- **Backend**: Django 4.2, Django ORM
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: TailwindCSS
- **Database**: SQLite
- **Authentication**: Django Auth System
- **Image Processing**: Pillow
- **Charts**: Chart.js

## 📚 API Endpoints

### Authentication
- `/signup/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/password-reset/` - Password reset

### Skills
- `/skills/` - List all skills
- `/skills/create/` - Create new skill
- `/skills/<id>/` - Skill detail
- `/skills/<id>/edit/` - Edit skill
- `/skills/search/` - AJAX search

### Requests
- `/requests/` - List requests
- `/requests/send/<skill_id>/` - Send request
- `/requests/<id>/accept/` - Accept request
- `/requests/<id>/reject/` - Reject request
- `/requests/<id>/complete/` - Mark complete

### Reviews
- `/reviews/create/<request_id>/` - Create review
- `/reviews/<user_id>/` - User reviews

### Dashboard
- `/dashboard/` - Main dashboard
- `/dashboard/stats/` - User statistics

## 👨‍💼 Admin Panel

Access at `/admin/` with superuser credentials

**Features:**
- User management
- Category management
- Skill moderation
- Request monitoring
- Review management
- System statistics

## 🔐 Security Features

- CSRF tokens on all forms
- SQL injection protection (Django ORM)
- XSS prevention (template escaping)
- Secure password hashing (PBKDF2)
- Login required decorators
- Permission-based access control

## 📸 Screenshots

*(Screenshots will be added after deployment)*

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Rohit Raj**
- GitHub: [@rr0h](https://github.com/rr0h)

## 🙏 Acknowledgments

- Django Documentation
- TailwindCSS Team
- FontAwesome Icons
- Chart.js Library

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

⭐ **Star this repository if you find it helpful!**
