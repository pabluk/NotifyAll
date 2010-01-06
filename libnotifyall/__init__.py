import os

APP_NAME = "Notify All"
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.notifyall')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'notifyall.cfg')

from libnotifyall.Message import Message
from libnotifyall.Service import Service
from libnotifyall.NotifyAll import NotifyAll

