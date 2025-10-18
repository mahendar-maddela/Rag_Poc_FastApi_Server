#  Base image
FROM python:3.11-slim

#  Working directory
WORKDIR /app

#  Install system-level dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    ghostscript \
    python3-tk \
    poppler-utils \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

#  Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#  Copy project files
COPY . .

#  Expose port
EXPOSE 8000

#  Run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
