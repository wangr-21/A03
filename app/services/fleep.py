from typing import Protocol


class FleepInfo(Protocol):
    type: list[str]
    extension: list[str]
    mime: list[str]

    def type_matches(self, type_: str) -> bool: ...
    def extension_matches(self, extension: str) -> bool: ...
    def mime_matches(self, mime: str) -> bool: ...


def get(data: bytes) -> FleepInfo:
    """获取文件类型信息"""
    import fleep

    return fleep.get(data[:256])  # pyright:ignore[reportReturnType]
