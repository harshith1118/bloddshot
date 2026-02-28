FROM python:3.11-slim

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire gutcheck-web folder
COPY gutcheck-web/ ./gutcheck-web/

# Build React app
WORKDIR /app/gutcheck-web
RUN npm install
RUN npm run build

# Setup backend
WORKDIR /app
COPY main.py .
COPY core/ ./core/
COPY prompts/ ./prompts/
COPY utils/ ./utils/

EXPOSE 7860

CMD ["python", "main.py"]
