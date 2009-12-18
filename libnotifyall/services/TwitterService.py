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
import time
import urllib2
import ConfigParser
import logging

import twitter

from libnotifyall import CONFIG_DIR, CONFIG_FILE
from libnotifyall import Message
from libnotifyall import Service
from libnotifyall import Logger

class TwitterService(Service):

    def __init__(self):
        Service.__init__(self, __name__)

    def load_config(self):
        Service.load_config(self)

        config = ConfigParser.ConfigParser()

        config.read(CONFIG_FILE)
        self.username = config.get("twitter", "username")
        self.password = config.get("twitter", "password")
        self.interval = int(config.get("twitter", "interval"))
        if not os.path.exists(CONFIG_DIR + "/twitter"):
            os.mkdir(CONFIG_DIR + "/twitter")

    def update(self):

        self.messages = []
        api = twitter.Api(self.username, self.password)

        try:
            statuses = api.GetFriendsTimeline(since_id = self.last_id)
            logging.debug("[Twitter] Update... OK")
        except:
            logging.error("[Twitter] Update... ERROR")
            return 1

        for status in self._reverse(statuses):
            self.last_id = status.id
            if not (self.ignore_init_msgs and self.first_run):

                if not os.path.exists(CONFIG_DIR + "/twitter/" + \
                                      str(status.user.id) + ".jpg"):
                    avatar = urllib2.urlopen(status.user.profile_image_url)
                    avatar_file = open(CONFIG_DIR + "/twitter/" + \
                                       str(status.user.id) + '.jpg', 'wb')
                    avatar_file.write(avatar.read())
                    avatar_file.close()

                m = Message(status.id, 'Twitter',
                            status.user.name + " (" + \
                            status.user.screen_name + ")",
                            status.text, self.configdir + "/twitter/" + \
                            str(status.user.id) + ".jpg")
                self.messages.append(m)

        self.first_run = False
