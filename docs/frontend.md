前端代码
的操作
 Web 前端项目结构
frontend_web/
├── index.html
├── package.json
├── vite.config.ts
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── api/                 # 后端 API 封装（重点）
│   │   ├── http.ts
│   │   ├── novel.ts
│   │   ├── auth.ts
│   │   └── version.ts
│   ├── pages/
│   │   ├── Home.vue         # 搜索小说
│   │   ├── Novel.vue        # 小说详情
│   │   └── Settings.vue
│   ├── components/
│   │   ├── NovelList.vue
│   │   └── DownloadButton.vue
│   └── router/
│       └── index.ts


api/ 目录是未来 Qt API client 的“蓝本”

12.20

原型前端遇到问题，后端接口返回正确函数，前端出现错误
frontend_web/prototype_test
todo:解决bug


12.23

原型前端问题解决，后端接口返回为正常的状态码，前端状态码进行判断

12.23

series接口修复，兼容性提升
vue+ts兼容在pycharm中修复



