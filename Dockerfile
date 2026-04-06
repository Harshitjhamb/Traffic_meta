FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir \
    numpy \
    matplotlib \
    imageio \
    gradio

# Expose port (required by Hugging Face)
EXPOSE 7860
# Run app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
