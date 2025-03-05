#!/bin/bash
set -e

# Superset 데이터베이스 마이그레이션
superset db upgrade
superset init

# 관리자 계정이 존재하는지 확인하고, 없으면 생성
superset fab list-users | grep -q "$SUPERSET_ADMIN_USER" || superset fab create-admin \
    --username "$SUPERSET_ADMIN_USER" \
    --firstname "Admin" \
    --lastname "User" \
    --email "$SUPERSET_ADMIN_EMAIL" \
    --password "$SUPERSET_ADMIN_PASSWORD" \
    --role Admin

# Superset 실행
exec superset run -h 0.0.0.0 -p 8088
