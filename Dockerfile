# 1. Base image with Python 3.12
FROM python:3.12-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir flask requests \
 && python -c "import flask, requests; print('✅ Flask', flask.__version__, 'Requests', requests.__version__)"

# 4. Copy the rest of your code
COPY . .

# 5. Expose Render’s default port
EXPOSE 10000

# 6. Start the app
CMD ["python", "app.py"]