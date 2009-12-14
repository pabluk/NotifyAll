#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnotifyme.message import Message
from libnotifyme.service import Service
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
        #print "[" + time.strftime("%H:%M") + "]",
        #print "[Gmail] Updating...",
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
                            m = Message(entry.link, 'Gmail', entry.author_detail.name, entry.title, os.getcwd() + "/" + "gmail.png")
                            self.messages.append(m)
        #print "[OK]"

