from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_CHAT_ID
from db import log_message
from ..commands.filter_commands import Parce

command = Parce(None, "")

def get_handler_info(events):
    return command, get_handler

async def get_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    await log_message(user.id, user.full_name, 'from_client', text)
    await context.bot.send_message(ADMIN_CHAT_ID, f"📩 From {user.full_name} (ID: {user.id}): {text}")
    await context.bot.send_message(user.id, "✅ Your message has been sent. Please wait for a reply.")
