import urllib2
import cookielib
from pprint import pprint
from PIL import Image
from io import BytesIO
import lxml.html
import pytesseract
import string
import urllib


def get_captcha(html):
    tree = lxml.html.fromstring(html)
    img_src = tree.cssselect('div#recaptcha img')[0].get('src')
    img_bs64 = img_src.partition(',')[-1]
    img_dbs64 = img_bs64.decode('base64')
    file_api = BytesIO(img_dbs64)
    img_captcha = Image.open(file_api)
    return img_captcha


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        data[e.get('name')] = e.get('value')
    return data


def ocr_img(img):
    gray = img.convert('L')
    bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
    word = pytesseract.image_to_string(bw, config=tessdata_dir_config)
    captcha_word = ''.join(w for w in word if w in string.letters).lower()
    return captcha_word


def reg_user(first_name, last_name, email, password):
    reg_url = 'http://example.webscraping.com/places/default/user/register?_next=/places/default/index'
    ck = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(ck))
    request1 = urllib2.Request(reg_url)
    html = opener.open(request1).read()
    # html = parse_form(html)
    # pprint(html)
    reg_form = parse_form(html)
    reg_form['first_name'] = first_name
    reg_form['last_name'] = last_name
    reg_form['email'] = email
    reg_form['password'] = password
    reg_form['password_two'] = password
    img_captcha = get_captcha(html)
    captcha_word = ocr_img(img_captcha)
    reg_form['recaptcha_response_field'] = captcha_word
    # pprint(reg_form)
    reg_form_data = urllib.urlencode(reg_form)
    request2 = urllib2.Request(reg_url, reg_form_data)
    reg_rep = opener.open(request2)
    pprint(reg_rep.geturl())


if __name__ == '__main__':
    first_name = 'z'
    last_name = 'ero'
    email = '147@qq.com'
    password = '123456'
    reg_user(first_name, last_name, email, password)
    # img_captcha.save('captcha-{}.png'.format(captcha_word))
    # pprint(captcha_word)
