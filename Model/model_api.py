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

    def clean_request_api(self, infos_of_products):
        """
            cleans items of api's request
            In reception : list of product dictionaries like...
            [{'name': 'TUC', 'brand': 'LU'...}, {'name': 'Gazpacho'...}]
            On return    : same list of dictionaries but cleaned
        """
        for info in infos_of_products:
            for data in info:
                # limits length of "ingredients
                if len(info[data]) > 350:
                    info[data] = info[data][:350]
                # delete page break "\n"
                my_txt = info[data].maketrans("\n", " ")
                info[data] = info[data].translate(my_txt)
                # delete page break "\n"
                my_txt = info[data].maketrans("\r", " ")
                info[data] = info[data].translate(my_txt)
            try:
                info['url'] = str(info['url']).replace("'", " ")
                info['product_name_fr'] = str(info['product_name_fr']).replace("'", " ")
                info['product_name_fr'] = str(info['product_name_fr']).replace("d'", "d ")
                info['brands'] = str(info['brands']).replace("'", " ")
                info['nutrition_grade_fr'] = str(info['nutrition_grade_fr']).replace("'", " ")
                info['ingredients_text_fr'] = str(info['ingredients_text_fr']).replace("'", " ")
                info['stores'] = str(info['stores']).replace("'", " ")
            except KeyError:
                pass
        return infos_of_products


if __name__ == '__main__':
    pass
