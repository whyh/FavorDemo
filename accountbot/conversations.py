import functools

from common import db
from common.bots import bot

(CREATE_POST,
 WITHDRAW,
 REPLENISH
 ) = (str(i) for i in range(3))

(STEP_AMOUNT,
 STEP_CARD,
 STEP_REWARD,
 STEP_TITLE,
 STEP_BODY,
 STEP_ATTACHMENT
 ) = (str(i) for i in range(6))


def entry(name: str):
    def wrap_wrap(function):
        @functools.wraps(function)
        async def wrap(user: db.LockedUser, *args, **kwargs):
            if user.conv.name == CREATE_POST:
                await user.post_content.clean(user.id)

            tmp_conv = user.conv
            user.conv = None
            user.conv.name = name

            result = await function(user, *args, **kwargs)

            await tmp_conv.clean(bot, user.id)
            return result

        return wrap

    return wrap_wrap
