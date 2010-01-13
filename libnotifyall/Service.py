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
import time
import pickle
import logging
import ConfigParser
from threading import Thread

from libnotifyall import CONFIG_DIR, CONFIG_FILE
from libnotifyall import Logger

class Service(Thread):
    """Threading class base for services."""

    def __init__(self, srv_name):

        self.srv_name = srv_name
        self.configfile = CONFIG_FILE
        self.configdir = CONFIG_DIR
        self.last_id = 0
        self.messages = []
        self.disable_libnotify = False
        self.logger = logging.getLogger(srv_name.title())

        Thread.__init__(self, name=srv_name)
        self.logger.debug("Thread started")

        self._load_config()

    def _load_config(self):
        """Load configuration settings for NotifyAll."""
        LOG_LEVELS = {'debug': logging.DEBUG,
                      'info': logging.INFO,
                      'warning': logging.WARNING,
                      'error': logging.ERROR,
                      'critical': logging.CRITICAL}

        config = ConfigParser.ConfigParser()

        config.read(CONFIG_FILE)
        self.disable_libnotify = config.getboolean("notifyall",
                                                   "disable_libnotify")
        self.loglevel = config.get("notifyall", "loglevel")
        self.logger.setLevel(LOG_LEVELS.get(self.loglevel, logging.INFO))

    def _add_new_messages(self, new_messages):
        """Add new messages to the array of messages."""
        # Fixed: maybe this could be improved
        for new_message in new_messages:

            for message in self.messages:
                if new_message.id == message.id:
                    if message.viewed == True:
                        new_message.viewed = True
                    break

        self.messages = new_messages
        return

    def _show_unseen_messages(self):
        """Shows the messages unseen."""
        for msg in self.messages:
            if not msg.viewed:
                if not self.disable_libnotify and os.environ.has_key('DISPLAY'):
                    if not msg.show():
                        break
                self.logger.info(msg.title + ": " + msg.summary)
                msg.viewed = True

    def _unseen_messages(self):
        """Returns the number of unseen messages."""
        i = 0
        for message in self.messages:
            if not message.viewed:
                i += 1
        return i

    def _reverse(self, data):
        """Returns the same array in reverse order."""
        for index in range(len(data)-1, -1, -1):
            yield data[index]

    def _load_messages(self):
        filename = os.path.join(self.configdir, self.srv_name + '.dat')
        if os.path.exists(filename):
            file = open(filename, 'r')
            self.messages = pickle.load(file)
            self.logger.debug("Loaded messages")
        else:
            self.logger.debug("Messages file does not exist")
        return

    def _save_messages(self):
        filename = os.path.join(self.configdir, self.srv_name + '.dat')
        file = open(filename, 'w')
        pickle.dump(self.messages, file)
        self.logger.debug("Saved messages")
        return

    def run(self):
        """Start the loop to update the service and display their own messages."""
        self._load_messages()
        while True:
            entries = self._get_updates()
            new_messages = self._normalize_entries(entries)
            self._add_new_messages(new_messages)
            self._save_messages()
            self._show_unseen_messages()

            self.logger.debug("Unseen message(s): " + str(self._unseen_messages()) + " of " + str(len(self.messages)))
            time.sleep(self.interval)


