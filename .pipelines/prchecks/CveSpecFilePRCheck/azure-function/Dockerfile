FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements-container.txt .
RUN pip install --no-cache-dir -r requirements-container.txt

# Copy application code
COPY app.py .

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
