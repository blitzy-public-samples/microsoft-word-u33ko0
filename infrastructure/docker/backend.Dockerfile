# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./app /app

# Expose port 8000 for API traffic
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# HUMAN ASSISTANCE NEEDED
# Please review the following:
# 1. Ensure that the Python version (3.9) is appropriate for your project.
# 2. Verify that the requirements.txt file is in the correct location relative to this Dockerfile.
# 3. Confirm that the application code is in the ./app directory relative to this Dockerfile.
# 4. Check if any additional environment variables or configurations are needed for your specific FastAPI application.