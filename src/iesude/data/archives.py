from pathlib import Path
import shutil
from .extractable import Extractable
from collections.abc import Iterable
from tarfile import TarFile
from zipfile import ZipFile
from typing import Any


class PlainFile(Extractable):
    def __init__(self, file: Path):
        self._file = file

    def extract(self, output_directory: Path) -> None:
        shutil.copy(self._file, output_directory.with_name(self._file.name))


class Tar(Extractable):
    def __init__(self, file: str | Path):
        self._file = TarFile(file)

    def _get_members(self) -> Iterable[Any]:
        yield from self._file.getmembers()

    def _extract(self, member, output_directory: Path) -> None:
        self._file.extract(member, output_directory)

    def extract(self, output_directory: Path):
        for m in self._get_members():
            self._extract(m, output_directory)


class Zip(Extractable):
    def __init__(self, file: str | Path):
        self._f = ZipFile(file)

    def _get_members(self):
        yield from self._f.infolist()

    def _check_zip_file_integrity(self):
        first_bad_file = self._f.testzip()
        if first_bad_file is not None:
            raise IOError

    def extract(self, output_directory: Path) -> None:
        self._check_zip_file_integrity()
        for m in self._get_members():
            self._f.extract(m, output_directory)
