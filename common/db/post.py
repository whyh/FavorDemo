from .orm import *
from .embedded import *
from common import phrases as phr, emoji as emj, keyboards as kb, telegram as tg
from common.bots import pub_bot, bot

__all__ = ("Post", "LockedPost")


class Post(Kind):
    @property
    def text(self) -> str:
        def state() -> str:
            if self.solved:
                return phr.SOLVED()
            if self.deal is None:
                return phr.ACTIVE() if self.publication is not None else phr.UNPUBLISHED()
            return phr.IN_DEAL()

        def reward() -> str:
            return "" if self.post_content.reward.text is None else f"\n\n{emj.MONEY_BAG} {self.post_content.reward.text}"

        def attachment() -> str:
            def text():
                return "".join([f"[    {file.emoji}    ]({tg.MEDIA_URL}/{file.media})"
                               for file in self.post_content.attachment.files])
            return "" if self.post_content.attachment.quantity == 0 else f"\n\n{emj.PAPERCLIPS}{text()}"

        return (f"{state()}\n\n"
                f"*{self.post_content.title.text}*\n"
                f"{self.post_content.body.text}"
                f"{reward()}"
                f"{attachment()}")

    async def send_preview(self) -> None:
        if self.deal is None:
            keyboard = (kb.publish_post if self.publication is None else kb.hide_post)(self.creator.lang, self.id)
        else:
            keyboard = None

        if self.preview is None:
            message = await bot.s_msg(self.creator.id, self.text, keyboard)
            self.preview = message
        else:
            await bot.e_msg(self.creator.id, self.preview, self.text, keyboard)

    async def send_publication(self) -> None:
        async def update_caption() -> None:
            for file in self.post_content.attachment.files:
                await file.store_media(kb.see_post(self.publication))

        keyboard = kb.contact(self.id) if self.deal is None else None

        if self.publication is None:
            self.publication = 1
            message = await pub_bot.s_msg(tg.BOARD_ID, self.text, keyboard)
            self.publication = message
        else:
            await pub_bot.e_msg(tg.BOARD_ID, self.publication, self.text, keyboard)

        await update_caption()
        await self.send_preview()

    async def send(self) -> None:
        await self.send_preview() if self.publication is None else await self.send_publication()

    creator = UserField()
    post_content = PostContentField(default=PostContentField)

    preview = IntegerField()
    publication = IntegerField()

    banned = ListField(IntegerField)
    deal = IntegerField()

    solved = BooleanField(default=False)


class LockedPost(Post):
    _kind = "post"
    _p_lock = True
