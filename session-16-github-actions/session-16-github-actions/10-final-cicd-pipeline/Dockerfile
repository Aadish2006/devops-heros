# Stage 1: Runtime Container for Session 16 Calculator
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Install Python runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/

# Set Python environment variables
ENV PYTHONUNBUFFERED=1

# Entrypoint command
CMD ["python", "app/calculator.py"]
