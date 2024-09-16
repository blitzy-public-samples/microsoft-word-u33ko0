#!/bin/bash

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required dependencies
echo "Installing required dependencies..."
sudo apt-get install -y nodejs npm python3 python3-pip python3-venv postgresql

# Set up virtual environments
echo "Setting up virtual environments..."
python3 -m venv backend/venv
source backend/venv/bin/activate

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Set up local database
echo "Setting up local database..."
sudo -u postgres psql -c "CREATE DATABASE msword_clone;"
sudo -u postgres psql -c "CREATE USER msword_user WITH PASSWORD 'password';"
sudo -u postgres psql -c "ALTER ROLE msword_user SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE msword_user SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE msword_user SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE msword_clone TO msword_user;"

# Configure environment variables
echo "Configuring environment variables..."
cp .env.example .env
# HUMAN ASSISTANCE NEEDED
# TODO: Update the .env file with appropriate values for production

# Run initial database migrations
echo "Running initial database migrations..."
cd backend
python manage.py makemigrations
python manage.py migrate
cd ..

# Print setup completion message
echo "Development environment setup complete!"
echo "To start the development server:"
echo "1. Activate the virtual environment: source backend/venv/bin/activate"
echo "2. Start the backend: cd backend && python manage.py runserver"
echo "3. In a new terminal, start the frontend: cd frontend && npm start"