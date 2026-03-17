#!/bin/bash

# 一键启动脚本 for DjangoDemo project

echo "Starting DjangoDemo project setup..."

# 创建日志目录
mkdir -p logs

# 动态获取python3和pip3路径
PYTHON3=$(which python3)
PIP3=$(which pip3)

if [ -z "$PYTHON3" ]; then
    echo "python3 not found. Exiting."
    exit 1
fi

if [ -z "$PIP3" ]; then
    echo "pip3 not found. Exiting."
    exit 1
fi

echo "Using Python: $PYTHON3"
echo "Using Pip: $PIP3"

echo "Installing dependencies..."
$PIP3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Exiting."
    exit 1
fi

echo "Running database migrations..."
$PYTHON3 manage.py migrate

if [ $? -ne 0 ]; then
    echo "Failed to run migrations. Exiting."
    exit 1
fi

echo "Starting Django development server..."
$PYTHON3 manage.py runserver 0.0.0.0:8000 &
SERVER_PID=$!

echo "Starting Celery worker..."
$PYTHON3 -m celery -A DjangoDemo worker --loglevel=info &
CELERY_WORKER_PID=$!

echo "Starting Celery beat..."
$PYTHON3 -m celery -A DjangoDemo beat --loglevel=info &
CELERY_BEAT_PID=$!

echo "All services started successfully!"
echo "Django server running on http://0.0.0.0:8000"
echo "To stop all services, run: kill $SERVER_PID $CELERY_WORKER_PID $CELERY_BEAT_PID"

# 等待所有进程
wait $SERVER_PID $CELERY_WORKER_PID $CELERY_BEAT_PID
