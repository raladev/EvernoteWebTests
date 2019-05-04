from selene.api import *
from src.pages.MainPage import MainPage


class LoginPage(object):
    def __init__(self):
        self._login_form = s(by.name('login_form'))
        self._username_field = self._login_form.s(by.name('username'))
        self._password_field = self._login_form.s(by.name('password'))
        self._google_oauth_btn = self._login_form.s("#googleOauthButton")

    def open(self):
        browser.open_url("/client/web")
        return self

    def should_have_login_form(self):
        self._login_form.should(be.visible)

# проверить авторизацию через куку?
    def login(self, login, pwd):
        self._username_field.set(login).press_enter()
        self._password_field.set(pwd).press_enter()
        return MainPage()

    def login_via_google(self, login, pwd):
        self._google_oauth_btn.click()
        s("#identifierId").set(login).press_enter()
        s(by.name("password")).set(pwd).press_enter()
        return MainPage()




