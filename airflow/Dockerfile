# Airflow 베이스 이미지
FROM apache/airflow:2.9.1-python3.10

# root 사용자로 전환
USER root

# DBT 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-distutils \
    libpq-dev \
    && apt-get clean

# 작업 디렉토리 설정
WORKDIR /opt/airflow

# DAG 및 DBT 설정 복사
COPY dags/ /opt/airflow/dags/
COPY dbt/ /opt/airflow/dbt/

# Entrypoint 스크립트 복사
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER airflow

# requirements.txt 복사 및 Python 패키지 설치
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 포트 노출
EXPOSE 8080

# Entrypoint 설정
ENTRYPOINT ["/app/entrypoint.sh"]