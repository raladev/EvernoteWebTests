from selene.api import *


class Note:

    def __init__(self, container):
        self.container = container
        # alternative xpath: ./div[substring(@id, string-length(@id) - string-length('NOTES_SIDEBAR_NOTE_SNIPPET') +1)
        # = 'NOTES_SIDEBAR_NOTE_SNIPPET']
        self.id = self.container.get_attribute('id')
        self._title = self.container.s(by.xpath("./div[1]"))
        self._body = self.container.s(by.xpath("./div[2]"))
        self._update_date = self.container.s(by.xpath("./div[3]"))

    def __eq__(self, other):
        try:
            if self.container == other.container:
                return True
            else:
                return False
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def title(self):
        return self._title.text

    def body(self):
        return self._body.text

    def update_date(self):
        return self._update_date.text

    def open(self):
        self.container.click()

    def date_should_be(self, text):
        self._update_date.should(have.text(text))

    def title_should_be(self, text):
        self._title.should(have.text(text))

    def body_should_be(self, text):
        self._body.should(have.text(text))

