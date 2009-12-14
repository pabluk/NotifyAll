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

from libnotifyall.services.TwitterService import TwitterService
from libnotifyall.services.GmailService import GmailService
from libnotifyall.services.FacebookService import FacebookService
import os, time, sys

from libnotifyall import CONFIG_DIR, CONFIG_FILE

def create_initial_config():
    os.mkdir(CONFIG_DIR)
    f = open(CONFIG_FILE, 'w')
    configdata = """
[twitter]
username: myuser
password: mypass
interval: 35

[gmail]
username: myuser
password: mypass
interval: 60

[labels]
# Add labels from you GMail account to be checked
label1: Inbox
label2: Label2
label3: Label3

"""
    f.write(configdata)
    f.close()
    print "This is the first time you run Notify All"
    print "You must edit your user and password in " + CONFIG_FILE 
    print "and re-run Notify All."
    sys.exit(1)


if __name__ == "__main__":

    if not os.path.exists(CONFIG_DIR):
        create_initial_config()

    s1 = TwitterService()
    s2 = GmailService()
    s3 = FacebookService()
    while 1:
        s1.update()
        s1.show_messages()
        s2.update()
        s2.show_messages()
        s3.update()
        s3.show_messages()
        time.sleep(80)

