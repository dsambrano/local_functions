#!/usr/bin/env python3

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests

# Check out: https://realpython.com/factory-method-python/#a-general-purpose-object-factory


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

    def common(self):
        """common function that works for all the Inerited classes"""
        # https://www.integralist.co.uk/posts/python-code-design/
        print("common method")
        pass


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
        stock = None if self.sold_out_text not in inventory_text else False
        stock = stock if self.in_stock_text not in inventory_text else True
        return stock


class MicrocenterInventory(Inventory):
    sold_out_text = "SOLD OUT"
    in_stock_text = "IN STOCK"
    soup_kwars = {"class_": "inventory"}
    cookies = {"storeSelected": "101"}  # 101 is CA; 121 is MA


class AdafruitInventory(Inventory):
    sold_out_text = "Out of stock"
    in_stock_text = "In stock"
    soup_kwars = {"attrs": {"itemprop": "availability"}}
