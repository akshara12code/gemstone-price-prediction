from __future__ import annotations
import json
from textwrap import dedent
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.pipeline.training_pipeline import TrainingPipeline

training_pipeline = TrainingPipeline()

with DAG(
    "gemstone_training_pipeline",
    default_args={"retries": 2},
    description="it is my training pipeline",
    schedule="@weekly",
    start_date=pendulum.datetime(2026, 1, 9, tz="UTC"),
    catchup=False,
    tags=["machine_learning", "classification", "gemstone"],
) as dag:
    
    dag.doc_md = __doc__
    
    def data_ingestion(**kwargs):
        ti = kwargs["ti"]
        train_data_path, test_data_path = training_pipeline.start_data_ingestion()
        ti.xcom_push("data_ingestion_artifact", {"train_data_path": train_data_path, "test_data_path": test_data_path})
    
    def data_transformation(**kwargs):
        ti = kwargs["ti"]
        data_ingestion_artifact = ti.xcom_pull(task_ids="data_ingestion", key="data_ingestion_artifact")
        train_arr, test_arr = training_pipeline.start_data_transformation(
            data_ingestion_artifact["train_data_path"],
            data_ingestion_artifact["test_data_path"]
        )
        train_arr = train_arr.tolist()
        test_arr = test_arr.tolist()
        ti.xcom_push("data_transformation_artifact", {"train_arr": train_arr, "test_arr": test_arr})
    
    def model_trainer(**kwargs):
        import numpy as np
        ti = kwargs["ti"]
        data_transformation_artifact = ti.xcom_pull(task_ids="data_transformation", key="data_transformation_artifact")
        train_arr = np.array(data_transformation_artifact["train_arr"])
        test_arr = np.array(data_transformation_artifact["test_arr"])
        training_pipeline.start_model_training(train_arr, test_arr)
    
    def push_data_to_storage(**kwargs):
        import os
        # Artifacts are already saved locally in /app/artifacts/
        # No cloud upload needed for now
        artifact_folder = "/app/artifacts/"
        if os.path.exists(artifact_folder):
            print(f"Artifacts saved locally at: {artifact_folder}")
            # List all artifacts
            for root, dirs, files in os.walk(artifact_folder):
                for file in files:
                    print(f"  - {os.path.join(root, file)}")
        else:
            print("No artifacts folder found")
    
    data_ingestion_task = PythonOperator(
        task_id="data_ingestion",
        python_callable=data_ingestion,
    )
    data_ingestion_task.doc_md = dedent(
        """
        #### Data Ingestion Task
        This task handles the ingestion of data from the source and splits it into training and testing datasets.
        """
    )
    
    data_transform_task = PythonOperator(
        task_id="data_transformation",
        python_callable=data_transformation,
    )
    data_transform_task.doc_md = dedent(
        """
        #### Data Transformation Task
        This task handles the transformation of the data for model training.
        """
    )
    
    model_trainer_task = PythonOperator(
        task_id="model_trainer",
        python_callable=model_trainer,
    )
    model_trainer_task.doc_md = dedent(
        """         
        #### Model Trainer Task
        This task is responsible for training the machine learning model using the transformed data.
        """
    )
    
    push_data_task = PythonOperator(
        task_id="push_data_to_storage",
        python_callable=push_data_to_storage,
    )
    
    data_ingestion_task >> data_transform_task >> model_trainer_task >> push_data_task