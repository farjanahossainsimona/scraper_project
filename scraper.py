import requests
from bs4 import BeautifulSoup

def scraper():
    URL = requests.form("url")
    page = requests.get(URL)

    results = BeautifulSoup(page.content, "html.parser")
    print(results.prettify())

