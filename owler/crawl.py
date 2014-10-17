#!/usr/bin/env python
"""Get articles from owler
Owler puts articles behind an iframe, so it requires a few steps to get. Also it involves running the javascript

mysqldump -u root shxreader > shxreader_$(date "+%Y%m%d").sql
"""
import calendar
import time
import urllib
import re
from random import shuffle
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import MySQLdb as mdb
from crawler.ratelimiter import rate_limited
from owler import ORGANIZATION_TO_URL
# from crawler import CHROME_USER_AGENT


TIMEOUT = 10.0  # page load timeout


@rate_limited(0.5)
def get_owler_article_pages(url):
    """Get owler article url on a owler news page for a company

    Parameters
    ----------
    url : str
        owler news url
        example - https://www.owler.com/iaApp/100242/uber-news
    """
    print url
    urls = []
    try:
        soup = BeautifulSoup(urllib.urlopen(url).read())
        feed = soup.find('ul', {'class': 'feeds_list'})
        if feed.findAll('li') is None:
            return urls
        for item in feed.findAll('li'):
            article_anchor = item.find('a', {'class': 'feedTitle'})
            if 'href' in article_anchor.attrs:
                url = article_anchor['href']
                title = article_anchor.text
                source = item.find('a', {'class': 'source'}).text
                duration = item.find('span', {'class': 'duration'}).text
                urls.append((url, title, source, duration))
    except IOError, AttributeError:
        print 'Error with ' + url
    return urls


@rate_limited(0.5)
def get_url_from_owler_article_page(url):
    """Get url from an owler article page

    Parameters
    ----------
    driver : WebDriver
        webdriver, usually PhantomJS
    url : str
        owler article url
        example - http://www.owler.com/iaApp/article/541cf77ce4b0e71dc7cd7d14.htm
    """
    print url
    try:
        soup = BeautifulSoup(urllib.urlopen(url).read())
        script = soup.findAll('script')[-1]
        m = re.search('location = "(?P<url>.+)"', str(script))
        if m is not None:
            return m.group('url')
    except IOError:
        print 'Error with ' + url


def update_organization(organization):
    con = mdb.connect('localhost', 'shxreader', 'shxreader', 'shxreader')
    with con:
        cur = con.cursor()
        prepared_statement = "select owler_url from owler"
        cur.execute(prepared_statement)
        results = cur.fetchall()
        known_urls = set(r[0] for r in results)
        news_url = ORGANIZATION_TO_URL[organization]
        urls = get_owler_article_pages(news_url)
        urls.reverse()
        prepared_statement = "INSERT INTO owler VALUES (%s, %s, %s, %s, %s, %s, %s)"
        for owler_url, heading, source, duration in urls:
            if owler_url not in known_urls:
                article_url = get_url_from_owler_article_page(owler_url)
                if article_url is not None:
                    timestamp = calendar.timegm(time.gmtime())
                    cur.execute(prepared_statement, (organization, owler_url, article_url, heading, source, duration, timestamp))
                    con.commit()


def get_articles(organization):
    con = mdb.connect('localhost', 'shxreader', 'shxreader', 'shxreader')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        query = "select * from owler where organization = %s and from_unixtime(timestamp)  >= ( CURDATE() - INTERVAL 2 DAY );"
        cur.execute(query, (organization))
        results = cur.fetchall()
    return results


def run():
    organizations = ORGANIZATION_TO_URL.keys()
    shuffle(organizations)
    for organization in organizations:
        update_organization(organization)
    driver.close()
    driver.quit()


def main():
    run()


if __name__ == '__main__':
    main()
