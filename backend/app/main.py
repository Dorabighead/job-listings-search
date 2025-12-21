from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import jobs, favorites, scraper
import os
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="就业信息爬取系统",
    description="自动爬取多个招聘网站的职位信息，提供搜索、筛选、收藏、导出功能",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(favorites.router, prefix="/api/favorites", tags=["favorites"])
app.include_router(scraper.router, prefix="/api/scraper", tags=["scraper"])

@app.get("/")
def root():
    return {
        "message": "欢迎使用就业信息爬取系统 API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
