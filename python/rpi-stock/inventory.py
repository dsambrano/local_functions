#!/usr/bin/env python3

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, ResultSet


class Inventory(ABC):
    """Abstract Base Class Implementation for Checking Inventory"""

    sold_out_text: str
    in_stock_text: str

    @abstractmethod
    def check_inventory(self, soup: BeautifulSoup) -> ResultSet:
        pass


class MicrocenterInventory(Inventory):
    sold_out_text: str = "SOLD OUT"
    in_stock_text: str = "IN STOCK"
    # Should probably initalize with a BS object and create soup object from parser
    # Alternatively, initalize with soup object so there are options here

    def check_inventory(self, soup: BeautifulSoup) -> str | None:
        """check_inventory takes a BeautifulSoup object and returns the section
        describing the Stock Inventory Levels

        Args:
            soup (BeautifulSoup): A BeautifulSoup parser for a product page

        Returns: (ResultSet) containing the text describing stock levels.

        """
        inventory_text = soup.find(class_="inventory")
        if not inventory_text:
            return None

        return inventory_text.text

    @property
    def in_stock(self) -> bool | None:
        # inventory_text = self.check_inventory()
        # if not inventory_text:
        #    return None
        # stock = None if sold_out_text in inventory_text else False
        stock = False
        return stock
