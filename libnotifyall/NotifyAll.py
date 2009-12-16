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

from libnotifyall.services.TwitterService import TwitterService
from libnotifyall.services.GmailService import GmailService
from libnotifyall.services.FacebookService import FacebookService

from libnotifyall import CONFIG_DIR, CONFIG_FILE
import os, time, sys

class NotifyAll:

    def __init__(self):
        self.services = []
        if not os.path.exists(CONFIG_DIR):
            self.create_initial_config()
        self._register_services()
        self._load_config()

    def create_initial_config(self):
        os.mkdir(CONFIG_DIR)
        f = open(CONFIG_FILE, 'w')
        configdata = """
[twitter]
username: myuser
password: mypass
interval: 35

[gmail]
username: myuser
password: mypass
# mark_viewed:
#   0 - show new/unread messages in each update
#   1 - show new/unread messages one time
mark_viewed: 1
interval: 60

[labels]
# labels to check in GMail
# Inbox is mandatory
label1: Inbox
label2: Label2
label3: Label3

[facebook]
# to see this values you must 
# visit http://www.facebook.com/notifications.php
# in your Facebook account and see the link for RSS
id: 0000
viewer: 0000
key: 0000
interval: 60
"""
        f.write(configdata)
        f.close()
        print "This is the first time you run Notify All"
        print "You must edit your user and password in " + CONFIG_FILE 
        print "and re-run Notify All."
        sys.exit(1)
    
    
    def _register_services(self):
        availables = dict(Twitter=TwitterService, Gmail=GmailService, Facebook=FacebookService)
        for name in iter(availables):
            self.services.append(availables[name]())

    def _load_config(self):
        for service in self.services:
            service.load_config()

    def start(self):
        for service in self.services:
            service.start()



