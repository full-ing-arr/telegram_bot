from telegram import Update
from telegram.ext import ContextTypes
from db import fetch_user_history
from ..commands.filter_commands import Command

command = Command('show', "")

def get_handler_info(events):
    return command, get_handler

async def get_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = int(context.args[0])
    rows = await fetch_user_history(uid)
    if rows:
        lines = [f"[{ts}] {direction}: {text}" for direction, text, ts in rows]
        await update.message.reply_text(f"History for {uid}:\n" + "\n".join(lines))
    else:
        await update.message.reply_text('No messages.')
