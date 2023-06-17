import asyncio
from loguru import logger
from telebot.async_telebot import AsyncTeleBot
from telebot import types


async def cmd_start(bot: AsyncTeleBot, message: types.Message):
    await bot.reply_to(message, "Hello, I'm a bot")


async def cmd_help(bot: AsyncTeleBot, message: types.Message):
    await bot.reply_to(
        message,
        "A simple bot. Code: https://github.com/KanaMiao/TGVoteToJoinBot",
        disable_web_page_preview=True,
    )


async def new_request(bot: AsyncTeleBot, request: types.ChatJoinRequest, config):
    user_id = request.from_user.id
    user_nickname = request.from_user.first_name
    msg = await bot.send_message(request.chat.id,
                                 f"New request from [{user_nickname}](tg://user?id={user_id})",
                                 parse_mode="MarkdownV2",)
    polling = await bot.send_poll(request.chat.id,
                                  f"Approve this request?",
                                  ["Approve", "Decline"],
                                  is_anonymous=True,
                                  allows_multiple_answers=False,
                                  reply_to_message_id=msg.message_id,
                                  )
    await asyncio.sleep(300)
    try:
        polling = await bot.stop_poll(request.chat.id, polling.message_id)
        if polling.total_voter_count == 0:
            await bot.send_message(request.chat.id, "No one vote, request rejected", reply_to_message_id=msg.message_id)
            await bot.decline_chat_join_request(request.chat.id, request.from_user.id)
            await bot.send_message(user_id, "No one vote. Your request has been rejected")
        elif polling.options[0].voter_count > polling.options[1].voter_count:
            await bot.send_message(request.chat.id, "Approved", reply_to_message_id=msg.message_id)
            await bot.approve_chat_join_request(request.chat.id, request.from_user.id)
            await bot.send_message(user_id, "Your request has been approved")
        elif polling.options[1].voter_count > polling.options[0].voter_count:
            await bot.send_message(request.chat.id, "Declined", reply_to_message_id=msg.message_id)
            await bot.decline_chat_join_request(request.chat.id, request.from_user.id)
            await bot.send_message(user_id, "Your request has been declined")
        elif polling.options[0].voter_count == polling.options[1].voter_count:
            await bot.send_message(request.chat.id, "Tie", reply_to_message_id=msg.message_id)
            await bot.decline_chat_join_request(request.chat.id, request.from_user.id)
            await bot.send_message(user_id, "Your request has been declined")
        else:
            await bot.send_message(request.chat.id, "Error", reply_to_message_id=msg.message_id)
            await bot.decline_chat_join_request(request.chat.id, request.from_user.id)
            await bot.send_message(user_id, "Error")
    except Exception as e:
        logger.error(e)
