from typing import Any, Awaitable, Callable

from aiohttp import web

from util.errors import BotError
from util.logging import log

routes = web.RouteTableDef()


class API:
    def __init__(self, path: str) -> None:
        self.path = path

    def __call__(self, func: Callable[[], Awaitable[Any]]):

        @routes.get("/api" + self.path)
        async def route(request: web.Request):
            res = "ok\n"
            try:
                res += str(await func(**request.rel_url.query))
            except BotError as e:
                log("Error processing request " + request.rel_url.path)
                return web.Response(text=str(e), status=500)

            return web.Response(text=res)


async def start_server():
    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    log("Server started")
