"""RSS Feeds"""
from bs4 import BeautifulSoup
import requests


def urls_from_xml_feed(url):
    xml = BeautifulSoup(requests.get(url).text, features="xml")
    urls = [article.find('link').text for article in xml.findAll('item')]
    urls = [url.replace('?ncid=rss', '') for url in urls]
    return urls


def techcrunch():
    url = 'http://techcrunch.com/feed/'
    return urls_from_xml_feed(url)


def venturebeat():
    url = 'http://venturebeat.com/feed/'
    return urls_from_xml_feed(url)

def main():
    pass


if __name__ == '__main__':
    main()
