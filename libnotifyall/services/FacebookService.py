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
        Service._load_config(self)

        config = ConfigParser.ConfigParser()

        config.read(CONFIG_FILE)
        self._disabled = config.getboolean(self.SRV_NAME, "disabled")
        self.fbid = config.get(self.SRV_NAME, "id")
        self.viewer = config.get(self.SRV_NAME, "viewer")
        self.key = config.get(self.SRV_NAME, "key")
        self.interval = int(config.get(self.SRV_NAME, "interval"))
        self.feed_url = self.FB_URL + \
                        "id=" + self.fbid + \
                        "&viewer=" + self.viewer + \
                        "&key=" + self.key + \
                        "&format=rss20"

    def _get_updates(self):
        """Retrieves updates from Facebook notification feed and return an array of entries."""
        entries = []
        try:
            a = feedparser.parse(self.feed_url)
        except:
            self.logger.error("Update error")
        else:
            self.logger.debug("Updated")
            entries.extend(a['entries'])
        finally:
            return entries

    def _normalize_entries(self, entries):
        """Normalizes and sorts an array of entries and returns an array of messages."""
        messages = []

        for entry in self._reverse(entries):
            if entry.has_key('link') and entry.has_key('title') and entry.has_key('date'):

                # We use the link as an id because the id 
                # provided is not reliable
                m = Message(entry.link, self.SRV_NAME,
                            entry.title, entry.date,
                            os.getcwd() + "/icons/" + "facebook.png")
                messages.append(m)

        return messages


