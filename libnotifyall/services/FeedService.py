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

from libnotifyall.Message import Message
from libnotifyall.Service import Service
from libnotifyall import CONFIG_DIR, CONFIG_FILE
from libnotifyall import Logger
import feedparser
import ConfigParser
import os, urllib2, time, sys, logging

class FeedService(Service):

    def load_config(self):
        Service.load_config(self)

        config = ConfigParser.ConfigParser()

        config.read(CONFIG_FILE)
        self.interval = int(config.get("feed", "interval"))
        self.feeds = config.items("feeds")

    def update(self):

        for feed in self.feeds:

            try:
                a = feedparser.parse(feed[1])
                logging.debug("[Feed] Update " + feed[1] +"... OK")
            except:
                logging.error("[Feed] Update... ERROR")
                return 1
    
            for entry in self._reverse(a['entries']):
                message_exists = False
                for message in self.messages:
                    if message.id == entry.link:
                        message_exists = True
                        break
    
                if not message_exists:
                    m = Message(entry.link, 'Feed',
                                entry.title, entry.link,
                                os.getcwd() + "/icons/" + "rss.png")
    
                    if self.ignore_init_msgs and self.first_run:
                        m.viewed = True
    
                    self.messages.append(m)
    
        self.first_run = False

    def _remove_html_tags(self, data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)
