import login
import lxml.html
import urllib
import urllib2
from pprint import pprint

def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        data[e.get('name')] = e.get('value')
    return data

if __name__ == '__main__':
    edit_url = 'http://example.webscraping.com/places/default/edit/China-47'
    opener = login.get_login_key()
    html = opener.open(edit_url).read()
    data = parse_form(html)
    pprint(data)
    # data['population'] = int(data['population']) + 1
    # epost_data = urllib.urlencode(data)
    # request = urllib2.Request(edit_url, epost_data)
    # response = opener.open(request)
