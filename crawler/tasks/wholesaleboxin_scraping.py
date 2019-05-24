website_url = 'https://wholesalebox.in/'

def format_categories(category):
    return {
        'title': category['link_title'],
        'url': category['href'],
        'category_id': int(category['value']),
        'meta': category,
    }

def format_product(product):
    return {
        'product_id': product['product_id'],
        'title': product['heading_title'],
        'country_origin': product['pickup_city'],
        'price': int(product['price_value']),
        'rating': product['rating'],
        'url': website_url + product['href'],
        'meta': product,
    }

def scrape_categories():
    from crawler.crawlers.wholesaleboxin_crawler import WholeSaleBoxInCategoryCrawler
    from crawler.models import Category, Site

    site = Site.objects.get(url=website_url)
    category_crawler = WholeSaleBoxInCategoryCrawler()
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


def scrape_category_products(category_id, page=5, from_page=1):
    from crawler.crawlers.wholesaleboxin_crawler import WholeSaleBoxInProductCrawler
    from crawler.models import Product, Category
    category = Category.objects.get(category_id=category_id)
    crawler = WholeSaleBoxInProductCrawler(
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

