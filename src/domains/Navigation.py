from selene.api import *
from src.domains.ActiveNote import ActiveNote
from src.domains.NotesTab import NotesTab
import time


class Navigation(object):

    def __init__(self, container):
        self._container = s(by.xpath('//section[@id = "qa-NAV"]'))
        self._user_menu = self._container.s("#qa-NAV_USER")
        self._new_note_btn = self._container.s(by.xpath(".//div[@data-tooltipmark = 'createnotenavitem']"))
        # self.search_box = s("#qa-NAV_SEARCH_BOX")
        # self.shortcuts = s("#qa-NAV_SHORTCUTS_HEADER")

        # Tabs in Menu
        self.all_notes = self._container.s("#qa-NAV_ALL_NOTES")
        # self.shares = s("#qa-SHARED_WITH_ME")
        # self.tags = s("#qa-NAV_TAGS")
        # self.trash = s("#qa-NAV_TRASH") #NotesTab
        # self.all_notebooks = s("#qa-NAV_ALL_NOTEBOOKS")

        self.active_tab = NotesTab()

    def open_tab(self, tab):
        tab.click()
        if tab == self.all_notes:
            return self.set_active_tab(NotesTab())

    def create_note(self):
        self._new_note_btn.click()
        time.sleep(5)
        if isinstance(self.active_tab, NotesTab):
            return self.set_active_tab(NotesTab())
        else:
            return self.set_active_tab(ActiveNote())

    def set_active_tab(self, tab):
        self.active_tab = tab
        return self.active_tab

    def get_username(self):
        return self._user_menu.text

    def username_should_be(self, text):
        self._user_menu.should(have.text(text))
