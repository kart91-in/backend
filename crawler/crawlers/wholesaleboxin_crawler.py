from .base_crawler import BaseCrawler


class WholeSaleBoxInProductCrawler(BaseCrawler):
    _last_result = None

    def __init__(self, **kwargs):
        self.from_page = kwargs.get('from_page') or 1
        self.page = kwargs.get('page') or -1
        self.category_id = kwargs.get('category_id')

    def start_crawl(self):
        params = {
            'path': self.category_id,
            'page': 1,
            'sort': 'p.date_added',
            'order': 'DESC',
            'filter': '',
            'option': '',
            'rating_filter': '',
            'price_filter': '',
            'search': '',
            'location': '',
            'store_code': '',
            'stock_filter': 0,
            'store_product': 0,
            'purchase_days': 0,
            'clearance_sale': 'undefined',
            'last_filter_action': 0,
        }
        url = 'https://www.wholesalebox.in/api/category/product_list'
        headers = {'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        data = {'client_preferences': "[]"}

        i = self.from_page
        while i < self.page or self.page == -1:
            params['page'] = i
            if i > 1:
                resp = self.get(url, params, headers)
            else:
                resp = self.post(url, params, data, headers)
            i += 1
            if resp.ok:
                data = resp.json()['data']
                if data['products'] == self._last_result:
                    print('no new results')
                    break

                if not hasattr(self, '_total_products'):
                    self._total_products = data['product_total']
                for product_data in data['products']:
                    yield product_data
                self._last_result = data['products']
            else:
                print('no Response')
                break


class WholeSaleBoxInCategoryCrawler(BaseCrawler):

    def start_crawl(self):
        resp = self.get('https://www.wholesalebox.in/api/header/menu')
        if resp.ok:
            categories = resp.json()['data']
            for child_category in categories['menus']:
                for category in child_category['children']:
                    if category.get('children'):
                        for cate in category.get('children'):
                            yield cate
                    else:
                        yield category
            for category in categories['preference_menu'][0]['children']:
                yield category
