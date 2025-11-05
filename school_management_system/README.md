# College Management System

A comprehensive school management system built with FastAPI, SQLAlchemy, and Jinja2 templates.

## Features

- User management (admin, teachers, parents)
- Student management
- Admission processing
- Subject management
- Timetable scheduling
- Exam and grade management
- Fee and payment processing
- Reporting system
- Web interface with responsive design

## Architecture

The application follows a layered architecture:

- **Models**: SQLAlchemy ORM models for database entities
- **API**: FastAPI endpoints for RESTful API
- **Services**: Business logic layer
- **Web**: Jinja2 templates for web interface

## Running the Application

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository
2. Install dependencies using the setup script (recommended):

```bash
cd school_management_system
python setup.py
```

This script will automatically install all required packages, including `pydantic-settings` if needed.

Alternatively, you can install dependencies manually:

```bash
pip install -r school_management_system/requirements.txt
pip install pydantic-settings  # If needed
```

### Configuration

The application can be configured using environment variables or a `.env` file. The following settings are available:

- `SECRET_KEY`: Secret key for JWT token generation
- `USE_SQLITE_MEMORY`: Set to `True` to use an in-memory SQLite database (default: `True`)
- `POSTGRES_SERVER`: PostgreSQL server address (default: `localhost`)
- `POSTGRES_USER`: PostgreSQL username (default: `postgres`)
- `POSTGRES_PASSWORD`: PostgreSQL password (default: `postgres`)
- `POSTGRES_DB`: PostgreSQL database name (default: `school_management`)

### Running without a Database Connection

The application is configured to run with an in-memory SQLite database by default, which means you don't need to set up a PostgreSQL database to test the features. The in-memory database will be populated with sample data on startup.

#### Quick Start (Recommended)

We've provided convenient scripts to set up and run the application:

**On Linux/macOS:**
```bash
cd school_management_system
chmod +x start.sh  # Make the script executable (first time only)
./start.sh
```

**On Windows:**
```
cd school_management_system
start.bat
```

These scripts will:
1. Create a virtual environment if it doesn't exist
2. Install all required dependencies
3. Start the application

#### Manual Start

If you prefer to run the application manually:

```bash
# Option 1: Using the run script
cd school_management_system
python run.py

# Option 2: Using the module directly (requires proper Python path setup)
# Make sure you're in the parent directory of school_management_system
python -m school_management_system.main
```

> **Note:** If you encounter a `ModuleNotFoundError` for `pydantic_settings`, you can either:
> 1. Install it: `pip install pydantic-settings`
> 2. The application now includes a fallback to use Pydantic's built-in BaseSettings if pydantic-settings is not available

The application will be available at http://localhost:8000.

### API Documentation

FastAPI automatically generates API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

The application includes sample data for testing when running with the in-memory SQLite database. You can use the following credentials to log in:

- Admin: `admin@example.com` / `password`
- Teacher: `teacher@example.com` / `password`
- Parent: `parent@example.com` / `password`

## Production Deployment

For production deployment, it's recommended to:

1. Set `USE_SQLITE_MEMORY` to `False`
2. Configure PostgreSQL connection settings
3. Set a strong `SECRET_KEY`
4. Use a production ASGI server like Uvicorn behind a reverse proxy

### Deploying to Render.com

This application is ready to be deployed to Render.com. We've included all the necessary configuration files:

- `Procfile`: Specifies the command to run the application
- `runtime.txt`: Specifies the Python version
- `render.yaml`: Blueprint for setting up the application and database on Render

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
