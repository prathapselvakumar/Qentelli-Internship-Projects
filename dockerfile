# Use the official Python image as base
FROM python:3.9-slim

# Set environment variables for FastAPI app
ENV APP_HOME /app
ENV PORT 8000

# Create and set the working directory
WORKDIR $APP_HOME

# Copy the Python dependencies file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the container
COPY app.py .

# Expose port 8000 for FastAPI
EXPOSE $PORT

# Command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
