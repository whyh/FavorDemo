from typing import List

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

from common import sed, fin
from common.glossary import SUPPORTED_LANGS
import limits as limit
import phrases as phr
import buttons as btn

CARD_NUMBERS = {phr.PRIVAT24: fin.PB_MERCH_CARD,
                phr.OTHER_BANK: fin.PB_MERCH_CARD}


def withdraw_all(balance: float) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[btn.withdraw_all(balance)]], resize_keyboard=True, one_time_keyboard=True)


def replenish(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[btn.replenish(lang)]])


def withdraw_cards(card_numbers: List[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[btn.withdraw_card(card_number)] for card_number in card_numbers], resize_keyboard=True, one_time_keyboard=True)


def language(user_lang: str) -> InlineKeyboardMarkup:
    keyboard = []
    column = 0

    for lang in SUPPORTED_LANGS:
        if lang != user_lang:
            keyboard.append([btn.language(lang), ]) if column == 0 else keyboard[-1].append(btn.language(lang))
            if limit.LANG_PER_ROW - column == 1:
                column = -1
            else:
                column += 1

    keyboard.append([btn.cancel_language(user_lang), ]) if column == -1 else keyboard[-1].append(btn.cancel_language(user_lang))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def replenish_method(lang: str) -> InlineKeyboardMarkup:
    data = {sed.kv.ACT: sed.kv.ACT_REPL_CARD}
    keyboard = []
    column = 0

    for method, card_number in CARD_NUMBERS.items():
        tmp_button = btn.replenish_method(method(lang), card_number, data)
        keyboard.append([tmp_button, ]) if column == 0 else keyboard[-1].append(tmp_button)
        if limit.METHODS_PER_ROW - column == 1:
            column = -1
        else:
            column += 1
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def top(lang: str, creator: bool, index: int, user_index: int, max_index: int) -> InlineKeyboardMarkup:
    keyboard = [[], []]
    data = {sed.kv.ACT: sed.kv.ACT_TOP, sed.kv.CREATOR: creator}

    if index > 5:
        keyboard[0].append(btn.top_next(index, data))
    if index > 11:
        keyboard[0].append(btn.top_best(data))
    if index - 6 > user_index > index + 6:
        keyboard[0].append(btn.top_me(lang, data))
    if index < max_index - 5:
        keyboard[0].append(btn.top_prev(index, data))

    keyboard[1].append(btn.top_contributor(lang) if creator else btn.top_creator(lang))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def request_options(lang: str, deal: int) -> InlineKeyboardMarkup:
    data = {sed.kv.DEAL: deal}
    return InlineKeyboardMarkup(inline_keyboard=[[btn.request_accept(lang, data), btn.request_decline(lang, data)],
                                                 [btn.request_ban(lang, data)]])


def join_chat(lang: str, invite_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[btn.join_chat(lang, invite_url)]])


def negotiable(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[btn.negotiable(lang)]], resize_keyboard=True, one_time_keyboard=True)


def create_post(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[btn.create_post(lang)]])
