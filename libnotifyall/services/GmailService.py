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

from libnotifyall.message import Message
from libnotifyall.service import Service
import feedparser
import ConfigParser
import os, urllib2, time, sys

class GmailService(Service):

    def load_config(self):

        config = ConfigParser.ConfigParser()

        config.read(self.configfile)
        self.username = config.get("gmail", "username")
        self.password = config.get("gmail", "password")
        self.interval = int(config.get("gmail", "interval"))
        self.labels = config.items("labels")
        self.atom_url = "https://mail.google.com/mail/feed/atom"

    def update(self):
        print "[" + time.strftime("%H:%M") + "]",
        print "[Gmail] Updating...",
        #self.messages = []

        auth = urllib2.HTTPBasicAuthHandler()
        auth.add_password("New mail feed", self.atom_url, self.username, self.password)
        opener = urllib2.build_opener(auth)

        if len(self.labels) > 0:
            for label in self.labels:

                try:
                    feed = opener.open(self.atom_url + "/" + label[1])
                except urllib2.HTTPError as detail:
                    print detail
                    if str(detail) == "HTTP Error 401: Unauthorized":
                        print "You must verify your username and password in " + self.configfile
                    sys.exit(1)

                a = feedparser.parse(feed)
                if len(a['entries']) > 0:
                    for entry in a['entries']:
                        message_exists = False
                        for message in self.messages:
                            if message.id == entry.link:
                                message_exists = True

                        if not message_exists:
                            m = Message(entry.link, 'Gmail', entry.author_detail.name, entry.title, os.getcwd() + "/icons/" + "gmail.png")
                            self.messages.append(m)
        print "[OK]"
