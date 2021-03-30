""" This module is used to search products on OpenFoodFats """
# coding: utf-8
import requests


class RequestApi:
    """ contains all the requests made on OpenFoodFacts's API """

    def get_products_of_category(self, catg_name, fields_products_api, products_nb, url):
        """
        For each category of products makes a request to OpenFoodFacts API
        In reception : all parameters to make request to API's OFF
        On return    : list of dictionaries where each dictionary
                        contains all information on one product
        """
        parameters_request_api = {
            'action': 'process', 'tagtype_0': 'categories',
            'tag_contains_0': 'contains', 'tag_0': catg_name,
            'fields': ','.join(fields_products_api),
            'page_size': products_nb, 'json': 'true'}

        req = requests.get(url, params=parameters_request_api)
        # selects only useful informations on products
        return req.json().get('products')


if __name__ == '__main__':
    pass
