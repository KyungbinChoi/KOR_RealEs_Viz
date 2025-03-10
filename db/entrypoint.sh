#!/bin/bash
set -e

# PostgreSQL 서버 실행
echo "Starting PostgreSQL server..."
docker-entrypoint.sh postgres &

# PostgreSQL 서버 대기
until pg_isready -h postgres -p 5432 -U airflow -d airflow; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

echo "PostgreSQL is ready!"

psql -U airflow -d postgres -f /docker-entrypoint-initdb.d/init.sql

# 가상 환경 활성화
source /opt/venv/bin/activate

# PostgreSQL 서버 유지
wait
