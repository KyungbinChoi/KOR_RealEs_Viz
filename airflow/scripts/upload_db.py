import os
import pickle
import pandas as pd
from sqlalchemy import create_engine

# 환경 변수에서 DB 연결 정보 가져오기
DB_USER = os.getenv("POSTGRES_USER", "airflow")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "airflow")

# PostgreSQL 연결 URL
DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy 엔진 생성
engine = create_engine(DB_URI)

# 적재할 테이블명 설정
TABLE_NAME = "all_transaction_real_estate"

# results.pkl 파일 경로 설정
RESULTS_FILE = "/opt/airflow/dataset/results.pkl"

def load_results_to_postgres():
    # 파일 존재 여부 확인
    if not os.path.exists(RESULTS_FILE):
        raise FileNotFoundError(f"{RESULTS_FILE} not found.")

    # ✅ pandas로 pickle 파일 로드
    df = pd.read_pickle(RESULTS_FILE)

    # ✅ 데이터가 비어 있는지 확인
    if df.empty:
        raise ValueError("⚠️ DataFrame is empty. No data to upload.")

    # ✅ 데이터베이스에 적재 (기존 데이터 덮어쓰기)
    df.to_sql(TABLE_NAME, engine, if_exists="append", index=False)

    print(f"✅ Data successfully loaded into PostgreSQL table '{TABLE_NAME}'.")

if __name__ == "__main__":
    load_results_to_postgres()
