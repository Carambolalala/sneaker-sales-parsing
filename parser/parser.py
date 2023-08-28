import requests
from bs4 import BeautifulSoup as bs
import pandas

from links import parsingCore

def parsing(categories: list):
    for category in categories:
        page = 1
        urlTemplate = parsingCore[category] + f'&page={page}'
        requestedPage = requests.get(urlTemplate)
        soupPage = bs(requestedPage.text, "html.parser")
        #amount = soupPage.