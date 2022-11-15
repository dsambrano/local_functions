#!/usr/bin/env python3


import time
import sites
import logging

COMPANIES = sites.COMPANIES
PRODUCTS = sites.PRODUCTS
BASE_URL = sites.BASE_URL
check_companies = ["microcenter", "adafruit"]


def get_product_pages(product:str, company:str) -> str:
    """get_product_pages: Docstring for get_product_pages.

    Args:
        product (str): Product key to be used for Unique Endpoint
        company (str): Company key to be used for Company Website

    Returns: (str) a URL for a company

    """
    return f"{BASE_URL[company]}{PRODUCTS[product][company]}"



    Returns: Creates log indicating Product Stock for Each Vender

    """
    # SOLD_OUT_TEXT = "SOLD OUT"
    # IN_STOCK_TEXT = "IN STOCK"
    return soup.find_all(class_="inventory")


products = [key for key in PRODUCTS]
product = products[0]
product_pages = [
    (key, get_product_pages(product, key))
    for key in PRODUCTS[product]
    if key in check_companies
]

for company, site in product_pages:
    logging.info(f"Checking Data from {product} at {company}")
    response = requests.get(site)
    soup = BeautifulSoup(response.content, "html5lib")
    # soup.find_all(class_ = "inventory") Only for Microcenter
