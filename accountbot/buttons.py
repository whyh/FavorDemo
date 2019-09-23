from typing import Dict, Any

from aiogram.types import InlineKeyboardButton, KeyboardButton

from common import sed, emj
import phrases as phr


def top_next(index: int, data: Dict[str, Any]) -> InlineKeyboardButton:
    return InlineKeyboardButton(emj.PLUS, callback_data=sed.encode(**data, **{sed.kv.DIR: sed.kv.DIR_NEXT, sed.kv.INDEX: index}))


def top_prev(index: int, data: Dict[str, Any]) -> InlineKeyboardButton:
    return InlineKeyboardButton(emj.MINUS, callback_data=sed.encode(**data, **{sed.kv.DIR: sed.kv.DIR_PREV, sed.kv.INDEX: index}))


def top_me(lang: str, data: Dict[str, Any]) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.ME(lang), callback_data=sed.encode(**data, **{sed.kv.DIR: sed.kv.DIR_ME}))


def top_best(data: Dict[str, Any]) -> InlineKeyboardButton:
    return InlineKeyboardButton(emj.TOP_DIRECTION, callback_data=sed.encode(**data, **{sed.kv.DIR: sed.kv.DIR_BEST}))


def top_contributor(lang: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.TOP_CONTRIBUTOR(lang), callback_data=sed.encode(**{sed.kv.ACT: sed.kv.ACT_TOP_CONTRIBUTOR}))


def top_creator(lang: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.TOP_CREATOR(lang), callback_data=sed.encode(**{sed.kv.ACT: sed.kv.ACT_TOP_CREATOR}))


def language(lang: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.LANGUAGE(lang), callback_data=sed.encode(**{sed.kv.ACT: sed.kv.ACT_CHANGE_LANG, sed.kv.LANG: lang}))


def cancel_language(lang: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.CANCEL(lang), callback_data=sed.encode(**{sed.kv.ACT: sed.kv.ACT_CANCEL_LANG}))


def replenish(lang: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.REPLENISH(lang), callback_data=sed.encode(**{sed.kv.ACT: sed.kv.ACT_REPL}))


def withdraw_card(card_number: str) -> KeyboardButton:
    return KeyboardButton(card_number)


def withdraw_all(balance: float) -> KeyboardButton:
    return KeyboardButton("{:.2f}".format(balance))


def replenish_method(method: str, card_number: str, data: Dict[str, Any]) -> InlineKeyboardButton:
    return InlineKeyboardButton(method, callback_data=sed.encode(**data, **{sed.kv.CARD: card_number}))


def request_accept(lang: str, data: Dict[str, Any]) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.REQUEST_ACCEPT(lang), callback_data=sed.encode(**data, **{sed.kv.ACT: sed.kv.ACT_ACCEPT}))


def request_decline(lang: str, data: Dict[str, Any]) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.REQUEST_DECLINE(lang), callback_data=sed.encode(**data, **{sed.kv.ACT: sed.kv.ACT_DECLINE}))


def request_ban(lang: str, data: Dict[str, Any]) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.REQUEST_BAN(lang), callback_data=sed.encode(**data, **{sed.kv.ACT: sed.kv.ACT_BAN}))


def negotiable(lang: str) -> KeyboardButton:
    return KeyboardButton(phr.NEGOTIABLE(lang))


def create_post(lang: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.POST_CREATE(lang), callback_data=sed.encode(**{sed.kv.ACT: sed.kv.ACT_CREATE_POST}))


def join_chat(lang: str, invite_url: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.JOIN_CHAT(lang), url=invite_url)
