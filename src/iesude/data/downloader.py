import contextlib
from pathlib import Path

import owncloud as oc
import tempfile
from typing import Protocol
from .extractable import ExtractableFn


class DataSetP(Protocol):
    file_path: str
    file_type: ExtractableFn


@contextlib.contextmanager
def create_tmp_file_path_for_archive(archive_name):
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir) / archive_name


class Downloader:
    def __init__(self) -> None:
        self.client: None | oc.Client = None

    def __enter__(self):
        self.client = oc.Client.from_public_link(
            "https://uni-duisburg-essen.sciebo.de/s/pWPghcaiYFhz6BW",
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.logout()

    def download(self, remote: DataSetP, output: str):
        assert self.client is not None
        if self.client.file_info(remote.file_path).is_dir():
            raise NotImplementedError
        with create_tmp_file_path_for_archive(remote.file_path) as tmp_out:
            self.client.get_file(remote.file_path, tmp_out)
            out_dir = Path(output)
            out_dir.mkdir(parents=True, exist_ok=True)
            archive = remote.file_type(tmp_out)
            archive.extract_all(out_dir)


def download_if_missing(archive_name: str, output_directory: str | Path):
    output_directory = Path(output_directory)
    if output_directory.exists():
        return
    with Downloader() as d:
        d.download(archive_name, output_directory)
