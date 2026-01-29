# Pixiv Novel Downloader

Pixiv 小说下载 API 服务

<div align="center">

<!-- 状态与版本徽章 -->
<img src="https://img.shields.io/badge/version-1.1.0-2E7D32" alt="Version">
<img src="https://img.shields.io/badge/license-MIT-01579B" alt="License">
<img src="https://img.shields.io/badge/status-active-4CAF50" alt="Status">
<img src="https://img.shields.io/badge/code_style-ruff-FFB300" alt="Code Style">

<!-- 技术栈图标徽章（横向排列） -->
<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/uvicorn-009688?logo=uvicorn&logoColor=white" alt="Uvicorn">
<img src="https://img.shields.io/badge/requests-FF9800?logo=requests&logoColor=white" alt="Requests">
<img src="https://img.shields.io/badge/Playwright-2EAD33?logo=playwright&logoColor=white" alt="Playwright">

</div>


## 概览

Pixiv Novel Downloader 是一个基于 FastAPI 的后端服务，提供 Pixiv 小说内容的检索、下载和管理功能。该服务通过 RESTful API 接口支持小说搜索、系列管理、批量下载等核心操作，并集成浏览器模拟登录和代理支持。

主要面向开发者提供 API 服务，可集成到桌面客户端或 Web 应用中。与直接爬取方案相比，本服务采用官方 API 接口，配合浏览器 Token 认证机制，提供更稳定的数据获取能力。

## 核心特性

- 小说搜索：支持关键词搜索、分页查询、多种排序模式
- 系列管理：支持系列信息获取、批量下载、合并/分拆导出
- 认证机制：支持浏览器 Token 认证、模拟登录
- 代理支持：内置代理配置、代理测试接口(默认代理端口为7890)
- 错误处理：统一的异常处理机制、详细的错误信息
- 日志系统：结构化日志输出、可配置日志级别

## 技术栈

| 类别       | 技术                  | 版本要求      | 说明                     |
|------------|-----------------------|---------------|--------------------------|
| 语言       | Python                | ≥3.10         | 主开发语言               |
| 框架       | FastAPI               | ≥0.100.0      | Web 框架                 |
| 服务器     | Uvicorn               | ≥0.20.0       | ASGI 服务器              |
| HTTP 客户端| Requests              | ≥2.28.0       | HTTP 请求封装            |
| 浏览器自动化| Playwright            | ≥1.40.0       | 浏览器模拟登录          |
| 配置管理   | PyYAML                | ≥6.0          | YAML 配置解析           |
| 异步IO     | Anyio                 | ≥3.0.0        | 异步IO库               |
| 数据验证   | Pydantic              | ≥2.7.0        | 数据验证和序列化        |
| ASGI框架   | Starlette             | ≥0.40.0       | ASGI工具包            |
| 代码质量   | Ruff                  | ≥0.1          | 代码检查和格式化        |

## 快速开始

最短路径启动（可直接复制执行）

```bash
git clone https://github.com/yourusername/pixiv-novel-download.git
cd pixiv-novel-download/backend
pip install -r requirements.txt
python run.py
```

服务启动后访问 http://localhost:8000/docs 查看 API 文档

## 开发环境要求

| 组件         | 最低版本 | 推荐版本 | 说明                |
|--------------|----------|----------|---------------------|
| Python       | 3.10     | 3.10+    | 解释器             |
| pip          | 23.0     | 最新     | 包管理器           |
| Git          | 2.30     | 最新     | 版本控制           |
| 浏览器       | —        | Chrome   | Playwright 依赖    |

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/pixiv-novel-download.git
cd pixiv-novel-download
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 4. 安装 Playwright 浏览器

```bash
playwright install chromium
```

### 5. 启动服务

```bash
python run.py
```

## 配置说明

### 环境变量

| 变量名             | 默认值    | 说明                    |
|--------------------|-----------|-------------------------|
| LOG_LEVEL          | INFO      | 日志级别                |
| API_HOST           | 0.0.0.0   | API 服务监听地址        |
| API_PORT           | 8000      | API 服务监听端口        |

### 配置文件

核心配置位于 `backend/app/core/config.py`：

```python
app_config = {
    "api_version": "1.1.0",
    "base_url": "https://www.pixiv.net/ajax",
    "default_page_size": 30,
    "supported_formats": ["txt"],
    "auth": {
        "cookie": ""
    },
    "proxy": {
        "enabled": False,
        "http": "",
        "https": ""
    }
}
```

## 开发常用命令

### 代码检查

```bash
# 运行 ruff 检查
ruff check backend

# 自动修复问题
ruff check backend --fix
```

### 服务启动

```bash
# 开发模式启动
python run.py

# 使用 uvicorn 直接启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 依赖管理

```bash
# 导出依赖
pip freeze > requirements.txt

# 安装依赖
pip install -r requirements.txt
```

## 目录结构

<details>
<summary>展开查看完整目录结构</summary>

```
pixiv_novel_download/
│
├── backend/                     # 后端 FastAPI 服务
│   ├── app/
│   │   ├── main.py              # FastAPI 启动入口
│   │   ├── routers/             # API 路由
│   │   │   ├── auth.py          # 认证接口
│   │   │   ├── proxy.py         # 代理服务接口
│   │   │   ├── version.py       # 版本检查接口
│   │   │   ├── config.py        # 配置读取接口
│   │   │   ├── novel.py         # 小说相关接口
│   │   │   └── series.py        # 系列相关接口
│   │   ├── core/
│   │   │   ├── config.py        # 配置加载
│   │   │   ├── security.py      # token/sign 加密
│   │   │   ├── browser.py       # 浏览器模拟登录
│   │   │   ├── exceptions.py    # 异常处理
│   │   │   └── logger.py        # 日志配置
│   │   ├── services/
│   │   │   ├── login_service.py # 登录服务
│   │   │   ├── proxy_service.py # 代理服务
│   │   │   ├── version_service.py # 版本服务
│   │   │   ├── novel_service.py # 小说服务
│   │   │   └── series_service.py # 系列服务
│   │   ├── utils/
│   │   │   ├── http.py          # HTTP 客户端封装
│   │   │   └── tools.py        # 工具函数
│   │   └── __init__.py
│   ├── requirements.txt
│   └── run.py                   # 后端启动脚本
│
├── frontend_qt/                 # 桌面客户端（可选）
│   ├── main.py                  # Qt 入口
│   ├── api/                     # API 客户端
│   ├── ui/                      # UI 文件
│   └── components/              # UI 组件
│
├── scripts/                     # 独立脚本
│   ├── get_browser_token.py
│   ├── simulate_login.py
│   └── proxy_test.py
│
├── configs/
│   ├── config.yaml              # 全局配置
│   └── proxy_list.yaml         # 代理列表
│
├── tests/
│   ├── test_login.py
│   ├── test_proxy.py
│   └── test_version.py
│
└── README.md
```

</details>

## 测试与质量控制

### 代码质量检查

```bash
# 运行 ruff 检查
ruff check backend

# 自动修复
ruff check backend --fix
```

### 测试执行

```bash
#安装测试
pip install pytest pytest-cov

# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_login.py

# 生成覆盖率报告
pytest tests/ --cov=app --cov-report=html
```

### 质量标准

- 代码检查：通过 Ruff 检查，无警告
- 测试覆盖率：核心模块 ≥80%
- API 文档：所有接口包含完整文档字符串

## 部署指南

### Docker 部署

```bash
# 构建镜像
docker build -t pixiv-novel-downloader .

# 运行容器
docker run -d -p 8000:8000 pixiv-novel-downloader
```

### 生产环境配置

建议使用 Gunicorn + Uvicorn workers：

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### 反向代理配置

Nginx 配置示例：

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## 外部依赖

| 依赖名称          | 用途              | 授权协议    |
|-------------------|-------------------|-------------|
| Pixiv API         | 数据获取          | Pixiv ToS   |
| Chromium          | 浏览器自动化      | BSD         |
| FastAPI           | Web 框架          | MIT         |
| Requests          | HTTP 客户端       | Apache 2.0  |

## 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 遵循 PEP 8 规范
- 使用 Ruff 进行代码检查
- 添加必要的类型注解
- 编写单元测试覆盖新功能

## 开源许可

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 参考文档

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pixiv API](https://www.pixiv.net/ajax/)
- [Playwright 文档](https://playwright.dev/python/)
- [Uvicorn 文档](https://www.uvicorn.org/)
