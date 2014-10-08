"""RSS Feeds"""
from urlparse import urlparse
from bs4 import BeautifulSoup
import requests


def remove_query_parameters(urls):
    urls = [urlparse(u) for u in urls]
    urls = map(lambda x: x.scheme + '://' + x.netloc + x.path, urls)
    return urls


def urls_from_xml_feed(url, remove_qs=True):
    xml = BeautifulSoup(requests.get(url).text, features="xml")
    urls = [article.find('link').text.strip() for article in xml.findAll('item')]
    if remove_qs:
        urls = remove_query_parameters(urls)
    return urls


def hacker_news():
    url = 'https://news.ycombinator.com/rss'
    rss = BeautifulSoup(requests.get(url).text, features="xml")
    urls = [link.text for link in rss.findAll('link')]
    urls = remove_query_parameters(urls)
    return urls


def main():
    pass


if __name__ == '__main__':
    main()
