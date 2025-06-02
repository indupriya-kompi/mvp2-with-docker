# # Use an official Python base image
# FROM python:3.10-slim

# # Set working directory in container
# WORKDIR /app

# # Copy the requirements first and install dependencies
# COPY requirements.txt .
# # RUN pip install --no-cache-dir -r requirements.txt

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy entire application code into container
# COPY . .
# # COPY ./app ./app

# # Expose FastAPI port (default: 8000)
# EXPOSE 8000

# # Command to run FastAPI server
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# # CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# Use an official Python base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy the requirements first and install dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire application code into container
COPY . .

# Expose FastAPI port (default: 8000)
EXPOSE 8000

# Command to run FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
