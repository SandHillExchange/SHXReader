"""RSS Feeds"""
from bs4 import BeautifulSoup
import requests


def urls_from_xml_feed(url):
    xml = BeautifulSoup(requests.get(url).text, features="xml")
    urls = [article.find('link').text for article in xml.findAll('item')]
    return urls


def techcrunch():
    url = 'http://techcrunch.com/feed/'
    urls = urls_from_xml_feed(url)
    urls = [url.replace('?ncid=rss', '') for url in urls]
    return urls


def venturebeat():
    url = 'http://venturebeat.com/feed/'
    return urls_from_xml_feed(url)


def hacker_news():
    url = 'https://news.ycombinator.com/rss'
    rss = BeautifulSoup(requests.get(url).text, features="xml")
    urls = [link.text for link in rss.findAll('link')]
    return urls


def mashable():
    url = 'http://mashable.com/category/startups/rss/'
    urls = urls_from_xml_feed(url)
    urls = [url.replace('?utm_medium=feed&utm_source=rss', '') for url in urls]
    return urls


def main():
    pass


if __name__ == '__main__':
    main()
