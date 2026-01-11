FROM apache/airflow:2.7.1-python3.8

USER airflow

WORKDIR /opt/airflow

# Install your additional Python packages (Airflow is already installed)
RUN pip install --no-cache-dir \
    flask==2.2.5 \
    scikit-learn==1.3.1 \
    pandas==2.0.3 \
    numpy==1.24.3 \
    mlflow==2.16.2 \
    python-dotenv==1.0.0 \
    gunicorn==21.2.0

# Copy your files
COPY --chown=airflow:root . .

ENV AIRFLOW_HOME="/opt/airflow"
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING=True

# Initialize DB and create user as airflow user (not root)
RUN airflow db init

RUN airflow users create \
    -e akshara12082005@gmail.com \
    -f akshara \
    -l srivastava \
    -p admin \
    -r Admin \
    -u admin

USER root
RUN chmod 777 start.sh

USER airflow

ENTRYPOINT ["/bin/bash"]
CMD ["start.sh"]