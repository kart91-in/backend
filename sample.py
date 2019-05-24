# from crawler.tasks.wholesaleboxin_scraping import scrape_categories, scrape_category_products
#
# # scrape_categories()
#
# scrape_category_products(245)
#
from crawler.models import Product

p = Product.objects.values('id', 'meta')

for pro in p:
    url = 'https://wholesalebox.in/' + pro['meta']['href']
    x = Product.objects.filter(id=pro['id']).update(url=url)
