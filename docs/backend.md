- 确保 Cookie 已配置 ：确认 configs/config.yaml 中填入了有效的 Pixiv PHPSESSID ，并且根据你的网络情况设置了代理开关。
- 访问 API 文档 ：在浏览器打开 http://127.0.0.1:8000/docs 。
- 测试搜索 ：
- 找到 GET /novel/search 接口。
- 点击 "Try it out"。
- 输入一个关键词（例如 "原神" 或你感兴趣的任何标签）。
- 点击 "Execute"。
- 查看 Response Body 是否返回了小说列表。


NEW：12.17

- 实现核心服务 ( backend/app/services/novel_service.py )

- search(keyword, page) : 搜索小说。
- get_info(novel_id) : 获取小说详情。
- get_content(novel_id) : 获取小说正文。
- download(novel_id) : 下载小说并格式化为文本文件。
- 添加 API 接口 ( backend/app/routers/novel.py )

- GET /novel/search : 搜索接口。
- GET /novel/{id} : 详情接口。
- GET /novel/{id}/download : 下载接口（直接返回文件流）。
- 增强基础设施

- 配置管理 : 修改了 backend/app/core/config.py ，使其能够读取 configs/config.yaml 。
- HTTP 客户端 : 升级了 backend/app/utils/http.py ，支持 Cookie 认证 、 代理 (Proxy) 和 User-Agent 伪装 ，以应对 Pixiv 的访问限制。
- 依赖 : 在 requirements.txt 中添加了 PyYAML 。