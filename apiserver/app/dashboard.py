import asyncio
from datetime import datetime
from functools import wraps
from numbers import Number
from typing import Awaitable, Callable, ParamSpec, TypedDict

import aiohttp
import aiohttp.client_exceptions

# TODO: use aiohttp or other async HTTP libraries
import requests

from .config import config


class DinoDict(TypedDict):
    card_uid: str
    score: str
    timestamp: datetime


class PopcatDict(TypedDict):
    card_uid: str
    score: str
    timestamp: datetime


class EmojiDict(TypedDict):
    card_uid: str
    content: str
    timestamp: datetime


P = ParamSpec("P")


def error_handler(func: Callable[P, requests.Response]) -> Callable[P, bool]:
    @wraps(func)
    def inner(*args, **kwargs) -> bool:
        try:
            resp = func(*args, **kwargs)
            if 200 <= resp.status_code < 300:
                return True
            print(f"Dashboard API failed, code={resp.status_code} msg=`{resp.text}`")
            return False
        except requests.exceptions.ConnectionError:
            print("ConnectionRefusedError to dashboard backend")
            return False

    return inner


def a_error_handler(
    func: Callable[P, Awaitable[aiohttp.ClientResponse]]
) -> Callable[P, Awaitable[bool]]:
    @wraps(func)
    async def inner(*args, **kwargs) -> bool:
        try:
            resp = await func(*args, **kwargs)
            if 200 <= resp.status < 300:
                return True
            print(f"Dashboard API failed, code={resp.status} msg=`{await resp.text()}`")
            return False
        except aiohttp.client_exceptions.ClientConnectorError:
            print("ConnectionRefusedError to dashboard backend")
            return False

    return inner


class Dashboard:
    def __init__(self, origin: str, api_key: str) -> None:
        """Get an interface to dashboard backend API.

        The provided methods return True if all the outgoing requests succeed,
        return False otherwise

        Args:
            origin: base URL to dashboard backend. For example:
                'http://dev.hitcon2023.online:8001'
            api_key: The API key required to push data to backend API.
        """
        self.base_url = f"{origin}/api/v1/badge"
        self.headers = {"X-API-KEY": api_key}
        self.session = aiohttp.ClientSession(headers=self.headers)

        self.disabled = origin == ""

    @error_handler
    def create_or_update_dino(self, card_uid: str, score: Number) -> requests.Response:
        return requests.put(
            f"{self.base_url}/dino/{card_uid}",
            headers=self.headers,
            json={"score": score},
        )

    def batch_create_or_update_dinos(self, dinos: list[DinoDict]) -> bool:
        return all(
            [
                self.create_or_update_dino(dino["card_uid"], dino["score"])
                for dino in dinos
            ]
        )

    @error_handler
    def create_or_update_popcat(
        self, card_uid: str, score: Number
    ) -> requests.Response:
        return requests.put(
            f"{self.base_url}/popcat/{card_uid}",
            headers=self.headers,
            json={"score": score},
        )

    def batch_create_or_update_popcats(self, popcats: list[PopcatDict]) -> bool:
        return all(
            [
                self.create_or_update_popcat(cat["card_uid"], cat["score"])
                for cat in popcats
            ]
        )

    @error_handler
    def create_emoji(
        self, card_uid: str, content: str, timestamp: datetime
    ) -> requests.Response:
        return requests.post(
            f"{self.base_url}/emoji/{card_uid}",
            headers=self.headers,
            json={
                "content": content,
                "timestamp": timestamp.astimezone().isoformat(),
            },
        )

    def batch_create_emojis(self, emojis: list[EmojiDict]) -> bool:
        return all(
            [
                self.create_emoji(
                    emoji["card_uid"], emoji["content"], emoji["timestamp"]
                )
                for emoji in emojis
            ]
        )

    @a_error_handler
    async def create_dino_record(
        self, card_uid: str, score: Number, timestamp: datetime
    ):
        return await self.session.post(
            f"{self.base_url}/dino/{card_uid}",
            json={"score": score, "timestamp": timestamp.astimezone().isoformat()},
        )

    @a_error_handler
    async def replace_all_dinos(self, dinos: list[DinoDict]):
        """Replace with new dino records

        Either old records are deleted and all new records create successfully,
        or nothing is applied.
        """
        return await self.session.put(
            f"{self.base_url}/dino/all",
            json=[
                {
                    "card_uid": dino["card_uid"],
                    "score": dino["score"],
                    "timestamp": dino["timestamp"].astimezone().isoformat(),
                }
                for dino in dinos
            ],
        )

    @a_error_handler
    async def create_popcat_record(
        self, card_uid: str, score: Number, timestamp: datetime
    ):
        return await self.session.post(
            f"{self.base_url}/popcat/{card_uid}",
            json={"score": score, "timestamp": timestamp.astimezone().isoformat()},
        )

    @a_error_handler
    async def replace_all_popcats(self, popcats: list[PopcatDict]):
        """Replace with new popcat records

        Either old records are deleted and all new records create successfully,
        or nothing is applied.
        """
        return await self.session.put(
            f"{self.base_url}/popcat/all",
            json=[
                {
                    "card_uid": popcat["card_uid"],
                    "score": popcat["score"],
                    "timestamp": popcat["timestamp"].astimezone().isoformat(),
                }
                for popcat in popcats
            ],
        )

    @a_error_handler
    async def a_create_emoji(self, card_uid: str, content: str, timestamp: datetime):
        return await self.session.post(
            f"{self.base_url}/emoji/{card_uid}",
            json={
                "content": content,
                "timestamp": timestamp.astimezone().isoformat(),
            },
        )

    @a_error_handler
    async def replace_all_emojis(self, emojis: list[EmojiDict]):
        return await self.session.put(
            f"{self.base_url}/emoji/all",
            json=[
                {
                    "card_uid": emoji["card_uid"],
                    "content": emoji["content"],
                    "timestamp": emoji["timestamp"].astimezone().isoformat(),
                }
                for emoji in emojis
            ],
        )


dashboard = Dashboard(config.DASHBOARD_ORIGIN, config.DASHBOARD_APIKEY)

# loop is created when aiohttp.ClientSession in __init__ is called
_loop = asyncio.get_event_loop()
_close = _loop.close


def _patch_close():
    _loop.run_until_complete(dashboard.session.close())
    _close()


_loop.close = _patch_close
