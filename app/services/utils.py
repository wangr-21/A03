import asyncio
import base64
import functools
import os
from collections.abc import Awaitable, Callable, Iterable
from typing import Self

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionContentPartParam,
    ChatCompletionUserMessageParam,
)

from . import fleep as fleep


def get_openai_client():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_base_url = os.getenv("OPENAI_BASE_URL")
    openai_model_name = os.getenv("OPENAI_MODEL_NAME") or "gpt-3.5-turbo"

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY 环境变量未设置")

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_base_url,
    )
    return client, openai_model_name


class CompletionMessage:
    content: list[ChatCompletionContentPartParam]

    def __init__(self) -> None:
        self.content = []

    def text(self, text: str) -> Self:
        self.content.append({"type": "text", "text": text})
        return self

    def image(self, image_url: str | bytes) -> Self:
        if isinstance(image_url, bytes):
            info = fleep.get(image_url)
            if not info or not info.mime:
                raise ValueError("无效的图片数据")

            encoded = base64.b64encode(image_url).decode("utf-8")
            image_url = f"data:{info.mime[0]};base64,{encoded}"

        self.content.append(
            {"type": "image_url", "image_url": {"url": image_url, "detail": "auto"}}
        )
        return self

    def images(self, image_urls: Iterable[str]) -> Self:
        for url in image_urls:
            self.image(url)
        return self

    def build(self) -> ChatCompletionUserMessageParam:
        return {"role": "user", "content": self.content}


def run_sync[**P, R](call: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    """一个用于包装 sync function 为 async function 的装饰器

    参数:
        call: 被装饰的同步函数
    """

    @functools.wraps(call)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return await asyncio.to_thread(call, *args, **kwargs)

    return wrapper
