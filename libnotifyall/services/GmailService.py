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

    def __init__(self):
        Service.__init__(self, __name__)

    def load_config(self):
        Service.load_config(self)

        config = ConfigParser.ConfigParser()

        config.read(CONFIG_FILE)
        self.username = config.get("gmail", "username")
        self.password = config.get("gmail", "password")
        self.mark_viewed = config.getboolean("gmail", "mark_viewed")
        self.interval = int(config.get("gmail", "interval"))
        self.labels = config.items("labels")
        self.atom_url = "https://mail.google.com/mail/feed/atom"

    def update(self):

        auth = urllib2.HTTPBasicAuthHandler()
        auth.add_password("New mail feed", self.atom_url, 
                          self.username, self.password)
        opener = urllib2.build_opener(auth)

        for label in self.labels:
            try:
                feed = opener.open(self.atom_url + "/" + label[1])
                logging.debug("[Gmail] " + label[1] + " update... OK")
            except urllib2.HTTPError as detail:
                if str(detail) == "HTTP Error 401: Unauthorized":
                    logging.error("[Gmail] " + label[1] + " update... " \
                                  "ERROR (You must verify your " \
                                  "username or password)")
                else:
                    logging.error("[Gmail] " + label[1] + \
                                  " update... ERROR")
                return 1

            a = feedparser.parse(feed)

            for entry in a['entries']:
                message_exists = False
                for message in self.messages:
                    if message.id == entry.link:
                        message_exists = True

                if not message_exists:
                    m = Message(entry.link, 'Gmail',
                                entry.author_detail.name, entry.title,
                                os.getcwd() + "/icons/" + "gmail.png")
                    self.messages.append(m)
                else:
                    if not self.mark_viewed:
                        message.viewed = False

        self.first_run = False

