import asyncio
from typing import Optional, Union, Any, Callable

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode, InputMedia, ReplyKeyboardRemove
from aiogram.utils import exceptions as exc

from . import telegram as tg

ReplyMarkup = Optional[Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]]
NOKB = ReplyKeyboardRemove()


class CustomBot(Bot):
    def secured(function: Callable):
        async def wrap(self, *args, **kwargs) -> Any:
            try:
                return await function(self, *args, **kwargs)
            except exc.RetryAfter as err:
                await asyncio.sleep(err.timeout)
                return await wrap(self, *args, **kwargs)
            except exc.RestartingTelegram:
                await asyncio.sleep(5)
                return await wrap(self, *args, **kwargs)
            except (exc.BadRequest, exc.ConflictError, exc.Unauthorized, exc.NetworkError, exc.MigrateToChat):
                return

        return wrap

    @secured
    async def d_msg(self, chat: int, message: int) -> None:
        if message is not None:
            await self.delete_message(chat, message)

    @secured
    async def e_msg(self, chat: int, msg: int, text: Optional[str] = None, kb: ReplyMarkup = None, markdown: bool = True, preview: bool = True) -> bool:
        if text is not None:
            await self.edit_message_text(text, chat, msg, parse_mode=ParseMode.MARKDOWN if markdown else None, disable_web_page_preview=not preview, reply_markup=kb)
        elif kb is not None:
            await self.edit_message_reply_markup(chat, msg, reply_markup=kb)
        else:
            return False
        return True

    @secured
    async def s_msg(self, chat: int, text: str, kb: ReplyMarkup = NOKB, reply: Optional[int] = None, markdown: bool = True, preview: bool = True, notify: bool = True) -> Optional[int]:
        message = await self.send_message(chat, text, parse_mode=ParseMode.MARKDOWN if markdown else None, disable_web_page_preview=not preview, disable_notification=not notify, reply_to_message_id=reply, reply_markup=kb)
        return message.message_id

    @secured
    async def e_media_msg(self, chat: int, message: int, file: str, kb: ReplyMarkup) -> bool:
        await self.edit_message_media(InputMedia(media=file), chat, message, reply_markup=kb)
        return True

    @secured
    async def s_media_msg(self, chat: int, file: str, type: int, kb: ReplyMarkup) -> Optional[int]:
        if type == tg.TYPE_DOCUMENT:
            send_file = self.send_document
        elif type == tg.TYPE_PHOTO:
            send_file = self.send_photo
        elif type == tg.TYPE_AUDIO:
            send_file = self.send_audio
        elif type == tg.TYPE_VIDEO:
            send_file = self.send_video
        try:
            message = await send_file(chat, file, reply_markup=kb)
        except NameError:
            return
        else:
            return message.message_id

    @secured
    async def export_invite(self, chat: int) -> Optional[str]:
        invite = await self.export_chat_invite_link(chat)
        return invite

    @secured
    async def kick(self, chat: int, user: int) -> bool:
        await self.kick_chat_member(chat, user)
        return True

    @secured
    async def chat_title(self, chat: int, title: str) -> bool:
        await self.set_chat_title(chat, title)
        return True


bot = CustomBot(tg.BOT_TOKEN)
deal_bot = CustomBot(tg.DEAL_BOT_TOKEN)
pub_bot = CustomBot(tg.PUB_BOT_TOKEN)
