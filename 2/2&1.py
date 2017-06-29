#!encoding:utf-8
import urllib2
import re
import urlparse
import robotparser
from datetime import datetime
import time
import csv
import lxml.html

def download(url, user_agent='idle', proxy=None, num_retries=3):
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)

    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code <= 600:
                return download(url, user_agent, proxy, num_retries-1)
    return html


# 获取链接并下载
def link_crawler(seed_url, link_regex, user_agent='idle', max_depth=2, delay=5, scrape_callback=None):
    crawl_queue = [seed_url]  # 地址添加到数组中
    seen = {seed_url: 0}  # 定义网址位置深度
    throttle = Throttle(delay)
    while crawl_queue:
        url = crawl_queue.pop()
        if get_robot(user_agent, url):
            throttle.wait(url)  # 添加延时
            html = download(url)
            links = []
            depth = seen[url]  # 获取网址深度
            if scrape_callback:
                links.append(scrape_callback(url, html) or [])
            if depth != max_depth:
                for link in get_link(html):
                    if re.match(link_regex, link):
                        link = urlparse.urljoin(seed_url, link)  # 把地址拼接成一个绝对路径
                        if link not in seen:
                            seen[link] = depth + 1
                            crawl_queue.append(link)
        else:
            print 'Block by robots.txt:', url


# 从页面中获取链接并返回
def get_link(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


# 获取网站的地图
def crawl_sitemap(url):
    u"""获取网站的地图."""
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    for link in links:
        html = download(link)
        if html:
            print 'Success!'


def get_robot(user_agent, url):
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp.can_fetch(user_agent, url)


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

# 回调类
class ScrapeCallback:
    def __init__(self):
            self.writer = csv.writer(open('my_countries.csv', 'w'))
            self.fields = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')
            self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
            self.writer.writerow(row)


if __name__ == '__main__':
    # 进行ScrapeCallback实例化
    link_crawler('http://example.webscraping.com', '/(index|view)', max_depth=-1, delay=0, scrape_callback=ScrapeCallback())
    # crawl_sitemap('http://example.webscraping.com/sitemap.xml')
