from typing import Union, Any, Optional

from aiogram.types import Update, Message, CallbackQuery
from aiohttp import web

from common import sed, db, tg
import conversations as conv
import commands as cmd
import handlers as handle


async def dispatch_deeplink(update: Message) -> Any:
    args = sed.decode(update.text[7:])
    action = args.get(sed.kv.ACT)

    if action == sed.kv.ACT_CONTACT:
        return await handle.create_request(update, args)

    elif action == sed.kv.ACT_REPL:
        return await handle.replenish(update)


async def dispatch_edit(update: Message) -> Any:
    async def check_text(owner: Union[db.User, db.Post]) -> bool:
        if (update.message_id == owner.post_content.title.id or
                update.message_id == owner.post_content.body.id or
                update.message_id == owner.post_content.reward.id):
            return True
        return False

    async def check_attachment(owner: Union[db.User, db.Post]) -> bool:
        for file in owner.post_content.attachment.files:
            if update.message_id == file.message:
                return True
        return False

    async def dispatch_text(owner: Union[db.LockedUser, db.LockedPost]) -> Any:
        if update.message_id == owner.post_content.title.id:
            return await handle.post_title(update, owner)

        elif update.message_id == owner.post_content.body.id:
            return await handle.post_body(update, owner)

        elif update.message_id == owner.post_content.reward.id:
            return await handle.post_reward(update, owner)

    async def dispatch_attachment(owner: Union[db.LockedUser, db.LockedPost]) -> Any:
        nbr = 0
        for file in owner.post_content.attachment.files:
            if update.message_id == file.message:
                if update.document is not None:
                    return await handle.post_attachment(update, owner, tg.TYPE_DOCUMENT, update.document.file_id, nbr)

                elif update.photo is not None:
                    return await handle.post_attachment(update, owner, tg.TYPE_PHOTO, update.photo[0].file_id, nbr)

                elif update.audio is not None:
                    return await handle.post_attachment(update, owner, tg.TYPE_AUDIO, update.audio.file_id, nbr)

                elif update.video is not None:
                    return await handle.post_attachment(update, owner, tg.TYPE_VIDEO, update.video.file_id, nbr)
            nbr += 1

    async def dispatch_post(dispatch, check) -> Any:
        async def dp(owner: Optional[Union[db.LockedUser, db.LockedPost]]) -> Any:
            if owner is None:
                return
            return await dispatch(owner)

        if check(user.post_content):
            await dp(db.LockedUser.find(update.from_user.id))

        for tmp_post in user.posts:
            post = db.Post.find(tmp_post)
            if post is None:
                continue
            if check(post.post_content):
                await dp(db.LockedPost.find(post.id))

    user = db.User.get(update.from_user)

    if update.text is not None:
        return await dispatch_post(dispatch_text, check_text)

    elif update.document is not None or update.video is not None or update.audio is not None or update.photo is not None:
        return await dispatch_post(dispatch_attachment, check_attachment)


async def dispatch_msg(update: Message) -> Any:
    if update.text is not None:
        if update.text == cmd.START or update.text == cmd.HELP:
            return await handle.help(update)

        if update.text[:6] == cmd.START:
            return await dispatch_deeplink(update)

        if update.text == cmd.CREATE_POST:
            return await handle.new_post(update)

        if update.text == cmd.CHANGE_LANGUAGE:
            return await handle.change_language(update)

        if update.text == cmd.REPLENISH:
            return await handle.replenish(update)

        if update.text == cmd.WITHDRAW:
            return await handle.withdraw(update)

        if update.text == cmd.STATS:
            return await handle.stats(update)

        if update.text == cmd.TOP:
            return await handle.top(update, False)

        if update.text[:1] == "/":
            return await handle.invalid_cmd(update)

        user = db.LockedUser.get_locked(update.from_user)

        if user.conv.name == conv.CREATE_POST:
            if user.conv.step == conv.STEP_TITLE:
                return await handle.post_title(update, user)

            elif user.conv.step == conv.STEP_BODY:
                return await handle.post_body(update, user)

            elif user.conv.step == conv.STEP_REWARD:
                return await handle.post_reward(update, user)

        elif user.conv.name == conv.WITHDRAW:
            if user.conv.step == conv.STEP_AMOUNT:
                return await handle.withdraw_amount(update, user)

            elif user.conv.step == conv.STEP_CARD:
                return await handle.withdraw_card(update, user)

        user.unlock()

    else:
        user = db.LockedUser.get_locked(update.from_user)

        if user.conv.name == conv.CREATE_POST:
            if user.conv.step == conv.STEP_ATTACHMENT:
                if update.document is not None:
                    return await handle.post_attachment(update, user, tg.TYPE_DOCUMENT, update.document.file_id)

                elif update.photo is not None:
                    return await handle.post_attachment(update, user, tg.TYPE_PHOTO, update.photo[0].file_id)

                elif update.audio is not None:
                    return await handle.post_attachment(update, user, tg.TYPE_AUDIO, update.audio.file_id)

                elif update.video is not None:
                    return await handle.post_attachment(update, user, tg.TYPE_VIDEO, update.video.file_id)

        user.unlock()


async def dispatch_callback(update: CallbackQuery) -> Any:
    if update.data is not None:
        args = sed.decode(update.data)
        action = args.get(sed.kv.ACT)

        if action == sed.kv.ACT_HIDE_POST:
            return await handle.hide_post(args)

        elif action == sed.kv.ACT_PUBLISH_POST:
            return await handle.publish_post(args)

        elif action == sed.kv.ACT_REPL:
            return await handle.replenish(update)

        elif action == sed.kv.ACT_TOP:
            return await handle.top(update, args.get(sed.kv.CREATOR, type=bool, default=False), args.get(sed.kv.DIR), args)

        elif action == sed.kv.ACT_TOP_CONTRIBUTOR:
            return await handle.top(update, False)

        elif action == sed.kv.ACT_TOP_CREATOR:
            return await handle.top(update, True)

        elif action == sed.kv.ACT_GRADE:
            return await handle.deal_grade(update, args)

        elif action == sed.kv.ACT_BAN:
            return await handle.ban_request(update, args)

        elif action == sed.kv.ACT_ACCEPT:
            return await handle.accept_request(update, args)

        elif action == sed.kv.ACT_DECLINE:
            return await handle.decline_request(update, args)

        elif action == sed.kv.ACT_CREATE_POST:
            return await handle.create_post(update)

        elif action == sed.kv.ACT_CANCEL_LANG:
            return await handle.language_cancel(update)

        elif action == sed.kv.ACT_CHANGE_LANG:
            return await handle.language(update, args)

        elif action == sed.kv.ACT_REPL_CARD:
            return await handle.replenish_card(update, args)


async def dispatcher(request: web.Request) -> Any:
    update = Update(**await request.json())
    if update.message is not None:
        return await dispatch_msg(update.message)

    if update.edited_message is not None:
        return await dispatch_edit(update.edited_message)

    if update.callback_query is not None:
        return await dispatch_callback(update.callback_query)
