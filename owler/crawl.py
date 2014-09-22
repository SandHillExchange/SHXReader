#!/usr/bin/env python
"""Get articles from owler
Owler puts articles behind an iframe, so it requires a few steps to get. Also it involves running the javascript
"""
import calendar
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import urllib
import re
import MySQLdb as mdb
from crawler.ratelimiter import rate_limited
# from crawler import CHROME_USER_AGENT


TIMEOUT = 10.0 # page load timeout


ORGANIZATION_TO_URL = {
    'actifio': 'https://www.owler.com/iaApp/123706/actifio-news',
    'adaptive-biotechnologies': 'https://www.owler.com/iaApp/383771/adaptive-biotechnologies-news',
    'affirm': 'https://www.owler.com/iaApp/1195149/affirm-news',
    'airbnb': 'https://www.owler.com/iaApp/116231/airbnb-news',
    'angellist': 'https://www.owler.com/iaApp/116312/angellist-news',
    'appnexus': 'https://www.owler.com/iaApp/104201/appnexus-news',
    'automattic': 'https://www.owler.com/iaApp/102038/automattic-news',
    'beepi': 'https://www.owler.com/iaApp/1395944/beepi-news',
    'big-health': 'https://www.owler.com/iaApp/1410777/big-health-news',
    'bitgo': 'https://www.owler.com/iaApp/1392180/bitgo-news',
    'bitpay': 'https://www.owler.com/iaApp/143463/bitpay-news',
    'blue-apron': 'https://www.owler.com/iaApp/209992/blue-apron-news',
    'bonobos': 'https://www.owler.com/iaApp/100338/bonobos-news',
    'carmenta-bioscience': 'https://www.owler.com/iaApp/219912/carmenta-bioscience-news',
    'chain': 'https://www.owler.com/iaApp/1624975/chain-news',
    'circle': 'https://www.owler.com/iaApp/707356/circle-news',
    'cloudera': 'https://www.owler.com/iaApp/100508/cloudera-news',
    'coinbase': 'https://www.owler.com/iaApp/137494/coinbase-news',
    'coursera': 'https://www.owler.com/iaApp/123087/coursera-news',
    'datafox': 'https://www.owler.com/iaApp/1185370/datafox-news',
    'docusign': 'https://www.owler.com/iaApp/120886/docusign-news',
    'dollar-shave-club': 'https://www.owler.com/iaApp/134638/dollar-shave-club-news',
    'domo': 'https://www.owler.com/iaApp/108757/domo-news',
    'doordash': 'https://www.owler.com/iaApp/217990/doordash-news',
    'dropbox': 'https://www.owler.com/iaApp/101638/dropbox-news',
    'etsy': 'https://www.owler.com/iaApp/121413/etsy-news',
    'eventbrite': 'https://www.owler.com/iaApp/100125/eventbrite-news',
    'fab-com': 'https://www.owler.com/iaApp/101152/fab-news',
    'fastly': 'https://www.owler.com/iaApp/172675/fastly-news',
    'flipkart': 'https://www.owler.com/iaApp/139206/flipkart-news',
    'github': 'https://www.owler.com/iaApp/128666/github-news',
    'good-eggs': 'https://www.owler.com/iaApp/365160/good-eggs-news',
    'homejoy': 'https://www.owler.com/iaApp/183855/homejoy-news',
    'houzz': 'https://www.owler.com/iaApp/135032/houzz-news',
    'ifttt': 'https://www.owler.com/iaApp/125005/ifttt-news',
    'imgur': 'https://www.owler.com/iaApp/122272/imgur-news',
    'jawbone': 'https://www.owler.com/iaApp/125318/jawbone-news',
    'julep': 'https://www.owler.com/iaApp/141657/julep-news',
    'knewton': 'https://www.owler.com/iaApp/100158/knewton-news',
    'leap-motion': 'https://www.owler.com/iaApp/139746/leap-motion-news',
    'livingsocial': 'https://www.owler.com/iaApp/104280/livingsocial-news',
    'lookout': 'https://www.owler.com/iaApp/123609/lookout-news',
    'mapr-technologies': 'https://www.owler.com/iaApp/100509/mapr-news',
    'mattermark': 'https://www.owler.com/iaApp/172098/mattermark-news',
    'medium': 'https://www.owler.com/iaApp/229499/medium-news',
    'mightytext': 'https://www.owler.com/iaApp/144329/mightytext-news',
    'mongodb': 'https://www.owler.com/iaApp/125134/mongodb-news',
    'mongodb-inc': 'https://www.owler.com/iaApp/125134/mongodb-news',
    'nextdoor': 'https://www.owler.com/iaApp/139804/nextdoor-news',
    'optimizely': 'https://www.owler.com/iaApp/105382/optimizely-news',
    'palantir-technologies': 'https://www.owler.com/iaApp/133110/palantir-news',
    'path': 'https://www.owler.com/iaApp/121985/path-news',
    'pinterest': 'https://www.owler.com/iaApp/111996/pinterest-news',
    'platfora': 'https://www.owler.com/iaApp/106567/platfora-news',
    'practice-fusion': 'https://www.owler.com/iaApp/122374/practice-fusion-news',
    'product-hunt': 'https://www.owler.com/iaApp/1484621/product-hunt-news',
    'pure-storage': 'https://www.owler.com/iaApp/122756/pure-storage-news',
    'ripple-labs': 'https://www.owler.com/iaApp/147208/ripple-labs-news',
    'secondmarket': 'https://www.owler.com/iaApp/123317/secondmarket-news',
    'secret': 'https://www.owler.com/iaApp/1183296/secret-news',
    'sendgrid': 'https://www.owler.com/iaApp/124152/sendgrid-news',
    'shyp': 'https://www.owler.com/iaApp/490204/shyp-news',
    'slack': 'https://www.owler.com/iaApp/359234/slack-news',
    'snapchat': 'https://www.owler.com/iaApp/141188/snapchat-news',
    'sofi': 'https://www.owler.com/iaApp/139446/sofi-news',
    # 'sosh': 'https://www.owler.com/iaApp/358911/sosh-news',
    # 'square': 'https://www.owler.com/iaApp/102407/square-news',
    'theranos': 'https://www.owler.com/iaApp/139733/theranos-news',
    'thrillist-com': 'https://www.owler.com/iaApp/100198/thrillist-news',
    'tinder': 'https://www.owler.com/iaApp/180478/tinder-news',
    'tiny-speck': 'https://www.owler.com/iaApp/134942/tiny-speck-news',
    'twilio': 'https://www.owler.com/iaApp/124188/twilio-news',
    'warby-parker': 'https://www.owler.com/iaApp/100305/warby-parker-news',
    # 'washio': 'https://www.owler.com/iaApp/1147581/washio-news',
    'wealthfront': 'https://www.owler.com/iaApp/122326/wealthfront-news',
    'wefunder': 'https://www.owler.com/iaApp/110408/wefunder-news',
    'yo': 'https://www.owler.com/iaApp/1530962/yo--news',
    'zenefits': 'https://www.owler.com/iaApp/217994/zenefits-news',
    'zocdoc': 'https://www.owler.com/iaApp/125194/zocdoc-news'
    }


@rate_limited(0.5)
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
    print url
    driver.get(url)
    wait = ui.WebDriverWait(driver, TIMEOUT)
    urls = []
    try:
        wait.until(lambda x: driver.find_element_by_class_name('feeds_list'))
        soup = BeautifulSoup(driver.page_source)
        feed = soup.find('ul', {'class': 'feeds_list'})
        for item in feed.findAll('li'):
            url = item.find('a', {'class' : 'feedTitle'})['href']
            title = item.find('a', {'class':'feedTitle'}).text

            source = item.find('a', {'class': 'source'}).text
            duration = item.find('span', {'class': 'duration'}).text

            urls.append((url, title, source, duration))
    except TimeoutException:
        print 'timeout'
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
    soup = BeautifulSoup(urllib.urlopen(url).read())
    script = soup.findAll('script')[-1]
    m = re.search('location = "(?P<url>.+)"', str(script))
    if m is not None:
        return m.group('url')


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
        query = "select * from owler where organization = %s"
        cur.execute(query, (organization))
        results = cur.fetchall()
    return results


def run():
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = CHROME_USER_AGENT
    # driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver = webdriver.PhantomJS()
    for organization in ORGANIZATION_TO_URL:
        update_organization(driver, organization)
    driver.close()
    driver.quit()


def main():
    run()


if __name__ == '__main__':
    main()
