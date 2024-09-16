#!/bin/bash

# Check for required GCP credentials
if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "Error: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set."
    exit 1
fi

# Build frontend assets
echo "Building frontend assets..."
npm run build

# Run backend tests
echo "Running backend tests..."
python -m pytest tests/

# Package application
echo "Packaging application..."
zip -r app.zip . -x "*.git*" -x "node_modules/*" -x "venv/*"

# Upload to Google Cloud Storage
echo "Uploading to Google Cloud Storage..."
gsutil cp app.zip gs://my-word-app-bucket/

# Deploy to Google App Engine
echo "Deploying to Google App Engine..."
gcloud app deploy app.yaml --quiet

# Update Google Cloud SQL database
echo "Updating Google Cloud SQL database..."
gcloud sql connect my-word-app-db --user=root < db_migrations.sql

# Configure Google Cloud CDN
echo "Configuring Google Cloud CDN..."
gcloud compute backend-services update my-word-app-backend --enable-cdn

# HUMAN ASSISTANCE NEEDED
# The following post-deployment checks might need to be customized based on the specific application requirements
echo "Running post-deployment checks..."
# Add custom post-deployment checks here
# For example:
# - Check if the application is responding
# - Verify database connections
# - Test critical functionalities

# Print deployment status
echo "Deployment completed successfully!"