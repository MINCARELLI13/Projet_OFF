# coding: utf-8
import requests
from Config.config import categories, fields_of_products, products_nb, url


class Request_Api:
    """ contains all the requests to practice on OpenFoodFacts's API """

    def get_products_of_category(self, catg_name):
        """
        For each category of products makes a request to OpenFoodFacts API
        """
        parameters_request_API = {
            'action': 'process', 'tagtype_0': 'categories',
            'tag_contains_0': 'contains', 'tag_0': catg_name,
            'fields': ','.join(fields_of_products),
            'page_size': products_nb, 'json': 'true'}

        req = requests.get(url, params=parameters_request_API)
        # selects only useful informations on products
        return req.json().get('products')


if __name__=='__main__':
    request_api = Request_Api()
    request_api.filling_table_Product()