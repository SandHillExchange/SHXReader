#!/usr/bin/env python
import rss.feeds as rss_feeds
from redis import Redis
from rq import Queue
import crawler.spider as spyder
from crawler.spider import crawl_and_store_page


def queue_urls(urls):
    q = Queue(connection=Redis())
    for url in urls:
        if spyder.lookup_page(url) is None:
            result = q.enqueue(crawl_and_store_page, url)


def main():
    urls = rss_feeds.techcrunch()
    print urls
    queue_urls(urls)

    urls = rss_feeds.venturebeat()

    urls = rss_feeds.hacker_news()

    urls = rss_feeds.mashable()


if __name__ == '__main__':
    main()
