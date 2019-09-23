import asyncio

from aiohttp import web

from common import tg
from dispatchers import dispatcher

handle = web.RouteTableDef()


@handle.post(f"/{tg.BOT_TOKEN}")
async def webhook(request: web.Request):
    asyncio.create_task(dispatcher(request))
    return web.Response(text="ok")


@handle.get("/_ah/warmup")
async def warmup(_):
    return web.Response(text="ok")


app = web.Application()
app.router.add_routes(handle)
