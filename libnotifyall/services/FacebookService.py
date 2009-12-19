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
import sys
import time
import urllib2
import logging
import ConfigParser

import feedparser

from libnotifyall import CONFIG_DIR, CONFIG_FILE
from libnotifyall import Message
from libnotifyall import Service
from libnotifyall import Logger

class FacebookService(Service):
    """Class to implement notifications from Facebook notification feed."""

    SRV_NAME = 'facebook'
    FB_URL = 'http://www.facebook.com/feeds/notifications.php?'

    def __init__(self):
        Service.__init__(self, self.SRV_NAME)
        
    def load_config(self):
        """Load configuration settings from the facebook section in CONFIG_FILE."""
        Service.load_config(self)

        config = ConfigParser.ConfigParser()

        config.read(CONFIG_FILE)
        self.fbid = config.get(self.SRV_NAME, "id")
        self.viewer = config.get(self.SRV_NAME, "viewer")
        self.key = config.get(self.SRV_NAME, "key")
        self.interval = int(config.get(self.SRV_NAME, "interval"))
        self.feed_url = self.FB_URL + \
                        "id=" + self.fbid + \
                        "&viewer=" + self.viewer + \
                        "&key=" + self.key + \
                        "&format=rss20"

    def update(self):
        """Gets and stores the entries from Facebook notification feed."""
        try:
            a = feedparser.parse(self.feed_url)
            logging.debug("[" + self.SRV_NAME + "] Update... OK")
        except:
            logging.error("[" + self.SRV_NAME + "] Update... ERROR")
            return 1

        # Sort entries by date ascending order with _reverse()
        for entry in self._reverse(a['entries']):
            message_exists = False

            for message in self.messages:
                if message.id == entry.link:
                    message_exists = True
                    break

            if not message_exists:
                m = Message(entry.link, self.SRV_NAME,
                            entry.title, entry.date,
                            os.getcwd() + "/icons/" + "facebook.png")
                if self.ignore_init_msgs and self.first_run:
                    m.viewed = True
                self.messages.append(m)

        self.first_run = False

