# 教育数据湾区 (E-DBA)

## 快速启动

[QuickStart](QUICKSTART.md) 查看快速启动指南。

## 项目概述

教育数据湾区(E-DBA)是一个为高等教育机构提供安全、透明、互操作的数据共享平台。该系统基于FastAPI框架开发，采用现代化的微服务架构，支持学生身份认证、论文访问控制、在线支付、课程信息共享等核心功能。

## 主要功能

- **组织管理**：支持组织注册、成员管理、服务配置
- **数据访问**：提供公开和私有数据访问控制
- **支付系统**：支持多种支付方式，包括银行转账、PayPal等
- **身份验证**：学生身份验证和GPA记录查询
- **论文管理**：论文上传、访问控制和下载管理
- **课程信息**：课程信息共享和查询
- **日志审计**：完整的操作日志记录和审计功能
- **数据保险库**：可选的数据存储服务

## 技术栈

- **后端**：Python 3.10+, FastAPI
- **数据库**：MySQL 8.0+
- **认证**：JWT Token
- **API文档**：Swagger UI, ReDoc
- **测试**：Pytest, Black-box testing
- **数据库迁移**：Alembic
- **静态文件服务**：FastAPI StaticFiles
- **文件上传**：支持大文件上传和断点续传

## 项目结构

```bash
app/
├── api/          # API路由和端点
│   ├── v1/      # API版本1
│   └── deps.py  # 依赖注入
├── core/         # 核心配置
│   ├── config.py    # 配置管理
│   ├── security.py  # 安全相关
│   └── logging.py   # 日志配置
├── crud/         # 数据库操作
│   ├── base.py      # 基础CRUD操作
│   └── user.py      # 用户相关操作
├── db/           # 数据库连接
│   ├── base.py      # 数据库基类
│   └── session.py   # 会话管理
├── models/       # SQLAlchemy数据模型
├── schemas/      # Pydantic模型
├── services/     # 业务逻辑服务
│   ├── auth.py      # 认证服务
│   ├── payment.py   # 支付服务
│   └── storage.py   # 存储服务
├── static/       # 静态文件
├── tests/        # 测试用例
│   ├── conftest.py  # 测试配置
│   └── api/         # API测试
└── utils.py      # 工具函数

alembic/          # 数据库迁移
├── versions/     # 迁移版本
└── env.py        # 迁移环境

uploads/          # 文件上传目录
public/           # 公共资源目录
```

## API文档

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

### 主要API端点

#### 认证相关

- POST `/api/v1/auth/login` - 用户登录
- POST `/api/v1/auth/refresh` - 刷新令牌
- POST `/api/v1/auth/logout` - 用户登出

#### 组织管理

- POST `/api/v1/organizations` - 创建组织
- GET `/api/v1/organizations` - 获取组织列表
- GET `/api/v1/organizations/{org_id}` - 获取组织详情
- PUT `/api/v1/organizations/{org_id}` - 更新组织信息

#### 成员管理

- POST `/api/v1/organizations/{org_id}/members` - 添加成员
- GET `/api/v1/organizations/{org_id}/members` - 获取成员列表
- PUT `/api/v1/organizations/{org_id}/members/{member_id}` - 更新成员信息

#### 论文管理

- POST `/api/v1/papers` - 上传论文
- GET `/api/v1/papers` - 获取论文列表
- GET `/api/v1/papers/{paper_id}` - 获取论文详情
- PUT `/api/v1/papers/{paper_id}` - 更新论文信息
- DELETE `/api/v1/papers/{paper_id}` - 删除论文

#### 支付系统

- POST `/api/v1/payments` - 创建支付订单
- GET `/api/v1/payments/{payment_id}` - 获取支付状态
- POST `/api/v1/payments/{payment_id}/verify` - 验证支付

## 数据库接口

详细的数据库接口文档请参考 [E-DBA External Database interface.md](E-DBA%20External%20Database%20interface.md)

## 测试

运行测试用例：

```bash
# 运行所有测试
pytest app/tests/

# 运行特定测试文件
pytest app/tests/test_auth.py

# 运行测试并显示覆盖率
pytest --cov=app app/tests/
```

## 部署

### 开发环境
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 生产环境
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

### 文档需求总结：教育数据湾区（E-DBA）设计与实现

#### **1. 项目概述**

- **目标**：为高等教育机构提供安全、透明、互操作的数据共享平台，支持以下核心功能：
  - 学生身份认证
  - 论文访问控制
  - 在线支付
  - 课程信息共享
  - （可选）数据保险库服务
- **参考模型**：基于IDS数据空间架构，但可扩展。

---

#### **2. 用户角色与权限**

| **角色**             | **职责**                                                                                     |
|----------------------|--------------------------------------------------------------------------------------------|
| **技术管理员（T-Admin）** | - 唯一存在，处理用户问题（登录频率：每日一次）<br>- 设置E-Admin和Senior E-Admin。           |
| **管理管理员（E-Admin）** | - 审批O-Convener的注册申请（3日内处理）<br>- 管理数据共享政策（增删改PDF文件）<br>- 查看全平台日志（按活动/用户/日期/组织过滤）。 |
| **高级管理管理员（Senior E-Admin）** | - 最终审批E-Admin通过的注册申请，通知O-Convener结果。                                      |
| **组织协调人（O-Convener）** | - 注册组织（需上传PDF证明文件及邮箱验证）<br>- 管理成员列表（Excel格式，支持通配符邮箱`*@domain`）<br>- 配置服务、支付账户及配额。 |
| **数据提供者/消费者**    | - 权限分三级：<br>  1. 公开数据访问（课程信息）<br>  2. 私有数据消费（论文下载、身份验证）<br>  3. 私有数据提供（配置服务接口）。 |

---

#### **3. 核心功能需求**
##### **3.1 工作区管理（O-Convener）**

- **注册与审批**：需通过邮箱验证，两步审批流程（E-Admin初审 → Senior E-Admin终审）。
- **成员管理**：支持Excel批量导入或手动编辑成员权限及论文下载配额（单位：RMB）。
- **服务配置**：
  - **必选服务**：课程信息共享（免费）、学生身份验证、论文共享。
  - **私有服务配置**：需绑定外部数据库接口（如学生信息库、论文库）。
  - **收费设置**：按使用次数收费（如身份验证按人次计费），由O-Convener自定义。
- **日志管理**：仅可查看本组织的活动日志（按用户/日期/操作过滤）。

##### **3.2 数据访问**

- **公开数据**：课程信息（支持关键词搜索）。
- **私有数据**：
  - **论文访问**：可设置下载权限（仅浏览或下载）及收费。
  - **学生身份验证**：输入学生基本信息或批量Excel文件，返回验证结果（Yes/No）。
  - **学生GPA记录**：输入方式同身份验证，返回姓名、入学/毕业年份及GPA（按记录数收费）。

##### **3.3 支付系统**

- **支付方式**：
  - 必选：银行转账（组织账户支付）。
  - 可选：PayPal、微信、支付宝、信用卡（可置灰未实现）。
- **支付失败处理**：用户需联系O-Convener处理。

##### **3.4 日志与审计**

- **记录内容**：用户登录/退出时间、访问的服务及服务提供组织。
- **权限**：E-Admin可查看全平台日志；O-Convener仅查看本组织日志。

##### **3.5 可选功能：数据保险库**

- **用途**：为无自主数据库的组织存储数据，按权限提供访问接口。
- **优先级**：非必选，不影响学期评分。

---

#### **4. 收费模型**

| **项目**               | **收费规则**                                                                 |
|------------------------|----------------------------------------------------------------------------|
| **会员费**             | - 权限1：1000元总费用或10元/人（由O-Convener选择）<br>- 权限2：100元/人<br>- 权限3：免费。 |
| **服务费**             | 由O-Convener自定义（如论文下载、身份验证按次收费）。                                     |
| **支付触发条件**       | 新增成员时触发会员费支付；服务使用时触发服务费支付（无退款机制）。                            |

---

#### **5. 外部接口需求（测试用）**

- **学生信息库**：提供身份验证（输入姓名、ID、照片）和记录查询接口。
- **论文库**：支持关键词搜索论文列表及标题精确下载PDF。
- **银行账户验证**：接口验证账户有效性及转账功能（输入银行名、账户名、账号、密码）。

---

#### **6. 非功能需求**

- **安全性**：日志不可篡改；支付密码字段隐藏。
- **可用性**：用户问题通过"Seek Help"提交，T-Admin回复后显示星标。
- **合规性**：需遵守数据主权法规（如政策文件上传至平台）。

---

#### **7. 附录与扩展**

- **成员表示例**：包含姓名、邮箱（支持通配符）、权限级别及下载配额。
- **政策管理**：支持PDF格式的政策文件（如版权政策、隐私政策）。
- **扩展性**：未来可集成更多服务（如保险库），当前仅实现核心功能。

**注**：需求可能进一步细化，需关注后续版本更新。
