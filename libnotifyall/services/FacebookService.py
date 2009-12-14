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

class FacebookService(Service):

    def load_config(self):

        config = ConfigParser.ConfigParser()

        config.read(self.configfile)
        self.fbid = config.get("facebook", "id")
        self.viewer = config.get("facebook", "viewer")
        self.key = config.get("facebook", "key")
        self.interval = int(config.get("facebook", "interval"))
        self.feed_url = "http://www.facebook.com/feeds/notifications.php?id="+self.fbid+"&viewer="+self.viewer+"&key="+self.key+"&format=rss20"

    def update(self):

        print "[" + time.strftime("%H:%M") + "]",
        print "[Facebook] Updating ...",
        try:
            a = feedparser.parse(self.feed_url)
            print "[OK]"
        except:
            print "[ERROR]",
            print "(You must verify your configuration)"
            return 1

        if len(a['entries']) > 0:
            for entry in self._reverse(a['entries']):
                message_exists = False
                for message in self.messages:
                    if message.id == entry.link:
                        message_exists = True

                if not message_exists:
                    m = Message(entry.link, 'Facebook', entry.title, entry.date, os.getcwd() + "/icons/" + "facebook.png")
                    self.messages.append(m)

