from selene.api import *
from src.domains.Navigation import Navigation


class MainPage(object):

    def __init__(self):
        self.nav = Navigation(s('#qa-NAV'))
        self.active_tab = self.nav.active_tab

    def open(self):
        browser.open_url("/client/web?login=true#?an=true")
        return self

    def refresh_page(self):
        browser.driver().refresh()

    def add_note(self, title, body):
        self.nav.open_tab(self.nav.all_notes).create_note()
        self.active_tab.active_note.set_title(title)
        self.active_tab.active_note.set_body(body)

