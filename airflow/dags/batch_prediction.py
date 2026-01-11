# from asyncio import tasks
# import json
# from textwrap import dedent
# import pendulum
# import os
# from airflow import DAG
# from airflow.operators.python import PythonOperator

# with DAG(
#     'batch_prediction',
#     default_args={'retries': 2},
#     description='gemstone batch prediction',
#     schedule_interval="@weekly",
#     start_date=pendulum.datetime(2023, 12, 11, tz="UTC"),
#     catchup=False,
#     tags=['example'],
# ) as dag:
    
#     def download_files(**kwargs):
#         from azure.storage.blob import BlobServiceClient
        
#         connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
#         container_name = os.getenv("AZURE_CONTAINER_NAME")
#         input_dir = "/app/input_files"
        
#         # creating directory
#         os.makedirs(input_dir, exist_ok=True)
        
#         # Download files from Azure Blob Storage
#         blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#         container_client = blob_service_client.get_container_client(container_name)
        
#         blob_list = container_client.list_blobs(name_starts_with="input_files/")
#         for blob in blob_list:
#             blob_client = container_client.get_blob_client(blob.name)
#             download_path = os.path.join(input_dir, os.path.basename(blob.name))
#             with open(download_path, "wb") as download_file:
#                 download_file.write(blob_client.download_blob().readall())
    
#     def batch_prediction(**kwargs):
#         from src.pipeline.batch_prediction import BatchPredictionConfig, SensorBatchPrediction
#         config = BatchPredictionConfig()
#         sensor_batch_prediction = SensorBatchPrediction(config=config)
#         sensor_batch_prediction.start_prediction()
    
#     def upload_files(**kwargs):
#         from azure.storage.blob import BlobServiceClient
        
#         connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
#         container_name = os.getenv("AZURE_CONTAINER_NAME")
        
#         blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#         container_client = blob_service_client.get_container_client(container_name)
        
#         # Upload archive files
#         archive_dir = "/app/archive"
#         if os.path.exists(archive_dir):
#             for root, dirs, files in os.walk(archive_dir):
#                 for file in files:
#                     file_path = os.path.join(root, file)
#                     blob_name = f"archive/{file}"
#                     blob_client = container_client.get_blob_client(blob_name)
#                     with open(file_path, "rb") as data:
#                         blob_client.upload_blob(data, overwrite=True)
        
#         # Upload outbox files
#         outbox_dir = "/app/outbox"
#         if os.path.exists(outbox_dir):
#             for root, dirs, files in os.walk(outbox_dir):
#                 for file in files:
#                     file_path = os.path.join(root, file)
#                     blob_name = f"outbox/{file}"
#                     blob_client = container_client.get_blob_client(blob_name)
#                     with open(file_path, "rb") as data:
#                         blob_client.upload_blob(data, overwrite=True)
    
#     download_input_files = PythonOperator(
#         task_id="download_file",
#         python_callable=download_files
#     )
    
#     generate_prediction_files = PythonOperator(
#         task_id="prediction",
#         python_callable=batch_prediction
#     )
    
#     upload_prediction_files = PythonOperator(
#         task_id="upload_prediction_files",
#         python_callable=upload_files
#     )
    
#     download_input_files >> generate_prediction_files >> upload_prediction_files