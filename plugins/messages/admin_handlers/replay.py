import shlex
from telegram import Update
from telegram.ext import ContextTypes
from db import log_message
from ..commands.filter_commands import Command

command = Command('send', "")

def get_handler_info(events):
    return command, get_handler

async def get_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = shlex.split(update.message.text)
    client_id = int(args[1])
    msg = ' '.join(args[2:])
    await log_message(client_id, 'Admin', 'to_client', msg)
    await context.bot.send_message(client_id, f"💬 Admin: {msg}")
    await update.message.reply_text('✅ Reply sent.')
