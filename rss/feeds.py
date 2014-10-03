"""RSS Feeds"""
from bs4 import BeautifulSoup
import requests


def techcrunch():
    url = 'http://techcrunch.com/feed/'
    xml = BeautifulSoup(requests.get(url).text, features="xml")
    urls = [article.find('link').text for article in xml.findAll('item')]
    urls = [url.replace('?ncid=rss', '') for url in urls]
    return urls


def main():
    pass


if __name__ == '__main__':
    main()
