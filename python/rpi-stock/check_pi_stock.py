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


def get_product_pages(base_url: str, endpoint: str) -> str:
    """get_product_pages: Docstring for get_product_pages.

    Args:
        product (str): Product key to be used for Unique Endpoint
        company (str): Company key to be used for Company Website

    Returns: (str) a URL for a company

    """
    return f"{base_url}{endpoint}"


def update_summary(summary: dict[str, str], product: str, company: str) -> None:
    """update_summary appends vender to product list

    Args:
        summary (dict[str, list]): A Dict to be updated

    Returns: None, Inplace changes on summary dictionary

    """
    companies = summary.get(product, None)
    if companies is None:
        summary.update({product: company})
    else:
        summary.update({product: f"{companies} and {company}"})


def summary_text(summary: dict[str, list]) -> None:
    """TODO: Docstring for summary_text.

    Args:
        summary (dict): A Dictionary of products listing each vender for which
        it is in stock

    Returns: None, prints results

    """
    # companies_str = " and ".join([vender for vender in companies])
    text = [
        f"{product} is in stock at {companies}"
        for product, companies in summary.items()
    ]
    for prod_text in text:
        print(prod_text)


def main():
    """main Check Raspberry Pi Stock at various Venders

    Returns: Creates log indicating Product Stock for Each Vender

    """
    summary = {}
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
            base_url, endpoint = BASE_URL[company], PRODUCTS[product][company]
            site = get_product_pages(base_url, endpoint)
            stock_checker.get_page(site)
            stock = stock_checker.in_stock
            if stock:
                update_summary(summary, product, company)

            # Logging Stock Status
            if stock is None:
                print(f"Stock Status Unknown. Manually Check: {site}")
                continue
            article = "is" if stock else "is not"
            stock_text = f"{product} {article} in stock at {company}"
            stock_text = f"{stock_text}: {site}" if stock else stock_text
            print(stock_text)
    summary_text(summary)


if __name__ == "__main__":
    main()
