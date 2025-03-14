# Use a lightweight Python base image
FROM python:3.12-slim-bookworm

# Create and switch to a working directory
WORKDIR /app

# Copy all files in your current directory to the container
COPY . .

# Install required Python packages
# (Adjust packages as needed, or if you have a requirements.txt, use that instead)
RUN pip install --no-cache-dir flask pandas numpy scikit-learn joblib

# Expose the port on which the Flask API runs
EXPOSE 5000

# By default, run the API
CMD ["python", "api.py"]
