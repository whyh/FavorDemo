from aiogram.types import InlineKeyboardButton

from common import sed, tg
import phrases as phr


def replenish(lang: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.REPLENISH(lang), url=tg.BOT_DEEPLINK + sed.encode(**{sed.kv.ACT: sed.kv.ACT_REPL}))


def close_deal(lang: str, creator: bool, contributor: bool) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.CONFIRM(lang), callback_data=sed.encode(**{sed.kv.ACT: sed.kv.ACT_CLOSE_DEAL, sed.kv.CONTRIBUTOR: contributor, sed.kv.CREATOR: creator}))
