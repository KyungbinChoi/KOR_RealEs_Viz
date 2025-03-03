#!/bin/bash
set -e

# PostgreSQL 서버 실행
echo "Starting PostgreSQL server..."
docker-entrypoint.sh postgres &

# PostgreSQL 서버 대기
until pg_isready -h localhost -p 5432 -U airflow -d airflow; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

echo "PostgreSQL is ready!"

# 가상 환경 활성화
source /opt/venv/bin/activate

# PostgreSQL 서버 유지
wait
