# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /gcs_to_bigquery

# Copy script, requirements, and service account JSON
COPY gcs_to_bigquery.py .
COPY server.py .
COPY requirements.txt .
COPY my-project-29069-451803-4c2f17ffb8fc.json .

# Install dependencies
RUN pip install -r requirements.txt

# Run server script
CMD ["python", "server.py"]
