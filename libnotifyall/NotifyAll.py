#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Notify All - Copyright (c) 2009 Pablo Seminario
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

import os
import time
import sys
import logging

from libnotifyall import CONFIG_DIR, CONFIG_FILE
from libnotifyall import Logger
from libnotifyall.services import TwitterService
from libnotifyall.services import GmailService
from libnotifyall.services import FacebookService
from libnotifyall.services import FeedService

class NotifyAll:
    """A class that contains all services."""

    def __init__(self):
        self.logger = logging.getLogger('NotifyAll')
        self.logger.info("Started")
        self.services = []
        if not os.path.exists(CONFIG_DIR):
            self._create_initial_config()
        self._register_services()
        self._load_config()

    def _create_initial_config(self):
        """Creates the configuration dir and writes a sample configuration."""
        os.mkdir(CONFIG_DIR)
        f = open(CONFIG_FILE, 'w')
        configdata = """
[notifyall]
# show old messages
ignore_init_msgs: 0
# to run without libnotify
disable_libnotify: 0
# Valid values for loglevel
# debug, info, warning, error, critical
loglevel: info

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

[feed]
interval: 120

[feeds]
url1: http://barrapunto.com/barrapunto.rss
url2: http://planet.gnome.org/atom.xml

"""
        f.write(configdata)
        f.close()
        print "This is the first time you run Notify All" + \
              "You must edit your user and password in " + CONFIG_FILE + \
              "and re-run Notify All."
        sys.exit(1)
    
    
    def _register_services(self):
        """Add the services available to the array of services."""
        availables = dict(Facebook=FacebookService,
                          Feed=FeedService,
                          Gmail=GmailService,
                          Twitter=TwitterService)
        for name in iter(availables):
            self.services.append(availables[name]())

    def _load_config(self):
        """Load the required settings for each service."""
        for service in self.services:
            service.load_config()

    def start(self):
        """Start a thread for each registered service."""
        for service in self.services:
            if not service._disabled:
                service.start()



