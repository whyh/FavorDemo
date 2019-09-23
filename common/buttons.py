from typing import Dict, Any

from aiogram.types import InlineKeyboardButton

from . import emoji as emj, sed, telegram as tg, phrases as phr


def send(lang: str, grade: int, data: Dict[str, Any]) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.SEND(lang), callback_data=sed.encode(**data, **{sed.kv.SEND: True, sed.kv.GRADE: grade}))


def plus(grade: int, data: Dict[str, Any]) -> InlineKeyboardButton:
    return InlineKeyboardButton(f"{emj.STAR}", callback_data=sed.encode(**data, **{sed.kv.GRADE: grade + 1}))


def minus(grade: int, data: Dict[str, Any]) -> InlineKeyboardButton:
    return InlineKeyboardButton(f"{emj.WEB}", callback_data=sed.encode(**data, **{sed.kv.GRADE: grade - 1}))


def publish_post(lang: str, post: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.PUBLISH(lang), callback_data=sed.encode(**{sed.kv.ACT: sed.kv.ACT_PUBLISH_POST, sed.kv.POST: post}))


def hide_post(lang: str, post: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.HIDE(lang), callback_data=sed.encode(**{sed.kv.ACT: sed.kv.ACT_HIDE_POST, sed.kv.POST: post}))


def contact(post: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.CONTACT(), url=tg.BOT_DEEPLINK + sed.encode(**{sed.kv.ACT: sed.kv.ACT_CONTACT, sed.kv.POST: post}))


def see_post(publication: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(phr.SEE_POST(), url=f"{tg.BOARD_URL}/{publication}")
