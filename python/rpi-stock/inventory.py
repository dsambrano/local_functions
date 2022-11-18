#!/usr/bin/env python3

from abc import ABC
from bs4 import BeautifulSoup, Tag
import requests

# Check out: https://realpython.com/factory-method-python/#a-general-purpose-object-factory
# Info on Common functions: https://www.integralist.co.uk/posts/python-code-design/


class Inventory(ABC):
    """Abstract Base Class Implementation for Checking Inventory"""

    sold_out_text: str
    in_stock_text: str
    soup_kwars: dict
    cookies: dict | None = None

    def get_page(self, site):
        """TODO: Docstring for get_page.

        Returns: TODO

        """
        response = requests.get(site, cookies=self.cookies)
        self.soup = BeautifulSoup(response.content, "html5lib")

    def check_inventory(self) -> str | None:
        """check_inventory takes a BeautifulSoup object and returns the section
        describing the Stock Inventory Levels

        Returns: (Text) containing the text describing stock levels.

        """
        inventory_text = self.soup.find(**self.soup_kwars)
        if not inventory_text:
            return None

        return inventory_text.text

    @property
    def in_stock(self) -> bool | None:
        inventory_text = self.check_inventory()
        if not inventory_text:
            return None
        stock = False if self.sold_out_text in inventory_text else None
        stock = True if self.in_stock_text in inventory_text else stock
        return stock


class MicrocenterInventory(Inventory):
    # Also '"0 "' NEW IN STOCK: see https://www.microcenter.com/product/460968/raspberry-pi-3-model-b?storeid=101
    sold_out_text = "SOLD OUT"
    in_stock_text = "IN STOCK"
    soup_kwars = {"class_": "inventory"}
    cookies = {"storeSelected": "101"}  # 101 = Tustin, CA; 121 = Camb, MA


class AdafruitInventory(Inventory):
    sold_out_text = "Out of stock"
    in_stock_text = "In stock"
    soup_kwars = {"attrs": {"itemprop": "availability"}}


class CanaInventory(Inventory):
    sold_out_text = "Sold Out"
    in_stock_text = "Add to Cart"
    soup_kwars = {"id": "ProductAddToCartDiv"}


class ChicagoInventory(Inventory):
    sold_out_text = "Out of stock"
    in_stock_text = "In stock"
    soup_kwars = {"class_": "sold_out"}

    @property
    def in_stock(self) -> bool | None:
        "Chicago has a class when a product is out of stock"
        inventory_text = self.check_inventory()
        if not inventory_text:
            return True

        return False


class PiShopInventory(Inventory):
    sold_out_text = "Out of stock"
    in_stock_text = "Add to Cart"
    soup_kwars = {"id": "form-action-addToCart"}

    def check_inventory(self) -> str | None:
        """check_inventory takes a BeautifulSoup object and returns the section
        describing the Stock Inventory Levels

        Returns: (Text) containing the text describing stock levels.

        """
        tag = self.soup.find(**self.soup_kwars)
        if not tag or type(tag) is not Tag:
            return None

        return tag.attrs.get("value", None)
