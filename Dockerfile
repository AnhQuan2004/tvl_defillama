# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container at /app
COPY main.py .

# Make port available to the world outside this container (Cloud Run uses $PORT)
# EXPOSE 5000 # EXPOSE is more for documentation/inter-container communication

# Run the application using Gunicorn (shell form to allow $PORT expansion)
# Bind to 0.0.0.0 and use the PORT environment variable provided by Cloud Run
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app