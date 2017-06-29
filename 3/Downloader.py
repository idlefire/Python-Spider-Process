#!encoding:utf-8
import random
import urllib2
import urlparse
from datetime import datetime
import time

class Downloader:

    def __init__(self, delay=0, user_agent='idle', proxy=None, num_retries=1, cache=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxy = proxy
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] <= 600:
                    result = None
        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxy) if self.proxy else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy, self.num_retries)
            if self.cache:
                self.cache[url] = result
        return result['html']

    def download(self, url, headers=None, proxy=None, num_retries=3, data=None):
        print 'Downloading:', url
        request = urllib2.Request(url, headers=headers)

        opener = urllib2.build_opener()
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            # code = response.code
        except urllib2.URLError as e:
            print 'Download error:', e.reason
            html = None
            if num_retries > 0:
                if hasattr(e, 'code'):
                    if 500 <= e.code <= 600:
                        return self.download(url, self.user_agent, headers, proxy, self.num_retries)
        return {'html': html}


# 添加延时
class Throttle:

    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)

        self.domains[domain] = datetime.now()
