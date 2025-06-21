# Use an official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Cloud Run listens on port 8080 by convention, so expose 8080
EXPOSE 8080

# Run the FastAPI app with uvicorn, binding to 0.0.0.0 and port 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
