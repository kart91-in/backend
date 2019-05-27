import json
from .base_crawler import BaseCrawler


class LimeRoadComProductCrawler(BaseCrawler):
    _last_result = None

    def __init__(self, **kwargs):
        self.from_page = kwargs.get('from_page') or 1
        self.page = kwargs.get('page') or -1
        self.category_id = kwargs.get('category_id')
        self.stop_product_id = kwargs.get('stop_product_id')

    def start_crawl(self):
        params = {
            's_start': 0,
            'p_queryparam': json.dumps({"classification":[self.category_id],"stock":["1"]}),
            'p_sortorder': 'threeQuarterStock_i+desc,created+desc',
            's_queryparam': json.dumps({"classification":[self.category_id],"stock":["1"]}),
            's_sortorder': 'threeQuarterStock_i+desc,created+desc',
            'isScrapOnlySearch': None,
            'group': False,
            'tag':'' ,
            'tag_condition': "",
            'issearch': False,
            'facets': 1,
            'product_id':'' ,
            'p_searchquery': '*:*',
            's_searchquery': '*:*',
            'ajax': True,
            'filterApply': True,
        }
        url = 'https://www.limeroad.com/listing/get_listing_objects/'
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        i = self.from_page
        while i <= self.page or self.page == -1:
            params['p_start'] = (i - 1) * 8
            i += 1
            resp = self.get(url, params, headers)
            if resp.ok:
                html = self.html(resp.text)
                item_tags = html.select('.fadeInUp.m6')
                for tag in item_tags:
                    product_id = tag.select_one('[id]').get('id')
                    if self.stop_product_id and self.stop_product_id == product_id:
                        break
                    price_sale = tag.select_one('.dIb.vM.c3.fs14')
                    price_sale = int(price_sale.get_text().replace('₹', '')) if price_sale else None
                    price = tag.select_one('.tdS.dIb.vM.fs12.c9')
                    price = int(price.get_text().replace('₹', '')) if price else None
                    product_url = tag.select_one('a').get('href')
                    store = tag.select_one('.tdN.wsN')
                    store_url = store.get('href')
                    store_name = store.get_text().replace('by ', '')
                    image = tag.select_one('img').get('data-src')

                    yield {
                        'product_id': product_id,
                        'price_sale': price_sale,
                        'image': image,
                        'price': price,
                        'store_url': 'https://www.limeroad.com' + store_url,
                        'store_name': store_name.strip(),
                        'url': 'https://www.limeroad.com' + product_url,
                    }

class LimeRoadComCategoryCrawler(BaseCrawler):

    def start_crawl(self):
        resp = self.get('https://www.limeroad.com/get_nav_categories?ajax=true')
        if resp.ok:
            html = self.html(resp.text)
            category_tags = html.select('a[data-obj="impAjaxMenuCloseLog"]')
            for tag in category_tags:
                attr_json = json.loads(tag.get('data-tr')).get('doid')
                yield {
                    'title': tag.get_text(),
                    'category_id': attr_json.replace('category:',''),
                    'url': 'https://www.limeroad.com' + tag.get('href'),
                }