# Stage 1: build
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the default Render port
EXPOSE 10000

# Command to run your Flask app
CMD ["python", "app.py"]