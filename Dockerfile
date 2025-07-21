# Use an official lightweight Python runtime as base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy local files into the container
COPY . .
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Set environment variables (optional, but you can also pass them at runtime)
# ENV ALPHA_VANTAGE_API_KEY=your_api_key_here

# Default command to run your script
CMD ["python", "main.py"]
