from redis import Redis
from rq import Queue
import crawler.spider as spider
from crawler.ratelimiter import rate_limited


if __name__ == '__main__':
    q = Queue(connection=Redis())
    result = q.enqueue(spider.crawl_and_store_page, 'http://nvie.com')

