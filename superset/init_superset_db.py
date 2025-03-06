import logging
from flask_appbuilder.security.sqla.models import User
from superset.app import create_app  # ✅ Superset의 Flask 앱 생성 함수 호출
from superset import db
from superset.models.core import Database

# Superset 애플리케이션 컨텍스트 생성
app = create_app()
with app.app_context():
    def add_database():
        """Superset에서 PostgreSQL을 자동으로 등록"""
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
        else:
            print("✅ PostgreSQL 데이터베이스가 이미 존재합니다.")

    add_database()
