import os

# 1. 데이터베이스 연결 설정 (PostgreSQL)
SQLALCHEMY_DATABASE_URI = "postgresql://airflow:airflow@postgres:5432/superset_db"

# 2. 보안 설정
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "mysecretkey")  # 보안 키 설정
WTF_CSRF_ENABLED = True  # CSRF 보호 활성화
WTF_CSRF_EXEMPT_LIST = []  # CSRF 예외 URL 설정 가능

# 3. 캐싱 설정 (선택 사항, 성능 향상)
CACHE_CONFIG = {
    "CACHE_TYPE": "simple",  # 기본 메모리 캐싱
}

# 4. 웹 서버 설정
ENABLE_PROXY_FIX = True  # 리버스 프록시 환경에서 올바른 요청 인식
SUPERSET_WEBSERVER_PORT = 8088  # 웹 서버 포트 설정

# 5. API 활성화 (필요 시)
ENABLE_REST_API = True

# 6. 파일 업로드 제한 (선택 사항)
# MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 최대 100MB 파일 업로드 가능

# 7. 기본 로케일 설정
BABEL_DEFAULT_LOCALE = "ko"  # 기본 언어를 한국어로 설정

# 8. 로깅 설정 (선택 사항)
LOGGING_CONFIGURATOR_CLASS = "superset.config.LOGGING_CONFIGURATOR"

# 9. 인증 방식 (기본 로그인 사용)
AUTH_TYPE = 1  # 기존 로그인 방식 유지
