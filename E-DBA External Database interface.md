
## 📄 一、文档概述

本文档是 SE_SDW_Project Long Description 中第 4.3 节“外部数据库接口”的补充说明。

- 提供了一个组织（Test-A）的6个API接口信息。
- 提供了学生数据、论文数据和银行账户数据样例。
- 描述了如何在 E-DBA 系统中**动态配置并调用外部 API 接口**。
- 给出了推荐的数据表结构和动态调用代码示例。

---

## 🔌 二、组织提供的接口（共6个）

| 接口路径 | 方法 | 功能说明 |
|---------|------|----------|
| `/hw/student/authenticate` | POST | 学生认证（姓名、学号、照片） |
| `/hw/student/record` | POST | 获取学生GPA及年份信息 |
| `/hw/thesis/search` | POST | 根据关键词搜索论文 |
| `/hw/thesis/pdf` | POST | 获取论文PDF路径 |
| `/hw/bank/authenticate` | POST | 银行账户认证 |
| `/hw/bank/transfer` | POST | 模拟银行转账 |

### ✅ 输入输出格式示例

#### ➤ `/hw/student/record`

```json
输入：
{
  "name": "string",
  "id": "string"
}

输出：
{
  "name": "string",
  "enroll_year": "string",
  "graduation_year": "string",
  "gpa": float
}
```

其他接口类似，可查看原始文档获取详细参数。

---

## 🛠️ 三、学生与论文接口的实现步骤（2.x）

### 步骤 1：设计前端界面用于配置接口信息

- 提供给组织（如Test-A）填写以下信息：
  - `Base URL`
  - `Path`
  - `Method (GET/POST)`
  - `Input Format（JSON）`
  - `Output Format（JSON）`
- 示例 UI 设计可自行设计或参考文档中的提示。

### 步骤 2：系统保存配置信息到数据库

建议创建一个表来存储配置：

```sql
CREATE TABLE api_config (
    id SERIAL PRIMARY KEY,
    institution_id INT NOT NULL,
    base_url VARCHAR(255) NOT NULL,
    path VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    input JSONB,
    output JSONB, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 步骤 3：系统后端动态调用接口

- 查询数据库 `api_config` 获取对应机构的接口配置。
- 构建请求体并发起 HTTP 请求（POST / GET）。
- 返回结果由前端渲染显示。

#### Python 伪代码示例：
```python
institution_id = 1
# 从数据库读取配置
base_url = '...'  
path = '/hw/student/record'
method = 'POST'

url = base_url + path
inputs = {"name":"string","id":"string"} 

# 用户输入数据
data_to_send = {
    "name": "Alice Huang",
    "id": "S20230001"
}

final_payload = {key: data_to_send.get(key, "") for key in inputs.keys()}

if method == 'POST':
    response = requests.post(url, json=final_payload)
elif method == 'GET':
    # TODO
```

### 步骤 4：提供前端UI基于接口配置自动生成查询页面

- 根据接口需要的字段数量自动生成对应的输入框。
- 例如 `/hw/student/record` 需要 name 和 id，则前端展示两个输入框。
- 若某接口配置了3个输入字段，前端需展示3个输入区域。

### 步骤 5：支持接口配置变更

- 允许组织修改接口配置信息。
- 不影响系统运行，配置应动态加载。

---

## 💳 四、银行接口实现说明

### 实现方式：

- 将银行接口配置写入文本文件（*.txt），由 E-DBA 系统读取使用。
- 文件内容虽在文档中未给出，但逻辑上应包括：
  - 银行名
  - 账户名
  - 账号
  - 密码
  - 其他必要字段

### 更新方法：

- 直接修改 TXT 配置文件即可完成更新，无需重启系统。

---

## ⚠️ 五、未正确配置接口的结果

- 如果不能实现动态配置：
  - 可将接口信息硬编码进程序。
  - 但会扣分。

---

## 🧾 六、附录：测试数据样本（仅供学习）

### 👩‍🎓 学生数据示例（3条）

```json
[
  {
    "name": "Alice Huang",
    "id": "S20230001",
    "enroll": "2020",
    "grad": "2024",
    "gpa": 3.75,
    "photo": "static/photos/alice.jpg" 
  },
  ...
]
```

### 📝 论文数据示例（6篇）

```json
[
  {
    "title": "AI in Education and Learning Systems",
    "abstract": "This paper discusses the topic: AI in Education and Learning Systems in detail."
  },
  ...
]
```

### 💰 银行账户数据（6组）

```json
[
  {
    "name": "Campus Cash Cooperative",
    "account": "641387141765274",
    "password": "8799",
    "bank": "Global Education Bank",
    "balance": 26932724.07
  },
  ...
],
```

---

## 🧱 七、开发建议与注意事项

- **禁止硬编码接口信息**，除非不得已而为之（会被扣分）。
- 所有接口名称、路径、输入输出格式都应从数据库动态获取。
- 前端界面应根据接口定义自适应生成输入控件。
- 测试时可以访问提供的模拟[测试网站](http://172.16.160.88:8899/tester.html)
- 注意照片资源需从 iSpace 下载（附加说明可能在课程平台）。

---

## 🗃️ 附注：术语表 & 缩略词解释

| 缩写/术语 | 含义 |
|----------|------|
| E-DBA | External Database Agent，即外部数据库代理 |
| Test-A | 本示例中演示的机构名称 |
| iSpace | 教学平台（假设为教师指定下载附件的地方）|
