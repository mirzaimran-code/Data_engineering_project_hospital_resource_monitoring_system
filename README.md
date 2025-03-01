# Data Engineering Project: Hospital Resource Monitoring System

This project is designed to monitor and manage hospital resources such as beds, equipment, staff, and ambulances. The data is collected and stored in Google Cloud BigQuery for analysis and reporting.

## Project Structure

- `gcs_to_bigquery.py`: Script to load CSV data from Google Cloud Storage to BigQuery.
- `server.py`: HTTP server script to trigger the `gcs_to_bigquery.py` script.
- `requirements.txt`: List of Python dependencies.
- `Dockerfile`: Docker configuration file to containerize the application.
- `my-project-29069-451803-4c2f17ffb8fc.json`: Google Cloud service account credentials (ignored in `.gitignore`).
- CSV files: Sample data files for beds, equipment status, staff, and ambulances.

## Setup Instructions

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-github-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Set up Google Cloud**:
   - Ensure you have a Google Cloud project set up.
   - Enable the necessary APIs: BigQuery, Cloud Storage, and Cloud Run.
   - Create a service account and download the JSON key file. Place it in the project directory and update the `.gitignore` file to ignore it.

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Build and run the Docker container locally**:
   ```sh
   docker build -t gcs_to_bigquery_image .
   docker run -p 8080:8080 gcs_to_bigquery_image
   ```

5. **Deploy to Google Cloud Run**:
   ```sh
   gcloud auth login
   gcloud auth configure-docker
   docker build -t gcr.io/my-project-29069-451803/gcs_to_bigquery_image .
   docker push gcr.io/my-project-29069-451803/gcs_to_bigquery_image
   gcloud run deploy gcs-to-bigquery-service --image gcr.io/my-project-29069-451803/gcs_to_bigquery_image --platform managed --region us-central1 --allow-unauthenticated
   ```

## Running the Project

1. **Trigger the data load**:
   - Access the HTTP server endpoint to trigger the `gcs_to_bigquery.py` script.
   - The script will load the CSV data from Google Cloud Storage to BigQuery.

2. **Monitor the logs**:
   - Check the logs to ensure the data load was successful.

## CSV Data Files

- `beds.csv`: Contains data about hospital beds.
- `equipment_status.csv`: Contains data about the status of hospital equipment.
- `staff.csv`: Contains data about hospital staff.
- `ambulance.csv`: Contains data about ambulances.

## License

This project is licensed under the MIT License.