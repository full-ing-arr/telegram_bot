import asyncio
from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from db import init_db
from plugin_managment import call_plugins
from app_events.event_manager import EventManager
from app_events.stop_app_event import StopAppEvent

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.stop_event = asyncio.Event()
        self.app = None
        self.parallel_tasks = []
        self.events = EventManager()

    async def stop_app_handler(self, event_data: StopAppEvent):
        self.stop_event.set()

        for task in self.parallel_tasks:
            task.cancel()

    def add_handler(self, handler):
        if self.app:
            self.app.add_handler(handler)
        else:
            raise RuntimeError("Application is not initialized yet")

    async def start(self):
        await init_db()
        self.app = ApplicationBuilder().token(self.token).build()
        
        self.events.listen(StopAppEvent, self.stop_app_handler)

        call_plugins("Setup plugins", "plugins", "setup", lambda m: m(self))
        call_plugins("Run parallel tasks", "plugins", "parallel_task", lambda m: self.parallel_tasks.append(asyncio.create_task(m(self))))

        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

        await self.stop_event.wait()

        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()

if __name__ == "__main__":
    bot = TelegramBot(BOT_TOKEN)
    asyncio.run(bot.start())
