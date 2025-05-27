import re
import shlex
from app_events.event_manager import EventManager

def get_help_info():
    return (
        ["console.debug.echo"],
        ["message"],
        "Prints the given message to the console.")

def get_console_command():
    return re.compile(r'^echo'), handle

async def handle(events: EventManager, args: str):
    args = shlex.split(args)
    msg = ' '.join(args[1:])
    print(msg)
    