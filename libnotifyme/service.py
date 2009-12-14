#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Notify All - Copyright (c) 2009 Juan Pablo Seminario
# This software is distributed under the terms of the GNU General
# Public License
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from libnotifyme import CONFIG_DIR, CONFIG_FILE
import time

class Service:

    def __init__(self):

        self.configfile = CONFIG_FILE
        self.configdir = CONFIG_DIR
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


