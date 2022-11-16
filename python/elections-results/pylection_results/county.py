#!/usr/bin/env python3


# dynamic webrequest
## Adapted from: https://stackoverflow.com/a/68787500
## Also See: https://www.tutorialspoint.com/python_web_scraping/python_web_scraping_dynamic_websites.htm
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://www.politico.com/2022-election/results/arizona/statewide-offices/"
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
# executable_path param is not needed if you updated PATH
browser = webdriver.Firefox(options=options)
browser.get(URL)
buttons = browser.find_elements(By.CSS_SELECTOR, ".styles_container__C5E_O")
_ = [x.click() for x in buttons]  # Really only need [0] but do all just in case
# Prints whole Page
html = browser.page_source
# prints just the data of interest
content = browser.find_elements(By.CSS_SELECTOR, ".styles_container__u2WsS")[0].text
browser.quit()
for x in content.split("\n"):
    if re.match(r"[a-zA-Z0-9_ ]* (County|City)", x):
        pass

#counties = re.findall(r"\w+ County", content)
counties = [x for x in content.split("\n") if re.match(r"[a-zA-Z0-9_ ]* (County|City).*", x)]
table = re.split(r"[a-zA-Z0-9_ ]* [(County|City)].*", content)
#table = re.split(r"\n[a-zA-Z0-9_ ]* County", content)
header, county_data = table[0], table[1:]
candidates = re.findall(r"(\w+)\npercent", header)
col_names = [f"{x}_{y}" for x in candidates for y in ["Percent", "Votes"]] + ["Total",""]
# col_names = re.sub(r"\n(percent\n.\n|.\n)", "\n", header).split("\n")[2:]
data = [re.sub(r"(^\n)|(\n$)|(%)|(,)", "", x).split("\n") for x in county_data]
df = pd.DataFrame(data, counties, columns=col_names).drop('', axis=1).astype(float)

def total(x, pct):
    return x / pct


def net_gain(x, pct_counted, pct_win):
    tot = total(x, pct_counted)
    left = tot - x
    return (left * pct_win) - (left * (1 - pct_win))


def results(x, pct_counted, pct_win):
    return({"total": total(x, pct_counted) - x, "E(gain)": net_gain(x, pct_counted, pct_win)})


class County():

    """Individual County for an Election Result"""

    def __init__(self):
        """TODO: to be defined. """
        super.__init__(self)

