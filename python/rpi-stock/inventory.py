#!/usr/bin/env python3

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, ResultSet
# Check out: https://realpython.com/factory-method-python/#a-general-purpose-object-factory


class Inventory(ABC):
    """Abstract Base Class Implementation for Checking Inventory"""

    sold_out_text: str
    in_stock_text: str
    cookies: dict | None = None
    class_: str | None  # Should probs combine with below to query and be a dictionary, **kwargs used in check and remove the versions
    attr: dict | None

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

    def check_inventory_attr(self) -> str | None:
        """check_inventory takes a BeautifulSoup object and returns the section
        describing the Stock Inventory Levels

        Returns: (Text) containing the text describing stock levels.

        """
        inventory_text = self.soup.find(attr=self.attr)
        if not inventory_text:
            return None

        return inventory_text.text

    def check_inventory_class(self) -> str | None:
        """check_inventory takes a BeautifulSoup object and returns the section
        describing the Stock Inventory Levels

        Returns: (Text) containing the text describing stock levels.

        """
        inventory_text = self.soup.find(class_=self.class_)
        if not inventory_text:
            return None

        return inventory_text.text


    def check_inventory(self) -> str | None:
        """check_inventory takes a BeautifulSoup object and returns the section
        describing the Stock Inventory Levels

        Returns: (Text) containing the text describing stock levels.

        """
        if not self.class_:
            return self.check_inventory_attr()

        return self.check_inventory_class()

    @property
    def in_stock(self) -> bool | None:
        # inventory_text = self.check_inventory()
        # if not inventory_text:
        #    return None
        # stock = None if sold_out_text in inventory_text else False
        stock = False
        return stock
