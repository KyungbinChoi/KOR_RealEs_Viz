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

    # pickle 파일 로드
    with open(RESULTS_FILE, "rb") as f:
        data = pickle.load(f)

    # 데이터가 딕셔너리 또는 리스트 형태인지 확인 후 DataFrame 변환
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        df = pd.DataFrame([data])  # 단일 딕셔너리라면 행 하나짜리 DataFrame으로 변환
    else:
        raise ValueError("Unsupported data format in results.pkl")

    # 데이터베이스에 적재 (기존 데이터 덮어쓰기 옵션 설정)
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)

    print(f"Data successfully loaded into PostgreSQL table '{TABLE_NAME}'.")

if __name__ == "__main__":
    load_results_to_postgres()
