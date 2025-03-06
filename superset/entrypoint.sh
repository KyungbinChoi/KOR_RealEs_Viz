#!/bin/bash
set -e

# Superset 데이터베이스 마이그레이션
superset db upgrade
superset init

echo "SUPERSET_ADMIN_USER: $SUPERSET_ADMIN_USER"
echo "SUPERSET_ADMIN_PASSWORD: $SUPERSET_ADMIN_PASSWORD"
echo "SQLALCHEMY_DATABASE_URI: $SQLALCHEMY_DATABASE_URI"

# 관리자 계정이 존재하는지 확인하고, 없으면 생성
if ! superset fab list-users | grep -q "$SUPERSET_ADMIN_USER"; then
    echo " 관리자 계정이 존재하지 않습니다. 생성합니다..."
    superset fab create-admin \
        --username "$SUPERSET_ADMIN_USER" \
        --firstname "Admin" \
        --lastname "User" \
        --email "$SUPERSET_ADMIN_EMAIL" \
        --password "$SUPERSET_ADMIN_PASSWORD"
        
    echo "관리자 계정이 생성되었습니다."
else
    echo "관리자 계정이 이미 존재합니다."
fi


# python /etc/superset/init_superset_db.py 

# Superset 실행
exec superset run -h 0.0.0.0 -p 8088
