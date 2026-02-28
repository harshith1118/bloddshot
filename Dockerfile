FROM python:3.11-slim

# Install Node.js for building React
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs

# Set working directory
WORKDIR /app

# Copy backend requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend package.json and install
COPY gutcheck-web/package.json gutcheck-web/
WORKDIR /app/gutcheck-web
RUN npm install

# Copy frontend source and build
COPY gutcheck-web/ ./
RUN npm run build

# Go back to app root
WORKDIR /app

# Copy backend code
COPY main.py .
COPY core/ ./core/
COPY prompts/ ./prompts/
COPY utils/ ./utils/

# Expose port
EXPOSE 7860

# Run the server
CMD ["python", "main.py"]
