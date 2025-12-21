from app.scrapers.base import BaseScraper
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)

class BossScraper(BaseScraper):
    def __init__(self, db):
        super().__init__(db, "boss")
        self.base_url = "https://www.zhipin.com"

    def build_search_url(self, keyword: str, location: str, page: int):
        city_code = self.get_city_code(location)
        query_keyword = keyword.replace(' ', '%20')

        url = f"{self.base_url}/web/geek/job?query={query_keyword}&city={city_code}&page={page}"
        return url

    def get_city_code(self, location: str):
        city_map = {
            "北京": "101010100",
            "上海": "101020100",
            "广州": "101280100",
            "深圳": "101280600",
            "杭州": "101210100",
            "成都": "101270100",
            "武汉": "101200100",
            "西安": "101110100",
            "南京": "101190100",
            "": "100010000"
        }
        return city_map.get(location, "100010000")

    def parse_job_list(self, html: str):
        soup = BeautifulSoup(html, 'lxml')
        job_urls = []

        job_cards = soup.select('.job-card-wrapper')

        for card in job_cards:
            link = card.select_one('a.job-card-left')
            if link and link.get('href'):
                job_url = self.base_url + link['href']
                job_urls.append(job_url)

        return job_urls

    def parse_job_detail(self, html: str):
        try:
            soup = BeautifulSoup(html, 'lxml')

            job_id_match = re.search(r'job_detail/(\w+)\.html', html)
            if not job_id_match:
                logger.warning("无法提取职位ID")
                return None

            job_id = f"boss_{job_id_match.group(1)}"

            title_elem = soup.select_one('.job-title .name')
            title = title_elem.text.strip() if title_elem else ""

            company_elem = soup.select_one('.company-name a')
            company = company_elem.text.strip() if company_elem else ""

            salary_elem = soup.select_one('.salary')
            salary_str = salary_elem.text.strip() if salary_elem else ""
            salary_min, salary_max = self.normalize_salary(salary_str)

            location_elem = soup.select_one('.location-address')
            location = location_elem.text.strip() if location_elem else ""
            if location:
                location = location.split('·')[0].strip()

            tags = soup.select('.tag-list .tag-item')
            experience = ""
            education = ""
            for tag in tags:
                text = tag.text.strip()
                if '经验' in text or '年' in text:
                    experience = text
                elif '学历' in text or '本科' in text or '大专' in text or '硕士' in text:
                    education = text

            description_elem = soup.select_one('.job-detail-section .text')
            description = description_elem.text.strip() if description_elem else ""

            welfare_tags = soup.select('.job-tag-list .tag-item')
            welfare = ', '.join([tag.text.strip() for tag in welfare_tags])

            job_data = {
                'job_id': job_id,
                'title': title,
                'company': company,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'location': location,
                'experience': experience,
                'education': education,
                'job_type': '全职',
                'description': description,
                'requirements': description,
                'welfare': welfare
            }

            return job_data

        except Exception as e:
            logger.error(f"解析职位详情失败: {str(e)}")
            return None
