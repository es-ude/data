from typing import Protocol, TypeAlias, TypeVar
from abc import abstractmethod
from pathlib import Path
from collections.abc import Callable


class Extractable(Protocol):
    @abstractmethod
    def extract(self, output_directory: Path) -> None: ...


ExtractableT = TypeVar("ExtractableT", bound=Extractable)
ExtractableFn: TypeAlias = Callable[[str | Path], ExtractableT]
