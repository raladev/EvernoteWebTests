import pytest
from selene.api import *
import json

#  Accounts for login
with open("accounts.json", "r") as read_file:
    data = json.load(read_file)
    simple_accounts = [(element['login'], element['password']) for element in data['simple_accounts']]
    google_accounts = [(element['login'], element['password']) for element in data['google_accounts']]

#  Notest for test_notes
notes_for_test = [('Eng title', 'Eng body'),  # заметка для заполнения и открытия
                  ('Ру заголовок', 'Ру текст'),  # заметка для заполнения и открытия
                  ('中国标题', '中文文本'),  # заметка для заполнения и открытия
                  ('заголовок for 变化', '测试 for изменения'),  # заметка для изменения
                  ('nota para apagar', 'nota para apagar')  # заметка для удаления
                  ]

@pytest.fixture(scope='session')
def setup(request):
    config.browser_name = 'chrome'
    config.timeout = 10
    config.base_url = "https://www.evernote.com"

    def teardown():
        browser.quit()

    request.addfinalizer(teardown)


@pytest.mark.usefixtures("setup")
class BaseTest(object):
    pass
