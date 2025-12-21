from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.scrapers.boss_scraper import BossScraper
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

scraper_status = {
    "running": False,
    "current_source": None,
    "jobs_scraped": 0,
    "message": ""
}

def run_scraper_task(source: str, keyword: str, location: str, pages: int, db: Session):
    global scraper_status

    try:
        scraper_status["running"] = True
        scraper_status["current_source"] = source
        scraper_status["jobs_scraped"] = 0

        sources_to_scrape = []
        if source == "all":
            sources_to_scrape = ["boss", "zhaopin", "51job", "lagou"]
        else:
            sources_to_scrape = [source]

        total_scraped = 0

        for src in sources_to_scrape:
            scraper_status["current_source"] = src

            if src == "boss":
                scraper = BossScraper(db)
                count = scraper.run(keyword=keyword, location=location, pages=pages)
                total_scraped += count

        scraper_status["jobs_scraped"] = total_scraped
        scraper_status["message"] = f"成功爬取 {total_scraped} 条职位信息"
        scraper_status["running"] = False

    except Exception as e:
        logger.error(f"爬虫任务失败: {str(e)}")
        scraper_status["message"] = f"爬虫任务失败: {str(e)}"
        scraper_status["running"] = False

@router.post("/run", response_model=schemas.ScraperResponse)
async def run_scraper(
    request: schemas.ScraperRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    if scraper_status["running"]:
        raise HTTPException(status_code=400, detail="爬虫任务正在运行中，请稍后再试")

    valid_sources = ["boss", "zhaopin", "51job", "lagou", "all"]
    if request.source not in valid_sources:
        raise HTTPException(status_code=400, detail=f"无效的数据源，支持: {', '.join(valid_sources)}")

    if request.source != "boss":
        raise HTTPException(status_code=501, detail=f"{request.source} 爬虫暂未实现，目前仅支持 Boss直聘")

    background_tasks.add_task(
        run_scraper_task,
        source=request.source,
        keyword=request.keyword,
        location=request.location or "",
        pages=request.pages or 1,
        db=db
    )

    return schemas.ScraperResponse(
        status="started",
        message=f"爬虫任务已启动，正在爬取 {request.source} 的职位信息"
    )

@router.get("/status")
def get_scraper_status():
    return scraper_status
