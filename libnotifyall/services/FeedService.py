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

class FeedService(Service):
    """Class to implement notifications from any RSS or Atom feed."""

    SRV_NAME = 'feed'

    def __init__(self):
        Service.__init__(self, self.SRV_NAME)

    def load_config(self):
        """Load configuration settings from the feed section in CONFIG_FILE."""
        Service._load_config(self)

        config = ConfigParser.ConfigParser()

        config.read(CONFIG_FILE)
        self.interval = int(config.get(self.SRV_NAME, "interval"))
        self.feeds = config.items("feeds")

    def _get_updates(self):
        """Retrieves updates from feed and return an array of entries."""
        all_entries = []
        for feed in self.feeds:
            try:
                a = feedparser.parse(feed[1])
                logging.debug("[" + self.SRV_NAME + "] Updated " + feed[1])
                all_entries.extend(a['entries'])
            except:
                logging.error("[" + self.SRV_NAME + "] Update error in " + feed[1])
                return 0
        return all_entries
    
    def _normalize_entries(self, entries):
        """Normalizes and sorts an array of entries and returns an array of messages."""
        messages = []

        for entry in self._reverse(entries):
            if entry.has_key('link') and entry.has_key('title'):

                m = Message(entry.link, self.SRV_NAME,
                            entry.title, entry.link,
                            os.getcwd() + "/icons/" + "rss.png")
                messages.append(m)

        return messages


