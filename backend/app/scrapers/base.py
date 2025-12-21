from abc import ABC, abstractmethod
import requests
import time
import random
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app import crud, schemas
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self, db: Session, source_name: str):
        self.db = db
        self.source_name = source_name
        self.ua = UserAgent()
        self.session = requests.Session()

    def get_headers(self):
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

    def fetch_page(self, url: str, max_retries: int = 3):
        for attempt in range(max_retries):
            try:
                response = self.session.get(
                    url,
                    headers=self.get_headers(),
                    timeout=10
                )
                response.raise_for_status()
                return response
            except Exception as e:
                logger.warning(f"请求失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    logger.error(f"请求最终失败: {url}")
                    return None

    def random_delay(self, min_sec: float = 2.0, max_sec: float = 5.0):
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def normalize_salary(self, salary_str: str):
        if not salary_str:
            return None, None

        salary_str = salary_str.lower().replace(' ', '').replace('，', ',')

        match = re.search(r'(\d+)[k|K]?[-~—至](\d+)[k|K]?', salary_str)
        if match:
            min_salary = int(match.group(1)) * 1000
            max_salary = int(match.group(2)) * 1000
            return min_salary, max_salary

        match = re.search(r'(\d+)[k|K]', salary_str)
        if match:
            salary = int(match.group(1)) * 1000
            return salary, salary

        return None, None

    def save_job(self, job_data: dict):
        try:
            existing_job = crud.get_job_by_job_id(self.db, job_data['job_id'])
            if existing_job:
                logger.info(f"职位已存在，跳过: {job_data['title']}")
                return False

            job_create = schemas.JobCreate(**job_data)
            crud.create_job(self.db, job_create)
            logger.info(f"保存职位成功: {job_data['title']} - {job_data['company']}")
            return True

        except Exception as e:
            logger.error(f"保存职位失败: {str(e)}")
            self.db.rollback()
            return False

    @abstractmethod
    def parse_job_list(self, html: str):
        pass

    @abstractmethod
    def parse_job_detail(self, html: str):
        pass

    @abstractmethod
    def build_search_url(self, keyword: str, location: str, page: int):
        pass

    def run(self, keyword: str, location: str = "", pages: int = 1):
        logger.info(f"开始爬取 {self.source_name}: 关键词={keyword}, 地点={location}, 页数={pages}")

        total_saved = 0

        for page in range(1, pages + 1):
            url = self.build_search_url(keyword, location, page)
            logger.info(f"正在爬取第 {page} 页: {url}")

            response = self.fetch_page(url)
            if not response:
                logger.warning(f"第 {page} 页获取失败")
                continue

            job_urls = self.parse_job_list(response.text)
            logger.info(f"第 {page} 页找到 {len(job_urls)} 个职位")

            for job_url in job_urls:
                self.random_delay(2, 4)

                detail_response = self.fetch_page(job_url)
                if not detail_response:
                    continue

                job_data = self.parse_job_detail(detail_response.text)
                if job_data:
                    job_data['source'] = self.source_name
                    job_data['url'] = job_url
                    if self.save_job(job_data):
                        total_saved += 1

            self.random_delay(3, 6)

        logger.info(f"爬取完成，共保存 {total_saved} 个职位")
        return total_saved
