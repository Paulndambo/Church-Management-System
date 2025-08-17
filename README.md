# Church Management System

A modern, comprehensive church management system built with Django, featuring an elegant and intuitive user interface designed specifically for church administration needs.

![Church Management System](https://img.shields.io/badge/Church-Management%20System-blue)
![Django](https://img.shields.io/badge/Django-4.2+-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)

## 🎯 Overview

The Church Management System is a full-featured web application designed to help churches manage their operations efficiently. From member management to financial tracking, attendance monitoring to project coordination, this system provides all the tools needed for modern church administration.

## ✨ Key Features

### 👥 Member Management
- **Member Registration**: Complete member profiles with contact information
- **Department Assignment**: Organize members into departments and branches
- **Status Tracking**: Monitor member activity and engagement
- **Search & Filter**: Advanced search capabilities with real-time filtering

### 💰 Financial Management
- **Offerings Tracking**: Record and manage church offerings
- **Tithing Management**: Track member tithes and contributions
- **Expense Management**: Monitor church expenses and budgets
- **Department Savings**: Manage savings for different departments

### 🏗️ Project Management
- **Project Creation**: Plan and track church projects
- **Contribution Tracking**: Monitor project contributions and pledges
- **Progress Monitoring**: Visual progress indicators and goal tracking
- **Budget Management**: Track project budgets and expenditures

### 📊 Attendance & Services
- **Service Management**: Schedule and manage church services
- **Attendance Tracking**: Monitor member attendance
- **Visitor Registration**: Register and track visitors
- **Reports & Analytics**: Generate attendance reports and insights

### 🏢 Department Management
- **Department Organization**: Create and manage church departments
- **Leadership Structure**: Assign department leaders and roles
- **Activity Tracking**: Monitor department activities and events
- **Resource Allocation**: Manage department resources and budgets

## 🎨 UI/UX Improvements

### Modern Design System
- **Professional Aesthetics**: Church-appropriate design with deep blue and gold color scheme
- **Typography**: Inter for UI elements, Playfair Display for headings
- **Consistent Spacing**: 12px border radius for cards, 8px for smaller elements
- **Smooth Animations**: 0.3s cubic-bezier transitions throughout

### Enhanced Dashboard
- **Welcome Header**: Personalized greeting with current date
- **Statistics Cards**: 4-column layout with progress bars and trend indicators
- **Interactive Charts**: Chart.js integration with church-themed colors
- **Quick Actions**: Easy access to common tasks with hover effects

### Improved Navigation
- **Modern Sidebar**: Clean organization with collapsible sections
- **Better Icons**: Consistent Font Awesome icons throughout
- **Mobile Responsive**: Hamburger menu with smooth transitions
- **Active States**: Clear indication of current page

### Table Redesign
- **Modern Tables**: Clean headers with sortable columns
- **Avatar System**: Circular initials for member identification
- **Enhanced Search**: Real-time search with loading indicators
- **Better Pagination**: Modern controls with page information

### Mobile Responsiveness
- **Mobile-First Design**: Optimized for all screen sizes
- **Touch-Friendly**: Proper touch targets and gestures
- **Responsive Grid**: Bootstrap grid with custom breakpoints
- **Performance**: Optimized loading and rendering

### Accessibility Features
- **WCAG Compliance**: Meets AA accessibility standards
- **Keyboard Navigation**: Logical tab order and focus indicators
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **Color Independence**: Information not conveyed by color alone

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/church-management-system.git
   cd church-management-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
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

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Login with your superuser credentials

## 📁 Project Structure

```
ChurchSystem/
├── apps/                    # Django applications
│   ├── core/               # Core functionality
│   ├── membership/         # Member management
│   ├── payments/           # Financial management
│   ├── projects/           # Project management
│   ├── users/              # User management
│   └── events/             # Event management
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Dashboard
│   ├── members/           # Member templates
│   ├── offerings/         # Offering templates
│   └── projects/          # Project templates
├── static/                # Static files (CSS, JS, images)
├── ChurchSystem/          # Django project settings
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🛠️ Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
The system uses SQLite by default. For production, consider using PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'church_db',
        'USER': 'church_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📊 Features in Detail

### Dashboard Analytics
- **Member Statistics**: Total members, new registrations, active members
- **Financial Overview**: Total offerings, tithes, expenses, savings
- **Project Progress**: Contribution tracking, goal completion
- **Attendance Trends**: Weekly attendance charts and patterns

### Member Management
- **Profile Management**: Complete member profiles with photos
- **Department Assignment**: Organize members by departments
- **Status Tracking**: Active, inactive, visitor status
- **Communication**: Email and SMS integration

### Financial Tracking
- **Offerings**: Daily, weekly, monthly offering records
- **Tithing**: Member tithe tracking and reports
- **Expenses**: Church expense management and categorization
- **Reports**: Financial reports and analytics

### Project Management
- **Project Planning**: Create and manage church projects
- **Contribution Tracking**: Monitor donations and pledges
- **Progress Monitoring**: Visual progress indicators
- **Budget Management**: Track project budgets and expenditures

## 🎨 Customization

### Theme Customization
The system uses CSS custom properties for easy theming:

```css
:root {
    --church-primary: #1a365d;      /* Primary blue */
    --church-gold: #d69e2e;         /* Accent gold */
    --church-secondary: #2d3748;    /* Secondary blue */
    --church-gray: #718096;         /* Text gray */
}
```

### Adding New Features
1. Create a new Django app: `python manage.py startapp new_feature`
2. Add the app to `INSTALLED_APPS` in settings.py
3. Create models, views, and templates
4. Add URL patterns to the main urls.py

## 🔧 Development

### Running Tests
```bash
python manage.py test
```

### Code Style
The project follows PEP 8 guidelines. Use a linter like `flake8`:

```bash
pip install flake8
flake8 .
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in settings
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure HTTPS
5. Set up environment variables

### Docker Deployment
```bash
# Build the image
docker build -t church-management-system .

# Run the container
docker run -p 8000:8000 church-management-system
```

## 📱 Mobile Support

The system is fully responsive and optimized for mobile devices:
- **Touch-friendly interface**: Proper touch targets and gestures
- **Mobile navigation**: Collapsible sidebar for mobile devices
- **Responsive tables**: Horizontal scrolling for data tables
- **Optimized forms**: Mobile-friendly form inputs and buttons

## 🔒 Security Features

- **User Authentication**: Secure login system
- **Permission Management**: Role-based access control
- **Data Validation**: Input validation and sanitization
- **CSRF Protection**: Cross-site request forgery protection
- **SQL Injection Prevention**: Parameterized queries

## 📈 Performance

- **Optimized Queries**: Efficient database queries
- **Caching**: Smart caching for frequently accessed data
- **Static File Optimization**: Minified CSS and JavaScript
- **Image Optimization**: Responsive images with proper sizing
- **Lazy Loading**: Efficient content loading

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new features
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure mobile responsiveness

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [User Guide](docs/user-guide.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)

### Getting Help
- **Issues**: Report bugs and request features on GitHub
- **Discussions**: Join community discussions
- **Email**: Contact support at support@churchsystem.com

## 🙏 Acknowledgments

- **Django Team**: For the excellent web framework
- **Bootstrap Team**: For the responsive CSS framework
- **Font Awesome**: For the beautiful icons
- **Chart.js**: For the interactive charts
- **Community Contributors**: For their valuable feedback and contributions

## 📊 System Requirements

### Minimum Requirements
- **Python**: 3.8+
- **RAM**: 512MB
- **Storage**: 1GB
- **Browser**: Chrome 80+, Firefox 75+, Safari 13+, Edge 80+

### Recommended Requirements
- **Python**: 3.9+
- **RAM**: 2GB+
- **Storage**: 5GB+
- **Database**: PostgreSQL 12+

## 🔄 Version History

### v2.0.0 (Current)
- ✨ Complete UI/UX redesign
- 📱 Enhanced mobile responsiveness
- ♿ Improved accessibility
- 🚀 Performance optimizations
- 🎨 Modern design system

### v1.0.0
- 🎉 Initial release
- 👥 Basic member management
- 💰 Financial tracking
- 📊 Simple reporting

---

**Built with ❤️ for churches worldwide**

For more information, visit our [website](https://churchsystem.com) or contact us at info@churchsystem.com.
