from typing import Type

from telebot.async_telebot import AsyncTeleBot
from telebot import types
from utils.base import join_request_details


async def start(bot: AsyncTeleBot, message: types.Message, config):
    await bot.reply_to(message, config.about)


async def help(bot: AsyncTeleBot, message: types.Message, config):
    await bot.reply_to(message, config.help)


async def get_join_request_details(message: types.ChatJoinRequest) -> join_request_details:
    user_id = message.from_user.id
    chat_id = message.chat.id
    return join_request_details(user=user_id, chat=chat_id)


async def send_poll(bot: AsyncTeleBot, message: join_request_details, config):
    await bot.send_poll(message.chat, config.poll_question, config.poll_options, is_anonymous=True)


async def approve_join_request(bot: AsyncTeleBot, message: join_request_details):
    await bot.approve_chat_join_request(message.user, message.chat)


async def decline_join_request(bot: AsyncTeleBot, message: join_request_details):
    await bot.decline_chat_join_request(message.user, message.chat)
