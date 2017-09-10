from bs4 import BeautifulSoup
import urllib.request
import urllib
from pymongo import MongoClient

# base url for scraping and concatenating with the "a" element href property
elpais_url = "https://elpais.com/"


def ScrapElPais():
    # Initializing the MongoClient and accessing the collection.
    # If the collection does not exist, it will be created now
    client = MongoClient()
    db = client.scrapings
    elPais_collection = db.elPais
    # Retrieving the HTML content from the base url and parsing it to be
    # "searchable" by BeautifulSoup
    html = urllib.request.urlopen(elpais_url).read()
    soup = BeautifulSoup(html, "html.parser")
    # Iterating "h2" elements to find the news headlines
    for article in soup.find_all("h2", class_="articulo-titulo"):
        headline = article.find("a")
        new_url = elpais_url + headline["href"]
        headline_text = headline.text
        new_document = {
            "title": headline_text,
            "url": new_url
        }
        elPais_collection.insert(new_document)

ScrapElPais()
