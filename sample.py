from crawler.crawlers.limeroadcom_crawler import LimeRoadComProductCrawler
from crawler.tasks.limeroadcom_scraping import scrape_categories, scrape_category_products

scrape_category_products('.0.1116.1240.1245', 50)
