from telegram.ext import filters
from plugin_managment import call_plugins
from config import ADMIN_CHAT_ID
from main import TelegramBot

group_filter = filters.User(ADMIN_CHAT_ID)

def setup(bot: TelegramBot):
    def process_get_handler_info(get_handler_info):
        command, handler = get_handler_info(bot.events)
        hnd = command.to_handler(handler, group_filter)
        bot.add_handler(hnd)

    call_plugins("Get admin's comands", 'plugins.messages.admin_handlers', 'get_handler_info', process_get_handler_info)
