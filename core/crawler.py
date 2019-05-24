
import requests


class BaseCrawler(object):

    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    @property
    def session(self):
        if not hasattr(self, '_session'):
            self._session = requests.Session()
        return self._session

    def post(self, url, params=None, data=None, headers=None):
        headers = headers or {}
        params = params or {}
        data = data or {}
        return self.session.post(url, params=params, data=data, headers={**self.default_headers, **headers})

    def get(self, url, params=None, headers=None):
        headers = headers or {}
        params = params or {}
        return self.session.get(url, params=params, headers={**self.default_headers, **headers})

    def start_crawl(self):
        params = {
            'path': 245,
            'page': 1,
            'sort': 'p.date_added',
            'order': 'DESC',
            'filter': '',
            'option': '',
            'ratingrating_filter': '',
            'price_filter': '',
        }
        url = 'https://www.wholesalebox.in/api/category/product_list'
        headers = {'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        data = {'client_preferences': []}

        resp = self.post(url, params, headers, data)

        if resp.ok:
            data = resp.json()
            for product_data in data['data']['products']:
                yield product_data
        else:
            pass

