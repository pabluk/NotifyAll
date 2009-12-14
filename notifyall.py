#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnotifyme.services.TwitterService import TwitterService
from libnotifyme.services.GmailService import GmailService
import time

s1 = TwitterService()
s2 = GmailService()
while 1:
    s1.update()
    s1.show_messages()
    s2.update()
    s2.show_messages()
    time.sleep(80)

