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
    'uber' : 'https://www.owler.com/iaApp/100242/uber-news',
    # 'livingsocial' : 'https://www.owler.com/iaApp/104280/livingsocial-news',
    # 'airbnb' : 'https://www.owler.com/iaApp/116231/airbnb-news',
    # 'lyft' : 'https://www.owler.com/iaApp/123687/lyft-news',
    # 'pinterest' : 'https://www.owler.com/iaApp/111996/pinterest-news',
    # 'dropbox' : 'https://www.owler.com/iaApp/101638/dropbox-news',
    # 'social-finance' : 'https://www.owler.com/iaApp/1167466/social-finance-news',
    # 'actifio' : 'https://www.owler.com/iaApp/123706/actifio-news',
    # 'cloudera' : 'https://www.owler.com/iaApp/100508/cloudera-news',
    # 'square' : 'https://www.owler.com/iaApp/102407/square-news',
    # 'fanatics' : 'https://www.owler.com/iaApp/139262/fanatics-news',
    # 'box' : 'https://www.owler.com/iaApp/102324/box-news',
    # 'zocdoc' : 'https://www.owler.com/iaApp/125194/zocdoc-news',
    # 'jawbone' : 'https://www.owler.com/iaApp/125318/jawbone-news',
    # 'adaptive-biotechnologies' : 'https://www.owler.com/iaApp/383771/adaptive-biotechnologies-news',
    # 'birchbox' : 'https://www.owler.com/iaApp/100239/birchbox-news',
    # 'warby-parker' : 'https://www.owler.com/iaApp/100305/warby-parker-news',
    # 'snapchat' : 'https://www.owler.com/iaApp/141188/snapchat-news',
    # 'zenefits' : 'https://www.owler.com/iaApp/217994/zenefits-news',
    # 'stripe' : 'https://www.owler.com/iaApp/100441/stripe-news',

    # 'imgur' : 'https://www.owler.com/iaApp/122272/imgur-news',
    # 'platfora' : '',
    # 'optimizely' : 'https://www.owler.com/iaApp/105382/optimizely-news',
    # 'knewton' : '',
    # 'tiny-speck' : '',
    # 'julep' : '',
    # 'twilio' : '',
    # 'leap-motion' : 'https://www.owler.com/iaApp/139746/leap-motion-news',
    # 'bonobos' : 'https://www.owler.com/iaApp/100338/bonobos-news',
    # 'sendgrid' : '',
    # 'mattermark' : '',
    # 'washio' : '',
    # 'homejoy' : '',
    # 'dollar-shave-club' : '',
    # 'yo' : '',
    # 'smoopa' : '',
    # 'copywriter-central' : '',
    # 'proximi' : '',
    # 'mightytext' : '',
    # 'sand-hill-exchange' : '',
    # 'product-hunt' : '',
    # 'secret' : '',
    # 'palantir-technologies' : '',
    # 'wealthfront' : '',
    # 'shyp' : '',
    # 'affirm' : '',
    # 'theranos' : '',
    # 'medium' : '',
    # 'eventbrite' : '',
    # 'pure-storage' : '',
    # 'coursera' : '',
    # 'tinder' : 'https://www.owler.com/iaApp/180478/tinder-news',
    # 'path' : '',
    # 'fastly' : '',
    # 'angellist' : '',
    # 'blue-apron' : '',
    # 'good-eggs' : '',
    # 'doordash' : 'https://www.owler.com/iaApp/217990/doordash-news',
    # 'carmenta-bioscience' : '',
    # 'big-health' : '',
    # 'beepi' : '',
    # 'sosh' : '',
    # 'thrillist-com' : '',
    # 'vurb' : '',
    # 'ripple-labs' : '',
    # 'docusign' : '',
    # 'domo' : '',
    # 'etsy' : '',
    # 'flipkart' : '',
    # 'houzz' : '',
    # 'lookout' : '',
    # 'mapr-technologies' : '',
    # 'nextdoor' : '',
    # 'practice-fusion' : '',
    # 'github' : '',
    # 'mongodb-inc' : '',
    # 'automattic' : '',
    # 'appnexus' : '',
    # 'ifttt' : '',
    # 'fab-com' : '',
    # 'datafox' : 'https://www.owler.com/iaApp/1185370/datafox-news'
    }


@rate_limited(1)
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
    wait = ui.WebDriverWait(driver, TIMEOUT)
    urls = []
    try:
        wait.until(lambda x: driver.find_element_by_class_name('feeds_list'))
        soup = BeautifulSoup(driver.page_source)
        feed = soup.find('ul', {'class': 'feeds_list'})
        for item in feed.findAll('li'):
            url = item.find('a', {'class' : 'feedTitle'})['href']
            title = item.find('a', {'class':'feedTitle'}).text
            urls.append((url, title))
    except TimeoutException:
        print 'timeout'
    return urls


@rate_limited(1)
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
