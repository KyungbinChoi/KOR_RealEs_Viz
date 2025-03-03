# PostgreSQL 기본 이미지 사용
FROM postgres:latest
# root 사용자로 전환
USER root

# Python 및 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3.11-venv \ 
    build-essential \
    libpq-dev \
    postgresql-client \
    && apt-get clean

# requirements.txt 복사 및 Python 패키지 설치
COPY requirements.txt /tmp/requirements.txt
# Python 가상 환경 생성
RUN python3 -m venv /opt/venv

# 가상 환경 활성화 및 pip 패키지 설치
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

# PATH에 가상 환경 추가
ENV PATH="/opt/venv/bin:$PATH"
# 작업 디렉토리 설정
WORKDIR /app

# 스크립트 및 데이터 복사
# COPY init.sql /docker-entrypoint-initdb.d/
COPY load_data.py /app/load_data.py
COPY data/ /app/data/

# Entrypoint 스크립트 복사
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# PostgreSQL 기본 포트 노출
EXPOSE 5432

# Entrypoint 설정
ENTRYPOINT ["/app/entrypoint.sh"]