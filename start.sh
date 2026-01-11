#!/bin/sh
nohup airflow scheduler &
airflow webserver --port 8080 --host 0.0.0.0