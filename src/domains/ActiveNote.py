from selene.api import *
from src.domains.ModalWindow import ModalWindow
import time


class ActiveNote:

    def __init__(self):
        self._container = s('#qa-NOTE_DETAIL')
        self.note_header = self.Header(self._container.s('#qa-NOTE_HEADER'))
        self._note_title = self._container.s("#qa-NOTE_EDITOR_TITLE")
        #in iframe
        self._note_textfield = s(by.xpath("//en-note[@id='en-note']"))

    def set_title(self, text):
        self._note_title.set_value(text)
        time.sleep(2)
        return self

    def set_body(self, text):
        browser.driver().switch_to.frame(0)
        self._note_textfield.set(text)
        time.sleep(2)
        browser.driver().switch_to.default_content()
        return self

    def title_should_be(self, text):
        self._note_title.should(have.attribute('value', text))

    def body_should_be(self, text):
        browser.driver().switch_to.frame(0)
        self._note_textfield.should(have.text(text))
        browser.driver().switch_to.default_content()

    class Header:

        def __init__(self, container):
            self._container = container
            self._actions_container = s('#qa-ACTIONS_MODAL')
            # self._notebook_name = s("#qa-NOTE_PARENT_NOTEBOOK_BTN")
            # self._share_btn = s("#qa-SHARE_BUTTON")
            # self._full_screen_btn = s("#qa-NOTE_FULLSCREEN_BTN")
            self._note_actions_dropdown = self._container.s(by.xpath(".//div[@data-tooltipmark='noteactionsdropdown']"))

        def open_actions_dropdown(self):
            self._note_actions_dropdown.click()
            return self.NoteActions(self._actions_container)

        class NoteActions:

            def __init__(self, container):
                self._container = container
                self._delete_note_btn = self._container.s('#qa-ACTION_DELETE')
                # self.share_note = container.s('#qa-ACTION_SHARE')
                # self.duplicate_note_btn = container.s('#qa-ACTION_DUPLICATE')

            def delete_note(self):
                self._delete_note_btn.click()
                return ModalWindow(confirm_btn=s('#qa-DELETE_CONFIRM_DIALOG_SUBMIT'),
                                   cancel_btn=s('#qa-DELETE_CONFIRM_DIALOG_SUBMIT'))
