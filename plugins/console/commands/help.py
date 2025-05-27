from app_events.event_manager import EventManager
from plugin_managment import call_plugins

def get_console_command():
    return "help", handle

def get_help_info():
    return (
        ["console.help"],
        [],
        "Show available commands")

def setup(bot):
    call_plugins("Get info about console comands", "plugins.console.commands", "get_help_info", lambda m: register_help(*m()))

async def handle(events: EventManager, args):
    print("📖 Available commands:\n")

    for commands, params, description in help_data:
        command_str = ', '.join(commands)
        params_str = ' '.join(f"<{p}>" for p in params)
        full_command = f"{command_str} {params_str}".strip()
        print(f"🔹 {full_command.ljust(30)} — {description}")

help_data = []

def register_help(commands, params, description):
    help_data.append((commands, params, description))
