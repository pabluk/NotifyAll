#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pynotify

class Message:

    def __init__(self, id = '', service = '', title = '', summary= '', icon = ''):
        self.id = id
        self.service = service
        self.title = title
        self.summary = summary
        self.icon = icon
        self.viewed = False

    def show(self):
        pynotify.init('NotifyMe')
        m = pynotify.Notification(self.title, self.summary, self.icon)
        m.show()

