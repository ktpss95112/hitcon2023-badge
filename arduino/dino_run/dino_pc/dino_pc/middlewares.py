import asyncio
from collections.abc import Callable, Awaitable
from pathlib import Path

import aiohttp
import aiohttp.client_exceptions
from aiohttp import web


def static_middleware(prefix: str, docpath: str | Path):
    @web.middleware
    async def inner_static_middleware(
        request: web.Request,
        handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
    ) -> web.StreamResponse:
        if request.method != "GET":
            return await handler(request)
        if request.url.path.startswith(prefix):
            rel_fs_path = request.url.path[len(prefix) :]
            if Path(docpath, rel_fs_path).is_file():
                return web.FileResponse(Path(docpath, rel_fs_path))
            if Path(docpath, rel_fs_path, "index.html").is_file():
                return web.FileResponse(Path(docpath, rel_fs_path, "index.html"))
        return await handler(request)

    return inner_static_middleware


@web.middleware
async def passthrough(
    request: web.Request,
    handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
) -> web.StreamResponse:
    return await handler(request)


def proxy(path: str, target: str, rewrite=lambda path: path):
    if target is None:
        print("proxy target not set")

    session = aiohttp.ClientSession()

    def reg_cleanup():
        loop = asyncio.get_running_loop()
        _close = loop.close

        def cleanup():
            session.close()
            _close()

        loop.close = cleanup

    reg_cleanup()

    @web.middleware
    async def inner_proxy_middleware(
        request: web.Request,
        handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
    ) -> web.StreamResponse:
        if not request.url.path.startswith(path):
            return await handler(request)
        if target is None:
            print("proxy target not set")
            return web.Response(status=500)

        req_headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
        req_path = rewrite(request.url.path_qs)
        try:
            async with session.request(
                request.method,
                f"{target}{req_path}",
                data=await request.read(),
                headers=req_headers,
            ) as resp:
                res_headers = {
                    k: v for k, v in resp.headers.items() if k.lower() != "server"
                }
                return web.Response(
                    status=resp.status, headers=res_headers, body=await resp.read()
                )
        except aiohttp.client_exceptions.ClientConnectorError:
            return web.Response(status=500)

    return inner_proxy_middleware
