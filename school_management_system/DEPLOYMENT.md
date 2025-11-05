# Deploying College Management System to Render.com

This guide provides step-by-step instructions for deploying the College Management System to Render.com.

## Prerequisites

1. A GitHub, GitLab, or Bitbucket account
2. A Render.com account (free tier is sufficient)

## Deployment Helper Scripts

We've included several helper scripts to make the deployment process easier:

- `deploy.sh` (Linux/macOS): Prepares your code for deployment, including generating a secure SECRET_KEY
- `deploy.bat` (Windows): Windows version of the deployment script
- `check_deployment.py`: Verifies that your deployment is working correctly

To use the deployment helper script:

```bash
# On Linux/macOS
cd school_management_system
./deploy.sh

# On Windows
cd school_management_system
deploy.bat
```

## Deployment Steps

### 1. Push the Code to a Git Repository

First, create a new repository on GitHub, GitLab, or Bitbucket and push the code:

```bash
# Initialize a Git repository if not already done
git init

# Add all files
git add .

# Commit the changes
git commit -m "Initial commit"

# Add your remote repository
git remote add origin <your-repository-url>

# Push the code
git push -u origin main
```

### 2. Deploy to Render.com

#### Option 1: Using the Render Blueprint (Recommended)

1. Log in to your Render.com account
2. Click on the "Blueprint" button in the dashboard
3. Connect your Git repository
4. Select the repository containing the College Management System
5. Render will automatically detect the `render.yaml` file and set up the services
6. Click "Apply" to start the deployment

#### Option 2: Manual Setup

1. Log in to your Render.com account
2. Create a new PostgreSQL database:
   - Click on "New" > "PostgreSQL"
   - Name: `college_management_db`
   - Select the free plan
   - Click "Create Database"
   - Note the connection string for later use

3. Create a new Web Service:
   - Click on "New" > "Web Service"
   - Connect your Git repository
   - Name: `college-management-system`
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd school_management_system && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Select the free plan
   - Add the following environment variables:
     - `SECRET_KEY`: Generate a random string (e.g., using `openssl rand -hex 32`)
     - `USE_SQLITE_MEMORY`: `false`
     - `DATABASE_URL`: Use the connection string from the PostgreSQL database
     - `FIRST_SUPERUSER`: `admin@example.com` (or your preferred admin email)
     - `FIRST_SUPERUSER_PASSWORD`: `admin` (or your preferred admin password)
   - Click "Create Web Service"

### 3. Access Your Deployed Application

Once the deployment is complete, you can access your application at:
- Web Interface: `https://college-management-system.onrender.com`
- API: `https://college-management-system.onrender.com/api`
- API Documentation: `https://college-management-system.onrender.com/docs`

### 4. Initial Login

Use the following credentials to log in:
- Email: `admin@example.com` (or the email you specified in the environment variables)
- Password: `admin` (or the password you specified in the environment variables)

## Verifying Your Deployment

After deploying the application, you can use the included `check_deployment.py` script to verify that everything is working correctly:

```bash
# From the school_management_system directory
python check_deployment.py https://your-app-name.onrender.com
```

This script will check various endpoints of your application and report any issues.

## Troubleshooting

If you encounter any issues during deployment:

1. Check the Render logs for error messages
2. Ensure all environment variables are correctly set
3. Verify that the database connection is working
4. Check if the application is running by accessing the `/api` endpoint
5. Run the `check_deployment.py` script to identify specific issues

For more help, refer to the [Render documentation](https://render.com/docs) or contact support.
