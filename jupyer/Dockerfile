# 기본 Jupyter Notebook 이미지 사용
FROM jupyter/base-notebook:python-3.10

# root 사용자로 전환
USER root

# PostgreSQL 클라이언트 설치
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean

# 필요한 Python 패키지 설치
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Jupyter Notebook 디렉토리 설정
WORKDIR /home/jovyan/work