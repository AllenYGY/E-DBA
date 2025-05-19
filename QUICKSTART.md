# 教育数据湾区(E-DBA)系统启动指南

## 项目简介

教育数据湾区(E-DBA)是一个为高等教育机构提供安全、透明、互操作的数据共享平台，基于FastAPI框架开发。系统支持学生身份认证、论文访问控制、在线支付、课程信息共享等核心功能。

## 环境要求

- Python 3.10+
- MySQL 8.0+
- pip 20.0+
- Git (可选，用于版本控制)
- Conda (可选，用于环境管理)

## 安装步骤

### 1. 克隆项目（可选）

```bash
git clone [repository-url]
cd edba
```

### 2. 创建虚拟环境（推荐）

#### 方法一：使用Python venv

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 方法二：使用Conda（推荐）

1. 安装Conda（如果尚未安装）：
   - 下载并安装Miniconda：<https://docs.conda.io/en/latest/miniconda.html>
   - 或下载并安装Anaconda：<https://www.anaconda.com/products/distribution>

2. 创建并激活Conda环境：

```bash
# 创建名为edba的Conda环境，指定Python版本
conda create -n edba python=3.10

# 激活环境
# Windows
conda activate edba

# macOS/Linux
source activate edba
```

3. 验证环境：

```bash
# 检查Python版本
python --version

# 检查已安装的包
conda list
```

### 3. 安装依赖包

#### 方法一：使用pip安装（推荐）

1. 更新pip到最新版本：

```bash
pip install --upgrade pip
```

2. 安装项目依赖：

```bash
pip install -r requirements.txt
```

3. 如果安装过程中遇到问题，可以尝试使用国内镜像源：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 方法二：使用conda安装

1. 首先安装conda包：

```bash
conda install --file requirements.txt
```

2. 对于conda仓库中没有的包，使用pip安装：

```bash
pip install -r requirements.txt
```

#### 依赖安装注意事项

1. **MySQL客户端安装**
   - Windows: 需要安装MySQL Connector/C
   - macOS: `brew install mysql-connector-c`
   - Linux: `sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`

2. **系统依赖**
   - 确保系统已安装必要的开发工具：
     - Windows: Visual C++ Build Tools
     - macOS: Xcode Command Line Tools
     - Linux: build-essential, python3-dev

3. **常见问题解决**
   - 如果安装mysqlclient失败，可以尝试：
     ```bash
     # Windows
     pip install --only-binary :all: mysqlclient
     
     # macOS/Linux
     pip install mysqlclient
     ```
   - 如果安装python-magic失败，可以尝试：
     ```bash
     # macOS
     brew install libmagic
     
     # Linux
     sudo apt-get install libmagic-dev
     ```

### 4. 配置数据库

1. 确保MySQL服务已启动
2. 创建数据库：

```sql
CREATE DATABASE edba CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 配置环境变量

1. 复制环境变量模板：

```bash
cp .env.example .env
```

2. 编辑`.env`文件，配置以下内容：

```python
# 数据库配置
MYSQL_SERVER=localhost
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DB=edba
MYSQL_PORT=3306

# 安全配置
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=11520

# 跨域配置
BACKEND_CORS_ORIGINS=["http://localhost:8000", "http://localhost:3000"]

# 项目配置
PROJECT_NAME=E-DBA
DEBUG=True

# 管理员配置
E_ADMIN_NAME=eadmin
E_ADMIN_EMAIL=eadmin@edba.com
E_ADMIN_PASSWORD=eadmin@123

SENIOR_E_NAME=senior
SENIOR_E_ADMIN_EMAIL=senior@edba.com
SENIOR_E_ADMIN_PASSWORD=SeniorEAdmin@123

T_ADMIN_NAME=tadmin
T_ADMIN_EMAIL=tadmin@edba.com
T_ADMIN_PASSWORD=TAdmin@123
```

## 部署说明

### 开发环境部署

1. **使用uvicorn（推荐）**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

2. **使用Python直接运行**

```bash
python -m app.main
```

### 生产环境部署

1. **使用gunicorn（推荐）**

```bash
# 安装gunicorn
pip install gunicorn

# 启动服务
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

2. **使用Docker部署**

创建 `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

构建和运行Docker容器：
```bash
# 构建镜像
docker build -t edba .

# 运行容器
docker run -d -p 8000:8000 --name edba edba
```

3. **使用Docker Compose部署**

创建 `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MYSQL_SERVER=db
      - MYSQL_USER=edba
      - MYSQL_PASSWORD=your_password
      - MYSQL_DB=edba
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=edba
      - MYSQL_USER=edba
      - MYSQL_PASSWORD=your_password
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

启动服务：
```bash
docker-compose up -d
```

## 系统配置

### 环境变量配置

完整的环境变量配置说明：

```python
# 数据库配置
MYSQL_SERVER=localhost        # MySQL服务器地址
MYSQL_USER=your_username     # MySQL用户名
MYSQL_PASSWORD=your_password # MySQL密码
MYSQL_DB=edba               # 数据库名
MYSQL_PORT=3306             # MySQL端口

# 安全配置
SECRET_KEY=your-secret-key-here           # JWT密钥
ACCESS_TOKEN_EXPIRE_MINUTES=11520         # 访问令牌过期时间（分钟）
REFRESH_TOKEN_EXPIRE_DAYS=7               # 刷新令牌过期时间（天）
ALGORITHM=HS256                          # JWT算法

# 跨域配置
BACKEND_CORS_ORIGINS=["http://localhost:8000", "http://localhost:3000"]  # 允许的跨域源

# 项目配置
PROJECT_NAME=E-DBA                        # 项目名称
DEBUG=True                                # 调试模式
API_V1_STR=/api/v1                        # API版本前缀
SERVER_HOST=0.0.0.0                       # 服务器主机
SERVER_PORT=8000                          # 服务器端口

# 文件上传配置
UPLOAD_DIR=uploads                        # 上传目录
MAX_UPLOAD_SIZE=104857600                 # 最大上传大小（字节）
ALLOWED_EXTENSIONS=["pdf", "doc", "docx"] # 允许的文件类型

# 日志配置
LOG_LEVEL=INFO                            # 日志级别
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s  # 日志格式
LOG_DIR=logs                              # 日志目录

# 管理员配置
E_ADMIN_NAME=eadmin                       # E-Admin用户名
E_ADMIN_EMAIL=eadmin@edba.com            # E-Admin邮箱
E_ADMIN_PASSWORD=eadmin@123              # E-Admin密码

SENIOR_E_NAME=senior                      # Senior E-Admin用户名
SENIOR_E_ADMIN_EMAIL=senior@edba.com     # Senior E-Admin邮箱
SENIOR_E_ADMIN_PASSWORD=SeniorEAdmin@123 # Senior E-Admin密码

T_ADMIN_NAME=tadmin                       # T-Admin用户名
T_ADMIN_EMAIL=tadmin@edba.com            # T-Admin邮箱
T_ADMIN_PASSWORD=TAdmin@123              # T-Admin密码

# 支付配置
PAYMENT_PROVIDER=bank_transfer           # 支付提供商
BANK_ACCOUNT=your_bank_account           # 银行账户
BANK_NAME=your_bank_name                 # 银行名称
```

### 日志配置

系统使用Python的logging模块进行日志记录。日志配置示例：

```python
# app/core/logging.py
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_dir = os.getenv("LOG_DIR", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "edba.log")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_format = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # 配置根日志记录器
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=[
            RotatingFileHandler(
                log_file,
                maxBytes=10485760,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
```

### 数据库迁移

使用Alembic进行数据库迁移管理：

1. **初始化迁移**

```bash
# 创建迁移脚本
alembic revision --autogenerate -m "Initial migration"

# 应用迁移
alembic upgrade head
```

2. **创建新的迁移**

```bash
# 创建迁移脚本
alembic revision --autogenerate -m "描述迁移内容"

# 应用迁移
alembic upgrade head
```

3. **回滚迁移**

```bash
# 回滚到上一个版本
alembic downgrade -1

# 回滚到特定版本
alembic downgrade <revision_id>
```

## 监控和维护

### 健康检查

系统提供了健康检查端点：

- GET `/api/v1/health` - 检查系统健康状态
- GET `/api/v1/health/db` - 检查数据库连接状态
- GET `/api/v1/health/storage` - 检查存储系统状态

### 性能监控

1. **使用Prometheus监控**

安装Prometheus客户端：
```bash
pip install prometheus-client
```

配置Prometheus指标：
```python
from prometheus_client import Counter, Histogram
import time

# 定义指标
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

# 中间件示例
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    REQUEST_COUNT.inc()
    start_time = time.time()
    response = await call_next(request)
    REQUEST_LATENCY.observe(time.time() - start_time)
    return response
```

2. **使用Grafana可视化**

创建Grafana仪表板，监控以下指标：

- 请求总数
- 请求延迟
- 错误率
- 数据库连接数
- 系统资源使用情况

## 故障排除

### 常见问题

1. **数据库连接错误**
   - 检查MySQL服务是否运行
   - 验证`.env`文件中的数据库配置
   - 确保数据库用户有正确的权限
   - 检查数据库端口是否被占用

2. **文件上传失败**
   - 检查上传目录权限
   - 验证文件大小是否超过限制
   - 确认文件类型是否允许
   - 检查磁盘空间是否充足

3. **认证问题**
   - 验证JWT密钥是否正确
   - 检查令牌是否过期
   - 确认用户权限是否正确
   - 查看日志中的认证错误

4. **性能问题**
   - 检查数据库索引
   - 优化查询语句
   - 调整工作进程数
   - 监控系统资源使用

### 日志分析

使用以下命令分析日志：

```bash
# 查看错误日志
grep ERROR logs/edba.log

# 查看特定用户的日志
grep "user@example.com" logs/edba.log

# 查看特定时间段的日志
grep "2024-03-20" logs/edba.log

# 实时查看日志
tail -f logs/edba.log
```

## 安全建议

1. **定期更新依赖**

```bash
pip install --upgrade -r requirements.txt
```

2. **数据库安全**
   - 使用强密码
   - 限制数据库访问IP
   - 定期备份数据
   - 启用SSL连接

3. **API安全**
   - 启用HTTPS
   - 实现请求速率限制
   - 验证所有输入
   - 使用安全的HTTP头

4. **文件安全**
   - 限制文件上传类型
   - 扫描上传文件
   - 使用安全的文件存储
   - 定期清理临时文件

## 联系支持

如遇到问题，请通过以下方式联系支持：

1. 提交Issue到项目仓库
2. 发送邮件到 <support@edba.com>
3. 在工作时间（9:00-18:00）拨打支持热线

## 测试

### 运行测试用例

```bash
# 运行所有测试
pytest app/tests/

# 运行特定测试文件
pytest app/tests/test_auth.py

# 运行测试并显示覆盖率
pytest --cov=app app/tests/
```

## 常见问题

1. **数据库连接错误**
   - 检查MySQL服务是否运行
   - 验证`.env`文件中的数据库配置
   - 确保数据库用户有正确的权限

2. **依赖包安装失败**
   - 更新pip：`pip install --upgrade pip`
   - 使用国内镜像源：
     ```bash
     pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
     ```

3. **端口被占用**
   - 查找占用端口的进程：`lsof -i :8000`
   - 修改启动端口：
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
     ```

4. **JWT认证失败**
   - 检查`SECRET_KEY`配置
   - 确保token未过期
   - 验证用户权限

5. **文件上传失败**
   - 检查`uploads`目录权限
   - 验证文件大小限制
   - 确保文件格式正确

## 维护建议

1. **定期备份**
   - 数据库备份
   - 配置文件备份
   - 上传文件备份

2. **日志管理**
   - 定期检查错误日志
   - 监控系统性能
   - 分析用户行为

3. **安全更新**
   - 定期更新依赖包
   - 检查安全漏洞
   - 更新SSL证书

## 获取帮助

- 查看API文档：<http://localhost:8000/docs>
- 提交Issue：<https://github.com/your-repo/issues>
- 联系技术支持：<support@edba.com>
