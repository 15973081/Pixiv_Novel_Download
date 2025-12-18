from fastapi import FastAPI
from .routers import auth, proxy, version, config, novel, series

app = FastAPI(title="My Backend API")

@app.get("/")
def root():
    return {"message": "Welcome to Pixiv Novel Downloader API", "docs_url": "/docs"}

# 注册路由
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(proxy.router, prefix="/proxy", tags=["Proxy"])
app.include_router(version.router, prefix="/version", tags=["Version"])
app.include_router(config.router, prefix="/config", tags=["Config"])
app.include_router(novel.router, prefix="/novel", tags=["Novel"])
app.include_router(series.router, prefix="/series", tags=["Series"])