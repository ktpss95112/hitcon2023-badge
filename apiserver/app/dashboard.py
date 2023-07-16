from datetime import datetime
from functools import wraps
from numbers import Number
from typing import Callable, ParamSpec, TypedDict

import requests


class DinoDict(TypedDict):
    card_uid: str
    score: str


class PopcatDict(TypedDict):
    card_uid: str
    score: str


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
            if resp.status_code >= 200 and resp.status_code < 300:
                return True
            print(f"Dashboard API failed, code={resp.status_code} msg=`{resp.text}`")
            return False
        except requests.exceptions.ConnectionError:
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

    @error_handler
    def create_or_update_dino(self, card_uid: str, score: Number):
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
    def create_or_update_popcat(self, card_uid: str, score: Number) -> bool:
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
    def create_emoji(self, card_uid: str, content: str, timestamp: datetime) -> bool:
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
