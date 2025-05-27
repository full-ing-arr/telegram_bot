import re
from telegram.ext import MessageHandler, CommandHandler, filters

class Parce:
    def __init__(self, pattern=None, description=None):
        self.pattern = re.compile(pattern or r'.*')
        self.description = description

    def to_handler(self, handler, filter):
        f = filter
        if not self.pattern:
            f = f & filters.Regex(self.pattern)
        return MessageHandler(f, handler)


class Command:
    def __init__(self, command, description=None):
        self.command = command
        self.description = description

    def to_handler(self, handler, filter):
        return CommandHandler(self.command, handler, filters=filter)
