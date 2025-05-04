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

## 启动应用

### 方法一：使用uvicorn（开发环境）

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 方法二：使用gunicorn（生产环境）

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

启动后，可以通过浏览器访问：

- 主页：<http://localhost:8000>
- API文档：<http://localhost:8000/docs>
- ReDoc文档：<http://localhost:8000/redoc>

## 数据库迁移

### 初始化数据库

```bash
# 创建迁移脚本
alembic revision --autogenerate -m "Initial migration"

# 应用迁移
alembic upgrade head
```

### 创建新的迁移

```bash
# 创建迁移脚本
alembic revision --autogenerate -m "描述迁移内容"

# 应用迁移
alembic upgrade head
```

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
