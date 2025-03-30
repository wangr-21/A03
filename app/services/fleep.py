from collections.abc import Sequence
from typing import Protocol


class FleepInfo(Protocol):
    type: Sequence[str]
    extension: Sequence[str]
    mime: Sequence[str]

    def type_matches(self, type: str, /) -> bool: ...  # noqa: A002
    def extension_matches(self, extension: str, /) -> bool: ...
    def mime_matches(self, mime: str, /) -> bool: ...


def get(data: bytes) -> FleepInfo:
    """获取文件类型信息"""
    import fleep

    return fleep.get(data[:256])  # pyright:ignore[reportReturnType]
