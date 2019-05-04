from selene.api import *
import re, time
from src.domains.ActiveNote import ActiveNote
from src.domains.Note import Note
from selenium.common.exceptions import TimeoutException


class NotesTab:

    def __init__(self):
        self.active_note = ActiveNote()
        self._notes_sidebar = s('#qa-NOTES_SIDEBAR')
        self._note_height = 120
        self._no_notes_flag = s('#qa-ALL_NOTES_EMPTY_LINK')
        self._notesList = [Note(s(by.xpath("//div[@id = '" + note.get_attribute('id') + "']")))
                           for note in ss(by.xpath("//div[substring(@id, string-length(@id) - string-length"
                                                   "('NOTES_SIDEBAR_NOTE') +1) ='NOTES_SIDEBAR_NOTE']"))]
        self.notes_counter = s("#qa-NOTES_HEADER_NOTE_COUNT")

    def open_note(self, title=None):
        if title is not None:
            self.note_by_title(title).open()
            time.sleep(2)
            return ActiveNote()

    def note_by_title(self, title):
        self.scroll_init_state()
        last_note_after_scroll = None

        while True:
            for note in self._notesList:
                if note.title() == title:
                    if not self.note_is_visible(note):
                        self.scroll_to_note(note)
                    return note

            last_note_before_scroll = self._notesList[-1]
            if last_note_after_scroll == last_note_before_scroll:
                break

            browser.execute_script('''document.evaluate("//div[@aria-label='grid']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollBy(0, ''' + str(self._notes_sidebar.rect.get('height')) + ''')''')
            time.sleep(2)
            self.reinit_notes_list()
            last_note_after_scroll = self._notesList[-1]

        return None

    def note_is_visible(self, note):
        if self._notesList.index(note)+1 > int(self._notes_sidebar.rect.get('height')/self._note_height):
            return False
        return True

    def scroll_to_note(self, note):
        browser.execute_script("document.getElementById('"+note.id+"').scrollIntoView({behavior:'smooth'})")
        time.sleep(2)

    def scroll_init_state(self):
        browser.execute_script(
            '''document.evaluate("//div[@aria-label='grid']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTo(0,0)''')
        self.reinit_notes_list()
        time.sleep(2)

    def notes_count(self):
        return int(re.match("\d+", self.notes_counter.text)[0])

    def first_note(self):
        if len(self._notesList) > 0:
            return self._notesList[0]
        else:
            return None

    def note_should_not_exist(self, title):
        assert self.note_by_title(title) is None

    def reinit_notes_list(self):
        self._notesList = [Note(s(by.xpath("//div[@id = '" + note.get_attribute('id') + "']")))
                           for note in ss(by.xpath("//div[substring(@id, string-length(@id) - string-length"
                                                   "('NOTES_SIDEBAR_NOTE') +1) ='NOTES_SIDEBAR_NOTE']"))]

    def delete_all_notes(self):
        while not self.page_is_empty():
            self.active_note.note_header.open_actions_dropdown().delete_note().confirm_action()

    def page_is_empty(self):
        try:
            self._no_notes_flag.should(be.in_dom, timeout=1)
            return True
        except TimeoutException:
            return False
