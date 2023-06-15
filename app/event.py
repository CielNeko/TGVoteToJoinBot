import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types


async def start(bot: AsyncTeleBot, message: types.Message):
    await bot.reply_to(message, "Hello, I'm a bot")


async def help(bot: AsyncTeleBot, message: types.Message):
    await bot.reply_to(message, "A simple bot. Code: github.com/KanaMiao/TGVoteToJoinBot")


async def new_request(bot: AsyncTeleBot, request: types.ChatJoinRequest):
    user_id = request.from_user.id
    user_nickname = request.from_user.first_name
    polling = await bot.send_poll(request.chat.id,
                                  f"Approve {user_nickname}({user_id}) 's Join Request?",
                                  ["Approve", "Decline"],
                                  is_anonymous=True,
                                  allows_multiple_answers=False,
                                  )
    await asyncio.sleep(300)
    poll_msg_id = polling.message_id
    polling = await bot.stop_poll(request.chat.id, poll_msg_id)
    if polling.total_voter_count == 0:
        await bot.send_message(request.chat.id, "No one vote, request rejected", reply_to_message_id=poll_msg_id)
        await bot.send_message(user_id, "No one vote. Your request has been rejected")
        await bot.decline_chat_join_request(request.chat.id, request.from_user.id)
    elif polling.options[0].voter_count > polling.options[1].voter_count:
        await bot.send_message(request.chat.id, "Approved", reply_to_message_id=poll_msg_id)
        await bot.send_message(user_id, "Your request has been approved")
        await bot.approve_chat_join_request(request.chat.id, request.from_user.id)
    elif polling.options[1].voter_count > polling.options[0].voter_count:
        await bot.send_message(request.chat.id, "Declined", reply_to_message_id=poll_msg_id)
        await bot.send_message(user_id, "Your request has been declined")
        await bot.decline_chat_join_request(request.chat.id, request.from_user.id)
    elif polling.options[0].voter_count == polling.options[1].voter_count:
        await bot.send_message(request.chat.id, "Tie", reply_to_message_id=poll_msg_id)
        await bot.send_message(user_id, "Your request has been declined")
        await bot.decline_chat_join_request(request.chat.id, request.from_user.id)
    else:
        await bot.send_message(request.chat.id, "Error", reply_to_message_id=poll_msg_id)
        await bot.send_message(user_id, "Error")
        await bot.decline_chat_join_request(request.chat.id, request.from_user.id)
