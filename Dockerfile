FROM python:3.11-slim

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm

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

# Copy backend files to /app
WORKDIR /app
COPY main.py .
COPY core/ ./core/
COPY prompts/ ./prompts/
COPY utils/ ./utils/

EXPOSE 7860

CMD ["python", "main.py"]
