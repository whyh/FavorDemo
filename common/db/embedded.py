from typing import Optional

from aiogram.types import InlineKeyboardMarkup

from .orm import *
from common import emoji as emj, telegram as tg
from common.bots import CustomBot, bot

__all__ = ("MessageField", "ConvField", "UserField", "PostContentField")


class MessageField(EmbeddedBaseField):
    async def clean(self, bot: CustomBot, chat: int) -> None:
        await bot.d_msg(chat, self.id)
        self.id = None

    id = IntegerField()
    text = StringField()


class UserField(EmbeddedBaseField):
    id = IntegerField()
    lang = StringField()
    name = StringField()
    url = StringField()


class ConvField(EmbeddedBaseField):
    async def clean(self, bot: CustomBot, chat: int):
        for message in self.messages:
            await bot.d_msg(chat, message)

    name = StringField()
    step = StringField()
    messages = ListField(IntegerField)

    data = StringField()


class PostContentField(EmbeddedBaseField):
    class AttachmentField(EmbeddedBaseField):
        class FileField(EmbeddedBaseField):
            async def store_media(self, kb: Optional[InlineKeyboardMarkup] = None) -> None:
                if self.media is None:
                    message = await bot.e_media_msg(tg.MEDIA_ID, self.media, self.id, kb)
                    self.media = message
                else:
                    await bot.s_media_msg(tg.MEDIA_ID, self.id, self.type, kb)

            @property
            def emoji(self):
                if self.type == tg.TYPE_AUDIO:
                    return emj.MICROPHONE
                elif self.type == tg.TYPE_DOCUMENT:
                    return emj.BOOKMARKS
                elif self.type == tg.TYPE_PHOTO:
                    return emj.NATIONAL_PARK
                elif self.type == tg.TYPE_VIDEO:
                    return emj.TAPE

            id = StringField()
            type = IntegerField()
            message = IntegerField()
            media = IntegerField()

        async def clean(self, chat: int) -> None:
            for file in self.files:
                await bot.d_msg(chat, file.message)

        files = ListField(FileField)
        quantity = IntegerField(default=0)

    async def clean(self, chat: int) -> None:
        await self.title.clean(bot, chat)
        await self.body.clean(bot, chat)
        await self.reward.clean(bot, chat)
        await self.attachment.clean(chat)

    title = MessageField(default=MessageField)
    body = MessageField(default=MessageField)
    reward = MessageField(default=MessageField)
    attachment = AttachmentField(default=AttachmentField)
