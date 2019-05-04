from tests.conftest import *
from src.pages.LoginPage import LoginPage


@pytest.fixture(scope='function')
def login_page(request):

    def teardown():
        browser.driver().delete_all_cookies()

    request.addfinalizer(teardown)

    return LoginPage().open()


class TestLoginPage(BaseTest):

    def test_open_login_page(self):
        LoginPage().open().should_have_login_form()

    @pytest.mark.parametrize("login, password", simple_accounts)
    @pytest.mark.usefixtures('login_page')
    def test_login(self, login_page, login, password):
        private_page = login_page.login(login=login, pwd=password)
        private_page.nav.username_should_be(login)

    @pytest.mark.parametrize("login, password", google_accounts)
    @pytest.mark.usefixtures('login_page')
    def test_login_via_google(self, login_page, login, password):
        private_page = login_page.login_via_google(login=login, pwd=password)
        private_page.nav.username_should_be(login)
