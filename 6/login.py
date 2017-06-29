import cookielib
import urllib2
import urllib
import os
import json
import time
import glob
import lxml.html


def load_ff_sessions(session_filename):
    cj = cookielib.CookieJar()
    if os.path.exists(session_filename):
        json_data = json.loads(open(session_filename, 'rb').read())
        for window in json_data.get('windows', []):
            for cookie in window.get('cookies', []):
                if(cookie.get('host', '') != 'example.webscraping.com'):
                    continue
                c = cookielib.Cookie(0, cookie.get('name', ''), cookie.get('value', ''), None, False, cookie.get('host', ''), cookie.get('host', '').startswith('.'), cookie.get('host', '').startswith('.'), cookie.get('path', ''), False, False, str(int(time.time()) + 3600*24*7), False, None, None, {})
            cj.set_cookie(c)
    else:
        print 'Session file does not exists:', session_filename

    return cj

def find_ff_sessions():
    path = '%APPDATA%\Mozilla\Firefox\Profiles\*.default\sessionstore-backups'
    filename = os.path.join(path, 'recovery.js')
    match = glob.glob(os.path.expandvars(filename))
    if match:
        return match[0]

def get_login_key():
    session_filename = find_ff_sessions()
    cj = load_ff_sessions(session_filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    return opener

def main():
    get_login_key()


if __name__ == '__main__':
    main()
    # session_filename = find_ff_sessions()
    # cj = load_ff_sessions(session_filename)
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # url = 'http://example.webscraping.com'
    # html = opener.open(url).read()
    # tree = lxml.html.fromstring(html)
    # print tree.cssselect('ul#navbar li a')[0].text_content()
