# Project Management System

A full-stack project management application built with FastAPI (Python) backend and React (Vite) frontend. This system allows users to manage projects and tasks with role-based access control, email notifications, and a modern drag-and-drop Kanban board interface.

## 🚀 Features

- **User Authentication & Authorization**: JWT-based authentication with role-based access (Admin/User)
- **Project Management**: Create, update, delete, and list projects with pagination and search
- **Task Management**: Assign tasks to users with status tracking (To Do, In Progress, Done)
- **Kanban Board**: Drag-and-drop interface for task management
- **Email Notifications**: Automated emails for task assignments and status updates
- **User Management**: List all users with role identification for task assignment
- **Real-time Updates**: React Query for optimistic updates and cache management
- **Responsive Design**: Modern UI built with Tailwind CSS

---

## 📋 Table of Contents

1. [Tech Stack](#tech-stack)
2. [Architecture Overview](#architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Setup Instructions](#setup-instructions)
5. [Environment Variables](#environment-variables)
6. [Database Migrations](#database-migrations)
7. [Running the Application](#running-the-application)
8. [Create Admin User](#create-admin-user) ⭐
9. [API Documentation](#api-documentation)
10. [Project Structure](#project-structure)

---

## 🛠 Tech Stack

### Backend
- **FastAPI** (v0.120.4) - Modern, fast web framework for building APIs
- **SQLAlchemy** (v2.0.36) - SQL toolkit and ORM
- **Alembic** (v1.14.0) - Database migration tool
- **PostgreSQL** - Primary database (via psycopg2-binary)
- **Pydantic** (v2.12.3) - Data validation using Python type annotations
- **Python-JOSE** - JWT token creation and validation
- **Bcrypt** - Password hashing
- **FastAPI-Mail** - Email service integration
- **Uvicorn** - ASGI server

### Frontend
- **React** (v19.1.1) - UI library
- **Vite** (v7.1.7) - Build tool and dev server
- **React Router DOM** (v6.22.3) - Client-side routing
- **Redux Toolkit** (v2.2.1) - State management
- **React Query** (v5.28.4) - Data fetching and caching
- **Axios** (v1.6.8) - HTTP client
- **Tailwind CSS** (v3.4.1) - Utility-first CSS framework
- **@hello-pangea/dnd** (v16.6.0) - Drag and drop for Kanban board
- **React Hot Toast** (v2.4.1) - Toast notifications
- **React Icons** (v5.0.1) - Icon library

---

## 🏗 Architecture Overview

### Backend Architecture

```
Server/
├── app/
│   ├── core/           # Core configuration and utilities
│   │   ├── config.py   # Environment configuration
│   │   ├── database.py # Database connection and session
│   │   ├── security.py # JWT and password hashing
│   │   ├── logger.py   # Logging configuration
│   │   └── email.py    # Email configuration
│   ├── models/         # SQLAlchemy ORM models
│   │   ├── user.py     # User model (auth + roles)
│   │   ├── project.py  # Project model
│   │   └── task.py     # Task model
│   ├── schemas/        # Pydantic schemas (request/response)
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── task.py
│   │   └── common.py
│   ├── routers/        # API route handlers
│   │   ├── auth.py     # Authentication endpoints
│   │   ├── projects.py # Project CRUD endpoints
│   │   └── task.py     # Task CRUD endpoints
│   ├── services/       # Business logic and external services
│   │   └── email_service.py
│   ├── templates/      # Email templates (Jinja2)
│   ├── dependencies.py # Dependency injection (auth, roles)
│   └── main.py        # FastAPI application entry point
├── alembic/           # Database migrations
└── requirements.txt   # Python dependencies
```

### Frontend Architecture

```
client/
├── src/
│   ├── components/    # Reusable React components
│   │   ├── ui/        # Base UI components (Button, Input, Modal, etc.)
│   │   ├── layout/    # Layout components (Navbar, Sidebar, Dashboard)
│   │   ├── tasks/     # Task-specific components (TaskCard, TaskModal)
│   │   ├── projects/  # Project-specific components
│   │   └── kanban/    # Kanban board components
│   ├── pages/         # Route pages
│   │   ├── auth/      # Login and Register pages
│   │   ├── dashboards/# Admin and User dashboards
│   │   └── ...
│   ├── services/      # API service layer
│   │   ├── api.js     # Axios instance with interceptors
│   │   ├── authService.js
│   │   ├── projectService.js
│   │   └── taskService.js
│   ├── store/         # Redux store
│   │   └── slices/    # Redux slices (auth, projects, tasks)
│   ├── utils/         # Utility functions and constants
│   └── main.jsx       # Application entry point
└── package.json
```

### Key Design Decisions

1. **JWT Authentication**: Token-based authentication for stateless API
2. **Role-Based Access Control**: Admin and User roles with middleware-level enforcement
3. **Background Tasks**: Async email sending to avoid blocking API responses
4. **React Query**: Efficient data fetching, caching, and synchronization
5. **Optimistic Updates**: Immediate UI updates with automatic rollback on failure
6. **Component-Based Architecture**: Reusable, maintainable React components
7. **Service Layer Pattern**: Separation of API calls from components
8. **Database Migrations**: Alembic for version-controlled schema changes

---

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+**
- **Node.js 18+** and **npm/yarn**
- **PostgreSQL 14+**
- **Git**

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project-management
```

### 2. Backend Setup

#### a. Create Virtual Environment

```bash
cd Server
python -m venv fastapi
```

#### b. Activate Virtual Environment

**Windows:**
```bash
fastapi\Scripts\activate
```

**macOS/Linux:**
```bash
source fastapi/bin/activate
```

#### c. Install Dependencies

```bash
pip install -r requirements.txt
```

#### d. Configure Environment Variables

Create a `.env` file in the `Server` directory:

```bash
# Server/.env
DATABASE_URL=postgresql://username:password@localhost:5432/project_management
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=600

# Email Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# Frontend URL (for CORS)
CLIENT_URL=http://localhost:5173
```

> **Note**: For Gmail, you need to create an [App Password](https://support.google.com/accounts/answer/185833) instead of using your regular password.

### 3. Frontend Setup

#### a. Navigate to Client Directory

```bash
cd ../client
```

#### b. Install Dependencies

```bash
npm install
# or
yarn install
```

#### c. Configure Environment Variables

Create a `.env` file in the `client` directory:

```bash
# client/.env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🗄 Environment Variables

### Backend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/dbname` |
| `SECRET_KEY` | JWT secret key (use strong random string) | `your-secret-key-here` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes | `600` |
| `MAIL_USERNAME` | SMTP email username | `your-email@gmail.com` |
| `MAIL_PASSWORD` | SMTP email password/app password | `your-app-password` |
| `MAIL_FROM` | Email sender address | `your-email@gmail.com` |
| `MAIL_SERVER` | SMTP server address | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP server port | `587` |
| `CLIENT_URL` | Frontend URL for CORS | `http://localhost:5173` |

### Frontend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000` |

---

## 🔄 Database Migrations

### Create Database

First, create a PostgreSQL database:

```sql
CREATE DATABASE project_management;
```

### Run Migrations

```bash
cd Server
alembic upgrade head
```

### Create New Migration (if needed)

```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Database Schema

The application uses three main tables:

- **users**: User accounts with authentication and role information
- **projects**: Projects created by admin users
- **tasks**: Tasks assigned to users within projects

---

## 🚀 Running the Application

### Start Backend Server

```bash
cd Server
# Make sure virtual environment is activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API Documentation (Swagger UI): `http://localhost:8000/docs`

### Start Frontend Development Server

```bash
cd client
npm run dev
# or
yarn dev
```

The frontend will be available at: `http://localhost:5173`

---

## 👤 Create Admin User

### Using CLI Management Tool (Recommended)

The project includes a professional CLI management tool for user administration.

#### Available Commands

```bash
# Navigate to Server directory
cd Server

# Create a new admin user (interactive)
python manage.py create-admin

# List all users
python manage.py list-users

# Change user role (promote user to admin or demote admin to user)
python manage.py change-role

# Show help
python manage.py help
```

#### Creating Your First Admin

**Development:**
```bash
cd Server
python manage.py create-admin
```

You'll be prompted for:
- Email address (validated format)
- Full name (3-100 characters)
- Password (must meet security requirements)
- Password confirmation

**Production Deployment:**
```bash
# SSH into production server
ssh user@your-server.com

# Navigate to project
cd /path/to/project-management/Server

# Activate virtual environment
source fastapi/bin/activate

# Create admin user
python manage.py create-admin
```

#### Password Requirements

The system enforces strong password policies:
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter (A-Z)
- ✅ At least one lowercase letter (a-z)
- ✅ At least one number (0-9)
- ✅ At least one special character (!@#$%^&*(),.?":{}|<>)

**Example Valid Password:** `Admin@2024Pass`

#### Example CLI Usage

```bash
$ python manage.py create-admin

============================================================
CREATE ADMIN USER
============================================================

Admin email: admin@company.com
Full name: System Administrator
Password: ********
Confirm password: ********

⏳ Creating admin user...

============================================================
✅ ADMIN USER CREATED SUCCESSFULLY!
============================================================
ID:         1
Email:      admin@company.com
Name:       System Administrator
Role:       admin
Created:    2024-01-01 10:30:00
============================================================
```

#### List All Users

```bash
$ python manage.py list-users

================================================================================
ALL USERS
================================================================================

ID    Email                              Name                      Role       Active
--------------------------------------------------------------------------------
1     admin@company.com                  System Administrator      admin      Yes
2     john@example.com                   John Doe                  user       Yes
3     jane@example.com                   Jane Smith                user       Yes
--------------------------------------------------------------------------------
Total users: 3
```

#### Promote User to Admin

```bash
$ python manage.py change-role

============================================================
CHANGE USER ROLE
============================================================

Enter user email or ID: john@example.com

📋 Current User Info:
   ID:    2
   Email: john@example.com
   Name:  John Doe
   Role:  user

Available roles: admin, user
Enter new role (current: user): admin

Change role from 'user' to 'admin'? (y/n): y

✅ User role updated successfully!
   john@example.com is now an 'admin'
```

### Alternative Methods

#### Option 1: Manual Database Update (Not Recommended)

If you absolutely need to manually update the database:

```bash
# Connect to database
psql -U username -d project_management

# Update user role
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
```

⚠️ **Warning**: Manual database updates bypass validation and logging. Use CLI tool instead.

#### Option 2: First User Auto-Admin

For development convenience, you can modify the registration endpoint to make the first user an admin automatically (not recommended for production):

```python
# In Server/app/routers/auth.py (for development only)
user_count = db.query(User).count()
role = "admin" if user_count == 0 else "user"
```

---

## 🔐 Admin User Best Practices

### For Development
1. Create admin using CLI: `python manage.py create-admin`
2. Use strong passwords even in development
3. Don't commit admin credentials to version control

### For Production
1. **Initial Setup**: 
   - SSH into production server
   - Run `python manage.py create-admin`
   - Use environment-specific strong password

2. **Credential Management**:
   - Store credentials in password manager (1Password, LastPass, etc.)
   - Share with client through encrypted channels
   - Force password change on first login

3. **Security**:
   - Use unique passwords for each environment
   - Enable 2FA if implemented
   - Regularly audit admin accounts: `python manage.py list-users`
   - Remove unused admin accounts

4. **Handover to Client**:
   - Create initial admin account
   - Provide credentials securely (encrypted email, password manager)
   - Client logs in and changes password immediately
   - Client can promote other users via CLI or create additional admins

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}

Response: 200 OK
{
  "success": true,
  "data": {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00"
  },
  "message": "User registered successfully"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}

Response: 200 OK
{
  "success": true,
  "data": {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  },
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer {token}

Response: 200 OK
{
  "success": true,
  "data": {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

#### Get All Users
```http
GET /api/auth/users
Authorization: Bearer {token}

Response: 200 OK
{
  "success": true,
  "data": [
    {
      "id": 1,
      "full_name": "John Doe",
      "email": "john@example.com",
      "role": "user",
      "is_active": true
    },
    {
      "id": 2,
      "full_name": "Admin User",
      "email": "admin@example.com",
      "role": "admin",
      "is_active": true
    }
  ],
  "message": "Users fetched successfully"
}
```

---

### Project Endpoints

#### Create Project (Admin Only)
```http
POST /api/project/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "New Website Project",
  "description": "Build a modern website with React and FastAPI"
}

Response: 200 OK
{
  "id": 1,
  "title": "New Website Project",
  "description": "Build a modern website with React and FastAPI",
  "created_by": 2,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### List Projects
```http
GET /api/project/?page=1&size=10&search=website&created_by=2
Authorization: Bearer {token}

Query Parameters:
- page: Page number (default: 1)
- size: Items per page (default: 10, max: 100)
- search: Search in title and description (optional)
- created_by: Filter by creator user ID (optional)

Response: 200 OK
{
  "success": true,
  "data": {
    "projects": [
      {
        "id": 1,
        "title": "New Website Project",
        "description": "Build a modern website",
        "created_by": 2,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
        "task_count": 5
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10,
    "total_pages": 1
  }
}
```

#### Get Project by ID
```http
GET /api/project/{project_id}
Authorization: Bearer {token}

Response: 200 OK
{
  "success": true,
  "data": {
    "id": 1,
    "title": "New Website Project",
    "description": "Build a modern website",
    "created_by": 2,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "tasks": [
      {
        "id": 1,
        "title": "Design homepage",
        "status": "todo",
        "assigned_to": 1
      }
    ]
  }
}
```

#### Update Project (Admin Only)
```http
PATCH /api/project/{project_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Updated Project Title",
  "description": "Updated description"
}

Response: 200 OK
{
  "id": 1,
  "title": "Updated Project Title",
  "description": "Updated description",
  "created_by": 2,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

#### Delete Project (Admin Only)
```http
DELETE /api/project/{project_id}
Authorization: Bearer {token}

Response: 200 OK
{
  "success": true,
  "data": null,
  "message": "Project deleted successfully"
}
```

---

### Task Endpoints

#### Create Task
```http
POST /api/task/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Design homepage",
  "description": "Create wireframes and mockups",
  "project_id": 1,
  "assigned_to": 3,
  "status": "todo",
  "due_date": "2024-12-31"
}

Response: 200 OK
{
  "id": 1,
  "title": "Design homepage",
  "description": "Create wireframes and mockups",
  "project_id": 1,
  "assigned_to": 3,
  "status": "todo",
  "due_date": "2024-12-31T00:00:00",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}

Note: Sends email notification to assigned user
```

#### List All Tasks
```http
GET /api/task/?page=1&size=10&search=design&status=todo&project_id=1&assigned_to=3
Authorization: Bearer {token}

Query Parameters:
- page: Page number (default: 1)
- size: Items per page (default: 10, max: 100)
- search: Search in title and description (optional)
- status: Filter by status (todo, in-progress, done) (optional)
- project_id: Filter by project ID (optional)
- assigned_to: Filter by assigned user ID (optional)

Response: 200 OK
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 1,
        "title": "Design homepage",
        "description": "Create wireframes and mockups",
        "project_id": 1,
        "assigned_to": 3,
        "status": "todo",
        "due_date": "2024-12-31T00:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10,
    "total_pages": 1
  }
}
```

#### Get Assigned Tasks (Current User)
```http
GET /api/task/assigned?page=1&size=10&status=todo
Authorization: Bearer {token}

Query Parameters:
- page: Page number (default: 1)
- size: Items per page (default: 10, max: 100)
- status: Filter by status (optional)

Response: 200 OK
{
  "success": true,
  "data": {
    "tasks": [...],
    "total": 5,
    "page": 1,
    "size": 10,
    "total_pages": 1
  }
}
```

#### Get Task by ID
```http
GET /api/task/{task_id}
Authorization: Bearer {token}

Response: 200 OK
{
  "id": 1,
  "title": "Design homepage",
  "description": "Create wireframes and mockups",
  "project_id": 1,
  "assigned_to": 3,
  "status": "todo",
  "due_date": "2024-12-31T00:00:00",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}

Note: Users can only view tasks assigned to them (admins can view all)
```

#### Update Task
```http
PATCH /api/task/{task_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Updated task title",
  "status": "in-progress",
  "due_date": "2024-12-25"
}

Response: 200 OK
{
  "id": 1,
  "title": "Updated task title",
  "status": "in-progress",
  "due_date": "2024-12-25T00:00:00",
  ...
}

Note: Status changes trigger email notifications to project creator
```

#### Delete Task
```http
DELETE /api/task/{task_id}
Authorization: Bearer {token}

Response: 200 OK
{
  "success": true,
  "data": null,
  "message": "Task deleted successfully"
}

Note: Users can only delete their own tasks (admins can delete any)
```

---

### Status Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 201  | Created |
| 400  | Bad Request (validation error) |
| 401  | Unauthorized (invalid/missing token) |
| 403  | Forbidden (insufficient permissions) |
| 404  | Not Found |
| 422  | Unprocessable Entity (validation error) |
| 500  | Internal Server Error |

---

## 📁 Project Structure

### Database Models

#### User Model
```python
- id: Integer (Primary Key)
- email: String (Unique)
- full_name: String
- hashed_password: String
- role: String (default: "user")  # admin or user
- is_active: Boolean (default: True)
- disabled: Boolean (default: False)
- created_at: DateTime
- updated_at: DateTime
```

#### Project Model
```python
- id: Integer (Primary Key)
- title: String
- description: String (Optional)
- created_by: Integer (Foreign Key -> users.id)
- created_at: DateTime
- updated_at: DateTime
```

#### Task Model
```python
- id: Integer (Primary Key)
- title: String
- description: String (Optional)
- project_id: Integer (Foreign Key -> projects.id)
- assigned_to: Integer (Foreign Key -> users.id)
- status: String (default: "todo")  # todo, in-progress, done
- due_date: Date (Optional)
- created_at: DateTime
- updated_at: DateTime
```

---

## 🔐 Security Features

1. **Password Hashing**: Bcrypt with automatic salt generation
2. **JWT Authentication**: Secure token-based authentication
3. **CORS Protection**: Configured for specific frontend origin
4. **Role-Based Access**: Middleware-level permission checking
5. **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
6. **Input Validation**: Pydantic models for request validation

---

## 📧 Email Notifications

The system sends automated emails for:

1. **Welcome Email**: Sent when a new user registers
2. **Task Assignment**: Sent when a task is assigned to a user
3. **Status Update**: Sent to project creator when task status changes

Email templates are located in `Server/app/templates/email/` and use Jinja2 templating.

---

## 🧪 Testing the API

You can test the API using:

1. **Swagger UI**: Visit `http://localhost:8000/docs`
2. **Postman**: Import the endpoints from the API documentation
3. **cURL**: Use command-line HTTP requests

Example cURL request:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

---

## 🐛 Troubleshooting

### Backend Issues

**Database Connection Error:**
- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Ensure database exists: `CREATE DATABASE project_management;`

**Migration Issues:**
```bash
# Reset migrations (WARNING: deletes all data)
alembic downgrade base
alembic upgrade head
```

**Email Not Sending:**
- Verify SMTP credentials in `.env`
- For Gmail, use App Password, not regular password
- Check firewall/antivirus blocking port 587

### Frontend Issues

**API Connection Error:**
- Verify backend is running on port 8000
- Check `VITE_API_BASE_URL` in `.env`
- Check browser console for CORS errors

**Build Errors:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 📝 License

This project is licensed under the MIT License.

---

## 👥 Contributors

Built with ❤️ by the development team.

---

## 🔮 Future Enhancements

- File attachments for tasks
- Task comments and activity log
- Real-time notifications with WebSockets
- Task dependencies and subtasks
- Calendar view for tasks
- Team/workspace management
- Advanced analytics and reporting
- Mobile application (React Native)
- Integration with external tools (Slack, GitHub, etc.)

---

For more information or support, please open an issue on the repository.

