FROM python:3.11-slim

# Install everything at once
RUN apt-get update && apt-get install -y nodejs npm git curl && \
    pip install --no-cache-dir --upgrade pip

WORKDIR /app

# Copy EVERYTHING at once
COPY . .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Build React
WORKDIR /app/gutcheck-web
RUN npm install && npm run build

# Run from /app
WORKDIR /app
EXPOSE 7860

CMD ["python", "main.py"]
