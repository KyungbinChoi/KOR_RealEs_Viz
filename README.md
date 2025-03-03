# KOR_RealEs_Viz
This project involves building a dashboard that provides real estate information based on actual real estate transaction data in Korea

```
real_estate_dashboard/
│── docker-compose.yml  # Docker 설정 파일 
│── .env                # 환경 변수 파일
│── superset_config.py  # Superset 설정 파일
│
├── airflow/  # Airflow 관련 설정 및 DAG 저장
│   ├── dags/
│   │   ├── fetch_real_estate_data.py  # API 호출 및 데이터 업데이트 DAG
│   │   ├── update_postgres.py         # DB 업데이트 DAG
│   ├── requirements.txt               # Airflow 패키지 의존성 관리
│   ├── dbt/                            # DBT 관련 설정
│   ├── logs/                           # Airflow 로그 디렉토리
│   ├── plugins/                        # Airflow 플러그인
│   ├── Dockerfile                      # Airflow용 Dockerfile
│
├── superset/  # Superset 관련 설정 및 데이터
│   ├── dashboards.json   # Superset 대시보드 설정 (옵션)
│   ├── superset_config.py # Superset 설정 파일
│
├── db/  # PostgreSQL 데이터베이스 설정
│   ├── init.sql  # 초기 테이블 생성 스크립트
│   ├── load_data.py  # 초기 데이터 로드 스크립트
│   ├── data/  # 데이터 파일 저장
│   ├── Dockerfile  # PostgreSQL용 Dockerfile
│
├── jupyter/  # Jupyter Notebook 환경
│   ├── notebooks/
│   │   ├── data_exploration.ipynb  # 데이터 분석 노트북
│   ├── Dockerfile  # Jupyter용 Dockerfile
│
└── plugins/  # Airflow 플러그인 (선택 사항)

```