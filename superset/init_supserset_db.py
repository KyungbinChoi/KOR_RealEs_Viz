from superset import db
from superset.models.core import Database

def add_database():
    """Superset 실행 후 PostgreSQL을 자동으로 등록"""
    engine = "postgresql://airflow:airflow@postgres:5432/airflow"

    existing_db = db.session.query(Database).filter_by(database_name="PostgreSQL").first()
    if not existing_db:
        postgres_db = Database(
            database_name="PostgreSQL",
            sqlalchemy_uri=engine,
            extra='{"metadata_params": {}, "engine_params": {}, "cache_timeout": 0}',
        )
        db.session.add(postgres_db)
        db.session.commit()
        print("✅ PostgreSQL이 Superset에 성공적으로 등록되었습니다.")

if __name__ == "__main__":
    add_database()
