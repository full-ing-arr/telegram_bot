from telegram import Update
from telegram.ext import ContextTypes
from app_events.event_manager import EventManager
from app_events.stop_app_event import StopAppEvent
from ..commands.filter_commands import Command

command = Command('stop', "")

def get_handler_info(events: EventManager):
    async def get_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('⛔ Stopping bot...')
        await events.invoke(StopAppEvent())

    return command, get_handler
