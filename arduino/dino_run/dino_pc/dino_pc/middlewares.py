from collections.abc import Callable, Awaitable
from pathlib import Path

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
