from selene.api import *
import time


class ModalWindow:
    def __init__(self, confirm_btn, cancel_btn):
        self._confirm = confirm_btn
        self._cancel = cancel_btn

    def confirm_action(self):
        self._confirm().click()
        time.sleep(2)

    def cancel_action(self):
        self._cancel().click()
