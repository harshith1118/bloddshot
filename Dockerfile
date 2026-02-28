FROM python:3.11-slim

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm curl

# Working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Build React frontend
WORKDIR /app/gutcheck-web
COPY gutcheck-web/package*.json ./
RUN npm install
COPY gutcheck-web/ ./
RUN npm run build

# Setup backend
WORKDIR /app
COPY main.py .
COPY core/ ./core/
COPY prompts/ ./prompts/
COPY utils/ ./utils/

# Expose port
EXPOSE 7860

# Run
CMD ["python", "main.py"]
