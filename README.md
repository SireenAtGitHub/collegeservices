# College Services API

A comprehensive Django REST API for managing college operations including students, subjects, semesters, and academic marks with teacher authentication and authorization.

## Project Overview

College Services API is a robust backend system designed to manage academic data in a college setting. It provides RESTful endpoints for managing students, subjects organized by semesters, marks/grades, and teacher authentication using JWT tokens.

## Features

- **Teacher Authentication**: JWT-based authentication for secure access to protected endpoints
- **Student Management**: Create, retrieve, and update student information
- **Subject Management**: Manage subjects with codes, descriptions, and semester associations
- **Semester Management**: Organize academic data by semesters with result publication status
- **Marks Tracking**: Record and manage student marks per subject
- **CORS Support**: Cross-Origin Resource Sharing enabled for frontend integration
- **Image Upload**: Support for subject icons/images via Pillow
- **Search Functionality**: Built-in search filters for students (by name and email)
- **Pagination & Filtering**: Query parameter-based filtering and retrieval

## Technology Stack

- **Framework**: Django 5.0.3
- **API**: Django REST Framework 3.15.0
- **Authentication**: Django REST Framework SimpleJWT
- **Database**: SQLite (development) / MySQL (via MySQLClient)
- **Python**: 3.x
- **Image Processing**: Pillow
- **CORS**: django-cors-headers
- **Server**: ASGI/WSGI compatible

## Project Structure

```
collegeservices/
├── api/                           # Main API app
│   ├── models.py                 # Data models (Semester, Student, Subject, Marks)
│   ├── views.py                  # API views and endpoints
│   ├── serializers.py            # DRF serializers for validation & serialization
│   ├── urls.py                   # API URL routing
│   ├── helpers.py                # Response helpers and constants
│   ├── tests.py                  # Test cases
│   ├── admin.py                  # Django admin configuration
│   ├── apps.py                   # App configuration
│   ├── migrations/               # 
│
├── collegeservices/              # Project settings & configuration
│   ├── settings.py               # Django settings (INSTALLED_APPS, middleware, etc.)
│   ├── urls.py                   # Main URL configuration
│   ├── asgi.py                   # ASGI application
│   ├── wsgi.py                   # WSGI application
├── media/                        # User uploaded files
│   └── images/                   # Subject icons and images
│
├── manage.py                     # Django management command
├── db.sqlite3                    # SQLite database
├── requirements.txt              # Python dependencies
├── run.ps1                       # PowerShell script to run server
├── mig.ps1                       # PowerShell script for migrations
└── README.md                     # This file
```

## Database Models

### Semester
```python
- id (Primary Key)
- name: CharField (max 50)
- result_published: BooleanField (default: False)
```

### Student
```python
- id (Primary Key)
- name: CharField (max 30)
- email: EmailField
- semester: ForeignKey → Semester
```

### Subject
```python
- id (Primary Key)
- name: CharField (max 100, min 5)
- code: CharField (max 10, unique, min 4)
- semester: ForeignKey → Semester
- description: TextField (max 450, optional)
- teacher: ForeignKey → User (nullable)
- image_icon: ImageField (optional)
```

### Marks
```python
- id (Primary Key)
- marks: PositiveIntegerField
- student: ForeignKey → Student
- subject: ForeignKey → Subject
```

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/teacher/login` | Login and get JWT tokens | None |
| POST | `/api/teacher/exists` | Check if teacher exists | None |

### Semesters
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/semester` | Get all semesters | None |
| GET | `/api/semester?id=<id>` | Get specific semester with subjects | None |

### Subjects
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/subject` | Get all subjects | None |
| GET | `/api/subject?code=<code>` | Get subject by code | None |
| POST | `/api/subject` | Create new subject | Authenticated |
| PATCH | `/api/subject` | Update subject | Authenticated |

### Students
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/student` | Get all students (searchable) | None |
| POST | `/api/student` | Create new student | Authenticated |
| PATCH | `/api/student` | Update student | Authenticated |
| DELETE | `/api/student` | Delete student(s) | Authenticated |

### Student Semester
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET/POST | `/api/student/semester` | Manage student semester | Authenticated |

### Marks
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET/POST | `/api/student/marks` | Get/Update student marks | Authenticated |

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Login Endpoint**: `/api/teacher/login`
   - Accepts `email` and `password`
   - Returns `access_token` and `refresh_token`

2. **Token Configuration**:
   - Access Token Lifetime: 5 hours
   - Refresh Token Lifetime: 1 day

3. **Usage**: Include the access token in the Authorization header:
   ```
   Authorization: Bearer <access_token>
   ```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment tool (venv)

### Step 1: Clone and Setup Environment

```powershell
# Navigate to project directory
cd e:\Repositories\collegeservices

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# If you encounter execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Environment Variables

Create a `.env` file in the project root with the following variables:

```
SECRET_KEY=your-secret-key-here
DEBUG_VALUE=True
DATABASE_URL=sqlite:///db.sqlite3
```

### Step 4: Database Migrations

```powershell
# Run migrations
python manage.py migrate

# Or use the migration script
.\mig.ps1
```

### Step 5: Create Superuser (Optional)

```powershell
python manage.py createsuperuser
```

### Step 6: Run Development Server

```powershell
# Using Python
python manage.py runserver

# Or use the provided script
.\run.ps1
```

The API will be available at: `http://127.0.0.1:8000/api/`

## Dependencies

See [requirements.txt](requirements.txt) for full list:

- **Django** 5.0.3 - Web framework
- **djangorestframework** 3.15.0 - REST API framework
- **djangorestframework-simplejwt** - JWT authentication
- **django-cors-headers** - CORS support
- **mysqlclient** 2.2.4 - MySQL database driver
- **Pillow** - Image processing
- **asgiref** 3.8.0 - ASGI utilities
- **sqlparse** 0.4.4 - SQL parsing

## ⚙️ Configuration

### Django Settings Overview

**INSTALLED_APPS**:
- Django core apps (admin, auth, contenttypes, sessions, messages, staticfiles)
- Third-party: corsheaders, rest_framework
- Project app: api

**REST Framework Settings**:
```python
DEFAULT_RENDERER_CLASSES: JSONRenderer
DEFAULT_AUTHENTICATION_CLASSES: JWTAuthentication
```

**CORS Configuration**: All origins allowed (`ALLOWED_HOSTS = ["*"]`)

**Database**: 
- Development: SQLite (db.sqlite3)
- Production: Configurable via DATABASE_URL

## Media Storage

- **Location**: `./media/images/`
- **Used for**: Subject icons and images
- **Accessible via**: API endpoints and static file serving

## 🛠️ Utility Scripts

### run.ps1
```powershell
python .\manage.py runserver
```
Starts the Django development server.

### mig.ps1
```powershell
# Typically runs: python manage.py migrate
```
Runs pending database migrations.

## 🔗 Integration Notes

- **CORS Enabled**: Safe for cross-origin requests from frontend applications
- **JWT Authentication**: Stateless authentication suitable for mobile and SPA applications
- **RESTful Design**: Standard RESTful conventions for all endpoints
- **Error Handling**: Comprehensive error messages and appropriate HTTP status codes

## Key Files

- [api/models.py](api/models.py) - Data models
- [api/views.py](api/views.py) - API views and business logic
- [api/serializers.py](api/serializers.py) - Data validation and serialization
- [api/helpers.py](api/helpers.py) - Helper functions and constants
- [collegeservices/settings.py](collegeservices/settings.py) - Django configuration
- [requirements.txt](requirements.txt) - Python dependencies

## Development Notes

- Debug mode configuration via `DEBUG_VALUE` environment variable
- Secret key should be stored securely in environment variables
- All uploaded images are stored in the `media/images/` directory
- Student search functionality supports filtering by name and email
- Permission framework ensures only authenticated users can modify data

---

**Last Updated**: March 2026
**Django Version**: 5.0.3
**Python Version**: 3.x
