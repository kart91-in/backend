website_url = 'https://www.limeroad.com/'

def format_categories(category):
    return {
        **category,
        'meta': category,
    }

def format_product(product):
    return {
        'product_id': product['product_id'],
        'price': product['price_sale'],
        'url': product['url'],
        'meta': product,
    }

def scrape_categories():
    from crawler.models import Category, Site
    from crawler.crawlers.limeroadcom_crawler import LimeRoadComCategoryCrawler
    site = Site.objects.get(url=website_url)
    category_crawler = LimeRoadComCategoryCrawler()
    categories_data = category_crawler.start_crawl()

    for category in categories_data:
        try:
            formatted_category = format_categories(category)
            formatted_category['site'] = site
            Category.objects.update_or_create(
                site=site,
                category_id=formatted_category['category_id'],
                defaults=formatted_category
            )
        except Exception as e:
            continue


def scrape_category_products(category_id, page=-1, from_page=1):
    from crawler.crawlers.limeroadcom_crawler import LimeRoadComProductCrawler
    from crawler.models import Product, Category
    category = Category.objects.get(category_id=category_id)
    latest_product_id = Product.objects.filter(category=category)\
        .order_by('-created_at').values('id').first()
    crawler = LimeRoadComProductCrawler(
        stop_product_id=latest_product_id,
        category_id=category_id,
        page=page,
        from_page=from_page,
    )
    data = crawler.start_crawl()

    for product in data:
        try:
            formatted_product = format_product(product)
            formatted_product['category'] = category
            Product.objects.update_or_create(
                category=category,
                product_id=formatted_product['product_id'],
                defaults=formatted_product
            )
        except Exception as e:
            raise e

