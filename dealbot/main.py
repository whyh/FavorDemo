import asyncio

from aiohttp import web

from common import tg
from dispatchers import dispatcher

handle = web.RouteTableDef()


@handle.post(f"/{tg.DEAL_BOT_TOKEN}")
async def web_hook(request: web.Request):
    asyncio.create_task(dispatcher(request))
    return web.Response(text="ok")


@handle.get("/_ah/warmup")
async def warm_up(_):
    return web.Response(text="ok")


app = web.Application()
app.router.add_routes(handle)
