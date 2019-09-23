from typing import Any

from aiogram.types import Update, CallbackQuery, Message
from aiohttp import web

from common import db, sed
import conversations as conv
import commands as cmd
import handlers as handle


async def dispatch_msg(update: Message) -> Any:
    deal = db.LockedDeal.find_where(chat=update.chat.id, _quantity=1)
    if deal is None:
        return

    if update.text is not None:
        if update.text == cmd.HELP:
            return await handle.help(deal)

        if deal.in_chat.creator and deal.in_chat.contributor:
            if update.text == cmd.SECURE_DEAL:
                return await handle.secure_deal(deal)

            if update.text == cmd.CLOSE_DEAL:
                return await handle.close_deal(deal)

            if deal.conv.name == conv.START_DEAL:
                return await handle.deal_reward(update, deal)

    elif update.new_chat_members:
        return await handle.join(update, deal)

    elif update.left_chat_member is not None:
        return await handle.left(update, deal)

    deal.unlock()


async def dispatch_callback(update: CallbackQuery) -> Any:
    deal = db.LockedDeal.find_where(chat=update.message.chat.id, _quantity=1)
    if deal is None:
        return

    if update.data is not None:
        args = sed.decode(update.data)
        action = args.get(sed.kv.ACT)
        if deal.in_chat.creator and deal.in_chat.contributor:
            if action == sed.kv.ACT_CLOSE_DEAL:
                return await handle.confirm_deal_close(update, deal, args)

    deal.unlock()


async def dispatcher(request: web.Request) -> Any:
    update = Update(**await request.json())
    if update.message is not None:
        return await dispatch_msg(update.message)

    if update.callback_query is not None:
        return await dispatch_callback(update.callback_query)
