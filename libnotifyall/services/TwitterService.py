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

import twitter
import ConfigParser
import os, urllib2, time

class TwitterService(Service):

    def load_config(self):

        config = ConfigParser.ConfigParser()

        config.read(self.configfile)
        self.username = config.get("twitter", "username")
        self.password = config.get("twitter", "password")
        self.interval = int(config.get("twitter", "interval"))
        if not os.path.exists(self.configdir + "/twitter"):
            os.mkdir(self.configdir + "/twitter")

    def update(self):
        print "[" + time.strftime("%H:%M") + "]",
        print "[Twitter] Updating...",
        self.messages = []
        api = twitter.Api(self.username, self.password)
        try:
            statuses = api.GetFriendsTimeline(since_id = self.last_id)
            print "[OK]"
        except:
            print "[ERROR]",
            print "(You must verify your username or password)"
            return 1
        quantity = len(statuses)
        i = 0
        for status in self._reverse(statuses):
            if not os.path.exists(self.configdir + "/twitter/" + str(status.user.id) + ".jpg"):
                avatar = urllib2.urlopen(status.user.profile_image_url)
                avatar_file = open(self.configdir + "/twitter/" + str(status.user.id) + '.jpg', 'wb')
                avatar_file.write(avatar.read())
                avatar_file.close()

            self.last_id = status.id
            m = Message(status.id, 'Twitter', status.user.name + " (" + status.user.screen_name + ")", status.text, self.configdir + "/twitter/" + str(status.user.id) + ".jpg")
            self.messages.append(m)


