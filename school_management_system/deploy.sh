#!/bin/bash
# Script to help with deployment to Render.com

# Generate a secure random key for SECRET_KEY
echo "Generating a secure random key..."
SECRET_KEY=$(openssl rand -hex 32)
echo "Generated SECRET_KEY: $SECRET_KEY"

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    echo "Git repository initialized."
fi

# Add all files to git
echo "Adding files to git..."
git add .
echo "Files added to git."

# Commit changes
echo "Committing changes..."
git commit -m "Prepare for deployment to Render.com"
echo "Changes committed."

echo ""
echo "=== NEXT STEPS ==="
echo "1. Create a repository on GitHub, GitLab, or Bitbucket"
echo "2. Add the remote repository:"
echo "   git remote add origin <your-repository-url>"
echo "3. Push the code:"
echo "   git push -u origin main"
echo "4. Follow the deployment instructions in DEPLOYMENT.md"
echo ""
echo "For Render.com deployment, use the following environment variables:"
echo "SECRET_KEY=$SECRET_KEY"
echo "USE_SQLITE_MEMORY=false"
echo "FIRST_SUPERUSER=admin@example.com"
echo "FIRST_SUPERUSER_PASSWORD=admin"
echo ""
echo "Make sure to change the admin password after deployment!"
