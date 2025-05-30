FROM python:3.13-slim

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ .

# Expose the Flask port
EXPOSE 5000

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
