# -*- coding: utf-8 -*-


class Borg:
    """ a borg style singleton """
    _shared_state = {}

    def __init__(self):
        """ init """
        self.__dict__ = self.shared_state
