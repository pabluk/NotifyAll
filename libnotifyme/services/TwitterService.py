#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnotifyme.message import Message
from libnotifyme.service import Service
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

    def update(self):
        #print "[" + time.strftime("%H:%M") + "]",
        #print "[Twitter] Updating...",
        self.messages = []
        api = twitter.Api(self.username, self.password)
        statuses = api.GetFriendsTimeline(since_id = self.last_id)
        quantity = len(statuses)
        i = 0
        for status in self._reverse(statuses):
            if not os.path.exists(os.getcwd() + "/" + str(status.user.id) + ".jpg"):
                avatar = urllib2.urlopen(status.user.profile_image_url)
                avatar_file = open(str(status.user.id) + '.jpg', 'wb')
                avatar_file.write(avatar.read())
                avatar_file.close()

            self.last_id = status.id
            if not self.first_run:
                m = Message(status.id, 'Twitter', status.user.name + " (" + status.user.screen_name + ")", status.text, os.getcwd() + "/" + str(status.user.id) + ".jpg")
                self.messages.append(m)
        self.first_run = False
        #print "[OK]"


