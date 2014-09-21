#!/usr/bin/env python
"""Get articles from owler
Owler puts articles behind an iframe, so it requires a few steps to get. Also it involves running the javascript
"""
import calendar
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import re
import MySQLdb as mdb
from crawler.ratelimiter import rate_limited


ORGANIZATION_TO_URL = {'uber' : 'https://www.owler.com/iaApp/100242/uber-news'}


@rate_limited(0.2)
def get_owler_article_pages(driver, url):
    """Get owler article url on a owler news page for a company

    Parameters
    ----------
    driver : WebDriver
        webdriver, usually PhantomJS
    url : str
        owler news url
        example - https://www.owler.com/iaApp/100242/uber-news
    """
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)
    feed = soup.find('ul', {'class': 'feeds_list'})
    urls = []
    for item in feed.findAll('li'):
        url = item.find('a', {'class' : 'feedTitle'})['href']
        title = item.find('a', {'class':'feedTitle'}).text
        urls.append((url, title))
    return urls


@rate_limited(0.2)
def get_url_from_owler_article_page(driver, url):
    """Get url from an owler article page

    Parameters
    ----------
    driver : WebDriver
        webdriver, usually PhantomJS
    url : str
        owler article url
        example - http://www.owler.com/iaApp/article/541cf77ce4b0e71dc7cd7d14.htm
    """
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)
    script = soup.findAll('script')[-1]
    return re.search('location = "(?P<url>.+)"', str(script)).group('url')


def update_organization(driver, organization):
    con = mdb.connect('localhost', 'shxreader', 'shxreader', 'shxreader')
    with con:
        cur = con.cursor()
        prepared_statement = "select owler_url from owler"
        cur.execute(prepared_statement)
        results = cur.fetchall()
        known_urls = set(r[0] for r in results)
        news_url = ORGANIZATION_TO_URL[organization]
        urls = get_owler_article_pages(driver, news_url)
        urls.reverse()
        prepared_statement = "INSERT INTO owler VALUES (%s, %s, %s, %s, %s)"
        for owler_url, heading in urls:
            if owler_url not in known_urls:
                article_url = get_url_from_owler_article_page(driver, owler_url)
                timestamp = calendar.timegm(time.gmtime())
                cur.execute(prepared_statement, (organization, owler_url, article_url, heading, timestamp))
                cur.commit()


def get_articles(organization):
    pass


def run():
    driver = webdriver.PhantomJS()
    for organization in ORGANIZATION_TO_URL:
        update_organization(driver, organization)
    driver.close()
    driver.quit()


def main():
    run()


if __name__ == '__main__':
    main()
