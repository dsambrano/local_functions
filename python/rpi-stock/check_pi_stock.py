#!/usr/bin/env python3


import time
import sites
import logging

COMPANIES = sites.COMPANIES
PRODUCTS = sites.PRODUCTS
BASE_URL = sites.BASE_URL
SCRAPPERS = sites.SCRAPPERS
check_companies = ["microcenter", "adafruit"]


def get_product_pages(product:str, company:str) -> str:
    """get_product_pages: Docstring for get_product_pages.

    Args:
        product (str): Product key to be used for Unique Endpoint
        company (str): Company key to be used for Company Website
 
    Returns: (str) a URL for a company

    """
    return f"{BASE_URL[company]}{PRODUCTS[product][company]}"


def main():
    """main Check Raspberry Pi Stock at various Venders

    Returns: Creates log indicating Product Stock for Each Vender

    """
    for scrapper in SCRAPPERS:
        pass
    products = [key for key in PRODUCTS]
    product = products[0]
    for product in PRODUCTS:
        # Probably Good enough since I really don't expect the same site for multiple
        time.sleep(3)  # Prevent issues of Rate Limiting
        for company in product:
            if company not in check_companies:
                logging.info(f"Skipping {company}")
                continue
            logging.info(f"Checking Data from {product} at {company}")
            site = get_product_pages(product, company)
            print(site)  # Need to figure out a way to call the right Class from here



if __name__ == "__main__":
    main()
