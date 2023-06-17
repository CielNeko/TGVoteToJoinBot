import asyncio
from app import event
from loguru import logger
from telebot import util
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage


class BotRunner(object):
    def __init__(self, config):
        self.bot = config.bot
        self.proxy = config.proxy

    def botcreate(self):
        bot = AsyncTeleBot(self.bot.botToken, state_storage=StateMemoryStorage())
        return bot, self.bot

    def run(self):
        # print(self.bot)
        logger.success("Bot Start")
        bot, _config = self.botcreate()
        if self.proxy.status:
            from telebot import asyncio_helper
            asyncio_helper.proxy = self.proxy.url
            logger.success("Proxy Set")

        @bot.message_handler(commands=["start", "help"], chat_types=['private'])
        async def handle_command(message):
            if "/start" in message.text:
                await event.cmd_start(bot, message)
            elif "/help" in message.text:
                await event.cmd_help(bot, message)

        # 加群事件捕获与处理
        @bot.chat_join_request_handler
        async def new_join_request(message):
            await event.new_request(bot, message, _config)

        async def main():
            await asyncio.gather(bot.polling(non_stop=True, allowed_updates=util.update_types))

        asyncio.run(main())
