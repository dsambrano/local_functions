#!/usr/bin/env python3


import sites
import requests
import logging

from bs4 import BeautifulSoup, ResultSet

COMPANIES = sites.COMPANIES
PRODUCTS = sites.PRODUCTS
BASE_URL = sites.BASE_URL
check_companies = ["microcenter"]


def get_product_pages(product, company) -> str:
    """TODO: Docstring for get_product_pages.

    Args:
        product (TODO): TODO

    Returns: (str) a URL for a company

    """
    return f"{BASE_URL[company]}{PRODUCTS[product][company]}"


def microcenter_inventory(soup: BeautifulSoup) -> ResultSet:
    """TODO: Docstring for microcenter_inventory.

    Args:
        soup (BeautifulSoup): A BeautifulSoup parser

    Returns: TODO

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
