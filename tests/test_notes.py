from tests.conftest import *
from src.pages.LoginPage import LoginPage
from src.pages.MainPage import MainPage


@pytest.fixture(scope='class')
def open_app(request, login=simple_accounts[0][0], password=simple_accounts[0][1]):
    LoginPage().open().login(login=login, pwd=password)\
        .nav.open_tab(MainPage().nav.all_notes)

    def teardown():
        app = MainPage()
        app.nav.open_tab(app.nav.all_notes).delete_all_notes()

    request.addfinalizer(teardown)


@pytest.fixture(scope='function')
def new_note():
    return MainPage().nav.create_note().active_note


class TestNotes(BaseTest):

    @pytest.mark.usefixtures("open_app")
    def test_create_new_note(self):
        app = MainPage()

        cnt_before_creation = app.active_tab.notes_count()
        notes_tab = app.nav.create_note()
        cnt_after_creation = notes_tab.notes_count()

        notes_tab.active_note.title_should_be('')
        notes_tab.first_note().date_should_be('a few seconds ago')
        assert 1 + cnt_before_creation == cnt_after_creation, 'Количество заметок не увеличилось на 1'

    @pytest.mark.parametrize("title, body", notes_for_test)
    @pytest.mark.usefixtures("open_app", "new_note")
    def test_note_filling(self, new_note, title, body):
        new_note.set_title(title).title_should_be(title)
        new_note.set_body(body).body_should_be(body)

    @pytest.mark.parametrize("title", [row[0] for row in notes_for_test])
    @pytest.mark.usefixtures("open_app")
    def test_note_opening(self, title):
        notes_tab = MainPage().active_tab
        notes_tab.open_note(title=title).title_should_be(title)

    @pytest.mark.parametrize("title", [notes_for_test[3][0]])
    @pytest.mark.usefixtures("open_app")
    def test_note_changing(self, title):
        app = MainPage()
        notes_tab = MainPage().active_tab

        notes_tab.open_note(title=title).set_title('title был 变')
        notes_tab.active_note.set_body('текст 改变了 too')

        app.refresh_page()

        notes_tab.first_note().title_should_be('title был 变')
        notes_tab.first_note().body_should_be('текст 改变了 too')

        notes_tab.active_note.title_should_be('title был 变')
        notes_tab.active_note.body_should_be('текст 改变了 too')

    @pytest.mark.parametrize("title", [notes_for_test[4][0]])
    @pytest.mark.usefixtures("open_app")
    def test_note_deleting(self, title):
        notes_tab = MainPage().active_tab
        notes_tab.open_note(title=title).note_header.open_actions_dropdown().delete_note()\
            .confirm_action()
        notes_tab.note_should_not_exist(title)







