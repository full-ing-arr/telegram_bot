import re
from aioconsole import ainput
from main import TelegramBot
from plugin_managment import call_plugins

registered_console_commands = []

def setup(bot: TelegramBot):
    call_plugins("Get console comands", "plugins.console.commands", "get_console_command", process_command)

async def parallel_task(bot: TelegramBot):
    while not bot.stop_event.is_set():
        cmd = await ainput("👥 Command: ")
        cmd = cmd.strip()
        handler, args = parse_console_command(cmd, registered_console_commands)

        if handler:
            await handler(bot, args)
        else:
            print("❗ Unknown command. Напиши 'help' для списку.")
    
def process_command(res):
    pattern, handler = res()
    
    if isinstance(pattern, str):
        patterns = [pattern]
    elif isinstance(pattern, re.Pattern):
        patterns = [pattern]
    else:
        patterns = pattern

    for p in patterns:
        registered_console_commands.append((p, handler))

def parse_console_command(cmd_text: str, commands):
    for pattern, handler in commands:
        if isinstance(pattern, str):
            if cmd_text == pattern:
                return handler, cmd_text
        elif isinstance(pattern, re.Pattern) or isinstance(pattern, str) and pattern.startswith('^'):
            if re.match(pattern, cmd_text):
                return handler, cmd_text
    return None, None
