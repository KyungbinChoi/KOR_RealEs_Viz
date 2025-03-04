from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# DAG 기본 설정
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 1),  # DAG 시작 기준일
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# 매월 1일 실행 설정
dag = DAG(
    "test_monthly_fetching",
    default_args=default_args,
    schedule_interval="0 0 1 * *",  # 매월 1일 00:00 실행
    catchup=False,
    description="Executes a script on the first day of each month with the date as an argument",
)

# 실행할 스크립트 경로
api_script_path = "/opt/airflow/script/monthly_fetching.py"
upload_script_path = "/opt/airflow/script/upload_db.py"

# 실행 시점의 날짜(yyyy-mm-dd)를 Airflow 매크로로 전달
api_fetching_task = BashOperator(
    task_id="run_monthly_script",
    bash_command=f"python {api_script_path} {{ ds }}",
    dag=dag,
)

upload_db_task = BashOperator(
    task_id="run_monthly_script",
    bash_command=f"python {upload_script_path}",
    dag=dag,
)

start_dag = EmptyOperator()
end_dag = EmptyOperator()

start_dag >> api_fetching_task >> upload_db_task >> end_dag
