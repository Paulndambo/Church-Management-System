# Church Management System

A comprehensive Django-based web application designed to help churches manage their operations, members, finances, and events efficiently.

## 🏛️ Overview

The Church Management System is a modern, user-friendly web application that provides churches with tools to manage various aspects of their operations. Built with Django and featuring a clean, responsive interface, this system helps church administrators streamline their daily tasks and maintain organized records.

## ✨ Features

### 👥 Member Management
- **Member Registration & Profiles**: Complete member information management
- **Branch Management**: Multi-branch church support with location tracking
- **Visitor Tracking**: Record and manage church visitors
- **Service Attendance**: Track member attendance at church services

### 💰 Financial Management
- **Tithes & Offerings**: Record and track member tithes and offerings
- **Department Savings**: Manage savings for different church departments
- **Expense Tracking**: Monitor church expenses and budgets
- **Financial Reports**: Generate comprehensive financial reports

### 🏗️ Project Management
- **Project Creation**: Plan and organize church projects
- **Pledge Management**: Track member pledges and contributions
- **Contribution Tracking**: Monitor project contributions
- **Project Status**: Track project completion status

### 📅 Event Management
- **Event Planning**: Create and manage church events
- **Service Scheduling**: Organize church services and schedules
- **Event Registration**: Handle event registrations and attendance

### 👤 User Management
- **Role-based Access**: Different access levels for administrators and users
- **User Authentication**: Secure login and user management
- **Profile Management**: User profile customization

## 🛠️ Technology Stack

- **Backend**: Django 5.1.x
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Custom responsive design
- **Deployment**: Docker support included

## 🚀 Installation

### Prerequisites
- Python 3.10+
- pip (Python package installer)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ChurchSystem
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # On Windows (cmd)
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - App: `http://127.0.0.1:8000`
   - Admin: `http://127.0.0.1:8000/admin`

### Quickstart
- Default login URL is `http://127.0.0.1:8000/users/login/`
- A custom user model is used: `users.User`
- Static files are served from `templates` and `static` during development; for production, configure a proper static files backend and run `python manage.py collectstatic`

### Docker Setup

1. **Build the image**
   ```bash
   docker build -t church-system .
   ```

2. **Apply migrations in the container**
   ```bash
   docker run --rm church-system python manage.py migrate
   ```

3. **Run the application**
   ```bash
   docker run -p 8000:8000 church-system
   ```

4. **Access the app**
   - `http://localhost:8000`

> Note: The provided Dockerfile runs the Django development server. For production, use a WSGI server (e.g., Gunicorn) behind a reverse proxy and configure persistent storage for the database and static/media files.

## 📁 Project Structure

```
ChurchSystem/
├── apps/                    # Django applications
│   ├── core/               # Core functionality & landing pages
│   ├── users/              # Custom user model & auth
│   ├── membership/         # Members, branches, visitors
│   ├── payments/           # Tithes, offerings, department savings
│   ├── projects/           # Projects, pledges, contributions
│   ├── events/             # Events, tickets, registrations
│   ├── districts/          # District/section/branch admin
│   ├── sections/           # Sections and reports
│   ├── attendances/        # Service attendance tracking
│   ├── partners/           # Partner management
│   ├── reports/            # Reporting
│   ├── finances/           # Expenses and accounts
│   ├── scheduling/         # Appointments and meetings
│   └── countries/          # Countries reference data
├── ChurchSystem/           # Main project settings
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
└── README.md               # This file
```

## 🔗 Base URLs
These routes are registered in `ChurchSystem/urls.py`:
- `/` → `apps.core`
- `/admin/` → Django Admin
- `/users/` → `apps.users`
- `/membership/` → `apps.membership`
- `/payments/` → `apps.payments`
- `/projects/` → `apps.projects`
- `/partners/` → `apps.partners`
- `/reports/` → `apps.reports`
- `/districts/` → `apps.districts`
- `/attendances/` → `apps.attendances`
- `/notifications/` → `apps.notifications`
- `/sections/` → `apps.sections`
- `/events/` → `apps.events`
- `/finances/` → `apps.finances`
- `/scheduling/` → `apps.scheduling`

## 🎨 UI Design

The application features a modern, clean interface with a carefully chosen color palette:
- **Primary**: Navy Blue (#2C3E50)
- **Secondary**: Soft Green (#81C784)
- **Accent**: Gold (#FFC107)
- **Background**: Off-White (#FAFAFA)
- **Text**: Charcoal (#333333)
- **Secondary Buttons**: Light Gray (#EEEEEE)

## 🔧 Configuration

### Environment Variables
For production, configure the following environment variables in your hosting platform and update `ChurchSystem/settings.py` or use a dedicated settings module:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgres://user:password@host:5432/dbname
```

### Database Configuration
The system uses SQLite by default for development (`db.sqlite3`). For production, switch to PostgreSQL and configure credentials in `ChurchSystem/settings.py` or through your chosen configuration approach:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📊 Usage Guide

### For Administrators
1. **Member Management**: Add, edit, and manage church members
2. **Financial Tracking**: Record tithes, offerings, and expenses
3. **Project Oversight**: Create and monitor church projects
4. **Event Planning**: Organize church events and services
5. **Reports**: Generate comprehensive reports for decision-making

### For Members
1. **Profile Management**: Update personal information
2. **Financial Records**: View personal tithe and offering history
3. **Project Participation**: Contribute to church projects
4. **Event Registration**: Register for church events

## 🔒 Security Features

- **CSRF Protection**: Built-in Django CSRF protection
- **Authentication**: Secure user authentication system
- **Authorization**: Role-based access control
- **Data Validation**: Comprehensive input validation
- **SQL Injection Protection**: Django ORM protection

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📈 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in settings or environment
- [ ] Configure production database
- [ ] Set up static file serving (e.g., WhiteNoise, CDN, or web server)
- [ ] Configure HTTPS/SSL
- [ ] Set up proper logging
- [ ] Configure backups and monitoring

### Recommended Hosting Platforms
- **DigitalOcean**: VPS with full control
- **AWS/GCP/Azure**: Scalable cloud infrastructure
- **Heroku/Fly.io/Render**: Simple PaaS deployments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0**: Initial release with core functionality
- Member management
- Financial tracking
- Project management
- Event planning
- User authentication

## 🙏 Acknowledgments

- Django community for the excellent framework
- Contributors and testers
- Church communities for feedback and suggestions


**Built with ❤️ for church communities worldwide**
