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
    urls = [article.find('link').text for article in xml.findAll('item')]
    if remove_qs:
        urls = remove_query_parameters(urls)
    return urls


def techcrunch():
    url = 'http://techcrunch.com/feed/'
    return urls_from_xml_feed(url)


def venturebeat():
    url = 'http://venturebeat.com/feed/'
    return urls_from_xml_feed(url)


def hacker_news():
    url = 'https://news.ycombinator.com/rss'
    rss = BeautifulSoup(requests.get(url).text, features="xml")
    urls = [link.text for link in rss.findAll('link')]
    return urls


def xconomy():
    url = 'http://www.xconomy.com/feed/'
    return urls_from_xml_feed(url)


def mashable():
    url = 'http://mashable.com/category/startups/rss/'
    urls = urls_from_xml_feed(url)
    return urls


def main():
    pass


if __name__ == '__main__':
    main()
