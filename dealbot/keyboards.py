from aiogram.types import InlineKeyboardMarkup

import buttons as btn


def close_deal(lang: str, creator: bool, contributor: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[btn.close_deal(lang, creator, contributor)]])


def replenish(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[btn.replenish(lang)]])
