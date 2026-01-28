from fastapi import FastAPI
from .routers import auth, proxy, version, config, novel, series
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from .core.exceptions import validation_error_handler, general_exception_handler
from .core.logger import setup_logging, get_logger

setup_logging(log_level="INFO")
logger = get_logger(__name__)

app = FastAPI(
    title="Pixiv Novel Downloader API",
    description="Pixiv 小说下载 API",
    version="1.1.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Pixiv Novel Downloader API",
        "docs_url": "/docs",
        "version": "1.1.0"
    }

# 注册异常处理器
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 注册路由
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(proxy.router, prefix="/proxy", tags=["Proxy"])
app.include_router(version.router, prefix="/version", tags=["Version"])
app.include_router(config.router, prefix="/config", tags=["Config"])
app.include_router(novel.router, prefix="/novel", tags=["Novel"])
app.include_router(series.router, prefix="/series", tags=["Series"])

# 允许跨端口调试
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 原型阶段 OK
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
