import os
import tempfile
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
from pandas_gbq import to_gbq

# Set GCS bucket & BigQuery details
GCS_BUCKET_NAME = "hospital-resources-data"
BQ_PROJECT_ID = "my-project-29069-451803"
BQ_DATASET_NAME = "hospital_resources_data"

# Authenticate using Service Account JSON
CREDENTIALS_PATH = r"/gcs_to_bigquery/my-project-29069-451803-4c2f17ffb8fc.json"
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

# Initialize Google Cloud Storage client
storage_client = storage.Client(credentials=credentials)

def list_gcs_csv_files(bucket_name):
    """List all CSV files in a GCS bucket."""
    bucket = storage_client.bucket(bucket_name)
    return [blob.name for blob in bucket.list_blobs() if blob.name.endswith('.csv')]

def sanitize_column_names(df):
    """Sanitize column names to ensure they are compatible with BigQuery."""
    df.columns = [col.strip().replace(" ", "_").replace(",", "_").replace("-", "_").lower() for col in df.columns]
    return df

def load_csv_to_bigquery(file_name):
    """Load a CSV file from GCS to BigQuery and auto-create table."""
    gcs_uri = f"gs://{GCS_BUCKET_NAME}/{file_name}"
    
    # Download CSV file from GCS
    blob = storage_client.bucket(GCS_BUCKET_NAME).blob(file_name)
    temp_dir = tempfile.gettempdir()  # Get OS-specific temp directory
    temp_csv_path = os.path.join(temp_dir, file_name)
    blob.download_to_filename(temp_csv_path)

    # Remove extra quotes from the CSV file
    with open(temp_csv_path, 'r') as file:
        data = file.read().replace('"', '')

    with open(temp_csv_path, 'w') as file:
        file.write(data)

    # Read CSV file into pandas DataFrame with explicit delimiter and quotechar
    df = pd.read_csv(temp_csv_path, sep=",", quotechar='"', header=0, dtype=str)

    # Print the columns to verify the data split correctly
    print("Columns in DataFrame after read:")
    print(df.columns)
    print("First few rows:")
    print(df.head())

    # Sanitize column names
    df = sanitize_column_names(df)

    # Generate table name dynamically (based on filename)
    table_name = file_name.split('.')[0]  # Remove .csv extension
    destination_table = f"{BQ_DATASET_NAME}.{table_name}"

    # Upload DataFrame to BigQuery
    to_gbq(
        df,
        destination_table=destination_table,
        project_id=BQ_PROJECT_ID,
        credentials=credentials,
        if_exists="replace",  # "replace" ensures table is recreated
    )

    print(f"✅ Successfully loaded {file_name} into {destination_table}")

def main():
    """List and load all CSV files from GCS to BigQuery."""
    csv_files = list_gcs_csv_files(GCS_BUCKET_NAME)

    if not csv_files:
        print("⚠️ No CSV files found in GCS bucket.")
        return

    for file_name in csv_files:
        load_csv_to_bigquery(file_name)

if __name__ == "__main__":
    main()
