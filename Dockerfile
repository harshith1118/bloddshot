FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y nodejs npm git curl

WORKDIR /app

# Copy EVERYTHING at once
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Build React app
WORKDIR /app/gutcheck-web
RUN npm install
RUN npm run build

# Go back to app root and run
WORKDIR /app
EXPOSE 7860

CMD ["python", "gutcheck-web/main.py"]
