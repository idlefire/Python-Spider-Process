#!encoding:utf-8
import urlparse
import re
import robotparser
from Downloader import Downloader
from DiskCache import DiskCache


def link_crawler(seed_url, link_regex, user_agent='idle', num_retries=1, max_depth=2, delay=0, scrape_callback=None, cache=None):
    crawl_queue = [seed_url]  # 地址添加到数组中
    seen = {seed_url: 0}  # 定义网址位置深度
    D = Downloader(delay=delay, user_agent=user_agent, num_retries=num_retries, cache=cache)
    while crawl_queue:
        url = crawl_queue.pop()
        if True:
            html = D(url)
            # print html
            links = []
            depth = seen[url]  # 获取网址深度
            if scrape_callback:
                links.append(scrape_callback(url, html) or [])
            if depth != max_depth:
                for link in get_link(html):
                    # print link
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


def get_robot(user_agent, url):
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp.can_fetch(user_agent, url)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', '/(places)', max_depth=-1, delay=0, cache=DiskCache())
