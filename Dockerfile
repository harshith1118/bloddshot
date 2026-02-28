FROM python:3.11-slim

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

# Copy Python requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy and build React app
COPY gutcheck-web/package*.json ./
RUN npm install
COPY gutcheck-web/src ./src
COPY gutcheck-web/public ./public
COPY gutcheck-web/index.html ./
COPY gutcheck-web/vite.config.js ./
COPY gutcheck-web/tailwind.config.js ./
COPY gutcheck-web/postcss.config.js ./
RUN npm run build

# Copy backend
COPY main.py .
COPY core ./core
COPY prompts ./prompts
COPY utils ./utils

EXPOSE 7860

CMD ["python", "main.py"]
