import mechanize

LOGIN_URL = 'http://example.webscraping.com/places/default/user/login?_next=/places/default/index'
EDIT_URL = 'http://example.webscraping.com/places/default/edit/China-47'


def Login():
    br = mechanize.Browser()
    br.open(LOGIN_URL)
    br.select_form(nr=0)
    login_email = '123456@qq.com'
    login_password = '123456'
    br['email'] = login_email
    br['password'] = login_password
    br.submit()
    return br


def Edit(br):
    br.open(EDIT_URL)
    br.select_form(nr=0)
    br['population'] = str(int(br['population']) + 1)
    br.submit()
    print 'Success!'


def main():
    br = Login()
    Edit(br)


if __name__ == '__main__':
    main()
