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

class GmailService(Service):
    """Class to implement notifications from GMail Atom Feed."""

    SRV_NAME = 'gmail'
    ATOM_URL = 'https://mail.google.com/mail/feed/atom'

    def __init__(self):
        Service.__init__(self, self.SRV_NAME)

    def load_config(self):
        """Load configuration settings from the gmail section in CONFIG_FILE."""
        Service._load_config(self)

        config = ConfigParser.ConfigParser()

        config.read(CONFIG_FILE)
        self._disabled = config.getboolean(self.SRV_NAME, "disabled")
        self.username = config.get(self.SRV_NAME, "username")
        self.password = config.get(self.SRV_NAME, "password")
        self.interval = int(config.get(self.SRV_NAME, "interval"))
        self.labels = config.items("labels")

    def _get_updates(self):
        """Retrieves updates from GMail Atom feed and return an array of entries."""
        all_entries = []
        auth = urllib2.HTTPBasicAuthHandler()
        auth.add_password("New mail feed", self.ATOM_URL, 
                          self.username, self.password)
        opener = urllib2.build_opener(auth)

        for label in self.labels:
            try:
                feed = opener.open(self.ATOM_URL + "/" + label[1])
            except urllib2.HTTPError as detail:
                if str(detail) == "HTTP Error 401: Unauthorized":
                    self.logger.error("Update error in " + label[1] + " label " \
                                  "(You must check your username or password)")
                else:
                    self.logger.error("Update error in " + label[1] + " label")
            except urllib2.URLError as detail:
                    self.logger.error("Update error in " + label[1] + " label")
            else:
                self.logger.debug("Updated " + label[1] + " label")
                a = feedparser.parse(feed)
                all_entries.extend(a['entries'])

        return all_entries

    def _normalize_entries(self, entries):
        """Normalizes and sorts an array of entries and returns an array of messages."""
        messages = []

        for entry in entries:
            if entry.has_key('link') and entry.has_key('title'):

                m = Message(entry.link, self.SRV_NAME,
                            entry.author_detail.name, entry.title,
                            os.getcwd() + "/icons/" + "gmail.png")
                messages.append(m)

        return messages


