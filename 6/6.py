import lxml.html
import urllib2
import urllib
import cookielib


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        data[e.get('name')] = e.get('value')
    return data


def build_opener():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    return opener


if __name__ == '__main__':
    login_url = 'http://example.webscraping.com/places/default/user/login'
    login_email = '123456@qq.com'
    login_password = '123456'
    opener = build_opener()
    html = opener.open(login_url).read()
    post_data = parse_form(html)
    post_data['email'] = login_email
    post_data['password'] = login_password
    epost_data = urllib.urlencode(post_data)
    request = urllib2.Request(login_url, epost_data)
    response = opener.open(request)
    print response.geturl()
