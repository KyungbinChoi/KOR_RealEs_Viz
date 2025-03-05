#!/bin/bash
set -e

# 데이터베이스 초기화
airflow db init

# 기본 사용자 생성
airflow users list | grep -q admin || airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin123

# 전달된 명령 실행
exec airflow webserver -p 8080 & airflow scheduler

