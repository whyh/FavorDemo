from aiogram.types import InlineKeyboardMarkup

from . import sed, buttons as btn


def grade(lang: str, gp: int, deal: int, partner: int, creator: bool) -> InlineKeyboardMarkup:
    data = {sed.kv.CREATOR: creator, sed.kv.DEAL: deal, sed.kv.ACT: sed.kv.ACT_GRADE, sed.kv.USER: partner}
    return InlineKeyboardMarkup(inline_keyboard=[[btn.minus(gp, data), btn.plus(gp, data)],
                                                 [btn.send(lang, gp, data)]])


def contact(post: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[btn.contact(post)]])


def hide_post(lang: str, post: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[btn.hide_post(lang, post)]])


def publish_post(lang: str, post: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[btn.publish_post(lang, post)]])


def see_post(publication: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[btn.see_post(publication)]])
