import os

__all__ = ['NotifyAll', 'Service', 'Message']

APP_NAME = "Notify All"
CONFIG_DIR = os.path.expanduser('~') + "/" + ".notifyall"
CONFIG_FILE = CONFIG_DIR + '/' + 'notifyall.cfg'

