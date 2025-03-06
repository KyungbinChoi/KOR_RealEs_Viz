# Superset 기본 이미지
FROM apache/superset:latest

# root 사용자로 변경
USER root

# PostgreSQL 클라이언트 설치 (pg_isready 포함)
RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY init_superset_db.py /etc/superset/init_superset_db.py
RUN chmod +x /etc/superset/init_superset_db.py

# Superset 기본 작업 경로 설정
WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Entrypoint 설정
ENTRYPOINT ["/app/entrypoint.sh"]