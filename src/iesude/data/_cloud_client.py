from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class FileInfo(Protocol):
    def is_dir(self) -> bool: ...

    def get_name(self) -> str: ...


class Client(Protocol):
    @abstractmethod
    def logout(self) -> None: ...

    @abstractmethod
    def file_info(self, remote_path: str) -> FileInfo: ...

    @abstractmethod
    def get_file(self, file_path: str, out_dir: Path | str) -> None: ...


class ClientFn(Protocol):
    def __call__(self, url: str) -> Client: ...
