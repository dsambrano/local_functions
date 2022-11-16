#!/usr/bin/env python3


import time
import sites
import logging
import inventory

COMPANIES = sites.COMPANIES
PRODUCTS = sites.PRODUCTS
BASE_URL = sites.BASE_URL
SCRAPPERS = sites.SCRAPPERS
exclude_companies = []


logging.basicConfig(level=logging.WARNING)

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
    for product in PRODUCTS:
        # Probably Good enough since I really don't expect the same site for multiple
        time.sleep(3)  # Prevent issues of Rate Limiting
        for company in PRODUCTS[product]:
            # if company in exclude_companies:
            if company != "microcenter":
                logging.info(f"Skipping {company}")
                continue
            logging.info(f"Checking Data from {product} at {company}")

            # Checking Stock
            stock_checker = inventory.MicrocenterInventory()
            site = get_product_pages(product, company)
            stock_checker.get_page(site)
            stock = stock_checker.in_stock

            # Logging Stock Status
            if stock is None:
                print(f"Stock Status Unknown. Manually Check: {site}")
                continue
            article = "is" if stock else "is not"
            stock_text = f"{product} {article} in stock at {company}"
            stock_text = f"{stock_text}: {site}" if stock else stock_text
            print(stock_text)



if __name__ == "__main__":
    main()
