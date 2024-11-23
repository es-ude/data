import contextlib
from pathlib import Path

import tempfile
from typing import Protocol

from ._oc_cloud_client import create_sciebo_client_from_public_url
from .extractable import ExtractableFn
from ._cloud_client import ClientFn, Client, FileInfo


class DataSetP(Protocol):
    @property
    def file_path(self) -> str: ...

    @property
    def file_type(self) -> ExtractableFn: ...


@contextlib.contextmanager
def tmp_file_path_for_archive(archive_name):
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir) / archive_name


class DownloaderNotInitializedException(Exception):
    def __init__(self):
        super().__init__("Downloader not initialized, use `with Downloader(...) as d: ...`")


class _ExplodingClient(Client):
    def logout(self) -> None:
        raise DownloaderNotInitializedException()

    def file_info(self, remote_path: str) -> FileInfo:
        raise DownloaderNotInitializedException()

    def get_file(self, file_path: str, out_dir: Path | str) -> None:
        raise DownloaderNotInitializedException()

class UnspecifiedDataSetTypeException(Exception):
    def __init__(self):
        super().__init__("Unspecified dataset type")


class _ExplodingDataSet:
    @property
    def file_path(self) -> str:
        raise UnspecifiedDataSetTypeException()

    @property
    def file_type(self) -> ExtractableFn:
        raise UnspecifiedDataSetTypeException()



class Downloader:
    def __init__(self, client_fn: ClientFn) -> None:
        self._client_fn: ClientFn = client_fn
        self._client: Client = _ExplodingClient()
        self._remote: DataSetP = _ExplodingDataSet()
        self._out_dir: Path  = Path("data")

    def __enter__(self):
        self.client = self._client_fn(
            "https://uni-duisburg-essen.sciebo.de/s/pWPghcaiYFhz6BW",
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.logout()

    def download(self, remote: DataSetP, output: str):
        self._remote = remote
        self._out_dir = Path(output)
        self._check_for_problems()
        with self._tmp_out_dir() as tmp_out:
            self._do_download(tmp_out)
            self._do_extract_from(tmp_out)

    def _remote_is_dir(self):
        return self._client.file_info(self._remote.file_path).is_dir()

    def _check_for_problems(self):
        if self.client is None:
            raise Exception("you have to create a connection first")
        if self._remote is None:
            raise ValueError()
        if self._remote_is_dir():
            raise NotImplementedError

    @contextlib.contextmanager
    def _tmp_out_dir(self):
        with tmp_file_path_for_archive(self._remote.file_path) as tmp_dir:
            yield tmp_dir

    def _do_download(self, out_dir: Path):
        self._client.get_file(self._remote.file_path, out_dir)

    def _do_extract_from(self, directory: Path):
        self.mk_permanent_out_dir()
        archive_path = directory / self._remote.file_path
        archive = self._remote.file_type(archive_path)
        archive.download(out_dir=self._out_dir)

    def mk_permanent_out_dir(self):
        self._out_dir.mkdir(parents=True, exist_ok=True)


def download_if_missing(archive_name: str, output_directory: str | Path):
    output_directory = Path(output_directory)
    if output_directory.exists():
        return
    with Downloader(create_sciebo_client_from_public_url) as d:
        d.download(archive_name, output_directory)
