#!/bin/bash

# 一键启动脚本 for DjangoDemo project

echo "Starting DjangoDemo project setup..."

# 确保当前目录是git仓库
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git remote add origin git@github.com:Eric168/DjangoMonitorDemo.git
    git fetch
    git checkout master
    echo "Git repository initialized and checked out to master branch."
else
    # 拉取最新代码
    echo "Pulling latest code from repository..."
    echo "Current directory is a git repository."
    echo "Checking remote repository..."
    git remote -v
    echo "Fetching latest changes..."
    git fetch
    if [ $? -ne 0 ]; then
        echo "Failed to fetch changes. Error code: $?"
    else
        echo "Fetch successful."
        echo "Pulling from origin master..."
        git pull origin master
        if [ $? -ne 0 ]; then
            echo "Failed to pull code. Error code: $?"
        else
            echo "Code pulled successfully."
        fi
    fi
fi

# 创建日志目录
mkdir -p logs

# 检查并安装Python 3和pip3
check_and_install_python() {
    echo "Checking Python 3 installation..."
    if ! which python3 > /dev/null; then
        echo "Python 3 not found. Installing..."
        
        # 检测系统类型
        if [ -f /etc/redhat-release ] || [ -f /etc/amazon-linux-release ]; then
            # RHEL or Amazon Linux
            sudo yum update -y
            sudo yum install python3 -y
        elif [ -f /etc/debian_version ]; then
            # Debian or Ubuntu
            sudo apt-get update -y
            sudo apt-get install python3 -y
        else
            echo "Unsupported Linux distribution. Please install Python 3 manually."
            exit 1
        fi
        
        echo "Python 3 installed successfully."
    else
        echo "Python 3 is already installed."
    fi
    
    # 确保pip3安装
    echo "Checking pip3 installation..."
    if ! which pip3 > /dev/null; then
        echo "pip3 not found. Installing..."
        
        if [ -f /etc/redhat-release ] || [ -f /etc/amazon-linux-release ]; then
            # RHEL or Amazon Linux
            sudo yum install python3-pip -y
        elif [ -f /etc/debian_version ]; then
            # Debian or Ubuntu
            sudo apt-get install python3-pip -y
        else
            echo "Unsupported Linux distribution. Please install pip3 manually."
            exit 1
        fi
        
        echo "pip3 installed successfully."
    else
        echo "pip3 is already installed."
    fi
}

# 执行Python检查和安装
check_and_install_python

# 检查并安装Redis
check_and_install_redis() {
    echo "Checking Redis installation..."
    if ! which redis-server > /dev/null && ! which redis-cli > /dev/null; then
        echo "Redis not found. Installing..."
        
        # 检测系统类型
        if [ -f /etc/redhat-release ]; then
            # RHEL
            sudo yum update -y
            sudo yum install redis -y
            sudo systemctl start redis
            sudo systemctl enable redis
        elif [ -f /etc/amazon-linux-release ]; then
            # Amazon Linux
            sudo yum update -y
            # 尝试安装redis6或redis
            if sudo yum install redis6 -y; then
                sudo systemctl start redis6
                sudo systemctl enable redis6
            elif sudo yum install redis -y; then
                sudo systemctl start redis
                sudo systemctl enable redis
            else
                echo "Failed to install Redis. Please install manually."
                # 继续执行，因为Redis是可选的（开发环境）
            fi
        elif [ -f /etc/debian_version ]; then
            # Debian or Ubuntu
            sudo apt-get update -y
            sudo apt-get install redis-server -y
            sudo systemctl start redis-server
            sudo systemctl enable redis-server
        else
            echo "Unsupported Linux distribution. Please install Redis manually."
            # 继续执行，因为Redis是可选的（开发环境）
        fi
        
        echo "Redis installation completed."
    else
        echo "Redis is already installed."
        # 确保Redis服务正在运行
        if [ -f /etc/redhat-release ]; then
            sudo systemctl start redis 2>/dev/null || true
        elif [ -f /etc/amazon-linux-release ]; then
            sudo systemctl start redis6 2>/dev/null || sudo systemctl start redis 2>/dev/null || true
        elif [ -f /etc/debian_version ]; then
            sudo systemctl start redis-server 2>/dev/null || true
        fi
    fi
}

# 执行Redis检查和安装
check_and_install_redis

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

# 检查并清理端口占用
echo "Checking port 8000..."
if lsof -i :8000 > /dev/null; then
    echo "Port 8000 is already in use. Killing process..."
    lsof -t -i :8000 | xargs kill -9
    echo "Process killed."
fi

echo "Starting Django development server..."
$PYTHON3 manage.py runserver 0.0.0.0:8000 &
SERVER_PID=$!

echo "Starting Celery worker..."
$PYTHON3 -m celery -A DjangoDemo worker --loglevel=info &
CELERY_WORKER_PID=$!

# 清理celerybeat-schedule文件
echo "Cleaning celerybeat-schedule file..."
if [ -f "celerybeat-schedule" ]; then
    rm -f celerybeat-schedule
    echo "celerybeat-schedule file removed."
fi

echo "Starting Celery beat..."
$PYTHON3 -m celery -A DjangoDemo beat --loglevel=info &
CELERY_BEAT_PID=$!

echo "All services started successfully!"
echo "Django server running on http://0.0.0.0:8000"
echo "To stop all services, run: kill $SERVER_PID $CELERY_WORKER_PID $CELERY_BEAT_PID"

# 等待所有进程
wait $SERVER_PID $CELERY_WORKER_PID $CELERY_BEAT_PID
