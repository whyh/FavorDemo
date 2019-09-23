import functools

from common import db
from common.bots import deal_bot

START_DEAL = "start_deal"

CLOSE_DEAL = "close_deal"


def entry(name: str):
    def wrap_wrap(function):
        @functools.wraps(function)
        async def wrap(deal: db.LockedDeal, *args, **kwargs):
            tmp_conv = deal.conv
            deal.conv = None
            deal.conv.name = name

            result = await function(deal, *args, **kwargs)
            await tmp_conv.clean(deal_bot, deal.chat)
            return result

        return wrap

    return wrap_wrap
