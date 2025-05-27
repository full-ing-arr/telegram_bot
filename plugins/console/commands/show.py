import re
from app_events.event_manager import EventManager
from db import fetch_user_history

def get_help_info():
    return (
        ["console.show"],
        ["user_id"],
        "print a history with specific user")

def get_console_command():
    return re.compile(r'^show\s+\d+$'), handle

async def handle(events: EventManager, args: str):
    try:
        uid = int(args.strip().split()[1])
        rows = await fetch_user_history(uid)
        print(f"📨 History for {uid}:")
        if rows:
            for direction, text, ts in rows:
                print(f"[{ts}] {direction}: {text}")
        else:
            print("No messages.")
    except (IndexError, ValueError):
        print("❌ Invalid ID")
