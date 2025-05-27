from app_events.event_manager import EventManager
from app_events.stop_app_event import StopAppEvent

def get_help_info():
    return ["stop", "exit"], [], "stop application and send status to admin"

def get_console_command():
    return ["stop", "exit"], handle

async def handle(events: EventManager, args: str):
    print("⛔ Stopping bot...")
    await events.invoke(StopAppEvent())
