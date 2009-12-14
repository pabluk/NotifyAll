#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

class Service:

    def __init__(self):
        self.configfile = 'app.cfg'
        self.last_id = 0
        self.messages = []
        self.first_run = True
        self.load_config()

    def load_config(self):
        pass

    def update(self):
        pass

    def show_messages(self):
        for msg in self.messages:
            if msg.viewed == False:
                print "[" + time.strftime("%H:%M") + "]",
                print "[" + msg.service + "] Showing... " + msg.title + ": " + msg.summary
                msg.show()
                msg.viewed = True

    def _reverse(self, data):
        for index in range(len(data)-1, -1, -1):
            yield data[index]


