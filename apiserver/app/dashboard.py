from datetime import datetime
from numbers import Number
from typing import TypedDict

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

    def response_checker(self, resp: requests.Response) -> bool:
        if resp.status_code >= 200 and resp.status_code < 300:
            return True
        print(f"Dashboard API failed, code={resp.status_code} msg=`{resp.text}`")
        return False

    def create_or_update_dino(self, card_uid: str, score: Number) -> bool:
        try:
            resp = requests.put(
                f"{self.base_url}/dino/{card_uid}",
                headers=self.headers,
                json={"score": score},
            )
            return self.response_checker(resp)
        except requests.exceptions.ConnectionError:
            print("ConnectionRefusedError to dashboard backend")
            return False

    def batch_create_or_update_dinos(self, dinos: list[DinoDict]) -> bool:
        return all(
            list(
                map(
                    lambda dino: self.create_or_update_dino(
                        dino["card_uid"], dino["score"]
                    ),
                    dinos,
                )
            )
        )

    def create_or_update_popcat(self, card_uid: str, score: Number) -> bool:
        try:
            resp = requests.put(
                f"{self.base_url}/popcat/{card_uid}",
                headers=self.headers,
                json={"score": score},
            )
            return self.response_checker(resp)
        except requests.exceptions.ConnectionError:
            print("ConnectionRefusedError to dashboard backend")
            return False

    def batch_create_or_update_popcats(self, popcats: list[PopcatDict]) -> bool:
        return all(
            list(
                map(
                    lambda cat: self.create_or_update_dino(
                        cat["card_uid"], cat["score"]
                    ),
                    popcats,
                )
            )
        )

    def create_emoji(self, card_uid: str, content: str, timestamp: datetime) -> bool:
        try:
            resp = requests.post(
                f"{self.base_url}/emoji/{card_uid}",
                headers=self.headers,
                json={
                    "content": content,
                    "timestamp": timestamp.astimezone().isoformat(),
                },
            )
            return self.response_checker(resp)
        except requests.exceptions.ConnectionError:
            print("ConnectionRefusedError to dashboard backend")
            return False

    def batch_create_emojis(self, emojis: list[EmojiDict]) -> bool:
        return all(
            list(
                map(
                    lambda emoji: self.create_emoji(
                        emoji["card_uid"], emoji["content"], emoji["timestamp"]
                    ),
                    emojis,
                )
            )
        )
