#!/bin/bash

set -e 


echo "Ожидание готовности PostgreSQL..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
    sleep 2
done

echo "PostgreSQL готов!"


echo "Ожидание готовности Redis..."
REDIS_READY=0
ATTEMPTS=0
MAX_ATTEMPTS=10

while [ $REDIS_READY -eq 0 ] && [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    if timeout 3 bash -c "</dev/tcp/$REDIS_HOST/$REDIS_PORT" 2>/dev/null; then
        REDIS_READY=1
    else
        sleep 2
        ATTEMPTS=$((ATTEMPTS + 1))
    fi
done

if [ $REDIS_READY -eq 0 ]; then
    echo "Не удалось подключиться к Redis."
    exit 1
fi

echo "Redis готов!"


echo "Активация виртуального окружения..."
VENV_PATH=".venv"
if [[ -f "$VENV_PATH/bin/activate" ]]; then
    source "$VENV_PATH/bin/activate"
else
    echo "Виртуальное окружение не найдено по пути $VENV_PATH"
    exit 1
fi

echo "Виртуальное окружение активировано..."


echo "Выполнение миграций базы данных..."
alembic upgrade head

echo "Миграции выполнены успешно!"


cd src 

echo "Запуск приложения..."
exec python main.py
