import re
import urllib2
import urlparse
from bs4 import BeautifulSoup
import lxml.html
import time

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')


def re_scraper(html):
    results = {}
    for field in FIELDS:
        results[field] = re.search('<tr id="places_%s__row">.*?<td\s*class="w2p_fw">(.*?)</td>' % field, html).groups()[0]
    return results


def bs_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = {}
    for filed in FIELDS:
        results[filed] = soup.find('table').find('tr', id='places_%s__row' % filed).find('td', class_='w2p_fw').text
    return results


def lxml_scraper(html):
    results = {}
    tree = lxml.html.fromstring(html)
    for filed in FIELDS:
        results[filed] = tree.cssselect('table > tr#places_%s__row > td.w2p_fw' % filed)[0].text_content()
    return results


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
                return download(url, user_agent, proxy, num_retries - 1)
    return html


if __name__ == '__main__':
    url = 'http://example.webscraping.com/view/Afghanistan-1'
    # url = 'http://210.41.233.144:8080/opac/item.php?marc_no=0000477060'
    html = download(url)
    # result = re.findall('<tr id="places_area__row"><td class="w2p_fl"><label for="places_area" id="places_area__label">Area: </label></td><td class="w2p_fw">(.*?)</td>', html)
    # result = re.findall('<tr id=["\']places_area__row["\']>.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>', html)
    # result = re.search('<tr id=["\']places_area__row["\']>.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>', html).groups()[0]
    # soup = BeautifulSoup(html, 'html.parser')
    # tr = soup.find('tr', attrs={'id': 'places_area__row'})
    # td = tr.find('td', attrs={'class': 'w2p_fw'})
    # area = td.text
    # dl = soup.find_all('dl', attrs={'class': 'booklist'})
    # tree = lxml.html.fromstring(html)
    # result = tree.cssselect('table > tr#places_area__row > td.w2p_fw')[0].text_content()
    NUM_TIMES = 100
    for name, scraper in [('Regex', re_scraper), ('BeautifulSoup', bs_scraper), ('Lxml', lxml_scraper)]:
        start = time.time()
        for i in range(NUM_TIMES):
            if scraper == 're_scraper':
                re.purge()
            results = scraper(html)
            assert(results['area'] == '647,500 square kilometres')
        end = time.time()
        print '%s: %.2f seeconds' % (name, end - start)
