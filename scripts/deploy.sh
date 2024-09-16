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
zip -r app.zip . -x "*.git*" "node_modules/*" "venv/*"

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

# Run post-deployment checks
echo "Running post-deployment checks..."
response=$(curl -s -o /dev/null -w "%{http_code}" https://my-word-app.appspot.com/health)
if [ $response -eq 200 ]; then
    echo "Health check passed."
else
    echo "Health check failed. HTTP status code: $response"
    exit 1
fi

# Print deployment status
echo "Deployment completed successfully!"